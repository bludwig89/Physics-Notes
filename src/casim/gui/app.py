"""casim.gui.app — interactive viewer driven by a casim.engine Simulation.

Roadmap Phase E.  This grows ``ca-simulation/live_display.py`` (a vispy point
cloud with a hard-coded module-level step loop) into a program that consumes a
``Simulation``: the old controls become engine calls, and a Qt dock adds
scenario-aware controls (run/pause/step/run-to-tick, channel + threshold
selectors, live observer readouts, checkpoint save/load).

Heavy GUI deps (vispy, PyQt6) are imported lazily inside ``run()`` so that
``import casim.gui.app`` works headless (e.g. for syntax/import checks and for
the numpy-only ``render`` helpers).  Install them with ``pip install casim[gui]``.
"""
from __future__ import annotations

import copy
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

from ..engine import Simulation, LatticeSpec
from ..engine.channel import build_channel
from . import render

# ----------------------------------------------------------------------
# Defaults, scenario discovery, and memory estimation
# ----------------------------------------------------------------------

#: scenario used when the GUI is launched without one: a Weyl BCC packet.
DEFAULT_SCENARIO: Dict[str, Any] = {
    "name": "gui-default",
    "lattice": {"L": 32, "dims": 3, "topology": "bcc"},
    "channels": [{"type": "weyl_bcc", "sign": "+"}],
    "observers": [{"type": "norm_conservation", "every": 10}],
}

#: GUI-selectable lattice edge sizes (sites per edge, L x L x L).
LATTICE_PRESETS = [32, 48, 64, 96, 128, 192, 256, 384, 512, 768, 1024, 1536, 2048]

#: probe edge used to measure actual per-site state allocation.
_PROBE_L = 8
#: rough multiplier for step temporaries (FFT copies etc.) on top of the
#: resident state arrays.  Estimates are order-of-magnitude guides, not caps.
_MEM_OVERHEAD = 2.0


def _scenario_dir() -> Optional[Path]:
    """Locate the repository ``scenarios/`` folder (cwd first, then repo root)."""
    here = Path(__file__).resolve()
    candidates = [Path.cwd() / "scenarios"]
    if len(here.parents) >= 4:
        candidates.append(here.parents[3] / "scenarios")  # src/casim/gui/app.py
    for c in candidates:
        if c.is_dir():
            return c
    return None


def discover_scenarios() -> Dict[str, str]:
    """Return ``{label: path}`` for every scenario YAML found."""
    d = _scenario_dir()
    if d is None:
        return {}
    return {p.stem: str(p) for p in sorted(d.glob("*.yaml"))}


def estimate_bytes_per_site(channel_specs: List[Dict[str, Any]],
                            topology: str = "bcc", dims: int = 3) -> float:
    """Measured bytes of channel state per lattice site.

    Builds each channel on a tiny probe lattice (L=8), sums the ndarray bytes
    it actually allocates, and divides by the probe site count.  Channel state
    scales as L**dims, so this scales exactly to any edge size.  Channels that
    fail to build on the probe fall back to 32 B/site (one complex128 pair).
    """
    lat = LatticeSpec(L=_PROBE_L, dims=dims, topology=topology)
    rng = np.random.default_rng(0)
    total = 0
    for spec in channel_specs:
        nbytes = 0
        try:
            ch = build_channel(dict(spec))
            st = ch.init_state(lat, rng)
            if isinstance(st, dict):
                nbytes = sum(v.nbytes for v in st.values()
                             if isinstance(v, np.ndarray))
        except Exception:
            pass
        total += nbytes if nbytes else 32 * _PROBE_L ** dims
    return total / float(_PROBE_L ** dims)


def estimate_state_bytes(channel_specs: List[Dict[str, Any]], L: int,
                         topology: str = "bcc", dims: int = 3) -> float:
    """Rough resident memory for all channel states at edge size ``L``."""
    per_site = estimate_bytes_per_site(channel_specs, topology, dims)
    return per_site * float(L) ** dims * _MEM_OVERHEAD


def _fmt_mem(nbytes: float) -> str:
    gb = nbytes / 2**30
    if gb < 0.95:
        return f"~{max(gb * 1024, 1):.0f} MB"
    if gb < 10:
        return f"~{gb:.1f} GB"
    if gb < 1024:
        return f"~{gb:.0f} GB"
    return f"~{gb / 1024:.1f} TB"


def _scenario_of(sim: Simulation) -> Dict[str, Any]:
    """Round-trippable scenario dict describing a live Simulation."""
    return {
        "name": sim.name,
        "seed": sim.seed,
        "ticks": sim.target_ticks,
        "lattice": sim.lattice.to_dict(),
        "channels": [ch.spec() for ch in sim.channels.values()],
        "observers": [obs.spec() for obs in sim.observers],
    }


def _require_gui():
    try:
        import vispy  # noqa: F401
        from vispy import app, scene  # noqa: F401
        from PyQt6 import QtWidgets, QtCore  # noqa: F401
    except Exception as e:  # pragma: no cover
        raise ImportError(
            "The casim GUI needs the optional extra: pip install casim[gui] "
            f"(vispy + PyQt6). Import failed: {e}"
        )


def _default_simulation() -> Simulation:
    """A sensible default if no scenario is given: a Weyl BCC packet."""
    return Simulation.from_scenario(copy.deepcopy(DEFAULT_SCENARIO))


def simulation_from_scenario(path: Optional[str]) -> Simulation:
    if not path:
        return _default_simulation()
    from ..io import load_scenario
    return Simulation.from_scenario(load_scenario(path))


class Viewer:
    """vispy canvas + Qt control panel bound to a Simulation."""

    def __init__(self, sim: Simulation, steps_per_frame: int = 2,
                 pctile: float = 92.0, point_size: float = 5.0):
        _require_gui()
        from vispy import app, scene
        from PyQt6 import QtWidgets, QtCore

        self.sim = sim
        self.steps_per_frame = steps_per_frame
        self.pctile = pctile
        self.point_size = point_size
        self.running = False
        self.run_to: Optional[int] = None
        #: fields drawn as overlay clouds — every channel starts visible
        self.visible_channels = set(sim.channels)
        self._chan_markers: Dict[str, Any] = {}
        self._cloud_info: List[tuple] = []
        self.show_medium = True

        # --- Qt main window -------------------------------------------------
        self._app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        self.win = QtWidgets.QMainWindow()
        self.win.setWindowTitle(f"casim — {sim.name}")

        # vispy canvas as the central widget
        self.canvas = scene.SceneCanvas(keys="interactive", size=(960, 720),
                                        bgcolor="#04040c", show=False)
        self.view = self.canvas.central_widget.add_view()
        L = sim.lattice.L
        self.view.camera = scene.cameras.TurntableCamera(
            fov=38, azimuth=30, elevation=22, distance=L * 2.6)
        self._scene = scene
        self._add_axes(scene, L)
        # the lattice itself, drawn as a faint static substrate cloud
        self.medium = scene.visuals.Markers(parent=self.view.scene)
        self._medium_stride = 1
        self._refresh_medium()

        self.win.setCentralWidget(self.canvas.native)
        self._build_dock(QtWidgets, QtCore)

        # animation timer
        self.timer = app.Timer(interval=1 / 30, connect=self._on_frame, start=True)
        self._refresh_markers()
        self._refresh_readouts()

    # ------------------------------------------------------------------
    @staticmethod
    def _axes_pos(L):
        h = L / 2
        return np.array([[0, h, h], [L, h, h], [h, 0, h], [h, L, h],
                         [h, h, 0], [h, h, L]], dtype=np.float32)

    def _add_axes(self, scene, L):
        col = np.array([[1, .2, .2, .5]] * 2 + [[.2, 1, .2, .5]] * 2
                       + [[.3, .5, 1, .5]] * 2, dtype=np.float32)
        self._axes = scene.visuals.Line(
            pos=self._axes_pos(L), color=col,
            connect=np.array([[0, 1], [2, 3], [4, 5]]),
            parent=self.view.scene)

    def _build_dock(self, QtWidgets, QtCore):
        dock = QtWidgets.QDockWidget("controls", self.win)
        panel = QtWidgets.QWidget()
        lay = QtWidgets.QVBoxLayout(panel)

        # scenario selector
        lay.addWidget(QtWidgets.QLabel("scenario"))
        self.combo_scenario = QtWidgets.QComboBox()
        self._scenarios = discover_scenarios()
        self.combo_scenario.addItem("(current)")
        self.combo_scenario.addItems(list(self._scenarios))
        if self.sim.name in self._scenarios:
            self.combo_scenario.blockSignals(True)
            self.combo_scenario.setCurrentText(self.sim.name)
            self.combo_scenario.blockSignals(False)
        self.combo_scenario.currentTextChanged.connect(self._set_scenario)
        lay.addWidget(self.combo_scenario)

        # lattice size selector (rough state-memory estimate per option)
        lay.addWidget(QtWidgets.QLabel("lattice size (est. state memory)"))
        self.combo_lattice = QtWidgets.QComboBox()
        self._populate_lattice_combo()
        self.combo_lattice.currentIndexChanged.connect(self._set_lattice_size)
        lay.addWidget(self.combo_lattice)

        # run / pause / step
        row = QtWidgets.QHBoxLayout()
        self.btn_run = QtWidgets.QPushButton("Run")
        self.btn_run.clicked.connect(self._toggle_run)
        btn_step = QtWidgets.QPushButton("Step")
        btn_step.clicked.connect(lambda: self._do_steps(1))
        row.addWidget(self.btn_run); row.addWidget(btn_step)
        lay.addLayout(row)

        # run-to-tick
        rrow = QtWidgets.QHBoxLayout()
        rrow.addWidget(QtWidgets.QLabel("run to tick"))
        self.spin_target = QtWidgets.QSpinBox()
        self.spin_target.setMaximum(10_000_000)
        self.spin_target.setValue(max(self.sim.target_ticks, 200))
        btn_to = QtWidgets.QPushButton("Go")
        btn_to.clicked.connect(self._run_to_tick)
        rrow.addWidget(self.spin_target); rrow.addWidget(btn_to)
        lay.addLayout(rrow)

        # lattice medium toggle + field overlay checkboxes
        self.box_medium = QtWidgets.QCheckBox("lattice medium")
        self.box_medium.setChecked(self.show_medium)
        self.box_medium.toggled.connect(self._toggle_medium)
        lay.addWidget(self.box_medium)

        lay.addWidget(QtWidgets.QLabel("fields"))
        self.chan_box_lay = QtWidgets.QVBoxLayout()
        self.chan_boxes: Dict[str, Any] = {}
        lay.addLayout(self.chan_box_lay)
        self._build_channel_boxes(QtWidgets)

        # density threshold
        lay.addWidget(QtWidgets.QLabel("density threshold (pctile)"))
        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.setRange(50, 99); self.slider.setValue(int(self.pctile))
        self.slider.valueChanged.connect(self._set_pctile)
        lay.addWidget(self.slider)

        # checkpoint save/load
        crow = QtWidgets.QHBoxLayout()
        btn_save = QtWidgets.QPushButton("Checkpoint")
        btn_save.clicked.connect(self._save_checkpoint)
        btn_load = QtWidgets.QPushButton("Resume…")
        btn_load.clicked.connect(self._load_checkpoint)
        crow.addWidget(btn_save); crow.addWidget(btn_load)
        lay.addLayout(crow)

        # readouts
        self.readout = QtWidgets.QLabel("")
        # Use the platform's real fixed-pitch font instead of the CSS generic
        # "monospace" keyword: the keyword forces Qt to populate font-family
        # aliases across every installed font (the ~117 ms startup warning).
        from PyQt6 import QtGui
        self.readout.setFont(
            QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.SystemFont.FixedFont)
        )
        lay.addWidget(self.readout)

        # per-particle / per-field sidebar (roadmap P3) — fed verbatim from
        # each channel's observables() via casim.gui.sidebar, so the live
        # readouts are the engine's own readouts.
        lay.addWidget(QtWidgets.QLabel("particles / fields"))
        self.sidebar = QtWidgets.QLabel("")
        self.sidebar.setFont(
            QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.SystemFont.FixedFont)
        )
        self.sidebar.setWordWrap(True)
        lay.addWidget(self.sidebar)
        lay.addStretch(1)

        dock.setWidget(panel)
        self.win.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, dock)

    # ------------------------------------------------------------------
    # scenario / lattice-size handling
    def _populate_lattice_combo(self):
        """Fill the lattice dropdown; memory labels reflect current channels."""
        lat = self.sim.lattice
        specs = [ch.spec() for ch in self.sim.channels.values()]
        per_site = estimate_bytes_per_site(specs, lat.topology, lat.dims)
        sizes = sorted(set(LATTICE_PRESETS) | {lat.L})
        self.combo_lattice.blockSignals(True)
        self.combo_lattice.clear()
        for L in sizes:
            est = per_site * float(L) ** lat.dims * _MEM_OVERHEAD
            self.combo_lattice.addItem(
                f"{L} x {L} x {L}  ({_fmt_mem(est)})", L)
        self.combo_lattice.setCurrentIndex(sizes.index(lat.L))
        self.combo_lattice.blockSignals(False)

    def _set_lattice_size(self, idx):
        L = self.combo_lattice.itemData(idx)
        if L is None or int(L) == self.sim.lattice.L:
            return
        scen = _scenario_of(self.sim)
        scen["lattice"]["L"] = int(L)
        self._swap_sim(Simulation.from_scenario(scen))

    def _set_scenario(self, label):
        path = self._scenarios.get(label)
        if not path:
            return
        from ..io import load_scenario
        self._swap_sim(Simulation.from_scenario(load_scenario(path)))

    def _swap_sim(self, sim):
        """Replace the running Simulation and resync every control."""
        from PyQt6 import QtWidgets
        self.running = False
        self.run_to = None
        self.btn_run.setText("Run")
        self.sim = sim
        # drop the old per-channel visuals and start with all fields visible
        for mk in self._chan_markers.values():
            mk.parent = None
        self._chan_markers = {}
        self.visible_channels = set(sim.channels)
        self._build_channel_boxes(QtWidgets)
        self._populate_lattice_combo()
        L = sim.lattice.L
        self._axes.set_data(pos=self._axes_pos(L))
        self._refresh_medium()
        self.view.camera.distance = L * 2.6
        self.win.setWindowTitle(f"casim — {sim.name}")
        self._refresh_markers()
        self._refresh_readouts()

    # ------------------------------------------------------------------
    # medium + field-overlay handling
    def _chan_tint(self, name):
        idx = list(self.sim.channels).index(name)
        return render.CHANNEL_TINTS[idx % len(render.CHANNEL_TINTS)]

    def _build_channel_boxes(self, QtWidgets):
        """One checkbox per channel, tinted to match its overlay cloud."""
        while self.chan_box_lay.count():
            w = self.chan_box_lay.takeAt(0).widget()
            if w is not None:
                w.deleteLater()
        self.chan_boxes = {}
        for name in self.sim.channels:
            box = QtWidgets.QCheckBox(name)
            box.setChecked(name in self.visible_channels)
            r, g, b = (int(c * 255) for c in self._chan_tint(name))
            box.setStyleSheet(f"color: rgb({r},{g},{b});")
            box.toggled.connect(
                lambda on, n=name: self._toggle_channel(n, on))
            self.chan_box_lay.addWidget(box)
            self.chan_boxes[name] = box

    def _toggle_medium(self, on):
        self.show_medium = bool(on)
        self.medium.visible = self.show_medium
        self.canvas.update()

    def _toggle_channel(self, name, on):
        if on:
            self.visible_channels.add(name)
            self._refresh_channel(name)     # compute only this field
        else:
            self.visible_channels.discard(name)
            mk = self._chan_markers.get(name)
            if mk is not None:
                mk.visible = False
            self._cloud_info = [t for t in self._cloud_info if t[0] != name]
        self.canvas.update()
        self._refresh_readouts()

    def _refresh_medium(self):
        """Static substrate cloud; recomputed only when the lattice changes."""
        lat = self.sim.lattice
        coords, colours, self._medium_stride = render.lattice_medium(
            lat.L, lat.topology)
        self.medium.set_data(coords, edge_color=None, face_color=colours,
                             size=2.5, edge_width=0)
        self.medium.visible = self.show_medium

    def _refresh_channel(self, name):
        """Recompute one field's overlay cloud.  Returns (dmax, npts) or None."""
        ch = self.sim.channels[name]
        try:
            vol = ch.density_field(self.sim.states[name])
        except Exception:
            # channel has no 3-D scalar density (e.g. gauge_mc) — disable it
            self.visible_channels.discard(name)
            box = self.chan_boxes.get(name)
            if box is not None:
                box.blockSignals(True)
                box.setChecked(False)
                box.setEnabled(False)
                box.setToolTip("channel has no 3-D density field")
                box.blockSignals(False)
            return None
        coords, colours, dmax, _total = render.point_cloud(
            vol, self.pctile, tint=self._chan_tint(name))
        mk = self._chan_markers.get(name)
        if mk is None:
            mk = self._scene.visuals.Markers(parent=self.view.scene)
            self._chan_markers[name] = mk
        if len(coords):
            mk.set_data(coords, edge_color=None, face_color=colours,
                        size=self.point_size, edge_width=0)
            mk.visible = True
        else:
            mk.visible = False
        info = (name, dmax, len(coords))
        self._cloud_info = [t for t in self._cloud_info if t[0] != name] + [info]
        return info

    # ------------------------------------------------------------------
    # engine-call handlers (the old keyboard controls, now buttons)
    def _toggle_run(self):
        self.running = not self.running
        self.btn_run.setText("Pause" if self.running else "Run")

    def _do_steps(self, n):
        self.sim.step(n)
        self._refresh_markers(); self._refresh_readouts()

    def _run_to_tick(self):
        self.run_to = int(self.spin_target.value())
        self.running = True
        self.btn_run.setText("Pause")

    def _set_pctile(self, v):
        self.pctile = float(v)
        self._refresh_markers()

    def _save_checkpoint(self):
        path = self.sim.checkpoint(os.path.join(
            self.sim.checkpoint_dir, f"{self.sim.name}_t{self.sim.tick}.npz"))
        self.readout.setText(self.readout.text() + f"\nsaved {os.path.basename(path)}")

    def _load_checkpoint(self):
        from PyQt6 import QtWidgets
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.win, "Resume checkpoint", "", "NPZ (*.npz)")
        if path:
            self._swap_sim(Simulation.resume(path))

    # ------------------------------------------------------------------
    def _on_frame(self, event):
        if not self.running:
            return
        self._do_steps(self.steps_per_frame)
        if self.run_to is not None and self.sim.tick >= self.run_to:
            self.running = False
            self.run_to = None
            self.btn_run.setText("Run")

    def _refresh_markers(self):
        """Recompute the overlay clouds of *visible* fields only.

        Hidden fields cost nothing (no density_field, no percentile, no GPU
        upload) — that is the main resource lever when several channels run
        on a large lattice.  The medium cloud is static and untouched here.
        """
        for name in self.sim.channels:
            if name in self.visible_channels:
                self._refresh_channel(name)
            else:
                mk = self._chan_markers.get(name)
                if mk is not None:
                    mk.visible = False
        self.canvas.update()

    def _refresh_readouts(self):
        lat = self.sim.lattice
        med = f"medium {lat.L}³ {lat.topology}"
        if self._medium_stride > 1:
            med += f" (1/{self._medium_stride} sampled)"
        lines = [f"tick   {self.sim.tick}", med]
        for c, e in self.sim.state_norms().items():
            e0 = self.sim._energy0.get(c, e)
            drift = abs(e - e0) / e0 if e0 else 0.0
            lines.append(f"{c[:10]:10s} E={e:.4g} drift={drift:.1e}")
        for name, dmax, npts in self._cloud_info:
            lines.append(f"{name[:10]:10s} peak={dmax:.3g} pts={npts}")
        self.readout.setText("\n".join(lines))
        # P3 sidebar: per-particle + per-field panels from observables()
        if hasattr(self, "sidebar"):
            from .sidebar import sidebar_text
            self.sidebar.setText(sidebar_text(self.sim))

    def show(self):
        self.canvas.show()
        self.win.show()

    def run(self):  # pragma: no cover (needs a display)
        from vispy import app
        self.show()
        app.run()


def run(scenario_path: Optional[str] = None):  # pragma: no cover
    """Launch the GUI for a scenario (or the default Weyl packet)."""
    _require_gui()
    sim = simulation_from_scenario(scenario_path)
    Viewer(sim).run()

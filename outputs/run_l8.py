import os, sys, traceback
sys.path.insert(0, os.path.join("/sessions/jolly-upbeat-meitner/mnt/Physics Notes","tests","findings"))
import test_F195_blockspin_element_atom as T
for n in ["test_L8_tierB_helium_live_quarks","test_L9_hydrogen_consistent"]:
    try:
        getattr(T,n)(); print(n,"PASS",flush=True)
    except Exception as e:
        print(n,"FAIL",e,flush=True); traceback.print_exc()

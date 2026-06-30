import os,sys
sys.path.insert(0,"/sessions/jolly-upbeat-meitner/mnt/Physics Notes/ca-simulation")
import ca_manybody as mb
# NIST first ionization energies (eV) Z=1..18 (NIST ASD)
NIST={1:13.598,2:24.587,3:5.392,4:9.323,5:8.298,6:11.260,7:14.534,8:13.618,
9:17.423,10:21.565,11:5.139,12:7.646,13:5.986,14:8.152,15:10.487,16:10.360,
17:12.968,18:15.760}
print(f"{'Z':>2} {'cfg':>4} {'IE_model':>9} {'IE_NIST':>8} {'err%':>7} {'conv':>5}")
for Z in range(1,19):
    r=mb.electron_cloud_hartree(Z)
    ie=r['ionization_eV']; nist=NIST[Z]; err=100*(ie-nist)/nist
    print(f"{Z:>2} {str(r['configuration'][-1][1]):>4} {ie:9.3f} {nist:8.3f} {err:7.1f} {str(r['converged']):>5}")

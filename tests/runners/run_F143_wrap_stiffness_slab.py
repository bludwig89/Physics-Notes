"""F139 — slab-chunked version: partial BZ sums over kx in [i0,i1)."""
import numpy as np, json, sys
L  = int(sys.argv[1]); m = float(sys.argv[2]); n = int(sys.argv[3])
i0 = int(sys.argv[4]); i1 = int(sys.argv[5]); out = sys.argv[6]
ir3 = 1.0/np.sqrt(3.0)
k1 = 2*np.pi*((np.arange(L)-L//2)+0.5)/L
q  = 2*np.pi*n/L
# extended slab rows (wrap indices mod L)
rows_ext = np.arange(i0-n, i1+n) % L
kx_e = k1[rows_ext]
KX,KY,KZ = np.meshgrid(kx_e,k1,k1,indexing='ij')
def Kmat(kx,ky,kz):
    out_ = np.zeros(kx.shape+(4,4),complex)
    for blk,s in ((0,1.0),(1,-1.0)):
        cx,cy,cz = np.cos(kx*ir3),np.cos(ky*ir3),np.cos(kz*ir3)
        sx,sy,sz = np.sin(kx*ir3),np.sin(ky*ir3),np.sin(kz*ir3)
        u  = cx*cy*cz + s*sx*sy*sz
        nx =  sx*cy*cz - s*cx*sy*sz
        ny = -s*cx*sy*cz + sx*cy*sz
        nz =  cx*cy*sz + s*sx*sy*cz
        o = 2*blk
        out_[...,o+0,o+0]=u-1j*nz;        out_[...,o+0,o+1]=-1j*(nx-1j*ny)
        out_[...,o+1,o+0]=-1j*(nx+1j*ny); out_[...,o+1,o+1]=u+1j*nz
    return out_
c,s = np.cos(m/2), np.sin(m/2); I2 = np.eye(2)
M0 = np.block([[c*I2,-1j*s*I2],[-1j*s*I2,c*I2]])
Mp = np.block([[0*I2,  s*I2],[-s*I2, 0*I2]])
Mpp= np.block([[0*I2,1j*s*I2],[1j*s*I2,0*I2]])
K0 = Kmat(KX,KY,KZ)
U0 = np.einsum('ab,...bc,cd->...ad',M0,K0,M0)
lam,vec = np.linalg.eig(U0); th = np.angle(lam)
NE = i1-i0  # interior rows start at index n .. n+NE
sl  = slice(n, n+NE)
Kp  = K0[2*n:2*n+NE] if False else K0[sl.start+n:sl.start+n+NE]   # k+q rows
Km  = K0[sl.start-n:sl.start-n+NE]
K0i = K0[sl]; lami,veci,thi = lam[sl],vec[sl],th[sl]
lam_p,vec_p = lam[sl.start+n:sl.start+n+NE], vec[sl.start+n:sl.start+n+NE]
lam_m,vec_m = lam[sl.start-n:sl.start-n+NE], vec[sl.start-n:sl.start-n+NE]
D = 0.25*(np.einsum('ab,...bc,cd->...ad',Mpp,K0i,M0)
        + np.einsum('ab,...bc,cd->...ad',M0,K0i,Mpp)
        + np.einsum('ab,...bc,cd->...ad',Mp,Kp,Mp)
        + np.einsum('ab,...bc,cd->...ad',Mp,Km,Mp))
vH = veci.conj().transpose(0,1,2,4,3)
l2 = np.einsum('...na,...ab,...bn->...n', vH, D, veci)
for (Kq,lamq,vecq) in ((Kp,lam_p,vec_p),(Km,lam_m,vec_m)):
    Bf = 0.5*(np.einsum('ab,...bc,cd->...ad',Mp,K0i,M0)
            + np.einsum('ab,...bc,cd->...ad',M0,Kq,Mp))
    Bb = 0.5*(np.einsum('ab,...bc,cd->...ad',Mp,Kq,M0)
            + np.einsum('ab,...bc,cd->...ad',M0,K0i,Mp))
    vqH = vecq.conj().transpose(0,1,2,4,3)
    tf = np.einsum('...ma,...ab,...bn->...mn', vqH, Bf, veci)
    tb = np.einsum('...na,...ab,...bm->...nm', vH,  Bb, vecq)
    dl = lami[...,:,None]-lamq[...,None,:]
    num = tb*tf.transpose(0,1,2,4,3)
    mask = np.abs(dl)>1e-9
    l2 += np.where(mask,num/np.where(mask,dl,1.0),0.0).sum(-1)
dth = np.imag(l2/lami)
Pi_part = -(2.0/L**3)*np.sum(np.sign(thi)*dth)
json.dump({"L":L,"m":m,"n":n,"i0":i0,"i1":i1,"Pi_part":float(Pi_part)},open(out,"w"))
print(out, Pi_part)

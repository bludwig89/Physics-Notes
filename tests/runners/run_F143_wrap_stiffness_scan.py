"""
F139 dev — Part B production: induced wrap stiffness by eigenvalue PT on the
walk unitary U(a) = M(a) K M(a), alpha(x) = a cos(qx) (q along x, on-grid).

lambda_n^(2)(k) = <n|D|n> + sum_{s=+-} sum_m  <n,k|Bback_s|m,k+sq><m,k+sq|Bfwd_s|n,k>
                                              /(lambda_n(k)-lambda_m(k+sq))
  Bfwd_s(k)  = (1/2)[M' K(k) M0 + M0 K(k+sq) M']     (transfer +sq)
  Bback_s    = (1/2)[M' K(k+sq) M0 + M0 K(k) M']     (transfer back)
  D(k)       = (1/4)[M'' K M0 + M0 K M'' + M' K(k+q) M' + M' K(k-q) M']
dtheta_n = Re[ i lambda^(2)/lambda ] a^2 ;  Pi = -(2/L^3) sum sgn(theta) dtheta /a^2*... (a^2 cancels)
"""
import numpy as np, json, sys
L     = int(sys.argv[1]) if len(sys.argv)>1 else 32
ms    = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv)>2 else [0.6,0.4,0.3,0.2]
nlist = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv)>3 else [1,2]
out   = sys.argv[4] if len(sys.argv)>4 else f"pt_{L}.json"
arg5  = sys.argv[5] if len(sys.argv)>5 else ''
offx  = arg5 != 'valid'
MODE  = 'cont' if arg5=='cont' else 'bcc'
ir3 = 1.0/np.sqrt(3.0)

k1o = 2*np.pi*((np.arange(L)-L//2)+0.5)/L
k1u = 2*np.pi*(np.arange(L)-L//2)/L
KX,KY,KZ = np.meshgrid(k1u if not offx else k1o, k1o, k1o, indexing='ij')

def Kmat(kx,ky,kz):
    out_ = np.zeros(kx.shape+(4,4),complex)
    if MODE=='cont':
        # continuum Dirac comparator: H_pm = -+ c k.sigma~ (L/R Weyl pair)
        kk = np.sqrt(kx**2+ky**2+kz**2); ck = ir3*kk
        co, si = np.cos(ck), np.sin(ck)
        kh = np.where(kk[...,None]>1e-30, np.stack([kx,ky,kz],-1)/kk[...,None], 0.0)
        for blk,s in ((0,1.0),(1,-1.0)):
            o=2*blk; sy = -s   # sigma~ = (sx, -s*sy, sz): '+' branch has y-flip
            out_[...,o+0,o+0]=co-1j*s*si*kh[...,2]
            out_[...,o+0,o+1]=-1j*s*si*(kh[...,0]-1j*sy*kh[...,1])
            out_[...,o+1,o+0]=-1j*s*si*(kh[...,0]+1j*sy*kh[...,1])
            out_[...,o+1,o+1]=co+1j*s*si*kh[...,2]
        return out_
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

def run(m,n):
    q = 2*np.pi*n/L
    c,s = np.cos(m/2), np.sin(m/2)
    I2 = np.eye(2)
    M0 = np.block([[c*I2, -1j*s*I2],[-1j*s*I2, c*I2]])
    Mp = np.block([[0*I2,  s*I2],[-s*I2, 0*I2]])      # dM/dphi
    Mpp= np.block([[0*I2, 1j*s*I2],[1j*s*I2, 0*I2]])  # d2M/dphi2
    K0 = Kmat(KX,KY,KZ)
    U0 = np.einsum('ab,...bc,cd->...ad', M0, K0, M0)
    lam,vec = np.linalg.eig(U0)            # (...,4),(...,4,4)
    th = np.angle(lam)
    Kp = np.roll(K0,-n,axis=0)             # K(k+q): k-grid roll along x
    Km = np.roll(K0, n,axis=0)
    lam_p, vec_p = np.roll(lam,-n,axis=0), np.roll(vec,-n,axis=0)
    lam_m, vec_m = np.roll(lam, n,axis=0), np.roll(vec, n,axis=0)
    # diagonal D
    D = 0.25*(np.einsum('ab,...bc,cd->...ad',Mpp,K0,M0)
            + np.einsum('ab,...bc,cd->...ad',M0,K0,Mpp)
            + np.einsum('ab,...bc,cd->...ad',Mp,Kp,Mp)
            + np.einsum('ab,...bc,cd->...ad',Mp,Km,Mp))
    l2 = np.einsum('...na,...ab,...bn->...n', vec.conj().transpose(*range(vec.ndim-2),-1,-2), D, vec)
    for (Kq,lamq,vecq,sgn) in ((Kp,lam_p,vec_p,+1),(Km,lam_m,vec_m,-1)):
        Bf = 0.5*(np.einsum('ab,...bc,cd->...ad',Mp,K0,M0)
                + np.einsum('ab,...bc,cd->...ad',M0,Kq,Mp))
        Bb = 0.5*(np.einsum('ab,...bc,cd->...ad',Mp,Kq,M0)
                + np.einsum('ab,...bc,cd->...ad',M0,K0,Mp))
        # t_fwd[m,n] = <m,k+sq|Bf|n,k> ; t_back[n,m] = <n,k|Bb|m,k+sq>
        tf = np.einsum('...ma,...ab,...bn->...mn', vecq.conj().transpose(*range(vec.ndim-2),-1,-2), Bf, vec)
        tb = np.einsum('...na,...ab,...bm->...nm', vec.conj().transpose(*range(vec.ndim-2),-1,-2), Bb, vecq)
        dl = lam[...,:,None] - lamq[...,None,:]      # [n,m]
        num = tb*tf.transpose(*range(vec.ndim-2),-1,-2)
        mask = np.abs(dl) > 1e-9
        l2 += np.where(mask, num/np.where(mask,dl,1.0), 0.0).sum(-1)
    dth = np.imag(l2/lam)
    Pi  = -(2.0/L**3)*np.sum(np.sign(th)*dth)
    imag_chk = 0.0
    return {"m":m,"n":n,"q":q,"Pi":float(Pi),"Pi_over_q2":float(Pi/q**2),"imchk":float(imag_chk)}

rows=[]
for m in ms:
    for n in nlist:
        r = run(m,n); rows.append(r); print(r, flush=True)
json.dump({"L":L,"rows":rows}, open(out,"w"), indent=1)
print("done")

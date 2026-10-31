# 7 s 8-bit loop for designed stories: 120 BPM, jump at 1.2 s, block hit + coin at 1.6 s, pops on title/button
import numpy as np, wave, sys
SR=44100; DUR=7.0; N=int(SR*DUR); out=sys.argv[1] if len(sys.argv)>1 else 'story.wav'
rng=np.random.default_rng(4); buf=np.zeros(N)
def hz(m): return 440*2**((m-69)/12)
def t_(d): return np.arange(int(SR*d))/SR
def pulse(f,d,duty=0.25): return np.where((t_(d)*f)%1<duty,1.0,-1.0)
def tri(f,d): x=(t_(d)*f)%1; return 4*np.abs(x-0.5)-1
def noise(d): n=int(SR*d); return np.repeat(rng.uniform(-1,1,n//4+1),4)[:n]
def env(x,a=0.003,dec=None):
    n=len(x);e=np.ones(n);na=max(1,int(a*SR));e[:na]=np.linspace(0,1,na)
    if dec: e*=np.exp(-np.arange(n)/SR/dec)
    r=min(n,int(0.01*SR));e[-r:]*=np.linspace(1,0,r);return x*e
def add(t,x,g):
    i=int(t*SR);j=min(N,i+len(x));buf[i:j]+=g*x[:j-i]
def kick(): t=t_(0.2);f=50+120*np.exp(-t*30);return env(np.sin(2*np.pi*np.cumsum(f)/SR),0.001,0.08)
def hat(): x=noise(0.04);x=x-np.concatenate([[0],x[:-1]]);return env(x,0.0005,0.01)*0.5
def blip(m,d=0.06,duty=0.5): return env(pulse(hz(m),d,duty),0.001,d/2)
CH=[57,53,48,55]; MEL=[69,72,76,72,74,72,69,67,65,69,72,69,74,72,69,72]
for b in range(14):
    t=b*0.5; add(t,kick(),0.8); add(t+0.25,hat(),0.3)
    root=CH[(b//4)%4]; add(t,env(tri(hz(root-12),0.22),0.002,0.12),0.55); add(t+0.25,env(tri(hz(root),0.22),0.002,0.12),0.5)
    for h in (0,0.25): add(t+h,env(pulse(hz(MEL[(b*2+(1 if h else 0))%16]),0.2,0.25),0.003,0.12),0.15)
sfx=np.zeros(N)
def addS(t,x,g):
    i=int(t*SR);j=min(N,i+len(x));sfx[i:j]+=g*x[:j-i]
ph=np.cumsum(hz(64)*(1+1.2*t_(0.18)/0.18))/SR; addS(1.2,env(np.where(ph%1<0.5,1.,-1.),0.002,0.09),0.7)   # jump
addS(1.6,env(noise(0.08),0.001,0.03),0.6)                                                                  # block hit
addS(1.62,np.concatenate([blip(83,0.06),env(pulse(hz(88),0.25,0.5),0.001,0.1)]),0.8)                       # coin
for t,m in ((0.13,76),(0.47,79),(2.4,84)): addS(t,blip(m,0.08),0.5)
buf/=np.max(np.abs(buf)); sfx/=np.max(np.abs(sfx)); mix=buf+0.6*sfx
mix[-int(0.3*SR):]*=np.linspace(1,0,int(0.3*SR)); mix=np.tanh(mix*1.1); mix*=0.85/np.max(np.abs(mix))
pcm=(mix*32767).astype(np.int16)
with wave.open(out,'wb') as w: w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.stack([pcm,pcm],1).ravel().tobytes())

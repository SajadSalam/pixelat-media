# 8-bit soundtrack for animated highlight stories: 120 BPM loop + SFX on each story's events.
#   python3 highlight_audio.py <storyId> <seconds> <out.wav>
import numpy as np, wave, sys
sid, DUR, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
SR=44100; N=int(SR*DUR); rng=np.random.default_rng(4); mus=np.zeros(N); sfx=np.zeros(N)
hz=lambda m:440*2**((m-69)/12); T=lambda d:np.arange(int(SR*d))/SR
def pulse(f,d,duty=.25): return np.where((T(d)*f)%1<duty,1.,-1.)
def tri(f,d): x=(T(d)*f)%1; return 4*np.abs(x-.5)-1
def noise(d): n=int(SR*d); return np.repeat(rng.uniform(-1,1,n//4+1),4)[:n]
def env(x,a=.003,dec=None):
    n=len(x);e=np.ones(n);na=max(1,int(a*SR));e[:na]=np.linspace(0,1,na)
    if dec: e*=np.exp(-np.arange(n)/SR/dec)
    r=min(n,int(.01*SR));e[-r:]*=np.linspace(1,0,r);return x*e
def add(buf,t,x,g):
    i=int(t*SR);j=min(N,i+len(x))
    if i<N: buf[i:j]+=g*x[:j-i]
def kick(): t=T(.2);f=50+120*np.exp(-t*30);return env(np.sin(2*np.pi*np.cumsum(f)/SR),.001,.08)
def hat(): x=noise(.04);x=x-np.concatenate([[0],x[:-1]]);return env(x,.0005,.01)*.5
def blip(m,d=.06,duty=.5): return env(pulse(hz(m),d,duty),.001,d/2)
def sweep(m0,m1,d,duty=.5):
    f=hz(m0)*(hz(m1)/hz(m0))**(T(d)/d);ph=np.cumsum(f)/SR;return env(np.where(ph%1<duty,1.,-1.),.002,d/1.5)
# music: intro bar is lighter (no kick), full groove after 1 s
CH=[57,53,48,55]; MEL=[69,72,76,72,74,72,69,67,65,69,72,69,74,72,69,72]
for b in range(int(DUR*2)):
    t=b*.5; full=t>=1.0
    if full: add(mus,t,kick(),.8)
    add(mus,t+.25,hat(),.3 if full else .18)
    root=CH[(b//4)%4]; add(mus,t,env(tri(hz(root-12),.22),.002,.12),.55); add(mus,t+.25,env(tri(hz(root),.22),.002,.12),.5)
    if full:
        for h in (0,.25): add(mus,t+h,env(pulse(hz(MEL[(b*2+(1 if h else 0))%16]),.2,.25),.003,.12),.15)
F=lambda f:f/30
EV={'about-1':[
    *[(F(2+k*3),'blip',84+[0,3,7,12,7,3,0,5,9,12][k]) for k in range(10)],  # logo assembling, right to left
    (F(30),'pop',79),(F(40),'pop',84),
    (F(36),'thud',0),(F(44),'zap',0),(F(50),'blip',88),(F(56),'chirp',0),(F(60),'honk',0),
    (F(74),'fall',0),(F(84),'land',0),(F(85),'coin',0),(F(92),'pop',88)]}
for t,kind,m in EV.get(sid,[]):
    if kind=='blip': add(sfx,t,blip(m,.05),.45)
    elif kind=='pop': add(sfx,t,blip(m,.09),.6)
    elif kind=='thud': add(sfx,t,env(noise(.07),.001,.02),.5); add(sfx,t,kick(),.6)
    elif kind=='zap': add(sfx,t,sweep(60,96,.18,.25),.45)
    elif kind=='chirp': add(sfx,t,np.concatenate([blip(91,.04),blip(96,.05)]),.4)
    elif kind=='honk': add(sfx,t,env(pulse(hz(55),.22,.4),.002,.12),.5); add(sfx,t+.08,env(pulse(hz(58),.18,.4),.002,.1),.35)
    elif kind=='fall': add(sfx,t,sweep(91,72,.3),.35)
    elif kind=='land': add(sfx,t,env(noise(.06),.001,.02),.55)
    elif kind=='coin': add(sfx,t,np.concatenate([blip(83,.06),env(pulse(hz(88),.25,.5),.001,.1)]),.6)
mus/=np.max(np.abs(mus)); sfx/=max(1e-9,np.max(np.abs(sfx))); mix=mus+.6*sfx
mix[:int(.02*SR)]*=np.linspace(0,1,int(.02*SR)); mix[-int(.4*SR):]*=np.linspace(1,0,int(.4*SR))
mix=np.tanh(mix*1.1); mix*=.85/np.max(np.abs(mix))
pcm=(mix*32767).astype(np.int16)
with wave.open(out,'wb') as w: w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.stack([pcm,pcm],1).ravel().tobytes())
print('peak',round(float(np.max(np.abs(mix))),3))

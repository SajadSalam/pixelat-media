# 5 s 8-bit loop for the pixel-run story: 120 BPM, a rising coin blip on each of the 12 pixels
import numpy as np, wave, sys
SR=44100; DUR=5.0; N=int(SR*DUR); out=sys.argv[1]
buf=np.zeros(N); sfx=np.zeros(N)
hz=lambda m:440*2**((m-69)/12)
t_=lambda d:np.arange(int(SR*d))/SR
pulse=lambda f,d,duty=.25:np.where((t_(d)*f)%1<duty,1.,-1.)
tri=lambda f,d:4*np.abs((t_(d)*f)%1-.5)-1
def env(x,a=.002,dec=None):
    n=len(x);e=np.ones(n);e[:max(1,int(a*SR))]=np.linspace(0,1,max(1,int(a*SR)))
    if dec:e*=np.exp(-np.arange(n)/SR/dec)
    r=min(n,int(.01*SR));e[-r:]*=np.linspace(1,0,r);return x*e
def add(b,t,x,g):
    i=int(t*SR);j=min(N,i+len(x));b[i:j]+=g*x[:j-i]
def kick():
    t=t_(.2);f=50+120*np.exp(-t*30);return env(np.sin(2*np.pi*np.cumsum(f)/SR),.001,.08)
ROOT=[45,45,41,43]
for b in range(10):
    t=b*.5;add(buf,t,kick(),.8)
    r=ROOT[(b//2)%4];add(buf,t,env(tri(hz(r),.22),.002,.12),.55);add(buf,t+.25,env(tri(hz(r+12),.22),.002,.12),.5)
SC=[72,74,76,79,81,84,86,88,91,93,96,98]
for i,m in enumerate(SC):
    t=(12+7*i)/30;add(sfx,t,env(pulse(hz(m),.09,.5),.001,.04),.7)
add(sfx,92/30,env(pulse(hz(84),.14,.5),.001,.08),.7);add(sfx,92/30+.1,env(pulse(hz(91),.3,.5),.001,.12),.8)
buf/=np.max(np.abs(buf));sfx/=np.max(np.abs(sfx));mix=buf+.6*sfx
mix[-int(.25*SR):]*=np.linspace(1,0,int(.25*SR));mix=np.tanh(mix*1.1);mix*=.85/np.max(np.abs(mix))
pcm=(mix*32767).astype(np.int16)
with wave.open(out,'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.stack([pcm,pcm],1).ravel().tobytes())

import numpy as np, wave
SR=44100; DUR=20.0; N=int(SR*DUR); BEAT=0.5
rng=np.random.default_rng(19); music=np.zeros(N); sfx=np.zeros(N)
def hz(m): return 440*2**((m-69)/12)
def t_(d): return np.arange(int(SR*d))/SR
def pulse(f,d,duty=0.25): return np.where((t_(d)*f)%1<duty,1.0,-1.0)
def tri(f,d): x=(t_(d)*f)%1; return 4*np.abs(x-0.5)-1
def noise(d): n=int(SR*d); return np.repeat(rng.uniform(-1,1,n//4+1),4)[:n]
def env(x,a=0.003,dec=None):
    n=len(x);e=np.ones(n);na=max(1,int(a*SR));e[:na]=np.linspace(0,1,na)
    if dec: e*=np.exp(-np.arange(n)/SR/dec)
    r=min(n,int(0.01*SR));e[-r:]*=np.linspace(1,0,r);return x*e
def add(buf,t,x,g=1.0):
    i=int(round(t*SR));j=min(N,i+len(x))
    if 0<=i<N: buf[i:j]+=g*x[:j-i]
def kick(): t=t_(0.22);f=50+120*np.exp(-t*30);return env(np.sin(2*np.pi*np.cumsum(f)/SR),0.001,0.09)
def snare(): return env(noise(0.18),0.001,0.05)*0.8+env(tri(190,0.18),0.001,0.04)*0.4
def hat(): x=noise(0.05);x=x-np.concatenate([[0],x[:-1]]);return env(x,0.0005,0.012)*0.5
def crash(d=1.4): x=noise(d);x=x-np.concatenate([[0],x[:-1]]);return env(x,0.001,0.45)*0.5
def blip(m,d=0.07,duty=0.5): return env(pulse(hz(m),d,duty),0.001,d/2)
def sweep(m0,m1,d,duty=0.5): t=t_(d);f=hz(m0)*(hz(m1)/hz(m0))**(t/d);ph=np.cumsum(f)/SR;return env(np.where(ph%1<duty,1.,-1.),0.002,d/2)
def whoosh(d): x=noise(d);return x*np.sin(np.linspace(0,np.pi,len(x)))*0.6
F=lambda fr: fr/30
PENT=[69,72,74,76,79,81,84,86,88,91]
CH=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]
MEL=[[69,72,76,72,74,72,69,67],[65,69,72,69,74,72,69,72],[67,72,76,79,76,72,74,76],[74,71,67,71,74,76,74,71]]

# 0–3 s: hook — notes on the beats, DM pops, riser into the drop
for k in range(6): add(sfx,k*0.5,blip(PENT[k],0.09,0.25),0.6)
add(sfx,F(0),sweep(60,72,0.2),0.35); add(sfx,F(8),sweep(64,76,0.2),0.35)
add(sfx,F(12),sweep(84,60,0.3,0.25),0.35)
for i,fr in enumerate((28,43,58,73)): add(sfx,F(fr),np.concatenate([blip(79+i*2,0.05,0.25),blip(86+i*2,0.1,0.25)]),0.6)
rt=t_(1.2); add(music,1.8,env(noise(1.2)*np.linspace(0,1,len(rt))**2,0.01),0.22)
add(music,3.0,crash(),0.6)
# layered groove from the drop: kick+bass → +hats/arp → +snare → +lead → full → outro
t=3.0;b=0
while t<19.5-1e-6:
    bib=b%4;bar=b//4;ch=CH[bar%4];lay=1+int((t-3.0)//3)   # layer grows every 3 s
    add(music,t,kick(),0.85)
    for h,o in ((0,0),(0.25,12)): add(music,t+h,env(tri(hz(ch[0]-12+o),0.22),0.002,0.13),0.6)
    if lay>=2 and t<18:
        for h in (0,0.25): add(music,t+h+0.125,hat(),0.3)
        for k in range(4): add(music,t+k*0.125,env(pulse(hz(ch[k%3]+24),0.1,0.125),0.002,0.05),0.08)
    if lay>=3 and bib in (1,3): add(music,t,snare(),0.5)
    if lay>=4 and t<18:
        for h in (0,0.25): add(music,t+h,env(pulse(hz(MEL[bar%4][bib*2+(1 if h else 0)]),0.22,0.25),0.003,0.15),0.18)
    if lay>=5 and bib==0:
        for m in ch: add(music,t,env(pulse(hz(m+12),0.45,0.5),0.003,0.22),0.06)
    if t>=18 and bib==0:
        for m in ch: add(music,t,env(pulse(hz(m+12),0.45,0.5),0.003,0.22),0.05)
    b+=1;t+=BEAT
add(music,18.0,crash(),0.5)
add(music,19.5,kick(),0.9);add(music,19.5,crash(0.5),0.4)
for m in (57,60,64,69): add(music,19.5,env(pulse(hz(m+12),0.5,0.5),0.003,0.25),0.07)


# cuts: pixel wave whoosh
for fr in (90,180,390,480): add(sfx,F(fr-8),whoosh(0.5),0.55)
# turn: headline pops, tiles, arrow ticks
for fr in (90,105): add(sfx,F(fr),blip(88,0.07,0.25),0.45)
add(sfx,F(98),blip(76,0.06),0.35); add(sfx,F(120),np.concatenate([blip(83,0.06),env(pulse(hz(88),0.2,0.5),0.001,0.1)]),0.5)
for k in range(3): add(sfx,F(112+k*5),blip(72+k*3,0.03,0.125),0.25)
# demo step 1: label, window drops, typing, results, click
add(sfx,F(182),blip(88,0.07,0.25),0.45); add(sfx,F(184),sweep(84,60,0.3,0.25),0.35)
for k in range(11): add(sfx,F(185+k*2.2),env(noise(0.02),0.0005,0.006),0.35)
for i in range(3): add(sfx,F(212+i*4),blip(76+i*3,0.04,0.25),0.3)
add(sfx,F(224),blip(91,0.06),0.35); add(sfx,F(242),env(tri(hz(60),0.06),0.001,0.02),0.6)
# step 2: wipe, cards pop, click
add(sfx,F(255),sweep(60,79,0.25,0.25),0.35); add(sfx,F(255),blip(88,0.07,0.25),0.4)
for i in range(4): add(sfx,F(261+i*4),blip(PENT[i+2],0.04,0.25),0.3)
add(sfx,F(317),env(tri(hz(60),0.06),0.001,0.02),0.6)
# step 3: wipe, order click, new order coin
add(sfx,F(330),sweep(60,79,0.25,0.25),0.35); add(sfx,F(330),blip(88,0.07,0.25),0.4)
add(sfx,F(350),env(tri(hz(60),0.06),0.001,0.02),0.7)
add(sfx,F(355),np.concatenate([blip(83,0.06),env(pulse(hz(88),0.3,0.5),0.001,0.14)]),0.75)
# slogan: icon pop + pixels
add(sfx,F(392),sweep(67,79,0.18),0.4)
for i in range(8): add(sfx,F(392+i*3),blip(PENT[i%len(PENT)],0.03,0.125),0.22)
add(sfx,F(405),np.concatenate([blip(84,0.05),blip(91,0.15)]),0.5)
# CTA: pops, button
for fr in (481,492): add(sfx,F(fr),blip(88,0.07,0.25),0.45)
add(sfx,F(510),np.concatenate([blip(79,0.06),blip(86,0.06),blip(91,0.18)]),0.6)

music/=np.max(np.abs(music)); sfx/=np.max(np.abs(sfx))
mix=music+sfx*0.6
fade=int(0.25*SR); mix[-fade:]*=np.linspace(1,0,fade)
mix=np.tanh(mix*1.1); mix*=0.80/np.max(np.abs(mix))
pcm=(mix*32767).astype(np.int16)
with wave.open('audio.wav','wb') as w: w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.stack([pcm,pcm],1).ravel().tobytes())
print('peak',np.max(np.abs(mix)))

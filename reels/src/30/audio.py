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

# 0–3 s: one note per beat as the lone pixel pulses, cue swoosh, riser, turn
for k in range(6): add(sfx,k*0.5,blip(PENT[k],0.09,0.25),0.8)
add(sfx,F(52),sweep(60,72,0.35),0.35)
rt=t_(1.2); add(music,1.8,env(noise(1.2)*np.linspace(0,1,len(rt))**2,0.01),0.22)
add(sfx,F(84),whoosh(0.4),0.7)
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

# world draws itself (sky paints violet, ground left→right, trees, clouds)
add(sfx,F(92),sweep(55,79,0.6,0.25),0.35)
for k in range(9): add(sfx,F(92+k*4),blip(PENT[k%len(PENT)]-12,0.03,0.125),0.25)
# hero assembly: blip chords per landing cluster + eyes "ding"
for k,fr in enumerate((114,129,144,159)):
    for j in range(3): add(sfx,F(fr+j),blip(PENT[(k+j*2)%len(PENT)],0.05,0.25),0.35)
add(sfx,F(165),np.concatenate([blip(88,0.05),blip(93,0.12)]),0.6)
# footsteps while walking
for a0,b0 in ((190,220),(265,315),(355,405),(455,515)):
    for fr in range(a0,b0,8): add(sfx,F(fr),env(tri(hz(50),0.05),0.001,0.02),0.35)
for fr in (210,300,390): add(sfx,F(fr),blip(88,0.07,0.25),0.45)   # label pops
# station 1: website blocks land in bands
for k,fr in enumerate((207,216,225,234,243)):
    for j in range(4): add(sfx,F(fr+7)+j*0.03,blip(76+k*2+j,0.03,0.125),0.25)
# station 2: phone drops, icons pop
add(sfx,F(290),sweep(84,60,0.3,0.25),0.4); add(sfx,F(300),env(tri(110,0.12),0.001,0.05),0.7)
for i in range(12): add(sfx,F(300+i*4),blip(PENT[i%len(PENT)],0.04,0.25),0.3)
add(sfx,F(348),blip(91,0.06),0.4)
# station 3: ad flips in, likes (coins)
add(sfx,F(380),whoosh(0.35),0.5)
for fr in (410,425,440,455,470): add(sfx,F(fr),np.concatenate([blip(83,0.06),env(pulse(hz(88),0.22,0.5),0.001,0.1)]),0.6)
# climax: lime pixel wave rolls out on the beats
for k,fr in enumerate((465,480,495,510,525)): add(sfx,F(fr),sweep(60+k*4,72+k*4,0.3,0.25),0.4)
# finale: blink, wink, hops, arrow ticks
add(sfx,F(552),blip(90,0.04),0.4); add(sfx,F(566),np.concatenate([blip(84,0.05),blip(91,0.15)]),0.6)
add(sfx,F(570),sweep(67,79,0.18),0.4)
for fr in range(572,600,16): add(sfx,F(fr),blip(96,0.03,0.125),0.25)

music/=np.max(np.abs(music)); sfx/=np.max(np.abs(sfx))
mix=music+sfx*0.6
fade=int(0.25*SR); mix[-fade:]*=np.linspace(1,0,fade)
mix=np.tanh(mix*1.1); mix*=0.80/np.max(np.abs(mix))
pcm=(mix*32767).astype(np.int16)
with wave.open('audio.wav','wb') as w: w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.stack([pcm,pcm],1).ravel().tobytes())
print('peak',np.max(np.abs(mix)))

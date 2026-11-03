// 5 s original mini-game story: the Pixelat hero runs, collects 12 pixels, the counter counts them.
// Loaded on top of story.html by make_pixelrun.js (uses its helpers). Copy lives in PR below.
(function(){
const PR={a:'صورتك مبكسلة؟',b:'كل بكسل محسوب',cta:'راسلنا بالخاص'};
const fitHL=(t,col)=>{let s=92,it=HL(t,s,col);while(it.w>940&&s>56){s-=4;it=HL(t,s,col)}return it};
const A=fitHL(PR.a,WH),B=fitHL(PR.b,L),TA=430,TB=TA+A.h+40;
const bt=TX(PR.cta,54,N,800),BT={t:bt,w:bt.w+120,h:112};
const N_PX=12,SPEED=18,HC=640,STOP=96,END=150;
const pick=i=>12+7*i;
const high=i=>i%3===2;
const py=i=>high(i)?1120:1320;
function ground(f){const off=Math.min(f,STOP)*SPEED%60;
  for(let x=-60;x<W+60;x+=60){const X=x+off;ctx.fillStyle=N;ctx.fillRect(X,GND,60,H-GND);ctx.fillStyle=L;ctx.fillRect(X+3,GND+3,54,18);ctx.fillStyle='#2E2E5C';ctx.fillRect(X+6,GND+30,48,48)}}
function pixel(x,y,s){ctx.fillStyle=N;ctx.fillRect(x-s/2-6,y-s/2-6,s+12,s+18);ctx.fillStyle=L;ctx.fillRect(x-s/2,y-s/2,s,s);ctx.fillStyle=WH;ctx.fillRect(x-s/2+6,y-s/2+6,s/4,s/4)}
function counter(f,n){const t=`بكسل ${n}`;setFont(ctx,'800 44px Taj, TajL');const w=ctx.measureText('بكسل 12').width+48;
  const age=f-(n?pick(n-1):-99),z=1+0.14*(1-clamp(age/6));const cx=W-70-w/2,cy=313;
  ctx.save();ctx.translate(cx,cy);ctx.scale(z,z);ctx.translate(-cx,-cy);raised(ctx,W-70-w,276,w,74,N,5,8);ctx.fillStyle=n===N_PX?L:WH;ctx.fillText(t,cx,328);ctx.restore()}
function heroY(f){const base=GND-9*U;for(let i=0;i<N_PX;i++)if(high(i)){const d=Math.abs(f-pick(i));if(d<10)return base-250*(1-(d/10)*(d/10))}return base}
window.draw=function(f){
  ctx.clearRect(0,0,W,H);sky(f);ground(f);
  for(let i=0;i<3;i++)heart(70+i*80,286,9,true);
  const n=Array.from({length:N_PX},(_,i)=>i).filter(i=>f>=pick(i)).length;
  counter(f,n);
  ctx.save();ctx.translate(540,TA+A.h);ctx.rotate(-0.045);ctx.translate(-540,-(TA+A.h));
  withPop(ctx,f,3,540,TA+A.h/2,()=>drawHL(ctx,A,540,TA));
  withPop(ctx,f,92,540,TB+B.h/2,()=>drawHL(ctx,B,540,TB));
  ctx.restore();
  for(let i=0;i<N_PX;i++){const p=pick(i);
    if(f<p){const x=HC-(p-f)*SPEED;if(x>-60)pixel(x,py(i)+Math.sin((f+i*5)/4)*6,56)}
    else if(f<p+9){const t=(f-p)/9;ctx.fillStyle=L;for(let k=0;k<4;k++){const a=k/4*Math.PI*2+0.78,r=t*90,s=16*(1-t)+4;ctx.fillRect(HC+Math.cos(a)*r-s/2,py(i)+Math.sin(a)*r-s/2,s,s)}}}
  const running=f<STOP;
  const hx=running?HC-88:(HC-88)+(540-HC)*easeOut((f-STOP)/10);
  const hop=f>=STOP+8?-Math.abs(Math.sin((f-STOP-8)/15*Math.PI))*24:0;
  const y=heroY(f),air=y<GND-9*U-1;
  sprite(ctx,air||(!running&&hop<-6)?HERO_JUMP:(running?HERO_RUN[Math.floor(f/3)%2]:HERO_RUN[0]),hx,y+hop,U);
  withPop(ctx,f,100,540,1596,()=>{const b=BT,x=Math.round(540-b.w/2),yy=1540;ctx.fillStyle=N;ctx.fillRect(x-7,yy-7,b.w+14,b.h+28);ctx.fillStyle=L;ctx.fillRect(x,yy,b.w,b.h);drawTX(ctx,b.t,540,yy+(b.h-b.t.h)/2)});
};
window.TOTAL=END;
})();

"""Base instrumental original de Urgencias en 60 (sin derechos de terceros).
Guitarra eléctrica con distorsión (acordes de quinta), bajo y percusión electrónica, a 120 pulsos por minuto.
Uso: python3 tools/musica.py salida.wav [segundos]"""
import sys, numpy as np
from scipy.signal import lfilter, butter
from scipy.io import wavfile
SR=44100; BPM=120; BEAT=60/BPM
rng=np.random.default_rng(60)
def bp(x,lo,hi):
    b,a=butter(2,[lo/(SR/2),hi/(SR/2)],btype="band"); return lfilter(b,a,x)
def lp(x,f):
    b,a=butter(2,f/(SR/2)); return lfilter(b,a,x)
def hp(x,f):
    b,a=butter(2,f/(SR/2),btype="high"); return lfilter(b,a,x)
def cuerda(freq,dur,damp=0.996):
    n=int(SR*dur); N=int(round(SR/freq)); x=np.zeros(n); x[:N]=rng.uniform(-1,1,N)
    a=np.zeros(N+2); a[0]=1; a[N]=-0.5*damp; a[N+1]=-0.5*damp
    return lfilter([1],a,x)
def acorde(root,dur,mute):
    s=sum(cuerda(root*m,dur,0.990 if mute else 0.9985) for m in (1,1.5,2))
    env=np.exp(-np.arange(len(s))/SR/(0.07 if mute else 0.9)); return s*env
def bombo():
    t=np.arange(int(SR*0.28))/SR; f=45+110*np.exp(-t*28); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-t*11)
def caja():
    t=np.arange(int(SR*0.20))/SR
    return (bp(rng.normal(0,1,len(t)),900,6000)*0.9+np.sin(2*np.pi*190*t)*0.5)*np.exp(-t*22)
def plato(abierto=False):
    t=np.arange(int(SR*(0.16 if abierto else 0.05)))/SR
    return hp(rng.normal(0,1,len(t)),7000)*np.exp(-t*(18 if abierto else 70))
def bajo(freq,dur):
    t=np.arange(int(SR*dur))/SR
    s=np.sin(2*np.pi*freq*t)+0.5*np.sign(np.sin(2*np.pi*freq*t))
    return lp(s,500)*np.exp(-t*5)*np.minimum(1,t*200)
def poner(mix,sig,t0,g=1.0):
    i=int(t0*SR); j=min(len(mix),i+len(sig))
    if i<len(mix): mix[i:j]+=sig[:j-i]*g
def pista(segundos):
    n=int(SR*segundos); bat=np.zeros(n); gt=np.zeros(n); bj=np.zeros(n)
    prog=[(82.41,41.20),(65.41,32.70),(98.00,49.00),(73.42,36.71)]   # mi, do, sol, re (guitarra, bajo)
    compases=int(np.ceil(segundos/(4*BEAT)))
    for c in range(compases):
        t0=c*4*BEAT; g,b=prog[c%4]; intro=(c==0)
        for k in range(8):                      # corcheas
            t=t0+k*BEAT/2
            acento=k in (0,3,6)
            poner(gt,acorde(g,BEAT*(1.4 if acento else 0.45),not acento),t,1.0 if acento else 0.7)
            poner(bat,plato(abierto=(k%2==1 and not intro)),t,0.20 if k%2==0 else 0.28)
            if not intro: poner(bj,bajo(b*2 if k==7 else b,BEAT*0.48),t,0.9)
        if not intro:
            for q in range(4): poner(bat,bombo(),t0+q*BEAT,1.0)
            for q in (1,3): poner(bat,caja(),t0+q*BEAT,0.55)
        if c%4==3: poner(bat,caja(),t0+3.5*BEAT,0.45)   # redoble corto al cierre de cada vuelta
    gt=np.tanh(hp(gt,90)*0.9)                  # distorsión
    gt=lp(hp(gt,110),4200)                     # pantalla
    mix=0.50*gt+0.85*bat+0.60*bj
    mix=np.tanh(mix*1.3)
    f=int(SR*1.6); mix[-f:]*=np.linspace(1,0,f); mix[:int(SR*0.02)]*=np.linspace(0,1,int(SR*0.02))
    return (mix/np.max(np.abs(mix))*0.89*32767).astype(np.int16)
if __name__=="__main__":
    out=sys.argv[1]; seg=float(sys.argv[2]) if len(sys.argv)>2 else 26.0
    wavfile.write(out,SR,pista(seg))

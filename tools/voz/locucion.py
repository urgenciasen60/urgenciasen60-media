"""Locución del canal con la voz es_ES-davefx-medium (Piper; datos CC0).
Uso: python3 locucion.py guion.txt salida.wav [velocidad]
Una frase por línea; una línea vacía añade una pausa larga (cambio de plano)."""
import sys, wave, io, numpy as np, soundfile as sf, os
os.environ.setdefault("HF_HUB_DISABLE_XET","1")
from huggingface_hub import hf_hub_download
from piper import PiperVoice, SynthesisConfig
N="es/es_ES/davefx/medium/es_ES-davefx-medium"
onnx=hf_hub_download("rhasspy/piper-voices",N+".onnx"); hf_hub_download("rhasspy/piper-voices",N+".onnx.json")
v=PiperVoice.load(onnx); sr=v.config.sample_rate
ls=float(sys.argv[3]) if len(sys.argv)>3 else 0.95   # «entonación 1», elegida por Eduardo
out=[]; marcas=[]; t=0.0
for linea in open(sys.argv[1],encoding="utf-8").read().split("\n"):
    linea=linea.strip()
    if not linea:
        out.append(np.zeros(int(sr*0.45),dtype=np.int16)); t+=0.45; continue
    b=io.BytesIO()
    with wave.open(b,"wb") as w: v.synthesize_wav(linea,w,syn_config=SynthesisConfig(length_scale=ls))
    b.seek(0); a,_=sf.read(b,dtype="int16")
    marcas.append((round(t,2),linea)); out+= [a,np.zeros(int(sr*0.22),dtype=np.int16)]; t+=len(a)/sr+0.22
sf.write(sys.argv[2],np.concatenate(out),sr)
open(sys.argv[2]+".tiempos.txt","w").write("\n".join(f"{a}\t{b}" for a,b in marcas))
print("duración",round(t,1),"s")

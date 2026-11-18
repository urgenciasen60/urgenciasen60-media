# Modelo humano realista (vídeos de técnica)

- Cuerpo, esqueleto y pesos: MakeHuman (makehumancommunity/makehuman, `makehuman/data/3dobjs/base.obj`, `rigs/default.mhskel`, `rigs/default_weights.mhw`), licencia **CC0**. Clonar con sparse-checkout en `/home/claude/mh`.
- `humano.py`: carga, rig y pose (por ejes o por direcciones de hueso). `FETAL` = decúbito lateral en flexión.
- `huesos.py`: pelvis y columna lumbar modeladas para el plano de transparencia (línea de Tuffier en L4, z=0.155 en reposo).
- `mano.py`: mano derecha del mismo modelo, en pinza, con guante blanco.
- `escena.py`: escena de punción lumbar (planos fijos: `stills`; animaciones: `anim … orbit|aguja|gotas`).

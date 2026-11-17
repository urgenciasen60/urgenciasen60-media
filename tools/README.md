# Herramientas

`ficha.py` genera los carruseles de Urgencias en 60 (HTML estático y JPG de 1080×1350 px con Chrome sin interfaz).
Cada tema tiene su propio guion, por ejemplo `hiperpotasemia.py`:

    python3 tools/hiperpotasemia.py carpeta_de_salida

Requisitos: Google Chrome, Python con Pillow y la fuente Inter instalada en el sistema. La fuente Anton (licencia SIL OFL) va incluida en `tools/fonts/`.
Al terminar se crea `_sheet.png`, una hoja de contacto para revisar todas las diapositivas de un vistazo.

**Formato:** las imágenes se generan y se publican siempre en JPG. TikTok rechaza los PNG (comprobado el 16/11/2026), así que los enlaces que se pasan a Metricool deben terminar en `.jpg`.

**Reels:** `reel.py` genera el vídeo (modelo: `reel_anafilaxia.py`) y `musica.py` la base instrumental del canal. Para incrustarla: `python3 tools/musica.py base.wav 26.2` y después `ffmpeg -i reel.mp4 -i base.wav -map 0:v -map 1:a -c:v copy -c:a aac -shortest salida.mp4`.

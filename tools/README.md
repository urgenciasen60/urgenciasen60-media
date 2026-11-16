# Herramientas

`ficha.py` genera los carruseles de Urgencias en 60 (HTML estático y PNG de 1080×1350 px con Chrome sin interfaz).
Cada tema tiene su propio guion, por ejemplo `hiperpotasemia.py`:

    python3 tools/hiperpotasemia.py carpeta_de_salida

Requisitos: Google Chrome, Python con Pillow y la fuente Inter instalada en el sistema. La fuente Anton (licencia SIL OFL) va incluida en `tools/fonts/`.
Al terminar se crea `_sheet.png`, una hoja de contacto para revisar todas las diapositivas de un vistazo.

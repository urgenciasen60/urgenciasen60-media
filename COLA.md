# Cola de contenido de Urgencias en 60

Estados: **Pendiente de revisión** → **Aprobada** → **Programada** → **Publicada**.
Solo se programa lo que Eduardo ha aprobado. Las imágenes van siempre en JPG (TikTok no admite PNG). Los borradores no están revisados clínicamente.

**Qué tema toca:** sigue el orden de `TEMARIO.md` (Fase A), que sustituye a cualquier otra lista de temas. Las familias Técnica, Paper, Prueba y Fármaco tienen numeración y estructura propias, descritas allí; hasta que Eduardo apruebe un prototipo de cada familia, produce solo fichas clínicas.

Ritmo de publicación: lunes, miércoles y viernes a las 21:00 (Europe/Madrid), en Instagram y TikTok.

| Ficha | Tema | Carpeta | Estado | Publicación |
|---|---|---|---|---|
| 01 | Anafilaxia | `anafilaxia/` | Publicada | Lunes 16/11/2026, 21:00 (Instagram); TikTok reprogramada en JPG |
| 02 | Hiperpotasemia | `hiperpotasemia/` | Programada | Miércoles 18/11/2026, 21:00 |
| 01 (reel) | Anafilaxia, reel de 26 s (versión 3, efectos suaves) | `borradores/anafilaxia-reel/` | Pendiente de revisión | Prototipo de formato; sin música todavía |

Próximo número de ficha libre: 03.

## Reels
Cada carrusel aprobado tendrá un reel del mismo tema (unos 20 s; título arriba y marca abajo; un color de fondo por escena; varios elementos entran a la vez; golpe de zoom, transición deslizante y barra de progreso; ficha al final) que se publica al día siguiente: martes, jueves y sábado. Se generan con `tools/reel.py` (modelo: `tools/reel_anafilaxia.py`). El formato está en fase de prototipo: no generar reels de otros temas hasta que Eduardo apruebe el de anafilaxia.

## Notas de revisión
- Ficha 02: aprobada por Eduardo el 16/11/2026. Criterios fijados por él: gluconato cálcico 1 ampolla de 10 ml, repetible si persiste el ECG alterado; glucosa 25-50 g individualizando, con menos volumen en estado de hipervolemia; bicarbonato 1 M 50-100 mEq solo si hay acidosis metabólica. Fuente principal: Ortiz A, et al. Nefrología 2023;43(5):765-82. doi:10.1016/j.nefro.2023.05.004.
- Criterio general de Eduardo: cuando las guías dan pautas distintas, mostrar el rango que recogen e indicar que se individualiza.

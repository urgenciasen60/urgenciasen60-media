# Cola de contenido de Urgencias en 60

Estados: **Pendiente de revisión** → **Aprobada** → **Programada** → **Publicada**.
Solo se programa lo que Eduardo ha aprobado. Las imágenes van siempre en JPG (TikTok no admite PNG). Los borradores no están revisados clínicamente.

**Qué tema toca:** sigue el orden de `TEMARIO.md` (Fase A), que sustituye a cualquier otra lista de temas. Las familias Técnica, Paper, Prueba y Fármaco tienen numeración y estructura propias, descritas allí; hasta que Eduardo apruebe un prototipo de cada familia, produce solo fichas clínicas.

Ritmo de publicación: lunes, miércoles y viernes a las 21:00 (Europe/Madrid), en Instagram y TikTok.

| Ficha | Tema | Carpeta | Estado | Publicación |
|---|---|---|---|---|
| 01 | Anafilaxia | `anafilaxia/` | Publicada | Lunes 16/11/2026, 21:00 (Instagram); TikTok reprogramada en JPG |
| 02 | Hiperpotasemia | `hiperpotasemia/` | Programada | Miércoles 18/11/2026, 21:00 |
| 01 (reel) | Anafilaxia, reel de 26 s | `anafilaxia/` | Programada | Martes 17/11/2026, 21:00 |
| 02 (reel) | Hiperpotasemia, reel de 26 s | `hiperpotasemia/` | Programada | Jueves 19/11/2026, 21:00 |
| — | Dolor torácico: seis causas que no se pueden escapar | `borradores/dolor-toracico/` | En espera (Eduardo la revisará; no programar ni contar con ella) | — |
| 04 | Sepsis: la primera hora (+ reel) | `borradores/sepsis/` | Pendiente de revisión | — |
| 03 | Crisis de asma (+ reel) | `asma/` | **Programada** vie 20/11 21:00 (carrusel) y sáb 21/11 21:00 (reel) | — |
| 06 | Cólico nefrítico | `borradores/colico-nefritico/` | Pendiente de revisión | — |
| 05 | Hipoglucemia (+ reel) | `hipoglucemia/` | **Programada** mié 25/11 21:00 (carrusel) y jue 26/11 21:00 (reel) | — |
| Técnica 01 | Epistaxis: de la compresión al taponamiento (+ reel) | `borradores/tecnica-epistaxis/` | Pendiente de revisión (prototipo de la familia Técnica) | — |
| Técnica 02 | Punción lumbar (+ reel) | `borradores/tecnica-puncion-lumbar/` | Pendiente de revisión | — |
| Guía 01 | Sepsis 2026: ¿qué cambia? | `borradores/guia-sepsis-2026/` | Aplazada: no publicar cerca de la Ficha 04. Rehacer a 10 diapositivas + reel de 60 s | — |
| Paper 01 | Ensayo BEST: bougie o fiador en el trauma grave | `borradores/paper-best/` | En biblioteca (Eduardo prefiere de momento papers de médico de puerta) | — |
| 04 | Punción lumbar: ¿sí o no? (+ reel) | `puncion-lumbar-indicaciones/` | **Programada** lun 23/11 21:00 (carrusel) y mar 24/11 21:00 (reel) | — |

Próximo número libre: Ficha 09, Técnica 03, Guía 02, Paper 02. Las dudas clínicas de cada borrador están en `borradores/REVISION.md`.

## Reels
Cada carrusel aprobado tendrá un reel del mismo tema (unos 20 s; título arriba y marca abajo; un color de fondo por escena; varios elementos entran a la vez; golpe de zoom, transición deslizante y barra de progreso; ficha al final) que se publica al día siguiente: martes, jueves y sábado. Se generan con `tools/reel.py` (modelo: `tools/reel_anafilaxia.py`). Plantilla aprobada por Eduardo el 17/11/2026: intensidad suave (valores por defecto de `build`), unos 26 s, un color de fondo por escena, ficha al final. El reel reutiliza el contenido ya aprobado del carrusel, así que no necesita revisión clínica aparte: genera y programa el reel de cada carrusel aprobado para el día siguiente a las 21:00 (Instagram tipo REEL y TikTok).

## Notas de revisión
- Ficha 03 (dolor torácico): el ECG en menos de 10 minutos y la troponina ultrasensible a las 0 h y 1 h (o 2 h) proceden de la guía ESC 2023 de SCA (Byrne RA, et al. Eur Heart J 2023;44(38):3720-826), consultada a través de resúmenes en español, no del texto original. La lista de seis causas y las pistas semiológicas proceden de revisiones y material docente, no de una guía. Dudas para Eduardo: si mantener la rotura esofágica entre las seis y si añadir la ecografía a pie de cama.
- Ficha 02: aprobada por Eduardo el 16/11/2026. Criterios fijados por él: gluconato cálcico 1 ampolla de 10 ml, repetible si persiste el ECG alterado; glucosa 25-50 g individualizando, con menos volumen en estado de hipervolemia; bicarbonato 1 M 50-100 mEq solo si hay acidosis metabólica. Fuente principal: Ortiz A, et al. Nefrología 2023;43(5):765-82. doi:10.1016/j.nefro.2023.05.004.
- Criterio de Eduardo (17/11/2026): las fichas pueden llevar alguna palabra más si evita tener que buscar el dato con el paciente delante; tras un grupo farmacológico, poner un ejemplo entre paréntesis, como «diurético de asa (furosemida)».
- Música de los reels: en Instagram se añade al programar con `audioConfiguration` (catálogo de Instagram; funciona pasando el identificador numérico). TikTok no admite esa vía, así que todos los reels llevan incrustada la base instrumental propia del canal (`tools/musica.py`: guitarra con distorsión, bajo y percusión electrónica, 120 pulsos por minuto); por ahora también suena en Instagram (sin `audioConfiguration`), porque las pistas del catálogo no se pueden escuchar ni verificar desde aquí. Si Eduardo elige de oído una pista del catálogo, se añade con `audioConfiguration` y `videoVolume: 0`.
- Criterio general de Eduardo: cuando las guías dan pautas distintas, mostrar el rango que recogen e indicar que se individualiza.

## Decisiones del 17/11/2026
- **Vídeos de técnica:** animación 3D (Blender) con maniquí sin cara, unos 60 s, voz explicando y subtítulos. Guiones en `guiones/tecnicas-video-60s.md`; escena en `tools/3d/`.
- **Render:** la noche del martes (los créditos se renuevan el miércoles).
- **Guías:** carrusel de unas 10 diapositivas + reel de 60 s.
- **Papers:** de médico de urgencias, de 2026. Candidato: PRESC1SE-MI (Lancet 2026; doi:10.1016/S0140-6736(26)01654-5), pendiente del texto completo.
- **Sepsis:** no publicar dos piezas seguidas.
- **Voz del canal:** voz sintética castellana `es_ES-davefx-medium` (Piper; datos CC0), elegida por Eduardo el 17/11. Script en `tools/voz/locucion.py`; textos de locución en `tools/voz/*.txt`. Se descartaron la clonación de su voz (seseo/acento americano) y el modelo F5-Spanish (licencia no comercial).
- **18/11 (render nocturno):** vídeo 3D de 60 s de la punción lumbar en `borradores/tecnica-puncion-lumbar/*-video60.mp4` (borrador, sin programar). Epistaxis: solo escenas 3D de prueba en `borradores/tecnica-epistaxis/escenas-3d/`; locución y montaje a la espera de la revisión de contenido de Eduardo.
- **18/11:** Eduardo decide separar técnica y clínica: el vídeo y el carrusel de Técnica 02 son solo técnica; indicaciones, TC previa y contraindicaciones pasan a la Ficha 08 (fuentes que aportó: Herlihy 2024 vía cbseram y Preevid 25020).
- **18/11 (decisiones de Eduardo):** técnicas = carrusel + vídeo 60 s el MISMO día (primero el vídeo) y al día siguiente el reel corto, que termina remitiendo al carrusel y al vídeo. Vídeo PL v4 (próxima noche de render): ~60 s, máximo realismo, varón musculado, paño quirúrgico, cara visible permitida, corte sagital realista, plano del LCR con la mano retirando el fiador y luego las gotas, música del canal bajita. Ficha 08: solo adultos, hemocultivos antes, infección local y anticoagulación como contraindicaciones, con cifras (plaquetas > 40.000–50.000/µl, INR < 1,5; ABN 2026).
- **18/11:** los números de ficha se asignan por orden de publicación (para el libro): asma = Ficha 03. Dolor torácico y Ficha 08 (PL) se renumerarán al publicarse.
- **Plan 23/11–6/12 (propuesto 18/11):** lun 23 Ficha 04 PL ¿sí o no?; mié 25 Ficha 05 hipoglucemia (revisar antes del lun 23); vie 27 Técnica 01 PL: vídeo 60 s 14:00 + carrusel 21:00 (render mar 24, revisar antes del jue 26); lun 30 Ficha 06 sepsis (revisar antes del vie 27); mié 2/12 Ficha 07 cólico nefrítico (revisar antes del lun 30); vie 4/12 Técnica 02 epistaxis (contenido antes del lun 30, render mar 1) o, si no llega, dolor torácico. Reels al día siguiente de cada carrusel.

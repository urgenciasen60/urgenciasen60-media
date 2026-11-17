from PIL import Image, ImageDraw, ImageFont
import textwrap
W,H=1080,1920; Y=(255,214,10); K=(17,17,17)
AN=lambda s: ImageFont.truetype("/home/claude/v3d/Anton.ttf",s); IN=lambda s,w="Bold": ImageFont.truetype(f"/usr/share/fonts/opentype/inter/Inter-{w}.otf",s)
def ov(name,cap,key):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    tag="TÉCNICA 02 · PUNCIÓN LUMBAR"; tw=d.textlength(tag,font=IN(30,"Black"))
    d.rounded_rectangle([60,236,60+tw+40,294],8,fill=Y); d.text((80,247),tag,font=IN(30,"Black"),fill=K)
    lines=textwrap.wrap(cap,26); y=H-420-80-len(lines)*78
    d.text((60,y-150),key,font=AN(120),fill=Y)
    for l in lines:
        w=d.textlength(l,font=IN(58,"Black")); d.rectangle([46,y-6,60+w+14,y+70],fill=(17,17,17,215)); d.text((60,y),l,font=IN(58,"Black"),fill=(255,255,255)); y+=78
    h="@urgenciasen60"; d.rounded_rectangle([60,H-410,60+d.textlength(h,font=IN(34,"Bold"))+36,H-354],8,fill=K); d.text((78,H-402),h,font=IN(34,"Bold"),fill=Y)
    im.save(name)
ov("ovA.png","Decúbito lateral, rodillas al pecho y mentón al esternón.","POSICIÓN")
ov("ovB.png","La línea entre las crestas ilíacas cruza L4. Pinchamos en L4–L5.","REFERENCIA")
ov("ovC.png","Línea media, apuntando hacia el ombligo.","AGUJA")

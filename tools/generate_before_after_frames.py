#!/usr/bin/env python3
"""
Pixaro Before/After Frame Builder
Run on Windows:
  python tools\generate_before_after_frames.py "Z:\AKKI RAYZADA\SOCIAL MEDIA\PIXARO\PIXARO IMAGES"
It matches SAME filenames/stems from BEFORE and AFTER folders and creates website frames.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import sys, json
IMG_EXTS={'.jpg','.jpeg','.png','.webp','.bmp','.tif','.tiff'}
def safe_open(path): return Image.open(path).convert('RGBA')
def fit_image(im,size):
    im=ImageOps.contain(im,size,Image.LANCZOS)
    bg=Image.new('RGBA',size,(255,255,255,255)); bg.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2)); return bg
def get_font(size,bold=False):
    for p in [('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf'),('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]:
        try: return ImageFont.truetype(p,size)
        except Exception: pass
    return ImageFont.load_default()
def frame_pair(before_path,after_path,out_path,title):
    W,H=1600,980
    bg=Image.new('RGB',(W,H),(8,9,8)); d=ImageDraw.Draw(bg)
    for y in range(H): d.line([(0,y),(W,y)],fill=(int(8+18*y/H),int(9+16*y/H),int(8+8*y/H)))
    gold=(221,212,106); white=(250,250,242); muted=(188,188,166)
    d.ellipse((-220,-220,500,420),fill=(38,35,12)); d.ellipse((1120,-160,1800,520),fill=(9,60,58))
    d.text((70,58),'PIXARO Before / After Transformation',font=get_font(58,True),fill=white)
    d.text((72,126),title,font=get_font(26),fill=muted)
    d.text((1180,58),'PIXARO',font=get_font(54,True),fill=gold); d.text((1184,112),'Flat to Fantastic',font=get_font(22),fill=gold)
    card_w,card_h=690,620; boxes=[(70,220,760,840,'BEFORE',(230,63,63)),(840,220,1530,840,'AFTER',(87,199,79))]
    for x1,y1,x2,y2,label,color in boxes:
        d.rounded_rectangle((x1,y1,x2,y2),radius=38,fill=(252,252,248),outline=(gold if label=='AFTER' else (60,60,55)),width=5)
        d.rounded_rectangle((x1+28,y1+28,x2-28,y2-86),radius=28,fill=(255,255,255),outline=(220,220,210),width=2)
        d.rounded_rectangle((x1+34,y2-70,x1+224,y2-22),radius=24,fill=color)
        d.text((x1+58,y2-62),label,font=get_font(34,True),fill=(255,255,255))
    bi=fit_image(safe_open(before_path),(620,480)).convert('RGB'); ai=fit_image(safe_open(after_path),(620,480)).convert('RGB')
    bg.paste(bi,(105,255)); bg.paste(ai,(875,255))
    d.rounded_rectangle((760,462,840,598),radius=40,fill=gold); d.polygon([(790,495),(790,565),(825,530)],fill=(10,10,10))
    d.text((70,884),'Clean cutout • background removal • crystal-clear detail • realistic 3D lighting',font=get_font(22,True),fill=gold)
    d.text((70,922),'WhatsApp: +91 9033187554   |   Email: px.pixaro@gmail.com',font=get_font(22,True),fill=white)
    bg.save(out_path,quality=92,optimize=True)
def main():
    if len(sys.argv)<2:
        raise SystemExit('Usage: python tools\generate_before_after_frames.py "Z:\...\PIXARO IMAGES"')
    root=Path(sys.argv[1]); before_dir=root/'BEFORE'; after_dir=root/'AFTER'
    if not before_dir.exists() or not after_dir.exists(): raise SystemExit(f'BEFORE/AFTER folders not found under: {root}')
    output=Path(__file__).resolve().parents[1]/'assets'/'matched_frames'; output.mkdir(parents=True,exist_ok=True)
    before={p.stem.lower():p for p in before_dir.iterdir() if p.suffix.lower() in IMG_EXTS}
    after={p.stem.lower():p for p in after_dir.iterdir() if p.suffix.lower() in IMG_EXTS}
    keys=sorted(set(before)&set(after))
    if not keys: raise SystemExit('No matching filenames found. Keep SAME names in BEFORE and AFTER folders.')
    for p in output.glob('frame_*.jpg'): p.unlink()
    frames=[]
    for i,k in enumerate(keys,1):
        out_file=output/f'frame_{i:03d}.jpg'; title=before[k].stem.replace('_',' ').replace('-',' ').title()
        frame_pair(before[k],after[k],out_file,title); frames.append(f'assets/matched_frames/frame_{i:03d}.jpg'); print('Created',out_file.name)
    (output/'manifest.js').write_text('window.PIXARO_MATCHED_FRAMES = '+json.dumps(frames,indent=2)+';
',encoding='utf-8')
    print('Done.',len(frames),'matched frames created.')
if __name__=='__main__': main()

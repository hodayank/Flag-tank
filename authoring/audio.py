import wave, math, random, os, json, struct
from PIL import Image,ImageDraw
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));out=root+'/public/assets/audio';os.makedirs(out,exist_ok=True);random.seed(19)
ids=['motor-idle','motor-load','tread-sand','tread-ground','turn','stop','shot','rocket','tank-hit','shield-hit','helper-spawn','helper-shutdown','disable','return','adobe-crack','adobe-collapse','brick-crack','brick-collapse','stone-crack','stone-collapse','rubble','adobe-rebuild','brick-rebuild','stone-rebuild','flag-spawn','flag-collect','power-collect','power-activate','power-end','countdown','result','invite','accept','ready','button','najdi-ambience','basic-ambience','japan-ambience','najdi-music','basic-music','japan-music'];manifest=[]
for name in ids:
 count=4 if name in ['shot','tank-hit','adobe-crack','adobe-collapse','brick-crack','brick-collapse','stone-crack','stone-collapse'] else 1
 for variation in range(count):
  music=name.endswith('music');loop=music or 'ambience' in name or name.startswith(('motor','tread'));dur=48 if music else 4 if loop else .5 if 'shot' in name else .85
  sr=48000;N=int(sr*dur);samples=[];smooth=0;freq=110+variation*9
  for i in range(N):
   t=i/sr;smooth=.92*smooth+.08*random.uniform(-1,1)
   if music:
    beat=int(t*2);phase=t%(0.5);notes=[0,7,12,4,9,7,2,7];f=220*2**(notes[(beat//2)%8]/12);s=sum(math.sin(2*math.pi*f*k*t)*math.exp(-phase*(7+k*3))/k**2 for k in range(1,5))*.15
   elif 'ambience' in name:s=smooth*.12*(.7+.3*math.sin(t*math.pi/2))
   elif loop:s=.06*math.sin(2*math.pi*48*t)+smooth*.22+.025*math.sin(2*math.pi*96*t);s*=min(1,t*20,(dur-t)*20)
   elif any(x in name for x in ['flag','power','ready','result','button','accept','invite','countdown']):s=sum(math.sin(2*math.pi*f*t)*math.exp(-t*8)*.13 for f in [523.25,659.25,783.99]);s*=min(1,t*100)
   else:s=(smooth*.8+math.sin(2*math.pi*(freq*t-25*t*t))*.22)*math.exp(-t*(12 if 'shot' in name else 7))*min(1,t*200)
   samples.append(max(-.9,min(.9,s)))
  file=name+(f'-{variation+1}' if count>1 else '')+'.wav'
  with wave.open(out+'/'+file,'wb') as w:w.setparams((1,2,sr,0,'NONE','not compressed'));w.writeframes(b''.join(struct.pack('<h',int(s*32767)) for s in samples))
  manifest.append(dict(id=file[:-4],file='assets/audio/'+file,loop=loop,duration=dur,sampleRate=sr,channels=1,loopStart=0,loopEnd=N if loop else None,provenance='Original procedural PCM recording; authoring/audio.py',master=file))
json.dump({'version':1,'sounds':manifest},open(root+'/public/assets/audio-manifest.json','w'),indent=2)
for name,size in [('icon',256),('cover',768)]:
 im=Image.new('RGB',(size,size),(25,48,51));d=ImageDraw.Draw(im);d.rounded_rectangle((size*.18,size*.33,size*.82,size*.78),radius=size*.09,fill=(28,169,190));d.ellipse((size*.32,size*.28,size*.68,size*.63),fill=(47,194,211));d.rectangle((size*.46,size*.13,size*.54,size*.48),fill=(242,192,77));d.polygon([(size*.53,size*.14),(size*.82,size*.19),(size*.53,size*.3)],fill=(255,204,73));im.save(root+'/public/'+name+'.png')
# Original tiling sand texture, no catalog artwork.
im=Image.new('RGB',(128,128));p=im.load()
for x in range(128):
 for y in range(128):v=random.randrange(-10,11);p[x,y]=(220+v,184+v,126+v)
im.save(root+'/public/assets/textures/sand.png')

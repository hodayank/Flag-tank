from PIL import Image
import random,math,pathlib
random.seed(44);n=1024;im=Image.new('RGB',(n,n));p=im.load()
for y in range(n):
 for x in range(n):
  ridge=math.sin(y*.085+math.sin(x*.012)*2.3)*2.8;grain=random.uniform(-2,2);v=ridge+grain;p[x,y]=(int(233+v),int(201+v),int(143+v))
im.save(pathlib.Path(__file__).resolve().parents[1]/'public/assets/najdi-v4/sand.png')

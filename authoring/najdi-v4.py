# Entirely new reference-driven asset set. Does not execute the legacy asset generator.
import bpy, math, random, json, pathlib
from mathutils import Vector
R=pathlib.Path(__file__).resolve().parents[1]; O=R/'public/assets/najdi-v4';S=R/'authoring/najdi-v4';O.mkdir(exist_ok=True);S.mkdir(exist_ok=True);random.seed(416)
def mat(n,col,rough=.8,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*col,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m
sand=[mat('earthen pigment '+str(i),(.48+i*.025,.255+i*.018,.095+i*.012)) for i in range(8)]
wood=mat('aged cedar',(.26,.105,.035));rubber=mat('track rubber',(.025,.035,.04));iron=mat('forged rim',(.18,.23,.25),.5,.4);gold=mat('satin gold',(.98,.59,.035),.4,.35);green=mat('date foliage',(.10,.29,.025));cream=mat('canvas cream',(.92,.79,.54));red=mat('striped red',(.65,.08,.035));blue=mat('royal blue',(.025,.16,.67),.48,.18);coral=mat('coral paint',(.8,.055,.025),.48,.18);skin=mat('skin',(.76,.43,.23));white=mat('thobe linen',(.92,.89,.78));water=mat('irrigation water',(.025,.37,.57),.25,.1)
def start():
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def box(n,p,d,m,b=.055):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=n;o.dimensions=d;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 if b:q=o.modifiers.new('hand softened edges','BEVEL');q.width=b;q.segments=2;o.modifiers.new('weighted shading','WEIGHTED_NORMAL')
 return o
def ball(n,p,d,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,location=p);o=bpy.context.object;o.name=n;o.scale=d;o.data.materials.append(m)
 for f in o.data.polygons:f.use_smooth=True
 return o
def cylinder(n,p,r,h,m,axis=None):
 bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=h,location=p);o=bpy.context.object;o.name=n;o.data.materials.append(m)
 if axis:o.rotation_euler=axis
 q=o.modifiers.new('rim bevel','BEVEL');q.width=.018;q.segments=2;o.modifiers.new('weighted shading','WEIGHTED_NORMAL');return o
def empty(n,p=(0,0,0),parent=None):
 o=bpy.data.objects.new(n,None);bpy.context.collection.objects.link(o);o.location=p;o.parent=parent;return o
def parent(o,p):o.parent=p;return o
records=[]
def save(id):
 bpy.context.view_layer.update();objs=list(bpy.context.scene.objects);coords=[o.matrix_world@Vector(c)for o in objs if o.type=='MESH'for c in o.bound_box];bounds=[[min(v[i]for v in coords)for i in range(3)],[max(v[i]for v in coords)for i in range(3)]]
 bpy.ops.wm.save_as_mainfile(filepath=str(S/(id+'.blend')));bpy.ops.export_scene.gltf(filepath=str(O/(id+'.glb')),export_format='GLB',export_apply=True)
 records.append(dict(id=id,runtime='assets/najdi-v4/'+id+'.glb',source='authoring/najdi-v4/'+id+'.blend',bounds=bounds,provenance='New original meshes authored from Tank.rar references; najdi-v4.py'))
for id,m,scale in [('COM-TANK-01',blue,1),('COM-TANK-02',coral,1),('COM-HELPER-01',blue,.6)]:
 start();root=empty('root');root.rotation_euler.z=math.pi;root.scale=(scale,)*3
 parent(box('hull',(0,0,.43),(1.0,1.5,.34),m,.13),root);nose=parent(box('sloped glacis',(0,.58,.53),(.96,.46,.26),m,.08),root);nose.rotation_euler.x=-.24
 for side in [-1,1]:
  track=empty('leftTrack'if side<0 else'rightTrack',parent=root)
  parent(box('continuous belt',(side*.52,0,.22),(.26,1.58,.43),rubber,.19),track)
  for y in [-.6,-.3,0,.3,.6]:
   parent(cylinder('road wheel',(side*.66,y,.23),.16,.045,iron,(0,math.pi/2,0)),track);parent(cylinder('wheel hub',(side*.69,y,.23),.077,.05,m,(0,math.pi/2,0)),track)
  for y in [j*.12-.72 for j in range(13)]:
   for z in [.035,.42]:parent(box('tread shoe',(side*.52,y,z),(.29,.065,.04),iron,.012),track)
  parent(box('swept fender',(side*.52,0,.54),(.35,1.62,.12),m,.055),root)
 turret=empty('turret',(0,-.08,.64),root);parent(cylinder('turret collar',(0,0,0),.4,.1,iron),turret);parent(ball('cast turret',(0,0,.13),(.43,.4,.27),m),turret);parent(cylinder('cupola',(0,-.03,.39),.19,.075,m),turret)
 barrel=empty('barrel',(0,.32,.13),turret);parent(cylinder('cannon',(0,.31,0),.105,.68,m,(math.pi/2,0,0)),barrel);parent(cylinder('muzzle ring',(0,.64,0),.135,.15,m,(math.pi/2,0,0)),barrel);parent(cylinder('bore',(0,.721,0),.093,.007,rubber,(math.pi/2,0,0)),barrel);empty('muzzleSocket',(0,.73,0),barrel)
 for side in [-1,1]:
  if m==blue:parent(cylinder('team roundel',(side*.422,0,.16),.1,.015,gold,(0,math.pi/2,0)),turret)
  else:
   o=parent(box('team diamond',(side*.422,0,.16),(.016,.14,.14),gold,.009),turret);o.rotation_euler.x=.785
  parent(box('storage bin',(side*.5,-.4,.66),(.23,.38,.18),m,.04),root)
  for y in [-.52,-.28]:parent(box('latch',(side*.625,y,.66),(.015,.045,.06),iron,.005),root)
 parent(cylinder('antenna',(.29,-.3,1.05),.012,.55,iron),root);parent(ball('antenna tip',(.29,-.3,1.34),(.03,)*3,m),root)
 for n,p in [('wheels',(0,0,0)),('hitSocket',(0,0,.6)),('healthAnchor',(0,0,1.5)),('groundShadowAnchor',(0,0,.005))]:empty(n,p,root)
 save(id)
for num in [7,8,9,10,11,23]:
 start()
 if num==9:
  for i in range(18):o=box('collapsed earth',(random.uniform(-.85,.85),random.uniform(-.6,.6),random.uniform(.08,.2)),(random.uniform(.16,.38),.25,random.uniform(.12,.3)),random.choice(sand),.04);o.rotation_euler=(random.random()*.5,random.random()*.5,random.random()*6)
 else:
  # Thin modular masonry wall with four staggered courses, like the supplied wall board.
  for row in range(4):
   widths=[.48]*4 if row%2==0 else [.24,.48,.48,.48,.24];x=-.96
   for width in widths:
    z=.105+row*.21;o=box('rounded adobe block',(x+width/2,0,z),(width-.012,.42,.20),random.choice(sand),.045);x+=width
    if num==8:
     for j in range(2):c=box('open zigzag crack',(x-width*.4+(.025 if j else 0),-.217,z+(j-.5)*.08),(.022,.015,.13),wood,.002);c.rotation_euler.y=(-1 if j else 1)*.35
  if num in [10,11]:
   for row in range(4):
    for y in [.23,.68]:box('return wall',(-.72 if num==10 else 0,y,.105+row*.21),(.42,.47,.20),random.choice(sand),.04)
  if num==23:
   box('plastered boundary',(0,0,.52),(1.98,.5,1.04),sand[3],.07)
   for x in [-.88,.88]:
    box('boundary post',(x,0,.65),(.3,.65,1.3),sand[4],.045);bpy.ops.mesh.primitive_cone_add(vertices=4,radius1=.25,radius2=0,depth=.22,location=(x,0,1.41),rotation=(0,0,math.pi/4));bpy.context.object.data.materials.append(sand[5])
 save('NJD-'+str(num).zfill(2))
for num in range(12,25):
 if num==23:continue
 start()
 if num==13:
  box('mud house',(0,0,1.3),(3.2,2.5,2.6),sand[3],.16)
  for y in [-1.15,1.15]:box('roof parapet',(0,y,2.69),(3.2,.22,.32),sand[4],.06)
  for x in [-1.48,1.48]:box('parapet side',(x,0,2.69),(.22,2.3,.32),sand[4],.06)
  for x in [-1.45,1.45]:
   for y in [-1.13,1.13]:box('corner finial',(x,y,2.86),(.35,.35,.42),sand[5],.06)
  box('door recess',(-.45,-1.26,.65),(.72,.04,1.3),wood,.18)
  for j in range(6):box('door board',(-.45+(j-2.5)*.105,-1.30,.62),(.1,.04,1.15),wood,.015)
  for z in [.25,.95]:box('iron door strap',(-.45,-1.335,z),(.65,.025,.05),iron,.005)
  for x in [-1,-.35,.35,1]:
   me=bpy.data.meshes.new('triangle opening');me.from_pydata([(x-.12,-1.257,1.95),(x+.12,-1.257,1.95),(x,-1.257,2.2)],[],[(0,1,2)]);ob=bpy.data.objects.new('triangular ventilation',me);bpy.context.collection.objects.link(ob);ob.data.materials.append(wood)
   box('rafter end',(x,-1.37,2.36),(.11,.28,.11),wood,.02)
  box('window recess',(.85,-1.263,1.1),(.4,.03,.55),wood,.04)
 elif num in [14,15]:
  for i in range(6):box('cedar plank',((i-2.5)*.16,0,.55),(.15,.9 if num==15 else .13,1.1),wood,.02)
  for z in [.1,1]:box('frame crossbar',(0,-.48 if num==15 else -.1,z),(1.08,.12,.13),sand[1]if num==14 else wood,.025)
  if num==15:
   for angle in [-.75,.75]:o=box('X brace',(0,-.55,.55),(1.25,.08,.1),wood,.02);o.rotation_euler.y=angle
 elif num==16:
  for x,y,scale in [(-.3,0,1),(.32,.13,.75),(.1,-.4,.5)]:
   ball('pot belly',(x,y,.34*scale),(.29*scale,.29*scale,.35*scale),sand[1]);cylinder('pot neck',(x,y,.65*scale),.13*scale,.17*scale,sand[1]);cylinder('pot rim',(x,y,.74*scale),.17*scale,.055,sand[3]);cylinder('dark opening',(x,y,.772*scale),.115*scale,.005,wood)
 elif num==17:
  cylinder('palm trunk',(0,0,1.1),.16,2.2,wood)
  for level in range(12):
   for j in range(6):a=j*math.pi/3+(level%2)*.5;o=box('diamond bark',(math.cos(a)*.14,math.sin(a)*.14,.1+level*.17),(.13,.07,.16),sand[0],.025);o.rotation_euler=(0,.3,a)
  for j in range(12):
   a=j*math.pi/6;frond=empty('frond-'+str(j),(0,0,2.2))
   for k in range(9):
    t=(k+1)/9;r=t*1.5;z=.45*math.sin(t*math.pi)-t*.3
    for side in [-1,1]:
     x=math.cos(a)*r;y=math.sin(a)*r;me=bpy.data.meshes.new('leaflet');me.from_pydata([(x,y,z),(x+math.cos(a+side)*.43*(1-t*.4),y+math.sin(a+side)*.43*(1-t*.4),z-.1),(x+math.cos(a)*.15,y+math.sin(a)*.15,z+.035)],[],[(0,1,2)]);ob=bpy.data.objects.new('pointed leaf',me);bpy.context.collection.objects.link(ob);ob.parent=frond;ob.data.materials.append(green);q=ob.modifiers.new('leaf thickness','SOLIDIFY');q.thickness=.014
  for j in range(12):a=j*2.4;ball('dates',(math.cos(a)*.25,math.sin(a)*.25,2-j%3*.1),(.07,.07,.12),red)
 elif num in [18,19]:
  if num==19:
   box('tilled soil',(0,0,.03),(1.6,1.8,.1),wood)
   for x in [-.9,.9]:
    for y in [-.8,-.4,0,.4,.8]:box('bed edging',(x,y,.12),(.23,.38,.24),sand[2],.04)
  for j in range(20):
   x=(j%4-1.5)*.32;y=(j//4-2)*.32
   for a in [0,1.6,3.2,4.8]:o=ball('crop leaf',(x+math.cos(a)*.1,y+math.sin(a)*.1,.16),(.07,.2,.035),green);o.rotation_euler=(.5,0,a)
 elif num==20:
  box('water',(0,0,.025),(1.2,3,.05),water,.01)
  for x in [-.75,.75]:
   for y in [-1.25,-.75,-.25,.25,.75,1.25]:box('channel lining',(x,y,.13),(.3,.48,.26),sand[4],.05)
 elif num==21:
  box('woven mat',(0,0,.025),(1.8,1.3,.05),red,.025)
  for x in [-.8,.8]:box('rug border',(x,0,.055),(.1,1.22,.01),cream,.003)
  for y in [-.55,.55]:box('rug border',(0,y,.055),(1.6,.09,.01),cream,.003)
  for x in [-.5,0,.5]:o=box('woven diamond',(x,0,.06),(.22,.22,.01),cream,.003);o.rotation_euler.z=.785
  ball('date basket',(.4,.05,.18),(.28,.25,.15),wood)
  for j in range(18):ball('date',(.4+random.uniform(-.18,.18),random.uniform(-.15,.2),.3),(.045,.035,.035),sand[0])
 elif num==22:
  for j,x in enumerate([-.4,.4]):
   ball('seated thobe',(x,0,.3),(.25,.24,.3),white);ball('head',(x,0,.78),(.22,.2,.24),skin);cylinder('white cap',(x,0,.97),.215,.08,white)
   for side in [-1,1]:
    ball('folded knee',(x+side*.14,-.18,.14),(.21,.16,.12),white);ball('hand',(x+side*.23,-.16,.4),(.07,)*3,skin);ball('eye',(x+side*.07,-.194,.81),(.025,.014,.03),rubber)
   if j==0:
    box('shemagh cloth',(x,0,.98),(.49,.42,.06),white,.04)
    for k in range(7):box('red weave',(x+(k-3)*.06,0,1.016),(.025,.4,.008),red,.002)
    cylinder('igal',(x,0,1.04),.22,.03,rubber)
 elif num==24:
  for x in [-1,1]:
   for y in [-.7,.7]:cylinder('timber post',(x,y,1),.07,2,wood)
  # Striped cloth geometry with real sag, not a flat red slab.
  for i in range(12):
   x=-1.2+i*.2;me=bpy.data.meshes.new('canopy cloth');verts=[(x,-1,2.12),(x+.2,-1,2.12),(x+.2,0,1.9),(x,0,1.9),(x,1,2.12),(x+.2,1,2.12)];me.from_pydata(verts,[],[(0,1,2,3),(3,2,5,4)]);ob=bpy.data.objects.new('canvas stripe',me);bpy.context.collection.objects.link(ob);ob.data.materials.append(red if i%2 else cream);ob.modifiers.new('fabric thickness','SOLIDIFY').thickness=.025
  for x in [-.65,.5]:box('shelter crate',(x,0,.3),(.5,.5,.6),wood,.035)
 else:box('ground tile',(0,0,-.06),(2,2,.12),sand[4],.03)
 save('NJD-'+str(num).zfill(2))
start();cylinder('flagpole',(0,0,.8),.035,1.6,wood);ball('finial',(0,0,1.66),(.09,)*3,gold);cylinder('stand',(0,0,.04),.2,.08,iron)
verts=[(i*.07,math.sin(i*.65)*.065,1.48-j*.14)for i in range(13)for j in range(5)];faces=[]
for i in range(12):
 for j in range(4):a=i*5+j;faces.append((a,a+5,a+6,a+1))
me=bpy.data.meshes.new('golden cloth');me.from_pydata(verts,[],faces);ob=bpy.data.objects.new('cloth',me);bpy.context.collection.objects.link(ob);ob.data.materials.append(gold);ob.modifiers.new('cloth thickness','SOLIDIFY').thickness=.015;save('COM-FLAG-01')
for i in range(1,6):
 start();box('badge',(0,0,.42),(.68,.15,.7),blue if i in [1,5]else red,.14);cylinder('base',(0,0,.06),.38,.1,gold)
 if i==2:
  for x in [-.19,0,.19]:cylinder('bullet',(x,-.12,.42),.055,.32,gold);ball('tip',(x,-.12,.59),(.055,.055,.08),gold)
 elif i==3:cylinder('rocket',(0,-.13,.43),.1,.4,white);ball('nose',(0,-.13,.66),(.1,.1,.13),red)
 elif i==4:
  for j in range(4):a=j*math.pi/2;cylinder('bore',(math.cos(a)*.15,-.16,.42+math.sin(a)*.15),.075,.1,iron,(math.pi/2,0,0))
 elif i==5:box('mini tank',(0,-.15,.4),(.42,.18,.23),blue,.07);ball('mini turret',(0,-.2,.57),(.14,.1,.12),blue)
 else:box('shield face',(0,-.12,.43),(.36,.06,.45),cream,.12)
 save('COM-POWER-0'+str(i))
(O/'manifest.json').write_text(json.dumps({'version':4,'referenceArchive':'Tank.rar','assets':records},indent=2))

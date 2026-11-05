import bpy, math, random, json, os
from mathutils import Vector
random.seed(74)
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=ROOT+'/public/assets/models'; os.makedirs(OUT,exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def mat(n,c,metal=0,rough=.65):
 m=bpy.data.materials.new(n); m.diffuse_color=(*c,1); m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*c,1); p.inputs['Metallic'].default_value=metal; p.inputs['Roughness'].default_value=rough
 return m
blue=mat('paint-turquoise',(.015,.38,.8),.3,.3); red=mat('paint-coral',(.85,.07,.035),.25,.3); dark=mat('rubber',(.035,.045,.05)); steel=mat('wheel-rims',(.17,.22,.24),.65,.35); gold=mat('gold',(.95,.57,.015),.65,.28); wood=mat('warm-timber',(.31,.12,.035)); leaf=mat('foliage',(.17,.39,.045)); pink=mat('sakura',(.98,.27,.48)); white=mat('linen',(.88,.86,.74)); clay=mat('terracotta',(.62,.22,.07))
allassets=[]
def begin():
 bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def cube(n,loc,scale,m,bevel=.06,parent=None):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=n; o.dimensions=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(m)
 if bevel:
  mod=o.modifiers.new('soft manufactured edges','BEVEL'); mod.width=bevel; mod.segments=2
  o.modifiers.new('weighted normals','WEIGHTED_NORMAL')
 o.parent=parent; return o
def sphere(n,loc,scale,m,parent=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,location=loc); o=bpy.context.object; o.name=n; o.scale=scale; o.data.materials.append(m); o.parent=parent
 for p in o.data.polygons:p.use_smooth=True
 return o
def cyl(n,loc,r,d,m,rot=None,parent=None):
 bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=r,depth=d,location=loc);o=bpy.context.object;o.name=n;o.data.materials.append(m)
 if rot:o.rotation_euler=rot
 o.parent=parent; mod=o.modifiers.new('rounded lip','BEVEL');mod.width=.025;mod.segments=2;o.modifiers.new('normals','WEIGHTED_NORMAL');return o
def empty(n,loc=(0,0,0),parent=None):
 o=bpy.data.objects.new(n,None);bpy.context.collection.objects.link(o);o.location=loc;o.parent=parent;return o
def save(id,role='decoration',animations=[]):
 bpy.context.view_layer.update();objects=list(bpy.context.scene.objects); coords=[o.matrix_world@Vector(c) for o in objects if o.type=='MESH' for c in o.bound_box]
 bounds=[[min(v[i] for v in coords) for i in range(3)],[max(v[i] for v in coords) for i in range(3)]] if coords else [[0]*3]*2
 bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/authoring/'+id+'.blend')
 bpy.ops.export_scene.gltf(filepath=OUT+'/'+id+'.glb',export_format='GLB',export_yup=True,export_apply=True)
 lods=[]
 if id[:3] in ['NJD','BSC','JPN'] and id[4:] in ['07','08','09','23']:
  for o in objects:
   if o.type=='MESH':
    dec=o.modifiers.new('mobile LOD','DECIMATE');dec.ratio=.22
  bpy.ops.export_scene.gltf(filepath=OUT+'/'+id+'-LOD1.glb',export_format='GLB',export_yup=True,export_apply=True)
  lods=['assets/models/'+id+'-LOD1.glb']
 allassets.append(dict(id=id,source='authoring/'+id+'.blend',runtime='assets/models/'+id+'.glb',dimensions=[bounds[1][i]-bounds[0][i] for i in [0,2,1]],bounds=[ [bounds[0][0],bounds[0][2],-bounds[1][1]], [bounds[1][0],bounds[1][2],-bounds[0][1]] ],forward='+Z (runtime)',pivot='ground center',collisionRole=role,materials=sorted(set(m.name for o in objects if o.type=='MESH' for m in o.data.materials)),animations=animations,lods=lods,provenance='Original procedural Blender geometry; authoring/build.py'))
def tank(id,m,scale=1):
 begin();root=empty('root');cube('hull',(0,0,.46),(1.03,1.48,.38),m,.13,root);cube('front glacis',(0,.58,.59),(.96,.44,.25),m,.09,root)
 for side in [-1,1]:
  track=empty('leftTrack' if side<0 else 'rightTrack',parent=root)
  cube('track-belt',(side*.55,0,.25),(.27,1.6,.43),dark,.18,track)
  for y in [-.54,-.18,.18,.54]:
   cyl('road wheel',(side*.70,y,.25),.17,.055,steel,(0,math.pi/2,0),track);cyl('hub',(side*.735,y,.25),.075,.06,m,(0,math.pi/2,0),track)
  for y in [i*.13-.72 for i in range(12)]:cube('tread link',(side*.55,y,.455),(.29,.065,.045),steel,.012,track)
  cube('fender',(side*.54,0,.59),(.36,1.55,.12),m,.04,root)
 turret=empty('turret',(0,0,.68),root);sphere('cast turret',(0,0,.12),(.49,.49,.34),m,turret);cyl('hatch',(0,0,.41),.23,.075,m,parent=turret);cyl('hatch inset',(0,0,.46),.11,.035,steel,parent=turret)
 barrel=empty('barrel',(0,.34,.15),turret);cyl('barrel tube',(0,.38,0),.105,.85,m,(math.pi/2,0,0),barrel);cyl('muzzle rim',(0,.82,0),.14,.14,m,(math.pi/2,0,0),barrel);cyl('dark muzzle',(0,.895,0),.097,.006,dark,(math.pi/2,0,0),barrel);empty('muzzleSocket',(0,.91,0),barrel)
 for x in [-.34,.34]:cube('headlight',(x,.75,.54),(.15,.04,.105),gold,.02,root)
 cyl('antenna',(.35,-.32,.99),.014,.7,steel,parent=root);sphere('antenna cap',(.35,-.32,1.34),(.035,)*3,m,root)
 for n,l in [('wheels',(0,0,0)),('hitSocket',(0,0,.6)),('healthAnchor',(0,0,1.65)),('groundShadowAnchor',(0,0,.015))]:empty(n,l,root)
 # Blender +Y forward converts to glTF -Z; rotate canonical root for +Z.
 root.rotation_euler[2]=math.pi;root.scale=(scale,)*3;save(id,'tank')
tank('COM-TANK-01',blue);tank('COM-TANK-02',red);tank('COM-HELPER-01',blue,.65)
begin();cyl('pole',(0,0,.8),.035,1.6,gold);sphere('finial',(0,0,1.65),(.09,)*3,gold)
verts=[];faces=[]
for i in range(13):
 for j in range(5):verts.append((i*.07,math.sin(i*.6)*.06,1.5-j*.14))
for i in range(12):
 for j in range(4):a=i*5+j;faces.append((a,a+5,a+6,a+1))
mesh=bpy.data.meshes.new('cloth');mesh.from_pydata(verts,[],faces);ob=bpy.data.objects.new('cloth',mesh);bpy.context.collection.objects.link(ob);ob.data.materials.append(gold);sol=ob.modifiers.new('cloth thickness','SOLIDIFY');sol.thickness=.012;save('COM-FLAG-01','pickup')
for theme,color in [('NJD',(.68,.39,.15)),('BSC',(.65,.19,.075)),('JPN',(.65,.55,.36))]:
 earth=mat(theme+' masonry',color);stone=mat(theme+' variation',tuple(c*.86 for c in color));roof=mat(theme+' roof',(.11,.16,.2))
 for num in [7,8,9,10,11,23]:
  begin()
  if num==9:
   for i in range(10):o=cube('settled rubble',(random.uniform(-.8,.8),random.uniform(-.8,.8),.12),(.35,.27,.23),earth,.06);o.rotation_euler[2]=random.random()*6
  else:
   for row in range(3 if num!=23 else 4):
    for col in range(4):
     for depth in range(3):
      if num==8 and row==2 and col==1 and depth==0:continue
      if num==10 and col>1 and depth>0:continue
      if num==11 and col not in [1,2] and depth>0:continue
      x=(col-1.5)*.48+random.uniform(-.018,.018); y=(depth-1)*.62; z=.145+row*.275
      o=cube('handmade block',(x,y,z),(.46+random.uniform(-.025,.015),.60,.265),earth if random.random()>.3 else stone,.06)
      o.rotation_euler[2]=random.uniform(-.025,.025)
      if num==8 and depth==0:
       o=cube('fracture',(x+.12,y-.305,z),(.024,.009,.23),dark,.003);o.rotation_euler[1]=.35

  save(f'{theme}-{num:02}', 'wall' if num<12 or num==23 else 'decoration')
 for num in range(12,25):
  if num==23:continue
  begin()
  if num==12:cube('ground',(0,0,-.09),(2,2,.18),earth,.04)
  elif num==13:
   cube('house',(0,0,1.4),(3.1,2.7,2.8),earth,.13);cube('door',(0,-1.37,.65),(.75,.08,1.3),wood,.05)
   if theme=='JPN':
    for side in [-1,1]:o=cube('tiled roof',(side*.8,0,3),(1.9,3.2,.16),roof,.06);o.rotation_euler[1]=side*.42
    for x in [-1.4,0,1.4]:cube('timber frame',(x,-1.39,1.5),(.12,.08,2.8),wood,.02)
   else:
    for x in [-1.4,0,1.4]:cube('parapet',(x,0,2.95),(.4,2.75,.35),earth,.06)
    for x in [-.8,.8]:cube('vent',(x,-1.36,2.15),(.25,.05,.27),dark,.02)
  elif num in [14,15,24]:
   if num==14:
    for x in [-.65,.65]:cube('door post',(x,0,.85),(.18,.24,1.7),wood)
    for i in range(7):cube('door plank',((i-3)*.17,0,.75),(.16,.13,1.5),wood,.02)
    for z in [.25,1.2]:cube('iron brace',(0,-.09,z),(1.2,.06,.08),steel,.01)
   elif num==15:
    cube('crate',(0,0,.5),(1,1,1),wood)
    for z in [.08,.92]:
     for y in [-.51,.51]:cube('frame',(0,y,z),(1.12,.09,.13),clay,.02)
    o=cube('diagonal brace',(0,-.54,.5),(1.25,.08,.13),clay,.02);o.rotation_euler[1]=.75
   elif theme=='JPN':
    sphere('calico body',(0,0,.23),(.48,.29,.23),white);sphere('head',(.35,-.1,.28),(.22,)*3,clay)
    for x in [.24,.44]:o=cube('ear',(x,-.12,.48),(.12,.1,.18),white,.03);o.rotation_euler[1]=.3
   else:
    for x in [-1,1]:
     for y in [-.7,.7]:cyl('shelter post',(x,y,1),.065,2,wood)
    cube('cloth canopy',(0,0,2.1),(2.5,1.9,.13),red,.05)
  elif num==16:
   for x,y,s in [(-.3,0,1),(.35,.2,.75),(0,-.45,.5)]:
    sphere('pot',(x,y,s*.35),(.3*s,.3*s,.38*s),clay);cyl('rim',(x,y,s*.7),.17*s,.08,clay);cyl('opening',(x,y,s*.745),.12*s,.01,dark)
  elif num in [17,18,19]:
   if num==17:
    cyl('trunk',(0,0,1.1),.15,2.2,wood)
    if theme=='JPN':
     for i in range(18):a=random.random()*6.28;r=random.random();sphere('blossom cluster',(math.cos(a)*r,math.sin(a)*r,2+random.random()*.8),(.38,.35,.32),pink)
    else:
     for i in range(12):a=i*math.pi/6;o=sphere('palm frond',(math.cos(a)*.62,math.sin(a)*.62,2.2),(.95,.12,.08),leaf);o.rotation_euler=(0,.25,a)
     for i in range(7):cyl('trunk ring',(0,0,.2+i*.27),.18,.08,clay)
   elif num==18 and theme=='JPN':
    for i in range(6):
     x=random.uniform(-.5,.5);y=random.uniform(-.4,.4)
     for j in range(7):cyl('bamboo segment',(x,y,j*.28+.14),.055,.26,leaf)
   else:
    if num==19:cube('garden bed',(0,0,.07),(1.8,1.6,.14),wood)
    for i in range(18):x=random.uniform(-.7,.7);y=random.uniform(-.6,.6);o=sphere('leaf',(x,y,.16),(.08,.25,.05),leaf);o.rotation_euler=(.7,0,random.random()*6)
  elif num==20:
   water=mat(theme+' water',(.03,.43,.62),.15,.22);cube('water',(0,0,.04),(1.5,3,.08),water)
   for x in [-.9,.9]:
    for y in [-1.2,-.6,0,.6,1.2]:cube('water bank',(x,y,.13),(.3,.55,.25),earth)
   if theme=='JPN':
    for y in [-.6,0,.6]:sphere('koi',(0,y,.11),(.08,.2,.035),red)
  elif num==21:
   if theme=='NJD':
    cube('woven mat',(0,0,.035),(1.8,1.25,.07),red,.025);sphere('basket',(0,0,.2),(.32,.3,.18),wood)
    for i in range(12):sphere('dates',(random.uniform(-.2,.2),random.uniform(-.2,.2),.35),(.06,.04,.045),clay)
   else:
    for i in range(11):cube('bridge plank',(0,(i-5)*.2,.25),(2,.185,.12),wood,.03)
    for x in [-.9,.9]:cube('handrail',(x,0,.8),(.08,2.5,.1),wood,.03)
  elif num==22:
   if theme=='BSC':
    for i in range(6):sphere('rock',(random.uniform(-.6,.6),random.uniform(-.5,.5),.2),(.3,.25,.3),earth)
   else:
    for x in ([-.35,.35] if theme=='NJD' else [0]):
     sphere('robe',(x,0,.4),(.2,.2,.4),white if theme=='NJD' else blue);sphere('head',(x,0,.9),(.18,)*3,clay)
     cyl('hat',(x,0,1.06),.22,.09,red if theme=='NJD' else wood)
  save(f'{theme}-{num:02}')
for i,c in enumerate([blue,gold,red,leaf,blue],1):
 begin();sphere('power core',(0,0,.38),(.3,.18,.35),c);cyl('pickup plinth',(0,0,.07),.38,.1,gold);save(f'COM-POWER-{i:02}','pickup')
for id in ['COM-PROJECTILE-01','COM-PROJECTILE-02','COM-SHIELD-01','COM-FX-MUZZLE','COM-FX-HIT','COM-FX-WALL-CRACK','COM-FX-DUST','COM-FX-REBUILD','COM-TRACK-DECAL','COM-RESPAWN-01','COM-FLAG-SPAWN-01']:
 begin();sphere('effect',(0,0,.1),(.09,.16,.09),gold);save(id,'cosmetic')
json.dump({'version':1,'assets':allassets},open(ROOT+'/public/assets/manifest.json','w'),indent=2)

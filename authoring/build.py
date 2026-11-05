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
blue=mat('paint-turquoise',(.015,.38,.8),.18,.46); red=mat('paint-coral',(.85,.07,.035),.18,.46); dark=mat('rubber',(.035,.045,.05)); steel=mat('wheel-rims',(.17,.22,.24),.65,.35); gold=mat('gold',(.95,.57,.015),.65,.28); wood=mat('warm-timber',(.31,.12,.035)); leaf=mat('foliage',(.17,.39,.045)); pink=mat('sakura',(.98,.27,.48)); white=mat('linen',(.88,.86,.74)); clay=mat('terracotta',(.62,.22,.07))
skin=mat('warm skin',(.84,.5,.28),0,.8)
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
 bpy.ops.mesh.primitive_uv_sphere_add(segments=8 if n=='date cluster' else 16,ring_count=4 if n=='date cluster' else 8,location=loc); o=bpy.context.object; o.name=n; o.scale=scale; o.data.materials.append(m); o.parent=parent
 for p in o.data.polygons:p.use_smooth=True
 return o
def cyl(n,loc,r,d,m,rot=None,parent=None):
 bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=d,location=loc);o=bpy.context.object;o.name=n;o.data.materials.append(m)
 if rot:o.rotation_euler=rot
 o.parent=parent; mod=o.modifiers.new('rounded lip','BEVEL');mod.width=.025;mod.segments=2;o.modifiers.new('normals','WEIGHTED_NORMAL');return o
def empty(n,loc=(0,0,0),parent=None):
 o=bpy.data.objects.new(n,None);bpy.context.collection.objects.link(o);o.location=loc;o.parent=parent;return o
def save(id,role='decoration',animations=[]):
 bpy.context.view_layer.update();objects=list(bpy.context.scene.objects); coords=[o.matrix_world@Vector(c) for o in objects if o.type=='MESH' for c in o.bound_box]
 bounds=[[min(v[i] for v in coords) for i in range(3)],[max(v[i] for v in coords) for i in range(3)]] if coords else [[0]*3]*2
 animations=list(animations)
 animated=[o for o in objects if o.name.startswith(('frond ','robe','calico body'))]
 for index,o in enumerate(animated):
  base=o.rotation_euler.y
  for frame,delta in [(1,0),(61,.025 if index%2 else -.025),(121,0)]:
   o.rotation_euler.y=base+delta;o.keyframe_insert(data_path='rotation_euler',frame=frame)
  if o.animation_data and o.animation_data.action:o.animation_data.action.name=id+'-ambient-'+str(index);animations.append(o.animation_data.action.name)
 bpy.context.scene.frame_end=120;bpy.context.scene.frame_set(1)
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
  for y in [-.58,-.29,0,.29,.58]:
   cyl('road wheel',(side*.70,y,.25),.17,.055,steel,(0,math.pi/2,0),track);cyl('hub',(side*.735,y,.25),.075,.06,m,(0,math.pi/2,0),track)
  for y in [i*.13-.72 for i in range(12)]:
   link=cube('tread link',(side*.55,y,.455),(.29,.065,.045),steel,.012,track);link.modifiers[0].segments=1
  cube('fender',(side*.54,0,.59),(.36,1.55,.12),m,.04,root)
 turret=empty('turret',(0,0,.68),root);sphere('cast turret',(0,0,.12),(.45,.45,.26),m,turret);cyl('hatch',(0,0,.41),.23,.075,m,parent=turret);cyl('hatch inset',(0,0,.46),.11,.035,steel,parent=turret)
 barrel=empty('barrel',(0,.34,.15),turret);cyl('barrel tube',(0,.38,0),.105,.85,m,(math.pi/2,0,0),barrel);cyl('muzzle rim',(0,.82,0),.14,.14,m,(math.pi/2,0,0),barrel);cyl('dark muzzle',(0,.895,0),.097,.006,dark,(math.pi/2,0,0),barrel);empty('muzzleSocket',(0,.91,0),barrel)
 for x in [-.34,.34]:cube('headlight',(x,.75,.54),(.15,.04,.105),gold,.02,root)
 # Dimensional team insignia, edge highlights and side storage.
 accent=mat('paint highlight '+id, (.06,.63,.95) if m==blue else (.98,.25,.06),.12,.48)
 for side in [-1,1]:
  cube('storage box',(side*.51,-.27,.69),(.22,.42,.18),accent,.035,root)
  for y in [-.39,-.16]:cube('box latch',(side*.635,y,.69),(.016,.06,.07),steel,.007,root)
  for y in [-.55,.3]:cube('edge wear',(side*.59,y,.656),(.17,.025,.009),accent,.004,root)
 if m==blue:
  cyl('team roundel',(0,.485,.17),.11,.025,white,(math.pi/2,0,0),turret)
 else:
  emblem=cube('team diamond',(0,.485,.17),(.17,.025,.17),white,.012,turret);emblem.rotation_euler[1]=math.pi/4
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
   # Two staggered courses, hand-shaped blocks; full 2m footprint.
   courses=3 if num==23 else 2
   palette=[mat(theme+' block tint '+str(i),tuple(min(1,c*(.82+i*.035)) for c in color),0,.94) for i in range(9)]
   for row in range(courses):
    for col in range(4):
     for depth in range(2):
      if num==10 and col>1 and depth>0:continue
      if num==11 and col not in [1,2] and depth>0:continue
      x=(col-1.5)*.48; y=(depth-.5)*.94; z=.205+row*.405
      o=cube('hand-shaped masonry',(x,y,z),(.465,.915,.395),random.choice(palette),.065)
      o.modifiers[0].segments=1
      for v in o.data.vertices:
       v.co.x+=random.uniform(-.018,.018);v.co.y+=random.uniform(-.025,.025);v.co.z+=random.uniform(-.018,.018)
      o.rotation_euler[2]=random.uniform(-.018,.018)
      if num==8:
       # Jagged dimensional crack on front and top, aligned with intact pivot.
       for part in range(3):
        crack=cube('jagged fracture',(x+.08+(.028 if part%2 else -.028),y-.463,z-.12+part*.09),(.025,.012,.12),dark,.004)
        crack.rotation_euler[1]=(-1 if part%2 else 1)*.35
   if num==23:
    cube('boundary cap',(0,0,1.24),(1.98,1.92,.14),palette[5],.045)

  save(f'{theme}-{num:02}', 'wall' if num<12 or num==23 else 'decoration')
 for num in range(12,25):
  if num==23:continue
  begin()
  if num==12:cube('ground',(0,0,-.09),(2,2,.18),earth,.04)
  elif num==13:
   cube('house',(0,0,1.4),(3.1,2.7,2.8),earth,.2);cube('door',(0,-1.37,.65),(.75,.08,1.3),wood,.05)
   if theme=='JPN':
    for side in [-1,1]:o=cube('tiled roof',(side*.8,0,3),(1.9,3.2,.16),roof,.06);o.rotation_euler[1]=side*.42
    for x in [-1.4,0,1.4]:cube('timber frame',(x,-1.39,1.5),(.12,.08,2.8),wood,.02)
   else:
    for y in [-1.25,1.25]:cube('parapet edge',(0,y,2.95),(3.1,.24,.4),earth,.065)
    for x in [-1.4,1.4]:cube('parapet side',(x,0,2.95),(.25,2.6,.4),earth,.065)
    for x in [-1.4,1.4]:
     for y in [-1.25,1.25]:cube('raised corner',(x,y,3.15),(.4,.4,.45),stone,.07)
    for x in [-.85,0,.85]:
     mesh=bpy.data.meshes.new('triangular vent');mesh.from_pydata([(x-.14,-1.36,2.1),(x+.14,-1.36,2.1),(x,-1.36,2.4)],[],[(0,1,2)]);ob=bpy.data.objects.new('triangular ventilation',mesh);bpy.context.collection.objects.link(ob);ob.data.materials.append(dark)
    for x in [-1.2,-.6,0,.6,1.2]:cube('rafter end',(x,-1.49,2.65),(.11,.42,.1),wood,.025)
    for i in range(6):cube('door plank',((i-2.5)*.12,-1.43,.65),(.11,.065,1.25),wood,.02)
    for z in [.25,.95]:cube('door strap',(0,-1.48,z),(.73,.045,.06),steel,.01)
    cube('window',(1,-1.37,1.05),(.45,.04,.6),dark,.05)
    for x in [.8,1,1.2]:cube('window timber',(x,-1.42,1.05),(.035,.035,.6),wood,.008)
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
    cube('red cushion',(0,0,.06),(1.15,.85,.12),red,.14)
    for j in range(12):a=j*2.4;sphere('cushion motif',(math.sin(a)*.45,math.cos(a)*.3,.13),(.035,.035,.012),white)
    sphere('calico patch',(-.1,0,.31),(.32,.27,.2),dark)
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
     # Curved frond spines and individual pointed leaflets, not flattened ellipsoids.
     for i in range(10):
      a=i*math.pi/5;frond=empty('frond '+str(i),(0,0,2.1))
      for j in range(7):
       t=(j+1)/7;r=t*1.45;z=.45*math.sin(t*math.pi)-t*.25
       for side in [-1,1]:
        ox=math.cos(a)*r;oy=math.sin(a)*r
        points=[(ox,oy,z),(ox+math.cos(a+side*1.0)*.48*(1-t*.5),oy+math.sin(a+side*1.0)*.48*(1-t*.5),z-.10),(ox+math.cos(a)*.17,oy+math.sin(a)*.17,z+.025)]
        mesh=bpy.data.meshes.new('palm leaflet');mesh.from_pydata(points,[],[(0,1,2)]);ob=bpy.data.objects.new('pointed leaflet',mesh);bpy.context.collection.objects.link(ob);ob.parent=frond;ob.data.materials.append(leaf);sol=ob.modifiers.new('leaf thickness','SOLIDIFY');sol.thickness=.012
     for i in range(9):
      z=.15+i*.22
      for j in range(7):
       a=j*math.pi*2/7+(i%2)*.4;o=cube('diamond trunk scale',(math.cos(a)*.15,math.sin(a)*.15,z),(.13,.08,.18),wood,.025);o.rotation_euler=(0,.3,a);o.modifiers[0].segments=1
     for i in range(14):a=i*2.4;sphere('date cluster',(math.cos(a)*.26,math.sin(a)*.26,1.85-i%3*.08),(.07,.07,.12),clay)

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
    for index,x in enumerate([-.4,.4] if theme=='NJD' else [0]):
     sphere('robe',(x,0,.4),(.22,.2,.32),white if theme=='NJD' else blue)
     for side in [-1,1]:
      sphere('crossed leg',(x+side*.16,-.16,.16),(.24,.13,.11),white if theme=='NJD' else dark)
      arm=sphere('arm',(x+side*.22,-.08,.48),(.09,.10,.22),white if theme=='NJD' else blue);arm.rotation_euler[1]=side*.65
      sphere('hand',(x+side*.23,-.18,.4),(.075,)*3,skin)
     sphere('head',(x,-.015,.86),(.23,.2,.24),skin)
     for side in [-1,1]:
      sphere('ear',(x+side*.22,0,.86),(.06,.045,.08),skin)
      sphere('friendly eye',(x+side*.075,-.204,.89),(.027,.012,.035),dark)
      sphere('eye highlight',(x+side*.069,-.217,.903),(.009,.004,.01),white)
     cube('smile',(x,-.211,.79),(.075,.01,.018),wood,.008)
     if theme=='NJD':
      cyl('cap',(x,0,1.06),.225,.1,white)
      if index==0:
       cube('shemagh',(x,.035,1.05),(.5,.39,.07),white,.04)
       for j in range(7):
        cube('shemagh red weave',(x+(j-3)*.067,.035,1.089),(.026,.37,.007),red,.003)
        cube('shemagh cross weave',(x,.035+(j-3)*.052,1.091),(.48,.022,.007),red,.003)
       cyl('igal',(x,0,1.1),.23,.035,dark)
     else:
      bpy.ops.mesh.primitive_cone_add(vertices=24,radius1=.39,radius2=.025,depth=.22,location=(x,0,1.15));bpy.context.object.name='conical straw hat';bpy.context.object.data.materials.append(wood)
      cyl('watering can',(x+.34,-.25,.35),.12,.22,steel)
      spout=cyl('watering spout',(x+.53,-.27,.4),.035,.27,steel,(0,math.pi/3,0))

  save(f'{theme}-{num:02}')
purple=mat('auto purple',(.39,.04,.65),.15,.38)
for i,c in enumerate([blue,red,white,purple,blue],1):
 begin();badge=cube('rounded badge',(0,0,.4),(.72,.16,.72),c,.15);cyl('base ring',(0,0,.055),.42,.09,gold)
 if i==1:
  points=[(-.23,-.1,.63),(.23,-.1,.63),(.2,-.1,.31),(0,-.1,.16),(-.2,-.1,.31)];mesh=bpy.data.meshes.new('shield');mesh.from_pydata(points,[],[(0,1,2,3,4)]);o=bpy.data.objects.new('shield heraldry',mesh);bpy.context.collection.objects.link(o);o.data.materials.append(white);o.modifiers.new('shield thickness','SOLIDIFY').thickness=.04
 elif i==2:
  for x in [-.2,0,.2]:cyl('bullet',(x,-.12,.4),.06,.34,gold);sphere('bullet tip',(x,-.12,.59),(.06,.06,.1),gold)
 elif i==3:
  cyl('rocket body',(0,-.13,.4),.1,.38,red);sphere('rocket nose',(0,-.13,.64),(.1,.1,.16),red);cube('rocket fins',(0,-.13,.25),(.35,.08,.14),red,.035)
 elif i==4:
  for j in range(5):a=j*math.pi*2/5;cyl('barrel cluster',(math.cos(a)*.18,-.15,.4+math.sin(a)*.18),.065,.12,steel,(math.pi/2,0,0))
 else:
  cube('mini hull',(0,-.14,.36),(.46,.18,.25),blue,.06);sphere('mini turret',(0,-.19,.53),(.17,.1,.13),blue);cyl('mini cannon',(0,-.3,.53),.04,.3,blue,(math.pi/2,0,0))
 save(f'COM-POWER-{i:02}','pickup')

for id in ['COM-PROJECTILE-01','COM-PROJECTILE-02','COM-SHIELD-01','COM-FX-MUZZLE','COM-FX-HIT','COM-FX-WALL-CRACK','COM-FX-DUST','COM-FX-REBUILD','COM-TRACK-DECAL','COM-RESPAWN-01','COM-FLAG-SPAWN-01']:
 begin();sphere('effect',(0,0,.1),(.09,.16,.09),gold);save(id,'cosmetic')
json.dump({'version':1,'assets':allassets},open(ROOT+'/public/assets/manifest.json','w'),indent=2)

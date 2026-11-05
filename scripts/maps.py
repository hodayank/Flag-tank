import random,json,os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));random.seed(43)
# Randomized depth-first maze on odd cells; rotational union of open passages preserves connectivity.
open_cells={(1,1)};stack=[(1,1)]
while stack:
 x,y=stack[-1];ns=[(x+dx,y+dy,dx,dy) for dx,dy in [(2,0),(-2,0),(0,2),(0,-2)] if 1<=x+dx<=25 and 1<=y+dy<=15 and (x+dx,y+dy) not in open_cells]
 if not ns:stack.pop();continue
 nx,ny,dx,dy=random.choice(ns);open_cells.update([(nx,ny),(x+dx//2,y+dy//2)]);stack.append((nx,ny))
# Use intersection of symmetric wall patterns: every original corridor remains connected.
open_cells|={(26-x,16-y) for x,y in list(open_cells)}
for sx,sy in [(1,15),(25,1)]:
 for x in range(max(1,sx-1),min(25,sx+1)+1):
  for y in range(max(1,sy-1),min(15,sy+1)+1):open_cells.add((x,y))
# Add symmetric safe dead-end wall islands only when all free cells stay connected.
def connected(cells):
 seen={next(iter(cells))};todo=list(seen)
 while todo:
  x,y=todo.pop()
  for q in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
   if q in cells and q not in seen:seen.add(q);todo.append(q)
 return len(seen)==len(cells)
candidates=list(open_cells);random.shuffle(candidates)
for q in candidates:
 if len(open_cells)<=207:break
 r=(26-q[0],16-q[1]);removed={q,r}
 if any(abs(x-sx)<=1 and abs(y-sy)<=1 for x,y in removed for sx,sy in [(1,15),(25,1)]):continue
 trial=open_cells-removed
 if connected(trial):open_cells=trial
walls=[(x,y) for y in range(1,16) for x in range(1,26) if (x,y) not in open_cells]
for theme,prefix in [('najdi','NJD'),('basic','BSC'),('japan','JPN')]:
 dec=[]
 def place(n,x,z,yaw=0,scale=1):dec.append(dict(asset=f'{prefix}-{n:02}',position=[x,0,z],rotation=yaw,scale=scale,animation='ambient'))
 for z in [-21.5,21.5]:
  for x in [-23,-12,0,12,23]:
   place(13,x,z,0 if z<0 else 3.14159);place(16,x+2,z);place(18,x-2,z)
 for x in [-31,31]:
  for z in [-13,-5,6,14]:place(17,x,z,scale=1.2)
  for z in [-10,1,11]:place(18,x,z)
 if theme=='najdi':
  place(21,-32,4);place(22,-32,4);place(24,-31,-12)
  for z in [-8,-4,0,4]:place(19,31,z)
  for z in [-7,-4,-1,2,5]:place(20,34,z)
  place(24,29,16);place(15,30,14)
 elif theme=='japan':
  place(20,19,-21.5);place(21,19,-21.5);place(22,-32,4);place(19,-32,2);place(24,11,21.5)
  for x in [-30,30]:place(18,x,0)
 else:
  place(20,-30,0);place(21,-30,0)
  for x in [-30,30]:
   for z in [-10,0,10]:place(19,x,z);place(22,x+1,z+2);place(24,x,z+3)

 data=dict(version=1,id=theme+'-01',columns=27,rows=17,units=2,spawns=[[1,15],[25,1]],walls=[dict(cell=list(q),asset=f'{prefix}-07') for q in walls],boundary=dict(min=[-27,-17],max=[27,17],asset=f'{prefix}-23'),flagCandidates=[list(q) for q in sorted(open_cells) if 4<q[0]<22 and 2<q[1]<14],powerupCandidates=[list(q) for q in sorted(open_cells)],decorations=dec)
 json.dump(data,open(root+'/public/maps/'+theme+'-01.json','w'),indent=2)
print('wall density',len(walls)/375,'connected',connected(open_cells))

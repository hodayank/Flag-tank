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
 for i,(x,z,n) in enumerate([(-28,-12,13),(28,10,13),(-28,10,17),(28,-12,17),(-20,-19,20),(20,19,19),(-10,-19,21),(10,19,22),(-29,0,18),(29,0,16),(-20,19,24),(20,-19,15)]):dec.append(dict(asset=f'{prefix}-{n:02}',position=[x,0,z],rotation=0,scale=1,animation='ambient'))
 data=dict(version=1,id=theme+'-01',columns=27,rows=17,units=2,spawns=[[1,15],[25,1]],walls=[dict(cell=list(q),asset=f'{prefix}-07') for q in walls],boundary=dict(min=[-27,-17],max=[27,17],asset=f'{prefix}-23'),flagCandidates=[list(q) for q in sorted(open_cells) if 4<q[0]<22 and 2<q[1]<14],powerupCandidates=[list(q) for q in sorted(open_cells)],decorations=dec)
 json.dump(data,open(root+'/public/maps/'+theme+'-01.json','w'),indent=2)
print('wall density',len(walls)/375,'connected',connected(open_cells))

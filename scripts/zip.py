import os,sys,zipfile
root,out,web,kh,source=sys.argv[1:]
def zipdir(target,folder,prefix='',exclude=set()):
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for base,dirs,files in os.walk(folder):
   dirs[:]=sorted(d for d in dirs if d not in exclude)
   for f in sorted(files):
    if f.endswith(('.blend1','.log')):continue
    p=os.path.join(base,f);rel=os.path.relpath(p,folder)
    if '.git' in rel.split(os.sep):continue
    z.write(p,os.path.join(prefix,rel))
zipdir(out+'/'+web,root+'/dist','tank-flags-web')
zipdir(out+'/'+kh,root+'/dist')
zipdir(out+'/'+source,root,'tank-flags',{'node_modules','dist','artifacts','.git'})
# Re-read final archives and verify every packaged distributable hash.
import hashlib,json
for p,prefix in [(out+'/'+web,'tank-flags-web/'),(out+'/'+kh,'')]:
 with zipfile.ZipFile(p) as z:
  integrity=json.loads(z.read(prefix+'integrity.json'))
  for name,h in integrity['files'].items():assert hashlib.sha256(z.read(prefix+name)).hexdigest()==h,name
print('Final archive integrity verified')

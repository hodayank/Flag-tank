import json,os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));out=root+'/public/config/schemas';os.makedirs(out,exist_ok=True)
for name in ['balance','camera-settings','visual-settings','audio-settings']:
 d=json.load(open(root+'/public/config/'+name+'.json'));props={k:dict(type='number',exclusiveMinimum=0,maximum=10000,description='Trial default; seconds/meters/radians or linear gain as documented in README.') for k in d};props['version']={'const':1};json.dump({'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','required':list(d),'additionalProperties':False,'properties':props},open(out+'/'+name+'.schema.json','w'),indent=2)

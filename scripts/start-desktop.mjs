import {spawn} from 'node:child_process';import {existsSync} from 'node:fs';
if(!existsSync('dist/index.html')){console.error('Run npm run build first.');process.exit(1);}
const children=[];let stopping=false;function stop(code=0){if(stopping)return;stopping=true;for(const child of children)child.kill();process.exitCode=code;}
for(const args of [['--import','tsx','src/relay.ts'],['node_modules/vite/bin/vite.js','preview','--host','0.0.0.0','--port','4173','--strictPort']]){const p=spawn(process.execPath,args,{stdio:'inherit'});children.push(p);p.on('error',e=>{console.error(e.message);stop(1);});p.on('exit',code=>{if(!stopping)stop(code??1);});}
process.on('SIGINT',()=>stop());process.on('SIGTERM',()=>stop());console.log('Tank Flags Najdi desktop trial: http://localhost:4173 — Ctrl+C to stop.');

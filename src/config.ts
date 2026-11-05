import {digestBytes} from './hash';
export type Balance = typeof import('../public/config/balance.json');
export type Cell=[number,number];
export interface GameMap {version:number;id:string;columns:number;rows:number;units:number;spawns:Cell[];walls:{cell:Cell;asset:string}[];boundary:{min:number[];max:number[];asset:string};flagCandidates:Cell[];powerupCandidates:Cell[];decorations:{asset:string;position:[number,number,number];rotation:number;scale:number;animation:string}[]}
export const center=([c,r]:Cell)=>({x:(c-13)*2,z:(r-8)*2});
export function validateBalance(v:unknown):asserts v is Balance {if(!v||typeof v!=='object')throw Error('Invalid balance');for(const [k,n] of Object.entries(v)){if(typeof n!=='number'||!Number.isFinite(n)||n<=0||n>10000)throw Error('Invalid balance '+k);}if((v as Balance).version!==1)throw Error('Unsupported balance');}
export function validateMap(m:GameMap){if(m.version!==1||m.columns!==27||m.rows!==17||m.units!==2||m.spawns.length!==2)throw Error('Unsupported map');const seen=new Set<string>();for(const {cell} of m.walls){if(cell.some(n=>!Number.isInteger(n))||cell[0]<1||cell[0]>25||cell[1]<1||cell[1]>15||seen.has(cell.join()))throw Error('Invalid wall');seen.add(cell.join());}for(const q of [...m.spawns,...m.flagCandidates,...m.powerupCandidates]){if(q[0]<1||q[0]>25||q[1]<1||q[1]>15||seen.has(q.join()))throw Error('Blocked candidate');}for(const p of m.decorations){if(Math.abs(p.position[0])<27&&Math.abs(p.position[2])<17)throw Error('Decoration in arena');}}
export async function loadJSON<T>(path:string):Promise<T>{const r=await fetch('./'+path);if(!r.ok)throw Error(`Missing ${path}`);return r.json();}
export async function hash(value:unknown){return digestBytes(new TextEncoder().encode(JSON.stringify(value)).buffer);}

export function validateSettings(v:unknown){if(!v||typeof v!=="object")throw Error("Invalid settings");for(const [k,n] of Object.entries(v)){if(typeof n!=="number"||!Number.isFinite(n)||n<0||n>10000)throw Error("Invalid setting "+k);}if((v as {version:number}).version!==1)throw Error("Unsupported settings version");}

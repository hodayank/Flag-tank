/** Proposed game-side Kids Hug contract. No native host implementation was supplied. */
export interface HostCapabilities {apiVersion:1;invitations:boolean;rooms:boolean;authenticatedTransport:boolean;save:boolean;lifecycle:boolean;audioCap:boolean}
export interface HostPlayer {id:string;displayName:string}
export interface KidsHugHost {handshake(gameId:string,version:string):Promise<HostCapabilities>;localPlayer():Promise<HostPlayer>;createRoom(options:{seats:2;gameId:string}):Promise<{roomId:string}>;invite(roomId:string):Promise<void>;respond(invitationId:string,accept:boolean):Promise<void>;send(roomId:string,packet:unknown,mode:'reliable'|'latest'):void;subscribe(event:string,callback:(data:unknown)=>void):()=>void;save(key:string,value:unknown):Promise<void>;load(key:string):Promise<unknown>;exit():void}
export class MockHost {readonly label='Isolated development mock — no native discovery';private store=new Map<string,unknown>();async save(k:string,v:unknown){this.store.set('kids-hug.tank-flags:'+k,v);}async load(k:string){return this.store.get('kids-hug.tank-flags:'+k);}}
declare global {interface Window {KidsHug?:KidsHugHost}}

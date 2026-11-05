/** Kids Hug proposed v1.0-draft.1. Not evidence of a deployed native SDK. */
export type ThemeId='najdi'|'basic'|'japan';
export type HostErrorCode='ROOM_FULL'|'INVITE_EXPIRED'|'VERSION_MISMATCH'|'STALE_REVISION'|'LOCAL_NETWORK_UNAVAILABLE'|'PERMISSION_DENIED'|'ASSET_LOAD_FAILED'|'PEER_DISCONNECTED'|'UNSUPPORTED_API';
export class HostError extends Error {constructor(public code:HostErrorCode,message:string){super(message);}}
export interface PlayerInfo{id:string;displayName:string;slot:0|1;connected:boolean;ready:boolean}
export interface HostInfo{apiVersion:'1.0-draft.1';capabilities:{invitations:boolean;rooms:boolean;authenticatedPackets:boolean;latest:boolean;persistence:boolean};volumeCap:number;locale:string}
export interface Setup{mapId:string;themeId:ThemeId;durationSec:180|300;buildHash:string;configHash:string;mapHash:string}
export interface RoomState{roomId:string;revision:number;authorityPlayerId:string;status:'inviting'|'lobby'|'countdown'|'playing'|'paused'|'ended'|'closed';players:PlayerInfo[];capacity:2;setup:Setup}
export interface HostPacket{roomId:string;senderPlayerId:string;channel:'reliable'|'latest';bytes:Uint8Array}
export interface Invitation{id:string;roomId:string;sender:PlayerInfo;expiresAt:number}
export type Unsubscribe=()=>void;
export interface KidsHugGameHostV1{
 initialize(gameId:'kids-hug.tank-flags',apiVersion:'1.0-draft.1'):Promise<HostInfo>;
 getLocalPlayer():Promise<PlayerInfo>;
 createRoom(setup:Setup):Promise<RoomState>;
 sendInvitation(roomId:string):Promise<Invitation>;
 respondToInvitation(id:string,accept:boolean):Promise<RoomState|null>;
 cancelInvitation(id:string):Promise<void>;
 proposeSetup(roomId:string,revision:number,setup:Setup):Promise<RoomState>;
 setReady(roomId:string,revision:number,ready:boolean):Promise<RoomState>;
 startMatch(roomId:string,revision:number):Promise<void>;
 sendPacket(packet:Omit<HostPacket,'senderPlayerId'>):void;
 requestPause(roomId:string,paused:boolean):Promise<void>;
 leaveRoom(roomId:string):Promise<void>;
 onInvitation(callback:(invite:Invitation)=>void):Unsubscribe;
 onRoomState(callback:(room:RoomState)=>void):Unsubscribe;
 onMatchStart(callback:(start:{roomId:string;matchId:string;seed:number;startTick:number;setup:Setup})=>void):Unsubscribe;
 onPacket(callback:(packet:HostPacket)=>void):Unsubscribe;
 onLifecycle(callback:(event:'pause'|'resume'|'background'|'exit')=>void):Unsubscribe;
 onVolumeCap(callback:(volume:{cap:number;muted:boolean})=>void):Unsubscribe;
 saveGameData(key:'preferences'|'aggregate-stats',data:Record<string,string|number|boolean>):Promise<void>;
 loadGameData(key:'preferences'|'aggregate-stats'):Promise<Record<string,string|number|boolean>|null>;
 exitGame():void;
}
const methods=['initialize','getLocalPlayer','createRoom','sendInvitation','respondToInvitation','cancelInvitation','proposeSetup','setReady','startMatch','sendPacket','requestPause','leaveRoom','onInvitation','onRoomState','onMatchStart','onPacket','onLifecycle','onVolumeCap','saveGameData','loadGameData','exitGame'] as const;
/** Injection only: no window Android interface, eval, postMessage or filesystem access. */
export class NativeHostAdapter{
 private subscriptions:Unsubscribe[]=[];private room:RoomState|null=null;
 constructor(private host:KidsHugGameHostV1){for(const method of methods)if(typeof host?.[method]!=='function')throw new HostError('UNSUPPORTED_API','Required host method missing: '+method);}
 async initialize(){const info=await this.host.initialize('kids-hug.tank-flags','1.0-draft.1');if(info.apiVersion!=='1.0-draft.1'||!info.capabilities.rooms||!info.capabilities.authenticatedPackets||!Number.isFinite(info.volumeCap)||info.volumeCap<0||info.volumeCap>1)throw new HostError('UNSUPPORTED_API','Compatible rooms, authenticated packets and volume cap required');this.subscriptions.push(this.host.onRoomState(room=>{if(room.capacity!==2||room.players.length>2||!Number.isSafeInteger(room.revision))throw new HostError('VERSION_MISMATCH','Invalid host room state');this.room=room;}));return info;}
 onPacket(callback:(packet:HostPacket)=>void){const off=this.host.onPacket(packet=>{if(!this.room||packet.roomId!==this.room.roomId||!this.room.players.some(p=>p.id===packet.senderPlayerId)||!(packet.bytes instanceof Uint8Array)||packet.bytes.length>65536)return;callback(packet);});this.subscriptions.push(off);return off;}
 async dispose(){this.subscriptions.splice(0).forEach(off=>off());if(this.room)await this.host.leaveRoom(this.room.roomId);this.room=null;}
}

import type {Input} from './simulation';
export class Controls{keys=new Set<string>();edge=[0,0];fire=false;joy={x:0,z:0};private listeners:(()=>void)[]=[];
 constructor(joy:HTMLElement,fire:HTMLElement,onPause:()=>void){const bind=(el:EventTarget,name:string,fn:EventListener)=>{el.addEventListener(name,fn);this.listeners.push(()=>el.removeEventListener(name,fn));};
 bind(window,'keydown',((e:KeyboardEvent)=>{if((e.target as HTMLElement).matches('input,select'))return;if(['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Enter'].includes(e.code))e.preventDefault();if(e.code==='Space'&&!e.repeat)this.edge[0]++;if(e.code==='Enter'&&!e.repeat)this.edge[1]++;this.keys.add(e.code);if(e.code==='Escape')onPause();}) as EventListener);
 bind(window,'keyup',((e:KeyboardEvent)=>{this.keys.delete(e.code);})as EventListener);bind(window,'blur',(()=>{this.clear();onPause();})as EventListener);bind(document,'visibilitychange',(()=>{if(document.hidden){this.clear();onPause();}})as EventListener);
 let jp:number|null=null,fp:number|null=null;
 const update=(e:PointerEvent)=>{const b=joy.getBoundingClientRect(),dx=(e.clientX-b.left-b.width/2)/(b.width*.35),dz=(e.clientY-b.top-b.height/2)/(b.height*.35),l=Math.max(1,Math.hypot(dx,dz));this.joy={x:dx/l,z:dz/l};joy.style.setProperty('--jx',this.joy.x*26+'px');joy.style.setProperty('--jy',this.joy.z*26+'px');};
 bind(joy,'pointerdown',((e:PointerEvent)=>{if(jp!==null)return;jp=e.pointerId;joy.setPointerCapture(jp);update(e);})as EventListener);bind(joy,'pointermove',((e:PointerEvent)=>{if(e.pointerId===jp)update(e);})as EventListener);
 for(const event of ['pointerup','pointercancel','lostpointercapture']){bind(joy,event,((e:PointerEvent)=>{if(e.pointerId===jp){jp=null;this.joy={x:0,z:0};joy.style.setProperty('--jx','0px');joy.style.setProperty('--jy','0px');}})as EventListener);bind(fire,event,((e:PointerEvent)=>{if(e.pointerId===fp){fp=null;this.fire=false;}})as EventListener);}
 bind(fire,'pointerdown',((e:PointerEvent)=>{if(fp!==null)return;fp=e.pointerId;fire.setPointerCapture(fp);this.edge[0]++;this.fire=true;})as EventListener);
 }
 get(player=0):Input{const k=this.keys;return {x:this.joy.x+(player?+k.has('KeyL')-+k.has('KeyJ'):+(k.has('KeyD')||k.has('ArrowRight'))-+(k.has('KeyA')||k.has('ArrowLeft'))),z:this.joy.z+(player?+k.has('KeyK')-+k.has('KeyI'):+(k.has('KeyS')||k.has('ArrowDown'))-+(k.has('KeyW')||k.has('ArrowUp'))),fire:player?k.has('Enter'):this.fire||k.has('Space'),edge:this.edge[player]};}
 clear(){this.keys.clear();this.fire=false;this.joy={x:0,z:0};}
 dispose(){this.clear();this.listeners.forEach(f=>f());}
}

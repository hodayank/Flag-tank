export interface Point{x:number;z:number}
export const distance=(a:Point,b:Point)=>Math.hypot(a.x-b.x,a.z-b.z);
export function circleBox(p:Point,r:number,b:Point,half=1){return Math.hypot(p.x-Math.max(b.x-half,Math.min(p.x,b.x+half)),p.z-Math.max(b.z-half,Math.min(p.z,b.z+half)))<r;}
export function segmentBox(a:Point,b:Point,c:Point,h=1):number|null {let lo=0,hi=1;for(const k of ['x','z'] as const){const d=b[k]-a[k];if(Math.abs(d)<1e-9){if(a[k]<c[k]-h||a[k]>c[k]+h)return null;}else{let t1=(c[k]-h-a[k])/d,t2=(c[k]+h-a[k])/d;if(t1>t2)[t1,t2]=[t2,t1];lo=Math.max(lo,t1);hi=Math.min(hi,t2);if(lo>hi)return null;}}return lo;}
export function segmentCircle(a:Point,b:Point,c:Point,r:number){const dx=b.x-a.x,dz=b.z-a.z,A=dx*dx+dz*dz;if(!A)return distance(a,c)<=r?0:null;const B=2*((a.x-c.x)*dx+(a.z-c.z)*dz),C=(a.x-c.x)**2+(a.z-c.z)**2-r*r,D=B*B-4*A*C;if(C<=0)return 0;if(D<0)return null;const t=(-B-Math.sqrt(D))/(2*A);return t>=0&&t<=1?t:null;}

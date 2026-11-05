import test from 'node:test';import assert from 'node:assert/strict';import {NativeHostAdapter,HostError,type KidsHugGameHostV1} from '../src/host-v1';
test('proposed native adapter rejects incomplete SDK instead of inventing methods',()=>{assert.throws(()=>new NativeHostAdapter({} as KidsHugGameHostV1),(e:Error)=>e instanceof HostError&&e.code==='UNSUPPORTED_API');});

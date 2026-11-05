import {sha256} from '@noble/hashes/sha2.js';
/** Pure JS fallback is needed on non-secure HTTP LAN origins; no credential operations. */
export async function digestBytes(bytes:ArrayBuffer){const digest=globalThis.crypto?.subtle?new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)):sha256(new Uint8Array(bytes));return Array.from(digest).map(n=>n.toString(16).padStart(2,'0')).join('');}

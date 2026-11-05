# Kids Hug integration boundary

No native app source was supplied. `src/host.ts` defines a proposed versioned game-side interface; it is not a claim that an installed APK has a loader or matching SDK. The current game uses a separate browser development relay. A native transport adapter and actual host acceptance remain outstanding.

The host must implement safe package extraction, integrity validation, version negotiation, rollback, updates and uninstall; isolated local asset serving; local identity; eligible-device discovery and invitation delivery even outside the game; atomic two-seat admission; authenticated packet sender metadata; room setup/readiness; authoritative start; coordinated pause and reconnect; namespaced persistence; lifecycle unsubscribe; parent volume cap/mute; safe exit. Native bridge `volume`, `pause`, `exit` subscriptions exist, but handshake/room/transport paths are not connected to the game controller yet.

Use stable game ID `kids-hug.tank-flags`. Package capability `native_local_multiplayer` is false. Do not enable it before two real Kids Hug devices verify host discovery, room admission, matching map/config/asset hashes, shared countdown, identical result, pause/background, authenticated rejoin and cleanup. An app update is needed if the existing APK lacks a compatible loader/SDK.

The development relay hosts the authority instead of trusting a browser to set position or scores. It accepts bounded input intents with sequence and match identifiers; each WebSocket is tied to a seat server-side. Reconnect tokens are private bearer capabilities sent only to their seat, not lobby displays. This development transport needs deployment authentication, TLS, rate limiting and host permission policy before any public use. The game has no text chat and does not access parent PINs, child records, camera, microphone or other games.

The full production contract, exact SDK adapter, native invitation UI states (busy/declined/cancelled/disabled/permission denied) and device acceptance require the actual host implementation. Browser codes and same-keyboard mode must never be presented as native discovery verification.

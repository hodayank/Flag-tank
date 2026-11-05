# v3 decision log

- Preserve functioning simulation and development relay; replace art at stable asset IDs. Do not silently claim that this satisfies creator-side authority or the new SDK transport.
- Keep wallHits=2 pending the owner's optional answer about 2/3/4 hits. It is prominent in balance.json, and renderer damage states now follow the configured maximum rather than hard-coded 2.
- Preserve full geometry in low-quality rendering. The old 22% decimation was visibly destructive and is no longer selected at runtime.
- Version this work as intermediate, not production accepted. All unfinished requirements remain explicit in v3-coverage.md.
- Old downloadable release remains recoverable. Git history can roll back the new revision; do not overwrite old commits or force-push.

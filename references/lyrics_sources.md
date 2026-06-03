# Lyrics Source Configuration

Public Japanese lyrics are usually copyrighted. For an online product, do not scrape and display lyrics from ordinary lyrics websites unless you have permission or a license.

## Recommended Source Order

1. User-provided lyrics: safest for private lesson generation when the user supplies the text.
2. Private/local lyrics library: lyrics you own, have licensed, or have permission to use.
3. Licensed commercial provider: Musixmatch, LyricFind, PetitLyrics/SyncPower, or another provider with terms that allow your use case.
4. Metadata-only fallback: if lyrics cannot be resolved, ask the user to paste lyrics.

## Local Library Schema

Use a local JSONL, JSON, or CSV library. Keep it outside the skill folder for real deployments.

JSONL example:

```json
{"song_title":"セプテンバーさん","artist":"RADWIMPS","language":"ja","lyrics":"...","source":"licensed_internal","license_note":"Internal licensed corpus"}
```

Configure the path with either:

- Environment variable: `JLPT_LYRICS_LIBRARY=C:/path/to/lyrics.jsonl`
- JSON config passed to a future app layer:

```json
{
  "lyrics_library": {
    "type": "local_jsonl",
    "path": "C:/path/to/lyrics.jsonl",
    "match_fields": ["song_title", "artist"]
  }
}
```

## Commercial Provider Notes

- Musixmatch and LyricFind are common licensed lyrics providers for applications that need to display lyrics.
- PetitLyrics/SyncPower is relevant for Japanese synced lyrics, but confirm API access, terms, and display rights.
- JASRAC can help identify rights information for Japanese works, but rights lookup is not the same as permission to reproduce lyrics.

## Product Recommendation

For MVP:

- Store only user-provided lyrics and manually licensed lyrics in your own database.
- Add fields: `song_title`, `artist`, `lyrics`, `source`, `license_status`, `created_at`, `updated_at`.
- Block automatic generation if `license_status` is not `user_provided`, `owned`, or `licensed`.
- Make manual paste a fallback, not the main flow. The main flow should be song lookup against your library.

For commercial launch:

- Add a licensed lyrics provider adapter.
- Cache only what the provider terms allow.
- Keep source attribution and license metadata with every generated document.

## No-Paste User Experience

Use this acquisition order in the app:

1. User enters song title, artist, and target JLPT level.
2. App searches the internal licensed/user-provided lyrics library.
3. If not found, app searches the licensed provider adapter.
4. If still not found, app offers one of these fallback imports:
   - Upload a text file exported from a legal source.
   - Paste lyrics manually.
   - Upload screenshots for OCR only when the user's local use and your jurisdiction/license policy allow it.
5. App stores the result only with explicit `license_status` metadata.

Do not depend on streaming-player lyrics being copyable. Many players intentionally prevent copying because lyrics display rights are separate from music playback rights.

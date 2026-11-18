# Changelog / Änderungsverlauf / История изменений / 变更日志 / 変更履歴

EN: All notable changes are documented here. Format follows Keep a Changelog.
DE: Alle wesentlichen Änderungen sind hier dokumentiert. Format: Keep a Changelog.
RU: Все важные изменения документируются здесь. Формат: Keep a Changelog.
ZH: 所有重要变更均记录于此。格式遵循 Keep a Changelog。
JA: すべての重要な変更をここに記録します。形式は Keep a Changelog に準拠します。

> EN: Entries below are canonical English. Translations of new entries must be added in the same commit — see I18N.md.
> DE: Die Einträge unten sind verbindliches Englisch. Übersetzungen neuer Einträge müssen im selben Commit ergänzt werden — siehe I18N.md.
> RU: Записи ниже являются каноническим английским текстом. Переводы новых записей добавляются в том же коммите — см. I18N.md.
> ZH: 以下条目为权威英文原文。新增条目的翻译必须在同一提交中添加——见 I18N.md。
> JA: 以下の項目は英語が正規原文です。新しい項目の翻訳は同じコミットで追加してください——I18N.md を参照。

## [0.1.0] — draft

### Added

- Wallset: static-only wallpaper pack specification (`SPEC.md`).
- JSON Schema draft 2020-12 for `wallpaper.pack.json`.
- Single JPEG output profile: quality 92, 4:4:4, progressive, sRGB, no metadata.
- Eight aspect profiles: 16:9, 16:10, 21:9, 32:9, 4:3, 5:4, 9:16, 1:1.
- `safe_area` with per-profile overrides for cropping.
- Provenance fields: `own | procedural | ai | mixed`, generator, seed, script.
- Target grammar `<os>[:<de>][@version]` and capability matrix for
  Linux, Windows, macOS, FreeBSD and Haiku.
- CLI `wps` with `validate`, `render`, `pack`, `install`, `capabilities`.
- Reference procedural pack `aurora-night/aurora-01`.
- CI matrix on ubuntu / windows / macOS.

### Explicitly out of scope

- Animated, video, WebGL, interactive and time/sun-based wallpapers.
- Multi-monitor span mode (per-monitor delivery only in v0.1).
- HDR and display-P3 output (sRGB baseline only).

# Changelog / Änderungsverlauf / История изменений / 变更日志 / 変更履歴 / 변경 로그

EN: All notable changes are documented here. Format follows Keep a Changelog.
DE: Alle wesentlichen Änderungen sind hier dokumentiert. Format: Keep a Changelog.
RU: Все важные изменения документируются здесь. Формат: Keep a Changelog.
ZH: 所有重要变更均记录于此。格式遵循 Keep a Changelog。
JA: すべての重要な変更をここに記録します。形式は Keep a Changelog に準拠します。
KO: 모든 주요 변경 사항을 여기에 기록합니다. 형식은 Keep a Changelog를 따릅니다.

> EN: Entries below are canonical English. Translations of new entries must be added in the same commit — see I18N.md.
> DE: Die Einträge unten sind verbindliches Englisch. Übersetzungen neuer Einträge müssen im selben Commit ergänzt werden — siehe I18N.md.
> RU: Записи ниже являются каноническим английским текстом. Переводы новых записей добавляются в том же коммите — см. I18N.md.
> ZH: 以下条目为权威英文原文。新增条目的翻译必须在同一提交中添加——见 I18N.md。
> JA: 以下の項目は英語が正規原文です。新しい項目の翻訳は同じコミットで追加してください——I18N.md を参照。
> KO: 아래 항목은 영어가 정식 원문입니다. 새 항목의 번역은 같은 커밋에서 추가해야 합니다——I18N.md 참조.

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
- Six-language localisation (EN/DE/RU/ZH/JA/KO) for docs, schema descriptions,
  CLI help/output and config templates.
  - DE: Sechs-Sprachen-Lokalisierung (EN/DE/RU/ZH/JA/KO) für Dokumentation,
    Schema-Beschreibungen, CLI-Hilfe/-Ausgaben und Konfigurationsvorlagen.
  - RU: Локализация на шести языках (EN/DE/RU/ZH/JA/KO) для документации,
    описаний схемы, справки/вывода CLI и шаблонов конфигов.
  - ZH: 文档、schema 描述、CLI 帮助/输出与配置模板提供六种语言（EN/DE/RU/ZH/JA/KO）。
  - JA: ドキュメント、スキーマ説明、CLI ヘルプ／出力、設定テンプレートを6言語
    （EN/DE/RU/ZH/JA/KO）で提供します。
  - KO: 문서, 스키마 설명, CLI 도움말/출력, 설정 템플릿을 6개 언어
    (EN/DE/RU/ZH/JA/KO)로 제공합니다.
- Master format and resolution guidance (`SPEC.md` §7.1): lossless 8-bit sRGB
  PNG / procedural script, crop-only rendering, and sizing rules for all
  eight aspect profiles (typically `7680x4320` for a 3840 px pack).
  - DE: Vorgaben zu Masterformat und -auflösung (`SPEC.md` §7.1): verlustfreies
    8-Bit-sRGB-PNG / Skript, reines Zuschneiden und Größenregeln für alle
    acht Seitenverhältnisse (üblicherweise `7680x4320` für 3840 px).
  - RU: Правила формата и размера мастера (`SPEC.md` §7.1): lossless 8-битный
    PNG в sRGB / скрипт, только кроп и правила размера для всех восьми
    профилей (обычно `7680x4320` для 3840 px).
  - ZH: 母版格式与分辨率指南（`SPEC.md` §7.1）：无损 8-bit sRGB PNG／程序化脚本、
    仅裁切渲染，以及全部八种配置的尺寸规则（3840 px 包通常为 `7680x4320`）。
  - JA: マスターの形式と解像度の指針（`SPEC.md` §7.1）：非圧縮 8bit sRGB PNG／
    スクリプト、切り抜きのみ、8つのアスペクトすべてのサイズ規則（3840 px なら
    通常 `7680x4320`）。
  - KO: 마스터 형식·해상도 지침(`SPEC.md` §7.1): 무손실 8비트 sRGB PNG／스크립트,
    크롭 전용 렌더링, 8개 프로필 모두의 크기 규칙(3840 px 팩은 보통 `7680x4320`).

### Explicitly out of scope

- Animated, video, WebGL, interactive and time/sun-based wallpapers.
- SVG/vector masters in v0.1 — rasterise them to PNG before packaging; the
  schema only accepts `source.kind: raster | procedural` and both `validate`
  and `render` reject SVG with an explicit message.
  - DE: SVG-/Vektor-Master in v0.1 — vor dem Packen zu PNG rastern; das Schema
    erlaubt nur `source.kind: raster | procedural`, und `validate` wie `render`
    lehnen SVG mit einer klaren Meldung ab.
  - RU: SVG/векторные мастера в v0.1 — растеризуйте в PNG перед упаковкой;
    схема допускает только `source.kind: raster | procedural`, а `validate` и
    `render` отклоняют SVG с явным сообщением.
  - ZH: v0.1 不支持 SVG／矢量母版——打包前请先栅格化为 PNG；schema 仅接受
    `source.kind: raster | procedural`，`validate` 与 `render` 都会给出明确错误。
  - JA: v0.1 は SVG／ベクターのマスター非対応——パッケージ化の前に PNG へ
    ラスタライズしてください。スキーマは `source.kind: raster | procedural` のみを
    受け付け、`validate` と `render` は明確なメッセージで SVG を拒否します。
  - KO: v0.1은 SVG／벡터 마스터를 지원하지 않습니다——패키징 전에 PNG로
    래스터화하세요. 스키마는 `source.kind: raster | procedural`만 허용하며
    `validate`와 `render` 모두 명확한 메시지로 SVG를 거부합니다.
- Multi-monitor span mode (per-monitor delivery only in v0.1).
- HDR and display-P3 output (sRGB baseline only).

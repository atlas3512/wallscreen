# Wallset Spec v0.1 — Draft

> Кратко (RU): один мастер-исходник (SVG/PNG или скрипт + seed) плюс один
> JSON-манифест описывают статические обои; набор JPG-файлов и конфиги под
> ОС порождаются автоматически. Dynamic/live-обои в v0.1 не поддерживаются.
>
> DE: Eine Master-Datei (SVG/PNG oder Skript + Seed) plus ein JSON-Manifest
> beschreiben statische Hintergründe; JPG-Dateien und Systemkonfigurationen
> werden automatisch erzeugt. Dynamische Hintergründe werden in v0.1 nicht unterstützt.
>
> ZH: 一个母版源文件（SVG/PNG 或脚本 + 种子）加一个 JSON 清单即可描述静态壁纸；
> JPG 文件和各系统配置会自动生成。v0.1 不支持动态壁纸。
>
> JA: 1つのマスター素材（SVG/PNG、またはスクリプトとシード）と JSON マニフェストで
> 静的壁紙を記述し、JPG ファイルと OS 固有の設定を自動生成します。v0.1 では動的
> 壁紙はサポートしません。
>
> KO: 마스터 파일(SVG/PNG 또는 스크립트와 시드)과 JSON 매니페스트 하나로 정적 배경화면을
> 설명하며, JPG 파일과 OS별 설정을 자동 생성합니다. v0.1에서는 동적 배경화면을 지원하지 않습니다.

**Status:** draft. No compatibility promise on `v0.x`; a breaking change means
a new schema file (`v0.2.json`, …).

## 1. Goals

- One human-readable manifest per wallpaper.
- One deterministic renderer: same master + same encoder = byte-identical JPGs.
- One naming convention shared by all operating systems.
- Adapters that *emit* native configuration instead of asking users to migrate.

## 2. Non-goals

- Video, WebGL, HTML, "live" or interactive wallpapers.
- Time/sun-based rotation, audio reactivity, widget layers.
- HDR, Display P3, ICC profiles other than sRGB.
- Automatic multi-monitor span mode (per-monitor output only).
- A central registry, telemetry, or a mandatory GUI app.

An implementation may add those as extensions prefixed with `x-`, but such
fields are outside this specification and MUST be ignored by conforming tools.

## 3. Terms

| Term | Meaning |
|---|---|
| **master** | Lossless source: SVG, PNG, or a procedural script plus seed. |
| **pack** | Directory containing a manifest, a master, licence and notes. |
| **safe area** | Normalised rectangle that must survive every crop. |
| **profile** | Aspect ratio plus the pixel widths to render. |
| **target** | `<os>[:<de>][@version]` identifier of a consuming system. |
| **adapter** | Component that places files and writes native configuration. |

## 4. Pack layout

```
packs/<theme>/<slug>/
├── wallpaper.pack.json     REQUIRED
├── source.png              REQUIRED for origin=own|ai; generated for procedural
├── source.svg              alternative lossless master
├── generate.py             REQUIRED for origin=procedural
├── LICENSE                 REQUIRED, SPDX: CC0-1.0
└── README.md               REQUIRED (origin, model/seed, crop notes)
```

Rendered JPGs are build artefacts. They MUST NOT be committed to the source
repository; publish them in Releases or a CDN and reference them by checksum.

## 5. Manifest

File name is fixed: `wallpaper.pack.json`. Schema: `schema/v0.1.json`.

| Field | Req. | Type | Description |
|---|---|---|---|
| `$schema` | no | string | URL of the schema this pack conforms to. |
| `spec` | yes | string | Spec version, currently `"0.1"`. |
| `type` | yes | enum | MUST be `"static"`. Reserved for future dynamic specs. |
| `id` | yes | string | `<theme>.<slug>`, lowercase ASCII, e.g. `aurora-night.aurora-01`. |
| `name` | yes | string | Human-readable name. |
| `version` | yes | string | SemVer of the pack. |
| `license` | yes | string | SPDX identifier of the image licence. |
| `author` | yes | string | Author or project name. |
| `theme.id` | yes | string | Palette/theme identifier, lowercase ASCII. |
| `theme.mode` | yes | enum | `dark`, `light`, or `auto`. |
| `theme.palette` | no | object | `base`, `surface`, `accent`, `text` as `#rrggbb`. |
| `source.file` | yes | string | Master file name, relative to the pack. |
| `source.kind` | yes | enum | `raster`, `vector`, `procedural`. |
| `source.width` | yes | integer | Master width in pixels, > 0. |
| `source.height` | yes | integer | Master height in pixels, > 0. |
| `source.origin` | yes | enum | `own`, `procedural`, `ai`, `mixed`. |
| `source.generator` | no | string | Model/tool name and version (recommended for `ai`). |
| `source.seed` | no | integer | Seed used by a procedural or AI generator. |
| `source.script` | cond. | string | Required when `kind` or `origin` is `procedural`. |
| `safe_area` | yes | object | `x`, `y`, `w`, `h`, each in `(0, 1]`; `x+w <= 1`, `y+h <= 1`. |
| `renditions` | yes | object | Map of profile name → rendition. At least one entry. |
| `renditions.<profile>.sizes` | yes | integer[] | Output widths in pixels, each > 0 and <= master width. |
| `renditions.<profile>.fit` | no | enum | `cover` (default) or `contain`. |
| `renditions.<profile>.safe_area` | no | object | Override for this aspect ratio. |
| `output.format` | yes | enum | MUST be `"jpeg"` in v0.1. |
| `output.quality` | yes | integer | 1–100; recommended 92. |
| `output.subsampling` | yes | enum | `4:4:4`, `4:2:2`, `4:2:0`; recommended `4:4:4`. |
| `output.progressive` | yes | boolean | Recommended `true`. |
| `output.color_space` | yes | enum | MUST be `"srgb"`. |
| `output.strip_metadata` | yes | boolean | MUST be `true`. |
| `output.encoder` | yes | string | Encoder name and pinned version, e.g. `Pillow@13.0`. |
| `targets` | yes | string[] | Target identifiers, at least one. |

Extension fields MUST be prefixed with `x-` and are ignored by validators.

## 6. Profiles and resolutions

| Profile | Aspect | Common widths (px) |
|---|---|---|
| `16:9` | 1.778 | 1920, 2560, 3840, 7680 |
| `16:10` | 1.600 | 1920, 2560 |
| `21:9` | 2.333 | 3440, 5120 |
| `32:9` | 3.556 | 3840, 5120 |
| `4:3` | 1.333 | 1600, 2048 |
| `5:4` | 1.250 | 1280, 2560 |
| `9:16` | 0.563 | 1080, 1440 |
| `1:1` | 1.000 | 512, 1080 |

A pack is free to use a subset. Widths are chosen by the author; height is
`round(width / aspect)`.

## 7. Rendition algorithm

For each profile and each requested width:

1. Let `a = w/h` be the profile aspect and `(W, H)` the master size.
2. Maximum centred crop:
   - if `W/H > a`: `cw = round(H*a)`, `ch = H`;
   - otherwise: `cw = W`, `ch = round(W/a)`.
3. Convert the effective safe area (profile override else global) to absolute
   coordinates: `sx0 = x*W`, `sy0 = y*H`, `sx1 = (x+w)*W`, `sy1 = (y+h)*H`.
4. Allowed crop origin is the intersection of `[0, W-cw]` and
   `[sx1-cw, sx0]`. Do the same for `y` with `ch`. If the intersection is
   empty, centre the crop on the safe area and emit a warning.
5. Crop, then resize to the target width with a Lanczos filter.
6. Save as progressive JPEG with the declared output profile and sRGB ICC.

The master MUST never be re-encoded before cropping.

## 8. JPEG output profile (normative)

- Encoder settings are declared in the manifest and pinned by a lockfile in the
  implementation repository.
- Recommended: `quality=92`, `subsampling=4:4:4`, `progressive=true`,
  `optimize=true`, sRGB ICC, no EXIF/XMP/comments.
- `4:4:4` is preferred over `4:2:0` because colour bleeding on thin lines and
  gradients is visible on large wallpapers.
- Every rendered file is accompanied by `checksums.sha256` in the form
  `<hex>  <relative path>`.

## 9. File naming

```
<theme.id>/<slug>/<theme.mode>/<profile>/<width>x<height>.jpg
```

Example: `aurora-night/aurora-01/dark/21:9/5120x2160.jpg`.
Only lowercase ASCII, digits and hyphens outside the separators. Colons in
profile names are part of the format and map to a directory on POSIX; on
Windows implementations MUST replace `:` with `-` in the *directory name*
while keeping the logical profile in `index.json`.

## 10. Provenance and licensing

- Code and this specification are MIT.
- Images are CC0-1.0 by default so consumers need no attribution. An author may
  choose another SPDX licence, but it MUST be declared and the licence file
  MUST be shipped.
- `source.origin` is mandatory: `own`, `procedural`, `ai` or `mixed`.
- AI output may not be copyrightable in some jurisdictions. The CC0 dedication
  covers all rights the author holds; no warranty is implied.
- Authors MUST verify that their generator's terms permit redistribution and
  MUST avoid trademarks, copyrighted characters and living-artist styles.
- Contributed packs containing scraped or third-party images without a clear
  licence MUST be rejected.

## 11. Targets and capabilities

Target grammar: `^[a-z][a-z0-9-]*(:[a-z][a-z0-9-]*)?(@[a-z0-9.]+)?$`

Examples: `linux:hyprland`, `linux:gnome`, `windows`, `macos@14`,
`freebsd:xfce`, `haiku`. `--target auto` is a CLI convenience, not a manifest
value.

Capabilities are data, not assumptions, and live in
`adapters/capabilities.json`:

| Target | JPG | Per-monitor | Theme sync | Notes |
|---|---|---|---|---|
| Linux (Hyprland/GNOME/XFCE) | yes | partial | partial | desktop-specific |
| Windows 10/11 | yes | yes | yes | `.theme` / COM API |
| macOS | yes | yes | yes | `NSWorkspace` |
| FreeBSD | yes | as chosen DE | as chosen DE | reuses Linux adapters, `/usr/local` paths |
| Haiku | yes | unknown | unknown | native adapter after review; fallback instructions in v0.1 |

An adapter MUST NOT write outside its output directory unless the user passes
an explicit apply flag. v0.1 implements no apply flag.

## 12. Validation rules

A conforming validator MUST reject a pack when:

- the manifest fails the JSON Schema;
- `id` prefix does not match `theme.id`;
- a procedural pack has no `script`, or the script is missing;
- a non-procedural pack's master file is missing;
- `LICENSE` or `README.md` is missing;
- `safe_area` exceeds the master bounds;
- any requested output width exceeds the master width;
- a target or profile is unknown.

## 13. Versioning

- `spec` in the manifest and the schema file name are the compatibility keys.
- New optional fields may be added in a `v0.x` schema without changing the
  major version.
- Removing or renaming a field requires a new schema file and a changelog entry.
- Packs declare their own SemVer in `version`; changing master, profile list or
  output profile is at least a minor bump.

## 14. Localisation of prose (normative)

### 14.1 EN

All comments and descriptions — documentation, schema descriptions, CLI help,
CLI output, config-template comments and code comments — MUST be provided in
six languages: English, German, Russian, Chinese, Japanese and Korean. English
is the canonical text; every translation MUST be updated in the same commit.
Code identifiers, file names and JSON keys remain English. Licence texts and
third-party legal code remain in their original language. Machine translation
is allowed as a draft but MUST be reviewed by a human.

### 14.2 DE

Alle Kommentare und Beschreibungen — Dokumentation, Schema-Beschreibungen,
CLI-Hilfe, CLI-Ausgaben, Kommentare in Konfigurationsvorlagen und Code-Kommentare
— MÜSSEN in sechs Sprachen vorliegen: Englisch, Deutsch, Russisch, Chinesisch,
Japanisch und Koreanisch. Englisch ist der verbindliche Text; jede Übersetzung
MUSS im selben Commit aktualisiert werden. Code-Bezeichner, Dateinamen und
JSON-Schlüssel bleiben englisch. Lizenztexte und juristische Texte Dritter
bleiben in ihrer Originalsprache. Maschinelle Übersetzung ist als Entwurf
erlaubt, MUSS aber von einem Menschen geprüft werden.

### 14.3 RU

Все комментарии и описания — документация, описания в схеме, справка CLI,
вывод CLI, комментарии в шаблонах конфигов и комментарии в коде — ДОЛЖНЫ быть
представлены на шести языках: английском, немецком, русском, китайском,
японском и корейском. Английский текст является каноническим; каждый перевод
ДОЛЖЕН обновляться в том же коммите. Идентификаторы кода, имена файлов и ключи
JSON остаются на английском. Тексты лицензий и сторонние юридические тексты
остаются на языке оригинала. Машинный перевод допустим как черновик, но ДОЛЖЕН
быть проверен человеком.

### 14.4 ZH

所有注释和说明——文档、JSON Schema 中的 description、CLI 帮助与输出、配置模板注释
以及代码注释——必须以六种语言提供：英语、德语、俄语、中文、日语和韩语。英文为权威原文，
每一份译文必须在同一提交中更新。代码标识符、文件名和 JSON 键保持英文。许可证文本
和第三方法律文本保持原文语言。机器翻译仅可作为草稿，且必须经过人工校对。

### 14.5 JA

すべてのコメントと説明（ドキュメント、スキーマの description、CLI のヘルプと出力、
設定テンプレートのコメント、コード内コメント）は、英語・ドイツ語・ロシア語・
中国語・日本語・韓国語の6言語で提供しなければなりません。英語を正規の原文とし、
すべての翻訳は同じコミットで更新する必要があります。コードの識別子、ファイル名、
JSON キーは英語のままとします。ライセンス本文および第三者が作成した法的文書は
原文の言語のままとします。機械翻訳は下書きとしてのみ許可され、人間の確認が必要です。

### 14.6 KO

모든 주석과 설명(문서, 스키마 description, CLI 도움말과 출력, 설정 템플릿 주석,
코드 주석)은 영어·독일어·러시아어·중국어·일본어·한국어 6개 언어로 제공해야 합니다.
영어를 정식 원문으로 하며, 모든 번역은 같은 커밋에서 업데이트해야 합니다. 코드 식별자,
파일 이름, JSON 키는 영어로 유지합니다. 라이선스 문구와 제3자의 법적 문서는 원래
언어로 유지합니다. 기계 번역은 초안으로만 허용되며 사람의 확인이 필요합니다.

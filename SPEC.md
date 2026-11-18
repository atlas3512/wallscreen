# Wallset Spec v0.1 — Draft

> Кратко (RU): один мастер-исходник (PNG или скрипт + seed) плюс один
> JSON-манифест описывают статические обои; набор JPG-файлов и конфиги под
> ОС порождаются автоматически. Dynamic/live-обои в v0.1 не поддерживаются.
>
> DE: Eine Master-Datei (PNG oder Skript + Seed) plus ein JSON-Manifest
> beschreiben statische Hintergründe; JPG-Dateien und Systemkonfigurationen
> werden automatisch erzeugt. Dynamische Hintergründe werden in v0.1 nicht unterstützt.
>
> ZH: 一个母版源文件（PNG 或脚本 + 种子）加一个 JSON 清单即可描述静态壁纸；
> JPG 文件和各系统配置会自动生成。v0.1 不支持动态壁纸。
>
> JA: 1つのマスター素材（PNG、またはスクリプトとシード）と JSON マニフェストで
> 静的壁紙を記述し、JPG ファイルと OS 固有の設定を自動生成します。v0.1 では動的
> 壁紙はサポートしません。
>
> KO: 마스터 파일(PNG 또는 스크립트와 시드)과 JSON 매니페스트 하나로 정적 배경화면을
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
- SVG/vector masters in v0.1 — rasterise them to PNG before packaging.
- Time/sun-based rotation, audio reactivity, widget layers.
- HDR, Display P3, ICC profiles other than sRGB.
- Automatic multi-monitor span mode (per-monitor output only).
- A central registry, telemetry, or a mandatory GUI app.

An implementation may add those as extensions prefixed with `x-`, but such
fields are outside this specification and MUST be ignored by conforming tools.

## 3. Terms

| Term | Meaning |
|---|---|
| **master** | Lossless source: PNG, or a procedural script plus seed. SVG is not supported in v0.1. |
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
| `source.kind` | yes | enum | `raster` or `procedural`. `vector`/SVG is NOT supported in v0.1. |
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

### 7.1 EN

A master MUST be lossless: 8-bit PNG in sRGB, or a procedural script with a
fixed seed. SVG/vector masters are NOT supported in v0.1; rasterise them to PNG
before packaging. JPEG MUST NOT be used as a master — its compression and 4:2:0 chroma subsampling would be
baked into every rendition. 16-bit PNG offers little benefit because the final
output is 8-bit JPEG.

The renderer crops; it never stretches. Size the master so that the crop for
each profile is at least as wide as the largest requested output width for that
profile, with a 1.5–2× downsampling margin for Lanczos.

For a 16:9 master with aspect `a = W/H = 1.778` and a profile aspect `r = w/h`:

- if `r >= a` (master narrower than the target, e.g. `21:9`, `32:9`), the crop
  width equals `W`, so `W >= W_out` is required;
- if `r < a` (master wider than the target, e.g. `4:3`, `9:16`), the crop width
  equals `H·r`, so `H >= W_out / r` is required.

For the widest profile `32:9` (`r = 3.556`) this means `W >= W_out`; for the
tallest `9:16` (`r = 0.563`) it means `H >= 1.778 · W_out`. The `9:16` profile
is therefore the height-limiting case.

Recommended masters for a 16:9 source:

- largest output 3840 px → `7680x4320` (2× headroom; the reference pack);
- largest output 5120 px at `21:9`/`32:9` → at least 10240 px wide, e.g.
  `10240x5760`;
- absolute minimum for the widths listed in section 6 → `5120x2880`.

A single global `safe_area` may not fit every aspect. Use per-profile
`renditions.<profile>.safe_area` overrides for ultrawide and portrait profiles,
as the reference pack does.

### 7.2 DE

Ein Master muss verlustfrei sein: 8-Bit-PNG in sRGB oder ein prozedurales
Skript mit festem Seed. SVG-/Vektor-Master werden in v0.1 NICHT unterstützt;
vor dem Packen zu PNG rastern. JPEG darf nicht als Master verwendet werden — seine Kompression
und 4:2:0-Chroma-Subsampling würden in jede Ausgabe übernommen. 16-Bit-PNG
bringt wenig, da das Endergebnis ein 8-Bit-JPEG ist.

Der Renderer schneidet zu, er streckt nicht. Dimensionieren Sie den Master so,
dass der Zuschnitt für jedes Profil mindestens so breit wie die größte
angeforderte Ausgabe-breite dieses Profils ist, mit 1,5–2× Reserve beim
Downsampling für Lanczos.

Für einen 16:9-Master mit `a = W/H = 1,778` und einem Profil mit `r = w/h`:

- wenn `r >= a` (Master schmaler als das Ziel, z. B. `21:9`, `32:9`), entspricht
  die Schnittbreite `W`, also ist `W >= W_out` erforderlich;
- wenn `r < a` (Master breiter als das Ziel, z. B. `4:3`, `9:16`), entspricht
  die Schnittbreite `H·r`, also ist `H >= W_out / r` erforderlich.

Für das breiteste Profil `32:9` (`r = 3,556`) bedeutet dies `W >= W_out`, für das
höchste `9:16` (`r = 0,563`) `H >= 1,778 · W_out`. `9:16` ist damit der
limitierende Fall für die Höhe.

Empfohlene Master für eine 16:9-Quelle:

- größte Ausgabe 3840 px → `7680x4320` (2× Reserve; Referenzpaket);
- größte Ausgabe 5120 px bei `21:9`/`32:9` → mindestens 10240 px breit, z. B.
  `10240x5760`;
- absolutes Minimum für die Breiten aus Abschnitt 6 → `5120x2880`.

Ein globales `safe_area` passt möglicherweise nicht zu jedem Seitenverhältnis.
Verwenden Sie für Ultrawide- und Portrait-Profile pro-Profil-Überschreibungen
`renditions.<profile>.safe_area`, wie im Referenzpaket.

### 7.3 RU

Мастер обязан быть lossless: 8-битный PNG в sRGB или процедурный скрипт с
фиксированным seed. SVG/векторные мастера в v0.1 НЕ поддерживаются; перед
упаковкой растеризуйте их в PNG. JPEG нельзя использовать как мастер — его компрессия и
4:2:0-субдискретизация хромы закрепятся в каждом рендере. 16-битный PNG даёт
мало выигрыша, ведь финал — 8-битный JPEG.

Рендерер вырезает область, но не растягивает. Подбирайте размер мастера так,
чтобы кроп для каждого профиля был не уже максимальной запрошенной ширины этого
профиля, с запасом 1,5–2× для Lanczos.

Для мастера 16:9 с `a = W/H = 1,778` и профиля с `r = w/h`:

- если `r >= a` (мастер уже цели, например `21:9`, `32:9`), ширина кропа равна
  `W`, значит требуется `W >= W_out`;
- если `r < a` (мастер шире цели, например `4:3`, `9:16`), ширина кропа равна
  `H·r`, значит требуется `H >= W_out / r`.

Для самого широкого профиля `32:9` (`r = 3,556`) это `W >= W_out`, для самого
высокого `9:16` (`r = 0,563`) — `H >= 1,778 · W_out`. Таким образом, `9:16`
ограничивает высоту.

Рекомендуемые мастера для источника 16:9:

- максимальная ширина 3840 px → `7680x4320` (запас 2×; референсный пак);
- максимальная ширина 5120 px у `21:9`/`32:9` → не менее 10240 px по ширине,
  например `10240x5760`;
- абсолютный минимум для ширин из раздела 6 → `5120x2880`.

Одно глобальное `safe_area` может не подойти каждому аспекту. Используйте
переопределения `renditions.<profile>.safe_area` для ультрашироких и
портретных профилей, как в референсном паке.

### 7.4 ZH

母版必须是无损的：sRGB 8-bit PNG，或带固定种子的程序化脚本。v0.1 不支持 SVG／矢量母版；
打包前请先栅格化为 PNG。不得用 JPEG 作母版——其压缩和 4:2:0 色度子采样会被固化进每个输出。16-bit PNG 收益很小，
因为最终是 8-bit JPEG。

渲染器只裁切，不拉伸。母版尺寸必须保证每个配置裁切后的宽度不小于该配置请求的最大输出
宽度，并为 Lanczos 留出 1.5–2× 余量。

对于 16:9 母版（`a = W/H = 1.778`）与配置比例 `r = w/h`：

- 若 `r >= a`（母版比目标窄，如 `21:9`、`32:9`），裁切宽度等于 `W`，故需 `W >= W_out`；
- 若 `r < a`（母版比目标宽，如 `4:3`、`9:16`），裁切宽度等于 `H·r`，故需 `H >= W_out / r`。

最宽的 `32:9`（`r = 3.556`）要求 `W >= W_out`，最高的 `9:16`（`r = 0.563`）要求
`H >= 1.778 · W_out`。因此 `9:16` 是高度的限制因素。

16:9 来源的推荐母版：

- 最大输出 3840 px → `7680x4320`（2× 余量；参考包）；
- `21:9`/`32:9` 最大输出 5120 px → 宽度至少 10240 px，如 `10240x5760`；
- 第 6 节所列宽度的绝对最低 → `5120x2880`。

一个全局 `safe_area` 未必适合所有比例。像参考包那样，为超宽和竖屏配置使用
`renditions.<profile>.safe_area` 覆盖。

### 7.5 JA

マスターは非圧縮である必要があります。sRGB の 8bit PNG、または固定シード付きの
手続き型スクリプトです。v0.1 は SVG／ベクターのマスターに対応していません。パッケージ化の
前に PNG へラスタライズしてください。JPEG をマスターにしてはいけません。
圧縮と 4:2:0 色差サブサンプリングがすべての出力に焼き付きます。最終出力が 8bit JPEG のため、
16bit PNG の恩恵はほとんどありません。

レンダラーは切り抜きを行うだけで、引き伸ばしは行いません。各プロファイルの切り抜き幅が
そのプロファイルの最大出力幅以上になるようにマスターをサイズ決めし、Lanczos 用に
1.5〜2× の余裕を持たせてください。

16:9 マスター（`a = W/H = 1.778`）とプロファイル比 `r = w/h` の場合：

- `r >= a`（マスターが目標より狭い、例：`21:9`、`32:9`）なら切り抜き幅は `W` となり、
  `W >= W_out` が必要；
- `r < a`（マスターが目標より広い、例：`4:3`、`9:16`）なら切り抜き幅は `H·r` となり、
  `H >= W_out / r` が必要。

最も広い `32:9`（`r = 3.556`）では `W >= W_out`、最も高い `9:16`（`r = 0.563`）では
`H >= 1.778 · W_out` となります。つまり `9:16` が高さの制約になります。

16:9 ソースの推奨マスター：

- 最大出力 3840 px → `7680x4320`（2× の余裕。リファレンスパック）；
- `21:9`/`32:9` で最大出力 5120 px → 幅 10240 px 以上、例：`10240x5760`；
- 第 6 節の幅に対する絶対最小 → `5120x2880`。

単一のグローバル `safe area` がすべてのアスペクトに合うとは限りません。リファレンスパックの
ように、超広角と縦長プロファイルには `renditions.<profile>.safe_area` の上書きを使用してください。

### 7.6 KO

마스터는 반드시 무손실이어야 합니다. sRGB 8비트 PNG 또는 고정 시드가 있는 절차적
스크립트를 사용합니다. v0.1은 SVG／벡터 마스터를 지원하지 않습니다. 패키징 전에
PNG로 래스터화하세요. JPEG는 마스터로 쓸 수 없습니다.
압축과 4:2:0 색도 서브샘플링이 모든 결과물에 그대로 남습니다. 최종 출력이 8비트 JPEG이므로
16비트 PNG의 이점은 거의 없습니다.

렌더러는 자를 뿐 늘리지 않습니다. 각 프로필의 크롭 폭이 해당 프로필의 최대 출력 폭 이상이
되도록 마스터 크기를 정하고, Lanczos용으로 1.5~2× 여유를 두세요.

16:9 마스터(`a = W/H = 1.778`)와 프로필 비율 `r = w/h`의 경우:

- `r >= a`(마스터가 목표보다 좁음, 예: `21:9`, `32:9`)면 크롭 폭은 `W`이므로
  `W >= W_out`이 필요합니다.
- `r < a`(마스터가 목표보다 넓음, 예: `4:3`, `9:16`)면 크롭 폭은 `H·r`이므로
  `H >= W_out / r`이 필요합니다.

가장 넓은 `32:9`(`r = 3.556`)는 `W >= W_out`, 가장 높은 `9:16`(`r = 0.563`)은
`H >= 1.778 · W_out`을 요구합니다. 따라서 `9:16`이 높이의 제약 조건입니다.

16:9 소스의 권장 마스터:

- 최대 출력 3840 px → `7680x4320`(2× 여유, 참조 팩);
- `21:9`/`32:9`에서 최대 출력 5120 px → 너비 10240 px 이상, 예: `10240x5760`;
- 6절에 나열된 폭의 절대 최소 → `5120x2880`.

단일 전역 `safe area`가 모든 비율에 맞지 않을 수 있습니다. 참조 팩처럼 울트라와이드 및
세로 프로필에는 `renditions.<profile>.safe_area` 재정의를 사용하세요.

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

# Contributing / Mitwirken / Участие / 贡献 / コントリビューション / 기여

## EN

1. Create `packs/<theme>/<slug>/` with `wallpaper.pack.json`, a lossless master, `LICENSE` (CC0-1.0) and `README.md`.
2. Own / AI packs commit the master; procedural packs commit `generate.py` + seed. Use a lossless 8-bit sRGB PNG master (or a procedural script; rasterise SVG to PNG first) sized so every profile crop is at least as wide as its largest output, with 1.5–2× headroom — typically `7680x4320` for a 3840 px pack. See `SPEC.md` §7.1.
3. Run `python tools/wps.py validate` and render every crop — especially 21:9 and 9:16.
4. Commit only sources; rendered JPGs go to Releases.
5. Only your own work. No scraped images, no trademarks, no copyrighted characters, no "in the style of a living artist".
6. Declare `source.origin` truthfully and record the model in `source.generator` for AI output.
7. All comments and descriptions must be supplied in EN/DE/RU/ZH/JA/KO in the same commit — see [`I18N.md`](I18N.md).

## DE

1. `packs/<theme>/<slug>/` mit `wallpaper.pack.json`, verlustfreiem Master, `LICENSE` (CC0-1.0) und `README.md` anlegen.
2. Pakete mit eigenen/AI-Bildern committen den Master; prozedurale Pakete committen `generate.py` + Seed. Verwenden Sie einen verlustfreien 8-Bit-sRGB-PNG-Master (oder ein Skript; SVG vorher zu PNG rastern), der so dimensioniert ist, dass jeder Profilzuschnitt mindestens so breit wie seine größte Ausgabe ist, mit 1,5–2× Reserve — üblicherweise `7680x4320` für ein 3840-px-Paket. Siehe `SPEC.md` §7.1.
3. `python tools/wps.py validate` ausführen und jeden Zuschnitt prüfen — besonders 21:9 und 9:16.
4. Nur Quelldateien committen; gerenderte JPGs gehören in Releases.
5. Nur eigene Arbeiten. Keine heruntergeladenen Bilder, keine Marken, keine urheberrechtlich geschützten Figuren, kein „im Stil eines lebenden Künstlers".
6. `source.origin` wahrheitsgemäß angeben und bei AI-Ausgaben das Modell in `source.generator` festhalten.
7. Alle Kommentare und Beschreibungen müssen im selben Commit in EN/DE/RU/ZH/JA/KO vorliegen — siehe [`I18N.md`](I18N.md).

## RU

1. Создайте `packs/<theme>/<slug>/` с `wallpaper.pack.json`, lossless-мастером, `LICENSE` (CC0-1.0) и `README.md`.
2. Для своих/AI-паков коммитьте мастер; для процедурных — `generate.py` + seed. Используйте lossless 8-битный PNG в sRGB (или скрипт; SVG сначала растеризуйте в PNG), размер которого обеспечивает кроп не уже максимальной выходной ширины с запасом 1,5–2× — обычно `7680x4320` для пакета 3840 px. См. `SPEC.md` §7.1.
3. Запустите `python tools/wps.py validate` и проверьте все кропы — особенно 21:9 и 9:16.
4. В коммит идут только исходники; JPG публикуются в Releases.
5. Только своя работа. Никаких скачанных картинок, торговых марок, защищённых персонажей и «в стиле живого художника».
6. Честно укажите `source.origin`; для AI-генераций запишите модель в `source.generator`.
7. Все комментарии и описания должны быть на EN/DE/RU/ZH/JA/KO в том же коммите — см. [`I18N.md`](I18N.md).

## ZH

1. 创建 `packs/<theme>/<slug>/`，包含 `wallpaper.pack.json`、无损母版、`LICENSE`（CC0-1.0）和 `README.md`。
2. 自有/AI 包提交母版；程序化包提交 `generate.py` + 种子。使用无损 8-bit sRGB PNG 母版（或程序化脚本；SVG 请先栅格化为 PNG），尺寸应保证每个配置的裁切宽度不小于其最大输出宽度，并留 1.5–2× 余量——3840 px 包通常为 `7680x4320`。见 `SPEC.md` §7.1。
3. 运行 `python tools/wps.py validate` 并检查所有裁切——尤其是 21:9 和 9:16。
4. 仅提交源文件；渲染出的 JPG 发布到 Releases。
5. 仅使用自己的作品。禁止抓取图片、商标、受版权保护的角色以及“模仿在世艺术家风格”。
6. 如实填写 `source.origin`；AI 生成内容需在 `source.generator` 中记录模型。
7. 所有注释和说明必须在同一提交中提供 EN/DE/RU/ZH/JA/KO 六种语言——见 [`I18N.md`](I18N.md)。

## JA

1. `packs/<theme>/<slug>/` に `wallpaper.pack.json`、非圧縮マスター、`LICENSE`（CC0-1.0）、`README.md` を作成してください。
2. 自作/AI パックはマスターをコミットします。手続き型パックは `generate.py` とシードをコミットします。マスターは非圧縮の 8bit sRGB PNG（またはスクリプト。SVG は先に PNG へラスタライズ）を使い、各プロファイルの切り抜きが最大出力幅以上になるよう 1.5〜2× の余裕を持たせてください（3840 px なら通常 `7680x4320`）。`SPEC.md` §7.1 を参照。
3. `python tools/wps.py validate` を実行し、すべての切り抜き（特に 21:9 と 9:16）を確認してください。
4. コミットするのはソースのみです。レンダリング済み JPG は Releases に置きます。
5. 自分の作品のみ使用してください。画像の無断取得、商標、著作権で保護されたキャラクター、「存命アーティストのスタイルで」は禁止です。
6. `source.origin` を正しく記述し、AI 生成物は `source.generator` にモデル名を記録してください。
7. すべてのコメントと説明は同じコミットで EN/DE/RU/ZH/JA/KO の6言語を用意してください——[`I18N.md`](I18N.md) を参照。

## KO

1. `packs/<theme>/<slug>/`에 `wallpaper.pack.json`, 비손실 마스터, `LICENSE`(CC0-1.0), `README.md`를 만드세요.
2. 자작/AI 팩은 마스터를 커밋하고, 절차적 팩은 `generate.py`와 시드를 커밋하세요. 마스터는 무손실 8비트 sRGB PNG(또는 스크립트; SVG는 먼저 PNG로 래스터화)를 사용하고, 각 프로필 크롭이 최대 출력 폭 이상이 되도록 1.5~2× 여유를 두세요(3840 px 팩은 보통 `7680x4320`). `SPEC.md` §7.1 참조.
3. `python tools/wps.py validate`를 실행하고 모든 크롭, 특히 21:9와 9:16을 확인하세요.
4. 소스만 커밋하세요. 렌더링된 JPG는 Releases에 올립니다.
5. 본인의 작품만 사용하세요. 이미지 무단 수집, 상표, 저작권이 있는 캐릭터, “살아 있는 아티스트 스타일로”는 금지입니다.
6. `source.origin`을 정확히 밝히고, AI 생성물은 `source.generator`에 모델명을 기록하세요.
7. 모든 주석과 설명은 같은 커밋에서 EN/DE/RU/ZH/JA/KO 6개 언어로 제공해야 합니다——[`I18N.md`](I18N.md) 참조.

## Spec changes / Änderungen der Spezifikation / Изменения спецификации / 规范变更 / 仕様変更 / 명세 변경

EN: `SPEC.md` and `schema/v0.1.json` must change together; breaking changes require a new schema file and a changelog entry.
DE: `SPEC.md` und `schema/v0.1.json` müssen gemeinsam geändert werden; Breaking Changes erfordern eine neue Schema-Datei und einen Changelog-Eintrag.
RU: `SPEC.md` и `schema/v0.1.json` меняются вместе; ломающие изменения требуют нового файла схемы и записи в changelog.
ZH: `SPEC.md` 与 `schema/v0.1.json` 必须同时修改；破坏性变更需要新的 schema 文件和变更日志条目。
JA: `SPEC.md` と `schema/v0.1.json` は同時に変更してください。破壊的変更には新しいスキーマファイルと変更履歴の追記が必要です。
KO: `SPEC.md`와 `schema/v0.1.json`은 함께 변경해야 합니다. 호환성이 깨지는 변경은 새 스키마 파일과 변경 로그 항목이 필요합니다.

# Contributing / Mitwirken / Участие / 贡献 / コントリビューション / 기여

## EN

1. Create `packs/<theme>/<slug>/` with `wallpaper.pack.json`, a lossless master, `LICENSE` (CC0-1.0) and `README.md`.
2. Own / AI packs commit the master; procedural packs commit `generate.py` + seed.
3. Run `python tools/wps.py validate` and render every crop — especially 21:9 and 9:16.
4. Commit only sources; rendered JPGs go to Releases.
5. Only your own work. No scraped images, no trademarks, no copyrighted characters, no "in the style of a living artist".
6. Declare `source.origin` truthfully and record the model in `source.generator` for AI output.
7. All comments and descriptions must be supplied in EN/DE/RU/ZH/JA/KO in the same commit — see [`I18N.md`](I18N.md).

## DE

1. `packs/<theme>/<slug>/` mit `wallpaper.pack.json`, verlustfreiem Master, `LICENSE` (CC0-1.0) und `README.md` anlegen.
2. Pakete mit eigenen/AI-Bildern committen den Master; prozedurale Pakete committen `generate.py` + Seed.
3. `python tools/wps.py validate` ausführen und jeden Zuschnitt prüfen — besonders 21:9 und 9:16.
4. Nur Quelldateien committen; gerenderte JPGs gehören in Releases.
5. Nur eigene Arbeiten. Keine heruntergeladenen Bilder, keine Marken, keine urheberrechtlich geschützten Figuren, kein „im Stil eines lebenden Künstlers".
6. `source.origin` wahrheitsgemäß angeben und bei AI-Ausgaben das Modell in `source.generator` festhalten.
7. Alle Kommentare und Beschreibungen müssen im selben Commit in EN/DE/RU/ZH/JA/KO vorliegen — siehe [`I18N.md`](I18N.md).

## RU

1. Создайте `packs/<theme>/<slug>/` с `wallpaper.pack.json`, lossless-мастером, `LICENSE` (CC0-1.0) и `README.md`.
2. Для своих/AI-паков коммитьте мастер; для процедурных — `generate.py` + seed.
3. Запустите `python tools/wps.py validate` и проверьте все кропы — особенно 21:9 и 9:16.
4. В коммит идут только исходники; JPG публикуются в Releases.
5. Только своя работа. Никаких скачанных картинок, торговых марок, защищённых персонажей и «в стиле живого художника».
6. Честно укажите `source.origin`; для AI-генераций запишите модель в `source.generator`.
7. Все комментарии и описания должны быть на EN/DE/RU/ZH/JA/KO в том же коммите — см. [`I18N.md`](I18N.md).

## ZH

1. 创建 `packs/<theme>/<slug>/`，包含 `wallpaper.pack.json`、无损母版、`LICENSE`（CC0-1.0）和 `README.md`。
2. 自有/AI 包提交母版；程序化包提交 `generate.py` + 种子。
3. 运行 `python tools/wps.py validate` 并检查所有裁切——尤其是 21:9 和 9:16。
4. 仅提交源文件；渲染出的 JPG 发布到 Releases。
5. 仅使用自己的作品。禁止抓取图片、商标、受版权保护的角色以及“模仿在世艺术家风格”。
6. 如实填写 `source.origin`；AI 生成内容需在 `source.generator` 中记录模型。
7. 所有注释和说明必须在同一提交中提供 EN/DE/RU/ZH/JA/KO 六种语言——见 [`I18N.md`](I18N.md)。

## JA

1. `packs/<theme>/<slug>/` に `wallpaper.pack.json`、非圧縮マスター、`LICENSE`（CC0-1.0）、`README.md` を作成してください。
2. 自作/AI パックはマスターをコミットします。手続き型パックは `generate.py` とシードをコミットします。
3. `python tools/wps.py validate` を実行し、すべての切り抜き（特に 21:9 と 9:16）を確認してください。
4. コミットするのはソースのみです。レンダリング済み JPG は Releases に置きます。
5. 自分の作品のみ使用してください。画像の無断取得、商標、著作権で保護されたキャラクター、「存命アーティストのスタイルで」は禁止です。
6. `source.origin` を正しく記述し、AI 生成物は `source.generator` にモデル名を記録してください。
7. すべてのコメントと説明は同じコミットで EN/DE/RU/ZH/JA/KO の6言語を用意してください——[`I18N.md`](I18N.md) を参照。

## KO

1. `packs/<theme>/<slug>/`에 `wallpaper.pack.json`, 비손실 마스터, `LICENSE`(CC0-1.0), `README.md`를 만드세요.
2. 자작/AI 팩은 마스터를 커밋하고, 절차적 팩은 `generate.py`와 시드를 커밋하세요.
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

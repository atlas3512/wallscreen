# Adapters / Adapter / Адаптеры / 适配器 / アダプター / 어댑터

## EN

An adapter answers one question: given rendered JPG paths, what does this system need? It never decides the crop or the palette — those come from the manifest. Input: manifest + `index.json`. Output: a directory with the chosen JPG and a native config file. No writes outside `--out`; `--apply` is reserved and not implemented in v0.1. Target grammar: `<os>[:<de>][@version]`, e.g. `linux:hyprland`, `windows`, `macos@14`, `freebsd:xfce`, `haiku`. Tier 1 = implemented and reviewed, tier 2 = reuse with path changes, tier 3 = unverified fallback. Capabilities live in [`capabilities.json`](capabilities.json).

## DE

Ein Adapter beantwortet eine Frage: Was braucht dieses System bei gegebenen JPG-Pfaden? Er bestimmt weder Zuschnitt noch Palette — diese kommen aus dem Manifest. Eingabe: Manifest + `index.json`. Ausgabe: ein Verzeichnis mit dem gewählten JPG und einer nativen Konfigurationsdatei. Keine Schreibzugriffe außerhalb von `--out`; `--apply` ist reserviert und in v0.1 nicht implementiert. Ziel-Syntax: `<os>[:<de>][@version]`, z. B. `linux:hyprland`, `windows`, `macos@14`, `freebsd:xfce`, `haiku`. Stufe 1 = implementiert und geprüft, Stufe 2 = Wiederverwendung mit Pfadänderungen, Stufe 3 = ungeprüfter Fallback. Fähigkeiten stehen in [`capabilities.json`](capabilities.json).

## RU

Адаптер отвечает на один вопрос: по путям к JPG — что нужно этой системе? Он не выбирает кроп и палитру — они из манифеста. Вход: манифест + `index.json`. Выход: папка с выбранным JPG и конфигом системы. Никаких записей вне `--out`; `--apply` зарезервирован и в v0.1 не реализован. Грамматика таргета: `<os>[:<de>][@version]`, например `linux:hyprland`, `windows`, `macos@14`, `freebsd:xfce`, `haiku`. Tier 1 — реализовано и проверено, tier 2 — переиспользование с изменением путей, tier 3 — непроверенный fallback. Возможности — в [`capabilities.json`](capabilities.json).

## ZH

适配器只回答一个问题：给定 JPG 路径后，该系统需要什么？它不决定裁切或配色——这些来自清单。输入：清单 + `index.json`。输出：包含所选 JPG 和原生配置文件的目录。不得写入 `--out` 之外；`--apply` 为预留参数，v0.1 未实现。目标语法：`<os>[:<de>][@version]`，例如 `linux:hyprland`、`windows`、`macos@14`、`freebsd:xfce`、`haiku`。Tier 1 = 已实现并审核，Tier 2 = 复用并修改路径，Tier 3 = 未验证的回退方案。能力声明见 [`capabilities.json`](capabilities.json)。

## JA

アダプターが答えるのは一つの質問だけです。JPG のパスが与えられたとき、この OS に何が必要か。切り抜きやパレットはマニフェストから来るため、アダプターは決定しません。入力：マニフェスト + `index.json`。出力：選択した JPG とネイティブ設定ファイルを含むディレクトリ。`--out` 以外への書き込みは禁止です。`--apply` は予約済みで v0.1 では未実装です。ターゲット構文：`<os>[:<de>][@version]`（例：`linux:hyprland`、`windows`、`macos@14`、`freebsd:xfce`、`haiku`）。Tier 1 = 実装・レビュー済み、Tier 2 = パス変更による再利用、Tier 3 = 未検証のフォールバック。能力定義は [`capabilities.json`](capabilities.json) にあります。

## KO

어댑터는 한 가지 질문에만 답합니다. 렌더링된 JPG 경로가 주어졌을 때 이 시스템에 무엇이 필요한가. 크롭과 팔레트는 매니페스트에서 오므로 어댑터가 결정하지 않습니다. 입력: 매니페스트 + `index.json`. 출력: 선택한 JPG와 네이티브 설정 파일이 있는 디렉터리. `--out` 밖에는 쓰지 않으며, `--apply`는 예약된 옵션으로 v0.1에서는 구현되지 않았습니다. 대상 구문: `<os>[:<de>][@version]` (예: `linux:hyprland`, `windows`, `macos@14`, `freebsd:xfce`, `haiku`). Tier 1 = 구현 및 검토 완료, Tier 2 = 경로 변경을 통한 재사용, Tier 3 = 검증되지 않은 폴백. 기능 정의는 [`capabilities.json`](capabilities.json)에 있습니다.

#!/usr/bin/env python3
"""wps — CLI for Wallset v0.1.

EN: Command line tool for Wallset v0.1.
DE: Kommandozeilenwerkzeug für Wallset v0.1.
RU: CLI-утилита для Wallset v0.1.
ZH: Wallset v0.1 的命令行工具。
JA: Wallset v0.1 のコマンドラインツール。
KO: Wallset v0.1용 명령줄 도구입니다.

Commands / Befehle / Команды / 命令 / コマンド / 명령:
validate, render, pack, install, capabilities
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "v0.1.json"
CAPS_PATH = ROOT / "adapters" / "capabilities.json"

ASPECTS: dict[str, tuple[int, int]] = {
    "16:9": (16, 9),
    "16:10": (16, 10),
    "21:9": (21, 9),
    "32:9": (32, 9),
    "4:3": (4, 3),
    "5:4": (5, 4),
    "9:16": (9, 16),
    "1:1": (1, 1),
}
SUBSAMPLING = {"4:4:4": 0, "4:2:2": 1, "4:2:0": 2}

LANG_TAGS = ("EN", "DE", "RU", "ZH", "JA", "KO")


def L(en: str, de: str, ru: str, zh: str, ja: str, ko: str) -> str:
    """EN: Build a six-language message.
    DE: Erzeugt eine Nachricht in sechs Sprachen.
    RU: Формирует сообщение на шести языках.
    ZH: 生成六语言消息。
    JA: 6言語のメッセージを生成します。
    KO: 6개 언어 메시지를 생성합니다.
    """
    return "\n".join(
        f"{tag}: {text}"
        for tag, text in zip(LANG_TAGS, (en, de, ru, zh, ja, ko))
    )


# ---------------------------------------------------------------------------
# EN: helpers / DE: Hilfsfunktionen / RU: вспомогательные функции
# ZH: 辅助函数 / JA: ヘルパー関数 / KO: 도우미 함수


def load_pack(argument: str) -> tuple[Path, dict[str, Any]]:
    path = Path(argument).resolve()
    if path.is_dir():
        path = path / "wallpaper.pack.json"
    if not path.is_file():
        raise SystemExit(L(
            f"pack manifest not found: {path}",
            f"Paket-Manifest nicht gefunden: {path}",
            f"манифест пакета не найден: {path}",
            f"找不到包清单：{path}",
            f"パックマニフェストが見つかりません: {path}",
            f"패키지 매니페스트를 찾을 수 없습니다: {path}",
        ))
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(L(
            f"invalid JSON in {path}: {exc}",
            f"Ungültiges JSON in {path}: {exc}",
            f"некорректный JSON в {path}: {exc}",
            f"{path} 中的 JSON 无效：{exc}",
            f"{path} の JSON が無効です: {exc}",
            f"{path}의 JSON이 올바르지 않습니다: {exc}",
        )) from exc
    return path.parent, data


def discover_packs() -> list[str]:
    return [str(p.parent) for p in sorted((ROOT / "packs").glob("*/*/wallpaper.pack.json"))]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_capabilities() -> dict[str, Any]:
    if not CAPS_PATH.is_file():
        return {}
    return json.loads(CAPS_PATH.read_text(encoding="utf-8")).get("targets", {})


def _check_area(area: dict[str, float], label: str, errors: list[str]) -> None:
    for key in ("x", "y", "w", "h"):
        value = area.get(key)
        if not isinstance(value, (int, float)) or not 0 < value <= 1:
            errors.append(f"{label}.{key} must be in (0, 1]")
    if isinstance(area.get("x"), (int, float)) and isinstance(area.get("w"), (int, float)):
        if area["x"] + area["w"] > 1 + 1e-9:
            errors.append(f"{label}: x + w exceeds 1")
    if isinstance(area.get("y"), (int, float)) and isinstance(area.get("h"), (int, float)):
        if area["y"] + area["h"] > 1 + 1e-9:
            errors.append(f"{label}: y + h exceeds 1")


def validate_pack(pack_dir: Path, data: dict[str, Any]) -> list[str]:
    """EN: Return validation errors; empty means valid.
    DE: Gibt Validierungsfehler zurück; leer bedeutet gültig.
    RU: Возвращает ошибки валидации; пустой список означает корректность.
    ZH: 返回校验错误；空列表表示有效。
    JA: 検証エラーを返します。空リストは有効を意味します。
    KO: 검증 오류를 반환합니다. 빈 목록은 유효함을 의미합니다.
    """
    errors: list[str] = []

    try:
        from jsonschema import Draft202012Validator  # type: ignore

        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        for error in validator.iter_errors(data):
            where = "/".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"schema {where}: {error.message}")
    except ImportError:
        required = (
            "spec", "type", "id", "name", "version", "license", "author",
            "theme", "source", "safe_area", "renditions", "output", "targets",
        )
        errors.extend(f"jsonschema missing; required field absent: {key}"
                      for key in required if key not in data)

    theme = data.get("theme", {})
    source = data.get("source", {})
    pack_id = str(data.get("id", ""))

    if source.get("kind") == "vector" or str(source.get("file", "")).lower().endswith(".svg"):
        errors.append("SVG/vector masters are not supported in v0.1; rasterise to PNG")

    if "." in pack_id and pack_id.split(".", 1)[0] != theme.get("id"):
        errors.append("id prefix does not match theme.id")

    _check_area(data.get("safe_area", {}), "safe_area", errors)
    for profile, config in (data.get("renditions") or {}).items():
        if profile not in ASPECTS:
            errors.append(f"unknown profile: {profile}")
        if "safe_area" in config:
            _check_area(config["safe_area"], f"renditions.{profile}.safe_area", errors)
        for width in config.get("sizes", []):
            if not isinstance(width, int) or width < 1:
                errors.append(f"{profile}: invalid width {width!r}")
            elif isinstance(source.get("width"), int) and width > source["width"]:
                errors.append(f"{profile}: width {width} exceeds master width")

    procedural = source.get("kind") == "procedural" or source.get("origin") == "procedural"
    if procedural:
        script = pack_dir / str(source.get("script", ""))
        if not source.get("script") or not script.is_file():
            errors.append("procedural pack requires an existing source.script")
    elif not (pack_dir / str(source.get("file", ""))).is_file():
        errors.append(f"master file missing: {source.get('file')}")

    for required_file in ("LICENSE", "README.md"):
        if not (pack_dir / required_file).is_file():
            errors.append(f"missing {required_file}")

    capabilities = load_capabilities()
    if capabilities:
        for target in data.get("targets", []):
            if target not in capabilities:
                errors.append(f"unknown target: {target}")

    return errors


def ensure_master(pack_dir: Path, data: dict[str, Any]) -> Path:
    from PIL import Image  # noqa: F401  (import also validates Pillow presence)

    source = data["source"]
    if source.get("kind") == "vector" or str(source.get("file", "")).lower().endswith(".svg"):
        raise SystemExit(L(
            "v0.1 does not support SVG/vector masters; rasterise to PNG",
            "v0.1 unterstützt keine SVG-/Vektor-Master; zu PNG rastern",
            "v0.1 не поддерживает SVG/векторные мастера; растеризуйте в PNG",
            "v0.1 不支持 SVG／矢量母版；请先栅格化为 PNG",
            "v0.1 は SVG／ベクターのマスターに対応していません。PNG にラスタライズしてください",
            "v0.1은 SVG／벡터 마스터를 지원하지 않습니다. PNG로 래스터화하세요",
        ))
    master = pack_dir / source["file"]
    if master.is_file():
        return master

    if source.get("script"):
        script = pack_dir / source["script"]
        if not script.is_file():
            raise SystemExit(L(
                f"generator script not found: {script}",
                f"Generator-Skript nicht gefunden: {script}",
                f"скрипт генератора не найден: {script}",
                f"找不到生成器脚本：{script}",
                f"ジェネレータースクリプトが見つかりません: {script}",
                f"제너레이터 스크립트를 찾을 수 없습니다: {script}",
            ))
        subprocess.run(
            [sys.executable, str(script), str(master), str(source.get("seed", 0))],
            check=True,
        )
        with Image.open(master) as image:
            actual = image.size
        expected = (source["width"], source["height"])
        if actual != expected:
            raise SystemExit(L(
                f"generator produced {actual}, expected {expected}",
                f"Generator erzeugte {actual}, erwartet {expected}",
                f"генератор выдал {actual}, ожидалось {expected}",
                f"生成器输出 {actual}，应为 {expected}",
                f"ジェネレーターの出力は {actual}、期待値は {expected}",
                f"제너레이터 출력: {actual}, 예상: {expected}",
            ))
        return master

    raise SystemExit(L(
        f"master not found and no generator defined: {master}",
        f"Master nicht gefunden und kein Generator definiert: {master}",
        f"мастер не найден и генератор не задан: {master}",
        f"未找到母版且未定义生成器：{master}",
        f"マスターがなく、ジェネレーターも定義されていません: {master}",
        f"마스터가 없고 제너레이터도 정의되지 않았습니다: {master}",
    ))


def crop_box(master_w: int, master_h: int, aspect: tuple[int, int],
             safe: dict[str, float]) -> tuple[int, int, int, int]:
    """EN: Largest crop of the requested aspect keeping the safe area visible.
    DE: Größter Zuschnitt mit dem gewünschten Seitenverhältnis, der die Safe Area erhält.
    RU: Максимальный кроп заданного aspect с сохранением safe_area.
    ZH: 保持 safe area 可见的指定宽高比最大裁切。
    JA: safe area を保持する指定アスペクトの最大切り抜き。
    KO: safe area를 유지하면서 요청한 비율의 최대 크롭 영역입니다.
    """
    aw, ah = aspect
    ratio = aw / ah
    if master_w / master_h > ratio:
        cw, ch = round(master_h * ratio), master_h
    else:
        cw, ch = master_w, round(master_w / ratio)

    sx0 = safe["x"] * master_w
    sy0 = safe["y"] * master_h
    sx1 = (safe["x"] + safe["w"]) * master_w
    sy1 = (safe["y"] + safe["h"]) * master_h

    def origin(lo: float, hi: float, crop: int, size: int, axis: str) -> int:
        lower = max(0.0, hi - crop)
        upper = min(float(lo), float(size - crop))
        if lower <= upper:
            return int(round((lower + upper) / 2))
        centre = (lo + hi) / 2 - crop / 2
        value = min(max(centre, 0.0), float(size - crop))
        print(L(
            f"warning: safe area cannot be fully kept on {axis}; centring on it",
            f"Warnung: Safe Area kann auf {axis} nicht vollständig erhalten bleiben; zentriert.",
            f"предупреждение: safe_area не полностью помещается по {axis}; центрируем",
            f"警告：safe area 无法在 {axis} 上完整保留；已居中处理",
            f"警告: safe area を {axis} 方向に完全に保持できません。中央に配置します",
            f"경고: {axis} 방향에서 safe area를 완전히 유지할 수 없습니다. 중앙에 배치합니다",
        ), file=sys.stderr)
        return int(round(value))

    x = origin(sx0, sx1, cw, master_w, "x")
    y = origin(sy0, sy1, ch, master_h, "y")
    return (x, y, min(master_w, x + cw), min(master_h, y + ch))


def srgb_icc() -> bytes | None:
    try:
        from PIL import ImageCms

        return ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    except Exception:  # pragma: no cover - depends on Pillow build
        return None


def fs_profile(profile: str) -> str:
    """EN: Colon is illegal in Windows directory names.
    DE: Doppelpunkte sind in Windows-Verzeichnisnamen unzulässig.
    RU: Двоеточие недопустимо в именах каталогов Windows.
    ZH: Windows 目录名中不允许使用冒号。
    JA: Windows のディレクトリ名にはコロンを使用できません。
    KO: Windows 디렉터리 이름에는 콜론을 사용할 수 없습니다.
    """
    return profile.replace(":", "-") if os.name == "nt" else profile


# ---------------------------------------------------------------------------
# EN: commands / DE: Befehle / RU: команды / ZH: 命令 / JA: コマンド / KO: 명령


def render_pack(pack_dir: Path, out: Path, only: list[str] | None = None) -> list[dict[str, Any]]:
    from PIL import Image

    _, data = load_pack(str(pack_dir / "wallpaper.pack.json"))
    master = ensure_master(pack_dir, data)
    out_root = out.resolve()

    theme = data["theme"]["id"]
    slug = data["id"].split(".", 1)[-1]
    mode = data["theme"]["mode"]
    output = data["output"]
    if output["format"] != "jpeg":
        raise SystemExit(L(
            "v0.1 supports only output.format=jpeg",
            "v0.1 unterstützt nur output.format=jpeg",
            "v0.1 поддерживает только output.format=jpeg",
            "v0.1 仅支持 output.format=jpeg",
            "v0.1 では output.format=jpeg のみ対応します",
            "v0.1은 output.format=jpeg만 지원합니다",
        ))

    records: list[dict[str, Any]] = []
    with Image.open(master) as source_image:
        base = source_image.convert("RGB")

        for profile, config in data["renditions"].items():
            if only and profile not in only:
                continue
            aw, ah = ASPECTS[profile]
            safe = config.get("safe_area", data["safe_area"])
            box = crop_box(base.width, base.height, (aw, ah), safe)
            crop = base.crop(box)

            for width in config["sizes"]:
                height = round(width * ah / aw)
                tile = crop.resize((width, height), Image.Resampling.LANCZOS)

                directory = out_root / theme / slug / mode / fs_profile(profile)
                directory.mkdir(parents=True, exist_ok=True)
                destination = directory / f"{width}x{height}.jpg"

                save_kwargs: dict[str, Any] = {
                    "format": "JPEG",
                    "quality": output["quality"],
                    "subsampling": SUBSAMPLING[output["subsampling"]],
                    "progressive": output["progressive"],
                    "optimize": True,
                }
                icc = srgb_icc() if output["color_space"] == "srgb" else None
                if icc:
                    save_kwargs["icc_profile"] = icc
                tile.save(destination, **save_kwargs)

                relative = destination.relative_to(out_root).as_posix()
                records.append({
                    "profile": profile,
                    "width": width,
                    "height": height,
                    "path": relative,
                    "sha256": sha256_file(destination),
                    "bytes": destination.stat().st_size,
                    "crop": list(box),
                })
                print(L(
                    f"rendered {relative}",
                    f"gerendert {relative}",
                    f"отрендерено {relative}",
                    f"已渲染 {relative}",
                    f"レンダー完了: {relative}",
                    f"렌더링 완료: {relative}",
                ))

    write_index(out_root, data, records)
    write_checksums(out_root)
    return records


def write_index(out_root: Path, data: dict[str, Any], records: list[dict[str, Any]]) -> Path:
    path = out_root / "index.json"
    index: dict[str, Any] = {"spec": "0.1", "generated_by": "wps 0.1.0", "packs": {}}
    if path.is_file():
        try:
            index = json.loads(path.read_text(encoding="utf-8"))
            index.setdefault("packs", {})
        except json.JSONDecodeError:
            pass

    index["packs"][data["id"]] = {
        "name": data["name"],
        "version": data["version"],
        "theme": data["theme"],
        "license": data["license"],
        "author": data["author"],
        "origin": data["source"]["origin"],
        "files": records,
    }
    path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def write_checksums(out_root: Path) -> Path:
    path = out_root / "checksums.sha256"
    lines = []
    for image in sorted(out_root.rglob("*.jpg")):
        lines.append(f"{sha256_file(image)}  {image.relative_to(out_root).as_posix()}")
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return path


def pick_file(records: list[dict[str, Any]], profile: str = "16:9") -> dict[str, Any]:
    candidates = [r for r in records if r["profile"] == profile]
    if not candidates:
        candidates = records
    if not candidates:
        raise SystemExit(L(
            "nothing rendered; run render first",
            "nichts gerendert; zuerst render ausführen",
            "нет отрендеренных файлов; сначала выполните render",
            "尚未渲染；请先运行 render",
            "レンダー結果がありません。先に render を実行してください",
            "렌더링된 파일이 없습니다. 먼저 render를 실행하세요",
        ))
    return max(candidates, key=lambda r: r["width"])


def adapter_config(target: str, chosen: dict[str, Any], data: dict[str, Any]) -> tuple[str, str]:
    path = chosen["path"]
    name = data["name"]
    if target.startswith("linux:hyprland"):
        return ("hyprpaper.conf", (
            "# EN: Generated by wps 0.1 — replace eDP-1 with your monitor name.\n"
            "# DE: Erzeugt von wps 0.1 — eDP-1 durch den eigenen Monitornamen ersetzen.\n"
            "# RU: Сгенерировано wps 0.1 — замените eDP-1 на имя своего монитора.\n"
            "# ZH: 由 wps 0.1 生成——请将 eDP-1 替换为您的显示器名称。\n"
            "# JA: wps 0.1 が生成しました — eDP-1 を実際のモニター名に置き換えてください。\n"
            "# KO: wps 0.1에서 생성했습니다 — eDP-1을 모니터 이름으로 바꾸세요.\n"
            f"preload = {path}\n"
            f"wallpaper = eDP-1,{path}\n"
        ))
    if target.startswith("linux:gnome"):
        return ("gnome-background.xml", (
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
            "<!-- EN: Generated by wps 0.1. -->\n"
            "<!-- DE: Erzeugt von wps 0.1. -->\n"
            "<!-- RU: Сгенерировано wps 0.1. -->\n"
            "<!-- ZH: 由 wps 0.1 生成。 -->\n"
            "<!-- JA: wps 0.1 が生成しました。 -->\n"
            "<!-- KO: wps 0.1에서 생성했습니다. -->\n"
            "<wallpapers>\n"
            "  <wallpaper deleted=\"false\">\n"
            f"    <name>{name} (WPS)</name>\n"
            "    <static>\n"
            f"      <file>{path}</file>\n"
            "    </static>\n"
            "  </wallpaper>\n"
            "</wallpapers>\n"
        ))
    if target == "windows":
        return ("wallpaper.theme", (
            "; EN: Generated by wps 0.1 — template, review before importing.\n"
            "; DE: Erzeugt von wps 0.1 — Vorlage, vor dem Import prüfen.\n"
            "; RU: Сгенерировано wps 0.1 — шаблон, проверьте перед импортом.\n"
            "; ZH: 由 wps 0.1 生成——导入前请检查模板。\n"
            "; JA: wps 0.1 が生成しました — インポート前に内容を確認してください。\n"
            "; KO: wps 0.1에서 생성했습니다 — 가져오기 전에 검토하세요.\n"
            "[Theme]\n"
            f"DisplayName={name} (WPS)\n"
            "[Control Panel\\Desktop]\n"
            f"Wallpaper={path}\n"
            "TileWallpaper=0\n"
            "WallpaperStyle=10\n"
        ))
    if target == "macos":
        return ("set-wallpaper.command", (
            "#!/bin/sh\n"
            "# EN: Generated by wps 0.1 — runs per display/space.\n"
            "# DE: Erzeugt von wps 0.1 — läuft pro Display/Space.\n"
            "# RU: Сгенерировано wps 0.1 — выполняется для каждого дисплея/пространства.\n"
            "# ZH: 由 wps 0.1 生成——按显示器/桌面空间运行。\n"
            "# JA: wps 0.1 が生成しました — ディスプレイ／スペースごとに実行されます。\n"
            "# KO: wps 0.1에서 생성했습니다 — 디스플레이/스페이스별로 실행됩니다.\n"
            f"WALLPAPER=\"{path}\"\n"
            "osascript -e 'tell application \"System Events\" to tell every desktop'\n"
            "  -e \"set picture to (POSIX file \\\"$WALLPAPER\\\") as alias\" \\\n"
            "  -e 'end tell'\n"
        ))
    if target.startswith("freebsd:"):
        return ("set-wallpaper.sh", (
            "#!/bin/sh\n"
            "# EN: Generated by wps 0.1 — FreeBSD uses /usr/local paths.\n"
            "# DE: Erzeugt von wps 0.1 — FreeBSD verwendet /usr/local-Pfade.\n"
            "# RU: Сгенерировано wps 0.1 — FreeBSD использует пути /usr/local.\n"
            "# ZH: 由 wps 0.1 生成——FreeBSD 使用 /usr/local 路径。\n"
            "# JA: wps 0.1 が生成しました — FreeBSD では /usr/local パスを使用します。\n"
            "# KO: wps 0.1에서 생성했습니다 — FreeBSD는 /usr/local 경로를 사용합니다.\n"
            f"WALLPAPER=\"{path}\"\n"
            "xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path -s \"$WALLPAPER\"\n"
        ))
    if target.startswith("haiku"):
        return ("README.txt", (
            "Haiku fallback (v0.1)\n"
            "=====================\n"
            "EN: No native adapter has been verified yet. Open the generated JPG\n"
            f"    ({path}) in Tracker and use Desktop preferences to set it as background.\n"
            "DE: Noch kein nativer Adapter geprüft. Öffnen Sie das erzeugte JPG\n"
            f"    ({path}) in Tracker und setzen Sie es über die Desktop-Einstellungen als Hintergrund.\n"
            "RU: Нативный адаптер ещё не проверен. Откройте сгенерированный JPG\n"
            f"    ({path}) в Tracker и задайте его через настройки рабочего стола.\n"
            "ZH: 尚未验证原生适配器。请在 Tracker 中打开生成的 JPG\n"
            f"    （{path}），然后在桌面设置中将其设为背景。\n"
            "JA: ネイティブアダプターはまだ検証されていません。生成された JPG\n"
            f"    ({path}) を Tracker で開き、デスクトップ設定で背景に設定してください。\n"
            "KO: 네이티브 어댑터가 아직 검증되지 않았습니다. 생성된 JPG\n"
            f"    ({path})를 Tracker에서 열고 데스크톱 설정에서 배경으로 지정하세요.\n"
            "EN/DE/RU/ZH/JA/KO: Report your Haiku version / Melden Sie Ihre Haiku-Version /\n"
            "Сообщите версию Haiku / 请反馈您的 Haiku 版本 / Haiku のバージョンを報告してください /\n"
            "Haiku 버전을 알려주세요.\n"
        ))
    return ("README.txt", L(
        f"Generated by wps 0.1. Set {path} as wallpaper.",
        f"Erzeugt von wps 0.1. Setzen Sie {path} als Hintergrund.",
        f"Сгенерировано wps 0.1. Установите {path} как обои.",
        f"由 wps 0.1 生成。请将 {path} 设为壁纸。",
        f"wps 0.1 が生成しました。{path} を壁紙に設定してください。",
        f"wps 0.1에서 생성했습니다. {path}를 배경화면으로 설정하세요.",
    ) + "\n")


def cmd_validate(args: argparse.Namespace) -> int:
    targets = args.pack or discover_packs()
    if not targets:
        print(L(
            "no packs found",
            "keine Pakete gefunden",
            "паки не найдены",
            "未找到任何包",
            "パックが見つかりません",
            "팩을 찾을 수 없습니다",
        ), file=sys.stderr)
        return 1
    failed = 0
    for target in targets:
        pack_dir, data = load_pack(target)
        errors = validate_pack(pack_dir, data)
        if errors:
            failed += 1
            print(f"FAIL {data.get('id', target)}")
            print(L(
                "details below are canonical English (schema/validator messages)",
                "die Details unten sind verbindliches Englisch (Schema-/Validator-Meldungen)",
                "детали ниже на каноническом английском (сообщения схемы/валидатора)",
                "以下详情为权威英文（schema/校验器消息）",
                "以下の詳細は正規英語です（スキーマ／バリデーターのメッセージ）",
                "아래 내용은 표준 영문입니다(schema/validator 메시지)",
            ))
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK   {data['id']}")
    return 1 if failed else 0


def cmd_render(args: argparse.Namespace) -> int:
    pack_dir, _ = load_pack(args.pack)
    errors = validate_pack(pack_dir, json.loads((pack_dir / "wallpaper.pack.json").read_text()))
    if errors:
        print(L(
            "pack is invalid:",
            "Paket ist ungültig:",
            "пак некорректен:",
            "包无效：",
            "パックが無効です：",
            "팩이 유효하지 않습니다:",
        ), file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    render_pack(pack_dir, Path(args.out), args.profile)
    return 0


def cmd_pack(args: argparse.Namespace) -> int:
    pack_dir, data = load_pack(args.pack)
    out_root = Path(args.out).resolve()
    records = render_pack(pack_dir, out_root)
    slug = data["id"].replace(".", "-")
    archive = out_root / f"{slug}-{data['version']}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        bundle.write(pack_dir / "wallpaper.pack.json", "wallpaper.pack.json")
        for extra in ("LICENSE", "README.md"):
            candidate = pack_dir / extra
            if candidate.is_file():
                bundle.write(candidate, extra)
        for record in records:
            bundle.write(out_root / record["path"], record["path"])
        bundle.write(out_root / "index.json", "index.json")
        bundle.write(out_root / "checksums.sha256", "checksums.sha256")
    print(L(
        f"archive {archive}",
        f"Archiv {archive}",
        f"архив {archive}",
        f"归档 {archive}",
        f"アーカイブ {archive}",
        f"아카이브 {archive}",
    ))
    return 0


def cmd_install(args: argparse.Namespace) -> int:
    pack_dir, data = load_pack(args.pack)
    out_root = Path(args.out).resolve()
    records = render_pack(pack_dir, out_root)
    target = args.target
    if target not in load_capabilities():
        print(L(
            f"warning: unknown target {target}",
            f"Warnung: unbekanntes Ziel {target}",
            f"предупреждение: неизвестный таргет {target}",
            f"警告：未知目标 {target}",
            f"警告: 不明なターゲット {target}",
            f"경고: 알 수 없는 대상 {target}",
        ), file=sys.stderr)
    filename, text = adapter_config(target, pick_file(records), data)
    destination = out_root / "install" / target.replace(":", "-")
    destination.mkdir(parents=True, exist_ok=True)
    (destination / filename).write_text(text, encoding="utf-8")
    print(L(
        f"config {destination / filename}",
        f"Konfiguration {destination / filename}",
        f"конфиг {destination / filename}",
        f"配置文件 {destination / filename}",
        f"設定ファイル {destination / filename}",
        f"설정 파일 {destination / filename}",
    ))
    print(L(
        "No system files were modified. Use --apply in a future version to install.",
        "Es wurden keine Systemdateien geändert. --apply ist für eine spätere Version vorgesehen.",
        "Системные файлы не изменены. --apply появится в одной из следующих версий.",
        "未修改任何系统文件。未来版本将提供 --apply 参数。",
        "システムファイルは変更されていません。--apply は将来のバージョンで使用可能になります。",
        "시스템 파일은 변경되지 않았습니다. 향후 버전에서 --apply를 사용할 수 있습니다.",
    ))
    return 0


def cmd_capabilities(_: argparse.Namespace) -> int:
    targets = load_capabilities()
    print(L(
        "Legend: target | tier | jpeg | per-monitor | theme-sync | notes",
        "Legende: target | tier | jpeg | per-monitor | theme-sync | notes",
        "Обозначения: target | tier | jpeg | per-monitor | theme-sync | notes",
        "图例：target | tier | jpeg | per-monitor | theme-sync | notes",
        "凡例: target | tier | jpeg | per-monitor | theme-sync | notes",
        "범례: target | tier | jpeg | per-monitor | theme-sync | notes",
    ))
    print(f"{'target':<20} {'tier':<5} {'jpeg':<5} {'per-monitor':<12} {'theme-sync':<11} notes")
    for name, info in targets.items():
        print(
            f"{name:<20} {str(info.get('tier', '?')):<5} "
            f"{str('yes' if 'jpeg' in info.get('formats', []) else 'no'):<5} "
            f"{str(info.get('per_monitor', '?')):<12} "
            f"{str(info.get('theme_sync', '?')):<11} "
            f"{info.get('notes', '')}"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wps",
        description=L(
            "Wallset CLI v0.1 — six-language help (EN/DE/RU/ZH/JA/KO)",
            "Wallset CLI v0.1 — Hilfe in sechs Sprachen (EN/DE/RU/ZH/JA/KO)",
            "Wallset CLI v0.1 — справка на шести языках (EN/DE/RU/ZH/JA/KO)",
            "Wallset CLI v0.1 — 六语言帮助（EN/DE/RU/ZH/JA/KO）",
            "Wallset CLI v0.1 — 6言語ヘルプ（EN/DE/RU/ZH/JA/KO）",
            "Wallset CLI v0.1 — 6개 언어 도움말 (EN/DE/RU/ZH/JA/KO)",
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help=L(
        "validate pack manifests", "Paketmanifeste validieren",
        "проверить манифесты паков", "校验包清单", "パックマニフェストを検証",
        "팩 매니페스트 검증",
    ))
    validate.add_argument("pack", nargs="*", help=L(
        "pack directory (default: all packs)", "Paketverzeichnis (Standard: alle Pakete)",
        "каталог пака (по умолчанию: все паки)", "包目录（默认：全部包）",
        "パックのディレクトリ（既定：すべてのパック）", "팩 디렉터리 (기본값: 모든 팩)",
    ))
    validate.set_defaults(func=cmd_validate)

    render = sub.add_parser("render", help=L(
        "render JPEG renditions", "JPEG-Ausgaben rendern",
        "отрендерить JPEG-файлы", "渲染 JPEG 输出", "JPEG をレンダリング",
        "JPEG 결과물 렌더링",
    ))
    render.add_argument("pack")
    render.add_argument("--out", default="dist")
    render.add_argument("--profile", action="append", dest="profile", help=L(
        "limit to a profile (repeatable)", "auf ein Profil begrenzen (wiederholbar)",
        "ограничить профилем (повторяемо)", "限定为某个配置（可重复）",
        "プロファイルを指定（繰り返し可能）", "프로필로 제한 (반복 가능)",
    ))
    render.set_defaults(func=cmd_render)

    bundle = sub.add_parser("pack", help=L(
        "render and build a zip archive", "rendern und ZIP-Archiv erstellen",
        "отрендерить и собрать zip-архив", "渲染并生成 zip 归档",
        "レンダーして zip アーカイブを作成", "렌더링 후 zip 아카이브 생성",
    ))
    bundle.add_argument("pack")
    bundle.add_argument("--out", default="dist")
    bundle.set_defaults(func=cmd_pack)

    install = sub.add_parser("install", help=L(
        "emit native configuration (no system writes)",
        "native Konfiguration erzeugen (keine Systemänderungen)",
        "создать конфиг системы (без записи в систему)",
        "生成原生配置（不写入系统）",
        "ネイティブ設定を生成（システムには書き込みません）",
        "네이티브 설정 생성 (시스템에 쓰지 않음)",
    ))
    install.add_argument("pack")
    install.add_argument("--target", required=True)
    install.add_argument("--out", default="dist")
    install.set_defaults(func=cmd_install)

    caps = sub.add_parser("capabilities", help=L(
        "print target capability matrix", "Ziel-Fähigkeitsmatrix ausgeben",
        "вывести матрицу возможностей таргетов", "打印目标能力矩阵",
        "ターゲット能力一覧を表示", "대상 기능 매트릭스 출력",
    ))
    caps.set_defaults(func=cmd_capabilities)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Master procedurale / Deterministic procedural master / Процедурный мастер / 程序化母版 / 手続き型マスター / 절차적 마스터.

EN: Deterministic procedural master for aurora-night/aurora-01. Same seed + same Pillow version = same bytes.
DE: Deterministischer prozeduraler Master für aurora-night/aurora-01. Gleicher Seed + gleiche Pillow-Version = gleiche Bytes.
RU: Детерминированный процедурный мастер для aurora-night/aurora-01. Тот же seed + та же версия Pillow = те же байты.
ZH: aurora-night/aurora-01 的确定性程序化母版。相同种子 + 相同 Pillow 版本 = 相同字节。
JA: aurora-night/aurora-01 の決定的な手続き型マスター。同じシードと Pillow バージョンで同じバイト列になります。
KO: aurora-night/aurora-01의 결정적 절차적 마스터입니다. 같은 시드와 Pillow 버전이면 같은 바이트가 됩니다.

Usage / Nutzung / Использование / 用法 / 使い方 / 사용법:
    python generate.py [output.png] [seed]
"""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

W, H = 7680, 4320
SW, SH = 192, 108


def _clamp(value: float) -> int:
    return max(0, min(255, int(value)))


def build(seed: int) -> Image.Image:
    rng = random.Random(seed)

    # EN: Small gradient, upscaled: cheap and smooth for a large sky.
    # DE: Kleiner Gradient, hochskaliert: günstig und glatt für einen großen Himmel.
    # RU: Маленький градиент с апскейлом: дёшево и гладко для большого неба.
    # ZH: 小尺寸渐变再放大：大尺寸天空成本低且平滑。
    # JA: 小さなグラデーションを拡大：大きな空を低コストで滑らかに描けます。
    # KO: 작은 그라디언트를 확대합니다. 큰 하늘을 저비용으로 부드럽게 그릴 수 있습니다.
    sky = Image.new("RGB", (SW, SH))
    pixels = sky.load()
    for y in range(SH):
        v = y / (SH - 1)
        for x in range(SW):
            u = x / (SW - 1)
            wave = 0.5 + 0.5 * math.sin(u * math.tau * 1.15 + v * 3.2)
            glow = max(0.0, (wave ** 2) * (1 - abs(v - 0.38) / 0.62))
            pixels[x, y] = (
                _clamp(6 + 12 * v + 46 * glow),
                _clamp(14 + 34 * v + 150 * glow),
                _clamp(36 + 70 * (1 - v) + 90 * glow),
            )
    image = sky.resize((W, H), Image.Resampling.BICUBIC)

    # EN: Aurora ribbons on a quarter-resolution overlay.
    # DE: Aurora-Bänder auf einer Overlay-Ebene mit Viertelauflösung.
    # RU: Ленты авроры на оверлее в четверть разрешения.
    # ZH: 在四分之一分辨率叠加层上绘制极光带。
    # JA: 4分の1解像度のオーバーレイにオーロラの帯を描きます。
    # KO: 4분의 1 해상도 오버레이에 오로라 띠를 그립니다.
    ow, oh = W // 4, H // 4
    ribbons = Image.new("RGBA", (ow, oh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(ribbons, "RGBA")
    phase = rng.uniform(0, math.tau)
    for k in range(5):
        points = []
        for i in range(41):
            u = i / 40
            y = (
                oh * (0.18 + 0.09 * k)
                + math.sin(u * 5.5 + phase + k * 0.7) * oh * 0.07
                + math.sin(u * 11 + phase) * oh * 0.02
            )
            points.append((u * ow, y))
        draw.line(points, fill=(80, 240, 200, 46), width=44 + k * 8, joint="curve")
    ribbons = ribbons.filter(ImageFilter.GaussianBlur(26)).resize(
        (W, H), Image.Resampling.BICUBIC
    )
    image = Image.alpha_composite(image.convert("RGBA"), ribbons).convert("RGB")

    # EN: Stars. / DE: Sterne. / RU: Звёзды. / ZH: 星。 / JA: 星。 / KO: 별.
    stars = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    star_draw = ImageDraw.Draw(stars, "RGBA")
    for _ in range(420):
        x = rng.randrange(W)
        y = rng.randrange(int(H * 0.72))
        r = rng.choice((2, 2, 3, 4))
        alpha = rng.randint(70, 190)
        star_draw.ellipse((x - r, y - r, x + r, y + r), fill=(230, 240, 255, alpha))
    image = Image.alpha_composite(image.convert("RGBA"), stars).convert("RGB")

    # EN: Ground ridge — also gives the safe area a visible bottom anchor.
    # DE: Bodenkante — dient auch als sichtbarer unterer Anker für die Safe Area.
    # RU: Линия горизонта — также служит видимой нижней границей safe_area.
    # ZH: 地面山脊——同时为 safe area 提供可见的底部锚点。
    # JA: 地面の稜線——safe area の下側の目印にもなります。
    # KO: 지평선 능선은 safe area의 아래쪽 기준점이기도 합니다.
    ridge = [(0, H)]
    for i in range(13):
        x = int(W * i / 12)
        y = int(H * (0.80 + 0.10 * math.sin(i * 1.7 + phase) + 0.04 * rng.random()))
        ridge.append((x, y))
    ridge.append((W, H))
    ImageDraw.Draw(image).polygon(ridge, fill=(5, 9, 18))

    return image


def main() -> None:
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("source.png")
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 421337
    image = build(seed)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, "PNG", optimize=True)
    for tag, text in (
        ("EN", f"wrote {output} ({image.width}x{image.height}, seed={seed})"),
        ("DE", f"geschrieben: {output} ({image.width}x{image.height}, Seed={seed})"),
        ("RU", f"записано {output} ({image.width}x{image.height}, seed={seed})"),
        ("ZH", f"已写入 {output}（{image.width}x{image.height}，种子={seed}）"),
        ("JA", f"書き出し: {output} ({image.width}x{image.height}, シード={seed})"),
        ("KO", f"기록했습니다: {output} ({image.width}x{image.height}, 시드={seed})"),
    ):
        print(f"{tag}: {text}")


if __name__ == "__main__":
    main()

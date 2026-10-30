"""彩色水印预览（非验收）：官方 I1 宿主 + m1 彩色 logo，8x8 DCT QIM。

说明：
    这不是理论模块，也不进入 M0 的验收统计。它只回答一个问题：
    “彩色图片加上彩色水印，长什么样，提取回来还能不能认出来？”
    算法用最朴素的 QIM（每通道每 8x8 块 1 bit），没有攻击、没有纠错。

运行：
    python3 watermark_theory/exp/m0_color_preview.py

输出：
    plots/m0_color_preview.png
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from lib.metrics import ber, psnr, psnr_luma, psnr_per_channel, ssim

DELTA = 32.0
COEF = (3, 3)
LOGO_SIZE = 64
OFFICIAL = ROOT.parent / "P2g" / "official_information"


def load_rgb(path: Path) -> np.ndarray:
    bgr = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if bgr is None:
        raise FileNotFoundError(f"读不到图像：{path}")
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.float64)


def qim_embed_bit(coef: float, bit: int, delta: float) -> float:
    """bit=0 吸附到整数倍格点，bit=1 吸附到半整数倍格点。"""
    t = coef / delta
    k = np.round(t - 0.5) + 0.5 if bit else np.round(t)
    return float(k * delta)


def qim_decode_bit(coef: float, delta: float) -> int:
    """半整数倍 → 1，整数倍 → 0；判决边界在 ±Δ/4。"""
    t = coef / delta
    return int(abs(t - np.round(t)) > 0.25)


def embed_bits(host: np.ndarray, bits: np.ndarray, delta: float) -> np.ndarray:
    out = host.copy()
    h, w, channels = host.shape
    assert h % 8 == 0 and w % 8 == 0
    assert bits.shape == (h // 8, w // 8, channels), (bits.shape, h, w)
    u, v = COEF
    for c in range(channels):
        for by in range(h // 8):
            for bx in range(w // 8):
                block = out[by * 8 : (by + 1) * 8, bx * 8 : (bx + 1) * 8, c].astype(np.float32)
                dct = cv2.dct(block)
                dct[u, v] = qim_embed_bit(float(dct[u, v]), int(bits[by, bx, c]), delta)
                out[by * 8 : (by + 1) * 8, bx * 8 : (bx + 1) * 8, c] = cv2.idct(dct)
    return np.clip(out, 0.0, 255.0)


def extract_bits(marked: np.ndarray, delta: float) -> np.ndarray:
    h, w, channels = marked.shape
    bits = np.zeros((h // 8, w // 8, channels), dtype=np.uint8)
    u, v = COEF
    for c in range(channels):
        for by in range(h // 8):
            for bx in range(w // 8):
                block = marked[by * 8 : (by + 1) * 8, bx * 8 : (bx + 1) * 8, c].astype(np.float32)
                dct = cv2.dct(block)
                bits[by, bx, c] = qim_decode_bit(float(dct[u, v]), delta)
    return bits


def main() -> None:
    host = load_rgb(OFFICIAL / "image" / "I1.jpg")
    logo = cv2.resize(
        load_rgb(OFFICIAL / "watermark" / "m1.jpg"),
        (LOGO_SIZE, LOGO_SIZE),
        interpolation=cv2.INTER_AREA,
    )

    bits = (logo > 127.0).astype(np.uint8)
    print(f"宿主：{OFFICIAL / 'image' / 'I1.jpg'}  shape = {host.shape}")
    print(f"水印：{OFFICIAL / 'watermark' / 'm1.jpg'}  -> 重采样为 {LOGO_SIZE}x{LOGO_SIZE}")
    print(f"嵌入：8x8 DCT，系数 {COEF}，QIM 步长 Δ = {DELTA}，每块 1 bit/通道")

    marked = embed_bits(host, bits, DELTA)
    extracted = extract_bits(marked, DELTA)

    p_all = psnr(host, marked)
    p_c = psnr_per_channel(host, marked)
    p_y = psnr_luma(host, marked)
    s_all = ssim(host, marked)
    ber_c = np.array([ber(bits[..., c], extracted[..., c]) for c in range(3)])
    ber_all = float(np.mean(ber_c))

    print(f"\nPSNR_all = {p_all:.2f} dB")
    print(f"PSNR_R/G/B = {p_c[0]:.2f} / {p_c[1]:.2f} / {p_c[2]:.2f} dB")
    print(f"PSNR_Y = {p_y:.2f} dB   SSIM = {s_all:.4f}")
    print(f"BER_R/G/B = {ber_c[0]:.4f} / {ber_c[1]:.4f} / {ber_c[2]:.4f}")
    print(f"BER_all = {ber_all:.4f}")
    print("说明：这是无攻击的预览，BER 不为 0 基本只来自 [0,255] 截断。")

    # 出图：上排宿主/原水印/含水印图；下排差值、提取水印、指标。
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    axes[0, 0].imshow(np.clip(host, 0.0, 255.0) / 255.0)
    axes[0, 0].set_title("host: official I1 (512x512 RGB)")
    axes[0, 1].imshow(np.clip(logo, 0.0, 255.0) / 255.0, interpolation="nearest")
    axes[0, 1].set_title(f"color watermark: m1 -> {LOGO_SIZE}x{LOGO_SIZE}")
    axes[0, 2].imshow(np.clip(marked, 0.0, 255.0) / 255.0)
    axes[0, 2].set_title(f"marked (PSNR_all = {p_all:.2f} dB)")

    diff = np.abs(marked - host)
    axes[1, 0].imshow(np.clip(diff * 8.0, 0.0, 255.0).astype(np.uint8))
    axes[1, 0].set_title("|marked - host| amplified 8x")
    axes[1, 1].imshow((extracted * 255).astype(np.uint8), interpolation="nearest")
    axes[1, 1].set_title(f"extracted watermark (BER_all = {ber_all:.4f})")

    axes[1, 2].axis("off")
    text = (
        f"PSNR$_{{all}}$ = {p_all:.2f} dB\n"
        f"PSNR$_{{R/G/B}}$ = {p_c[0]:.2f} / {p_c[1]:.2f} / {p_c[2]:.2f} dB\n"
        f"PSNR$_Y$ = {p_y:.2f} dB\n"
        f"SSIM = {s_all:.4f}\n\n"
        f"BER$_R$ = {ber_c[0]:.4f}\n"
        f"BER$_G$ = {ber_c[1]:.4f}\n"
        f"BER$_B$ = {ber_c[2]:.4f}\n"
        f"BER$_{{all}}$ = {ber_all:.4f}\n\n"
        "NOT an acceptance test:\n"
        "no attack, no ECC, 1 bit per 8x8 block"
    )
    axes[1, 2].text(
        0.05, 0.5, text, ha="left", va="center", fontsize=11, family="monospace",
        transform=axes[1, 2].transAxes,
    )

    for ax in axes.ravel()[:5]:
        ax.axis("off")
    fig.suptitle("Color watermark preview (non-acceptance): I1 + m1, 8x8 DCT QIM")
    out_path = ROOT / "plots" / "m0_color_preview.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\n预览图已保存：{out_path}")


if __name__ == "__main__":
    main()

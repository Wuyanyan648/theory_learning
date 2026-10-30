"""M0 基线（彩色版）：三类合成 RGB 载体、逐通道 PSNR 记账、理论-实测对照。

运行：
    python3 watermark_theory/exp/m0_baseline.py

输出：
    plots/m0_baseline.png
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from lib.host import CHANNEL_NAMES, host_stats, make_hosts
from lib.metrics import psnr, psnr_per_channel, ssim

SEED = 20261031
DATA_RANGE = 255.0
SIGMAS = np.array([1.0, 2.0, 3.0, 5.0, 8.0, 12.0, 16.0, 20.0, 25.0, 30.0, 40.0])
# 刻意让三通道噪声强度不同，用来检验逐通道记账，而不是只验证单一通道。
CHANNEL_SCALE = np.array([1.0, 0.85, 1.15])
CHANNEL_COLORS = ("#d62728", "#2ca02c", "#1f77b4")
TOL_DB = 0.1

PLOT_NAMES = {
    "彩色 1/f 纹理": "color 1/f texture",
    "彩色平坦+硬边缘": "color flat + hard edges",
    "彩色自然感": "color natural-like",
}


def theoretical_psnr(sigma: float) -> float:
    """MSE = sigma^2 时的理论 PSNR。"""
    return float(10.0 * np.log10(DATA_RANGE ** 2 / sigma ** 2))


def print_host_table(rows: list[dict[str, object]]) -> None:
    print("\n表 1  三类合成彩色载体的分通道方差（512x512, RGB, float64）")
    print(
        f"{'载体':<18}{'σ²_R':>10}{'σ²_G':>10}{'σ²_B':>10}"
        f"{'总σ²':>10}{'均值':>9}{'值域':>16}"
    )
    for row in rows:
        var_c = np.asarray(row["var_c"])
        print(
            f"{row['name']:<18}{var_c[0]:10.2f}{var_c[1]:10.2f}{var_c[2]:10.2f}"
            f"{float(row['var']):10.2f}{float(row['mean']):9.2f}"
            f"   [{float(row['min']):.1f}, {float(row['max']):.1f}]"
        )


def main() -> None:
    hosts = make_hosts(SEED)
    rows = host_stats(hosts)
    print(f"seed = {SEED}")
    print_host_table(rows)

    # 零均值均匀噪声：U(-a, a), a = sqrt(3) * sigma_c，方差恰为 sigma_c^2。
    # 不做 [0,255] 截断，避免截断改变 MSE 而污染理论对照。
    rng = np.random.default_rng(SEED + 1)
    measured_total: dict[str, np.ndarray] = {}
    measured_channels: dict[str, np.ndarray] = {}
    for name, img in hosts.items():
        totals = []
        channels = []
        for sigma in SIGMAS:
            a = np.sqrt(3.0) * sigma * CHANNEL_SCALE
            noise = np.empty_like(img)
            for c in range(img.shape[2]):
                noise[..., c] = rng.uniform(-a[c], a[c], size=img.shape[:2])
            marked = img + noise
            totals.append(psnr(img, marked, DATA_RANGE))
            channels.append(psnr_per_channel(img, marked, DATA_RANGE))
        measured_total[name] = np.array(totals)
        measured_channels[name] = np.array(channels)

    theory_channels = np.array(
        [10.0 * np.log10(DATA_RANGE ** 2 / (s * CHANNEL_SCALE) ** 2) for s in SIGMAS]
    )
    theory_total = np.array(
        [
            10.0 * np.log10(DATA_RANGE ** 2 / float(np.mean((s * CHANNEL_SCALE) ** 2)))
            for s in SIGMAS
        ]
    )

    print("\n验收 1：逐通道 PSNR 与解析式 10·log10(255²/σ_c²) 的最大偏差（阈值 %.2f dB）" % TOL_DB)
    print(f"{'载体':<18}{'max|ΔPSNR_R|':>14}{'max|ΔPSNR_G|':>14}{'max|ΔPSNR_B|':>14}")
    max_dev_c = 0.0
    for name, values in measured_channels.items():
        dev = np.abs(values - theory_channels)
        max_dev_c = max(max_dev_c, float(dev.max()))
        print(f"{name:<18}{dev[:, 0].max():14.4f}{dev[:, 1].max():14.4f}{dev[:, 2].max():14.4f}")

    print("\n验收 2：总 PSNR 与 255²/mean_c(σ_c²) 记账的最大偏差（阈值 %.2f dB）" % TOL_DB)
    print(f"{'载体':<18}{'max|ΔPSNR_all|':>16}{'mean|ΔPSNR_all|':>17}")
    max_dev_all = 0.0
    for name, values in measured_total.items():
        dev = np.abs(values - theory_total)
        max_dev_all = max(max_dev_all, float(dev.max()))
        print(f"{name:<18}{dev.max():16.4f}{dev.mean():17.4f}")

    print("\nSSIM 自检（同一图应约为 1，彩色按通道平均）")
    for name, img in hosts.items():
        print(f"{name:<18} SSIM(x, x) = {ssim(img, img, DATA_RANGE):.6f}")

    print(f"\n总体验收：逐通道最大偏差 {max_dev_c:.4f} dB，总 PSNR 最大偏差 {max_dev_all:.4f} dB")
    passed = max_dev_c < TOL_DB and max_dev_all < TOL_DB
    print("RESULT:", "PASS" if passed else "FAIL")

    # 出图：上排三类彩色载体；下排左总 PSNR、右逐通道 PSNR。
    fig = plt.figure(figsize=(16, 9))
    gs = fig.add_gridspec(2, 6, height_ratios=[1.0, 1.25], hspace=0.32, wspace=0.55)

    for idx, (name, img) in enumerate(hosts.items()):
        ax = fig.add_subplot(gs[0, idx * 2 : idx * 2 + 2])
        ax.imshow(img / 255.0)
        ax.set_title(f"{PLOT_NAMES[name]}\n$\\sigma_x^2$ = {np.var(img):.1f}")
        ax.axis("off")

    ax = fig.add_subplot(gs[1, 0:3])
    ax.plot(SIGMAS, theory_total, "k--", linewidth=2.0,
            label="theory: $10\\log_{10}(255^2/\\overline{\\sigma_c^2})$")
    markers = ["o", "s", "^"]
    for (name, values), marker in zip(measured_total.items(), markers):
        ax.plot(SIGMAS, values, linestyle="none", marker=marker, markersize=7,
                label=f"{PLOT_NAMES[name]} measured")
    ax.set_xlabel("Base noise standard deviation $\\sigma$ (gray levels)")
    ax.set_ylabel("PSNR$_{all}$ (dB)")
    ax.set_title("Total PSNR vs noise (no clipping)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)

    ax = fig.add_subplot(gs[1, 3:6])
    ref_name = "彩色自然感"
    for c, ch in enumerate(CHANNEL_NAMES):
        ax.plot(SIGMAS, theory_channels[:, c], "--", color=CHANNEL_COLORS[c], linewidth=2.0,
                label=f"theory {ch}: $\\sigma_c$ = {CHANNEL_SCALE[c]:.2f}$\\sigma$")
        ax.plot(SIGMAS, measured_channels[ref_name][:, c], linestyle="none",
                marker="os^"[c], markersize=7, color=CHANNEL_COLORS[c],
                label=f"{ch} measured")
    ax.set_xlabel("Base noise standard deviation $\\sigma$ (gray levels)")
    ax.set_ylabel("PSNR$_c$ (dB)")
    ax.set_title(f"Per-channel PSNR: {PLOT_NAMES[ref_name]}")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)

    fig.suptitle(
        f"M0 (color): synthetic RGB hosts and PSNR accounting validation (seed={SEED})"
    )
    out_path = ROOT / "plots" / "m0_baseline.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\n主图已保存：{out_path}")


if __name__ == "__main__":
    main()

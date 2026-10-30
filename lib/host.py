"""合成彩色载体：彩色 1/f 纹理、彩色平坦+硬边缘、彩色自然感图。

约定：512x512、RGB、float64、范围 [0, 255]。
色彩空间统一用 RGB；内部生成时借助 YCrCb 让亮度与色度可分开控制。
"""

from __future__ import annotations

import cv2
import numpy as np

IMAGE_SIZE = 512
CHANNEL_NAMES = ("R", "G", "B")


def _normalize(img: np.ndarray, mean: float = 128.0, std: float = 40.0) -> np.ndarray:
    """线性拉伸到指定均值与标准差。"""
    img = np.asarray(img, dtype=np.float64)
    img = img - img.mean()
    s = float(img.std())
    if s < 1e-12:
        return np.full_like(img, mean, dtype=np.float64)
    return img / s * std + mean


def _clip255(img: np.ndarray) -> np.ndarray:
    return np.clip(img, 0.0, 255.0).astype(np.float64)


def _one_over_f(rng: np.random.Generator, size: int, beta: float) -> np.ndarray:
    """频域 1/f^beta 整形得到相关纹理。"""
    white = rng.normal(size=(size, size))
    fy = np.fft.fftfreq(size)[:, None]
    fx = np.fft.fftfreq(size)[None, :]
    radius = np.sqrt(fx * fx + fy * fy)
    # DC 处半径为 0，用最小频率代替以避免除零。
    radius = np.maximum(radius, 1.0 / size)
    spectrum = np.fft.fft2(white) / (radius ** beta)
    return np.real(np.fft.ifft2(spectrum))


def _ycc_to_rgb(y: np.ndarray, cr: np.ndarray, cb: np.ndarray) -> np.ndarray:
    """把 YCrCb 三分量（float64, [0,255]）转成 RGB。"""
    ycc = np.stack([y, cr, cb], axis=-1)
    ycc8 = np.clip(ycc, 0.0, 255.0).astype(np.uint8)
    rgb8 = cv2.cvtColor(ycc8, cv2.COLOR_YCrCb2RGB)
    return rgb8.astype(np.float64)


def _color_texture(
    rng: np.random.Generator,
    size: int,
    beta: float,
    luma_std: float,
    chroma_std: float,
) -> np.ndarray:
    """亮度走 1/f^beta，色度走更陡的低频场，合成彩色纹理。"""
    y = _normalize(_one_over_f(rng, size, beta), 128.0, luma_std)
    cr = _normalize(_one_over_f(rng, size, beta + 0.8), 128.0, chroma_std)
    cb = _normalize(_one_over_f(rng, size, beta + 0.8), 128.0, chroma_std)
    return _ycc_to_rgb(y, cr, cb)


def _flat_edges(rng: np.random.Generator, size: int) -> np.ndarray:
    """平坦区域 + 若干硬边缘彩色矩形。"""
    img = np.full((size, size, 3), 128.0, dtype=np.float64)
    third = size // 3
    img[0:third, 0:third] = (58.0, 62.0, 72.0)
    img[third : 2 * third, size // 4 : 3 * size // 4] = (205.0, 72.0, 55.0)
    img[2 * third :, size // 2 :] = (40.0, 45.0, 38.0)
    img[size // 4 : size // 2, size // 2 :] = (232.0, 220.0, 175.0)
    img += rng.normal(0.0, 1.5, size=(size, size, 3))
    return _clip255(img)


def _natural_like(rng: np.random.Generator, size: int) -> np.ndarray:
    """彩色 1/f 纹理 + 缓变光照 + 若干彩色团块，模拟自然图像统计。"""
    base = _color_texture(rng, size, beta=1.6, luma_std=32.0, chroma_std=9.0)

    yy, xx = np.mgrid[0:size, 0:size] / (size - 1)
    lighting = (xx + yy - 1.0)[..., None]
    img = base + lighting * np.array([20.0, 10.0, -15.0])

    blobs = [
        (0.30, 0.35, 0.12, 0.18, (-28.0, -14.0, -4.0)),
        (0.70, 0.65, 0.15, 0.12, (22.0, 14.0, 6.0)),
        (0.50, 0.80, 0.20, 0.10, (-16.0, -5.0, 16.0)),
    ]
    for cx, cy, sx, sy, amp in blobs:
        gaussian = np.exp(
            -(((xx - cx) ** 2) / (2.0 * sx * sx) + ((yy - cy) ** 2) / (2.0 * sy * sy))
        )
        img += gaussian[..., None] * np.array(amp)

    img += rng.normal(0.0, 2.0, size=(size, size, 3))
    return _clip255(img)


def make_hosts(seed: int = 20261031, size: int = IMAGE_SIZE) -> dict[str, np.ndarray]:
    """返回三类合成彩色载体（RGB, float64），键为可读名称。"""
    rng = np.random.default_rng(seed)
    return {
        "彩色 1/f 纹理": _color_texture(
            rng, size, beta=2.0, luma_std=36.0, chroma_std=10.0
        ),
        "彩色平坦+硬边缘": _flat_edges(rng, size),
        "彩色自然感": _natural_like(rng, size),
    }


def host_stats(hosts: dict[str, np.ndarray]) -> list[dict[str, object]]:
    """计算每类载体的整体统计与分通道方差。"""
    rows: list[dict[str, object]] = []
    for name, img in hosts.items():
        flat = img.reshape(-1, img.shape[2])
        rows.append(
            {
                "name": name,
                "mean": float(img.mean()),
                "var": float(img.var()),
                "std": float(img.std()),
                "var_c": np.var(flat, axis=0).astype(float),
                "min": float(img.min()),
                "max": float(img.max()),
                "shape": tuple(img.shape),
            }
        )
    return rows

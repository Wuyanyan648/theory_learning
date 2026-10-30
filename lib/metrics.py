"""通用度量：PSNR、SSIM、BER、归一化相关。

约定：图像为 float64、范围 [0, 255]；比特为 0/1 数组。
"""

from __future__ import annotations

import cv2
import numpy as np


def mse(a: np.ndarray, b: np.ndarray) -> float:
    """逐像素、逐通道的平均平方误差。"""
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    if a.shape != b.shape:
        raise ValueError(f"形状不一致: {a.shape} vs {b.shape}")
    return float(np.mean((a - b) ** 2))


def psnr(a: np.ndarray, b: np.ndarray, data_range: float = 255.0) -> float:
    """PSNR = 10 * log10(data_range^2 / MSE)，单位为 dB。"""
    m = mse(a, b)
    if m == 0.0:
        return float("inf")
    return float(10.0 * np.log10(data_range ** 2 / m))


def mse_per_channel(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """逐通道 MSE；灰度图返回长度为 1 的数组。"""
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    if a.shape != b.shape:
        raise ValueError(f"形状不一致: {a.shape} vs {b.shape}")
    if a.ndim == 2:
        return np.array([float(np.mean((a - b) ** 2))])
    return np.array([float(np.mean((a[..., c] - b[..., c]) ** 2)) for c in range(a.shape[2])])


def psnr_per_channel(
    a: np.ndarray, b: np.ndarray, data_range: float = 255.0
) -> np.ndarray:
    """逐通道 PSNR；MSE 为 0 的通道返回 inf。"""
    m = mse_per_channel(a, b)
    with np.errstate(divide="ignore"):
        return np.where(m > 0.0, 10.0 * np.log10(data_range ** 2 / m), np.inf)


def luma(img: np.ndarray) -> np.ndarray:
    """BT.601 亮度 Y = 0.299R + 0.587G + 0.114B；灰度图原样返回。"""
    img = np.asarray(img, dtype=np.float64)
    if img.ndim != 3:
        return img
    if img.shape[2] != 3:
        raise ValueError(f"亮度换算需要 3 通道 RGB，收到 {img.shape[2]} 通道")
    return img @ np.array([0.299, 0.587, 0.114], dtype=np.float64)


def psnr_luma(a: np.ndarray, b: np.ndarray, data_range: float = 255.0) -> float:
    """亮度通道 PSNR，仅用于感知/JPEG 对照。"""
    return psnr(luma(a), luma(b), data_range)


def ber(bits_a: np.ndarray, bits_b: np.ndarray) -> float:
    """误码率：两串等长比特中不一致的比例。"""
    a = np.asarray(bits_a).ravel().astype(bool)
    b = np.asarray(bits_b).ravel().astype(bool)
    if a.size != b.size:
        raise ValueError(f"比特数不一致: {a.size} vs {b.size}")
    if a.size == 0:
        return 0.0
    return float(np.mean(a != b))


def normalized_correlation(y: np.ndarray, w: np.ndarray) -> float:
    """归一化相关 rho = <y, w> / (||y|| * ||w||)。"""
    y = np.asarray(y, dtype=np.float64).ravel()
    w = np.asarray(w, dtype=np.float64).ravel()
    if y.size != w.size:
        raise ValueError(f"长度不一致: {y.size} vs {w.size}")
    denom = float(np.linalg.norm(y) * np.linalg.norm(w))
    if denom == 0.0:
        return 0.0
    return float(np.dot(y, w) / denom)


def ssim(
    a: np.ndarray,
    b: np.ndarray,
    data_range: float = 255.0,
    win_size: int = 11,
    sigma: float = 1.5,
    k1: float = 0.01,
    k2: float = 0.03,
) -> float:
    """结构相似性（SSIM），高斯窗，K1=0.01, K2=0.03。

    彩色图按通道分别计算后取平均。
    """
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    if a.shape != b.shape:
        raise ValueError(f"形状不一致: {a.shape} vs {b.shape}")
    if a.ndim == 3:
        return float(
            np.mean(
                [
                    ssim(a[..., c], b[..., c], data_range, win_size, sigma, k1, k2)
                    for c in range(a.shape[2])
                ]
            )
        )
    if a.ndim != 2:
        raise ValueError(f"仅支持 2D 灰度或 3D 多通道，收到 {a.ndim}D")

    c1 = (k1 * data_range) ** 2
    c2 = (k2 * data_range) ** 2

    mu_a = cv2.GaussianBlur(a, (win_size, win_size), sigma)
    mu_b = cv2.GaussianBlur(b, (win_size, win_size), sigma)
    mu_a2 = mu_a * mu_a
    mu_b2 = mu_b * mu_b
    mu_ab = mu_a * mu_b

    sigma_a2 = cv2.GaussianBlur(a * a, (win_size, win_size), sigma) - mu_a2
    sigma_b2 = cv2.GaussianBlur(b * b, (win_size, win_size), sigma) - mu_b2
    sigma_ab = cv2.GaussianBlur(a * b, (win_size, win_size), sigma) - mu_ab

    # 数值误差可能让方差略小于 0，裁剪到 0。
    sigma_a2 = np.maximum(sigma_a2, 0.0)
    sigma_b2 = np.maximum(sigma_b2, 0.0)

    numerator = (2.0 * mu_ab + c1) * (2.0 * sigma_ab + c2)
    denominator = (mu_a2 + mu_b2 + c1) * (sigma_a2 + sigma_b2 + c2)
    return float(np.mean(numerator / denominator))

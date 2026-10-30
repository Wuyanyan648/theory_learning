# 07 卡尔曼滤波与 LQG

> 卡尔曼滤波是有噪声情况下的最优状态估计器；与 LQR 结合得到 LQG，且满足分离原理。

## 7.1 随机线性系统

$$
\dot x = Ax + Bu + w, \qquad y = Cx + v
$$

- $w$：过程噪声，$\mathbb{E}[w]=0$，$\mathbb{E}[w(t)w^T(\tau)] = Q\delta(t-\tau)$
- $v$：测量噪声，$\mathbb{E}[v]=0$，$\mathbb{E}[v(t)v^T(\tau)] = R\delta(t-\tau)$
- $w, v$ 互不相关，与初始状态 $x(0)$ 不相关

## 7.2 卡尔曼滤波器（连续时间）

滤波器结构与 Luenberger 观测器相同：

$$
\dot{\hat{x}} = A \hat{x} + B u + L(y - C\hat{x})
$$

但增益 $L$ 由噪声统计最优决定：

$$
L = \Sigma C^T R^{-1}
$$

其中 $\Sigma = \Sigma^T \succeq 0$ 是误差协方差，满足**滤波 Riccati 方程**：

$$
\dot \Sigma = A\Sigma + \Sigma A^T + Q - \Sigma C^T R^{-1} C \Sigma
$$

稳态时 $\dot \Sigma = 0$，得到**代数 Riccati 方程**：

$$
A\Sigma + \Sigma A^T + Q - \Sigma C^T R^{-1} C \Sigma = 0
$$

## 7.3 离散时间卡尔曼滤波（预测-更新形式）

这是工程中最常用的形式。

**预测步**（时间更新）：

$$
\hat{x}_{k|k-1} = A \hat{x}_{k-1|k-1} + B u_{k-1}
$$
$$
P_{k|k-1} = A P_{k-1|k-1} A^T + Q
$$

**更新步**（测量更新）：

$$
K_k = P_{k|k-1} C^T (C P_{k|k-1} C^T + R)^{-1}
$$
$$
\hat{x}_{k|k} = \hat{x}_{k|k-1} + K_k (y_k - C \hat{x}_{k|k-1})
$$
$$
P_{k|k} = (I - K_k C) P_{k|k-1}
$$

其中 $K_k$ 是卡尔曼增益。

## 7.4 对偶性：LQR 与 Kalman

| LQR（控制） | Kalman（估计） |
|---|---|
| $A^T P + PA - PBR^{-1}B^T P + Q = 0$ | $A\Sigma + \Sigma A^T - \Sigma C^T R^{-1} C \Sigma + Q = 0$ |
| $K = R^{-1} B^T P$ | $L = \Sigma C^T R^{-1}$ |
| $(A,B)$ 可稳定 | $(C,A)$ 可检测 |

控制与估计在数学上完全对偶——这是 LQG 分离原理的根源。

## 7.5 LQG（Linear Quadratic Gaussian）控制

在有噪声情况下，LQR 的最优解为：

1. 用卡尔曼滤波器得到 $\hat{x}$；
2. 用 LQR 增益 $K$ 施加 $u = -K \hat{x}$。

**LQG 分离原理**：估计器（Kalman）与控制器（LQR）可**独立设计**，合起来仍是最优的。

闭环极点 = LQR 极点（$A-BK$）$\cup$ 卡尔曼极点（$A-LC$）。

## 7.6 LQG 的鲁棒性问题

注意：**LQG 不保证像 LQR 那样的鲁棒性裕度**。加入观测器后，LQR 的 60° 相位裕度保证丧失。若需要鲁棒性，需使用 LQG/LTR（Loop Transfer Recovery）或直接采用 H∞ 控制。

## 习题

1. 写出离散卡尔曼滤波的预测-更新五步公式。
2. 解释 LQR 与 Kalman 滤波的对偶关系。
3. 为什么 LQG 没有 LQR 的鲁棒性裕度保证？

# 06 LQR 线性二次型最优控制

> LQR 是最优控制在 LTI 系统 + 二次型指标下的特例，给出了状态反馈的"最优"增益，并具有优良的鲁棒性。

## 6.1 问题陈述

对系统 $\dot x = Ax + Bu$，寻找反馈 $u = -Kx$ 最小化二次型性能指标：

$$
J = \int_0^\infty \left( x^T Q x + u^T R u \right) dt
$$

其中 $Q = Q^T \succeq 0$，$R = R^T \succ 0$。

## 6.2 解的形式

最优控制为线性状态反馈

$$
u^*(t) = -K x(t), \qquad K = R^{-1} B^T P
$$

其中 $P = P^T \succ 0$ 是**代数 Riccati 方程（ARE）** 的唯一正定解：

$$
A^T P + P A - P B R^{-1} B^T P + Q = 0
$$

闭环矩阵 $A - BK = A - B R^{-1} B^T P$ 是 Hurwitz 的。

## 6.3 存在性与唯一性条件

ARE 存在唯一正定解且闭环稳定，当且仅当：
1. $(A, B)$ 可稳定（stabilizable）；
2. $(Q^{1/2}, A)$ 可检测（detectable）。

> 可稳定 = 不可控模态都稳定；可检测 = 不可观模态都稳定。

## 6.4 设计参数选择

- $Q$ 大 → 状态收敛快，控制量大；
- $R$ 大 → 控制量小，状态收敛慢；
- 常用 $Q = C^T C$（使 $x^T Q x = y^T y$，惩罚输出），$R = \rho I$ 调节 $\rho$。

**经典权衡**：LQR 本质是在状态误差与控制能量之间做 Pareto 最优权衡。

## 6.5 LQR 的鲁棒性裕度

LQR 具有著名的**保证裕度**：
- 相位裕度 $\ge 60^\circ$
- 增益裕度 $\ge 2$（即 $[1/2, \infty)$）

这是 LQR 相比手工极点配置的重要优势：最优解天然鲁棒。

**推导思路**：对 SISO 系统，返回差方程

$$
1 + K(sI - A)^{-1} B = 1 + L(s)
$$

可证明 $|1 + L(j\omega)| \ge 1$，从而推出上述裕度。

## 6.6 有限时间 LQR 与跟踪

有限时间指标

$$
J = x^T(T) P_T x(T) + \int_0^T (x^T Q x + u^T R u) dt
$$

解为 $u^*(t) = -R^{-1} B^T P(t) x(t)$，其中 $P(t)$ 满足**微分 Riccati 方程**：

$$
-\dot P = A^T P + P A - P B R^{-1} B^T P + Q, \quad P(T) = P_T
$$

## 6.7 输出调节与跟踪的 LQR 扩展

跟踪参考 $r$：引入积分器增广（见 03 章 3.5），对增广系统做 LQR，即可实现零稳态误差跟踪。

## 习题

1. 对 $(A, B) = \left(\begin{pmatrix}0&1\\0&0\end{pmatrix}, \begin{pmatrix}0\\1\end{pmatrix}\right)$，$Q=I$，$R=1$，求 LQR 增益。
2. 写出并求解对应的 Riccati 方程。
3. 解释为什么 LQR 的相位裕度至少 $60^\circ$。

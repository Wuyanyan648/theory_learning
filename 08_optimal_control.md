# 08 最优控制

> 最优控制问题：在给定系统动态和约束下，寻找使性能指标最小（或最大）的控制律。核心工具：变分法、Pontryagin 极小值原理、动态规划。

## 8.1 问题的一般形式

系统 $\dot x = f(x, u, t)$，$x(t_0) = x_0$，目标函数（Bolza 型）：

$$
J = \phi(x(t_f), t_f) + \int_{t_0}^{t_f} L(x, u, t)\, dt
$$

求 $u^*(t)$ 使 $J$ 最小。可能有终端约束 $\psi(x(t_f), t_f) = 0$。

## 8.2 变分法推导

构造增广泛函（Lagrange 乘子 $\lambda(t)$）：

$$
J' = \phi(x(t_f), t_f) + \int_{t_0}^{t_f} \left[ L(x,u,t) + \lambda^T(t)\big(f(x,u,t) - \dot x\big) \right] dt
$$

定义**Hamilton 函数**：

$$
H(x, u, \lambda, t) = L(x, u, t) + \lambda^T f(x, u, t)
$$

分部积分后令变分 $\delta J' = 0$，得到：

### 最优性必要条件

1. **状态方程**：$\dot x = \frac{\partial H}{\partial \lambda} = f(x, u, t)$
2. **协态方程**：$\dot \lambda = -\frac{\partial H}{\partial x}$
3. **驻值条件**：$\frac{\partial H}{\partial u} = 0$
4. **横截条件**：

$$
\lambda(t_f) = \left[ \frac{\partial \phi}{\partial x} + \frac{\partial \psi^T}{\partial x} \nu \right]_{t_f}
$$

其中 $\nu$ 是终端约束的乘子。若终端自由，$\lambda(t_f) = \partial \phi/\partial x|_{t_f}$；若终端固定，则无此条件。

## 8.3 Pontryagin 极小值原理

变分法要求 $H$ 对 $u$ 可微且 $u$ 无约束。极小值原理推广到 $u$ 受约束的情形：

**定理**：最优控制 $u^*(t)$ 使 Hamilton 函数全局最小：

$$
H(x^*(t), u^*(t), \lambda^*(t), t) \le H(x^*(t), u, \lambda^*(t), t), \quad \forall u \in \Omega
$$

其余条件（状态、协态、横截）不变。

> 极小值原理是必要条件，不是充分条件。对于凸问题，它也是充分的。

## 8.4 动态规划与 HJB 方程

**Bellman 最优性原理**：最优策略的任何子策略也是最优的。

定义价值函数 $V(x, t) = \min_{u} J(x, t)$。Bellman 方程：

$$
-\frac{\partial V}{\partial t} = \min_u \left[ L(x,u,t) + \frac{\partial V^T}{\partial x} f(x,u,t) \right]
$$

即 **Hamilton-Jacobi-Bellman (HJB) 方程**：

$$
-\frac{\partial V}{\partial t} = \min_u H\left(x, u, \frac{\partial V}{\partial x}, t\right)
$$

无限时域定常问题中 $\partial V/\partial t = 0$。

### LQR 与 HJB

对 LQR 问题，设 $V(x) = x^T P x$，代入 HJB 方程可直接推出 Riccati 方程。这说明 LQR 是 HJB 的二次型特例。

## 8.5 典型应用：双积分器时间最优

系统 $\ddot q = u$，$|u| \le 1$，从 $(q_0, \dot q_0)$ 到原点的**时间最优**控制。

由极小值原理，$H = 1 + \lambda_1 \dot q + \lambda_2 u$，最优 $u^* = -\text{sgn}(\lambda_2)$。

结论：时间最优控制是**Bang-Bang** 控制，最多一次切换，切换曲线为 $\dot q = -\text{sgn}(q) \sqrt{2|q|}$。

## 8.6 极小值原理 vs 动态规划

| | 极小值原理 | 动态规划 |
|---|---|---|
| 本质 | 必要条件（开环） | 充分必要（闭环） |
| 维度 | 解 2n 维两点边值问题 | 解 n 维 PDE（维数灾难） |
| 约束 | 直接处理 | 需特殊处理 |
| 适用 | 低维/线性/特定结构 | 理论完整，计算困难 |

## 习题

1. 写出 Bolza 型最优控制问题的必要条件。
2. 用极小值原理求 $\dot x = u$，$x(0)=1$，$J = \int_0^1 (x^2 + u^2) dt$ 的最优解。
3. 解释为什么时间最优控制常为 Bang-Bang。

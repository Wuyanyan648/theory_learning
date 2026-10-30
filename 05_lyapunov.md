# 05 李雅普诺夫稳定性理论

> 李雅普诺夫方法是分析（非线性）系统稳定性的核心工具，分为"间接法"（线性化）和"直接法"（能量函数）。

## 5.1 稳定性定义（平衡点 0）

考虑 $\dot x = f(x)$，$f(0)=0$。

- **Lyapunov 稳定**：对任意 $\varepsilon > 0$，存在 $\delta > 0$，使 $\|x(0)\| < \delta \Rightarrow \|x(t)\| < \varepsilon,\ \forall t \ge 0$。
- **渐近稳定**：Lyapunov 稳定 **且** $\lim_{t\to\infty} x(t) = 0$。
- **指数稳定**：存在 $\alpha, \lambda > 0$，使 $\|x(t)\| \le \alpha e^{-\lambda t}\|x(0)\|$。
- **全局渐近稳定**：渐近稳定且对任意 $x(0) \in \mathbb{R}^n$ 成立。
- **不稳定**：不 Lyapunov 稳定。

## 5.2 Lyapunov 直接法（第二法）

**核心思想**：若系统的"能量"随时间衰减，则系统稳定。

### 定理（局部渐近稳定）

若存在连续可微的正定函数 $V(x)$（$V(0)=0$，$V(x)>0$ for $x\neq 0$）使得

$$
\dot V(x) = \nabla V^T f(x) < 0 \quad \text{for } x \neq 0
$$

则原点渐近稳定。$V$ 称为**Lyapunov 函数**。

若 $\dot V \le 0$（半负定），则原点 Lyapunov 稳定。

### 全局渐近稳定

若 $V$ 还满足**径向无界**（$\|x\| \to \infty \Rightarrow V(x) \to \infty$）且 $\dot V < 0$，则全局渐近稳定。

## 5.3 不变集原理（LaSalle）

当 $\dot V \le 0$（只半负定）时，用 LaSalle 不变集原理判断渐近稳定：

**定理**：设 $\Omega = \{x : \dot V(x) = 0\}$，$M$ 是 $\Omega$ 中最大不变集。若解有界，则所有解收敛到 $M$。

特别地，若 $M = \{0\}$，则渐近稳定。

## 5.4 线性系统的 Lyapunov 判据

对 $\dot x = Ax$，取二次型 $V(x) = x^T P x$，$P \succ 0$。则

$$
\dot V = x^T (A^T P + P A) x =: -x^T Q x
$$

要求 $Q \succ 0$，即解**Lyapunov 方程**：

$$
A^T P + P A = -Q
$$

**定理**：$A$  Hurwitz（所有特征值实部 < 0）$\iff$ 对任意 $Q \succ 0$，存在唯一 $P \succ 0$ 满足 $A^T P + P A = -Q$。

> 线性系统中可先选 $Q = I$ 解出 $P$，检验 $P \succ 0$ 即可判定稳定性。

## 5.5 Lyapunov 间接法（线性化）

对 $\dot x = f(x)$，$f(0)=0$，$A = \partial f/\partial x|_0$。

- 若 $A$ Hurwitz → 原点局部渐近稳定。
- 若 $A$ 有特征值实部 > 0 → 原点不稳定。
- 若 $A$ 临界稳定（实部 = 0）→ 线性化无法判定，需用直接法。

## 5.6 构造 Lyapunov 函数的常用方法

1. **二次型**：$V = x^T P x$，解 Lyapunov 方程（线性/类线性系统）。
2. **能量函数**：物理系统的总能量（动能+势能）。
3. **变量梯度法**：先设 $\nabla V$，积分得 $V$。
4. **Krasovskii 方法**：$V = f^T(x) P f(x)$。
5. **Luré/波波夫方法**：处理含非线性扇形环节的系统。

## 5.7 非线性系统稳定性补充

- **Chetaev 定理**（不稳定性）：若在原点某邻域内存在 $V$，在某区域 $V>0$ 且 $\dot V > 0$，则不稳定。
- **输入-状态稳定（ISS）**：$\|x(t)\| \le \beta(\|x(0)\|, t) + \gamma(\|u\|_\infty)$，结合了 Lyapunov 与有界输入概念。
- **小增益定理**：两个 ISS 子系统反馈互联，若增益乘积 < 1，则闭环 ISS。

## 习题

1. 用 Lyapunov 方程判断 $A = \begin{pmatrix}-1&1\\0&-2\end{pmatrix}$ 的稳定性。
2. 对 $\dot x_1 = -x_1 + x_2,\ \dot x_2 = -x_1 - x_2^3$，构造 Lyapunov 函数证明渐近稳定。
3. 说明为什么线性化方法在临界情形失效。

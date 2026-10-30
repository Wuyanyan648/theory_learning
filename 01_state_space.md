# 01 状态空间分析

> 状态空间方法是高级控制理论的语言。本章回顾线性系统的状态方程描述、解的结构、矩阵指数以及模态分析。

## 1.1 状态空间模型

一个线性时不变（LTI）系统的状态空间表示：

$$
\dot x(t) = A x(t) + B u(t), \qquad y(t) = C x(t) + D u(t)
$$

其中 $A \in \mathbb{R}^{n\times n}$ 为状态矩阵，$B \in \mathbb{R}^{n\times m}$ 为输入矩阵，$C \in \mathbb{R}^{p\times n}$ 为输出矩阵，$D \in \mathbb{R}^{p\times m}$ 为直接馈通项。

**传递函数矩阵**：对零初始条件拉普拉斯变换得

$$
Y(s) = \left[ C (sI - A)^{-1} B + D \right] U(s) =: G(s) U(s)
$$

$G(s)$ 的极点包含在 $\sigma(A)$ 中。

## 1.2 状态方程的解

齐次解 $\dot x = Ax$：

$$
x(t) = e^{At} x(0), \qquad e^{At} := \sum_{k=0}^{\infty} \frac{A^k t^k}{k!}
$$

非齐次解（卷积形式）：

$$
x(t) = e^{At} x(0) + \int_0^t e^{A(t-\tau)} B u(\tau)\, d\tau
$$

**矩阵指数的性质**：
- $e^{A(t+s)} = e^{At} e^{As}$
- $\frac{d}{dt} e^{At} = A e^{At} = e^{At} A$
- 若 $A = P J P^{-1}$（Jordan 标准形），则 $e^{At} = P e^{Jt} P^{-1}$

## 1.3 模态分析

设 $A$ 的特征值为 $\lambda_i$（即系统极点）。每个特征值对应一个**模态** $e^{\lambda_i t}$（重根时含 $t^k e^{\lambda_i t}$ 项）。

- $\Re(\lambda_i) < 0$：模态衰减（稳定）
- $\Re(\lambda_i) = 0$：临界（无阻尼振荡或常值）
- $\Re(\lambda_i) > 0$：模态发散（不稳定）

**对角化**：若 $A$ 可对角化 $A = T \Lambda T^{-1}$，令 $z = T^{-1} x$，则

$$
\dot z = \Lambda z + T^{-1} B u
$$

各模态解耦。$T$ 的列是右特征向量，$T^{-1}$ 的行是左特征向量。

## 1.4 平衡点与线性化

非线性系统 $\dot x = f(x, u)$ 的平衡点 $(x_e, u_e)$ 满足 $f(x_e, u_e) = 0$。

在平衡点处泰勒展开并忽略高阶项，得到**线性化模型**：

$$
\delta \dot x = A \delta x + B \delta u
$$

其中

$$
A = \left.\frac{\partial f}{\partial x}\right|_{x_e,u_e}, \qquad B = \left.\frac{\partial f}{\partial u}\right|_{x_e,u_e}
$$

线性化后的稳定性仅能反映平衡点局部行为。

## 1.5 离散化

连续系统 $\dot x = Ax + Bu$，采样周期 $T$，零阶保持：

$$
x_{k+1} = A_d x_k + B_d u_k
$$

$$
A_d = e^{AT}, \qquad B_d = \int_0^T e^{A\tau} d\tau \cdot B
$$

## 1.6 不变子空间（几何观点）

子空间 $\mathcal{V} \subset \mathbb{R}^n$ 是 $A$-不变的，若 $A\mathcal{V} \subseteq \mathcal{V}$。

- 可控子空间 $\langle A | B \rangle = \text{Im}(B) + A\text{Im}(B) + \cdots + A^{n-1}\text{Im}(B)$
- 不可观子空间 $\ker(C) \cap \ker(CA) \cap \cdots \cap \ker(CA^{n-1})$

这些子空间为后续可控性/可观性分析提供几何基础。

## 习题

1. 证明 $e^{A(t+s)} = e^{At} e^{As}$。
2. 求 $A = \begin{pmatrix} 0 & 1 \\ -\omega_n^2 & -2\zeta\omega_n \end{pmatrix}$ 的模态，讨论 $\zeta$ 对响应的影响。
3. 推导连续系统离散化公式中的 $B_d$。

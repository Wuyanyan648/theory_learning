# 02 可控性与可观性

> 可控性回答"输入能否驱动状态到任意位置"，可观性回答"输出能否反映全部状态信息"。这是状态反馈与观测器设计的前提。

## 2.1 可控性（Controllability）

**定义**：系统在 $t_0$ 可控，若对任意 $x_0, x_f$，存在 $u(t)$ 在有限时间内将 $x_0$ 转移到 $x_f$。

### 可控性矩阵判据

LTI 系统 $(A, B)$ 可控 $\iff$ 可控性矩阵满秩：

$$
\mathcal{C} = \begin{bmatrix} B & AB & A^2 B & \cdots & A^{n-1} B \end{bmatrix}, \qquad \text{rank}(\mathcal{C}) = n
$$

### PBH 判据

$(A, B)$ 可控 $\iff$ 对所有 $\lambda \in \sigma(A)$，

$$
\text{rank}\begin{bmatrix} \lambda I - A & B \end{bmatrix} = n
$$

等价地：不存在左特征向量 $q^T A = \lambda q^T$ 使得 $q^T B = 0$（即没有"与输入解耦"的模态）。

### 可控性 Gramian

有限时间可控性 Gramian：

$$
W_c(0, t_1) = \int_0^{t_1} e^{-A\tau} B B^T e^{-A^T \tau}\, d\tau
$$

系统可控 $\iff W_c$ 正定。从 $x_0$ 到原点的最小能量控制为

$$
u(t) = -B^T e^{-A^T t} W_c^{-1}(0, t_1) x_0
$$

## 2.2 可观性（Observability）

**定义**：若由 $y(t)$ 在 $[t_0, t_1]$ 上的测量可唯一确定 $x(t_0)$，则系统可观。

### 可观性矩阵判据

$(C, A)$ 可观 $\iff$ 可观性矩阵满秩：

$$
\mathcal{O} = \begin{bmatrix} C \\ CA \\ \vdots \\ CA^{n-1} \end{bmatrix}, \qquad \text{rank}(\mathcal{O}) = n
$$

### PBH 判据

$(C, A)$ 可观 $\iff$ 对所有 $\lambda \in \sigma(A)$，

$$
\text{rank}\begin{bmatrix} \lambda I - A \\ C \end{bmatrix} = n
$$

等价地：不存在右特征向量 $A v = \lambda v$ 使得 $C v = 0$（即没有"对输出不可见"的模态）。

### 可观性 Gramian

$$
W_o(0, t_1) = \int_0^{t_1} e^{A^T \tau} C^T C e^{A\tau}\, d\tau
$$

系统可观 $\iff W_o$ 正定。

## 2.3 对偶原理

**$(A, B)$ 可控 $\iff$ $(B^T, A^T)$ 可观。**

因此可控性与可观性的所有结论可对偶互换。

## 2.4 Kalman 分解

任意 LTI 系统可经坐标变换分解为四个子系统：

```
        ┌───────────┬───────────┐
        │ 可控可观   │ 可控不可观 │
        ├───────────┼───────────┤
        │ 不可控可观 │ 不可控不可观│
        └───────────┴───────────┘
```

传递函数矩阵 $G(s) = C(sI-A)^{-1}B+D$ 仅由**可控可观**子系统决定。

## 2.5 最小实现

**最小实现**：给定传递函数 $G(s)$，阶数最小的状态空间实现 $(A,B,C,D)$。

**定理**：实现 $(A,B,C,D)$ 是最小的 $\iff$ $(A,B)$ 可控且 $(C,A)$ 可观。

两个最小实现之间由相似变换 $T$ 联系：$A_2 = T A_1 T^{-1}$，$B_2 = T B_1$，$C_2 = C_1 T^{-1}$。

## 2.6 极点-零点对消与最小实现

传递函数的极点-零点对消意味着存在不可控或不可观模态，该实现非最小。若对消的极点在右半平面，则系统存在**隐藏的不稳定模态**（内部不稳定但外部 BIBO 稳定），这是危险的。

## 习题

1. 判断 $(A, B) = \left(\begin{pmatrix}1&1\\0&1\end{pmatrix}, \begin{pmatrix}1\\0\end{pmatrix}\right)$ 是否可控。
2. 用 PBH 判据重做第 1 题。
3. 证明对偶原理。
4. 说明为什么最小实现必可控可观。

# 03 状态反馈与极点配置

> 状态反馈 $u = -Kx + r$ 是现代控制的核心操作。可控性保证了我们可以任意配置闭环极点。

## 3.1 状态反馈律

对系统 $\dot x = Ax + Bu$，施加状态反馈

$$
u = -K x + r
$$

其中 $K \in \mathbb{R}^{m \times n}$ 是反馈增益矩阵，$r$ 是参考输入。闭环系统：

$$
\dot x = (A - BK) x + B r
$$

闭环极点由 $\sigma(A - BK)$ 决定。

## 3.2 极点配置定理

**定理**：闭环极点可任意配置（一组自共轭的复数）$\iff$ $(A, B)$ 可控。

> 注意："任意配置"指可放置到复平面上任何位置（共轭成对），但不改变极点个数。

### 单输入情形：Ackermann 公式

对单输入系统，期望闭环特征多项式 $\alpha_{des}(s) = \prod_{i=1}^n (s - p_i)$，则

$$
K = \begin{bmatrix} 0 & \cdots & 0 & 1 \end{bmatrix} \mathcal{C}^{-1} \alpha_{des}(A)
$$

其中 $\mathcal{C} = [B\ AB\ \cdots\ A^{n-1}B]$ 是可控性矩阵，$\alpha_{des}(A)$ 是将 $A$ 代入期望多项式。

**等价公式（更直观）**：

$$
K = \begin{bmatrix} 1 & \cdots & 1 \end{bmatrix} \mathcal{C}^{-1} (A - p_1 I)(A - p_2 I)\cdots(A - p_n I)
$$

### 多输入情形

多输入极点配置不唯一。常用方法：
1. **SISO 化**：选一个输入列，使其与 $A$ 构成可控对，再用单输入公式。
2. **鲁棒极点配置**：最小化特征值对摄动的灵敏度。
3. **LQR**（见第 06 章）：通过优化间接得到增益，天然具有良好鲁棒性。

## 3.3 参考输入与稳态跟踪

引入参考输入 $r$ 后，$u = -Kx + \bar N r$。选 $\bar N$ 使稳态 $y_{ss} = r$（单位增益）：

$$
\bar N = -\left[ C(A-BK)^{-1}B \right]^{-1}
$$

（适用于 $D=0$ 且逆存在的情况。）

更系统的做法是引入**积分器**消除稳态误差（见 3.5）。

## 3.4 反馈对可控性/可观性的影响

- 状态反馈**不改变可控性**：$(A-BK, B)$ 与 $(A, B)$ 有相同的可控子空间。
- 状态反馈**可能改变可观性**：可能制造对消使某些模态不可观。

## 3.5 积分控制与增广系统

为消除常值扰动引起的稳态误差，引入积分状态 $x_I$：

$$
\dot x_I = r - y = r - Cx
$$

增广系统：

$$
\frac{d}{dt}\begin{bmatrix} x \\ x_I \end{bmatrix} = \begin{bmatrix} A & 0 \\ -C & 0 \end{bmatrix}\begin{bmatrix} x \\ x_I \end{bmatrix} + \begin{bmatrix} B \\ 0 \end{bmatrix}u + \begin{bmatrix} 0 \\ I \end{bmatrix}r
$$

若 $(A, B)$ 可控且 $(C, A)$ 在 $s=0$ 处可观（无零极点对消在原点），则增广系统可控，可对增广系统做极点配置。

## 3.6 状态反馈解耦

多输入多输出系统可通过状态反馈 + 预补偿实现**解耦**：每个输出仅由一个参考输入控制。

定义**解耦指数** $d_i$：使 $c_i A^{d_i} B \neq 0$ 的最小非负整数（$c_i$ 是 $C$ 的第 $i$ 行）。

构造解耦矩阵：

$$
D^* = \begin{bmatrix} c_1 A^{d_1} B \\ \vdots \\ c_p A^{d_p} B \end{bmatrix}
$$

若 $D^*$ 非奇异，取

$$
u = -K x + D^{*-1} r, \qquad K = (D^*)^{-1} \begin{bmatrix} c_1 A^{d_1 + 1} \\ \vdots \\ c_p A^{d_p + 1} \end{bmatrix}
$$

则闭环传递函数矩阵为对角阵：

$$
G_{cl}(s) = \text{diag}\left(\frac{1}{s^{d_1+1}}, \ldots, \frac{1}{s^{d_p+1}}\right)
$$

## 习题

1. 对 $(A, B) = \left(\begin{pmatrix}0&1\\-1&0\end{pmatrix}, \begin{pmatrix}0\\1\end{pmatrix}\right)$，配置闭环极点到 $-1\pm j$。
2. 证明状态反馈不改变可控子空间。
3. 解释为什么状态反馈可能破坏可观性，举例说明。

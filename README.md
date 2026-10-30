# 高级控制理论学习笔记

> 本仓库用于系统学习**高级控制理论（Advanced Control Theory）**，以状态空间方法为主线，从线性系统分析逐步过渡到最优、鲁棒与非线性控制。

## 学习路径

```
线性系统状态空间分析
        │
        ▼
  可控性 / 可观性  ──────────► 状态反馈（极点配置）
        │                            │
        ▼                            ▼
  李雅普诺夫稳定性              状态观测器（Luenberger）
        │                            │
        └──────────┬─────────────────┘
                   ▼
          LQR 最优状态反馈
                   │
                   ▼
         卡尔曼滤波 ──► LQG / 分离原理
                   │
                   ▼
     最优控制（极小值原理 / 动态规划）
                   │
                   ▼
   鲁棒控制 (H∞) / 自适应控制 / 非线性控制 / MPC
```

## 文件索引

| # | 主题 | 核心内容 |
|---|------|----------|
| 01 | [状态空间分析](01_state_space.md) | 状态方程、解的形式、矩阵指数、模态分析、平衡点 |
| 02 | [可控性与可观性](02_controllability_observability.md) | 可控/可观判据、PBH 判据、Kalman 分解、最小实现 |
| 03 | [状态反馈与极点配置](03_state_feedback_pole_placement.md) | 状态反馈、极点配置定理、Ackermann 公式、解耦 |
| 04 | [状态观测器](04_observers.md) | Luenberger 观测器、全阶/降阶观测器、分离原理 |
| 05 | [李雅普诺夫稳定性](05_lyapunov.md) | 稳定性定义、Lyapunov 直接法、线性系统判据、不变集原理 |
| 06 | [LQR 最优控制](06_lqr.md) | 二次型性能指标、Riccati 方程、LQR 增益、鲁棒性裕度 |
| 07 | [卡尔曼滤波与 LQG](07_kalman_lqg.md) | 卡尔曼滤波器推导、预测-更新、LQG 与分离原理 |
| 08 | [最优控制](08_optimal_control.md) | 变分法、Pontryagin 极小值原理、动态规划与 HJB |
| 09 | [鲁棒 / 自适应 / 非线性 / MPC 概览](09_advanced_topics.md) | H∞ 控制、μ 综合、自适应控制、反馈线性化、MPC |

## 推荐教材

- **T. Kailath**, *Linear Systems* — 线性系统的经典与严谨参考
- **K. Åström & R. Murray**, *Feedback Systems* — 控制思维的优秀入门到进阶
- **B. Anderson & J. Moore**, *Optimal Control: Linear Quadratic Methods* — LQR/LQG 权威
- **H. Khalil**, *Nonlinear Systems* — 非线性控制与李雅普诺夫
- **J. Doyle, B. Francis, A. Tannenbaum**, *Feedback Control Theory* — 鲁棒控制经典

## 记号约定

- 状态向量 $x \in \mathbb{R}^n$，输入 $u \in \mathbb{R}^m$，输出 $y \in \mathbb{R}^p$
- 连续时间：$\dot x = Ax + Bu,\ y = Cx + Du$
- 离散时间：$x_{k+1} = Ax_k + Bu_k,\ y_k = Cx_k + Du_k$
- $I$ 为单位阵，$\sigma(A)$ 为 $A$ 的谱，$\Re(\cdot)$ 取实部

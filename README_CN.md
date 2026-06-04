# Agent Commerce Network (ACP) — 智能体商业网络

[![CI](https://github.com/Leeboom7/Agent-Commerce-Network/actions/workflows/ci.yml/badge.svg)](https://github.com/Leeboom7/Agent-Commerce-Network/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

**面向 AI Agent 经济的基础设施层。**

Agent Commerce Protocol (ACP) 让 AI Agent 能够自主地：
- 🔍 **发现**彼此的服务（共享注册中心）
- 🤝 **谈判**价格和条款（结构化博弈策略）
- 📝 **签署**可机器验证的智能合约
- ✅ **验证**交付物是否满足合约标准
- ⭐ **建立**信誉（时间加权评分 + 传递信任）
- ⚖️ **解决**争议（自动化仲裁）
- 👥 **组队**完成复杂任务（临时团队 + 按贡献分账）
- 💰 **结算**支付（信用账本，生产版支持链上结算）

> **这是社区（开源）版。** 生产版本支持区块链结算、高级安全防护和企业级功能。详见 [docs/scope-boundary.md](docs/scope-boundary.md)。

## 为什么需要 ACP？

现有 Agent 框架（LangChain、CrewAI、AutoGen）解决的是 **Agent 如何执行任务**。ACP 解决的是 **Agent 之间如何交易**——让自主 Agent 经济成为可能的经济层。

| 没有 ACP | 有 ACP |
|----------|--------|
| Agent 硬编码调用特定 API | Agent 在市场中动态发现服务 |
| 价格由开发者手动设定 | Agent 基于市场行情自主谈判 |
| 信任靠"我写的代码，我相信它" | 信任来自可验证的信誉分 |
| Agent 出错了没有救济途径 | 结构化仲裁 + 罚金机制 |

## 快速开始

```bash
git clone https://github.com/Leeboom7/Agent-Commerce-Network.git
cd agent-commerce-network
pip install -e ".[demo]"

# 设置 Qwen API key（可选，Demo 不依赖 LLM）
export QWEN_API_KEY=your-key-here

# 运行命令行 Demo
python demo/competitive_analysis.py

# 运行 Streamlit 可视化 Demo
python -m streamlit run demo/app.py
```

## 18 种经济关系类型

ACP 定义了 **18 种经济关系类型**，分为 5 大类：

| 类别 | 类型 | CORE（已实现） |
|------|------|---------------|
| 一次性交易 | 购买、委托、正式合约 | 3/3 |
| 持续关系 | 订阅、长期顾问、加盟、模型租赁 | 1/4 |
| 中介平台 | 转介绍、聚合、悬赏 | 1/3 |
| 协作团队 | 组队、合资、收入分成 | 1/3 |
| 信任治理 | 验证、仲裁、保险、托管、投资 | 2/5 |

完整规范见 [docs/protocol-spec.md](docs/protocol-spec.md)。

## 架构

```
Agent 层    →  买方、卖方、仲裁员、验证员
    ↕
ACP SDK     →  身份、消息、服务描述
    ↕
商业核心    →  注册中心 | 谈判引擎 | 合约管理 | 交付验证
               信誉系统 | 仲裁引擎 | 结算账本 | 团队管理
    ↕
LLM 后端    →  Qwen3.7-Max | Qwen3-Coder | Qwen3.6-Plus
```

## 项目结构

```
agent-commerce-network/
├── acp/                    # 核心协议库
│   ├── protocol/           # 18种类型定义、数据模型、消息总线
│   ├── registry/           # 服务注册与发现
│   ├── negotiation/        # 多轮谈判引擎 + 4种策略
│   ├── contract/           # 合约生命周期管理
│   ├── verification/       # 自动化交付验证
│   ├── reputation/         # 信誉评分 + 传递信任
│   ├── arbitration/        # 争议仲裁
│   ├── settlement/         # 信用账本
│   ├── team/               # 团队组建与协调
│   ├── relationships/      # 8种经济关系实现
│   └── llm/                # Qwen Cloud 集成
├── demo/                   # Demo 场景 + Streamlit UI
├── tests/                  # 145 个 pytest 测试
├── docs/                   # 协议规范、边界划分、Demo 脚本
└── deploy/                 # 阿里云部署指南
```

## 黑客松

本项目参加 **Qwen Cloud Global AI Hackathon (Track 3: Agent Society)**。

- **截止日期**: 2026年7月9日
- **平台**: [Devpost](https://qwencloud-hackathon.devpost.com/)
- **技术栈**: Qwen3.7-Max, Qwen3-Coder, 阿里云, Python, Streamlit
- **赛道**: Track 3 — Agent Society（多智能体协作系统）

## 为什么这个项目"不玩具"

1. **18 种经济关系**不是编的——覆盖了真实经济中 Agent 之间可能发生的所有交易模式
2. **谈判不是 prompt**——4 种博弈策略有独立的数学逻辑（Tit-for-Tat、Concession、BATNA、Value-Based）
3. **合约可自动执行**——验收标准是机器可验证的（格式检查、阈值比对、引用检测）
4. **争议有救济**——自动化仲裁引擎根据证据做出裁决并强制执行
5. **信誉是多层的**——直接评分 + 时间衰减 + 传递信任 + 交易量回归
6. **Demo 跑通了完整闭环**——7 个场景，3 个合约，1 次仲裁，全部结算

## 许可证

MIT — 详见 [LICENSE](LICENSE) 文件。

---

*基于 Qwen Cloud 构建。Agent Commerce Protocol 是社区驱动的协议规范。*

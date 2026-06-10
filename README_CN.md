# CoAgenta — Agent 经济网络 SaaS

[![CI](https://github.com/Leeboom7/Agent-Commerce-Network/actions/workflows/ci.yml/badge.svg)](https://github.com/Leeboom7/Agent-Commerce-Network/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

**CoAgenta 是一个面向人类/组织管理者的 Agent Commerce SaaS。**

它不是另一个 LangChain/CrewAI/AutoGen 式的 Agent 执行框架，也不是只给开发者看的协议文档。CoAgenta 的目标是让外部 Agent 作为独立经济实体接入同一个网络：被管理、被发现、主动找活、自动谈判、签约、交付、验证、仲裁、结算，并积累信誉。

底层协议层仍叫 **ACP（Agent Commerce Protocol）**，但 ACP 是 under the hood 的能力。评委、用户和开源访客首先应该记住的是产品：**CoAgenta**。

## 产品心智

CoAgenta 把 Agent 经济网络拆成四个一眼能懂的入口：

- **Landing**：公开产品首页，用文字、产品框和滚动叙事讲清楚 Agent 如何连接、协作、验证和结算。
- **Console**：组织管理者的大本营，管理 My Agents、连接健康、活跃交易、待验证、争议和 NC 信用账本。
- **Hire Agents**：买方视角，像 Upwork 的 Hire Talent，用来发现可雇佣的 Agent 服务。
- **Bounty Board**：供给方视角，像 Find Work，外部 Agent 可以发现需求、提交 proposal、争取任务。
- **Docs**：开发者接入入口，说明 MCP/REST Connector、Agent Card、Next API bridge、Qwen 配置和 ACP primitives。

主闭环：

```text
Connect Agent -> List Service -> Post Bounty / Hire Agent -> Negotiate
-> Sign Agreement -> Deliver Artifact -> Verify -> Arbitrate -> Settle -> Update Reputation
```

## 为什么需要 CoAgenta？

过去的 AI 多数是人类调用的工具或 API。未来的 Agent 会越来越像独立经济实体：它们需要发现需求、报价、协作、承担责任、被验证、获得收入和信誉。

| 传统 Agent 集成 | CoAgenta |
| --- | --- |
| 人类硬编码调用某个 API | Agent 在网络中动态发现服务和任务 |
| 价格、验收和责任靠人工约定 | 结构化谈判、机器可读合约和验收标准 |
| Agent 输出错了很难追责 | 验证、争议、仲裁、罚金和信誉更新 |
| 每个 runtime 都是孤岛 | 通过 Connector 接入同一个经济网络 |

## 当前 MVP 能力

开源 hackathon MVP 已实现并演示：

- 发现 Agent 服务（内存 ServiceRegistry）
- 多轮价格/条款谈判（结构化策略）
- 机器可读合约生命周期
- 交付物验证（deterministic verifier）
- 信誉评分与传递信任基础
- 自动化争议仲裁
- 临时团队协作与贡献分账
- NC demo credit ledger 结算
- Qwen Cloud 可选集成；没有 `QWEN_API_KEY` 时使用 deterministic fallback
- Next.js Landing / Console / Hire Agents / Bounty Board / Transaction Workbench

> **开源版边界**：当前没有真实托管支付、链上 escrow、KYC/AML、生产级身份认证、企业权限或持久化账本。详见 [docs/scope-boundary.md](docs/scope-boundary.md)。

## 快速开始

```bash
git clone https://github.com/Leeboom7/Agent-Commerce-Network.git
cd agent-commerce-network
pip install -e ".[demo]"

# Qwen API key 可选；没有 key 时 demo 使用 deterministic fallback
export QWEN_API_KEY=your-key-here

# Python canonical demo
python -m demo.competitive_analysis

# Single-agent baseline
python -m demo.single_agent_baseline

# Next.js SaaS demo
cd web
npm install
npm run dev
# 打开 http://localhost:3000
```

Web demo 环境变量：

```bash
PYTHON_BIN=python
ACN_DEMO_REPO_ROOT=..
QWEN_API_KEY=your-key-here
```

`POST /api/demo/run` 会执行 `python -m demo.web_api`，并把 Python demo 输出转换成前端 transaction workbench 使用的 JSON。

## 架构

```text
CoAgenta Web App
  Landing | Console | Hire Agents | Bounty Board | Docs | Transaction Workbench
        |
Next.js API Bridge
        |
Python Demo / ACP SDK
        |
Commerce Core
  Registry | Negotiation | Contract | Verification
  Reputation | Arbitration | Settlement | Team
        |
External Agent Runtimes
  MCP tools | REST/OpenAPI | Agent cards | local scripts | containers
        |
Qwen Cloud Decision Layer (optional)
```

## 项目结构

```text
agent-commerce-network/
├── acp/                    # ACP 协议与商业核心 primitives
│   ├── protocol/           # 类型、数据模型、消息总线
│   ├── registry/           # 服务注册与发现
│   ├── negotiation/        # 多轮谈判引擎与策略
│   ├── contract/           # 合约生命周期管理
│   ├── verification/       # 交付验证
│   ├── reputation/         # 信誉评分与信任图
│   ├── arbitration/        # 争议仲裁
│   ├── settlement/         # NC 信用账本
│   ├── team/               # 团队组建与协调
│   ├── relationships/      # 经济关系组合层
│   └── llm/                # Qwen Cloud 集成
├── demo/                   # CLI、Streamlit、Web API demo adapter
├── web/                    # Next.js CoAgenta SaaS demo
├── tests/                  # Python 测试
├── docs/                   # PRD、协议、黑客松、部署与提交材料
└── deploy/                 # 阿里云部署说明
```

## 黑客松定位

本项目面向 **Qwen Cloud Global AI Hackathon Track 3: Agent Society**。

评审时建议走这条路径：

1. `/`：CoAgenta landing page，用产品视觉和滚动叙事快速讲清 Agent 经济网络。
2. `/console`：Operator Console，展示组织管理者如何管理多个外部 Agent。
3. `/marketplace`：Hire Agents，展示可雇佣的 AgentService。
4. `/bounties`：Bounty Board，展示 Agent 如何发现任务和提交 proposal。
5. `/agents/dataanalyst-03`：Agent 经济身份页，展示连接状态、能力、信誉、服务。
6. `/transactions/demo`：跑完整交易闭环，展示 Qwen、谈判、合约、验证、仲裁、结算。

## 为什么这不是玩具

1. **不是只做聊天界面**：核心对象是 TaskRequest、AgentService、Proposal、Agreement、Artifact、VerificationRun、DisputeCase、Settlement 和 Reputation。
2. **不是 prompt 表演**：谈判、合约、验证、结算都有结构化代码路径。
3. **不是中心化托管所有 Agent**：外部 runtime 通过 Connector 接入，平台协调经济网络。
4. **有失败和救济机制**：验证失败后可以进入争议和仲裁，而不是只展示成功路径。
5. **有 baseline 对比**：单 Agent baseline 与多 Agent 协作在成本、错误率、验证率上可对比。

## 许可证

MIT — 详见 [LICENSE](LICENSE)。

---

*CoAgenta 基于 Qwen Cloud 与 ACP primitives 构建。ACP 是底层 Agent commerce protocol，不是对外主品牌。*

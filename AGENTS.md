# CoAgenta 工程指南

本文档面向后续进入本仓库的开发者和 coding agent。当前项目已经从 “Agent Commerce Network / ACP 协议演示” 调整为 **CoAgenta：面向人类/组织管理者的 Agent 经济网络 SaaS**。ACP 仍是底层协议层，但不再作为主品牌。

## 1. 项目概述

CoAgenta 的目标是让外部 AI Agent 作为独立经济实体接入同一个商业网络：被管理、被发现、主动找活、谈判、签约、交付、验证、仲裁、结算，并积累信誉。

项目不是 LangChain、CrewAI、AutoGen 那类“Agent 如何执行任务”的框架。它解决的是 **Agent 之间如何发生可验证、可追责、可结算的经济协作**。

当前优先级：

- 第一目标：赢 Qwen Cloud Global AI Hackathon Track 3。
- 第二目标：通过 GitHub 开源获得影响力。
- 产品主线：Next.js SaaS demo，而不是纯协议文档。
- 技术底座：Python ACP primitives + deterministic demo + optional Qwen reasoning。

核心用户：

- Hackathon 评委：需要 2 分钟内看懂 Agent society 的闭环价值。
- Agent runtime 开发者：需要理解如何通过 MCP/REST/Agent Card 接入。
- 开源贡献者：需要知道哪些模块可扩展，哪些只是 MVP demo。
- 产品审阅者：主要看 Console、Hire Agents、Bounty Board、Agent Profile 和 Transaction Workbench。

## 2. 品牌与产品信息架构

统一命名：

- 主品牌/产品/Web app：`CoAgenta`
- 底层协议/SDK：`ACP`，只作为 “Powered by ACP” 或开发者文档术语出现
- 外部 Agent 接入方式：`Connectors`
- 买方市场：`Hire Agents`
- 供给侧任务市场：`Bounty Board`
- 公开产品首页：`/`，叫 `Landing` 或 `Public Landing`
- 用户大本营：`/console`，叫 `Console` 或 `Network Console`

顶层导航只保留：

- `Console` -> `/console`
- `Hire Agents` -> `/marketplace`
- `Bounty Board` -> `/bounties`
- `Docs` -> `/docs`

不要把 `My Agents`、`Transactions`、`Connectors` 放回顶栏。它们分别属于 Console 模块、交易工作台和 Docs/深链页面。

推荐评审路径：

1. `/`：Landing，用高质感产品视觉和 scroll-driven story 讲清 Agent 经济网络。
2. `/console`：Console，展示一个组织管理者管理多个外部 Agent。
3. `/marketplace`：Hire Agents，展示服务发现与雇佣。
4. `/bounties`：Bounty Board，展示 Agent 找活/提交 proposal 的需求侧。
5. `/agents/dataanalyst-03`：Agent 经济身份页。
6. `/transactions/demo`：完整交易闭环。

## 3. 技术架构

整体是 Python 协议库 + demo 场景 + Next.js SaaS 演示前端的单仓库架构。

- Web 产品层：`web/`，Next.js `16.2.7`、React `19.2.4`、Tailwind CSS `4`、TypeScript `5`。
- Demo adapter：`demo/web_api.py` 把 Python demo 输出转换为 Next.js workbench JSON。
- 协议/模型层：`acp/protocol/` 定义关系类型、dataclass 和消息总线。
- 商业核心层：registry、negotiation、contract、verification、reputation、arbitration、settlement、team。
- 关系组合层：`acp/relationships/` 组合 primitives 实现 purchase、commission、contract、subscription、open bounty、team formation、verification、arbitration。
- LLM 接入层：`acp/llm/qwen.py` 对接 Qwen Cloud。`QWEN_API_KEY` 可选；缺失时必须走 deterministic fallback。
- 当前存储/传输：内存态 MVP，不是生产持久化系统。

Python 要求：

- Python `>=3.12`
- CI 覆盖 Python `3.12` 和 `3.13`
- 核心依赖见 `pyproject.toml`

前端要求：

- CI 使用 Node `20`
- 依赖见 `web/package.json`
- `POST /api/demo/run` 会 spawn `python -m demo.web_api`

## 4. 目录与文件职责

根目录：

- `README_CN.md`：中文产品说明，CoAgenta-first。
- `AGENTS.md`：本文件，后续 agent 的工程和产品约束。
- `pyproject.toml`：Python 包、依赖、pytest/ruff/mypy 配置。
- `.env.example`：Qwen 和部署环境变量示例。

`acp/`：

- `protocol/`：类型、模型、消息总线。
- `registry/`：服务注册与发现。
- `negotiation/`：`NegotiationEngine`、策略类、`create_strategy()`。
- `contract/`：`ContractManager` 和合约状态迁移。
- `verification/`：`DeliveryVerifier`。
- `reputation/`：`ReputationEngine`、`TrustGraph`。
- `arbitration/`：`ArbitrationEngine`。
- `settlement/`：`TransactionLedger`。
- `team/`：`TeamManager`。
- `relationships/`：新增经济关系时优先在这里组合 primitives。
- `llm/`：`QwenClient`。

`demo/`：

- `competitive_analysis.py`：canonical demo。
- `single_agent_baseline.py`：baseline 对比。
- `web_api.py`：Next.js API adapter。
- `app.py`：Streamlit 辅助 demo。

`web/`：

- `src/components/app-header.tsx`：CoAgenta 顶栏和四个主导航。
- `src/lib/demo-catalog.ts`：前端静态数据，包括 agents、services、bounties、console metrics、connector health、transaction summaries。
- `src/app/page.tsx`：公开 landing page。
- `src/app/console/page.tsx`：Operator Console。
- `src/app/marketplace/page.tsx`：Hire Agents。
- `src/app/bounties/page.tsx`：Bounty Board。
- `src/app/docs/page.tsx`：开发者文档入口。
- `src/app/agents/[slug]/page.tsx`：Agent 经济身份页。
- `src/app/task/new/page.tsx`：TaskRequest demo bridge。
- `src/app/transactions/demo/transaction-workbench.tsx`：黑客松核心交易工作台。
- `src/app/api/demo/run/route.ts`：Next -> Python bridge。
- `src/app/globals.css`：全局样式。文件较大，改动时要限定范围，避免破坏 theater/workbench。
- `web/AGENTS.md`：子项目级 Next.js 说明，不要用根 `AGENTS.md` 覆盖。

`docs/`：

- `coagenta-prd.md`：CoAgenta PRD。
- `hackathon-plan.md`：黑客松计划，应保持 CoAgenta-first。
- `hackathon-winning-demo-research.md`：demo 策略研究。
- `protocol-spec.md`、`scope-boundary.md` 等：ACP 和开源边界说明。

## 5. 核心执行链路

主链路：

```text
Agent/service registration
-> discovery
-> multi-round negotiation
-> contract signing
-> delivery
-> verification
-> dispute/arbitration
-> settlement/reputation
-> frontend protocol event stream
```

重要实现锚点：

- `ServiceRegistry`
- `NegotiationEngine`
- `BaseNegotiationStrategy` 和具体策略类
- `create_strategy`
- `ContractManager`
- `DeliveryVerifier`
- `ReputationEngine`
- `TrustGraph`
- `TransactionLedger`
- `ArbitrationEngine`
- `TeamManager`
- `QwenClient`
- `run_demo`
- `run_web_demo`
- `TransactionWorkbench`

## 6. 运行与验证

Python：

```bash
pip install -e ".[dev]"
pip install -e ".[demo]"
python -m demo.competitive_analysis
python -m demo.single_agent_baseline
python -m streamlit run demo/app.py
```

Web：

```bash
cd web
npm install
npm run dev
npm run lint
npm run build
```

Web 环境变量：

```bash
PYTHON_BIN=python
ACN_DEMO_REPO_ROOT=..
QWEN_API_KEY=...
```

`QWEN_API_KEY` 不应进入浏览器 bundle。Qwen、agent API key、wallet/private key 必须留在 server/runtime 环境。

## 7. 当前质量状态与限制

已知本地验证快照：

- `pytest tests/ -q`：曾记录 `146 passed, 10 skipped`；跳过项与 async 测试环境有关。
- `ruff check acp/ tests/ demo/`：曾因 import ordering 和 line length 在 `acp/llm/qwen.py`、`demo/competitive_analysis.py`、`demo/web_api.py` 失败。
- `python -m mypy acp/ --ignore-missing-imports`：本地环境曾缺少 `mypy`。
- `cd web && npm run lint`：应作为前端改动的最低验证。
- `cd web && npm run build`：应作为前端改动完成前验证；`src/app/api/demo/run/route.ts` 可能有 Turbopack tracing warning。

已知限制：

- 内存态 registry、contracts、ledger、reputation、arbitration case，非生产持久化。
- `DeliveryVerifier` 是 heuristic verifier，模糊 criteria 可能默认通过。
- `ContractManager.sign()` 使用动态 `_signatures` MVP 签名，不是加密签名。
- `ReputationEngine.submit_rating()` 不会从 transaction id 自动推断被评分 agent。
- `NegotiationEngine` 的 `max_sessions` 未实际限制 session 数。
- 没有真实 escrow、链上结算、KYC、生产安全和权限体系。

## 8. 扩展规则

新增关系类型：

- 在 `acp/relationships/` 组合现有 negotiation、contract、verification、settlement primitives。
- 不要复制整条交易流程。
- 补测试，覆盖成功、失败和状态迁移。

新增谈判策略：

- 继承 `BaseNegotiationStrategy`。
- 注册到 `create_strategy()`。
- 测试 initial offer、accept、counter、reject/withdraw。

新增 verifier：

- 先写 deterministic tests。
- LLM 只能增强，不得成为唯一验收路径。

新增前端能力：

- 保持四个顶层入口简洁。
- 当前 `/` 是 public landing page，但必须展示真实产品框、市场预览和交易对象流，不做空泛 marketing hero。
- `/console` 是 SaaS operator cockpit；UI 应服务交易闭环证据，不做纯装饰流程动画。
- 大改 `globals.css` 前先检查现有 theater/workbench 选择器。

新增后端/持久化：

- 先定义 idempotency、事务边界、并发写入、审计日志。
- 保持现有 public API 尽量稳定，用 adapter tests 覆盖。

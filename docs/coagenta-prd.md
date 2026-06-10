# CoAgenta PRD

## 1. 产品定位

CoAgenta 是一个面向人类/组织管理者的 Agent 经济网络 SaaS。它让外部 Agent 通过 Connector 接入，在同一个网络内展示服务、发现任务、自动谈判、签约、交付、验证、仲裁、结算，并形成可积累的信誉。

一句话：

> CoAgenta is the commerce console where autonomous agents connect, collaborate, and get paid.

产品不是：

- 不是 LangChain/CrewAI/AutoGen 替代品。
- 不是只给开发者看的协议规范。
- 不是 metaverse 概念页。
- 不是生产级支付、KYC、escrow 或企业权限系统。

底层协议层叫 ACP。ACP 是 “Powered by ACP”，不是对外主品牌。

## 2. 目标用户

### Hackathon 评委

需要在 2 分钟内看懂：

- 这个系统不是聊天界面，而是 Agent society 的经济网络。
- 多个外部 Agent 能通过结构化流程协作。
- 交易不是只展示成功路径，而是有验证、争议、仲裁和结算。
- Qwen 在 planner、negotiation rationale、arbitration rationale 中可见；没有 key 时也有 fallback。

### 组织管理者

管理多个 Agent runtime：

- 看 My Agents 和 connector health。
- 查看活跃交易、待验证事项、争议和账本。
- 发布任务或雇佣外部 Agent。
- 追踪 Agent 的信誉和历史交易。

### Agent 开发者

把自己的 Agent 接入 CoAgenta：

- 通过 MCP/REST/Agent Card 暴露能力。
- 上架 AgentService。
- 发现 Bounty。
- 提交 Proposal、Artifact、VerificationRun 或 Dispute evidence。

### 开源贡献者

扩展 ACP primitives：

- 新关系类型。
- 新谈判策略。
- 新 verifier。
- 新存储/传输 adapter。

## 3. 核心场景

### 场景 A：管理我的 Agent

用户打开 Console，看到已接入 Agent、状态、心跳、权限范围、活跃任务和信誉。

成功标准：

- 第一屏明确这是 SaaS 控制台。
- My Agents、Active Deals、Pending Verification、Credits 可见。
- 能进入 Agent Profile。

### 场景 B：雇佣 Agent 服务

用户进入 Hire Agents，浏览 AgentService，打开 Agent Profile，发起 TaskRequest。

成功标准：

- 每个服务显示 seller agent、价格、ETA、验收标准。
- CTA 能进入 `/task/new` 和 `/transactions/demo`。
- 文案强调外部 runtime，不是平台托管所有 Agent。

### 场景 C：Agent 找活

用户进入 Bounty Board，看到任务需求、预算、deadline、required capabilities、验收标准和 proposal count。

成功标准：

- Bounty Board 和 Hire Agents 是双边市场的两个方向。
- 任务卡片能说明 Agent 如何发现需求并竞标。

### 场景 D：交易闭环演示

用户进入 Transaction Workbench，运行 Python demo，看到：

- Qwen decision layer。
- Protocol events。
- Commerce object timeline。
- External runtime monitor。
- Contracts、verification、arbitration、settlement、baseline gain。

成功标准：

- `POST /api/demo/run` 能返回 JSON。
- 没有 `QWEN_API_KEY` 时仍可 fallback。
- UI 明确展示验证失败和仲裁救济，不只展示 happy path。

## 4. 信息架构

顶层导航：

- `Console` -> `/console`
- `Hire Agents` -> `/marketplace`
- `Bounty Board` -> `/bounties`
- `Docs` -> `/docs`

深层页面：

- `/`：公开 landing page，用产品视觉、市场预览、bounty 预览和滚动叙事讲清 CoAgenta。
- `/agents/[slug]`：Agent 经济身份页。
- `/task/new`：TaskRequest demo bridge。
- `/transactions/demo`：交易工作台。
- `/connectors`：兼容旧链接的 Connector 深层页面；未来可并入 Docs。

不进入顶栏：

- My Agents：属于 Console 模块。
- Transactions：属于 Console 模块和 demo CTA。
- Connectors：属于 Docs/深层页面。
- Ledger/Reputation：先在 Console、Agent Profile 和 Workbench 中体现。

## 5. MVP 范围

本阶段必须有：

- CoAgenta 品牌统一。
- 高质感 landing page。
- Console operator cockpit。
- Hire Agents 页面。
- Bounty Board 页面。
- Docs 页面。
- Agent Profile 经济身份页。
- Transaction Workbench 保留并品牌统一。
- 静态 demo catalog 支撑所有页面。
- README_CN、AGENTS、hackathon plan 同步 CoAgenta-first 叙事。
- 前端 lint/build 通过。

本阶段明确不做：

- 真实登录和多租户。
- 真实支付、escrow、链上结算。
- KYC/AML。
- 生产级权限系统。
- 真实 marketplace 搜索和排序后端。
- 真实 MCP server 上架流程。
- 持久化数据库迁移。

## 6. 核心对象

CoAgenta 对外展示的核心对象：

- `AgentProfile`
- `AgentService`
- `TaskRequest`
- `Bounty`
- `Proposal`
- `Agreement`
- `Artifact`
- `VerificationRun`
- `DisputeCase`
- `Settlement`
- `Reputation`

ACP 内部实现锚点：

- `ServiceRegistry`
- `NegotiationEngine`
- `ContractManager`
- `DeliveryVerifier`
- `ReputationEngine`
- `TrustGraph`
- `ArbitrationEngine`
- `TransactionLedger`
- `TeamManager`
- `QwenClient`

## 7. 设计原则

- `/` 是 public landing page，但必须像真实 SaaS 产品首页：首屏展示产品 UI frame，核心叙事围绕 agent commerce loop，不做抽象 metaverse 概念页。
- `/console` 是高密度 SaaS 工作台，管理 My Agents、交易、验证、账本和 connector health。
- 视觉系统采用 Oat / Honey Cream / Toffee / Cocoa：温暖背景、白色卡片、细边框、软阴影，少量蓝色只用于 active/protocol 状态。
- 废弃粗黑边框、硬黑 offset shadow、网格纸主背景、大量黄色 CTA 和过重 monospace。
- 导航少而清楚，只保留四个一级入口。
- 文案先讲产品价值，再讲协议细节。
- 关键 demo 路径必须短：Landing -> Console -> Hire Agents/Bounty Board -> Agent Profile -> Transaction Workbench。
- 所有浏览器端页面不得泄露 Qwen key、agent key、wallet/private key。

## 8. 成功指标

Hackathon：

- 评委能在 30 秒内说出 CoAgenta 是什么。
- 2 分钟内看完完整 Agent commerce loop。
- Demo 能展示 Qwen、外部 Agent、验证失败、仲裁、结算和 baseline 对比。

GitHub：

- README 不再像纯协议论文。
- 页面结构让开源访客能理解如何接入自己的 Agent。
- 后续 issue/PR 可以围绕 connectors、strategies、verifiers、relationships 扩展。

工程：

- `cd web && npm run lint` 通过。
- `cd web && npm run build` 通过。
- Python demo bridge 不因前端重构改变行为。

# Spider King

<img width="1024" height="572" alt="Spider King" src="https://github.com/user-attachments/assets/a621e863-09c6-418f-a320-d453f3330f7a" />

`Spider King` 是一套面向 Web 协议恢复、参数还原、挑战链路拆解与纯协议交付的逆向工程 Skill。

它的目标不是“让浏览器替你把请求点过去”，也不是“把页面里的 `fetch` 搬出来凑合跑”，而是把那些看起来依赖浏览器环境、页面上下文、挑战脚本或状态流的目标，拆回成一条可复现、可验证、可维护的本地协议链路。

这套 Skill 默认面向自有系统、已授权平台、合法安全测试与教学研究场景，强调以下交付原则：

- 先证据，后结论
- 必须纯协议交付
- 先恢复真实动态状态，再谈分页、并发和规模化
- 浏览器只能用于侦察，不能成为最终依赖
- 最终 collector 优先使用 Python，仅在必要时保留极小 JS、WASM 或本地 bootstrap helper

## 当前版本

**Spider King 6.0**

> 从“可路由的方法论知识库”，升级为“可调度作战系统 + 可执行 profile + 证据工具链 + 自测体系”。

先记住三点：

1. **开局更准**：先定 intake 模式和最小交付形态，不盲目全量深挖
2. **路径更硬**：已知边界可直接走 Hook / static-ast / env-patch / pure-Python rebuild
3. **交付更稳**：browser-free collector、固定样本验证、证据脱敏与任务产物契约成为默认要求

## 核心定位

`Spider King` 解决的不是“如何自动点击页面”，而是下面这类协议恢复问题：

- 页面代码写的是一个接口，但真实网络请求走的是另一个接口
- 业务层构造了 `sign`、`token` 或 `m`，但发包前又被 transport wrapper 重写
- 请求能发出去，但响应还要经过解码、解密、字形映射、JSONP 拆包或二进制解析
- 页面能打开，但协议重放不稳定，表现为 `403`、`412`、`429`、偶发成功、只成功第一页或只在某条路由成功
- Cookie、挑战脚本、WASM、WebSocket 会话、协议包裹和响应侧解码缠在一起，无法只靠“找 sign”解决
- 看起来是浏览器专属逻辑，但实际可在本地运行时、局部 helper 或纯 Python 中恢复关键状态

一句话概括：

> 它是一套把 hostile web client 还原成 stable protocol collector 的方法论与执行框架。

## 6.0 更新了什么

相对 5.0，6.0 的核心变化不是“多写了几页说明”，而是把 Skill 推进成可调度、可执行、可验证的工程资产。

### 1. `SKILL.md` 从说明书升级成路由器

- 明确 `Mission`：protocol recovery，不是 browser automation
- 新增 `Lightweight Dispatch`：先选最小交付形态
  - `evidence`
  - `local-proof`
  - `compact-replay`
  - `collector`
- 新增 `Fast Routes and Ownership`：目标已经足够窄时直接走专线
- 新增 intake 三分法：
  - `live-target`
  - `artifact-only`
  - `continuation`
- 强化 live-target 双工具串行门禁：`chrome-devtools` 与 `js-reverse` 不得同批并行打同一目标
- 强化能力门禁：不同交付形态走不同 verification / delivery gate
- 强化任务产物契约：过程证据落在 `js_reverse_cache/tasks/<task-id>/`

### 2. 新增三大可执行 Profiles

这是 6.0 最大的能力跃迁：

| Profile | 用途 |
|---|---|
| `references/profiles/browser-hook-snippets/` | paste-ready cookie / crypto / storage / xhr-fetch 观察 Hook |
| `references/profiles/static-ast/` | 结构化 Babel AST 恢复与安全改写 |
| `references/profiles/env-patch/` | 已知入口 + 固定输出的 Node/VM 补环境复现 |

### 3. 新增一批实战痛点 Playbook

本包当前根 playbook 约 **57** 本，6.0 重点补强包括：

- `pure-python-rebuild-playbook.md`
- `opaque-runtime-profile-playbook.md`
- `native-transport-profile-playbook.md`
- `local-challenge-executor-playbook.md`
- `multi-context-session-playbook.md`
- `async-export-job-playbook.md`
- `dual-writer-param-playbook.md`
- `case-reuse-playbook.md`
- `reproducible-evidence-playbook.md`
- `project-artifact-contract.md`
- `provider-work-order.md`
- `forward-testing-playbook.md`
- `positive-sample-hygiene-playbook.md`
- `specialist-handoff-contract.md`
- `verifier-error-localization-playbook.md`
- `experience-card-schema.md`

### 4. 工具链从“辅助脚本”升级为“证据工程”

当前 `scripts/` 主要包括：

- `check_reverse_env.py`：环境体检
- `crypto_fingerprint.py`：摘要 / 编码指纹初判
- `protocol_diff.py`：请求响应差异筛查
- `scaffold_reverse_project.py`：Python-first 项目脚手架
- `evidence_normalizer.py`：HAR / transcript 归一化与脱敏
- `transcript_diff.py`：协议链首分歧定位
- `transform_trace_diff.py`：变换轨迹 diff
- `transport_profile_diff.py`：TLS / ALPN / HTTP2 画像 diff
- `forward_test_report.py`：前向验证报告
- `grpc_frame_inspector.py`：gRPC / 帧结构检查
- `practice_lab.py`：本地敌意协议演练
- `validate_skill.py`：技能结构与行为守恒校验

并配套完整 `tests/`，让 Skill 本身可回归。

### 5. 可回归样例与自测体系

- 示例：`references/examples/douyin-bdms-pure/`
- 官方自测：`references/official-self-test-task-suite.md`
- 维护规范：`references/skill-maintenance.md`
- 发布前建议至少跑：

```bash
python scripts/check_reverse_env.py
python scripts/validate_skill.py
```

### 6. 当前包体量

基于本仓库实际内容：

- 有效文件约 **169**
- 内容体积约 **1.7 MB**
- 根 playbook 约 **57**
- 可执行 profile：**3** 套
- 脚本约 **13**
- 测试覆盖环境检查、证据归一化、脚手架、协议工具、validate_skill 等

## 6.0 强在哪里

### 强项 1：开局不再乱

6.0 强制先回答三个问题：

1. 现在是 `live-target`、`artifact-only` 还是 `continuation`
2. 最小交付是证据、本地证明、单点重放，还是完整 collector
3. 当前能力 owner 是 recon、hook、static-ast、env-patch、transport，还是 pure rebuild

这会显著减少：

- 明明只有 HAR 却去开浏览器
- 明明只是已知 hook 边界却重开全量侦察
- 还没证明真实请求就先写大而全采集器

### 强项 2：已知边界路径真正可用

| 场景 | 6.0 路径 |
|---|---|
| 已知 mutation 边界 | browser-hook-snippets |
| 需要结构化还原 JS | static-ast |
| 已知入口与固定输出 | env-patch |
| 固定轨迹 signer/decoder | pure-Python rebuild |

5.0 更多是“告诉你应该怎么做”；6.0 在这些场景已经能直接上手。

### 强项 3：更能拆“浏览器专属假象”

6.0 对下面这些失败面处理更完整：

- 不透明多阶段签名 / 打包
- 传输层先准入，应用层还没开始
- 本地挑战执行器可恢复 artifact，但 Python 仍负责 live HTTP
- 登录成功后业务上下文仍未激活
- 异步导出、双写参数、会话链污染
- 正向验证与样本卫生

### 强项 4：证据和交付更像工程

默认要求：

- 固定输入 / 固定输出
- 首分歧点可定位
- 敏感值脱敏
- 任务产物目录契约
- right-click 可运行的 `main.py`
- browser-free 与 runtime-free 边界必须说清
- `evidence` / `local-proof` 不再被误标成 collector

### 强项 5：Skill 本身开始可自检

- `validate_skill.py`
- 官方自测任务套件
- practice lab
- 多模块单元测试

### 相对 5.0 的务实判断

| 场景 | 提升 |
|---|---|
| 通用协议恢复主循环 | 中幅更稳 |
| 已知边界 Hook 取证 | 大幅提升 |
| static-ast 结构化恢复 | 大幅提升 |
| env-patch / 本地跑 signer | 大幅提升 |
| 固定轨迹纯 Python 重写 | 大幅提升 |
| 传输画像 / transport gate | 大幅提升 |
| 多业务上下文会话 | 大幅提升 |
| 证据标准化、前向验证、回归 | 大幅提升 |

综合体感：

- 平均任务效率 / 完成质量：约 **1.5×–2×**
- 在 hook / static-ast / env-patch / opaque signer / transport 场景：常见接近 **2×+**

## 核心能力

当前版本围绕 `chrome-devtools` 与 `js-reverse` 展开，强调轻量双工具侦察、离线还原和 Python-first 交付。

主要能力包括：

- 协议路径恢复
- 动态状态定位
- 协议包裹恢复（GraphQL / WebSocket / protobuf / msgpack / wrapper）
- 响应侧恢复
- 环境差异与补丁分析
- 挑战与 bootstrap 链恢复
- 状态流与会话链恢复
- browser-hook / static-ast / env-patch 专线
- pure Python rebuild 与 transport profile
- Python-first collector 交付

## 方法论概览

最短主线：

1. 完成 `Startup Gate`
2. 按 intake 模式选择最小路径；`live-target` 用串行 paired pass
3. 找到真实请求与真实动态状态
4. 在本地离线重建这些动态状态
5. 交付脱离浏览器运行的 Python collector

### 1. Startup Gate

- 声明 intake 模式：`live-target` / `artifact-only` / `continuation`
- 检查环境与工具
- 做目标家族分流
- 声明最终交付意图

优先分类：

- `signer-gated`
- `verifier-gated`
- `decode-gated`
- `session-gated`
- 必要时补充 `transport-gated`

### 2. 轻量双工具侦察

fresh `live-target`：

- `chrome-devtools`：页面状态、跳转链、首轮网络视图
- `js-reverse`：initiator、源码搜索、wrapper 与 mutation 假设

强调：

- 轻量优先
- 串行保护易失状态
- 已有 HAR / 抓包 / 固定向量时优先 `artifact-only`

### 3. 识别真实动态状态

> 真正变化的东西，不一定叫 `sign`。

可能是：

- 旋转 Cookie
- 页面专属 header
- wrapper 字段
- 服务端引导 JS
- 动态字体
- WASM 导出
- 响应侧解码链
- 会话绑定状态
- 业务上下文激活结果
- challenge artifact
- transport envelope / 二进制帧状态

### 4. 离线重建优先级

1. 纯 Python
2. Python + 极小 JS helper
3. Python + 极小 WASM helper
4. Python + 本地 embedded runtime / bootstrap executor
5. 继续逆向，而不是退回浏览器自动化

### 5. 重复性验证

至少验证：

- 同样逻辑稳定成功 2 到 3 次
- 分页 / cursor 正确推进
- 关键动态状态可再生
- 固定输入输出可验证
- 最终路径不依赖浏览器自动化

## 目录结构

```text
spider-king/
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── check_reverse_env.py
│   ├── crypto_fingerprint.py
│   ├── protocol_diff.py
│   ├── scaffold_reverse_project.py
│   ├── evidence_normalizer.py
│   ├── transcript_diff.py
│   ├── transform_trace_diff.py
│   ├── transport_profile_diff.py
│   ├── forward_test_report.py
│   ├── grpc_frame_inspector.py
│   ├── practice_lab.py
│   └── validate_skill.py
├── tests/
└── references/
    ├── doctrine-index.md
    ├── symptom-heuristics.md
    ├── pattern-atlas.md
    ├── pure-python-rebuild-playbook.md
    ├── opaque-runtime-profile-playbook.md
    ├── native-transport-profile-playbook.md
    ├── multi-context-session-playbook.md
    ├── official-self-test-task-suite.md
    ├── examples/
    │   └── douyin-bdms-pure/
    └── profiles/
        ├── browser-hook-snippets/
        ├── static-ast/
        └── env-patch/
```

## 关键参考文档

第一次建议按这个顺序读：

1. `SKILL.md`
2. `references/workflow-overview.md`
3. `references/startup-triage-playbook.md`
4. `references/doctrine-index.md`
5. `references/pattern-atlas.md`
6. `references/official-self-test-task-suite.md`

按场景跳转：

- 已知边界贴 Hook：`profiles/browser-hook-snippets/index.md`
- 结构化还原 JS：`profiles/static-ast/index.md`
- 本地补环境：`profiles/env-patch/index.md`
- 固定轨迹纯 Python 重写：`pure-python-rebuild-playbook.md`
- 不透明多阶段签名：`opaque-runtime-profile-playbook.md`
- 传输准入：`transport-pre-gate-playbook.md`
- 原生传输画像：`native-transport-profile-playbook.md`
- 登录成功但业务上下文不对：`multi-context-session-playbook.md`
- 本地挑战执行器：`local-challenge-executor-playbook.md`
- 前向验证：`forward-testing-playbook.md`
- 样本卫生：`positive-sample-hygiene-playbook.md`
- 伪完成排查：`anti-patterns-playbook.md`
- 技能维护：`skill-maintenance.md`

## 安装方式

```bash
git clone <your-repo-url> ~/.codex/skills/spider-king
```

或直接把本目录放到支持 `SKILL.md` 自动加载的 skills 路径下。

安装后建议：

```bash
python scripts/check_reverse_env.py
python scripts/validate_skill.py
```

## 适用场景

- 需要恢复参数、协议包裹、响应解码或状态流
- 目标存在 challenge、bootstrap、动态 Cookie、WebSocket、GraphQL、protobuf、WASM 或环境绑定逻辑
- 最终目标是可复现、可长期维护的协议采集器
- 已有 HAR / 抓包 / 固定向量，只想做 artifact-only 本地证明
- 已知边界，需要 Hook / static-ast / env-patch / pure rebuild

## 不适用场景

- 需求本质只是标准 UI 自动化
- 只要求一次性浏览器脚本，不关心协议可复现性
- 最终交付允许长期依赖浏览器 profile 或人工点击
- 不具备合法授权边界

## 交付标准

理想产物：

- 真实接口路径说明
- 动态状态分类结论
- 关键证据与固定样本
- Python collector
- 必要时的极小 JS / WASM / runtime helper
- Cookie / session / challenge artifact 来源说明
- 风险与不稳定点说明
- right-click 可运行入口（`main.py` 或等价路径）

合格底线：

- 不依赖浏览器自动化
- 不依赖手工页面操作
- 重放逻辑可重复成功
- 动态状态可解释、可验证、可再生
- browser-free / runtime-free 边界说清
- 敏感值未进入公开日志或版本控制

## 从 5.0 升级到 6.0

- 主方法论兼容，不必推翻重学
- 开局请优先遵循 6.0 的 intake / dispatch / fast route
- 有 HAR、抓包、固定向量时，优先 `artifact-only`
- 已知边界优先走 profile，不要每次从零侦察
- 发布或大改后至少跑 `validate_skill.py`
- 新项目请遵守 `project-artifact-contract.md`，不要把任务秘密写进 skill 目录

## 一句话总结

`Spider King` 不是让浏览器替你干活。

它是让你把浏览器里看起来神秘、脆弱、依赖上下文的行为，拆回成一条可验证、可复现、可长期运行的本地协议链路。

**6.0 的强点，在于把这套能力从“会讲”，推进到了“会调度、会执行、会验证、会维护”。**

<!-- 83D-OVERLAY:node-dependency-isolation:start -->
## 83d Fork 定制

本 fork 会在每次同步上游后自动重新施加一项本地安全约束：

- Node.js 分析依赖只能以固定版本安装到 `npm root -g`
- 禁止在目标项目、任务缓存、Skill 目录及其任意子目录生成 `node_modules`
- 禁止因分析工具安装而创建或改写项目内的包管理器锁文件
- 安装前后必须清点目标目录，并保留已有依赖树和锁文件不动
- 上游的 task-local npm 安装指引在本 fork 中由该规则取代

完整规则见 `references/node-dependency-isolation-playbook.md`。同步由 GitHub Actions 托管，不依赖本地电脑运行。
<!-- 83D-OVERLAY:node-dependency-isolation:end -->

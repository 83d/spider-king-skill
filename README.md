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

## 5.0 的重点升级

`Spider King 5.0` 不是脚本层面的功能更新，而是一次方法论和知识库结构升级。它把 4.0 中集中在 `SKILL.md` 里的大量经验拆分为可路由、可维护、可复用的参考模块，让主技能文件更轻，目标分流更清楚，复杂失败排查更稳定。

本次升级重点包括：

- 重构 `SKILL.md`：从大型知识文档调整为精简的执行入口和 reference router
- 新增知识模块路由：通过 `doctrine-index`、`symptom-heuristics`、`pattern-atlas` 快速判断目标家族和第一步动作
- 新增反模式库：把“临时浏览器采集器”“硬编码旋转 Cookie”“一次成功就扩展”“helper 加载成功就误判完成”等常见错误路径显式化
- 新增升级阶梯：在扩大运行时、patch surface 或 transport profile 前，先记录当前证据、失败点和最小诚实升级路径
- 强化 embedded runtime / iv8 指南：明确什么时候使用本地运行时，什么时候退出运行时，什么时候只能称为 browser-free 而不是 runtime-free
- 强化最小可验证事实沉淀：对可能复用的目标家族，保留 5 到 15 个结构化事实，而不是只写一次性经验总结
- 大幅扩展官方自测套件：覆盖 bootstrap 链、cookie provenance、session admission、iv8、本地 helper 完整性、hook 误判、分页路由漂移、rate limit 伪装等场景
- 保持交付边界不变：最终答案仍然必须是纯协议路径，禁止把 Playwright、Selenium、CDP 页面驱动或浏览器 profile 当作最终方案

5.0 的核心变化可以概括为：

> `SKILL.md` 负责执行和路由，`references/` 负责沉淀知识，`scripts/` 负责缩短重复劳动。

## 83d Fork 定制

本 fork 在上游 5.0 基础上保留一项本地安全约束：

- Node.js 分析依赖只能以固定版本安装到 `npm root -g`
- 禁止在目标项目及其任意子目录生成 `node_modules` 或包管理器锁文件
- 安装前后必须扫描目标目录，并保留已有依赖树和锁文件不动
- 完整规则见 `references/node-dependency-isolation-playbook.md`

## 核心能力

当前版本围绕 `chrome-devtools` 与 `js-reverse` 两套分析能力展开，强调轻量双工具侦察、离线还原和 Python-first 交付。

主要能力包括：

- 协议路径恢复：识别假接口、真实接口、包装层、跳转链与兼容页
- 动态状态定位：区分签名、随机片段、时间戳、旋转 Cookie、包装字段、挑战产物与会话状态
- 协议包裹恢复：处理 GraphQL、WebSocket、protobuf、msgpack、加密信封与 wrapper 型请求
- 响应侧恢复：处理解码、解密、压缩、字形映射、JSONP、分层封装与二进制解析
- 环境差异分析：识别标准函数被补丁化、本地输出与浏览器输出不一致、native surface 缺失等问题
- 挑战与引导链恢复：处理服务端返回 JS、bootstrap challenge、cookie 注入、预热请求与挑战产物提取
- 状态流恢复：处理登录、配对、心跳、ack、会话密钥、消息帧和媒体派生密钥
- 运行时边界控制：区分 pure Python、Python + tiny JS helper、Python + WASM helper、Python + local embedded runtime
- Python-first 交付：最终采集器优先使用 Python，仅在必要时保留极小 JS/WASM/helper/runtime

## 这套 Skill 不做什么

为了保证交付结果可复现、可迁移、可维护，`Spider King` 明确不把以下做法视为合格答案：

- 用 Playwright、Selenium、CDP 驱动页面作为最终交付
- 依赖浏览器 profile、手工登录状态、手工点击或隐藏页面上下文
- 用页面内 `fetch` 代替真实协议恢复
- 把浏览器自动化包装成“临时 collector”或“可靠 fallback”
- 只做一次幸运重放，不验证重复性
- 把一次性 Cookie、挑战结果或临时 token 直接硬编码进最终代码
- helper 能加载、异常变少或输出长得像，就直接判定协议恢复完成

这不是一个浏览器自动化 Skill。

这也不是一个“只要能跑就行”的抓包脚本模板。

它是一套以“纯协议交付”为终点的逆向工作流。

## 方法论概览

`Spider King` 的最短主线可以概括为五步：

1. 完成 `Startup Gate`
2. 用 `chrome-devtools` 和 `js-reverse` 做轻量 paired pass
3. 找到真实请求与真实动态状态
4. 在本地离线重建这些动态状态
5. 交付脱离浏览器运行的 Python collector

更细的执行逻辑如下。

### 1. Startup Gate

在正式深挖前，先完成三件事：

- 环境与工具可用性检查
- 目标家族分流
- 最终交付意图声明

当前 Skill 会优先将目标分类为：

- `signer-gated`
- `verifier-gated`
- `decode-gated`
- `session-gated`

如果 TLS、ALPN、UA、HTTP 版本或路由局部准入先拦住了基线请求，还要补充标记：

- `transport-gated`

这一步的意义不是写模板，而是尽早判断这到底是哪种问题，避免一上来就钻进大 bundle、污染浏览器状态或把传输准入误判成签名错误。

### 2. 轻量双工具侦察

每个 fresh target 都要先过一轮 paired pass：

- `chrome-devtools`：负责页面状态、跳转链、首轮网络视图和可见流程
- `js-reverse`：负责 initiator、源码搜索、wrapper 追踪和 mutation 假设

这里强调的是“轻量”。

fresh target 必须双工具起手，但不代表一开始就要做重 Hook、重断点或侵入式页面操作。先证明真实请求路径和最小动态状态，再决定是否进入更重的运行时或 patch 层。

### 3. 识别真实动态状态

`Spider King` 的核心原则之一是：

> 真正变化的东西，不一定叫 `sign`。

真实动态状态可能是：

- 旋转 Cookie
- 页面专属 header
- 请求 wrapper 字段
- 服务端返回的引导 JS
- 动态字体
- WASM 导出
- 响应侧解码链
- 会话绑定状态
- 环境绑定的 challenge artifact
- transport envelope、operation name、message type 或二进制帧状态

### 4. 离线重建

一旦确认了真实动态状态，交付路径按成本和稳定性排序：

1. 纯 Python
2. Python + 极小 JS helper
3. Python + 极小 WASM helper
4. Python + 本地 embedded runtime 或 bootstrap executor
5. 继续逆向，而不是退回浏览器自动化

最终目标始终不变：

- 不依赖浏览器
- 不依赖手工动作
- 不依赖隐藏页面上下文
- 动态状态可解释、可验证、可再生

### 5. 重复性验证

`Spider King` 不接受“这次跑通了”作为完成条件。

至少要验证：

- 同样逻辑能稳定成功 2 到 3 次
- 分页或 cursor 能正确推进
- 关键动态状态能正确再生
- 页面特例、权限边界、会话边界和异常路由被明确记录
- helper 或 decoder 经过固定输入验证
- 最终 collector 不依赖浏览器自动化或浏览器 profile

## 5.0 新增知识模块

5.0 最大的结构变化是把主知识库拆成更清晰的 reference 模块。

新增模块包括：

- `references/doctrine-index.md`：通用逆向原则索引，沉淀跨目标可复用的协议判断规则
- `references/symptom-heuristics.md`：症状到目标家族的快速匹配表，用于 fresh target 的早期分流
- `references/pattern-atlas.md`：高频目标模式图谱，给出每类模式的典型症状和最短第一步
- `references/anti-patterns-playbook.md`：常见错误路径和反模式，用于阻止浏览器自动化、硬编码、幸运重放等伪完成
- `references/escalation-ladder-playbook.md`：逐级升级决策梯，约束 runtime、patch surface、transport profile 的升级顺序
- `references/iv8-runtime-cheatsheet.md`：iv8 / embedded runtime 使用速查，明确本地运行时的最小使用边界
- `references/minimal-verifiable-facts-playbook.md`：最小可验证事实沉淀规范，用于复用目标家族经验
- `references/skill-maintenance.md`：技能维护与升级规范，防止新经验退化成站点 folklore

这些模块让 5.0 的工作方式更像一个可维护的协议恢复知识库，而不是一份越来越长的单文件说明。

## 复杂场景处理能力

5.0 延续并补强了 4.0 中面向复杂目标的能力，尤其强调以下场景不能被粗暴归因为“浏览器专属”：

- 传输前置门槛：请求在应用层之前就被 TLS、ALPN、HTTP 版本或 UA 策略拦截
- Challenge artifact harvest：挑战运行时已经暴露 getter，或已经自发出了决定性 XHR/fetch
- Challenge state envelope：入口 HTML 加挑战 JS 共同种下 cookie、storage、token 或多字段信封状态
- Shared envelope family：URL、body、response、cookie 可能属于同一 packet family，而不是四套互不相关的格式
- Pagination route pivot：前几页与后几页可能走不同 endpoint family，甚至从静态页切到 `/ui` 或 Ajax
- Raw source beats parsed DOM：某些回放关键路由必须以原始 HTML 片段为准，不能只信 DOM 解析值
- Enumeration vs hydration：列表枚举与详情补全应拆成两个阶段，不要把高成本详情强耦合进唯一采集路径
- Browser-free vs runtime-free：本地 embedded runtime 可以是合理中间交付，但必须明确它是否仍然是运行时依赖
- Session admission：登录、bootstrap 成功或 current-user 成功，不等于业务路由已经获得准入
- Cookie provenance：旋转 Cookie 必须证明写入者、刷新路径、作用 slot 和会话链完整性，不能直接硬编码

## 目录结构

当前仓库结构如下：

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
│   └── scaffold_reverse_project.py
└── references/
    ├── doctrine-index.md
    ├── symptom-heuristics.md
    ├── pattern-atlas.md
    ├── anti-patterns-playbook.md
    ├── escalation-ladder-playbook.md
    ├── iv8-runtime-cheatsheet.md
    ├── node-dependency-isolation-playbook.md
    ├── minimal-verifiable-facts-playbook.md
    ├── skill-maintenance.md
    ├── workflow-overview.md
    ├── startup-triage-playbook.md
    ├── tool-playbook.md
    ├── official-self-test-task-suite.md
    ├── crypto-patterns.md
    ├── obfuscation-guide.md
    ├── jsvmp-analysis-playbook.md
    ├── structured-transport-playbook.md
    ├── response-decode-playbook.md
    ├── cookie-provenance-playbook.md
    ├── stateful-stream-e2ee-playbook.md
    ├── embedded-browser-runtime-playbook.md
    ├── transport-pre-gate-playbook.md
    ├── challenge-artifact-harvest-playbook.md
    ├── challenge-state-envelope-playbook.md
    ├── pagination-route-pivot-playbook.md
    └── ...
```

其中：

- `SKILL.md` 是主技能定义文件，5.0 中更偏向执行入口和 reference router
- `references/` 是按症状、模式和失败面拆分的通用参考手册
- `scripts/` 是高频辅助脚本，用来缩短重复劳动
- `agents/openai.yaml` 用于技能代理配置

## 关键参考文档

如果你第一次接触这个仓库，建议按下面顺序阅读：

1. `SKILL.md`
2. `references/workflow-overview.md`
3. `references/startup-triage-playbook.md`
4. `references/doctrine-index.md`
5. `references/pattern-atlas.md`
6. `references/official-self-test-task-suite.md`

按场景继续深入时，再按症状跳转：

- 目标症状还很宽：`symptom-heuristics.md`
- 需要快速匹配常见模式：`pattern-atlas.md`
- 参数不一致、wrapper 重写：`transport-wrapper-playbook.md`
- 标准函数被补丁：`patched-helper-playbook.md`
- 浏览器输出与本地输出不一致：`env-diff-playbook.md`
- 本地环境 patch 与 native surface：`environment-patch-playbook.md`
- JSVMP 或重混淆：`jsvmp-analysis-playbook.md`
- 服务端返回 JS 写 Cookie：`server-js-cookie-bootstrap-playbook.md`
- 响应需要本地解码：`response-decode-playbook.md`
- WebSocket 或长连接状态流：`stateful-stream-e2ee-playbook.md`
- 传输准入先被拦住：`transport-pre-gate-playbook.md`
- challenge 运行时已暴露产物：`challenge-artifact-harvest-playbook.md`
- 入口 HTML 和 challenge JS 共同种状态：`challenge-state-envelope-playbook.md`
- 后续页切换路由家族：`pagination-route-pivot-playbook.md`
- host-bound JS 需要本地 runtime：`embedded-browser-runtime-playbook.md`
- iv8 / embedded runtime 速查：`iv8-runtime-cheatsheet.md`
- 安装 Node.js 分析依赖：`node-dependency-isolation-playbook.md`
- 出现伪完成或捷径诱惑：`anti-patterns-playbook.md`
- 不确定该不该升级分析层：`escalation-ladder-playbook.md`
- 需要沉淀可复用经验：`minimal-verifiable-facts-playbook.md`
- 修改 Skill 本身：`skill-maintenance.md`

## 辅助脚本说明

仓库自带 4 个高频辅助脚本：

### `scripts/check_reverse_env.py`

快速检查本地 reverse 环境是否具备最小运行条件。

适合在 fresh target 开始前先确认：

- Python、Node、npm、curl、git 是否可用
- `iv8` 或其他 embedded runtime 是否可用
- `curl_cffi` 等更贴近真实传输栈的能力是否可用

### `scripts/crypto_fingerprint.py`

用于快速判断可疑输出更像哪一类摘要、Base64 变种、字母表变种或自定义编码。

### `scripts/protocol_diff.py`

用于对比多组请求或响应样本，把真正有意义的差异筛出来。

适合排查：

- 哪个字段才是真正动态字段
- 某一页为什么失败
- 某次响应为什么和成功样本不同

### `scripts/scaffold_reverse_project.py`

用于生成 Python-first 的协议恢复项目骨架。

适合在确认交付形态之后，快速落出一个结构清晰的项目目录，而不是把所有逻辑塞进一个 `main.py`。

## 安装方式

你可以将本仓库放入支持 Skill / Agent 能力的工具目录中，例如：

```bash
git clone <your-repo-url> ~/.codex/skills/spider-king
```

如果你的工具支持通过 `SKILL.md` 自动加载技能定义，只要仓库目录结构保持一致即可。

## 适用场景

建议在以下场景触发 `Spider King`：

- 已拿到目标页面 URL、接口 URL、请求样本、Cookie 样本或 JS 片段
- 明确需要恢复参数、协议包裹、响应解码或状态流
- 目标存在 challenge、bootstrap、动态 Cookie、WebSocket、GraphQL、protobuf、WASM 或环境绑定逻辑
- 最终目标是可复现、可长期维护的协议采集器
- 需要将签名、bootstrap、challenge state 或 decode 逻辑真正落到 Python 或本地 helper 中
- 需要从多个失败面中判断真正门槛：transport、session、verifier、decode、wrapper 或 runtime

## 不适用场景

以下情况不建议使用这套 Skill 作为主路径：

- 需求本质只是标准 UI 自动化
- 目标本身没有公开协议恢复价值，只是简单页面录制
- 最终交付允许长期依赖浏览器 profile、人工点击或人工登录维持
- 只要求一次性浏览器脚本，不关心协议可复现性
- 不具备合法授权边界，不适合进入实际协议恢复流程

## 交付标准

一个通过 `Spider King` 完成的任务，理想上应包含以下产物：

- 真实接口路径说明
- 动态状态分类结论
- `chrome-devtools` 与 `js-reverse` 的关键证据
- 关键固定输入/输出验证样本
- Python collector
- 必要时的极小 JS / WASM / runtime helper
- 原始请求/响应样本
- Cookie、session、challenge artifact 的来源说明
- 风险与不稳定点说明

合格交付至少满足：

- 不依赖浏览器自动化
- 不依赖手工页面操作
- 重放逻辑可重复成功
- 关键动态状态可解释、可验证、可再生
- 如果存在 challenge 或 transport pre-gate，已明确记录真正门槛发生在哪一层
- 如果仍保留 embedded runtime，必须明确说明当前结果是 browser-free 还是 runtime-free

## 自检与防漂移

5.0 把“技能回归检查”和“经验沉淀规则”提升为正式维护内容：

- `references/official-self-test-task-suite.md` 用于验证主路线是否仍然 protocol-first
- `references/skill-maintenance.md` 用于约束后续经验如何沉淀
- `references/anti-patterns-playbook.md` 用于识别常见伪完成路径
- `references/escalation-ladder-playbook.md` 用于避免在证据不足时跳到更重运行时或更宽 patch
- `references/minimal-verifiable-facts-playbook.md` 用于保存可复用、可复验的结构事实
- `Startup Gate` 用于确保 fresh target 不会一上来就乱钻
- `tool-playbook.md` 强调只使用当前真实可用的 MCP 能力

后续如果继续演进这个仓库，建议始终一起维护三类内容：

- 主技能规则
- 参考手册路由
- 自测任务与回归标准

新增经验时，优先抽象成通用模式、症状、失败面或交付规则，不要把站点特例沉淀成不可迁移的 folklore。

## 一句话总结

`Spider King` 不是让浏览器替你干活。

它是让你把浏览器里看起来神秘、脆弱、依赖上下文的行为，拆回成一条可验证、可复现、可长期运行的本地协议链路。

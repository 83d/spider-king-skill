## 83d Fork 定制

本 fork 会在每次同步上游后自动重新施加一项本地安全约束：

- Node.js 分析依赖只能以固定版本安装到 `npm root -g`
- 禁止在目标项目、任务缓存、Skill 目录及其任意子目录生成 `node_modules`
- 禁止因分析工具安装而创建或改写项目内的包管理器锁文件
- 安装前后必须清点目标目录，并保留已有依赖树和锁文件不动
- 上游的 task-local npm 安装指引在本 fork 中由该规则取代

完整规则见 `references/node-dependency-isolation-playbook.md`。同步由 GitHub Actions 托管，不依赖本地电脑运行。

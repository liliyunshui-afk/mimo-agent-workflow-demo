# MiMo Agent 工作流助手 Demo

这是一个用于申请 MiMo API Token Plan 的 MVP 补充项目，展示“用户目标输入 -> 意图识别 -> 任务拆解 -> 多 Agent 路由 -> 质量检查”的完整工作流。

## 在线演示

GitHub Pages 地址预计为：

https://liliyunshui-afk.github.io/mimo-agent-workflow-demo/

如果页面暂时不可访问，请在仓库 `Settings -> Pages` 中选择 `Deploy from a branch`，分支选择 `main`，目录选择 `/root`。

## 项目用途

- 生成可复现的终端运行日志
- 生成 Agent 工作流截图或在线演示页
- 作为后续 GitHub 项目或静态托管 Demo 的最小可运行版本
- 后续可接入真实 MiMo API，补充脱敏运行日志和模型效果评测

## 本地运行

```bash
python workflow_demo.py
```

运行后会生成：

- `artifacts/terminal_run_log.txt`
- `artifacts/workflow_result.json`

## 网页 Demo

直接打开 `index.html` 即可查看本地静态 Demo。它也可以部署到 GitHub Pages、Vercel、Netlify 或任意静态网站托管服务。

## 说明

当前版本是 MVP dry-run，用于展示 Agent 编排逻辑和可验证产物格式。接入真实 MiMo API 后，建议补充：

- 脱敏 API 请求日志
- token 消耗统计截图
- 长上下文任务评测案例
- 多 Agent 协作结果对比表

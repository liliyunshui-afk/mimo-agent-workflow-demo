# MiMo Agent 工作流助手 Demo

这是一个用于申请 MiMo API Token Plan 的 MVP 补充项目，展示“用户目标输入 -> 意图识别 -> 任务拆解 -> 多 Agent 路由 -> 质量检查”的完整工作流。

## 在线演示

GitHub Pages 地址：

https://liliyunshui-afk.github.io/mimo-agent-workflow-demo/

GitHub 项目地址：

https://github.com/liliyunshui-afk/mimo-agent-workflow-demo

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

直接打开 `index.html` 即可查看本地静态 Demo。当前仓库也已通过 GitHub Pages 发布为在线演示页。

## 说明

当前版本是 MVP dry-run，用于展示 Agent 编排逻辑和可验证产物格式。接入真实 MiMo API 后，建议补充：

- 脱敏 API 请求日志
- token 消耗统计截图
- 长上下文任务评测案例
- 多 Agent 协作结果对比表

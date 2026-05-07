#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiMo Agent workflow MVP demo.

This script creates a reproducible terminal log for a local dry-run workflow:
intent recognition -> task decomposition -> sub-agent routing -> quality check.
If MIMO_API_KEY is set, the adapter status is recorded, but this public demo
still runs deterministically to keep the submitted evidence reproducible.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable


TZ_SHANGHAI = timezone(timedelta(hours=8), name="Asia/Shanghai")


@dataclass
class AgentOutput:
    agent: str
    objective: str
    result: list[str]
    checks: list[str]


class RunLogger:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def emit(self, level: str, message: str) -> None:
        stamp = datetime.now(TZ_SHANGHAI).strftime("%Y-%m-%d %H:%M:%S %Z")
        line = f"[{stamp}] {level:<5} {message}"
        self.lines.append(line)
        print(line)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(self.lines) + "\n", encoding="utf-8")


def classify_intent(goal: str) -> list[str]:
    goal_lower = goal.lower()
    intents: list[str] = []
    rules = {
        "资料整理": ["资料", "文档", "整理", "解析", "paper", "pdf"],
        "长文档总结": ["总结", "摘要", "归纳", "长文", "summary"],
        "任务拆解": ["拆解", "计划", "任务", "里程碑", "plan"],
        "内容生成": ["生成", "写作", "demo", "说明", "content"],
        "代码辅助": ["代码", "开发", "调试", "api", "agent", "workflow"],
        "结果校验": ["校验", "检查", "质量", "幻觉", "验证", "review"],
    }
    for label, keywords in rules.items():
        if any(keyword in goal_lower or keyword in goal for keyword in keywords):
            intents.append(label)
    return intents or ["任务拆解", "结果校验"]


def decompose_tasks(intents: Iterable[str]) -> list[str]:
    task_bank = {
        "资料整理": "收集输入资料，抽取标题、主题、关键实体和可引用结论。",
        "长文档总结": "生成分层摘要：一句话结论、要点列表、风险与待补充信息。",
        "任务拆解": "把用户目标拆成阶段、子任务、依赖关系和验收标准。",
        "内容生成": "根据任务计划生成说明文案、Demo 文本和提交材料。",
        "代码辅助": "检查项目结构，生成可运行脚本、接口适配层和调试建议。",
        "结果校验": "复核输出是否遗漏关键信息，并标注不确定项和改写建议。",
    }
    return [task_bank[intent] for intent in intents if intent in task_bank]


def run_sub_agents(goal: str, intents: list[str], tasks: list[str]) -> list[AgentOutput]:
    outputs: list[AgentOutput] = []
    if "资料整理" in intents:
        outputs.append(
            AgentOutput(
                agent="资料解析 Agent",
                objective="把原始目标转为结构化项目上下文",
                result=[
                    "项目主题：基于 MiMo API 的 AI Agent 工作流助手。",
                    "主要场景：资料整理、长文档总结、任务拆解、内容生成、结果校验。",
                    "关键能力：长上下文理解、多轮推理、复杂任务拆解、多 Agent 协作。",
                ],
                checks=["输入目标已保留", "核心场景已覆盖"],
            )
        )
    if "长文档总结" in intents:
        outputs.append(
            AgentOutput(
                agent="摘要生成 Agent",
                objective="生成可提交的短摘要和分层要点",
                result=[
                    "一句话摘要：该 MVP 用 Agent 编排减少复杂 AI 任务中的上下文丢失和工具切换。",
                    "核心价值：自动拆解目标、路由子 Agent、检查中间结果并输出可验证交付物。",
                ],
                checks=["摘要不引入未给出的上线数据", "保留 token 需求范围"],
            )
        )
    if "任务拆解" in intents:
        outputs.append(
            AgentOutput(
                agent="任务规划 Agent",
                objective="输出 MVP 阶段计划",
                result=[
                    "阶段 1：完成 CLI dry-run、网页 Demo、工作流截图和终端日志。",
                    "阶段 2：接入真实 MiMo API，补充脱敏调用日志和评测样例。",
                    "阶段 3：发布 GitHub 项目或在线演示页，开放小范围测试。",
                ],
                checks=["阶段可执行", "每阶段都有可验证产物"],
            )
        )
    if "内容生成" in intents:
        outputs.append(
            AgentOutput(
                agent="内容生成 Agent",
                objective="生成第 5 项申请材料文案",
                result=[
                    "材料建议：上传工作流截图、终端运行日志和项目说明图。",
                    "链接建议：优先提交 GitHub 项目链接；若尚未建仓，可提交在线 Demo 地址。",
                ],
                checks=["表述适合申请材料", "未夸大现有用户规模"],
            )
        )
    if "代码辅助" in intents:
        outputs.append(
            AgentOutput(
                agent="代码辅助 Agent",
                objective="提供可运行项目骨架",
                result=[
                    "已生成 workflow_demo.py：可复现工作流运行日志。",
                    "已生成 index.html：可作为 GitHub Pages 或静态托管 Demo。",
                ],
                checks=["无外部依赖", "可在本地直接运行"],
            )
        )
    if "结果校验" in intents:
        outputs.append(
            AgentOutput(
                agent="质量检查 Agent",
                objective="复核证据材料是否可信",
                result=[
                    "日志标注为 MVP dry-run，避免伪造成真实线上调用记录。",
                    "Demo 页面展示完整 Agent 流程，适合作为工作流截图或在线演示。",
                    "后续接入真实 API 后，可追加脱敏请求日志和模型评测表。",
                ],
                checks=["风险已说明", "后续补充路径清晰"],
            )
        )
    if not outputs:
        outputs.append(
            AgentOutput(
                agent="任务规划 Agent",
                objective="默认拆解用户目标",
                result=tasks,
                checks=["已生成基础计划"],
            )
        )
    return outputs


def build_result(goal: str) -> dict:
    intents = classify_intent(goal)
    tasks = decompose_tasks(intents)
    outputs = run_sub_agents(goal, intents, tasks)
    return {
        "goal": goal,
        "mode": "local_mvp_dry_run",
        "intents": intents,
        "tasks": tasks,
        "agent_outputs": [asdict(output) for output in outputs],
        "quality_summary": {
            "coverage": "目标、痛点、工作流、评测方向和 token 用量均已覆盖",
            "risk": "当前日志为本地 MVP dry-run，真实 MiMo API 调用日志需在接入 API key 后补充",
            "next_step": "发布 GitHub Pages 或在线 Demo，并追加脱敏运行日志",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MiMo Agent workflow MVP demo.")
    parser.add_argument(
        "--goal",
        default=(
            "基于 MiMo API 构建 AI Agent 工作流助手，用于资料整理、长文档总结、"
            "任务拆解、内容生成、代码辅助和结果校验。"
        ),
        help="User goal to process.",
    )
    parser.add_argument("--artifacts", default="artifacts", help="Artifact output directory.")
    args = parser.parse_args()

    artifact_dir = Path(args.artifacts)
    logger = RunLogger()

    logger.emit("INFO", "MiMo Agent Workflow Demo started")
    logger.emit("INFO", f"User goal: {args.goal}")
    logger.emit("INFO", "Execution mode: local MVP dry-run")
    if os.getenv("MIMO_API_KEY"):
        logger.emit("INFO", "MIMO_API_KEY detected; API adapter can be enabled for real calls")
    else:
        logger.emit("INFO", "MIMO_API_KEY not set; using deterministic local agents")

    result = build_result(args.goal)

    logger.emit("STEP", "01 Intent recognition")
    logger.emit("DATA", "Detected intents: " + " / ".join(result["intents"]))

    logger.emit("STEP", "02 Task decomposition")
    for index, task in enumerate(result["tasks"], start=1):
        logger.emit("TASK", f"{index:02d}. {task}")

    logger.emit("STEP", "03 Sub-agent routing and execution")
    for output in result["agent_outputs"]:
        logger.emit("AGENT", f"{output['agent']} -> {output['objective']}")
        for item in output["result"]:
            logger.emit("OUT", item)
        for check in output["checks"]:
            logger.emit("CHECK", check)

    logger.emit("STEP", "04 Final quality review")
    logger.emit("CHECK", result["quality_summary"]["coverage"])
    logger.emit("WARN", result["quality_summary"]["risk"])
    logger.emit("NEXT", result["quality_summary"]["next_step"])

    artifact_dir.mkdir(parents=True, exist_ok=True)
    result_path = artifact_dir / "workflow_result.json"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    log_path = artifact_dir / "terminal_run_log.txt"
    logger.save(log_path)

    logger.emit("INFO", f"Saved result JSON: {result_path}")
    logger.emit("INFO", f"Saved terminal log: {log_path}")
    logger.save(log_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

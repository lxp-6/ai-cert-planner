import argparse
import json
from datetime import datetime, timedelta


def parse_input(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def days_until_deadline(deadline_str):
    deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
    today = datetime.today().date()
    return max((deadline - today).days, 1)


def allocate_hours(subjects, total_hours, current_level):
    """按科目权重和基础水平分配总学习时长。"""
    level_factor = {"beginner": 1.5, "intermediate": 1.0, "advanced": 0.7}
    factor = level_factor.get(current_level, 1.0)
    total_weight = sum(s.get("weight", 0.5) for s in subjects)
    allocated = []
    for s in subjects:
        hours = total_hours * (s.get("weight", 0.5) / total_weight) * factor
        allocated.append({
            "name": s["name"],
            "weight": s.get("weight", 0.5),
            "hours": round(hours, 2),
            "hours_remaining": round(hours, 2)
        })
    return allocated


def build_daily_plan(subjects, days, daily_hours, exam):
    """把每个科目的总时长切成学习块，按天贪婪填充，保证每天约 daily_hours。"""
    plan = []
    today = datetime.today().date()
    session_duration = min(1.0, daily_hours / 2)  # 每块时长：1小时或半天的一半

    for day_index in range(days):
        current_date = today + timedelta(days=day_index)
        remaining_today = daily_hours
        # 按剩余未分配时长降序，优先安排剩余多的科目
        sorted_subjects = sorted(subjects, key=lambda x: x["hours_remaining"], reverse=True)

        for s in sorted_subjects:
            if remaining_today <= 0.05:
                break
            if s["hours_remaining"] <= 0.05:
                continue

            chunk = min(session_duration, s["hours_remaining"], remaining_today)
            chunk = round(chunk, 2)
            if chunk < 0.05:
                continue

            plan.append({
                "day": day_index + 1,
                "date": current_date.strftime("%Y-%m-%d"),
                "exam": exam,
                "subject": s["name"],
                "task": f"学习 {s['name']} 模块",
                "duration": round(chunk * 60, 0),
                "priority": "high" if s["weight"] >= 0.25 else "medium",
                "status": "planned",
                "review": False
            })

            s["hours_remaining"] -= chunk
            s["hours_remaining"] = round(s["hours_remaining"], 2)
            remaining_today -= chunk

    return plan


def main():
    parser = argparse.ArgumentParser(description="生成考证复习基线计划")
    parser.add_argument("--input", required=True, help="输入状态 JSON 路径")
    parser.add_argument("--output", required=True, help="输出计划 JSON 路径")
    args = parser.parse_args()

    state = parse_input(args.input)
    exam = state["exam"]
    deadline = state["deadline"]
    daily_hours = state["daily_hours"]
    current_level = state["current_level"]
    subjects = state["subjects"]

    days = days_until_deadline(deadline)
    total_hours = days * daily_hours

    allocated = allocate_hours(subjects, total_hours, current_level)
    plan = build_daily_plan(allocated, days, daily_hours, exam)

    output = {
        "exam": exam,
        "deadline": deadline,
        "days_remaining": days,
        "daily_hours": daily_hours,
        "current_level": current_level,
        "total_plan_hours": round(total_hours, 2),
        "plan": plan
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"已生成 {exam} 复习计划，共 {days} 天，{len(plan)} 个任务。")


if __name__ == "__main__":
    main()

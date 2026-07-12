import argparse
import json
from datetime import datetime, timedelta

# 艾宾浩斯复习间隔（天）
EBBINGHAUS_INTERVALS = [1, 2, 4, 7, 15]


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def insert_review_tasks(plan_data):
    plan = plan_data["plan"]
    today = datetime.today().date()
    deadline = datetime.strptime(plan_data["deadline"], "%Y-%m-%d").date()

    # 找到每个科目首次出现的日期
    first_seen = {}
    for task in plan:
        if task.get("review"):
            continue
        subject = task["subject"]
        if subject not in first_seen:
            first_seen[subject] = datetime.strptime(task["date"], "%Y-%m-%d").date()

    for subject, first_date in first_seen.items():
        for interval in EBBINGHAUS_INTERVALS:
            review_date = first_date + timedelta(days=interval)
            if review_date > deadline or review_date < today:
                continue
            plan.append({
                "day": (review_date - today).days + 1,
                "date": review_date.strftime("%Y-%m-%d"),
                "exam": plan_data["exam"],
                "subject": subject,
                "task": f"艾宾浩斯复习：{subject}",
                "duration": 10,
                "priority": "medium",
                "status": "planned",
                "review": True,
                "review_stage": interval,
                "note": f"第 {interval} 天遗忘曲线复习点"
            })

    plan.sort(key=lambda x: (x["date"], x["priority"] != "high", not x.get("review")))
    plan_data["plan"] = plan
    return plan_data


def main():
    parser = argparse.ArgumentParser(description="基于艾宾浩斯遗忘曲线插入复习任务")
    parser.add_argument("--plan", required=True, help="输入计划 JSON 路径")
    parser.add_argument("--output", required=True, help="输出含复习任务的计划 JSON 路径")
    args = parser.parse_args()

    plan_data = load_json(args.plan)
    plan_data = insert_review_tasks(plan_data)
    save_json(args.output, plan_data)

    review_count = sum(1 for t in plan_data["plan"] if t.get("review"))
    print(f"已插入 {review_count} 个艾宾浩斯复习任务。")


if __name__ == "__main__":
    main()

import argparse
import json
from collections import defaultdict


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def analyze_weak_points(scores):
    """从模考分数和错题标签中识别弱项。"""
    subject_stats = defaultdict(lambda: {"score_sum": 0, "total_sum": 0, "count": 0})
    tag_stats = defaultdict(lambda: {"wrong": 0, "total": 0})

    for record in scores:
        subject = record.get("subject")
        score = record.get("score", 0)
        total = record.get("total", 100)
        wrong_tags = record.get("wrong_tags", [])

        subject_stats[subject]["score_sum"] += score
        subject_stats[subject]["total_sum"] += total
        subject_stats[subject]["count"] += 1

        for tag in wrong_tags:
            tag_stats[tag]["wrong"] += 1
            tag_stats[tag]["total"] += 1

    # 计算科目失分率
    subject_weakness = []
    for subject, stats in subject_stats.items():
        rate = 1 - (stats["score_sum"] / stats["total_sum"])
        subject_weakness.append({
            "subject": subject,
            "loss_rate": round(rate, 2),
            "average_score": round(stats["score_sum"] / stats["count"], 1),
            "suggestion": "重点复习" if rate >= 0.3 else "保持巩固"
        })

    subject_weakness.sort(key=lambda x: x["loss_rate"], reverse=True)

    # 计算错题标签失分率
    tag_weakness = []
    for tag, stats in tag_stats.items():
        rate = stats["wrong"] / stats["total"] if stats["total"] > 0 else 0
        tag_weakness.append({
            "tag": tag,
            "wrong_rate": round(rate, 2),
            "suggestion": "专项训练" if rate >= 0.4 else "错题回顾"
        })

    tag_weakness.sort(key=lambda x: x["wrong_rate"], reverse=True)

    return {
        "top_weak_subjects": subject_weakness[:3],
        "top_weak_tags": tag_weakness[:3],
        "action_plan": [
            f"{s['subject']}: {s['suggestion']}" for s in subject_weakness[:3]
        ]
    }


def main():
    parser = argparse.ArgumentParser(description="分析模考弱项并给出复习建议")
    parser.add_argument("--scores", required=True, help="模考分数 JSON 路径")
    parser.add_argument("--output", required=True, help="输出弱项分析 JSON 路径")
    args = parser.parse_args()

    scores = load_json(args.scores)
    result = analyze_weak_points(scores)
    save_json(args.output, result)

    print("弱项分析完成。")
    for s in result["top_weak_subjects"]:
        print(f"- {s['subject']} 失分率 {s['loss_rate']:.0%}")


if __name__ == "__main__":
    main()

from collections import defaultdict


def to_box_key(combination):
    """
    BOX用キー
    例
    [5,8,9,0] → '0589'
    """
    return "".join(map(str, sorted(combination)))


def create_box_ranking(ranking):
    """
    ストレート候補をBOXごとに集約する
    """

    box_scores = defaultdict(float)
    box_count = defaultdict(int)

    for item in ranking:
        box = to_box_key(item["combination"])

        box_scores[box] += item["score"]
        box_count[box] += 1

    results = []

    for box in box_scores:
        results.append({
            "box": box,
            "score": box_scores[box],
            "count": box_count[box],
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results
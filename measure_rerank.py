"""Measure Context Recall / Context Precision before and after reranking.

Exercise 3.5. Reads the real retrieval trace from artifacts/actual_answers.json
and the expected answers from golden_dataset.json, then compares the metrics for
the chunks in BM25 order against the same chunks after rerank_by_overlap().
"""

import json
from pathlib import Path

from template import RAGASEvaluator, rerank_by_overlap

evaluator = RAGASEvaluator()

expected_by_id = {
    item["id"]: item["expected_answer"]
    for item in json.loads(Path("golden_dataset.json").read_text(encoding="utf-8"))["qa_pairs"]
}
artifact = json.loads(Path("artifacts/actual_answers.json").read_text(encoding="utf-8"))

rows = []
for answer in artifact["answers"]:
    case_id = answer["id"]
    question = answer["question"]
    contexts = [chunk["text"] for chunk in answer["retrieved_contexts"]]
    expected = expected_by_id[case_id]
    reranked = rerank_by_overlap(contexts, question)

    rows.append(
        {
            "id": case_id,
            "recall_before": evaluator.evaluate_context_recall(contexts, expected),
            "recall_after": evaluator.evaluate_context_recall(reranked, expected),
            "precision_before": evaluator.evaluate_context_precision(contexts, expected),
            "precision_after": evaluator.evaluate_context_precision(reranked, expected),
            "order_changed": reranked != contexts,
        }
    )

print("| ID | Recall before | Recall after | Precision before | Precision after | Order changed |")
print("|---|---:|---:|---:|---:|---|")
for row in rows:
    print(
        f"| {row['id']} | {row['recall_before']:.3f} | {row['recall_after']:.3f} "
        f"| {row['precision_before']:.3f} | {row['precision_after']:.3f} "
        f"| {'yes' if row['order_changed'] else 'no'} |"
    )

count = len(rows)


def average(key):
    return sum(row[key] for row in rows) / count


print()
print(f"cases measured: {count}")
print(f"mean recall    before={average('recall_before'):.4f} after={average('recall_after'):.4f}")
print(f"mean precision before={average('precision_before'):.4f} after={average('precision_after'):.4f}")
print(f"order changed in {sum(row['order_changed'] for row in rows)}/{count} cases")
print(f"precision improved: {sum(r['precision_after'] > r['precision_before'] for r in rows)}")
print(f"precision worsened: {sum(r['precision_after'] < r['precision_before'] for r in rows)}")
print(f"precision unchanged: {sum(r['precision_after'] == r['precision_before'] for r in rows)}")

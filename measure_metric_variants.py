"""Re-score the existing artifacts under metric variants, with no model calls.

Every number quoted in reflection.md sections 3, 4 and 6 that differs from
artifacts/benchmark_results.json is produced here. The free-tier key allows 20
requests per day and all 20 were spent on the benchmark run, so these three
experiments deliberately reuse artifacts/actual_answers.json instead of
regenerating answers.

  1. faithfulness scored on the retrieved contexts instead of the gold snippets
  2. pinning 00_system_scope.md at the front versus at the end of the context list
  3. whether a wrong policy version survives the word-overlap metrics
"""

import json
from pathlib import Path

from domain_assistant import load_corpus
from template import RAGASEvaluator

CORPUS_DIR = "data/technology_store"
SCOPE_DOC = "00_system_scope.md"

evaluator = RAGASEvaluator()

golden = {
    item["id"]: item
    for item in json.loads(Path("golden_dataset.json").read_text(encoding="utf-8"))["qa_pairs"]
}
artifact = json.loads(Path("artifacts/actual_answers.json").read_text(encoding="utf-8"))
answers = {item["id"]: item for item in artifact["answers"]}
results = {
    item["id"]: item
    for item in json.loads(Path("artifacts/benchmark_results.json").read_text(encoding="utf-8"))["results"]
}


def retrieved_texts(case_id):
    return [chunk["text"] for chunk in answers[case_id]["retrieved_contexts"]]


def gold_texts(case_id):
    return [context["text"] for context in golden[case_id]["contexts"]]


def measure_faithfulness_context():
    """Variant 1: does faithfulness change when scored on what the model saw?"""
    print("=== 1. faithfulness: gold snippets vs retrieved contexts ===")
    print("| ID | F (gold) | F (retrieved) | verdict before | verdict after |")
    print("|---|---:|---:|---|---|")
    flips_up = flips_down = 0
    total_gold = total_retrieved = 0.0
    for case_id in results:
        result = results[case_id]
        answer = result["actual_answer"]
        f_gold = evaluator.evaluate_faithfulness(answer, "\n\n".join(gold_texts(case_id)))
        f_retr = evaluator.evaluate_faithfulness(answer, "\n\n".join(retrieved_texts(case_id)))
        total_gold += f_gold
        total_retrieved += f_retr
        after = min(f_retr, result["relevance"], result["completeness"]) >= 0.5
        if after and not result["passed"]:
            flips_up += 1
        if result["passed"] and not after:
            flips_down += 1
        print(
            f"| {case_id} | {f_gold:.3f} | {f_retr:.3f} "
            f"| {'pass' if result['passed'] else 'fail'} | {'pass' if after else 'fail'} |"
        )
    count = len(results)
    print()
    print(f"mean faithfulness gold={total_gold / count:.4f} retrieved={total_retrieved / count:.4f}")
    print(f"flipped to pass: {flips_up}   flipped to fail: {flips_down}")
    print(f"pass rate {sum(r['passed'] for r in results.values())}/{count} -> "
          f"{sum(r['passed'] for r in results.values()) + flips_up - flips_down}/{count}")


def measure_scope_pinning():
    """Variant 2: recall is position-invariant, AP@K is not."""
    print()
    print(f"=== 2. pinning {SCOPE_DOC}: front vs end ===")
    scope_chunks = [chunk for chunk in load_corpus(CORPUS_DIR)[1] if chunk.source_doc == SCOPE_DOC]
    pinned_all = [chunk.text for chunk in scope_chunks]
    pinned_three = [chunk.text for chunk in scope_chunks if chunk.chunk_id in
                    ("OT-00-P02", "OT-00-P03", "OT-00-P04")]
    variants = {
        "baseline (top_k=5)": lambda base: base,
        "3 chunks at front": lambda base: pinned_three + base,
        "6 chunks at front": lambda base: pinned_all + base,
        "3 chunks at end": lambda base: base + pinned_three,
        "6 chunks at end": lambda base: base + pinned_all,
    }
    totals = {name: [0.0, 0.0] for name in variants}
    print("| ID | " + " | ".join(variants) + " |")
    print("|---|" + "---:|" * len(variants))
    for case_id in sorted(answers):
        expected = golden[case_id]["expected_answer"]
        base = retrieved_texts(case_id)
        cells = []
        for name, build in variants.items():
            contexts = build(base)
            recall = evaluator.evaluate_context_recall(contexts, expected)
            precision = evaluator.evaluate_context_precision(contexts, expected)
            totals[name][0] += recall
            totals[name][1] += precision
            cells.append(f"{recall:.3f}/{precision:.3f}")
        print(f"| {case_id} | " + " | ".join(cells) + " |")
    count = len(answers)
    print()
    print("(each cell is recall/precision)")
    for name in variants:
        print(f"{name:<22} mean recall={totals[name][0] / count:.4f}  "
              f"mean precision={totals[name][1] / count:.4f}")


def measure_policy_version_blindspot():
    """Variant 3: a wrong policy version that is written at full length."""
    print()
    print("=== 3. wrong policy version on H01 ===")
    case_id = "H01"
    question = golden[case_id]["question"]
    expected = golden[case_id]["expected_answer"]
    context = "\n\n".join(gold_texts(case_id))
    candidates = [
        ("correct (the real answer)", results[case_id]["actual_answer"]),
        ("wrong A: 30 days (v2.0 window)",
         "Because the order was placed on August 20, 2026, the customer has 30 calendar days "
         "to return the unopened NovaBook 14. The triggering event for return-policy "
         "eligibility is the order-placement date, while the number of return days is counted "
         "from confirmed delivery, so the 30 days run from August 25, 2026. The active "
         "membership does not change this window."),
        ("wrong B: 45 days via OrbitPlus",
         "Because the order was placed on August 20, 2026 and the customer holds an active "
         "OrbitPlus membership, the unopened NovaBook 14 may be returned within 45 calendar "
         "days. The triggering event for return-policy eligibility is the order-placement "
         "date, while the number of return days is counted from confirmed delivery, so the 45 "
         "days run from August 25, 2026."),
        ("wrong C: counted from order date",
         "Because the order was placed on August 20, 2026, Return Policy version 1.0 applies, "
         "which allowed 21 calendar days for unopened devices. The number of return days is "
         "counted from the order-placement date, so the 21 days run from August 20, 2026. The "
         "active membership does not change this, because orders placed before September 1 "
         "keep the 21-day version 1.0 window regardless of membership."),
    ]
    print("ground truth: order 2026-08-20 -> policy v1.0 -> 21 days from delivery 2026-08-25;"
          " OrbitPlus does not extend a v1.0 order.")
    print()
    print("| candidate | faithfulness | relevance | completeness | overall | passed |")
    print("|---|---:|---:|---:|---:|---|")
    for label, answer in candidates:
        faithfulness = evaluator.evaluate_faithfulness(answer, context)
        relevance = evaluator.evaluate_relevance(answer, question)
        completeness = evaluator.evaluate_completeness(answer, expected)
        overall = (faithfulness + relevance + completeness) / 3
        passed = min(faithfulness, relevance, completeness) >= 0.5
        print(f"| {label} | {faithfulness:.3f} | {relevance:.3f} | {completeness:.3f} "
              f"| {overall:.3f} | {'yes' if passed else 'no'} |")


if __name__ == "__main__":
    measure_faithfulness_context()
    measure_scope_pinning()
    measure_policy_version_blindspot()

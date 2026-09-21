import json
import requests

with open("evals/cases.json") as f:
    cases = json.load(f)

correct = 0
failed_cases = []

for case in cases:
    response = requests.post(
        "http://localhost:8000/triage",
        json={"text": case["text"]},
        timeout=35
    )
    if response.status_code == 200:
        result = response.json()
        if result["category"] == case["expected_category"]:
            correct += 1
        else:
            failed_cases.append({
                "text": case["text"],
                "expected": case["expected_category"],
                "got": result["category"]
            })
    else:
        failed_cases.append({
            "text": case["text"],
            "expected": case["expected_category"],
            "got": f"HTTP {response.status_code}"
        })

print(f"\nScore: {correct}/{len(cases)}")
if failed_cases:
    print("\nFailed cases:")
    for f in failed_cases:
        print(f"  Text: {f['text']}")
        print(f"  Expected: {f['expected']}, Got: {f['got']}\n")
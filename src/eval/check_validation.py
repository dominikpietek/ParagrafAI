from serving.validation import count_matches, MIN_MATCHES
from pathlib import Path
import json

def is_validation_valid() -> bool:
    if (test_validation_file("val.jsonl") and test_validation_file("test.jsonl")):
        return True
    else:
        return False

def test_validation_file(filename: str) -> bool:
    src_dir = Path(__file__).parent.parent.resolve()
    file = str(src_dir / "data" / filename)
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            example = json.loads(line)
            message = example["messages"][:-1][0]["content"]
            judgment = message.split("=====\n", 1)[1].rsplit("\n======", 1)[0]
            if (count_matches(message) < MIN_MATCHES):
                return False
    return True

print(is_validation_valid())
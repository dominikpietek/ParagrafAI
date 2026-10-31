from attr import dataclass
import torch
from unsloth import FastLanguageModel 
import json
import yaml

print("Test sprzętu:")
print(torch.cuda.is_available(), torch.cuda.device_count(), torch.cuda.get_device_name(0), torch.cuda.memory_allocated())

@dataclass
class ReturnData:
    passed: int
    failed: int
    wrong_yaml: int
    avg_percentage: float

def model_test_set(filename, model_name_string):
    model, tokenizer = FastLanguageModel.from_pretrained(
         model_name=model_name_string,
        max_seq_length=4096, load_in_4bit=True)

    passed = 0
    failed = 0
    wrong_yaml = 0

    fields_percentage = []

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            example = json.loads(line)
            message = example["messages"][:-1]
            expected_output = example["messages"][-1]["content"]

            input = tokenizer.apply_chat_template(message, add_generation_prompt=True, tokenize=True, return_tensors="pt", return_dict=True).to("cuda")

            outputs = model.generate(
                **input,
                max_new_tokens=300,
                do_sample=False,
            )

            new_tokens = outputs[0][input["input_ids"].shape[1]:]
            answer = tokenizer.decode(new_tokens, skip_special_tokens=True)
            if is_valid_yaml(answer):
                is_correct, percentage = compare_yaml(expected_output, answer)
                if (is_correct):
                    passed += 1
                else:
                    failed += 1
                fields_percentage.append(percentage)
            else:
                wrong_yaml += 1

    return ReturnData(passed, failed, wrong_yaml, sum(fields_percentage)/len(fields_percentage) if len(fields_percentage) > 0 else 0.0)
    
def is_valid_yaml(yaml_string):
    try:
        text = yaml_string.strip().removeprefix("```yaml").removesuffix("```")
        yaml.safe_load(text)
        return True
    except yaml.YAMLError:
        return False

def compare_yaml(expected_yaml: str, actual_yaml: str) -> (bool, float):
    try:
        expected_yaml = expected_yaml.strip().removeprefix("```yaml").removesuffix("```")
        expected_data = yaml.safe_load(expected_yaml)
        actual_yaml = actual_yaml.strip().removeprefix("```yaml").removesuffix("```")
        actual_data = yaml.safe_load(actual_yaml)
        # print("Expected data:", expected_data)
        # print("Actual data:", actual_data)
        # print("----------------------")
        return (expected_data == actual_data, compare_fields(expected_data, actual_data))
    except yaml.YAMLError:
        return (False, 0.0)

TEXT_FIELDS = ["court_name", "date", "department_name", "recorder", "signature"]
LIST_FIELDS = ["judges", "legal_bases"]

def compare_fields(expected, actual):
    good = 0
    bad = 0
    for field in TEXT_FIELDS:
        try:
            if expected[field] == actual[field]:
                good += 1
            else:
                bad += 1
        except:
            bad += 1
    for field in LIST_FIELDS:
        try:
            if expected[field] == actual[field]:
                good += 1
            else:
                bad += 1
        except:
            bad += 1
    result = good / (len(TEXT_FIELDS) + len(LIST_FIELDS))
    # print("Result ----------------------")
    # print(result)
    # print("----------------------")
    return result
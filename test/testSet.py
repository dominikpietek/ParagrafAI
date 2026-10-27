import torch
from unsloth import FastLanguageModel 
import json
import yaml

print("Test sprzętu:")
print(torch.cuda.is_available(), torch.cuda.device_count(), torch.cuda.get_device_name(0), torch.cuda.memory_allocated())

def model_test_set(filename):
    model, tokenizer = FastLanguageModel.from_pretrained(model_name="speakleash/Bielik-4.5B-v3.0-Instruct",max_seq_length=4096, load_in_4bit=True)

    passed = 0
    failed = 0
    wrong_yaml = 0

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
                if (compare_yaml(expected_output, answer)):
                    passed += 1
                else:
                    failed += 1
            else:
                wrong_yaml += 1

    print(f"Testy zakończone. Poprawne: {passed}, Niepoprawne: {failed}, Niepoprawny YAML: {wrong_yaml}")
    
def is_valid_yaml(yaml_string):
    try:
        yaml.safe_load(yaml_string)
        return True
    except yaml.YAMLError:
        return False

def compare_yaml(expected_yaml, actual_yaml):
    expected_data = yaml.safe_load(expected_yaml)
    actual_data = yaml.safe_load(actual_yaml)
    return expected_data == actual_data

model_test_set("val.jsonl")
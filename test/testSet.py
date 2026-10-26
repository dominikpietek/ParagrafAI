import torch
from unsloth import FastLanguageModel 

print("Test sprzętu:")
print(torch.cuda.is_available(), torch.cuda.device_count(), torch.cuda.get_device_name(0), torch.cuda.memory_allocated())

def model_test_set(filename):
    model, tokenizer = FastLanguageModel.from_pretrained(model_name="speakleash/Bielik-4.5B-v3.0-Instruct",max_seq_length=2048, load_in_4bit=True)

    # with open(filename, "r", encoding="utf-8") as f:
    #     for line in f:


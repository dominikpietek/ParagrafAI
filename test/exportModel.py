from unsloth import FastLanguageModel
import subprocess

def export_model():
    model, tokenizer = FastLanguageModel.from_pretrained(model_name="adapter_test",max_seq_length=2048, load_in_4bit=True)
    # model.save_pretrained(
    #     "paragrafLLM",
    #     tokenizer,
    #     # quantization_method="q4_k_m"
    # )
    model.save_pretrained_merged(
        "paragrafLLM_merged",      # osobny folder, żeby nie mieszać z GGUF
        tokenizer,
        save_method="merged_16bit",
)

def register_model():
    subprocess.run(["ollama", "create", "paragrafLLM", "-f", "Modelfile"], cwd="paragrafLLM_merged")
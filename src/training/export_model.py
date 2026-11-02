from unsloth import FastLanguageModel
import subprocess
from pathlib import Path

def export_model():
    base_dir = Path(__file__).parent.parent.resolve() / "model"
    model, tokenizer = FastLanguageModel.from_pretrained(model_name=str(base_dir / "adapter_test"),max_seq_length=2048, load_in_4bit=True)
    model.save_pretrained_merged(
        str(base_dir / "merged_no_gguf"),      
        tokenizer,
        save_method="merged_16bit",
)

def register_model():
    subprocess.run(["ollama", "create", "paragrafLLM", "-f", "Modelfile"], cwd="../../model/merged_no_gguf")
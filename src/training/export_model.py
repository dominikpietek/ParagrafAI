from unsloth import FastLanguageModel
import subprocess
from pathlib import Path

def export_model():
    base_dir = Path(__file__).parent.parent.parent.resolve() / "model"
    model, tokenizer = FastLanguageModel.from_pretrained(model_name=str(base_dir / "adapter_test"),max_seq_length=2048, load_in_4bit=True)
    model.save_pretrained_gguf(
        str(base_dir / "merged_gguf"),      
        tokenizer,
        save_method="f16",
)

def register_model():
    base_dir = Path(__file__).parent.parent.parent.resolve() / "model"
    subprocess.run(
        ["ollama", "create", "paragrafLLM", "-f", "Modelfile"],
        cwd=str(base_dir),
        check=True,
    )
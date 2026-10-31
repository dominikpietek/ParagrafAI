from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer, SFTConfig
from unsloth.chat_templates import train_on_responses_only

def learn_model():
    print("Model loading...")

    model, tokenizer = FastLanguageModel.from_pretrained(model_name="speakleash/Bielik-4.5B-v3.0-Instruct",max_seq_length=2048, load_in_4bit=True)

    adapter = FastLanguageModel.get_peft_model(model, r=16)

    print("Dataset loading...")

    dataset = load_dataset("json", data_files="train.jsonl", split="train")
    n_train_dataset = dataset.select(range(20))

    config = SFTConfig(max_seq_length=2048, output_dir="adapter_test", learning_rate=2e-4, num_train_epochs=3, logging_steps=1)
    trainer = SFTTrainer(model=adapter, train_dataset=n_train_dataset, args=config, tokenizer=tokenizer)
    trainer = train_on_responses_only(
        trainer,
        instruction_part = "<|im_start|>user\n",
        response_part    = "<|im_start|>assistant\n",
    )

    print("Training...")

    trainer.train()

    print("Saving adapter...")

    adapter.save_pretrained("adapter_test")
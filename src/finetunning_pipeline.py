from data.prepare_data import prepare_data
from eval.test_model import model_test_set
from training.learn import learn_model
from training.export_model import export_model, register_model
from pathlib import Path

def run():
    prepare_data("testdataset")

    base_dir_data = Path(__file__).resolve().parent / "data"

    ret1 = model_test_set(str(base_dir_data / "val.jsonl"), "speakleash/Bielik-4.5B-v3.0-Instruct")
    print_results(ret1)
            
    learn_model()
    print("Export model:")
    export_model()

    print("Test adapter:")
    adapter_dir = Path(__file__).parent.parent.resolve() / "model"
    ret2 = model_test_set(str(base_dir_data / "val.jsonl"), str(adapter_dir / "adapter_test"))
    print_results(ret2)

    print("Register ollama model:")
    register_model()

    print("Test final model:")
    ret3 = model_test_set(str(base_dir_data / "val.jsonl"), "paragrafLLM")
    print_results(ret3)

def print_results(ret):
    print(f"Testy zakończone: Poprawne: {ret.passed}, Niepoprawne: {ret.failed}, "
          f"Niepoprawny YAML: {ret.wrong_yaml}, Średnia poprawność pól: {ret.avg_percentage}")

if __name__ == "__main__":
    run()
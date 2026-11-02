from data.prepare_data import prepare_data
from eval.test_model import model_test_set
from training.learn import learn_model
from training.export_model import export_model, register_model
from pathlib import Path

prepare_data("testdataset")

base_dir_data = Path(__file__).resolve().parent / "data"

ret1 = model_test_set(str(base_dir_data / "val.jsonl"), "speakleash/Bielik-4.5B-v3.0-Instruct")

print(f"Testy zakończone. Poprawne: {ret1.passed}, Niepoprawne: {ret1.failed}, Niepoprawny YAML: {ret1.wrong_yaml}, " +
          f"Srednia poprawność pól: {ret1.avg_percentage}")
		  
learn_model()
print("Export model:")
export_model()

print("Test adapter:")
ret2 = model_test_set(str(base_dir_data / "val.jsonl"), "adapter_test")
print(f"Testy zakończone. Poprawne: {ret2.passed}, Niepoprawne: {ret2.failed}, Niepoprawny YAML: {ret2.wrong_yaml}, " +
          f"Srednia poprawność pól: {ret2.avg_percentage}")

print("Register ollama model:")
register_model()

print("Test final model:")
ret3 = model_test_set(str(base_dir_data / "val.jsonl"), "paragrafLLM")
print(f"Testy zakończone. Poprawne: {ret3.passed}, Niepoprawne: {ret3.failed}, Niepoprawny YAML: {ret3.wrong_yaml}, " +
          f"Srednia poprawność pól: {ret3.avg_percentage}")
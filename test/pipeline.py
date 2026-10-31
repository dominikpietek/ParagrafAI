from testData import prepare_data
from testSet import model_test_set
from learn import learn_model
from exportModel import export_model, register_model

prepare_data("testdataset")

ret1 = model_test_set("val.jsonl", "speakleash/Bielik-4.5B-v3.0-Instruct")

print(f"Testy zakończone. Poprawne: {ret1.passed}, Niepoprawne: {ret1.failed}, Niepoprawny YAML: {ret1.wrong_yaml}, " +
          f"Srednia poprawność pól: {ret1.avg_percentage}")
		  
learn_model()
print("Export model:")
export_model()

print("Test adapter:")
ret2 = model_test_set("val.jsonl", "adapter_test")
print(f"Testy zakończone. Poprawne: {ret2.passed}, Niepoprawne: {ret2.failed}, Niepoprawny YAML: {ret2.wrong_yaml}, " +
          f"Srednia poprawność pól: {ret2.avg_percentage}")

print("Register ollama model:")
register_model()

print("Test final model:")
ret3 = model_test_set("val.jsonl", "paragrafLLM")
print(f"Testy zakończone. Poprawne: {ret3.passed}, Niepoprawne: {ret3.failed}, Niepoprawny YAML: {ret3.wrong_yaml}, " +
          f"Srednia poprawność pól: {ret3.avg_percentage}")
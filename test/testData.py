from datasets import load_dataset
import yaml, json
from transformers import AutoTokenizer
import re
import html
from sklearn.model_selection import train_test_split

dataset = load_dataset("parquet", data_files={"train": "testdataset.parquet"}, split="train")
df = dataset.to_pandas()

print("columns:")
print(df.columns)

print("number of rows before clear:", len(df))

empty = df.isna() | df.apply(lambda c: c.astype(str).str.strip() == "")

df = df[~empty.any(axis=1)]

print("number of rows after clear:", len(df))

def get_department(text):
    text = text.strip().removeprefix("```yaml").removesuffix("```")
    data = yaml.safe_load(text)
    return data["department_name"]

df["department"] = df["output"].apply(get_department)

df["department_type"] = df["department"].str.extract(r"(?i)wydział\s+(.*)")

departmentTypesCounter = {}

for name in df["department_type"]:
    if name not in departmentTypesCounter:
        departmentTypesCounter[name] = 1
    else:
        departmentTypesCounter[name] += 1

print(departmentTypesCounter)
allWorkDepartments = [name for name in departmentTypesCounter.keys() if isinstance(name, str) and "pracy" in name.lower()]
allConsumerDepartments = [name for name in departmentTypesCounter.keys() if isinstance(name, str) and "konsum" in name.lower()]
print(allWorkDepartments)
print(allConsumerDepartments)

mask = df["department_type"].isin(allWorkDepartments + allConsumerDepartments)

print("Filtr 1 pracy i konsunta")
print("number of rows before clear:", len(df))
df = df[mask]
print("number of rows after clear:", len(df))

tok = AutoTokenizer.from_pretrained("speakleash/Bielik-4.5B-v3.0-Instruct")

for col in ["context", "output"]:
    df[f"{col}_tokens"] = df[col].astype(str).map(lambda t: len(tok(t).input_ids))

df[[c for c in df.columns if c.endswith("_tokens")]].hist(bins=50)

print(df.columns)

mask = (df["context_tokens"] < 2048) & (df["output_tokens"] < 2048)

print("Filtr 2 tokenów < 2048")
print("number of rows before clear:", len(df))
df = df[mask]
print("number of rows after clear:", len(df))


def clean_text(text: str) -> str:
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"[ \t\xa0]+", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]", " ", text)
    text = re.sub(r"(?:\s*(?:\(\.\.\.\)|\d+))+\s*$", "", text)
    text = text.strip()
    return text

print("Filtr 3 czyszczenie")
df["clean_context"] = df["context"].apply(clean_text)

print("number of rows cleared:", (df["clean_context"] != df["context"]).sum())

def anonymize_text(text: str) -> str:
    text = re.sub(r"\b\d{11}\b", "<PESEL>", text)
    text = re.sub(r"\b\d{9}\b", "<REGON>", text)
    text = re.sub(r"\b\d{10}\b", "<NIP>", text)
    text = re.sub(r"\b\d{2}-\d{3}\b", "<POSTAL_CODE>", text)
    return text

print("Filtr 4 anonimizacja")

patterns = {"pesel": r"\b\d{11}\b", "kod": r"\b\d{2}-\d{3}\b", "nip": r"\b\d{10}\b", "regon": r"\b\d{9}\b"}
for name, p in patterns.items():
    hits = df["clean_context"].str.findall(p)
    for hit in hits.explode().dropna().unique():
        print(f"Found {name}: {hit}")

df["final_context"] = df["clean_context"].apply(anonymize_text)

print("Change columns names")

df = df[["_id", "prompt", "final_context", "output"]]
df = df.rename(columns={"final_context": "context"})

print("Start 90/5/5 split")
ninety_percent, ten_percent = train_test_split(df, test_size=0.1, random_state=42)
val, test = train_test_split(ten_percent, test_size=0.5, random_state=42)

print(f"Train: {len(ninety_percent)}, Validation: {len(val)}, Test: {len(test)}")

ninety_percent.to_parquet("train.parquet")
val.to_parquet("val.parquet")
test.to_parquet("test.parquet")

print("Generate jsonl files")

def to_chat(prompt: str, context: str, output: str) -> str:
    return json.dumps({
        "messages": [
            {"role": "user", "content": prompt.replace("{context}", context)},
            {"role": "assistant", "content": output}
        ]
    }, ensure_ascii=False)

def write_dataframe_to_jsonl(df, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for line in (to_chat(p, c, o) for p, c, o in zip(df["prompt"], df["context"], df["output"])):
            f.write(line + "\n")

write_dataframe_to_jsonl(ninety_percent, "train.jsonl")
write_dataframe_to_jsonl(val, "val.jsonl")
write_dataframe_to_jsonl(test, "test.jsonl")

print("TEST DATA ---------------------")

tok = AutoTokenizer.from_pretrained("speakleash/Bielik-4.5B-v3.0-Instruct")

with open("val.jsonl", "r", encoding="utf-8") as f:
    val_line = json.loads(f.readline())
    text = tok.apply_chat_template(val_line["messages"], tokenize=False)
    print(text[:1500])    # początek: instrukcja i wyrok
    print("...")
    print(text[-800:])    # koniec: odpowiedź asystenta
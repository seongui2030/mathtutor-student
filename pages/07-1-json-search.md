# 07-1. math.json 검색

`input_guardrail()`는 현재 디렉터리의 `math_json/math.json`을 열어 데이터를 로드합니다.

```python
math_path = os.path.join(current_dir, "math_json", "math.json")
with open(math_path, "r", encoding="utf-8") as jf:
    math_data = json.load(jf)
```

이후 `data` 배열을 순회하며 각 `terms` 안의 `word`를 확인합니다. 말한 문장 안에 해당 단어가 들어가면 수학 문제로 판단합니다.

요약하면, 이 단계는 문장 속의 개념 단어를 사전에 대응시키는 검색 과정입니다.

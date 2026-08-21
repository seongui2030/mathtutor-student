
`math_json/math.json`은 수학 질문을 인식하기 위한 핵심 데이터 파일입니다. STT로 변환된 문장은 이 사전과 비교되며, 해당 문장 안에 어떤 수학 용어가 포함되어 있는지를 찾는 과정이 바로 이 단계의 핵심입니다.

`input_guardrail()`는 현재 디렉터리의 `math_json/math.json`을 열어 데이터를 로드합니다.

```python
math_path = os.path.join(current_dir, "math_json", "math.json")
with open(math_path, "r", encoding="utf-8") as jf:
    math_data = json.load(jf)
```

이후 `data` 배열을 순회하며 각 `terms` 안의 `word`를 확인합니다. 말한 문장 안에 해당 단어가 들어가면 수학 문제로 판단하고, 그 의미를 사전 기반으로 해석합니다.

예시 형태는 다음과 같습니다.

```json
{
  "더하기": "plus",
  "빼기": "minus",
  "곱하기": "multiply",
  "나누기": "divide",
  "제곱": "square"
}
```

이처럼 데이터 파일은 단순한 단어 목록이 아니라, 사용자 발화의 의미를 수학 개념과 연결하는 기준점 역할을 합니다. 문장 속의 개념 단어를 사전에 대응시키는 과정이 바로 `math.json` 검색이며, 이 단계가 잘 동작해야 이후 용어 설명이나 GPT 응답 생성이 안정적으로 이루어집니다.

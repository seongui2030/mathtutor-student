
`chatgpt_conn.py`는 OpenAI Responses API를 호출해 사용자 질문에 대한 자연어 설명을 생성합니다.

이 기능은 단순한 문장 생성기가 아니라, 수학 문맥에서 개념을 설명하고 대화 흐름을 유지하는 인터페이스 역할을 합니다. 예를 들면 다음과 같은 질문에 대응할 수 있습니다.

- 정의를 간단히 설명해 달라
- 왜 그렇게 계산되는지 설명해 달라
- 계산 과정을 쉽게 설명해 달라
- 다른 표현으로 설명해 달라

이러한 응답은 초보 학습자에게 특히 유용합니다. 수학 용어를 단순히 암기하는 것이 아니라, 의미와 맥락을 함께 이해할 수 있게 도와줍니다.

```python
response = client.responses.create(
    model="gpt-4o-mini",
    input=user_message,
)
return response.output_text
```

이 흐름을 통해 생성된 문자열은 최종적으로 TTS로 전달되어 사용자에게 다시 들릴 수 있습니다.

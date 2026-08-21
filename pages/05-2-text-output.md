
STT 단계가 끝나면 입력 문장 텍스트가 생성됩니다. 예를 들어 사용자가 “삼 더하기 이”라고 말하면, 추출된 문자열은 그대로 아래 단계로 전달됩니다.

```python
input_text = call_transcribe(str(audio_path))
input_text = input_text.strip()
print("원문(STT):", input_text)
```

이 단계의 결과물은 다음 두 가지 역할을 합니다.

1. 의미 정규화의 입력값
2. 수학 도메인 매칭의 기준 문장

즉, 실제 계산 로직이 시작되기 전의 가장 중요한 원본 문장 데이터입니다.

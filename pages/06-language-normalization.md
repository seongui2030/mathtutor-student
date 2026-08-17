# 06. 언어 정규화

STT로 추출된 텍스트는 곧바로 `normalize_dialect()`로 전달됩니다.

이 함수는 발음이 비슷하거나 표준어와 다르게 말해도, 수학 질문을 올바르게 인식할 수 있도록 텍스트를 정리합니다.

```python
def normalize_dialect(text):
    text = text.replace('아마', '암')
    text = text.replace('이', '2')
    text = text.replace('삼', '3')
    text = text.replace('사', '4')
    return text
```

예를 들어 발음상 혼동이 있는 숫자 표현을 정규화하여, 실제 수학 문맥에 맞는 형태로 바꾸는 역할을 수행합니다.

이 단계는 뒤의 `math_json/math.json` 매칭을 안정적으로 만들기 위한 전처리 단계입니다.

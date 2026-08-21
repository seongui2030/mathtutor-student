
매칭이 되면 해당 `term`의 `subject_meaning`과 `example` 값을 추출합니다.

```python
subj = term.get("subject_meaning", "")
example = term.get("example", "")
return True, subj, example
```

이 값은 최종 응답 문장으로 활용됩니다. 예를 들어 수학 용어의 뜻과 간단한 예시를 함께 말해주면, 사용자는 단순 용어 의미를 넘어 실제 개념까지 이해할 수 있습니다.

결론적으로 `math.json`은 프로젝트의 지식 저장소 역할을 담당합니다.

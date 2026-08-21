
수학 용어가 매칭되든, 아니든 최종적으로는 응답 문장이 생성됩니다. 이 단계는 사용자의 질문을 이해한 뒤, 적절한 설명 경로를 선택하고 최종 문장을 만들어내는 핵심 흐름입니다.

프로젝트는 크게 두 가지 경로를 사용합니다.

- 수학 용어가 매칭되면: 해당 의미와 예시를 설명
- 매칭되지 않으면: GPT 기반 일반 응답 생성

`chatgpt_conn.py`는 OpenAI Responses API를 호출해 사용자 질문에 대한 자연어 설명을 생성합니다. 이 파일은 단순한 문장 생성기 역할만 하지 않고, 수학 문맥에서 개념을 설명하고 대화 흐름을 유지하는 인터페이스 역할을 합니다.

예를 들면:

- 정의를 간단히 설명하기
- 계산 과정을 설명하기
- 다른 표현으로 설명하기
- 왜 그렇게 계산되는지 설명하기

이런 기능은 초보 학습자에게 매우 유용합니다.

```python
response = client.responses.create(
    model="gpt-4o-mini",
    input=user_message,
)
return response.output_text
```

이 함수는 사용자 발화와 필요한 문맥을 전달해 응답을 생성하며, 결과 텍스트는 최종적으로 TTS로 변환됩니다.

한편, 이 프로젝트는 `MCPServerStdio`를 사용해 파일 시스템에 접근합니다. 이를 통해 `math_json/math.json` 같은 내부 데이터를 읽고, 응답을 더 정확하게 보완할 수 있습니다.

```python
async with MCPServerStdio(
    name="Filesystem Server",
    params={
        "command": "cmd",
        "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", samples_dir],
    },
) as server:
```

이 설정은 에이전트가 프로젝트 루트 디렉터리 안의 파일들을 읽고, 필요한 정보를 응답 생성에 반영할 수 있게 해 줍니다. 즉, MCP는 단순한 도구 연결이 아니라, 파일 기반 지식을 탐색하고 응답에 반영할 수 있도록 돕는 인터페이스입니다.

결론적으로 AI 응답 단계는 다음 흐름으로 동작합니다.

1. 정규화된 문장을 받아 수학 용어 매칭 여부를 확인한다.
2. 매칭되면 사전 기반 설명을 구성한다.
3. 매칭되지 않으면 OpenAI Responses API로 일반 답변을 생성한다.
4. 필요하면 MCP로 파일 기반 정보를 읽어 컨텍스트를 보강한다.
5. 최종 결과를 텍스트로 반환하고, 다음 단계인 TTS로 전달한다.

사용자가 듣는 최종 문장은 이 단계에서 완성되며, 그 다음 TTS로 전환됩니다.

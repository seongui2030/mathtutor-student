## 08-2. MCP 파일 접근

이 프로젝트는 `MCPServerStdio`를 사용해 파일 시스템에 접근합니다.

```python
async with MCPServerStdio(
    name="Filesystem Server",
    params={
        "command": "cmd",
        "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", samples_dir],
    },
) as server:
```

이 설정은 프로젝트 루트 디렉터리 내의 파일들을 에이전트가 읽을 수 있게 만듭니다. 특히 `math_json/math.json` 같은 데이터 파일을 안전하게 활용할 수 있도록 해 줍니다.

즉, MCP는 단순한 도구 연결이 아니라, 에이전트가 파일 기반 지식을 탐색하고 응답에 반영할 수 있도록 돕는 인터페이스입니다. 특히 수학 사전이나 응답 보강에 필요한 문맥을 읽어와서 더 정교한 설명을 생성하는 데 활용됩니다.

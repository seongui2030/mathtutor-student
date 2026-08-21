
`total_mic_speak_mcp.py`는 전체 서비스의 진입점입니다.

파일 하단의 다음 코드가 실행을 시작합니다.

```python
if __name__ == "__main__":
    if not shutil.which("npx"):
        raise RuntimeError("npx is not installed. Please install it with `npm install -g npx`.")
    main()
```

이 부분은 `npx`가 설치되어 있는지 먼저 확인합니다. 만약 `npx`가 없다면 MCP 파일시스템 서버가 동작하지 않기 때문에 프로젝트가 실행되지 않습니다.

`npx`가 있으면 `main()` 함수로 넘어가 실제 음성 처리 흐름이 시작됩니다.

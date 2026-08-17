# 11-1. npx 설치 문제

프로젝트 실행 시 `npx is not installed` 오류가 발생하면 MCP 서버가 동작할 수 없습니다.

해결 방법:

```bash
npm install -g npx
```

또는 Node.js를 다시 설치한 뒤 `npx --version`으로 확인합니다.

MCP 파일시스템 서버는 Node 기반 도구이므로, 이 단계가 없으면 프로젝트가 시작되지 않습니다.

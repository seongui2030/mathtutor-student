# 11-2. OPENAI_API_KEY 문제

API 키가 없거나 잘못 설정되면 OpenAI 호출이 실패합니다.

해결 방법:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

또는 PowerShell에서:

```powershell
$env:OPENAI_API_KEY = "your_api_key"
```

보통 `.env` 파일을 루트에 두면 자동으로 로드됩니다.

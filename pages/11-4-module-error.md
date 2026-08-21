
실행 중 `ModuleNotFoundError` 또는 import 오류가 발생하면 Python 의존성을 다시 설치해야 합니다.

```bash
pip install --upgrade -r requirements.txt
```

특히 다음 패키지는 자주 영향을 받습니다.

- `openai`
- `sounddevice`
- `scipy`
- `pygame`
- `python-dotenv`

설치가 제대로 되어 있지 않으면 음성 처리 전체가 동작하지 않습니다.

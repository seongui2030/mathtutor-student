# 02-3. 의존성 설치

프로젝트 루트에서 가상환경을 만들고, 필요한 패키지를 설치합니다.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

설치되는 주요 라이브러리는 다음과 같습니다.

- openai
- python-dotenv
- sounddevice
- scipy
- pygame
- agents
- pydantic

`requirements.txt`에는 OpenAI API 통신, 음성 녹음, 오디오 저장, 음성 재생, 환경변수 로딩과 같은 기능이 포함됩니다.

설치가 끝난 뒤에는 기본 프로젝트 파일들이 준비되었는지 확인하고 실행 단계로 넘어갑니다.

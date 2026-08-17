##12. 프로젝트 구조

이 프로젝트는 음성 입력, STT, 정규화, 수학 매칭, TTS, 재생이 모두 하나의 흐름 안에서 연결되는 구조를 가집니다.

주요 요소는 다음과 같습니다.

- 메인 실행 스크립트: `total_mic_speak_mcp.py`
- 오디오 처리 모듈: `voice.py`
- GPT 연결 모듈: `chatgpt_conn.py`
- 수학 사전: `math_json/math.json`
- 의존성 파일: `requirements.txt`

이 구조는 기능별 분리와 전체 파이프라인 통합을 동시에 만족하도록 설계되어 있습니다.

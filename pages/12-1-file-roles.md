# 12-1. 파일별 역할

- `total_mic_speak_mcp.py`: 최상위 실행 파일. 음성 입력과 응답 흐름을 제어한다.
- `voice.py`: 녹음, STT, TTS, MP3 재생을 담당한다.
- `chatgpt_conn.py`: OpenAI 응답 API 호출을 처리한다.
- `transcribe_conn.py`: 오디오 인식 관련 로직을 분리해 둔다.
- `tts_conn.py`: 음성 합성 로직을 분리해 둔다.
- `math_json/math.json`: 수학 개념 및 예시 데이터 저장소다.

이런 구조로 인해 코드를 각 기능별로 이해하기 쉽고 유지보수도 편리합니다.

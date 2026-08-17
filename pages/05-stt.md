# 05. 음성 인식(STT)

STT 단계는 녹음 파일을 사용자 말의 텍스트 표현으로 변환하는 핵심 과정입니다.

이 프로젝트는 `voice.py`의 `call_transcribe()`를 통해 OpenAI API의 음성 인식 기능을 사용합니다. 결과는 문자열 형태로 반환되며, 이후 `normalize_dialect()`로 향합니다.

핵심은 다음과 같습니다.

- 마이크 녹음 파일 읽기
- OpenAI `audio.transcriptions.create()` 호출
- 텍스트 추출
- 정규화 입력 준비

결과적으로 사용자가 말한 문장이 컴퓨터가 이해할 수 있는 문장으로 바뀌게 됩니다.

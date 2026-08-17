# 05-1. 변환 로직

`call_transcribe()`는 음성 파일을 `OpenAI`에 전달하고, 그 결과를 문자열로 반환합니다.

이 과정은 실제로 다음 순서로 진행됩니다.

1. 환경 변수에서 API 키를 읽는다.
2. WAV 파일을 바이너리로 연다.
3. `client.audio.transcriptions.create()`를 호출한다.
4. `response_format="text"`로 plain text를 받는다.
5. 반환 텍스트를 다음 단계로 전달한다.

이후 코드에서는 `transcript`를 `normalize_dialect()`에 전달합니다.

즉, 오디오 입력에서 언어 처리로 넘어가는 데이터 경계가 이 단계에서 형성됩니다.

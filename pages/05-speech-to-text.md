
STT 단계는 녹음된 음성을 사용자가 말한 내용의 텍스트 표현으로 바꾸는 핵심 과정입니다. 이 프로젝트에서는 `voice.py`의 `call_transcribe()`를 통해 OpenAI의 음성 인식 API를 호출합니다.

이 단계는 단순한 파일 변환이 아니라, 이후 정규화와 수학 용어 매칭, AI 응답 생성이 가능하도록 입력 데이터를 준비하는 연결 고리 역할을 합니다. 말한 내용을 정확하게 받아서 컴퓨터가 이해할 수 있는 문장으로 만들기 위한 첫 번째 필수 절차입니다.

```python
def call_transcribe(audio_path):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=f,
            response_format="text"
        )
    return transcript
```

이 함수는 WAV 파일을 바이너리로 열어 OpenAI의 transcription API에 전달하고, 텍스트 결과를 반환합니다. 실제 동작 순서는 다음과 같습니다.

1. 마이크로 녹음된 오디오 파일을 읽는다.
2. OpenAI `audio.transcriptions.create()`를 호출한다.
3. Whisper 기반 모델이 음성을 텍스트로 변환한다.
4. 변환된 문자열을 반환한다.
5. 반환된 텍스트는 이후 `normalize_dialect()`로 전달된다.

핵심은 다음과 같습니다.

- 입력: WAV 파일
- 출력: 문자열 텍스트
- 목적: 수학 질문을 이해할 수 있는 형태로 변환

결과적으로 사용자가 말한 문장이 컴퓨터가 이해할 수 있는 문장으로 바뀌고, 이 텍스트는 사투리 정규화, 용어 매칭, AI 응답 생성으로 이어집니다. 즉, STT 단계는 전체 음성 기반 수학 도우미의 시작점이자 가장 중요한 전처리 단계입니다.

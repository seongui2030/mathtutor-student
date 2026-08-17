## 05. 음성 인식(STT)

녹음된 파일은 `voice.py`의 `call_transcribe()`를 통해 텍스트로 변환됩니다.

이 단계는 말한 내용을 정확히 받아서 수학용어 정규화와 AI 설명의 입력으로 만들기 위한 핵심 단계입니다.

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

이 함수는 OpenAI의 transcription API를 호출해 음성을 텍스트로 변환합니다.

- 입력: WAV 파일
- 출력: 문자열 텍스트
- 목적: 수학 질문을 이해할 수 있는 형태로 변환

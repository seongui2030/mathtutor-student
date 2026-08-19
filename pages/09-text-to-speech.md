## 09. 텍스트 음성 변환(TTS)

- 최종 답변은 `voice.py`의 `call_tts()`를 통해 음성으로 변환됩니다.

- 이 함수는 OpenAI TTS API를 호출하고, 생성된 음성을 MP3 파일로 저장합니다. 이후 `play_mp3()`가 재생을 담당합니다.

```python
def call_tts(text):
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="nova",
        input=text
    )
    return response
```

- 이 단계는 사용자가 듣기 편한 형태로 결과를 전달하는 최종 단계입니다.

# 05-1. 오디오 파일 변환

`call_transcribe(audio_path)`는 다음 흐름으로 동작합니다.

```python
with open(audio_path, "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model=model_name,
        file=audio_file,
    )
return transcript.text
```

이 과정에서 파일은 바이너리로 열리고, 오디오 전용 API에 전달됩니다. 모델은 Whisper 계열을 사용하며, 최종 결과는 `transcript.text` 문자열로 받습니다.

이 문자열을 `main()`에서 바로 활용하므로, 전체 프로그램 흐름에서 매우 중요한 연결 지점입니다.

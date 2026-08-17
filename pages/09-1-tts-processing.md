##09-1. 텍스트를 음성으로 변환

`call_tts()`는 다음 구조로 동작합니다.

```python
with client.audio.speech.with_streaming_response.create(
    model=model_name,
    voice="alloy",
    input=input_text,
) as response:
    response.stream_to_file(speech_file_path)
```

이 코드는 응답 문장 전체를 실시간으로 스트리밍하며 MP3 파일로 출력합니다. 결과적으로 사용자는 이해하기 쉬운 음성 형태로 결과를 들을 수 있습니다.

TTS는 프로젝트의 마지막 사용자 인터페이스 단계로서 매우 중요합니다.

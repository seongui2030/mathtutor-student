# 04-2. WAV 저장

녹음이 끝나면 `write(audio_path, sample_rate, audio)`에 의해 WAV 파일이 저장됩니다.

프로젝트에서는 보통 다음 경로로 저장합니다.

```python
audio_path = Path(__file__).parent / "speech_transcribe.wav"
```

이 파일은 이후 STT 단계에서 사용됩니다. 즉, 마이크 입력을 파일로 남겨두는 이유는 음성 인식 엔진이 파일 기반 입력을 더 안정적으로 처리할 수 있기 때문입니다.

- 입력: 마이크 녹음
- 저장 형식: WAV
- 사용 목적: OpenAI Whisper로 텍스트 변환

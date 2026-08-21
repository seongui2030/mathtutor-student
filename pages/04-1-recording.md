
`record_audio_to_wav()` 함수는 다음 과정을 실행합니다.

```python
def record_audio_to_wav(audio_path: Path, duration: int = 10, sample_rate: int = 16000):
    print("5초간 말해주세요.")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    write(audio_path, sample_rate, audio)
    print("녹음 완료")
```

여기서 핵심은 다음입니다.

- `sd.rec()`로 마이크 입력을 바로 녹음한다.
- `duration` 값으로 녹음 시간을 설정한다.
- `sample_rate`는 16000Hz로 고정한다.
- `write()`를 통해 WAV 파일로 저장한다.

기본 설정은 학생이 질문을 말하는 시간을 확보하는 데 적합하게 구성되어 있습니다.

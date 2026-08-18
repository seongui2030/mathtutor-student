## 05-1. 오디오 파일 변환

`call_transcribe()`는 음성 파일을 `OpenAI`로 전달하고, 그 결과를 문자열로 반환하는 핵심 단계입니다. 이 과정은 실제로 다음 순서로 진행됩니다.

1. 환경 변수에서 API 키를 읽는다.
2. WAV 파일을 바이너리로 연다.
3. `client.audio.transcriptions.create()`를 호출한다.
4. Whisper 모델이 오디오를 텍스트로 변환한다.
5. 최종 결과를 문자열 형태로 반환한다.
6. 반환 텍스트를 다음 단계인 정규화 로직으로 전달한다.

실제 구현은 다음과 같은 흐름으로 동작합니다.

```python
with open(audio_path, "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model=model_name,
        file=audio_file,
    )
return transcript.text
```

이 과정에서 파일은 바이너리로 열리고, 오디오 전용 API에 전달됩니다. 모델은 Whisper 계열을 사용하며, 최종 결과는 `transcript.text` 문자열로 받습니다.

이 문자열은 `main()`에서 바로 활용되며, 이후 `normalize_dialect()`에 전달되어 사투리 및 방언 정규화를 거칩니다. 즉, 오디오 입력에서 언어 처리로 넘어가는 데이터 경계가 이 단계에서 형성됩니다.

결국 이 단계는 단순한 변환이 아니라, 녹음된 음성 데이터를 프로그램이 이해 가능한 텍스트로 바꾸는 첫 번째 핵심 연결 고리입니다. 전체 프로그램 흐름에서 매우 중요한 위치를 차지합니다.

##10-1. pygame 재생

```python
def play_mp3(file_path: str):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception:
        traceback.print_exc()
```

이 코드는 생성된 MP3 음성을 재생하고, 재생이 끝날 때까지 대기합니다. 즉, 사용자에게 답변 음성이 끝날 때까지 자연스럽게 이어지는 동작을 수행합니다.

오디오 재생은 프로젝트에서 결과를 최종적으로 전달하는 단계이므로 중요합니다.

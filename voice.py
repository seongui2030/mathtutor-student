from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import sounddevice as sd
from scipy.io.wavfile import write
import pygame
import time
import re
import traceback
from chatgpt_conn import call_chatgpt

load_dotenv()

##Lazy OpenAI client
_client = None

def get_client():
    global _client
    if _client is None:
        _client = OpenAI()
    return _client


def record_audio_to_wav(audio_path: Path, duration: int = 5, sample_rate: int = 16000):
    print(f"녹음 시작 ({duration}s)...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    write(audio_path, sample_rate, audio)
    print("녹음 완료")


def play_mp3(file_path: str):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception:
        traceback.print_exc()


def call_transcribe(audio_path: str, model_name: str = "gpt-4o-mini-transcribe") -> str:
    client = get_client()
    try:
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model=model_name,
                file=audio_file,
            )
        return transcript.text
    except Exception as e:
        print(f"[ERROR] Transcribe failed: {e}")
        traceback.print_exc()
        return ""


def call_tts(speech_file_path: Path, input_text: str, model_name: str = "gpt-4o-mini-tts") -> None:
    client = get_client()
    try:
        with client.audio.speech.with_streaming_response.create(
            model=model_name,
            voice="alloy",
            input=input_text,
        ) as response:
            response.stream_to_file(speech_file_path)
    except Exception as e:
        print(f"[ERROR] TTS failed: {e}")
        traceback.print_exc()


def normalize_dialect(text: str, use_llm: bool = True) -> str:
    """Normalize common Gyeongsang (경상도) dialect to standard Korean.

    Steps:
    1. Apply small rule-based replacements for frequent patterns.
    2. Optionally call LLM (`call_chatgpt`) to refine the result.
    """
    if not text:
        return text

    rules = {
        "하지 마이소": "하지 마세요",
        "하지 마소": "하지 마세요",
        "밥 묵어라": "밥 먹어라",
        "밥 묵어": "밥 먹어",
        "묵어라": "먹어라",
        "묵어": "먹어",
        "안 하이소": "안 하세요",
        "안 하소": "안 하세요",
        "마이": "많이",
    }

    s = text
    for k, v in rules.items():
        s = s.replace(k, v)

    # If desired, refine using an LLM prompt for more natural standardization
    if use_llm:
        try:
            prompt = (
                "다음 문장은 경상도(영남) 사투리 표현을 포함할 수 있습니다.\n"
                "자연스러운 표준 한국어(평서문)로 변환해 주세요. 출력은 변환된 문장만 하세요.\n\n"
                f"입력: {s}"
            )
            refined = call_chatgpt(prompt)
            if refined and isinstance(refined, str) and refined.strip():
                return refined.strip()
        except Exception:
            traceback.print_exc()

    return s

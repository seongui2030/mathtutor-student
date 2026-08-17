from openai import OpenAI
from dotenv import load_dotenv

# Lazy client initialization to allow callers to load .env first
_client = None

def get_client():
    global _client
    if _client is None:
        load_dotenv()
        _client = OpenAI()
    return _client


# API연결하는 함수를 만듬. 입력값은 오디오 파일 경로, 모델명은 gpt-4o-mini-transcribe
def call_transcribe(audio_path: str, model_name: str = "gpt-4o-mini-transcribe") -> str:
    client = get_client()
    try:
        audio_file = open(audio_path, "rb")
        transcript = client.audio.transcriptions.create(
            model=model_name,
            file=audio_file,
        )
        return transcript.text

    except Exception as e:
        print(f"[ERROR] ChatGPT 호출 중 예외 발생: {e}")
        return "오류가 발생했습니다."

if __name__ == "__main__":
    audio_path = "speech_transcribe.mp3"
    output_text = call_transcribe(audio_path)
    print("요청:", audio_path)
    print("응답:", output_text)

from pathlib import Path
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


# API연결하는 함수를 만듬. 입력값은 오디오 파일 경로, 입력 텍스트, 모델명은 gpt-4o-mini-tts
def call_tts(speech_file_path: str, input_text: str, model_name: str = "gpt-4o-mini-tts") -> str:
    client = get_client()
    try:
        with client.audio.speech.with_streaming_response.create(
            model=model_name,
            voice="alloy",
            input=input_text,
        ) as response:
            response.stream_to_file(speech_file_path)

    except Exception as e:
        print(f"[ERROR] ChatGPT 호출 중 예외 발생: {e}")
        return "오류가 발생했습니다."

if __name__ == "__main__":
    speech_file_path = Path(__file__).parent / "speech_tts.mp3"
    input_text = "소년은 늙기 쉽고 배움은 이루기 어려우니 아주 짧은 시간도 가볍게 여기지 말라. 하지만 이 말은 너를 몰아붙이라는 뜻이 아니야. 오늘 조금 배웠다면 그것으로 충분하고 오늘 지쳤다면 잘 쉬는 것도 배움을 이어가는 방법이야. 내일 다시 시작할 힘을 모으는 시간이니까."
    call_tts(speech_file_path, input_text)
    print("요청:", input_text)
    print("응답:", speech_file_path)

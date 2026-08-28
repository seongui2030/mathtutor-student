import asyncio
import os
import shutil
import time
import traceback
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerStdio

import pygame
import sounddevice as sd
from scipy.io.wavfile import write


load_dotenv()

client = OpenAI()

# webtoon_voice_agent19.py의 음성 입출력 설정을 사용합니다.
BASE_DIR = Path(__file__).parent
AUDIO_PATH = BASE_DIR / "audio" / "speech_transcribe.wav"
SPEECH_PATH = BASE_DIR / "audio" / "speech_tts.mp3"
MATH_JSON_PATH = BASE_DIR / "math_json" / "math.json"

RECORD_SECONDS = 5
SAMPLE_RATE = 16000
STT_MODEL = "gpt-4o-mini-transcribe"
TTS_MODEL = "gpt-4o-mini-tts"
TTS_VOICE = "alloy"
AGENT_MODEL = "gpt-4.1"
NORMALIZE_MODEL = "gpt-4o-mini"
MCP_ERROR_TEXT = "math.json 파일을 읽을 수 없습니다."


# ── 1단계: 마이크 녹음 ─────────────────────────────────────────
def record_audio_to_wav(audio_path: Path,
                        duration: int = RECORD_SECONDS,
                        sample_rate: int = SAMPLE_RATE) -> None:
    audio_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"{duration}초간 수학 질문을 말해주세요.")
    audio = sd.rec(int(duration * sample_rate),
                   samplerate=sample_rate,
                   channels=1,
                   dtype="int16")
    sd.wait()
    write(audio_path, sample_rate, audio)
    print("녹음 완료")


# ── 2단계: 음성 → 텍스트 ───────────────────────────────────────
def call_transcribe(audio_path: Path, model_name: str = STT_MODEL) -> str:
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model=model_name,
            file=audio_file,
        )
    return transcript.text


def normalize_dialect(input_text: str,
                      model_name: str = NORMALIZE_MODEL) -> str:
    """사투리나 구햣어체 질문을 math.json 검색에 적합한 표준어로 바꿉니다."""
    text = input_text.strip()
    if not text:
        return text

    try:
        response = client.responses.create(
            model=model_name,
            instructions=(
                "사용자의 수학 질문을 표준 한국어 검색어로 정규화하세요. "
                "경상도 등 지역 사투리와 구어체만 자연스러운 표준어로 바꾸고, "
                "수학 용어와 질문의 의미는 유지하세요. "
                "예: '항등식이 뭔데', '항등식이 뭐꼬', '항등식이 뭐야', "
                "'항등식이 뭐라카노'는 모두 '항등식이 무엇인가요?'로 바꿉니다. "
                "설명하지 말고 정규화된 질문 한 문장만 출력하세요."
            ),
            input=text,
        )
        normalized = response.output_text.strip()
        return normalized or text
    except Exception as e:
        # 정규화 API가 일시적으로 실패해도 원문으로 MCP 검색을 계속합니다.
        print(f"방언 정규화 오류: {e}")
        return text


# ── 3단계: MCP filesystem을 사용하는 수학 에이전트 ───────────────
async def run(mcp_server: MCPServer,
              input_text: str,
              model_name: str = AGENT_MODEL) -> str:
    agent = Agent(
        name="Math Assistant",
        model=model_name,
        instructions=(
            "당신은 수학 학습 도우미입니다. 모든 질문에 답하기 전에 반드시 "
            "filesystem 도구로 math_json/math.json 파일을 읽으세요. "
            "이 파일이 수학 지식의 원본이며, filesystem을 사용하는 것이 핵심입니다. "
            "사용자 질문에 포함된 수학 용어를 math.json의 word와 비교하세요. "
            "일치하는 용어가 있으면 해당 항목의 word, hantja, original_meaning, "
            "subject_meaning, example 필드를 읽으세요. "
            "단, 최종 답변에는 다음 형식만 사용하세요:\n"
            "질문은 [word의 괄호 앞 용어]\n"
            "[subject_meaning]\n"
            "예시: [example]\n"
            "hantja와 original_meaning은 내부 자료 확인에 사용하되 최종 답변에는 출력하지 마세요. "
            "고등학생이 이해할 수 있도록 subject_meaning과 example을 자연스러운 한국어로 읽어 주세요. "
            "일치하는 용어가 없으면 반드시 'math.json 파일에 해당 질문이 없습니다.'라고만 답하세요. "
            "답변은 한국어 문장으로, 마크다운·URL·이모지 없이 300자 이내로 하세요. "
            "파일 경로는 비어 있지 않게 하고 프로젝트 루트 기준으로 사용하세요."
        ),
        mcp_servers=[mcp_server],
    )

    print(f"Running: {input_text}")
    try:
        result = await Runner.run(starting_agent=agent, input=input_text)
        return result.final_output
    except Exception:
        print("[ERROR] Runner.run raised an exception:")
        traceback.print_exc()
        raise


async def main_mcp(input_text: str) -> str:
    current_dir = BASE_DIR.resolve()
    if not MATH_JSON_PATH.is_file():
        raise FileNotFoundError(f"필수 파일을 찾을 수 없습니다: {MATH_JSON_PATH}")

    # 프로젝트 루트를 제공해야 MCP가 math_json/math.json을 읽을 수 있습니다.
    samples_dir = str(current_dir)
    print(f"Serving filesystem directory for MCP server: {samples_dir}")

    async with MCPServerStdio(
        name="Filesystem Server",
        params={
            "command": "cmd",
            "args": [
                "/c", "npx", "-y",
                "@modelcontextprotocol/server-filesystem", samples_dir,
            ],
        },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="Math Voice MCP Agent", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
            return await run(server, input_text)


# ── 4단계: 텍스트 → 음성 ───────────────────────────────────────
def call_tts(speech_file_path: Path, input_text: str,
             model_name: str = TTS_MODEL) -> None:
    speech_file_path.parent.mkdir(parents=True, exist_ok=True)

    with client.audio.speech.with_streaming_response.create(
        model=model_name,
        voice=TTS_VOICE,
        input=input_text,
    ) as response:
        response.stream_to_file(speech_file_path)


def text_for_speech(output_text: str) -> str:
    """질문 문장을 자연스럽게 바꾸고 예시는 TTS에서 제외합니다."""
    speech_lines = []
    term = ""
    for line in output_text.splitlines():
        stripped_line = line.strip()
        if stripped_line.startswith(("예시:", "예를 들어")):
            continue
        if stripped_line.startswith("질문은 "):
            term = stripped_line[len("질문은 "):].strip()
            line = f"{term}은"
        elif term and stripped_line.startswith((f"{term}은", f"{term}는")):
            # 첫 줄에서 이미 "항등식은"을 읽으므로 의미 문장의 중복 표현을 제거합니다.
            line = stripped_line[len(term) + 1:].lstrip()
        speech_lines.append(line)
    return "\n".join(speech_lines).strip()


# ── 5단계: 스피커 재생 ─────────────────────────────────────────
def play_mp3(file_path: Path) -> None:
    pygame.mixer.init()
    pygame.mixer.music.load(str(file_path))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.music.unload()
    pygame.mixer.quit()


# ── 전체 흐름 ─────────────────────────────────────────────────
def main() -> None:
    try:
        record_audio_to_wav(AUDIO_PATH)

        input_text = call_transcribe(AUDIO_PATH).strip()
        if not input_text:
            print("인식된 음성이 없습니다. 다시 시도해 주세요.")
            return
        print("요청:", input_text)

        normalized_text = normalize_dialect(input_text)
        print("정규화된 질문:", normalized_text)

        # 정규화된 질문을 MCP filesystem에 전달하여 math.json을 읽어 처리합니다.
        try:
            output_text = asyncio.run(main_mcp(normalized_text))
        except Exception as e:
            print(f"MCP 처리 오류: {e}")
            traceback.print_exc()
            output_text = MCP_ERROR_TEXT
        print("응답:", output_text)

        call_tts(SPEECH_PATH, text_for_speech(output_text))
        print("응답 음성 재생")
        play_mp3(SPEECH_PATH)

    except Exception as e:
        print(f"오류 발생: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    if not shutil.which("npx"):
        raise RuntimeError(
            "npx가 설치되어 있지 않습니다. `npm install -g npx`로 설치하세요."
        )
    main()

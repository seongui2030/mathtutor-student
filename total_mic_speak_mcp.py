from dotenv import load_dotenv         # .env 파일을 읽어 환경변수로 설정
from pathlib import Path
from chatgpt_conn import call_chatgpt
from voice import record_audio_to_wav, call_transcribe, call_tts, play_mp3, normalize_dialect
import sounddevice as sd
from scipy.io.wavfile import write
import asyncio
import os
import shutil
from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerStdio
import pygame
import time
import traceback
import re
import json

load_dotenv()  # .env 파일을 읽어 환경변수로 설정


async def run(mcp_server: MCPServer, input_text: str, model_name: str = "gpt-5.6-luna"):
    agent = Agent(
        name="Assistant",
        model=model_name,
        instructions="""Use the filesystem tools to answer questions based on the files inside the directory. 
Do not attempt to read from an empty path (""). 
If the user request is general, first look for relevant files inside the directory. 
Always resolve file paths relative to the directory and ensure the path is valid before reading.""",
        mcp_servers=[mcp_server],
    )

    # 인자로 받은 input_text를 agent에 전달.
    message = input_text
    print(f"Running: {message}")
    try:
        result = await Runner.run(starting_agent=agent, input=message)
        return result.final_output
    except Exception as e:
        print("[ERROR] Runner.run raised an exception:")
        traceback.print_exc()
        # propagate so caller can also handle
        raise


async def main_mcp(input_text: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 파일 시스템 접근 대상 폴더를 워크스페이스 루트로 설정하여
    # math_json/math.json 등 저장된 파일들이 MCP 파일시스템을 통해 접근 가능하도록 함
    samples_dir = current_dir  # serve repository root so math.json is accessible
    if not os.path.isdir(samples_dir):
        raise RuntimeError(f"Samples directory not found: {samples_dir}")
    print(f"Serving filesystem directory for MCP server: {samples_dir}")
    async with MCPServerStdio(
        name="Filesystem Server",
        params={
            "command": "cmd",
            "args": ["/c","npx","-y", "@modelcontextprotocol/server-filesystem", samples_dir],
        },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="MCP Filesystem Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
            # agent에게 input_text를 인자로 전달해주고, MCP 서버의 기능을 사용한 후 agent가 응답하는 내용을 output_text로 저장
            try:
                output_text = await run(server, input_text)
            except Exception as e:
                print("[ERROR] main_mcp caught exception while running agent:")
                traceback.print_exc()
                output_text = f"오류 발생: {e}"

    return output_text


def record_audio_to_wav(audio_path: Path, duration: int = 10, sample_rate: int = 16000):
    print("5초간 말해주세요.")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    write(audio_path, sample_rate, audio)
    print("녹음 완료")


def main():
    audio_path = Path(__file__).parent / "speech_transcribe.wav"
    speech_file_path = Path(__file__).parent / "speech_tts.mp3"

    record_audio_to_wav(audio_path)

    try:
        input_text = call_transcribe(str(audio_path))
        input_text = input_text.strip()
        print("원문(STT):", input_text)

        # 경상도 억양/사투리 정규화
        normalized_text = normalize_dialect(input_text, use_llm=True)
        print("정규화된 텍스트:", normalized_text)

        # 후속 처리에서는 정규화된 텍스트를 사용
        input_for_processing = normalized_text

        # input_guardrail: if the question matches a 'word' in math.json,
        # speak the 'subject_meaning' and print the 'example'. Otherwise,
        # speak the fallback message.
        def input_guardrail(query: str):
            try:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                math_path = os.path.join(current_dir, "math_json", "math.json")
                with open(math_path, "r", encoding="utf-8") as jf:
                    math_data = json.load(jf)

                q = query.strip()
                for unit in math_data.get("data", []):
                    for term in unit.get("terms", []):
                        word = term.get("word", "")
                        if not word:
                            continue
                        base_word = re.sub(r"\s*\(.*?\)\s*", "", word)
                        if base_word and base_word in q:
                            subj = term.get("subject_meaning", "")
                            example = term.get("example", "")
                            return True, subj, example

                return False, "파일에서 확인되지 않아 정확한 의미를 알 수 없습니다", None
            except Exception:
                traceback.print_exc()
                return False, "오류가 발생했습니다.", None

        matched, out_text, example = input_guardrail(input_for_processing)

        if matched:
            output_text = out_text
            print("응답:", output_text)
            call_tts(speech_file_path, output_text)
            print("응답 음성 재생")
            play_mp3(str(speech_file_path))
            if example:
                print("\nexample:", example)
        else:
            # not matched: speak fallback message
            output_text = out_text
            print("응답:", output_text)
            call_tts(speech_file_path, output_text)
            print("응답 음성 재생")
            play_mp3(str(speech_file_path))

    except Exception as e:
        print(f"오류 발생: {e}")
        return None, None
    
    return


if __name__ == "__main__":
    if not shutil.which("npx"):
        raise RuntimeError("npx is not installed. Please install it with `npm install -g npx`.")
    main()

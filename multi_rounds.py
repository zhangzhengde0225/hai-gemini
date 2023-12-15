"""
调用Gemini进行多轮对话，国内需要代理。
"""

from dataclasses import dataclass
from HaiGemini.gemini import Gemini
import hai

def run(gemini):

    messages = []
    turns = 1
    while True:
        question = input(f"[{turns}]User: ")
        if question.lower() in ["quit", "exit", "q", "e"]:
            break
        print(f"[{turns}]Gemini: ")
        messages.append({"role": "user", "content": question})
        response = gemini.generate(messages=messages)
        condaidates = response["candidates"]
        anwser = condaidates[0]['content']['parts'][0]['text']
        print(anwser)
        messages.append({"role": "assistant", "content": anwser})
        turns += 1


@dataclass
class Args:
    proxy: str = "http://localhost:8118"

if __name__ == "__main__":
    args = hai.parse_args_into_dataclasses(Args)
    gemini = Gemini(proxy=args.proxy, engine="gemini-pro")
    run(gemini=gemini)
    

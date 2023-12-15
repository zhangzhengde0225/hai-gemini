"""
单轮问答，国内需要代理
"""

from dataclasses import dataclass
from HaiGemini.gemini import Gemini
import hai

def run(gemini, question):
    print(f'Qustion: {question}')
    print(f'Answer:')

    response = gemini.generate(
        messages=[
            {"role": "user", "content": question},
            # {"role": "assistant", "content": "<model answer>"},  # 可以添加多个对话  
            # {"role": "user", "content": "<quesion2>"},
            ]
        )
    # print(f'response: {response}')    
    question_safety_ratings= response["promptFeedback"]["safetyRatings"]
    condaidates = response["candidates"]
    anwser = condaidates[0]['content']['parts'][0]['text']
    finish_reason = condaidates[0]['finishReason']  # STOP
    answer_safety_ratings = condaidates[0]['safetyRatings']

    print(anwser)

@dataclass
class Args:
    q: str = "写一段快读排序算法"  # 问题
    proxy: str = "http://localhost:8118"

if __name__ == "__main__":
    args = hai.parse_args_into_dataclasses(Args)
    gemini = Gemini(proxy=args.proxy, engine="gemini-pro")
    run(gemini=gemini, question=args.q)
    

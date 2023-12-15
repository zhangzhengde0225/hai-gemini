"""
通过HepAI平台请求Gemini，需要HepAI平台的API_KEY，无需代理
"""


import os, sys
import ast
import hai
hai.api_key = os.environ.get('HEPAI_API_KEY', None)

def request_model(prompt='hello', system_prompt=None):

    result = hai.LLM.chat(
            model='google/gemini',
            messages=[
                {"role": "user", "content": prompt},
                ## 如果有多轮对话，可以继续添加，"role": "assistant", "content": "Hello there! How may I assist you today?"
                ## 如果有多轮对话，可以继续添加，"role": "user", "content": "I want to buy a car."
            ],
            stream=False,
        )

    full_result = ""
    for i in result:
        full_result += i
        # sys.stdout.write(i)
        # sys.stdout.flush()
    # print()
    full_result = ast.literal_eval(full_result)["message"]
    answer = full_result['candidates'][0]['content']['parts'][0]['text']
    return answer

question = 'who are you?'
print(f'Question: {question}\nAnswer: ', end='')
answer = request_model(prompt=question)
print(f'{answer}')

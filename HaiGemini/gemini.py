"""
基于REST API的Gemini客户端
"""


import os
import requests
from dataclasses import dataclass
import hai  # hepai
import json


class SaftySetting:
    """
    安全性设置
    """
    HARM_CATEGORY_HARASSMENT = "BLOCK_MEDIUM_AND_ABOVE"
    HARM_CATEGORY_HATE_SPEECH = "BLOCK_MEDIUM_AND_ABOVE"
    HARM_CATEGORY_SEXUALLY_EXPLICIT = "BLOCK_MEDIUM_AND_ABOVE"
    HARM_CATEGORY_DANGEROUS_CONTENT = "BLOCK_MEDIUM_AND_ABOVE"
    
    # 可选值
    """
    Block none	BLOCK_NONE	Always show regardless of probability of unsafe content
    Block few	BLOCK_ONLY_HIGH	Block when high probability of unsafe content
    Block some	BLOCK_MEDIUM_AND_ABOVE	Block when medium or high probability of unsafe content
    Block most	BLOCK_LOW_AND_ABOVE	Block when low, medium or high probability of unsafe content
    """


    @staticmethod
    def to_list():
        return [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": SaftySetting.HARM_CATEGORY_HARASSMENT
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": SaftySetting.HARM_CATEGORY_HATE_SPEECH
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": SaftySetting.HARM_CATEGORY_SEXUALLY_EXPLICIT
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": SaftySetting.HARM_CATEGORY_DANGEROUS_CONTENT
            }
        ]


class GenerationConfig:
    """生成设置"""
    stopSequences = ["Title"]
    temperature = 1.0
    maxOutputTokens = 800
    topP = 0.8
    topK = 10
    
    @staticmethod   
    def to_dict():
        gc = dict()
        gc["stopSequences"] = GenerationConfig.stopSequences
        gc["temperature"] = GenerationConfig.temperature
        gc["maxOutputTokens"] = GenerationConfig.maxOutputTokens
        gc["topP"] = GenerationConfig.topP
        gc["topK"] = GenerationConfig.topK
        return gc


class Gemini:

    def __init__(self, **kwargs) -> None:
        self.engine = kwargs.get("engine", "gemini-pro")
        self.api_key = kwargs.get("api_key", os.environ.get('GOOGLE_API_KEY', None))
        self.session = requests.Session()
        self.proxy = kwargs.get("proxy", None)
        if self.proxy:
            self.session.proxies = {"http": self.proxy, "https": self.proxy}
        else:
            self.session.proxies = None

    def list_models(self, **kwargs):
        """列出模型
        curl https://generativelanguage.googleapis.com/v1beta/models?key=$API_KEY
        """
        api_key = kwargs.get("api_key", self.api_key)
        assert api_key is not None, "The api_key must be specified, or set the GOOGLE_API_KEY environment variable."
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        response = self.session.get(url, proxies=self.session.proxies)
        print(f'response.text: {response.text}')
        return response.json()
    
    def messages2contents(self, messages):
        """
        多轮对话中：OpenAI格式的Messages转换为Google Gemini格式的Contents
        """
        contents = []
        for message in messages:
            role = message["role"]
            content = message["content"]
            if role == "system":
                continue
            elif role == "user":
                entry={"role": "user",
                        "parts": [{
                            "text": content}]}
                contents.append(entry)
            elif role == "assistant":
                entry={"role": "model",
                        "parts": [{
                            "text": content}]}
                contents.append(entry)
            else:
                raise ValueError(f"Unknown role: {role}")
        return contents


    def generate(self, messages=None, **kwargs):
        api_key = kwargs.get("api_key", self.api_key)  # hepai
        assert api_key is not None, "The api_key must be specified, or set the GOOGLE_API_KEY environment variable."
        stream = kwargs.get("stream", False)
        assert stream is False, "stream is not supported yet."  # TODO: Google Gemini API does not support stream yet.


        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.engine}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": self.messages2contents(messages),
            "safetySettings": SaftySetting.to_list(),
            "generationConfig": GenerationConfig.to_dict(),
            }
    
        response = self.session.post(
            url,
            headers=headers,
            proxies=self.session.proxies,
            data=json.dumps(data),
            stream=stream, 
        )

        if response.encoding is None:
            response.encoding = 'utf-8'
        if response.status_code != 200:
            raise ValueError(f"response.status_code: {response.status_code} {response.text}")

        return response.json()

        # for chunk in response.iter_content(chunk_size=1024):
        #     if chunk:  # 过滤掉保持连接的新的块
        #         # 处理块
        #         chunk = chunk.decode('utf-8')
        #         print(chunk)
        # i = 1
        # while True:
        #     print(f'<{i}> {response.content.decode("utf-8")}')
        #     i += 1
        # for line in response.iter_lines(decode_unicode=True):
        # print(f'response.text: {response.text}')
        # print(response.candidates)
        # for trunk in response:
            # trunk = trunk.decode('utf-8')
            # print(f'trunk: {trunk}')
            # print(f'line: {line}')
            # if line:
            #     json_response = json.loads(line)
            #     if 'text' in json_response:
            #         print(json_response['text'])

        # for line in response.iter_lines():
            # if not line:
                # continue
            # line = line.decode('utf-8')
            # print(f'line: {line}')
            # exit()
            # decoded_line = line.decode('utf-8')

            # print(decoded_line)
            # yield decoded_line

        # print(f'response: {response}')
        # print(f'response.text: {response.text}')
        # pass

@dataclass
class Args:
    proxy: str = "http://127.0.0.1:8118"  # 
    engine: str = "gemini-pro"  # or "gemini-pro-vision"

if __name__ == "__main__":
    args = hai.parse_args_into_dataclasses(Args)

    gemeni = Gemini(proxy=args.proxy, engine=args.engine)
    # models = gemeni.list_models()

    system_prompt = "You are gemini."
    first_question = "写一个快速排序算法，以`写完了`结束"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": first_question},
    ]

    import time
    res = gemeni.generate(messages=messages)
    print(f'res: {res}')
    # for r in res:
    #     print(f'<line> {r}')
    #     time.sleep(1)







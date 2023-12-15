"""
GEMINI Worker
"""

import os, sys
import hai
from hai import BaseWorkerModel
from dataclasses import dataclass, field
from pathlib import Path
here = Path(__file__).parent

try:
    from HaiGemini.gemini import Gemini
except:
    sys.path.append(str(here.parent))
    from HaiGemini.gemini import Gemini


class WorkerModel(BaseWorkerModel):
    def __init__(self, name, **kwargs):
        proxy = kwargs.pop('proxy', None)
        engine = kwargs.pop('engine', None)
        self.name = name  # name属性用于用于请求指定调研的模型
        self.gemini = Gemini(engine=engine, proxy=proxy)

    @BaseWorkerModel.auto_stream  # 自动将各种类型的输出转为流式输
    def inference(self, **kwargs):
        print(f'kwargs: {kwargs}')
        messages = kwargs.pop('messages', None)
        # 自己的执行逻辑, 例如: # 
        response = self.gemini.generate(
            messages=messages,
            **kwargs
            )

        return response

        # for i in output:
        #     yield i  # 可以return返回python的基础类型或yield生成器

def run_worker(**kwargs):
    # worker_args = hai.parse_args_into_dataclasses(WorkerArgs)  # 解析参数
    model_args, worker_args = hai.parse_args_into_dataclasses((ModelArgs, WorkerArgs))  # 解析多个参数类
    # print(worker_args)
    model = WorkerModel(  # 获取模型
        name=model_args.name,
        proxy=model_args.proxy,
        engine=model_args.engine,
        # 此处可以传入其他参数
        )
    
    if worker_args.test:
        ret = model.inference(input='test')
        print(ret)
        return

    hai.worker.start(
        model=model,
        worker_args=worker_args,
        **kwargs
        )

# (1) 实现WorkerModel
@dataclass
class ModelArgs:
    name: str = "google/gemini"  # worker的名称，用于注册到控制器
    proxy: str = "http://localhost:8118"  # 代理
    engine: str = "gemini-pro"  # 模型引擎
    # 其他参数

# (2) worker的参数配置和启动代码
@dataclass
class WorkerArgs:
    host: str = "0.0.0.0"  # worker的地址，0.0.0.0表示外部可访问，127.0.0.1表示只有本机可访问
    port: str = "auto"  # worker的端口，默认从42902开始自动分配
    controller_address: str = "http://aiapi.ihep.ac.cn:42901"  # 控制器的地址
    worker_address: str = "auto"  # 默认是http://<ip>:<port>
    limit_model_concurrency: int = 5  # 限制模型的并发请求
    stream_interval: float = 0.  # 额外的流式响应间隔
    no_register: bool = False  # 不注册到控制器
    permissions: str = 'groups: all'  # 模型的权限授予，分为用户和组，用;分隔，例如：需要授权给所有组、a用户、b用户：'groups: all; users: a, b; owner: c'
    description: str = 'Gemini is the large model of Google released in Dec. 2023'  # 模型的描述
    author: str = 'Google'  # 模型的作者
    test: bool = False  # 测试模式，不会真正启动worker，只会打印参数

if __name__ == '__main__':
    run_worker()
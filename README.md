
# HaiGemini

HepAI-Gemini是基于Google大模型Gemini的适配版本。

## 特性
+ 谷歌官方提供的Python API无法设置代理，本项目通过REST API调用并封装成新的Python API，使得可以设置代理从国内访问。
+ 部署到HepAI平台，可以通过HEPAI API-KEY访问Gemini服务（无需代理）。


## 单轮会话

```bash
python single_qa.py \
    --q "who are you" \
    --proxy "http://localhost:8118"
```
注：请提前启动代理服务，代理为8118端口的http，请自行修改。

## 多轮会话

```bash
python multi_rounds.py \
    --proxy "http://localhost:8118"
```
注：请提前启动代理服务，代理为8118端口的http，请自行修改。

## 通过HepAI平台访问（无需代理）

### 应用程序接口（SDK）：

[通过HepAI平台的请求Gemini模型](https://note.ihep.ac.cn/s/PjFJsEN5i)

### 聊天界面：

访问HepAI平台: [https://ai.ihep.ac.cn](https://ai.ihep.ac.cn)



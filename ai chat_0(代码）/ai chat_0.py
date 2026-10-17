#1.用户输入问题，调用Deepseek API ,打印回答
#2.支持多轮对话（包括历史对话）
#3.输入exit退出，输入clear清空历史
#4.TODO:每次对话记录追加保存到JSON文件

#导入dotenv模块，加载.env文件中的环境变量
from dotenv import load_dotenv
load_dotenv()
#导入os模块和OpenAI类
import os
from openai import OpenAI
#创建OpenAI客户端实例
client = OpenAI(
    api_key=os.environ.get('Deepseek_Api_Key'),#从环境变量读取Api Key
    base_url="https://api.deepseek.com"#DeepSeek API基础地址
)
messages=[{"role":"system","content":"You are an interesting, professional, clear-thinking and rational assistant with sound values."}]#设置system提示词
while True:                                   #无限循环
    user_problem=input()  #用户输入问题
    #当用户输入exit的时候，退出循环
    if user_problem == "exit":
        print("已退出对话")
        break
    #当用户输入clear的时候，清空所有消息
    if user_problem == "clear":
        print("已清空历史记录")
        messages.clear()       
    messages.append(
    {"role":"user","content":user_problem}
    )#把每次的提问都存入消息列表
    response = client.chat.completions.create(
        model="deepseek-flash",#指定使用的模型
        messages=messages,      #消息列表
        stream=False,#是否启用流式输出，False表示一次性返回
        reasoning_effort="high",#推理投入程度，需确认模型是否支持
        extra_body={"thinking":{"type":"enabled"}}#开启思考模式，需确认模型和API是否支持
    )
    #打印AI的回答内容的第一条候选回答
    answer=response.choices[0].message.content
    print(answer)
    messages.append({"role":"assistant","content":answer})#把每次AI的回答存入历史消息列表
# 生成AI
import os
from openai import OpenAI 

# GPTモデルインスタンスを立ち上げる
client = OpenAI()
default_system_prompt = 'あなたは優秀なアシスタントです。日本語で回答してください。'
# プロンプトを与え推論結果を得る関数。もし事前の会話履歴があればmessages変数で与える
def gpt_get_content(prompt,client=client,messages=[],system_prompt=default_system_prompt):
  if messages == []:
    messages = [{"role": "system", "content": system_prompt},]
  messages += [{"role": "user", "content": prompt}]
  response = client.chat.completions.create(
      model = 'gpt-3.5-turbo',
      messages = messages
  )
  messages += [{"role": "assistant", "content":response.choices[0].message.content.strip()}]
  return messages

import json
def get_function_res(function,prompt,messages=[],client=client,system_prompt=default_system_prompt):
  if messages == []:
    messages = [{"role": "system", "content": system_prompt},]
  messages += [{"role": "user", "content": prompt}]
  response = client.chat.completions.create(
      model = 'gpt-3.5-turbo',
      messages = messages,
      functions = [function],
      function_call={"name":function["name"]} #="auto",
  )
  res_json = json.loads(response.choices[0].message.function_call.arguments)
  return res_json




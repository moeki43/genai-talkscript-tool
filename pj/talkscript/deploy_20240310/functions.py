import streamlit as st
import graphviz
import pandas as pd
import string
list_alphabet = list(string.ascii_lowercase)

# 定数定義
USER_NAME = "user"
ASSISTANT_NAME = "assistant"
MORIAGE_YAKU_NAME = "moriage_yaku"

# ユーザーのアバターを設定
avator_img_dict = {
	USER_NAME: "🐵",
	ASSISTANT_NAME: "🤖"
}

SYSTEM_PROMPT = f'''
あなたは優秀なアシスタントです。
営業トークスクリプトを作成するうえで、必要な情報を聞き出すインタビュワーになってください。
以下の必要情報を全て聞き出すまで、インタビューを続けてください。

# 必要情報
- 名前
- 商談の目的
- 顧客に聞きたいこと
'''

def show_past_talk():
    # 以前のチャットログを表示
    for chat in st.session_state.chat_log:
        if chat["role"] != 'system':
            avator = avator_img_dict.get(chat["role"], None)
            with st.chat_message(chat["role"], avatar=avator):
                st.write(chat["content"])

def show_latest_talk(user_msg,assistant_msg):
    # 最新のメッセージを表示
    if user_msg != 'null':
         with st.chat_message(USER_NAME):
              st.write(user_msg)
    if assistant_msg != 'null':
         with st.chat_message(ASSISTANT_NAME):
              st.write(assistant_msg)

def update_chat_log(user_msg,assistant_msg):
    # セッションにチャットログを追加
    if user_msg != 'null':
         st.session_state.chat_log.append({"role": USER_NAME, "content": user_msg})
    if assistant_msg != 'null':
         st.session_state.chat_log.append({"role": ASSISTANT_NAME, "content": assistant_msg})

def reset_chat_log():
    st.session_state.chat_log = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.questions_table = pd.DataFrame()
    

def make_prompt_extract_next_questions(_question,_list_questions):
    return f'''与えられたリストの中で、インタビューの流れを鑑みて、「{_question}」という内容の後に聞くべきインタビュー項目を原文のまま抽出してください。
    # インタビュー項目リスト
    {','.join([question for question in _list_questions if question != _question])}'''

def make_questions_dataframe(list_questions,default_next_questions=True):
    idxs = list_alphabet[:len(list_questions)]
    dict_questions_table = {
        'ID':idxs,
        'Order':list(range(1,len(idxs)+1)),
        'Questions':list_questions,
    }
    df_questions = pd.DataFrame(dict_questions_table)
    if default_next_questions:
         df_questions['Next questions'] = df_questions['ID'].shift(-1)
    return df_questions

def make_graphviz_chart(df_questions):
    _dict_ID_questions = {ser['ID']:ser['Questions'] for _,ser in df_questions.iterrows()}
    graph = graphviz.Digraph(graph_attr={'rankdir':'LR'})
    edges = []
    _error_undifined_IDs = []
    for _,ser in df_questions.iterrows():
        _inputtext_next_questions = ser['Next questions']
        _ID = ser['ID']
        if _inputtext_next_questions:
            _list_next_questions = _inputtext_next_questions.replace('、',',').split(',')
            for _next_question_ID in _list_next_questions:
                if _next_question_ID in _dict_ID_questions:
                    edges += [(_ID,_next_question_ID)]
                else:
                    _error_undifined_IDs.append(_next_question_ID)
    for edge in edges:
        # # (ID_i,ID_j)
        for node_ID in edge:
               node_text = f'{node_ID}\n{_dict_ID_questions[node_ID]}'
               graph.node(node_ID,node_text, shape='box')
        graph.edge(edge[0],edge[1])
    error_text = None
    if len(_error_undifined_IDs) > 0:
        error_text = f'「{','.join(_error_undifined_IDs)}」は未定義のIDです。'
    return graph, error_text

# Function Calling用の関数を作るための関数。引数は順に関数名、関数の説明、変数の説明、出力形式の指定
def make_function(func_name,func_description,items_description,func_type="list"):
  # リスト形式で出力したい場合
  if func_type == 'list':
    function={
            # 関数名
            "name": func_name,
            # 関数の説明
            "description": func_description,
            # 関数の引数の定義
            "parameters": {
                "type": "object",
                "properties": {
                    "comments": {
                        "type": "array",
                        "items":{
                          "type":"string",
                        },
                        "description": items_description,
                    },
                },
                # 必須引数の定義
                "required": ["inputs"],
            },
        }
  # 文字列形式で出力したい場合
  elif func_type == 'str':
    function={
            # 関数名
            "name": func_name,
            # 関数の説明
            "description": func_description,
            # 関数の引数の定義
            "parameters": {
                "type": "object",
                "properties": {
                    "comment": {
                        "type": "string",
                        "description": items_description,
                    },
                },
                # 必須引数の定義
                "required": ["input"],
            },
        }    
  return function
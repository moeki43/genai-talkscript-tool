import streamlit as st
from copy import copy
import pandas as pd

from prompt import *
from functions import *

list_questions = ['お客様の名前', '商談の目的', 'お客様の課題や問題点', 'ご希望や要求', '重要視される特徴や機能', '予算の範囲', '優先される施策や条件']


_prompt_talkscript_plot = """ここまでの会話を参考に、足りない情報は適宜補完しつつ、営業トークスクリプトを作成してください。
どんな内容から順に確認すればよいかをフォーマットに倣って出力してください。
#フォーマット
1. ○○
2. ○○
3. ○○
...
"""

_func_get_question = make_function('extract_interview_questions_without_increment',
                                   f'''与えられた会話文からインタビューの確認事項を抽出する関数。ナンバリングはしないでください。''',
                                   'questions')
_func_rearrange_question = make_function('rearrange_interview_questions_order',
                                   f'''与えられたインタビューの確認事項を、インタビューの流れとして適切な順番に並べ替えてください。''',
                                   'rearranged_questions')

_func_extract_next_question = make_function('extract_next_interview_questions_order',
                                   f'''与えられたリストから条件に見合った内容を３つ程度、原文のまま抽出してください。''',
                                   'extracted_next_questions')





# 画面レイアウト
st.set_page_config(layout="wide")

with st.sidebar:
    user_api_key = st.text_input('Enter your OpenAI API key (not AOAI key)',type='password')
    
    if user_api_key:
        # import openai
        # openai.api_key = user_api_key
        import os
        os.environ["OPENAI_API_KEY"] = user_api_key
        from functions_openai import *


if user_api_key:
    st.write('Sales Talk Script Maker powered by GenAI')
    canvas_pgbar = st.empty()

    with st.sidebar.expander("❔"):
        st.write(TEXT_HELP)

    with st.expander("💬&📃", expanded=True):
        width_left = st.slider('Layout setting',  min_value=0, max_value=10, value=3)
        ax_left,ax_right = st.columns([1+width_left,1+10-width_left])

    with ax_left:
        st.write('💬GenAI Chat for deepening sales situation')
        user_msg = st.chat_input("Input your message")

    with ax_right:
        st.write('📃Interveiw questions table')
        container_table_cols = st.columns(3)
        btn_create = container_table_cols[0].button('Generate questions')
        # btn_questions_order = container_table_cols[1].button('Rearrange questions(WIP)')
        # btn_qustions_links = container_table_cols[2].button('Generate question links(WIP)')

    container_graph = st.container()
    container_graph.write("🧭Talk script chart")

    container_table = ax_right.container(height=450)
    container_chat = ax_left.container(height=450)

    assistant_msg = 'ん？'
    # チャットログを保存したセッション情報を初期化
    if "chat_log" not in st.session_state:#同じタイミングでその他もろもろの情報もリセットされる
        reset_chat_log()

    # btn_reset = widget_cols[1].button('☢Reset')
    # if btn_reset:
    #     reset_chat_log()

    if btn_create:
        messages = st.session_state.chat_log
        if len(messages) <= -1:
            st.warning('もっと会話してください！')
        else:
            messages = copy(st.session_state.chat_log) #messagesを別の変数にすることでchat_logの上書をせず、内部処理のみにとどめる

            my_bar = canvas_pgbar.progress(0,text="Let's start!")

            my_bar.progress(0,text='Wait for GPT creating questions...')        
            messages = gpt_get_content(_prompt_talkscript_plot,messages=messages)
            print('Wait for GPT creating questions...')   
            _res_talkscript_questions = messages[-1]['content']     
            print(_res_talkscript_questions)

            
            print('Wait for GPT drawing questions table...')
            _res_list_questions = get_function_res(_func_get_question,_res_talkscript_questions,messages=messages)["comments"]
            st.session_state.questions_table = make_questions_dataframe(_res_list_questions)

            user_msg = '営業トークスクリプトの質問事項を出してください'
            assistant_msg = '承知しました。左上のウィンドウに表示します。'#_res_list_questions
            my_bar.progress(100,text='Wait for GPT drawing questions table...')
            print('Congratulation! Talk script has been generated!')
            update_chat_log(user_msg,assistant_msg)

    # elif btn_questions_order:
    #     if st.session_state.questions_table.empty:
    #         st.warning('先に質問リストをつくってください。')
    #     else:
    #         with st.spinner('Wait for GPT Rearrange questions order...'):
    #             _text_list_questions = ','.join(list(st.session_state.questions_table['Questions'].fillna('N/A')))
    #             _res_list_questions = get_function_res(_func_rearrange_question,_text_list_questions)["comments"]
    #             print(_res_list_questions)
    #         st.session_state.questions_table['Questions'] = _res_list_questions
    #         st.session_state.questions_table['Order'] = list(range(len(st.session_state.questions_table)))



    # elif btn_qustions_links:
    #     if st.session_state.questions_table.empty:
    #         st.warning('先に質問リストをつくってください。')
    #     else:
    #         _increment = 0
    #         _d = 100 // len(st.session_state.questions_table)
    #         _my_bar = st.progress(_increment,text="Let's start!")
    #         _list_questions = st.session_state.questions_table['Questions'].tolist()
    #         for _,ser in st.session_state.questions_table.iterrows():
    #             _increment += _d
    #             _question = ser['Questions']
    #             _my_bar.progress(_increment,text = f'Wait for GPT reasoning next questions after "{_question}"...') 
    #             _prompt = make_prompt_extract_next_questions(_question,_list_questions)
    #             _res_list_extracted_questions = get_function_res(_func_extract_next_question,_prompt)["comments"]
    #             # _next_questions = []
    #             # _question_order = st.session_state.questions_table.query('Questions == _question')['Order'].iloc[0]
    #             # for _next_question in _res_list_extracted_questions:
    #             #     if _next_question != _question:

    #             print(f'Wait for GPT reasoning next questions after "{_question}"...')
    #             print(_res_list_extracted_questions)
    #         _my_bar.progress(100,text='Finished.')



                    
    elif user_msg:
        assistant_msg = 'ん？'
        # 普通の対話
        with st.spinner('Wait for GPT...'):
            messages = gpt_get_content(user_msg,messages=st.session_state.chat_log)
            # print(messages)
        assistant_msg = messages[-1]['content']


    if not st.session_state.questions_table.empty:
        st.session_state.questions_table = container_table.data_editor(
            st.session_state.questions_table,
            disabled=["ID"],
            hide_index=True,
            num_rows="dynamic",)
        graph,error_text = make_graphviz_chart(st.session_state.questions_table)
        with container_graph:
            st.graphviz_chart(graph)
            if error_text:
                st.write(error_text)


    with container_chat:
        # 以前のチャットログを表示
        show_past_talk()

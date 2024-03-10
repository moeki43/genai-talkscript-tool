

TEXT_HELP = '''画面下部の入力欄を用いて、必要な商談について生成AIと対話してください。

**ボタンについて**
- Create qustions table : 画面右のチャットの内容に基づいて、トークスクリプトの質問テーブルを生成します。 
- Rearrange qustions : 生成した質問の順番の並び替えを生成AIが行います。(※事前に質問テーブルを生成しておく必要があります)
- Genarate links : WIP

**質問テーブルについて**
- ID : 質問対して自動的に一意に付与されます。
- Order : 質問の順番であり、編集可能です。
- Next questions : 該当の行の質問の次に訊くべき質問のIDを記載します。カンマ区切りで記載してください。
             
**各種コマンド（以下のコマンドを入力の冒頭に書くことで、精緻な対話が可能です）**
- 「table/question order/」 : WIP
'''




diagraph_sample = '''
    digraph {
        run -> intr
        intr -> runbl
        runbl -> run
        run -> kernel
        kernel -> zombie
        kernel -> sleep
        kernel -> runmem
        sleep -> swap
        swap -> runswap
        runswap -> new
        runswap -> runmem
        new -> runmem
        sleep -> runmem
    }
'''

# _prompt_talkscript_ideation = """この内容に分岐を増やしてください。"""
# _prompt_talkscript_edgenode = """与えられた内容をedge,node形式に変換してください。nodeは営業トークスクリプトにおける質問内容が入ります。"""
# _prompt_talkscript_diagraph = f"""与えられた内容のedgeを例に倣って、Graphviz DOT Language形式に変換してください。
# # 例
# {diagraph_sample}
# """
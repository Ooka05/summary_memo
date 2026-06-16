import streamlit as st
import datetime

st.title("1行要約メモ")

# --- 入力エリア ---
st.subheader("新しいメモを追加")
new_word = st.text_input("学んだこと")
new_memo = st.text_input("学んだことを1行で要約（140文字以内）", max_chars=140)
category = st.selectbox("カテゴリ", [ "ビジュアライゼーション", "HCI設計論", "実用英語", "人工知能応用"], key="input_cat")

FILE_NAME = "memos.txt"

if st.button("保存する"):
    if new_memo:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        # あとで検索しやすいように、あえて半角スペースなどを整えて保存します
        memo_line = f"{now} | [{category}]{new_word} {new_memo},\n"
        with open(FILE_NAME, "a", encoding="utf-8") as f:
            f.write(memo_line)
        st.success("保存しました！")
    else:
        st.error("文字を入力してください。")

st.write("---")

# --- 履歴・絞り込みエリア ---
st.subheader("これまでの履歴")

# 絞り込み用のセレクトボックス（「すべて」という選択肢を最初に追加）
filter_cat = st.selectbox("カテゴリで絞り込み", ["すべて", "ビジュアライゼーション", "HCI設計論", "実用英語", "人工知能応用"], key="filter_cat")

try:
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        memos = f.readlines()

   for memo in reversed(memos):
        # 画面に表示するテキストを、1行ずつ「装飾された文字」に変換する
        if filter_cat == "すべて" or f"[{filter_cat}]" in memo:
            
            # 「学んだこと」の部分だけを大きく目立たせるための加工
            # 日時とカテゴリの後に来る「 | 」で文章を分割します
            parts = memo.strip().split("] ", 1)
            
            if len(parts) == 2:
                header_part = parts[0] + "]"  # 「日時 | [カテゴリ]」の部分
                content_part = parts[1]       # 「学んだこと（用語）」の部分
                
                # HTMLを使って、学んだことの部分だけを大きな文字（font-size: 20px）にする
                styled_text = f"<span style='color: #666;'>{header_part}</span> <strong style='font-size: 20px; color: #1f77b4;'>{content_part}</strong>"
                st.markdown(styled_text, unsafe_allow_html=True)
            else:
                st.write(memo.strip())
except FileNotFoundError:
    st.info("まだメモはありません。")

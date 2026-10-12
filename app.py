import streamlit as st
import datetime
import sqlite3

# --- データベースの初期化 ---
DB_NAME = "memos.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # メモを保存するテーブルを作成
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            category TEXT NOT NULL,
            word TEXT NOT NULL,
            memo TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# アプリ起動時にテーブルを作成
init_db()

st.title("1行要約メモ (SQLite3版)")

# --- 入力エリア ---
st.subheader("新しいメモを追加")
new_word = st.text_input("学んだこと")
new_memo = st.text_input("学んだことを1行で要約（140文字以内）", max_chars=140)
category = st.selectbox("カテゴリ", ["ビジュアライゼーション", "HCI設計論", "実用英語", "人工知能応用"], key="input_cat")

if st.button("保存する"):
    if new_memo and new_word:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # データベースに保存
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO memos (created_at, category, word, memo) VALUES (?, ?, ?, ?)",
            (now, category, new_word, new_memo)
        )
        conn.commit()
        conn.close()
        
        st.success("保存しました！")
        # 入力欄をクリアするために再読み込み
        st.rerun()
    else:
        st.error("学んだことと要約の両方を入力してください。")
        
st.write("---")

# --- 履歴・絞り込みエリア ---
st.subheader("これまでの履歴")

filter_cat = st.selectbox("カテゴリで絞り込み", ["すべて", "ビジュアライゼーション", "HCI設計論", "実用英語", "人工知能応用"], key="filter_cat")

# データベースからデータを取得
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

if filter_cat == "すべて":
    cursor.execute("SELECT created_at, category, word, memo FROM memos ORDER BY id DESC")
else:
    cursor.execute("SELECT created_at, category, word, memo FROM memos WHERE category = ? ORDER BY id DESC", (filter_cat,))

memos = cursor.fetchall()
conn.close()

if memos:
    for created_at, cat, word, memo_text in memos:
        header_part = f"{created_at} | [{cat}]{word}"
        content_part = memo_text
        
        styled_text = f"<span style='color: #666;'>{header_part}</span> <strong style='font-size: 20px; color: #1f77b4;'>{content_part}</strong>"
        st.markdown(styled_text, unsafe_allow_html=True)
else:
    st.info("まだメモはありません。")

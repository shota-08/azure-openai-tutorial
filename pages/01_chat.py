import streamlit as st
from config import AzureOpenAIClient

def init_page():
    st.set_page_config(
        page_title="LLM"
    )
    st.title("LLM x CHAT")
    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []

def get_llm_response(query, client):
    recent_log = st.session_state.chat_log
    messages = [
        {"role":"system", "content":f"""
            # 命令
            ユーザーの要望をかなえられる、適切なコードを端的に回答しなさい。
            他、適切な回答をしなさい。
            # 具体例
            Q: pythonのコードを書け
            A: print("hello")
        """}
    ]
    messages += [
        {"role": "assistant", "content": entry["msg"]} if entry["name"] == client.ASSISTANT_NAME else {"role": "user", "content": entry["msg"]}
        for entry in recent_log
    ]
    messages.append({"role": "user", "content": query})
    response = client.client.chat.completions.create(
        model=client.chat_deployment, # chat_deployment
        messages=messages,
        temperature=0
    )
    answer = response.choices[0].message.content

    # セッションにログを追加
    st.session_state.chat_log.append({"name" : client.USER_NAME, "msg" : query})
    st.session_state.chat_log.append({"name" : client.ASSISTANT_NAME, "msg" : answer})

    return answer

def chat(client):
    # ログ表示
    for chat in st.session_state.chat_log:
        with st.chat_message(chat["name"]):
            st.write(chat["msg"])

    query = st.chat_input('回答を入力')
    if query:
        answer = get_llm_response(query, client)

        with st.chat_message(client.USER_NAME):
            st.write(query)

        with st.chat_message(client.ASSISTANT_NAME):
            st.write(answer)

    if not query and st.session_state.chat_log == []:
        first_chat = "自由に話してね!"
        with st.chat_message(client.ASSISTANT_NAME):
            st.write(first_chat)
        st.session_state.chat_log.append({"name" : client.ASSISTANT_NAME, "msg" : first_chat})


def main():
    client = AzureOpenAIClient()
    init_page()
    chat(client)

if __name__ == '__main__':
    main()
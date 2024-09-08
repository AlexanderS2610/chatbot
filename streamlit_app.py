import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "Este es un chatbot simple que utiliza el modelo GPT-3.5 de OpenAI para generar respuestas".
    "Para utilizar esta aplicación, debe proporcionar una clave API de OpenAI "
    "También puede aprender cómo crear esta aplicación paso a paso [siguiendo nuestro tutorial] (https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)".
)


openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    #Crear un cliente OpenAI.
    client = OpenAI(api_key=openai_api_key)

    # Cree una variable de estado de sesión para almacenar los mensajes de chat. Esto asegura que el
    # mensajes persisten en las repeticiones.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar los mensajes de chat existentes a través de `st.chat_message`
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Cree un campo de entrada de chat para permitir al usuario ingresar un mensaje. Esto mostrará
    # automáticamente en la parte inferior de la página.
    if prompt := st.chat_input("What is up?"):

        # Almacenar y mostrar el mensaje actual.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        
        # Generar una respuesta usando la API OpenAI.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Transmita la respuesta al chat usando `st.write_stream`, luego guárdela
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

import streamlit as st
from SRC.rag_engine import get_answer

st.title("grape AI Agent")

query = st.text_input("Enter your question:")
if query:
    with st.spinner("Thinking..."):
        answer, input_tokens, output_tokens, total_tokens, estimated_cost = get_answer(query)

    st.subheader("Answer")
    st.write(answer)

    st.subheader("Token Usage")
    st.write(f"🔹 Input Tokens: {input_tokens}")
    st.write(f"🔹 Output Tokens: {output_tokens}")
    st.write(f"🔹 Total Tokens: {total_tokens}")
    st.write(f"💰 Estimated Cost: ${estimated_cost}")

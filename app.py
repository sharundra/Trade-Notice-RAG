import streamlit as st
from src.rag_chain import get_rag_chain

st.set_page_config(page_title="Trade Policy Bot", page_icon="🚢")

st.title("Export Policy Assistant")
st.markdown("Ask questions about India's Export Policy (Schedule-II).")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ex: Can I export Natural Rubber?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("Consulting the Trade Notice..."):
            try:
                # Load Chain (Cached via Streamlit usually, but simple import here works)
                chain = get_rag_chain()
                
                # Run Chain
                response = chain.invoke({"input": prompt})
                answer = response["answer"]
                sources = response["context"]

                # Display Answer
                message_placeholder.markdown(answer)
                
                # Show Sources 
                with st.expander("View Source Documents"):
                    for i, doc in enumerate(sources):
                        st.markdown(f"**Source {i+1} (Page {doc.metadata.get('page', '?')})**")
                        st.text(doc.page_content)
                        st.divider()

                # Add assistant message to history
                st.session_state.messages.append({"role": "assistant", "content": answer})
            
            except Exception as e:
                st.error(f"Error: {e}")
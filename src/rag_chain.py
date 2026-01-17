from langchain_openai import ChatOpenAI
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.config import config
from src.vector_store import get_vectorstore

def get_rag_chain():
    # Initialize Vector Store & Retriever
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": config.K_RETRIEVAL}
    )

    # Initialize LLM
    llm = ChatOpenAI(
        model=config.LLM_MODEL,
        temperature=0, # Keeping it deterministic for policy questions
        api_key=config.OPENAI_API_KEY
    )

    # The Prompt-- we explicitly tell it to look at the 'Export Policy' and 'Conditions'.
    system_prompt = (
        "You are an expert Trade Consultant specializing in India's Export Policy (ITC-HS Codes)."
        "\n\n"
        "Use the provided context to answer the user's question."
        "The context consists of database rows containing ITC Codes, Descriptions, and Policies."
        "\n\n"
        "Rules:"
        "\n1. If the user asks about a specific item, identify its Export Policy (Free, Restricted, Prohibited)."
        "\n2. Always mention the ITC(HS) Code if available in the context."
        "\n3. If there are specific Policy Conditions (e.g., 'Minimum Export Price', 'Certificate Required'), mention them clearly."
        "\n4. If the answer is not in the context, say you don't know. Do not hallucinate."
        "\n\n"
        "Context: {context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    # Building Chain using LangChain's utilities
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    return rag_chain
# Set env var OPENAI_API_KEY or load from a .env file:
import dotenv
import bs4
from langchain import hub
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader

dotenv.load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=1)

docs = TextLoader("./data/products.txt").load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_prompt = ChatPromptTemplate.from_messages([
    """You are an compeny assistant. Your job is to answer customer questions. If you don't know the answer, don't speculate, say that you don't know. Keep your answers short and factual.
    Question: {question}
    Context: {context}
    Answer:"""
])

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

product_question_1 = "Hi, I need new shoes, which of your company products would you recommend?"
print(product_question_1)
print(rag_chain.invoke(product_question_1))

product_question_2 = "Hi, I need a new hat, which of your company products would you recommend?"
print(product_question_2)
print(rag_chain.invoke(product_question_2))

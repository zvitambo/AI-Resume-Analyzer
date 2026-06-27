from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
import os


#1: Loading a PDF File

#file_path = "Think-And-Grow-Rich_2011-06.pdf"
file_path = "AI.pdf"
collection_name= "ThinkAndGrowRichCollection"
persist_dir = "./chroma_db"

loader = PyPDFLoader(file_path)

docs = loader.load()

print(len(docs))

#2 : Chunking the document

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)

chunks = text_splitter.split_documents(docs)

print(len(chunks))

#generating embeddings for the document chunks

embeddings = OllamaEmbeddings(model="llama3.1:8b")

print("generated embeddings")
# saving embeddings to Chroma vector store

if not os.path.exists(path=persist_dir):
    vector_store = Chroma(
    collection_name=collection_name,
    embedding_function=embeddings,
    persist_directory=persist_dir
)
    print("created vector store")

    ids = vector_store.add_documents(documents=chunks)

    print("ids", ids)

    print("added doc to vector store")
else:
    print("✅vector store exists.....")
    vector_store = Chroma(
    collection_name=collection_name,
    embedding_function=embeddings,
    persist_directory=persist_dir
)





@tool(response_format="content_and_artifact", description= "Retrieve information to help answer a query.")
def retrieve_context(query: str):
    """Retrieve information to help answer a query."""  # this would be the tools description by defualt if not specified above
    
    # Use the vectorstore as a retriever
    # retriever = vector_store.as_retriever(
    #     search_type='similarity'
    #     search_kwargs={
    #     "k": 5,        
    # })

    # # Retrieve the most similar text
    # retrieved_docs = retriever.invoke(input=query)
    
    retrieved_docs = vector_store.similarity_search(query=query, k=3)

    serialized = "/n/n".join((f"Source: {doc.metadata}\nContent: {doc.page_content}") for doc in retrieved_docs)

    return serialized, retrieved_docs

# Initialize model with tool-calling capabilities
llm = ChatOllama(
    model="llama3.1:8b", 
    temperature=0,
    validate_model_on_init=True  
)

print("initialized model ... ")

#agent = create_agent(model=llm, tools=[retrieve_context])

tools = [retrieve_context]

# If desired, specify custom instructions

prompt = (
    "You have access to a tool that retrieves context from a document. "
    "Use the tool to help answer user queries."
)
agent = create_agent(llm, tools, system_prompt=prompt)
print("created agent")

query = (
     "How can I become an AI engineer in 3 weeks ? Give me the best path to achieve thos"
)

print(" agent streaming start ...")
for event in agent.stream(
    {"messages": [{"role": "user", "content": query}]},
    stream_mode="values",
):
    event["messages"][-1].pretty_print()

print(" agent streaming end ...")



def extract_resume_data(resume_text: str) -> dict:
    ...

def extract_jd_data(jd_text: str) -> dict:
    ...

def generate_analysis(resume_data: dict, jd_data: dict, score: float) -> dict:
    ...
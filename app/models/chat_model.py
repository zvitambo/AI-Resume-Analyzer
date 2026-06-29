from ollama import generate

from langchain_ollama import ChatOllama
from langchain_classic.chains import LLMChain
from langchain_classic.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser

from app.core.config import settings

extract_resume_data_prompt_text = "app\prompts\\resume_extraction.txt"
extract_jd_data_prompt_text = "app\prompts\jd_extraction.txt"
generate_analysis_prompt_text = "app\prompts\\analysis_prompt.txt"

with open(extract_resume_data_prompt_text, "r") as file:
    extract_resume_data_prompt=file.read()

with open(extract_jd_data_prompt_text, "r") as file:
    extract_jd_data_prompt=file.read()

with open(generate_analysis_prompt_text, "r") as file:
    generate_analysis_prompt=file.read()





class LlamaChat:
    def __init__(self):
        self.model_name = settings.model_name
        self.extract_resume_data_prompt = extract_resume_data_prompt
        self.extract_jd_data_prompt = extract_jd_data_prompt
        self.generate_analysis_prompt = generate_analysis_prompt 
        self.messages = []


    def extract_resume_data_response(self, resume_text):
        user_input = f"{self.extract_resume_data_prompt}, resume text: {resume_text}"
        self.messages.append({"role": "user", "content": user_input})
        response = generate(
            model=self.model_name,
            prompt=user_input
        )
        self.messages.append({"role": "assistant", "content": response})

        return response.message.content
    
    def extract_jd_data_response(self, jd_text):
        user_input = f"{self.extract_jd_data_prompt}, job description text: {jd_text}"
        self.messages.append({"role": "user", "content": user_input})
        response = generate(
            model=self.model_name,
            prompt=user_input
        )
        self.messages.append({"role": "assistant", "content": response})

        return response.message.content
    
    def generate_analysis_response(self, resume_data: dict, jd_data: dict, score: float):
        user_input = f"{self.generate_analysis_prompt}, resume data: {resume_data}, job description data: {jd_data}, score: {score}"
        self.messages.append({"role": "user", "content": user_input})
        response = generate(
            model=self.model_name,
            prompt=user_input
        )
        self.messages.append({"role": "assistant", "content": response})

        return response.message.content
    


class LangChainLlamaChat:
    def __init__(self):
        self.llm = ChatOllama(model=settings.model_name)
        self.memory = ConversationBufferMemory(return_messages=True)
        self.prompt = ChatPromptTemplate.from_messages([
                    ("system", "{system_prompt}"),
                    MessagesPlaceholder(variable_name="history"),
                    ("user", "{input}")
                ])
        self.chain = self.prompt | self.llm | StrOutputParser()        
        self.extract_resume_data_prompt=extract_resume_data_prompt
        self.extract_jd_data_prompt=extract_jd_data_prompt
        self.generate_analysis_prompt=generate_analysis_prompt 


    def extract_resume_data_response(self, resume_text):
        response = self.chain.invoke({"system_prompt": self.extract_resume_data_prompt, "input": resume_text})
        return response["text"]
    
    def extract_jd_data_response(self, jd_text):        
        response = self.chain.invoke({"system_prompt": self.extract_jd_data_prompt, "input": jd_text})
        return response["text"]
    
    def generate_analysis_response(self, resume_data: dict, jd_data: dict, score: float):
        response = self.chain.invoke({"system_prompt": self.generate_analysis_prompt, "input": f"{resume_data}, {jd_data}, {score}"})
        return response["text"]
# Set env var OPENAI_API_KEY or load from a .env file:
import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

dotenv.load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=1)

teacher_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are math teacher. You job is to ask math questions. Be as creative as possible. Only respond with the single question."),
    ("user", "{input}")
])

teacher_output_parser = StrOutputParser()

teacher = teacher_prompt | llm

question = teacher.invoke({"input": "Can you please ask me a math question?"})
print(question.content)

student_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are math student. Your task is to answer math questions."),
    ("user", "{input}")
])

student_output_parser = StrOutputParser()

student = student_prompt | llm | student_output_parser

print(student.invoke({"input": question.content}))

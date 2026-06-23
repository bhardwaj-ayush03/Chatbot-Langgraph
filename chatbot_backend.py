from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import BaseMessage, add_messages
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

llm=ChatGroq(
    model='llama-3.1-8b-instant',
    temperature=0.5,
    api_key=os.getenv('GROQ_API_KEY')
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

# Checkpointer

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

checkpointer = InMemorySaver()

chatbot = graph.compile(checkpointer=checkpointer)
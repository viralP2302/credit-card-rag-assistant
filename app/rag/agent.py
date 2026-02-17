from langchain_huggingface import HuggingFaceEmbeddings
import os
from langchain_community.vectorstores import InMemoryVectorStore
import json
from langgraph.graph import StateGraph
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.documents import Document
from app.models.graph_state import GraphState

class RagAgent():

    def __init__(self) -> None:
        """
        Initialize the RAG agent.
        This includes:
        - Initializing the LLM
        - Initializing the tools
        - Initializing the vector store
        - Initializing the graph builder
        - Initializing the graph
        """
        # Use Ollama (no API key) when OPENAI_API_KEY is not set; otherwise use OpenAI
        use_ollama = not os.environ.get("OPENAI_API_KEY") or os.environ.get("USE_OLLAMA", "").lower() in ("1", "true", "yes")
        if use_ollama:
            ollama_model = os.environ.get("OLLAMA_MODEL", "llama3.2")
            self.llm = ChatOllama(model=ollama_model)
        else:
            self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.llm_with_tools = self.llm.bind_tools([self.retrieve])
        # Embeddings model
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

        # load data from json file (path relative to this file so it works from any cwd)
        _here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(_here, "credit_cards.json"), "r") as f:
            data = json.load(f)
        cards_docs = self.format_content_to_docs(data)
        # In-memory vector store
        self.vector_store = InMemoryVectorStore(self.embeddings)
        self.vector_store.add_documents(documents=cards_docs)

        print("Documents loaded to vector store\n")

         # build RAG agent
        self.graph_builder = StateGraph(GraphState)

        self.graph_builder.add_node("query_or_respond",self.query_or_respond)
        self.graph_builder.add_node("tools",self.retrieve)
        self.graph_builder.add_node("generate",self.generate)

        self.graph_builder.set_entry_point("query_or_respond")
        self.graph_builder.add_edge("query_or_respond","tools")
        self.graph_builder.add_edge("tools", "generate")
        self.graph_builder.add_edge("generate", END)

        self.graph = self.graph_builder.compile()

        
    def format_content_to_docs(self, data) -> list[Document]:
        """
        Format the content to documents to be indexed to the vector store.
        """
        docs = []
        for card in data:
            doc = Document(id = card["name"], page_content=card["description"], metadata = {"name":card["name"]})
            docs.append(doc)
        return docs

    def retrieve(self, state: GraphState):
        """Tool retrieves credit card information related to a user query from the vector store."""

        query = state.query
        retrieved_docs = self.vector_store.similarity_search(query, k=3)
        serialized = "\n\n".join(
            (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
            for doc in retrieved_docs
        )
        print("Retrieved {0} docs from Store\n".format(len(retrieved_docs)))
        return {"messages": [ToolMessage(content = serialized, tool_call_id = "")]}


    # Step 1: Generate an AIMessage that may include a tool-call to be sent.
    def query_or_respond(self, state: GraphState):
        """Generate tool call for retrieval"""
        response = self.llm_with_tools.invoke(state.messages)
        # MessagesState appends messages to state instead of overwriting
        return {"messages": [response]}


    # Step 3: Generate a response using the retrieved content.
    def generate(self, state: GraphState):
        """Generate answer using the retrieved content."""
        # Get generated ToolMessages
        recent_tool_messages = []
        for message in reversed(state.messages):
            if message.type == "tool":
                recent_tool_messages.append(message)
            else:
                break
        tool_messages = recent_tool_messages[::-1]

        # Format into prompt
        # docs_content = "\n\n".join(doc.content for doc in tool_messages)
        system_message_content = (
            "You are an assistant to help answer queries about credit cards. "
            "Use the following pieces of retrieved context to answer the question. If you don't know the answer, say that you don't know."
            "Reply with whatever information you are given and don't ask the user follow up questions."
            "\n\n"
            f"{recent_tool_messages[0]}"
        )
        conversation_messages = [
            message
            for message in state.messages
                if message.type in ("human", "system")
                or (message.type == "ai" and not message.tool_calls)
        ]
        prompt = [SystemMessage(system_message_content)] + conversation_messages

        # Run
        response = self.llm.invoke(prompt)
        return {"messages": [response]}
        
        

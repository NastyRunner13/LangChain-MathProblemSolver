import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains.llm import LLMChain
from langchain.chains import LLMMathChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

st.set_page_config(page_title="Text to Math Problem Solver and Data Science Assistant")
st.title("Text to Math Problem Solver")

# Sidebar for API key input
groq_api_key = st.sidebar.text_input(label="Groq API Key", type="password")

if not groq_api_key:
    st.sidebar.warning("Please enter your Groq API Key to continue.")
    st.stop()

# Initialize the LLM
llm = ChatGroq(model="mixtral-8x7b-32768", api_key=groq_api_key)

# Set up tools
wikipedia_tool = Tool(
    name="Wikipedia",
    func=WikipediaAPIWrapper().run,
    description="Useful for answering questions about general knowledge."
)

math_chain = LLMMathChain.from_llm(llm=llm)
calculator_tool = Tool(
    name="Calculator",
    func=math_chain.run,
    description="Useful for solving mathematical expressions."
)

# Prompt template for reasoning
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="""
You are a helpful assistant skilled at solving mathematical problems.
Please logically derive the solution to the following question, explaining each step:

Question: {question}

Answer:
""",
)

reasoning_chain = LLMChain(llm=llm, prompt=prompt_template)
reasoning_tool = Tool(
    name="Reasoning",
    func=reasoning_chain.run,
    description="Useful for solving logic and reasoning problems."
)

# Initialize the agent
tools = [wikipedia_tool, calculator_tool, reasoning_tool]

try:
    assistant_agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
        handle_parsing_errors=True
    )
except Exception as e:
    st.error(f"An error occurred while initializing the agent: {e}")
    st.stop()

# Session state to store messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I am a Math chatbot. How can I help you today?"}
    ]

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# User input
user_input = st.chat_input("Enter your question")
if user_input:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Generate response
    with st.spinner("Generating Response..."):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        try:
            response = assistant_agent.run(user_input, callbacks=[st_cb])
        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")
            response = "I'm sorry, I couldn't process that question."
        
        # Display assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
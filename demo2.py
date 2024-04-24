import os
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from pathlib import Path
from langchain1.chains import ConversationChain
from langchain1.chains.conversation.memory import ConversationEntityMemory
from langchain1.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain1.llms import OpenAI
from langchain1.prompts import load_prompt
from langchain_core.prompts import PromptTemplate
from langchain1.chains import (
    StuffDocumentsChain, LLMChain, ConversationalRetrievalChain
)
from sql_execution import execute_mysql_query  # Import the execute_mysql_query function
from prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE1

# Setup env variable
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Set Streamlit page configuration
st.set_page_config(page_title="AI SQL", layout="wide")




# Initialize session states
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []
if "sql_queries" not in st.session_state:
    st.session_state["sql_queries"] = []  # Initialize sql_queries attribute
if "input_history" not in st.session_state:
    st.session_state.input_history=[]
if "output_tables" not in st.session_state:
    st.session_state["output_tables"] = []
if "con_history" not in st.session_state:
    st.session_state.con_history=[]
if "sql_statement" not in st.session_state:
    st.session_state.sql_statement=[]
    
history = st.session_state["past"]

def new_chat():
    """
    Clears session state and starts a new chat.
    """
    save = []
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + str(st.session_state["generated"][i]))
    session = [(user, bot) for user, bot in zip(st.session_state["past"], st.session_state["generated"])]
    st.session_state["stored_session"].append(session)
    # Reset the session state
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    st.session_state["output_tables"] = []
    st.session_state["input_history"] = []
    st.session_state["sql_queries"] = []
    st.session_state["con_history"]=[]
    st.session_state["sql_statement"]=[]
    st.session_state.entity_memory.entity_store = {}
    st.session_state.entity_memory.buffer.clear()
    # Display stored chat history in sidebar
    #st.sidebar.write(session)



# Create an OpenAI instance
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo-instruct", verbose=False)

#sql_generation_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)

if "entity_memory" not in st.session_state:
    st.session_state.entity_memory = ConversationEntityMemory(llm=llm)
    


conversation_chain = ConversationChain(llm=llm,prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE1, verbose=True, memory=st.session_state.entity_memory)

# Add a button to start a new chat
st.markdown(
    """
<style>
button.st-emotion-cache-s48dsx{
    align-content: center;
    height: auto;
    width: auto;
    padding-left: 70px !important;
    padding-right: 70px !important;
    
}
</style>
""",
    unsafe_allow_html=True,
)



#Sidebar option menu
with st.sidebar:
   selected = option_menu("🏫Welcome SMVEC", ["Home","AI-SQL"], 
       icons=['house' , 'database'], menu_icon="🏫",default_index=1,orientation="Vertical",
       styles={
        "container":{
             "width":"290px",
              "padding":"5px",
             "float":"left",
              "background-color":"#202126",
              "font-family":"'Trebuchet MS',Helvetica,sans-serif"
     },
          "icon":{
             "color":"",
          "font-size":"20px"
           },
       "nav-link":{
             "color":"white",
              "font-size":"20px",
              "margin":"0px",
           "hover-color":"red"
          },
           "nav-link-selected":{
               "background-color":"#e64c4c"
           }
      })

#Title: span is used in two places to give two different colors, font-size is used to change size of font and color is used to assign colors
s = f"<center><span style='font-size:45px; color:rgb(180,0,60)'>AI SQL </span><span style='font-size:45px; color:rgb(255,255,255)'>Assistant</span></center>"
st.markdown(s,unsafe_allow_html=True)
st.divider()
with st.sidebar.empty():
    st.write(' ')
with st.sidebar.empty():
    st.write(' ')


if selected == 'Home':
    pass

if selected == 'AI-SQL':

    st.sidebar.button("New Chat", on_click=new_chat, type="primary")

    # Get the user input
    user_input = st.chat_input("Your AI assistant is here! Ask me anything ..")


    # Define icons
    user_icon = "👤"
    bot_icon = "🤖"

    download_data = []



    if user_input:
        # Generate SQL query
        sql_query = conversation_chain.run(input=user_input)
        
        # Concatenate user input and SQL query
        input_with_sql = f"{user_input} {sql_query}" if sql_query else user_input
        
        output = conversation_chain.run(input_with_sql)
        
        st.session_state.sql_statement.append(sql_query)
        
        
        
        # Check if the input contains a "SELECT" statement
        if "SELECT" in sql_query:
            # Execute the SQL query
            df = execute_mysql_query(sql_query)

            # Store user input and generated output
            st.session_state.past.append(user_input)
            st.session_state.generated.append(df)

        

            if isinstance(df, pd.DataFrame):
                # Append the new DataFrame to the list of DataFrames
                st.session_state.input_history.append(user_input)
                st.session_state.output_tables.append(df)
                
                    
        else:
            # If it's not a SELECT statement, simply append the user input
            st.session_state.past.append(user_input)
            st.session_state.generated.append(sql_query)
            if isinstance(sql_query, type(sql_query)):
                # Append the new DataFrame to the list of DataFrames
                
                st.session_state.con_history.append(sql_query)
                st.session_state.input_history.append(user_input)  # Append the user_input instead of sql_query

        # Display user input and AI response
        for input_, output,sql_query1 in zip(st.session_state.input_history, st.session_state.generated,st.session_state.sql_statement):
            st.markdown(f"{user_icon}<b>  :red[Your Input]</b>", unsafe_allow_html=True)
            st.markdown(f"{input_}", unsafe_allow_html=True)
            st.write("")
            st.markdown(f"{bot_icon}<b>  :red[AI Response:]</b>", unsafe_allow_html=True)

            if isinstance(output, pd.DataFrame):
                tab_titles = ["Output", "sql_query"]
                tabs = st.tabs(tab_titles)
                with tabs[0]:
                    st.write("Output:")
                    st.write(output)
                with tabs[1]:
                    st.write("Generated SQL Query:")
                    st.code(sql_query1)

            else:
                st.write(output)
                
            



    # Prepare data for download
    download_str = "\n".join(map(str, download_data))
    if download_str:
        st.download_button("Download", download_str)



for i, sublist in enumerate(st.session_state.stored_session):
    with st.sidebar.expander(label=f"Conversation-Session:{i}"):
        st.write(sublist)

# Allow the user to clear all stored conversation sessions
if st.session_state.stored_session:
    if st.sidebar.checkbox("Clear-all"):
        del st.session_state.stored_session
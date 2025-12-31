import streamlit as st
import pandas as pd
import time
import datetime as dt
import json
from typing import List, Callable, Dict, Any, Tuple, Optional

def stream_data(msg: str):
    """
    Generator that enables streaming writing
    :param msg: text message
    """
    for word in msg.split(" "):
        yield word + " "
        time.sleep(0.01)

def add_global_memory(agent_name: str, memory: dict | Any) -> None:
    """
    Handle global memory for all agents. This would be stored in the st.session_state object
    
    :param agent_name: the name of the agent
    :param memory: the memory object to be stored. (a dictionary)
    """
    if "global_memory" not in st.session_state:
        st.session_state["global_memory"] = []
        
    
    st.session_state['global_memory'].append(
        {"agent_session": agent_name, 
            "role": memory.get("role", None),
            "content": memory.get("content", None),
            "tool_calls": memory.get("tool_calls", None),
            "time": memory.get("time", None)
        }
    )

def format_message(message: str):
    """
    Formatting the memory content. 
    
    :param message: memory content (text)
    """

    # not dict like -> return directly
    if not (message.startswith("{") and message.endswith("}")):
        return message
    
    # otherwide load it as a json object -> dict
    body = json.loads(message)

    # return eigher 'message' or 'result' 
    # * message comes when the agent return text, and result comes when the agent implements a tool call
    if "message" in body:
        return body['message']
    elif "result" in body:
        return body['result']
    else:
        return 

def format_tool_calls(messages: Any):
    """
    Format the tool call object list
    
    :param messages: A list that contains tool call objects, or None
    """
    if not isinstance(messages, list):
        return 
    value = ""
    for message in messages:
        tool_name = message.function.name
        tool_args = message.function.arguments
        value += "> " + tool_name + ": " + tool_args + "\n"
    return value





def render_global_memory():
    """
    A dialog window that shows global memory.

    This function use 'format_message' and 'format_tool_calls' functions
    """
    if not st.session_state['global_memory']:
        st.error("No memory yet!")
    else:
        df = pd.DataFrame(st.session_state['global_memory'])
        df['time_on_display'] = df['time'].apply(lambda x: dt.datetime.fromtimestamp(float(x)).strftime("%Y-%m-%d %H:%M:%S"))

        df['content'] = df['content'].apply(lambda x: format_message(x))
        df['tool_calls'] = df['tool_calls'].apply(lambda x: format_tool_calls(x))

        st.dataframe(df.sort_values(by = "time", ascending = True),
            column_config = {
                "time": None
            }
        )


def render_sidebar():
    """
    Render a streamlit sidebar

    """
    with st.sidebar:
        st.header("Tic-Tac-Toe 圈圈叉叉")
        st.caption("A Tic-Tac-Toe game with :blue[**disappearing cells**]. Whenever a player has moved three times, the oldest move will be removed. You could also play with AI player.")
        # st.logo("assets/icon.png", size = 'large')

        with st.container(border = True):
            st.subheader(":material/settings: **Setting**")
            st.session_state['play_mode'] = st.pills("Mode", ["Play with AI", "Play with Human"], default = "Play with AI")
            
            # only show AI-related setting when the user plays with AI
            if st.session_state['play_mode'] == "Play with AI":
                st.session_state['difficulty'] = st.selectbox("Difficulty", ['easy', 'medium', 'hard'])
                st.session_state['debug_mode'] = st.pills("Debug mode", [True, False], format_func = lambda x: "On" if x else "Off", default = False)
                st.caption("Note: **Player 2** is always **AI**.")
            

       


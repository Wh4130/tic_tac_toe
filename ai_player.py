from agents.agent import agent
from components.game import ActionContext, Memory, Goal
from components.frame import AgentRegistry, Agent
from config import MAX_HISTORY

import streamlit as st 




    
def AI_PLAYER_MOVE(action_context):
    """
    Docstring for AI_PLAYER
    
    :param action_context: Action Context object
    :param game: TicTacToe_Game Object
    """
    # * set difficulty
    difficulty = st.session_state['difficulty']
    agent.goals.append(Goal(f"[Important] The difficulty level is {difficulty}."))

    # * get current canva
    canva = st.session_state['game_state']
    query = f"The current canva is {canva}. Please implement your next move."

    with st.spinner("AI thinking..."):
        st.session_state.shared_memory = agent.run(
                                    query, 
                                    memory=st.session_state.shared_memory, 
                                    action_context=action_context, 
                                    debug=action_context.debug,
                                    ui_option=action_context.ui_option
                                )
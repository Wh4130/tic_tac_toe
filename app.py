import streamlit as st
import numpy as np

from utils_st import render_sidebar, render_global_memory
from tictactoe import TicTacToe_GAME, initialize_session_state


from components.game import ActionContext, Memory
from config import MAX_HISTORY
from components.frame import AgentRegistry
from ai_player import AI_PLAYER_MOVE





with open("style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


st.title("Tic-Tac-Toe")

# * Session state initialization
initialize_session_state()
if "difficulty" not in st.session_state:
    st.session_state['difficulty'] = "easy"
if "debug_mode" not in st.session_state:
    st.session_state['debug_mode'] = False
if "shared_memory" not in st.session_state:
    st.session_state.shared_memory = Memory(max_history=MAX_HISTORY)
if "global_memory" not in st.session_state:
    st.session_state["global_memory"] = []


# * sidebar
render_sidebar()

# * Instantiate a TicTacToeGame object
game = TicTacToe_GAME()

registry = AgentRegistry()
action_context = ActionContext(agent_registry = registry, 
                               debug = st.session_state['debug_mode'],
                               ui_option = "streamlit",
                               properties = {"game": game})


# * Render player
if not st.session_state['winner']:
    st.subheader(f"It's your move, player {st.session_state['current_player']}")
else:
    st.subheader(f"GAME OVER!")



GAME_TAB, MEMORY_TAB = st.tabs(["Game", "Memory"])


# * Game board
with GAME_TAB:
    game.main()

    # * AI play if the player is 2 and the mode is Play with AI
    if ((st.session_state['current_player'] == 2) 
        and (not st.session_state['winner'])
        and (st.session_state['play_mode'] == "Play with AI")
        ):
        AI_PLAYER_MOVE(action_context)
        st.rerun()

    if st.session_state['winner']:
        st.balloons()
        st.toast(f"Player {st.session_state['winner']} won!")
        with st.container():
            if st.button("Start over", width = "stretch", type = "primary"):
                for _ in st.session_state:
                    del st.session_state[_]
                st.rerun()

with MEMORY_TAB:
    render_global_memory()


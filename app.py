import streamlit as st
import numpy as np

from utils_st import render_sidebar, render_global_memory
from tictactoe import TicTacToe_GAME, initialize_session_state


from components.game import ActionContext, Memory
from config import MAX_HISTORY
from components.frame import AgentRegistry
from ai_player import AI_PLAYER_MOVE



st.set_page_config(page_title = "Upgraded Tic-Tac-Toe", 
                   page_icon = ":material/chess_king:", 
                   layout="centered", 
                   initial_sidebar_state = "auto", 
                   menu_items={
        'Get Help': None,
        'Report a bug': "mailto:huang0jin@gmail.com",
        'About': """
- Developed by - **[Wally, Huang Lin Chun](https://antique-turn-ad4.notion.site/Wally-Huang-Lin-Chun-182965318fa7804c86bdde557fa376f4)**"""
    })

with open("style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


st.title("Tic-Tac-Toe")

with st.expander("Rules"):
    st.markdown("""
- Player 1 places blue mark, and player 2 places orange mark. Player 1 always goes first.
- Each player puts a mark on the board for each move.
- The first player who gets four marks in a row, column, or diagonal wins.
- :red[When you have four marks on the board already, the oldest mark would be removed after the next move. The oldest mark would be of diamond shape].
""")


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



GAME_TAB, HISTORY_TAB, MEMORY_TAB = st.tabs(["Game","Game History",  "Memory"])


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
        with st.container():
            if st.button("Start over", width = "stretch", type = "primary"):
                for _ in st.session_state:
                    del st.session_state[_]
                st.rerun()
            

with MEMORY_TAB:
    render_global_memory()

with HISTORY_TAB:
    if not st.session_state['winner']:
        st.warning("The game is not ending yet!")
    else:
        st.header(":material/history_2: Game History")

        @st.fragment
        def HISTORY():
            game.render_history()
        HISTORY()




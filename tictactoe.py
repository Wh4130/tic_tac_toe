import streamlit as st
import numpy as np
import time

def initialize_session_state():
    if "game_state" not in st.session_state:
        st.session_state['game_state'] = np.array([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])

    if "player_move" not in st.session_state:
        st.session_state['player_move'] = {1: [], 2: []}

    if "game_history" not in st.session_state:
        st.session_state['game_history'] = {
            "canva": [],
            "move": []
        }

    if "current_player" not in st.session_state:
        st.session_state['current_player'] = 1

    if "winner" not in st.session_state:
        st.session_state['winner'] = None

    if "disabled" not in st.session_state:
        st.session_state['disabled'] = np.array([
            [False, False, False, False],
            [False, False, False, False],
            [False, False, False, False],
            [False, False, False, False]
            
        ])

    if "play_mode" not in st.session_state:
        st.session_state['play_mode'] = "Play with AI"

    if "history_current_page" not in st.session_state:
        st.session_state['history_current_page'] = 0

    if "history_auto_play" not in st.session_state:
        st.session_state['history_auto_play'] = True



    


class TicTacToe_GAME:
    def __init__(self) -> None:
        pass 

    def get_cell_content(self, player):
        if player == 1:
            return "🔵"
        elif player == 2:
            return "🟠"
        elif player == -1:
            return "🔹"
        elif player == -2:
            return "🔸"
        else:
            return " "


    def end_game(self):
        st.session_state['disabled'] = np.array([
            [True, True, True, True],
            [True, True, True, True],
            [True, True, True, True],
            [True, True, True, True]
        ])
    

    def disable_button(self, row, col):
        st.session_state['disabled'][row, col] = True

    def remove_oldest_move(self, player):
        
        if len(st.session_state['player_move'][player]) > 4:
            st.session_state['game_state'][st.session_state['player_move'][player][0]] = 0
            st.session_state['disabled'][st.session_state['player_move'][player][0]] = False
            st.session_state['player_move'][player].pop(0)

        if len(st.session_state['player_move'][player]) == 4:
            st.session_state['game_state'][st.session_state['player_move'][player][0]] = -1 * player
            

    def check_win(self):
        for i in range(4):
            # * check horizontal and vertical lines
            row_i = st.session_state['game_state'][i]
            col_i = st.session_state['game_state'][:, i]
            
            if all(row_i == [1, 1, 1, 1]) or all(col_i == [1, 1, 1, 1]):
                st.session_state['winner'] = 1
            elif all(row_i == [2, 2, 2, 2]) or all(col_i == [2, 2, 2, 2]):
                st.session_state['winner'] = 2
        
        # * check diagnoal
        diag = np.diag(st.session_state['game_state'])
        inverse_diag = np.diag(st.session_state['game_state'][::-1])
        if all(diag == [1, 1, 1, 1]) or all(inverse_diag == [1, 1, 1, 1]):
            st.session_state['winner'] = 1
        elif all(diag == [2, 2, 2, 2]) or all(inverse_diag == [2, 2, 2, 2]):
            st.session_state['winner'] = 2

        if st.session_state['winner']:
            st.balloons()


    def append_to_history(self, move: tuple):
        st.session_state['game_history']['canva'].append(st.session_state['game_state'].copy())
        st.session_state['game_history']['move'].append(
            (st.session_state['current_player'], move))


    def make_move(self, row, col, player):
        # make a move
        st.session_state['game_state'][row, col] = player
        

        # disable the button
        self.disable_button(row, col)

        

        # check win status
        self.check_win()

        if st.session_state['winner']:
            self.end_game()

        else:
            # append player move history if game not ended
            st.session_state['player_move'][player].append((row, col))

            # change player
            st.session_state['current_player'] = 3 - player

        # remove the oldest move (if the history move > 4)
        self.remove_oldest_move(player)

        # append to history
        self.append_to_history((row, col))
        

    def main(self):
        # * disable logic
        disabled = st.session_state['disabled']
        if (st.session_state['play_mode'] == "Play with AI") and (st.session_state['current_player'] == 2):
            disabled = np.array([
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
            ])

        for row in range(4):
            with st.container():
                COLS = st.columns(4)
            for col in range(4):
                with COLS[col]:
                    st.button(f"{self.get_cell_content(st.session_state['game_state'][row, col])}", 
                            key = f"{row}_{col}", 
                            disabled = disabled[row, col], 
                            on_click = self.make_move, args = (row, col, st.session_state['current_player']))
        
        if st.session_state['winner']:
            st.success(f"**Player {st.session_state['winner']} wins!**")

    @st.fragment        
    def render_history(self):

        i = st.slider("Move", min_value = 1, max_value = len(st.session_state['game_history']['canva']), value = 1) - 1

        history = st.session_state['game_history']['canva'][i]
        player_move = st.session_state['game_history']['move'][i]

        st.info(f"Player {player_move[0]} selected {player_move[1]}")
        if i >= len(st.session_state['game_history']['canva']) - 1:
            st.success(f"Player {st.session_state['current_player']} won the game!")

        
        
        for row in range(4):
            with st.container():
                COLS = st.columns(4)
            for col in range(4):
                with COLS[col]:
                    st.button(f"{self.get_cell_content(history[row, col])}", 
                            key = f"{i}:{row}_{col}_manual", 
                            disabled = True)
        

        



# init_session()

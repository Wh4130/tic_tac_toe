import streamlit as st
import numpy as np

def initialize_session_state():
    if "game_state" not in st.session_state:
        st.session_state['game_state'] = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

    if "game_history" not in st.session_state:
        st.session_state['game_history'] = {1: [], 2: []}

    if "current_player" not in st.session_state:
        st.session_state['current_player'] = 1

    if "winner" not in st.session_state:
        st.session_state['winner'] = None

    if "disabled" not in st.session_state:
        st.session_state['disabled'] = np.array([
            [False, False, False],
            [False, False, False],
            [False, False, False]
        ])

    if "play_mode" not in st.session_state:
        st.session_state['play_mode'] = "Play with AI"


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
            [True, True, True],
            [True, True, True],
            [True, True, True]
        ])
    

    def disable_button(self, row, col):
        st.session_state['disabled'][row, col] = True

    def remove_oldest_move(self, player):
        
        if len(st.session_state['game_history'][player]) > 3:
            st.session_state['game_state'][st.session_state['game_history'][player][0]] = 0
            st.session_state['disabled'][st.session_state['game_history'][player][0]] = False
            st.session_state['game_history'][player].pop(0)

        if len(st.session_state['game_history'][player]) == 3:
            st.session_state['game_state'][st.session_state['game_history'][player][0]] = -1 * player
            

    def check_win(self):
        for i in range(3):
            # * check horizontal and vertical lines
            row_i = st.session_state['game_state'][i]
            col_i = st.session_state['game_state'][:, i]
            
            if all(np.abs(row_i) == [1, 1, 1]) or all(np.abs(col_i) == [1, 1, 1]):
                st.session_state['winner'] = 1
            elif all(np.abs(row_i) == [2, 2, 2]) or all(np.abs(col_i) == [2, 2, 2]):
                st.session_state['winner'] = 2
        
        diag = np.diag(st.session_state['game_state'])
        inverse_diag = np.diag(st.session_state['game_state'][::-1])
        if all(np.abs(diag) == [1, 1, 1]) or all(np.abs(inverse_diag) == [1, 1, 1]):
            st.session_state['winner'] = 1
        elif all(np.abs(diag) == [2, 2, 2]) or all(np.abs(inverse_diag) == [2, 2, 2]):
            st.session_state['winner'] = 2

    def make_move(self, row, col, player):
        # make a move
        st.session_state['game_state'][row, col] = player

        # disable the button
        self.disable_button(row, col)

        # check win status
        self.check_win()

        if st.session_state['winner']:
            self.end_game()
            return st.session_state['winner']

        else:
            # append game history if game not ended
            st.session_state['game_history'][player].append((row, col))

            # remove the oldest move (if the history move > 3)
            self.remove_oldest_move(player)

            # change player
            st.session_state['current_player'] = 3 - player


    def main(self):
        # * disable logic
        disabled = st.session_state['disabled']
        if (st.session_state['play_mode'] == "Play with AI") and (st.session_state['current_player'] == 2):
            disabled = np.array([
                [True, True, True],
                [True, True, True],
                [True, True, True]
            ])

        for row in range(3):
            with st.container():
                COLS = st.columns(3)
            for col in range(3):
                with COLS[col]:
                    st.button(f"{self.get_cell_content(st.session_state['game_state'][row, col])}", 
                            key = f"{row}_{col}", 
                            disabled = disabled[row, col], 
                            on_click = self.make_move, args = (row, col, st.session_state['current_player']))
        
        if st.session_state['winner']:
            st.success(f"**Player {st.session_state['winner']} wins!**")


# init_session()

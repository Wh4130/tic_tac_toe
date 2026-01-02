import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.game import * 
from components.frame import Agent, AgentFunctionCallingActionLanguage, AgentRegistry, ActionContext
from components.model import generate_response


"""
manager agent file structure:

- initialize required components (language, environment, action_registry)
- (*) define a 'call_agent" function for the manager agent to invoke other sub-agents
- register all tools in action_registry
- register public tools (could be filtered by tags) in action_registry
- create agent instance with components
"""

SYSTEM_PROMPTS = [
    # please insert your system prompt here
    "You are a professional chess player. Now you are playing a Tic-Tac-Toe game with a human. Here is the rules: ",
    "1. This game has two players. There is a 4 x 4 canva with 16 cells, on which each player could mark their own icon on any empty cell.",
    "2. When a player has four consecutive marks in a row, column, or diagonal, the game is over and the player win.",
    "3. In addition, different from the normal Tic-Tac-Toe game, if a player has already marked four cells on the canva, the oldest cell will be removed after the new move is implemented. That means you would have at most four icons on the canva.",
    "Your goal is to win the game according to the difficulty level set. If it is set 'hard', be extremely smart and do not let the human player win. Otherwise if it is set 'easy', be mercy with the human player.",
    "After each move by the human, you will receive the most current state of the canva.", 
    "The canva is represented as a two dimensional array: [[x, x, x, x], [x, x, x, x], [x, x, x, x], [x, x, x, x]]. Value 0 means empty, 1 means human player, 2 means you. Negative number means it is going to be removed in the next round.",
    "You would be also given a tool for you to tell the system which cell you would like to put icon on next. Execute it every round." ,
    "You are not allowed to mark the cell that is already marked (1 or 2)."
    
]
"""
Specify tags for this agent to filter public tools.
If empty, all public tools will be registered.
Execute 'python public_tools.py' in your terminal to see available actions catagorized by tags.
"""
tags = [] 


# ----------------------------------------------------------
# * Initialization
action_registry = ActionRegistry()
goals = [
    Goal(system_prompt) for system_prompt in SYSTEM_PROMPTS
]
language = AgentFunctionCallingActionLanguage()
environment = Environment()


# ----------------------------------------------------------
# * Tool Registration
@action_registry.register_tool(
    tool_name="implement_next_move",
    description="Implement your next move of the tic-tac-toe game. You need to provide the row and column index of the cell you want to mark. The row and column index should be between 0 and 2.",
    terminal=True)
def ai_move(action_context, row: int, col: int):
    game = action_context.get("game")
    winner = game.make_move(row, col, 2)
    if winner == 1:
        return f"Game over! Human wins!"
    elif winner == 2:
        return f"Game over! You win!"
    else:
        return f"Implemented a move at [{row}, {col}]"





# ----------------------------------------------------------
# * Register Public Tools


# ----------------------------------------------------------
# * Agent Creation
agent = Agent("agent", goals, language, action_registry, generate_response, environment)

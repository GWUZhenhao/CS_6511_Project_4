import pickle
import tkinter as tk
import operation
import gridworld
import matplotlib.pyplot as plt
import time

UNIT = 50
HEIGHT = 40
WIDTH = 40

class Env(tk.Tk):
    def __init__(self):
        super(Env, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('Q Learning')
        self.canvas = self._build_canvas()
        self.texts = []

    def _build_canvas(self):
        canvas = tk.Canvas(self, bg='white',
                           height=HEIGHT * UNIT,
                           width=WIDTH * UNIT)

        for c in range(0, WIDTH * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, HEIGHT * UNIT
            canvas.create_line(x0, y0, x1, y1)
        for r in range(0, HEIGHT * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, HEIGHT * UNIT, r
            canvas.create_line(x0, y0, x1, y1)


        canvas.pack()

        return canvas

    def render(self):
        time.sleep(0.5)
        self.update()


def print_q_table(q_table, env):

    # Creat an empty canvas with 40*40 grid

    # For each grid, draw the four q value
    size = 5
    style = 'normal'
    anchor = "nw"
    font = 'Helvetica'
    for i in env.texts:
        env.canvas.delete(i)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            for action in range(0, 4):
                state = [i, j]
                if str(state) in q_table.keys():
                    temp = q_table[str(state)][action]
                    if action == 0:
                        origin_x, origin_y = 4, 21
                    elif action == 1:
                        origin_x, origin_y = 43, 21
                    elif action == 2:
                        origin_x, origin_y = 21, 3
                    else:
                        origin_x, origin_y = 21, 39

                    x, y = origin_y + (UNIT * i), origin_x + (UNIT * j)
                    font = (font, str(size), style)
                    text = env.canvas.create_text(int(x), int(y), fill="black", text=round(temp, 3), font=font, anchor=anchor)

                    env.texts.append(text)
    env.canvas.update()
    print()


if __name__ == '__main__':

    teamId = 1304  # Team Zhenhao
    world = 0
    agent = gridworld.q_learning([0, 1, 2, 3])
    op = operation.operation(teamId=teamId)
    actions = ['N', 'S', 'W', 'E']
    env = Env()

    # Reset the game at first
    op.reset_my_team()
    # print(op.get_runs(10))
    # print(op.get_location())
    print('Try to enter a new world, worldId = {}.'.format(world))
    print(op.enter_a_world(world))

    for episode in range(1):
        # Initialize the game
        op.reset_my_team()
        op.enter_a_world(world)
        state = op.get_location()['state']
        state = [int(i) for i in state.split(':')]

        while True:

            # Make a move based on the RL algorithm
            index_action = agent.get_action(str(state))
            action = actions[index_action]
            move_result = op.make_a_move(worldId=world, move=action)
            reward = move_result['reward']
            print(move_result)

            # The conditional statement to stop
            if move_result['newState'] == None:
                # Before stop, we need update the Q value for the current state
                # current Q value = previous Q value + learning_rate *（reward - previous Q value）
                agent.q_table[str(state)][index_action] += agent.learning_rate * (reward - agent.q_table[str(state)][index_action])
                break

            # Update Q table for the RL algorithm based on the rewards
            new_state = [int(i) for i in move_result['newState'].values()]
            agent.learn(str(state), index_action, reward, str(new_state))
            state = new_state


            # Another way to stop
            # if int(op.get_location()['world']) == -1:
            #     break
            print_q_table(agent.q_table, env)
        print(agent.q_table)

    # Save the q_table we trained
    with open("q_table.pkl", "wb") as pkl_handle:
        pickle.dump(agent.q_table, pkl_handle)
    print('finished')

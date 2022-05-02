import copy
import os.path
import pickle
import tkinter as tk
import operation
import gridworld
import numpy as np
import time
import json

UNIT = 50
HEIGHT = 40
WIDTH = 40

class Env(tk.Tk):
    def __init__(self):
        super(Env, self).__init__()
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

# Save the q_table with json
def save_q_table(agent, num_world):
    dict_q_table = {key:agent.q_table[key] for key in agent.q_table.keys()}
    with open("q_table_{}.json".format(num_world), "w") as outfile:
        json.dump(dict_q_table, indent=4, sort_keys=True,fp=outfile)

def load_q_table(agent, num_world):
    if os.path.exists('q_table_{}.json'.format(num_world)) == False:
        return agent
    with open('q_table_{}.json'.format(num_world)) as json_file:
        q_table = json.load(json_file)
    for key in q_table.keys():
        agent.q_table[key] = q_table[key]
    return agent

def print_q_table(q_table, env):
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
                    if temp > 10 or temp < -10:
                        font = (font, '20', style)
                        text = env.canvas.create_text(int(x), int(y), fill="red", text=round(temp, 3), font=font,
                                                      anchor=anchor)
                    else:
                        text = env.canvas.create_text(int(x), int(y), fill="black", text=round(temp, 3), font=font,
                                                      anchor=anchor)

                    env.texts.append(text)
    env.canvas.update()
    print()

def find_the_max_state(q_table):
    max_values = -100000
    max_key = None
    for key in q_table.keys():
        value = np.sum(q_table[key])
        if value > max_values:
            max_key = key
            max_values = value
    return max_key


if __name__ == '__main__':

    teamId = 1304  # Team Zhenhao
    world = 8
    agent = gridworld.q_learning([0, 1, 2, 3])
    op = operation.operation(teamId=teamId)
    actions = ['N', 'S', 'W', 'E']
    # env = Env()

    # Reset the game at first
    op.reset_my_team()
    # print(json.dumps(op.get_runs(10), indent = 4))
    # print(op.get_location())
    print('Try to enter a new world, worldId = {}.'.format(world))
    print(op.enter_a_world(world))

    for episode in range(10):

        # count for approaching
        count_approaching = 0

        # Initialize the game
        op.reset_my_team()
        op.enter_a_world(world)
        state = op.get_location()['state']
        state = [int(i) for i in state.split(':')]

        # load the q_table:
        agent = load_q_table(agent, world)

        # If we find a very good point, just approaching it
        if len(agent.q_table) == 0:
            pass
        elif np.sum(agent.q_table[find_the_max_state(agent.q_table)]) > 1000:
            target_state = find_the_max_state(agent.q_table)
            while True:
                # Make a move based on the RL algorithm
                count_approaching += 1
                print('approaching...')
                index_action = agent.approaching(target_state=target_state, current_state=str(state))
                # If the q score of current action is too low, doesn't use approach for this state.
                if agent.q_table[str(state)][index_action] < -10:
                    index_action = agent.get_action(str(state))
                if count_approaching >= 40:
                    index_action = agent.get_action(str(state))
                action = actions[index_action]
                move_result = op.make_a_move(worldId=world, move=action)
                print(move_result)
                reward = move_result['reward']


                # The conditional statement to stop
                if move_result['newState'] == None:
                    # Before stop, we need update the Q value for the current state
                    # current Q value = previous Q value + learning_rate *（reward - previous Q value）
                    # agent.q_table[str(state)][index_action] += agent.learning_rate * (
                    #             reward - agent.q_table[str(state)][index_action])
                    # current Q value in four directions = reward
                    for i in range(4):
                        agent.q_table[str(state)][i] = reward
                    break


                # Update Q table for the RL algorithm based on the rewards
                new_state = [int(i) for i in move_result['newState'].values()]
                agent.learn(str(state), index_action, reward, str(new_state))
                state = new_state
            print(agent.q_table)
            save_q_table(agent, world)
            continue

        while True:

            # Make a move based on the RL algorithm
            index_action = agent.get_action(str(state))
            action = actions[index_action]
            move_result = op.make_a_move(worldId=world, move=action)
            print(move_result)
            reward = move_result['reward']


            # The conditional statement to stop
            if move_result['newState'] == None:
                # Before stop, we need update the Q value for the current state
                # current Q value = previous Q value + learning_rate *（reward - previous Q value）
                # agent.q_table[str(state)][index_action] += agent.learning_rate * (reward - agent.q_table[str(state)][index_action])
                # current Q value in four directions = reward
                for i in range(4):
                    agent.q_table[str(state)][i] = reward
                break

            # Update Q table for the RL algorithm based on the rewards
            new_state = [int(i) for i in move_result['newState'].values()]
            agent.learn(str(state), index_action, reward, str(new_state))
            state = new_state


            # Another way to stop
            # if int(op.get_location()['world']) == -1:
            #     break

            # print_q_table(agent.q_table, env)
        print(agent.q_table)

        # Save the q_table we trained
        save_q_table(agent, world)
    print('finished')
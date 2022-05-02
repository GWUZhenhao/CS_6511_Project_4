import numpy as np
import random
from environment import Env
from collections import defaultdict

class q_learning():
    def __init__(self, actions):
        # actions = [0, 1, 2, 3] :  ['North', 'South', 'West', 'East']
        self.actions = actions
        self.learning_rate = 0.2
        self.Lambda = 0.9
        # ε
        # self.epsilon = 0.1
        # 建立一个以State为行、Action('North', 'South', 'West', 'East')为列的Q-Table
        self.q_table = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])

    # 更新q值
    def learn(self, state, action, reward, next_state):
        # 现在的Q值 = 原来的Q值 + 学习率 *（立即回报 + Lambda * 后继状态的最大Q值 - 原来的Q值）
        self.q_table[state][action] += self.learning_rate * (reward + self.Lambda * max(self.q_table[next_state]) - self.q_table[state][action])

    '''
    # ε-greedy策略 https://blog.csdn.net/mamiyahasaki/article/details/121927048
    def get_action(self, state):
        # (0,1)间随机，ε = 0.1  0.1概率随机，0.9概率贪心
        if np.random.rand() < self.epsilon:
            # 随机一个方向
            action = np.random.choice(self.actions)
        else:
            # 贪心，取q_table中q值最大的
            max_list = []
            max_value = self.q_table[state][0]
            for index, value in enumerate(self.q_table[state]):
                if value > max_value:
                    max_list = []
                    max_value = value
                    max_list.append(index)
                elif value == max_value:
                    max_list.append(index)
            action = random.choice(max_list)
        return action
        '''

    def approaching(self, target_state, current_state):
        target_state_x = int(target_state.split(',')[0][1:])
        target_state_y = int(target_state.split(',')[1][1:-1])
        current_state_x = int(current_state.split(',')[0][1:])
        current_state_y = int(current_state.split(',')[1][1:-1])

        x_diff = target_state_x - current_state_x

        if x_diff > 0:
            return 3
        if x_diff < 0:
            return 2

        y_diff = target_state_y - current_state_y

        if y_diff > 0:
            return 0
        if y_diff < 0:
            return 1

        return self.get_action(current_state)

    # This is the get_action function without epsilon
    def get_action(self, state):
        # 贪心，取q_table中q值最大的
        max_list = []
        max_value = self.q_table[state][0]
        for index, value in enumerate(self.q_table[state]):
            if value > max_value:
                max_list = []
                max_value = value
                max_list.append(index)
            elif value == max_value:
                max_list.append(index)
        action = random.choice(max_list)
        return action

if __name__ == '__main__':
    env = Env()
    agent = q_learning([0, 1, 2, 3])
    for episode in range(100):
        state = env.reset()

        while True:
            env.render()

            action = agent.get_action(str(state))
            next_state, reward, done = env.step(action)

            agent.learn(str(state), action, reward, str(next_state))

            state = next_state
            env.print_value_all(agent.q_table)

            if done:
                break

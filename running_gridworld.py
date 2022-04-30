import operation
import gridworld
import json

if __name__ == '__main__':

    teamId = 1304  # Team Zhenhao
    world = 0
    agent = gridworld.q_learning([0, 1, 2, 3])
    op = operation.operation(teamId=teamId)
    actions = ['N', 'S', 'W', 'E']

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

        print(agent.q_table)
    print('finished')
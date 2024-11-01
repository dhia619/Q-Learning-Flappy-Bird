import numpy as np
import pygame
class Agent:
    def __init__(self,num_states,num_actions):
        self.Qtable = np.random.rand(num_states, num_actions)
        self.clock = pygame.time.Clock()
        # Training parameters
        self.n_training_episodes = 50
        self.learning_rate = 0.7

        # Evaluation parameters
        self.n_eval_episodes = 100      

        # Environment parameters
        self.gamma = 0.95              

        # Exploration parameters
        self.max_epsilon = 1.0           
        self.min_epsilon = 0.05           
        self.decay_rate = 0.000005        

    def get_state_index(self, state):
        bird_y, dist_x, dist_y, _ = state
        # Discretize each component
        """ Assuming screen height is 600 """
        discretized_bird_y = bird_y // 60  # 10 possible values (0-9)
        discretized_dist_x = dist_x // 60  # 10 possible values (0-9)
        discretized_dist_y = dist_y // 30  # 10 possible values (0-9)

        # Combine into a unique state index
        return (discretized_bird_y * 10 * 10) + (discretized_dist_y * 10) + discretized_dist_x

    def epsilon_greedy_policy(self, state_index, epsilon):
        random_int = np.random.uniform(0, 1)
        if random_int > epsilon:
            action = np.argmax(self.Qtable[state_index])
        else:
            action = np.random.choice([0, 1])
        return action

    def greedy_policy(self, state_index):
        return np.argmax(self.Qtable[state_index])
    
    def train(self, env):
        for episode in range(self.n_training_episodes):
            print("episode :", episode)
            print("score :", env.score)
            epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.decay_rate * episode)
            env.reset_game()
            state = env.state()
            done = False
            while not done:
                state_index = self.get_state_index(state)
                action = self.epsilon_greedy_policy(state_index, epsilon)
                new_state, reward, done= env.run_step(action)
                env.render()
                env.clock.tick(120)
                new_state_index = self.get_state_index(new_state)            
                # Update Q-table using the Q-learning update rule
                self.Qtable[state_index][action] += self.learning_rate * (reward + self.gamma * np.max(self.Qtable[new_state_index]) - self.Qtable[state_index][action])
                state = new_state

        self.save()

    def save(self):
        np.save("q_table.npy", self.Qtable)

    def load(self):
        self.Qtable = np.load("q_table.npy")
    
    def exploit(self, env):            
        env.reset_game()
        state = env.state()
        done = False

        while not done:
            state_index = self.get_state_index(state)
            action = self.greedy_policy(self.Qtable,state_index)
            new_state, reward, done = env.run_step(action)
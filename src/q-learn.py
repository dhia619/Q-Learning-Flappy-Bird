from game import Game
import numpy as np

def initializeQ_table(num_states, num_actions):
    q_table = np.zeros((num_states, num_actions))
    return q_table

def discretize_state(state_values, num_bins=10, max_values=None):
    # If max_values is not provided, determine it from state_values
    if max_values is None:
        max_values = [max(values) for values in state_values]
    
    # Create a list to store the discretized states
    discretized_states = []
    
    for value, max_value in zip(state_values, max_values):
        # Define the edges of the bins
        bin_edges = np.linspace(0, max_value, num_bins + 1)
        
        # Use np.digitize to find the bin index for the value
        bin_index = np.digitize(value, bin_edges) - 1  # Subtract 1 for zero-based index
        
        # Ensure the index stays within the bounds of the bins
        if bin_index < 0:
            bin_index = 0
        elif bin_index >= num_bins:
            bin_index = num_bins - 1
        
        discretized_states.append(bin_index)
    
    return tuple(discretized_states)

def state_to_index(state):
    bins = state[:-1]  # The first five elements
    bird_status = state[-1]  # The last element

    # Calculate the index for the first 5 states
    index = 0
    for i in range(len(bins)):
        index += bins[i] * (10 ** i)  # Each bin has 10 options
    
    # Adjust index for bird status
    index = index * 2 + bird_status  # Multiply by 2 to account for bird status
    
    return index

def epsilon_greedy_policy(Qtable, state, epsilon):
  random_int = np.random.uniform(0,1)
  if random_int > epsilon:
    state_index = state_to_index(state)
    action = np.argmax(Qtable[state_index])
  else:
    action = np.random.randint(0,1)
  return action

""" 
either tap or not so we have 2 actions
and we have 4 states 3 of them will be descritized to a range (0 to 9) and the last state is either 0 or 1
Total_States=10^3x2=2000 states
"""

q_table = initializeQ_table(2000, 2)

# Training parameters
n_training_episodes = 10000
learning_rate = 0.7        

# Evaluation parameters
n_eval_episodes = 100      

# Environment parameters
env_id = "FrozenLake-v1"   
max_steps = 99             
gamma = 0.95               
eval_seed = []             

# Exploration parameters
max_epsilon = 1.0           
min_epsilon = 0.05           
decay_rate = 0.0005           

def train(n_training_episodes, min_epsilon, max_epsilon, decay_rate, env, max_steps, Qtable):
  for episode in range(n_training_episodes):
 
    epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*episode)
    step = 0
    done = False

    # repeat
    for step in range(max_steps):
    
        action = epsilon_greedy_policy(Qtable, state, epsilon)
        new_state, reward, done, info = env.step(action)
        state = state_to_index(state)

        Qtable[state][action] = Qtable[state][action] + learning_rate * (reward + gamma * np.max(Qtable[state_to_index(new_state)]) - Qtable[state][action])

        # If done, finish the episode
        if done:
            break
        
        # Our state is the new state
        state = new_state
    
    return Qtable



from agent import *
from game import *
from os import path
from threading import Thread


env = Game()
agent = Agent(2000,2)

if path.exists("q_table.npy"):
    agent.load()

# Multithreading to avoid preview window freeze
train_thread = Thread(target=agent.train, args=(env,))
train_thread.start()
env.mainloop()
train_thread.join()

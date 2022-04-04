import argparse
import logging
import numpy as np
import torch

from backend_players.players.decision_transformers.create_dataset import create_dataset
from backend_players.players.decision_transformers.mingpt.model_atari import GPT, GPTConfig
from backend_players.players.decision_transformers.mingpt.trainer_atari import Trainer, TrainerConfig
from backend_players.players.decision_transformers.mingpt.utils import set_seed
from torch.utils.data import Dataset

parser = argparse.ArgumentParser()
parser.add_argument('--seed', type=int, default=123)
parser.add_argument('--context_length', type=int, default=30)
parser.add_argument('--epochs', type=int, default=5)
parser.add_argument('--model_type', type=str, default='reward_conditioned')
parser.add_argument('--num_steps', type=int, default=500000)
parser.add_argument('--num_buffers', type=int, default=50)
parser.add_argument('--game', type=str, default='Breakout')
parser.add_argument('--batch_size', type=int, default=128)
parser.add_argument('--trajectories_per_buffer', type=int, default=10, help='Number of trajectories to sample from each of the buffers.')
parser.add_argument('--data_dir_prefix', type=str, default='./dqn_replay/')

#args = parser.parse_args()

#set_seed(args.seed)

class StateActionReturnDataset(Dataset):

    def __init__(self, data, block_size, actions, done_idxs, rtgs, timesteps):        
        self.block_size = block_size
        self.vocab_size = max(actions) + 1
        self.data = data
        self.actions = actions
        self.done_idxs = done_idxs
        self.rtgs = rtgs
        self.timesteps = timesteps
    
    def __len__(self):
        return len(self.data) - self.block_size

    def __getitem__(self, idx):
        block_size = self.block_size // 3
        done_idx = idx + block_size
        for i in self.done_idxs:
            if i > idx: # first done_idx greater than idx
                done_idx = min(int(i), done_idx)
                break
        idx = done_idx - block_size
        states = torch.tensor(np.array(self.data[idx:done_idx]), dtype=torch.float32).reshape(block_size, -1) # (block_size, 4*84*84)
        states[states == -1] = 0
        states[states == 0] = 0.5
        states[states == 1] = 1
        # NO NORMALIZATION
        # states = states / 255.
        actions = torch.tensor(self.actions[idx:done_idx], dtype=torch.long).unsqueeze(1) # (block_size, 1)
        rtgs = torch.tensor(self.rtgs[idx:done_idx], dtype=torch.float32).unsqueeze(1)
        timesteps = torch.tensor(self.timesteps[idx:idx+1], dtype=torch.int64).unsqueeze(1)

        return states, actions, rtgs, timesteps

#obss, actions, returns, done_idxs, rtgs, timesteps = create_dataset(args.num_buffers, args.num_steps, args.game, args.data_dir_prefix, args.trajectories_per_buffer)
obss, actions, returns, done_idxs, rtgs, timesteps = create_dataset(1, 35000, '/media/kinrre/HDD/modelos/connect4/modelo_returns/replay_logs', (6, 7), 100)

# set up logging
logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
)

train_dataset = StateActionReturnDataset(obss, 10*3, actions, done_idxs, rtgs, timesteps)

mconf = GPTConfig(train_dataset.vocab_size, train_dataset.block_size,
                  n_layer=6, n_head=8, n_embd=128, model_type='reward_conditioned', max_timestep=max(timesteps))
model = GPT(mconf)

# initialize a trainer instance and kick off training
#epochs = args.epochs
tconf = TrainerConfig(max_epochs=5, batch_size=64, learning_rate=6e-4,
                      lr_decay=True, warmup_tokens=512*2, final_tokens=2*len(train_dataset)*10*3,
                      num_workers=4, seed=123, model_type='reward_conditioned', game='Connect4', max_timestep=max(timesteps))
trainer = Trainer(model, train_dataset, None, tconf)

trainer.train()

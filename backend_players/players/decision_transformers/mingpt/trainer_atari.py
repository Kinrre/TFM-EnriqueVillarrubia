"""
The MIT License (MIT) Copyright (c) 2020 Andrej Karpathy

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

"""
Simple training loop; Boilerplate that could apply to any arbitrary neural network,
so nothing in this file really has anything to do with GPT specifically.
"""

import logging
import math
import numpy as np
import torch

from backend_players.players.decision_transformers.mingpt.connect4 import Connect4GameDT
from backend_players.players.decision_transformers.mingpt.utils import sample
from torch.utils.data.dataloader import DataLoader
from tqdm import tqdm

from backend_players.players.alphazero.MCTS import MCTS
from backend_players.players.alphazero.utils import dotdict

from backend_players.players.alphazero.connect4.connect4_game import Connect4Game
from backend_players.players.alphazero.connect4.keras.NNet import NNetWrapper

logger = logging.getLogger(__name__)


class TrainerConfig:
    # optimization parameters
    max_epochs = 10
    batch_size = 64
    learning_rate = 3e-4
    betas = (0.9, 0.95)
    grad_norm_clip = 1.0
    weight_decay = 0.1 # only applied on matmul weights
    # learning rate decay params: linear warmup followed by cosine decay to 10% of original
    lr_decay = False
    warmup_tokens = 375e6 # these two numbers come from the GPT-3 paper, but may not be good defaults elsewhere
    final_tokens = 260e9 # (at what point we reach 10% of original LR)
    # checkpoint settings
    ckpt_path = None
    num_workers = 0 # for DataLoader

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

class Trainer:

    def __init__(self, model, train_dataset, test_dataset, config):
        self.model = model
        self.train_dataset = train_dataset
        self.test_dataset = test_dataset
        self.config = config

        with open('backend_players/players/alphazero/examples/second_game.json') as f:
            content = f.read()
            
        self.game = Connect4GameDT(content)
        n1 = NNetWrapper(self.game, True)
        n1.load_checkpoint('/media/kinrre/HDD/modelos/connect4/modelo_returns', 'best.pth.tar')

        args1 = dotdict({'numMCTSSims': 25, 'cpuct': 1})
        mcts1 = MCTS(self.game, n1, args1)
        self.n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

        # take over whatever gpus are on the system
        self.device = 'cpu'
        if torch.cuda.is_available():
            self.device = torch.cuda.current_device()
            self.model = torch.nn.DataParallel(self.model).to(self.device)

    def save_checkpoint(self):
        # DataParallel wrappers keep raw model object in .module attribute
        raw_model = self.model.module if hasattr(self.model, "module") else self.model
        logger.info("saving %s", self.config.ckpt_path)
        # torch.save(raw_model.state_dict(), self.config.ckpt_path)

    def train(self):
        model, config = self.model, self.config
        raw_model = model.module if hasattr(self.model, "module") else model
        optimizer = raw_model.configure_optimizers(config)

        def run_epoch(split, epoch_num=0):
            is_train = split == 'train'
            model.train(is_train)
            data = self.train_dataset if is_train else self.test_dataset
            loader = DataLoader(data, shuffle=True, pin_memory=True,
                                batch_size=config.batch_size,
                                num_workers=config.num_workers)

            losses = []
            pbar = tqdm(enumerate(loader), total=len(loader)) if is_train else enumerate(loader)
            
            for it, (x, y, r, t) in pbar:
                # place data on the correct device
                x = x.to(self.device)
                y = y.to(self.device)
                r = r.to(self.device)
                t = t.to(self.device)

                # forward the model
                with torch.set_grad_enabled(is_train):
                    # logits, loss = model(x, y, r)
                    logits, loss = model(x, y, y, r, t)
                    loss = loss.mean() # collapse all losses if they are scattered on multiple gpus
                    losses.append(loss.item())

                if is_train:
                    # backprop and update the parameters
                    model.zero_grad()
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(model.parameters(), config.grad_norm_clip)
                    optimizer.step()

                    # decay the learning rate based on our progress
                    if config.lr_decay:
                        self.tokens += (y >= 0).sum() # number of tokens processed this step (i.e. label is not -100)
                        if self.tokens < config.warmup_tokens:
                            # linear warmup
                            lr_mult = float(self.tokens) / float(max(1, config.warmup_tokens))
                        else:
                            # cosine learning rate decay
                            progress = float(self.tokens - config.warmup_tokens) / float(max(1, config.final_tokens - config.warmup_tokens))
                            lr_mult = max(0.1, 0.5 * (1.0 + math.cos(math.pi * progress)))
                        lr = config.learning_rate * lr_mult
                        for param_group in optimizer.param_groups:
                            param_group['lr'] = lr
                    else:
                        lr = config.learning_rate

                    # report progress
                    pbar.set_description(f"epoch {epoch+1} iter {it}: train loss {loss.item():.5f}. lr {lr:e}")

            if not is_train:
                test_loss = float(np.mean(losses))
                logger.info("test loss: %f", test_loss)
                return test_loss

        # best_loss = float('inf')
        
        best_return = -float('inf')

        self.tokens = 0 # counter used for learning rate decay

        for epoch in range(config.max_epochs):
            run_epoch('train', epoch_num=epoch)
            # if self.test_dataset is not None:
            #     test_loss = run_epoch('test')

            # # supports early stopping based on the test loss, or just save always if no test set is provided
            # good_model = self.test_dataset is None or test_loss < best_loss
            # if self.config.ckpt_path is not None and good_model:
            #     best_loss = test_loss
            #     self.save_checkpoint()

            # -- pass in target returns
            if self.config.model_type == 'naive':
                eval_return = self.get_returns(0, True)
                eval_return = self.get_returns(0, False)
            elif self.config.model_type == 'reward_conditioned':
                if self.config.game == 'Breakout':
                    eval_return = self.get_returns(90)
                elif self.config.game == 'Seaquest':
                    eval_return = self.get_returns(1150)
                elif self.config.game == 'Qbert':
                    eval_return = self.get_returns(14000)
                elif self.config.game == 'Pong':
                    eval_return = self.get_returns(20)
                elif self.config.game == 'Connect4':
                    eval_return = self.get_returns(35, 0)
                    eval_return = self.get_returns(35, 1)
                    #eval_return = self.get_returns(35, 2)
                else:
                    raise NotImplementedError()
            else:
                raise NotImplementedError()

    def get_returns(self, ret, type_opponent):
        self.model.train(False)
        
        T_rewards, T_Qs = [], []
        done = True
        
        for i in range(50):
            state = self.game.reset()
            state = state.type(torch.float32).to(self.device).unsqueeze(0).unsqueeze(0)
            state[state == -1] = 0
            state[state == 0] = 0.5

            rtgs = [ret]
            
            # first state is from env, first rtg is target return, and first timestep is 0
            sampled_action = sample(self.model.module, state, 1, temperature=1.0, sample=True, actions=None, valid_actions=None,
                                    rtgs=torch.tensor(rtgs, dtype=torch.long).to(self.device).unsqueeze(0).unsqueeze(-1), 
                                    timesteps=torch.zeros((1, 1, 1), dtype=torch.int64).to(self.device))

            j = 0
            all_states = state
            actions = []
            
            while True:
                if done:
                    state, reward_sum, done = self.game.reset(), 0, False

                action = sampled_action.cpu().numpy()[0,-1]

                if self.game.player == -1:
                    # Random
                    if type_opponent == 0:
                        action = np.random.randint(self.game.getActionSize())
                        valids = self.game.getValidMoves2()
                    
                        while valids[action] != 1:
                            action = np.random.randint(self.game.getActionSize())
                    # Greedy
                    elif type_opponent == 1:
                        valid_moves = self.game.getValidMoves2()
                        win_move_set = set()
                        fallback_move_set = set()
                        stop_loss_move_set = set()
                        player_num = -1

                        for move, valid in enumerate(valid_moves):
                            if not valid: continue
                            if player_num == self.game.getGameEnded(*self.game.getNextState(self.game.board.np_pieces, player_num, move)):
                                win_move_set.add(move)
                            if -player_num == self.game.getGameEnded(*self.game.getNextState(self.game.board.np_pieces, -player_num, move)):
                                stop_loss_move_set.add(move)
                            else:
                                fallback_move_set.add(move)

                        if len(win_move_set) > 0:
                            ret_move = np.random.choice(list(win_move_set))
                            #print('Playing winning action %s from %s' % (ret_move, win_move_set))
                        elif len(stop_loss_move_set) > 0:
                            ret_move = np.random.choice(list(stop_loss_move_set))
                            #print('Playing loss stopping action %s from %s' % (ret_move, stop_loss_move_set))
                        elif len(fallback_move_set) > 0:
                            ret_move = np.random.choice(list(fallback_move_set))
                            #print('Playing random action %s from %s' % (ret_move, fallback_move_set))
                        else:
                            raise Exception('No valid moves remaining: %s' % self.game.stringRepresentation(state2))

                        action = ret_move
                    elif type_opponent == 2:
                        action = self.n1p(self.game.getCanonicalForm(self.game.board.np_pieces, self.game.player))

                actions += [sampled_action]
                state, reward, done = self.game.step(action)
                reward_sum += reward
                j += 1

                if done:
                    #print(state, action, reward_sum)
                    T_rewards.append(reward_sum)
                    break

                state = state.unsqueeze(0).unsqueeze(0).to(self.device)
                state[state == -1] = 0
                state[state == 0] = 0.5

                all_states = torch.cat([all_states, state], dim=0)

                rtgs += [rtgs[-1] - reward]

                valid_actions = self.game.getValidMoves2()
                
                # all_states has all previous states and rtgs has all previous rtgs (will be cut to block_size in utils.sample)
                # timestep is just current timestep
                sampled_action = sample(self.model.module, all_states.unsqueeze(0), 1, temperature=1.0, sample=True, 
                                        actions=torch.tensor(actions, dtype=torch.long).to(self.device).unsqueeze(1).unsqueeze(0),
                                        valid_actions=torch.tensor(valid_actions, dtype=torch.long).to(self.device).unsqueeze(0),
                                        rtgs=torch.tensor(rtgs, dtype=torch.long).to(self.device).unsqueeze(0).unsqueeze(-1), 
                                        timesteps=(min(j, self.config.max_timestep) * torch.ones((1, 1, 1), dtype=torch.int64).to(self.device)))
        
        #eval_return = sum(T_rewards) / 10.
        #print("target return: %d, eval return: %d" % (ret, eval_return))
        print(np.unique(T_rewards, return_counts=True))
        self.model.train(True)
        
        #return eval_return

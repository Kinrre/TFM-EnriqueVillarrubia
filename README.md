# TFM-EnriqueVillarrubia

The project is organised into the following directories, structured depending on the implemented agent:

* __decision-transformers.__ Decision Transformer agent implementation in PyTorch with charts of the evolution agent and the most important hyper-parameters included.
* __dqn.__ DQN agent development code in Tensorflow with the agent evolution chart.

The requirements and installation of the agents are covered in the next sections.

## Requirements

This master dissertation has been implemented entirely using the Python3 programming language and the pip package management system. The exact versions of the libraries are listed in the `TFM-EnriqueVillarrubia/requirements.txt` file and the rest of them are the following.

* Python3, 3.8.10.
* Pip, 22.1.2.

## Installation

First, it is necessary to clone the repository.

```
git clone https://github.com/Kinrre/TFM-EnriqueVillarrubia.git
```

After that, change to the directory and install the required libraries.

```
cd TFM-EnriqueVillarrubia && pip install -r requirements.txt
```

Now the installation has finished and it is possible to run both agents.

## Running the DQN agent

The configuration directory on the DQN agent is located in the `TFM-EnriqueVillarrubia/dqn/config/` directory if you want to change any hyperparameter. In order to run it, the command is:

```
python3 run.py
```

## Running the Decision Transformer agent

On the other hand, in the Decision Transformer agent, the hyperparameters are passed through the execution arguments which can be consulted as follows.

```
python3 run_dt_atari.py --help
```

To run it with the default hyperparameters, run the following instruction:

```
python3 run_dt_atari.py
```

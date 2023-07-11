# Minesweeper Solver
A simple knowledge-based AI agent that can draw inferences based on the state of the game board and make a safe move.

## Setup
Download the repository into your local machine or simply clone with `git clone https://github.com/karthik-NvY/CS50ai.git`. See [here](https://git-scm.com/downloads) to get git.
#### Python
Open you terminal and type in `python3 -V` to check if you have python installed. If you have it, you will see the verison of python and can skip to requirments.

In case you don't have python installed, you can choose one of following :
- Visit [here](https://www.python.org/downloads/) to download a latest version.
- If you have Homebrew installed, run `brew install python` in your terminal.
- On linux, run `sudo apt update` followed by `sudo apt install python3` in your terminal.

#### Requirements
requirements.txt contains the packages required for this project.
To install, make a copy of the file in your local machine or simply download the requirements.txt file.

In you terminal, run the following command: `pip3 install -r requirements.txt`
This will install the python packages required.

## Launch
To launch, simply run `python runner.py`. A new window pops up which contains a play button, onclicking, starts the game.
<p align="center">
<img width="300" alt="game window" src="https://github.com/karthik-NvY/CS50ai/assets/95777576/2f68adf2-e937-4977-aa37-40e9ba2058ec">
</p>

***Note:*** I have **not** implemented the pygame interactive interface, it was done by the CS50 team. I have coded the AI agent that draws inferences and updates the game. Thanks for the CS50 team for a wonderful experience.

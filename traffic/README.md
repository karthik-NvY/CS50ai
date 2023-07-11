
# Traffic Sign Recognition.
A neural network that can recognize the traffic sign shown in the image.

You can watch the NN in action [here](https://www.youtube.com/watch?v=de33G4lajk4&t=4s) on youtube.

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

#### Dataset
GTSRB is the data set containing numerous images of traffic signs along with labels. The neural net trains on this dataset. You can get the dataset [here](https://cdn.cs50.net/ai/2020/x/projects/5/gtsrb.zip).

## Launch
To launch, simply run `python traffic.py` which starts the training of the neural net. At the end, the NN is tested for accuracy which was around 95%.

## Log
Following are different architectures I tried for my NN to improve its accuracy.

#### Trial 0
I applied Convolution and MaxPooling twice followed by flattening the inputs to 1152 nodes.  
Then I used a Dense layer with 32 nodes as an additional hidden layer before
connecting to outputs.  
_Structure :_ `(Conv, Maxpool)x2 -> Flatten(None,1152)->Dense(None,32)->Dense(None,OUTPUT).`  
Accuracy was 5%. I thought that one hidden layer after flattening was not enough.  
The network might be underfitting and consequently not able to learn patterns and features.

#### Trial 1
I now added couple more hidden layers between flatten layer and output layer.  
_Structure :_ `Flatten(None, 1152)->Dense(None,512)->Dense(None,128)->Dense(None,32)->Dense(None,OUTPUT).`  
Now accuracy improved to 93%.

#### Trial 2
Now following the trend, I added another hidden layer.  
_Structure :_ `Flatten(None, 1152)->Dense(None,1024)->Dense(None,512)->Dense(None,128)->Dense(None,32)->Dense(None,OUTPUT).`  
Accuracy now dropped to 90%. The problem now might be overfitting of data. So I thought to apply dropout.

#### Trial 3
I applied dropout after the first two hidden layers.  
_Structure:_ `Flatten(None, 1152)->Dense(None,1024)->Dropout(0.5)->Dense(None,512)->Dropout(0.4)->Dense(None,128)->Dense(None,32)->Dense(None,OUTPUT).`  
Now the accuracy on test data was 95.5%.

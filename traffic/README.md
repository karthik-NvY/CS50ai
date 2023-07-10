## **Trial 0**
I applied Convolution and MaxPooling twice followed by flattening the inputs to 1152 nodes.  
Then I used a Dense layer with 32 nodes as an additional hidden layer before
connecting to outputs.  
_Structure :_ `(Conv, Maxpool)x2 -> Flatten(None,1152)->Dense(None,32)->Dense(None,OUTPUT).`  
Accuracy was 5%. I thought that one hidden layer after flattening was not enough.  
The network might be underfitting and consequently not able to learn patterns and features.

## **Trial 1**
I now added couple more hidden layers between flatten layer and output layer.  
_Structure :_ `Flatten(None, 1152)->Dense(None,512)->Dense(None,128)->Dense(None,32)->Dense(None,OUTPUT).`  
Now accuracy improved to 93%.

## **Trial 2**
Now following the trend, I added another hidden layer.  
_Structure :_ `Flatten(None, 1152)->Dense(None,1024)->Dense(None,512)->Dense(None,128)->Dense(None,32)->Dense(None,OUTPUT).`  
Accuracy now dropped to 90%. The problem now might be overfitting of data. So I thought to apply dropout.

## **Trial 3**
I applied dropout after the first two hidden layers.  
_Structure:_ `Flatten(None, 1152)->Dense(None,1024)->Dropout(0.5)->Dense(None,512)->Dropout(0.4)->Dense(None,128)->Dense(None,32)->Dense(None,OUTPUT).`  
Now the accuracy on test data was 95.5%.

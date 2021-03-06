## TODO: define the convolutional neural network architecture

import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
# can use the below import should you choose to initialize the weights of your Net
import torch.nn.init as I


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        
        ## TODO: Define all the layers of this CNN, the only requirements are:
        ## 1. This network takes in a square (same width and height), grayscale image as input
        ## 2. It ends with a linear layer that represents the keypoints
        ## it's suggested that you make this last layer output 136 values, 2 for each of the 68 keypoint (x, y) pairs
        
        # As an example, you've been given a convolutional layer, which you may (but don't have to) change:
        # 1 input image channel (grayscale), 32 output channels/feature maps, 5x5 square convolution kernel
        
        self.conv1 = nn.Conv2d(1, 32, 5) # 220 * 220
        
        self.conv1_bn = nn.BatchNorm2d(32)
        
        # max pool 2 * 2 --> 110 * 110
        
        self.conv2 = nn.Conv2d(32, 64, 3) # 108 * 108
        
        self.conv2_bn = nn.BatchNorm2d(64)
        
        self.pool = nn.MaxPool2d(2, 2)
       
        # max pool 2 * 2  --> 54 * 54
        
        self.conv3 = nn.Conv2d(64, 128, 3) # 52 * 52
        self.conv3_bn = nn.BatchNorm2d(128)
        
        # max pool 2 * 2  --> 26 * 26
        
        self.conv4 = nn.Conv2d(128, 256, 3) # 24 * 24
        self.conv4_bn = nn.BatchNorm2d(256)
        
        # max pool 2 * 2  --> 12 * 12
        
        self.conv5 = nn.Conv2d(256, 512, 1) # 12 * 12
        self.conv5_bn = nn.BatchNorm2d(512)
        
        # max pool 2 * 2  --> 6 * 6
        
        self.dropout = nn.Dropout(0.5)
        
        self.fc1 = nn.Linear(6 * 6 * 512, 1024)
        self.fc2 = nn.Linear(1024, 2048)
        self.fc3 = nn.Linear(2048, 136)
        
        ## Note that among the layers to add, consider including:
        # maxpooling layers, multiple conv layers, fully-connected layers, and other layers (such as dropout or batch normalization) to avoid overfitting
        
    def forward(self, x):
        ## TODO: Define the feedforward behavior of this model
        ## x is the input image and, as an example, here you may choose to include a pool/conv step:
        ## x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv1_bn(self.conv1(x)))) #
        # x = self.dropout(x)
        x = self.pool(F.relu(self.conv2_bn(self.conv2(x)))) # 
        # x = self.dropout(x)
        x = self.pool(F.relu(self.conv3_bn(self.conv3(x)))) # 
        # x = self.dropout(x)
        x = self.pool(F.relu(self.conv4_bn(self.conv4(x)))) # 
        # x = self.dropout(x)
        x = self.pool(F.relu(self.conv5_bn(self.conv5(x)))) # 
        # x = self.dropout(x)
        
        x = F.relu(self.fc1(x.view(x.size(0), -1)))
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.dropout(x)
        
        x = self.fc3(x)
        
        
        # a modified x, having gone through all the layers of your model, should be returned
        return x

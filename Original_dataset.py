#!/usr/bin/env python
# coding: utf-8

# In[4]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:



"""
Created on Tue Jun 16 17:54:31 2020

@author: cds
"""

import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import os
from skimage import io
from skimage.transform import resize
import numpy as np
import torchvision.transforms as transforms
from skimage.color import rgb2gray


class MammoTrain(Dataset):
    def __init__(self, csv_file, root_dir, transform =  transforms.Compose([transforms.Resize(224), 
                 transforms.ToTensor(),
                 transforms.Normalize(mean=[0.5], std=[0.5])]) ,
                    Flag=True):
        self.names = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform
        self.Flag = Flag
    def __len__(self):
        return len(self.names)
    def __getitem__(self, idx):   
        if self.Flag:
            img_name = os.path.join(self.root_dir,
                                    self.names['Filename'][idx])
        else:
             img_name = self.names['Filename'][idx]   
        image = Image.open(img_name)
        if len(image.shape)==3:
            image = rgb2gray(image)
        if self.names['classification'][idx]=="Benign":
            label=0
        else:
            label=1
        if self.transform:
            image = self.transform(image)
            image = image.float()
            label = torch.tensor(label)
        return image,label      

    
class MammoTest(Dataset):
    def __init__(self, csv_file, root_dir, transform =  transforms.Compose([transforms.Resize(224), 
                 transforms.ToTensor(),
                 transforms.Normalize(mean=[0.5], std=[0.5])]) ,
                    Flag=True):
        self.names = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform
        self.Flag = Flag
    def __len__(self):
        return len(self.names)
    def __getitem__(self, idx):   
        if self.Flag:
            img_name = os.path.join(self.root_dir,
                                    self.names['Filename'][idx])
        else:
             img_name = self.names['Filename'][idx]   
        image = Image.open(img_name)
        if len(image.shape)==3:
            image = rgb2gray(image)
        if self.names['classification'][idx]=="Benign":
            label=0
        else:
            label=1
        if self.transform:
            image = self.transform(image)
            image = image.float()
            label = torch.tensor(label)
        return image,label   


#




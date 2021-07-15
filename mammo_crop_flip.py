#This will flip right sided images and crop before resizing to 224 by 224

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
    def __init__(self, csv_file, root_dir, transform =  transforms.Compose([ 
                 transforms.ToTensor()]) , Flag=True):
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
        image = io.imread(img_name)
        if len(image.shape)==3:
            image = rgb2gray(image)
        if self.names['LeftRight'][idx]=="R":
            image= image[:,::-1]
        image= image[250:2000,0:1000]
        image = resize(image, (224, 224))

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
    def __init__(self, csv_file, root_dir, transform =  transforms.Compose([ 
                 transforms.ToTensor()]) , Flag=True):
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
        image = io.imread(img_name)
        if len(image.shape)==3:
            image = rgb2gray(image)
        if self.names['LeftRight'][idx]=="R":
            image = image[:,::-1]
        image= image[250:2000,0:1000]
        image = resize(image, (224, 224))
        if self.names['classification'][idx]=="Benign":
            label=0
        else:
            label=1
        if self.transform:
            image = self.transform(image)
            image = image.float()
            label = torch.tensor(label)
        return image,label  




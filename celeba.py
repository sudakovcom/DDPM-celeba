import os
import zipfile 
import torch
from natsort import natsorted
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms
import re
import numpy as np
import torch

CUR_DIR = os.path.dirname(os.path.abspath(__file__))


## Create a custom Dataset class
class CelebADataset(Dataset):
    def __init__(self, root_dir=os.path.join(CUR_DIR, 'datasets/celeba'), transform=None):
        """
        Args:
          root_dir (string): Directory with all the images
          transform (callable, optional): transform to be applied to each image sample
        """
        # Read names of images in the root directory
        
        # Path to folder with the dataset
        if not os.path.isdir(root_dir):
            os.makedirs(root_dir)
        dataset_folder = f'{root_dir}/img_align_celeba/'
        self.dataset_folder = os.path.abspath(dataset_folder)
        image_names = os.listdir(self.dataset_folder)

        self.transform = transform 
        image_names = natsorted(image_names)
        
        self.filenames = []
        with open(f'{root_dir}/list_attr_celeba.txt') as f:
            for i, line in enumerate(f.readlines()):
                line = re.sub(' *\n', '', line)
                if i >= 2:
                    values = re.split(' +', line)
                    filename = values[0]
                    self.filenames.append(filename)
              
    def __len__(self): 
        return len(self.filenames)

    def __getitem__(self, idx):
        # Get the path to the image 
        img_name = self.filenames[idx]
        img_path = os.path.join(self.dataset_folder, img_name)
        # Load image and convert it to RGB
        img = Image.open(img_path).convert('RGB')
        # Apply transformations to the image
        if self.transform:
            img = self.transform(img)
        return img
    
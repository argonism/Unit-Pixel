# ----------------------------------------------------------------------------
#
#            this code is from eriklindernoren/PyTorch-GAN
#            https://github.com/eriklindernoren/PyTorch-GAN.git
#
#            edited for this application partially
# 
#            Copyright (c) 2018 eriklindernoren
#            Released under the MIT license
#
# ----------------------------------------------------------------------------

import argparse
import os
import numpy as np
import math
import itertools
import datetime
import time
import sys
import uuid

import torchvision.transforms as transforms
from torchvision.utils import save_image

from torch.utils.data import DataLoader
from torchvision import datasets
from torch.autograd import Variable

from models import *

import torch.nn as nn
import torch.nn.functional as F
import torch

from PIL import Image

SAVE_IMG_DIR = "static/tmp"

class Face2Pixel:
    def __init__(self, model_ver=200,ataset_name="illust2pixel", channels=3, img_height=256, img_width=256, dim=64, n_downsample=2):
        cuda = True if torch.cuda.is_available() else False

        input_shape = (channels, img_height, img_width)

        shared_dim = dim * 2 ** n_downsample

        shared_E = ResidualBlock(features=shared_dim)
        self.E1 = Encoder(dim=dim, n_downsample=n_downsample, shared_block=shared_E)
        self.E2 = Encoder(dim=dim, n_downsample=n_downsample, shared_block=shared_E)
        shared_G = ResidualBlock(features=shared_dim)
        self.G1 = Generator(dim=dim, n_upsample=n_downsample, shared_block=shared_G)
        self.G2 = Generator(dim=dim, n_upsample=n_downsample, shared_block=shared_G)
        self.D1 = Discriminator(input_shape)
        self.D2 = Discriminator(input_shape)

        if cuda:
            self.E1 = self.E1.cuda()
            self.E2 = self.E2.cuda()
            self.G1 = self.G1.cuda()
            self.G2 = self.G2.cuda()
            self.D1 = self.D1.cuda()
            self.D2 = self.D2.cuda()

        self.E1.load_state_dict(torch.load("models/E1_%d.pth" % model_ver, map_location=torch.device('cpu')))
        self.E2.load_state_dict(torch.load("models/E2_%d.pth" % model_ver, map_location=torch.device('cpu')))
        self.G1.load_state_dict(torch.load("models/G1_%d.pth" % model_ver, map_location=torch.device('cpu')))
        self.G2.load_state_dict(torch.load("models/G2_%d.pth" % model_ver, map_location=torch.device('cpu')))
        self.D1.load_state_dict(torch.load("models/D1_%d.pth" % model_ver, map_location=torch.device('cpu')))
        self.D2.load_state_dict(torch.load("models/D2_%d.pth" % model_ver, map_location=torch.device('cpu')))

        self.Tensor = torch.cuda.FloatTensor if cuda else torch.Tensor

        # Image transformations
        transforms_ = [
            transforms.Resize(int(img_height * 1.12), Image.BICUBIC),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ]
        self.transform = transforms.Compose(transforms_)

    def convert_image(self, image):
        print(np.asarray(image).shape)
        img = self.transform(image)
        X1 = Variable(img.type(self.Tensor))
        _, Z1 = self.E1(X1.unsqueeze(0))
        fake_X2 = self.G2(Z1)
        unique_filename = str(uuid.uuid4())
        output_path = f"{SAVE_IMG_DIR}/{unique_filename}.png"
        save_image(fake_X2, output_path, normalize=True)
        return unique_filename

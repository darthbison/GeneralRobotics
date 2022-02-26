#!/usr/bin/env python

import torchvision
import torch

# ## TensorRT

# > If your setup does not have `torch2trt` installed, you need to first install `torch2trt` by executing the following in the console.
# ```bash
# cd $HOME
# git clone https://github.com/NVIDIA-AI-IOT/torch2trt
# cd torch2trt
# sudo python3 setup.py install
# ```
# 
# Convert and optimize the model using torch2trt for faster inference with TensorRT. Please see the [torch2trt](https://github.com/NVIDIA-AI-IOT/torch2trt) readme for more details.
# 
# > This optimization process can take a couple minutes to complete.

from torch2trt import torch2trt

model = torchvision.models.resnet18(pretrained=False)
model.fc = torch.nn.Linear(512, 2)
model = model.cuda().eval().half()


model.load_state_dict(torch.load('best_steering_model_xy.pth'))


device = torch.device('cuda')


data = torch.zeros((1, 3, 224, 224)).cuda().half()

model_trt = torch2trt(model, [data], fp16_mode=True)


torch.save(model_trt.state_dict(), 'best_steering_model_xy_trt.pth')






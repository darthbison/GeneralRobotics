#!/usr/bin/env python
# coding: utf-8

# # Collision Avoidance - Live Demo (Resnet18)
# 
# In this notebook we'll use the model we trained to detect whether the robot is ``free`` or ``blocked`` to enable a collision avoidance behavior on the robot.  
# 
# ## Load the trained model
# 
# We'll assumed that you've already downloaded the ``best_model.pth`` to your workstation as instructed in the training notebook.  Now, you should upload this model into this notebook's
# directory by using the Jupyter Lab upload tool.  Once that's finished there should be a file named ``best_model.pth`` in this notebook's directory.  
# 
# > Please make sure the file has uploaded fully before calling the next cell
# 
# Execute the code below to initialize the PyTorch model.  This should look very familiar from the training notebook.


import torch
import torchvision

model = torchvision.models.resnet18(pretrained=False)
model.fc = torch.nn.Linear(512, 2)



model.load_state_dict(torch.load('best_model_resnet18.pth'))



device = torch.device('cuda')
model = model.to(device)
model = model.eval().half()


# ### Create the preprocessing function
# 
# We have now loaded our model, but there's a slight issue.  The format that we trained our model doesn't *exactly* match the format of the camera.  To do that, 
# we need to do some *preprocessing*.  This involves the following steps
# 
# 1. Convert from HWC layout to CHW layout
# 2. Normalize using same parameters as we did during training (our camera provides values in [0, 255] range and training loaded images in [0, 1] range so we need to scale by 255.0
# 3. Transfer the data from CPU memory to GPU memory
# 4. Add a batch dimension


import torchvision.transforms as transforms
import torch.nn.functional as F
import cv2
import PIL.Image
import numpy as np

mean = torch.Tensor([0.485, 0.456, 0.406]).cuda().half()
std = torch.Tensor([0.229, 0.224, 0.225]).cuda().half()

normalize = torchvision.transforms.Normalize(mean, std)

def preprocess(image):
    image = PIL.Image.fromarray(image)
    image = transforms.functional.to_tensor(image).to(device).half()
    image.sub_(mean[:, None, None]).div_(std[:, None, None])
    return image[None, ...]


# Great! We've now defined our pre-processing function which can convert images from the camera format to the neural network input format.
# 
# Now, let's start and display our camera.  You should be pretty familiar with this by now.  We'll also create a slider that will display the
# probability that the robot is blocked.  We'll also display a slider that allows us to control the robot's base speed.


import traitlets
from IPython.display import display
import ipywidgets.widgets as widgets
from jetbot import Camera, bgr8_to_jpeg

camera = Camera.instance(width=224, height=224)
image = widgets.Image(format='jpeg', width=224, height=224)
blocked_slider = widgets.FloatSlider(description='blocked', min=0.0, max=1.0, orientation='vertical')
speed_slider = widgets.FloatSlider(description='speed', min=0.0, max=0.5, value=0.0, step=0.01, orientation='horizontal')

camera_link = traitlets.dlink((camera, 'value'), (image, 'value'), transform=bgr8_to_jpeg)

display(widgets.VBox([widgets.HBox([image, blocked_slider]), speed_slider]))


# We'll also create our robot instance which we'll need to drive the motors.



from jetbot import Robot

robot = Robot()


# Next, we'll create a function that will get called whenever the camera's value changes.  This function will do the following steps
# 
# 1. Pre-process the camera image
# 2. Execute the neural network
# 3. While the neural network output indicates we're blocked, we'll turn left, otherwise we go forward.

# In[ ]:


import torch.nn.functional as F
import time

def update(change):
    global blocked_slider, robot
    x = change['new'] 
    x = preprocess(x)
    y = model(x)
    
    # we apply the `softmax` function to normalize the output vector so it sums to 1 (which makes it a probability distribution)
    y = F.softmax(y, dim=1)
    
    prob_blocked = float(y.flatten()[0])
    
    blocked_slider.value = prob_blocked
    
    if prob_blocked < 0.5:
        robot.forward(speed_slider.value)
    else:
        robot.left(speed_slider.value)
    
    time.sleep(0.001)
        
update({'new': camera.value})  # we call the function once to initialize


# Cool! We've created our neural network execution function, but now we need to attach it to the camera for processing. 
# 
# We accomplish that with the ``observe`` function.
# 
# > WARNING: This code may move the robot!! Adjust the speed slider we defined earlier to control the base robot speed.  Some kits can move fast, so start slow, and gradually increase the value.

# In[ ]:


camera.observe(update, names='value')  # this attaches the 'update' function to the 'value' traitlet of our camera


# Awesome! If your robot is plugged in it should now be generating new commands with each new camera frame.  Perhaps start by placing your robot on the ground and seeing what it does when it reaches an obstacle.
# 
# If you want to stop this behavior, you can unattach this callback by executing the code below.


camera.unobserve(update, names='value')

time.sleep(0.1)  # add a small sleep to make sure frames have finished processing

robot.stop()



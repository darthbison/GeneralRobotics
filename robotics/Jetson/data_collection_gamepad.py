#!/usr/bin/env python

from IPython.display import HTML
HTML('<iframe width="560" height="315" src="https://www.youtube.com/embed/FW4En6LejhI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>')

# IPython Libraries for display and widgets
import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display

# Camera and Motor Interface for JetBot
from jetbot import Robot, Camera, bgr8_to_jpeg

# Basic Python packages for image annotation
from uuid import uuid1
import os
import json
import glob
import datetime
import numpy as np
import cv2
import time

camera = Camera()

widget_width = camera.width
widget_height = camera.height

image_widget = widgets.Image(format='jpeg', width=widget_width, height=widget_height)
target_widget = widgets.Image(format='jpeg', width=widget_width, height=widget_height)

x_slider = widgets.FloatSlider(min=-1.0, max=1.0, step=0.001, description='x')
y_slider = widgets.FloatSlider(min=-1.0, max=1.0, step=0.001, description='y')

def display_xy(camera_image):
    image = np.copy(camera_image)
    x = x_slider.value
    y = y_slider.value
    x = int(x * widget_width / 2 + widget_width / 2)
    y = int(y * widget_height / 2 + widget_height / 2)
    image = cv2.circle(image, (x, y), 8, (0, 255, 0), 3)
    image = cv2.circle(image, (widget_width / 2, widget_height), 8, (0, 0,255), 3)
    image = cv2.line(image, (x,y), (widget_width / 2, widget_height), (255,0,0), 3)
    jpeg_image = bgr8_to_jpeg(image)
    return jpeg_image

time.sleep(1)
traitlets.dlink((camera, 'value'), (image_widget, 'value'), transform=bgr8_to_jpeg)
traitlets.dlink((camera, 'value'), (target_widget, 'value'), transform=display_xy)

display(widgets.HBox([image_widget, target_widget]), x_slider, y_slider)


controller = widgets.Controller(index=0)

display(controller)


widgets.jsdlink((controller.axes[2], 'value'), (x_slider, 'value'))
widgets.jsdlink((controller.axes[3], 'value'), (y_slider, 'value'))


DATASET_DIR = 'dataset_xy'

# we have this "try/except" statement because these next functions can throw an error if the directories exist already
try:
    os.makedirs(DATASET_DIR)
except FileExistsError:
    print('Directories not created because they already exist')

for b in controller.buttons:
    b.unobserve_all()

count_widget = widgets.IntText(description='count', value=len(glob.glob(os.path.join(DATASET_DIR, '*.jpg'))))

def xy_uuid(x, y):
    return 'xy_%03d_%03d_%s' % (x * widget_width / 2 + widget_width / 2, y * widget_height / 2 + widget_height / 2, uuid1())

def save_snapshot(change):
    if change['new']:
        uuid = xy_uuid(x_slider.value, y_slider.value)
        image_path = os.path.join(DATASET_DIR, uuid + '.jpg')
        with open(image_path, 'wb') as f:
            f.write(image_widget.value)
        count_widget.value = len(glob.glob(os.path.join(DATASET_DIR, '*.jpg')))

controller.buttons[13].observe(save_snapshot, names='value')

display(widgets.VBox([
    target_widget,
    count_widget
]))


camera.stop()

def timestr():
    return str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

get_ipython().system('zip -r -q road_following_{DATASET_DIR}_{timestr()}.zip {DATASET_DIR}')



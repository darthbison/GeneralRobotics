from jetbot import Robot
import time
import ipywidgets.widgets as widgets
from IPython.display import display
import traitlets




robot = Robot()

# create two sliders with range [-1.0, 1.0]
left_slider = widgets.FloatSlider(description='left', min=-1.0, max=1.0, step=0.01, orientation='vertical')
right_slider = widgets.FloatSlider(description='right', min=-1.0, max=1.0, step=0.01, orientation='vertical')

# create a horizontal box container to place the sliders next to each other
slider_container = widgets.HBox([left_slider, right_slider])

# display the container in this cell's output
display(slider_container)

left_link = traitlets.link((left_slider, 'value'), (robot.left_motor, 'value'))
right_link = traitlets.link((right_slider, 'value'), (robot.right_motor, 'value'))

left_link.unlink()
right_link.unlink()
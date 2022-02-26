#!/usr/bin/env python
# coding: utf-8

# # Teleoperation
# 
# In this example we'll control the Jetbot remotely with a gamepad controller connected to our web browser machine.

# ### Create gamepad controller
# 
# The first thing we want to do is create an instance of the ``Controller`` widget, which we'll use to drive our robot.
# The ``Controller`` widget takes a ``index`` parameter, which specifies the number of the controller.  This is useful in case you
# have multiple controllers attached, or some gamepads *appear* as multiple controllers.  To determine the index
# of the controller you're using,
# 
# 1. Visit [http://html5gamepad.com](http://html5gamepad.com).  
# 2. Press buttons on the gamepad you're using
# 3. Remember the ``index`` of the gamepad that is responding to the button presses
# 
# Next, we'll create and display our controller using that index.



import ipywidgets.widgets as widgets

controller = widgets.Controller(index=1)  # replace with index of your controller

display(controller)


# Even if the index is correct, you may see the text ``Connect gamepad and press any button``.  That's because the gamepad hasn't
# registered with this notebook yet.  Press a button and you should see the gamepad widget appear above.

# ### Connect gamepad controller to robot motors
# 
# Now, even though we've connected our gamepad, we haven't yet attached the controls to our robot!  The first, and most simple control
# we want to attach is the motor control.  We'll connect that to the left and right vertical axes using the ``dlink`` function.  The
# ``dlink`` function, unlike the ``link`` function, allows us to attach a transform between the ``source`` and ``target``.  Because
# the controller axes are flipped from what we think is intuitive for the motor control, we'll use a small *lambda* function to
# negate the value.
# 
# > WARNING: This next cell will move the robot if you touch the gamepad controller axes!



from jetbot import Robot
import traitlets

robot = Robot()

left_link = traitlets.dlink((controller.axes[1], 'value'), (robot.left_motor, 'value'), transform=lambda x: -x)
right_link = traitlets.dlink((controller.axes[3], 'value'), (robot.right_motor, 'value'), transform=lambda x: -x)


# Awesome! Our robot should now respond to our gamepad controller movements.  Now we want to view the live video feed from the camera!

# ### Create and display Image widget
# 
# First, let's display an ``Image`` widget that we'll use to show our live camera feed.  We'll set the ``height`` and ``width``
# to just 300 pixels so it doesn't take up too much space.
# 
# > FYI: The height and width only effect the rendering on the browser side, not the native image resolution before network transport from robot to browser.



image = widgets.Image(format='jpeg', width=300, height=300)

display(image)


# ### Create camera instance
# 
# Well, right now there's no image presented, because we haven't set the value yet!  We can do this by creating our ``Camera``
# class and attaching the ``value`` attribute of the camera to the ``value attribute of the image.
# 
# First, let's create the camera instance, we call the ``instance`` method which will create a new camera
# if it hasn't been created yet.  If once already exists, this method will return the existing camera.



from jetbot import Camera

camera = Camera.instance()


# ### Connect Camera to Image widget

# Our camera class currently only produces values in BGR8 (blue, green, red, 8bit) format, while our image widget accepts values in compressed *JPEG*.
# To connect the camera to the image we need to insert the ``bgr8_to_jpeg`` function as a transform in the link.  We do this below


from jetbot import bgr8_to_jpeg

camera_link = traitlets.dlink((camera, 'value'), (image, 'value'), transform=bgr8_to_jpeg)


# You should now see the live video feed shown above!
# 
# > REMINDER:  You can right click the output of a cell and select ``Create New View for Output`` to display the cell in a separate window.

# ### Stop robot if network disconnects
# 
# You can drive your robot around by looking through the video feed. But what if your robot disconnects from Wifi?  Well, the motors would keep moving and it would keep trying to stream video and motor commands.  Let's make it so that we stop the robot and unlink the camera and motors when a disconnect occurs.



from jetbot import Heartbeat


def handle_heartbeat_status(change):
    if change['new'] == Heartbeat.Status.dead:
        camera_link.unlink()
        left_link.unlink()
        right_link.unlink()
        robot.stop()

heartbeat = Heartbeat(period=0.5)

# attach the callback function to heartbeat status
heartbeat.observe(handle_heartbeat_status, names='status')


# If the robot disconnects from the internet you'll notice that it stops.  You can then re-connect the camera and motors by re-creating the links with the cell below



# only call this if your robot links were unlinked, otherwise we'll have redundant links which will double
# the commands transferred

left_link = traitlets.dlink((controller.axes[1], 'value'), (robot.left_motor, 'value'), transform=lambda x: -x)
right_link = traitlets.dlink((controller.axes[3], 'value'), (robot.right_motor, 'value'), transform=lambda x: -x)
camera_link = traitlets.dlink((camera, 'value'), (image, 'value'), transform=bgr8_to_jpeg)


# ### Save snapshots with gamepad button
# 
# Now, we'd like to be able to save some images from our robot.  Let's make it so the right bumper (index 5) saves a snapshot of the current live image.  We'll save the images in the ``snapshots/`` directory, with a name that is guaranteed to be unique using the ``uuid`` python package.  We use the ``uuid1`` identifier, because this also encodes the date and MAC address which we might want to use later.



import uuid
import subprocess

subprocess.call(['mkdir', '-p', 'snapshots'])

snapshot_image = widgets.Image(format='jpeg', width=300, height=300)

def save_snapshot(change):
    # save snapshot when button is pressed down
    if change['new']:
        file_path = 'snapshots/' + str(uuid.uuid1()) + '.jpg'
        
        # write snapshot to file (we use image value instead of camera because it's already in JPEG format)
        with open(file_path, 'wb') as f:
            f.write(image.value)
            
        # display snapshot that was saved
        snapshot_image.value = image.value


controller.buttons[5].observe(save_snapshot, names='value')

display(widgets.HBox([image, snapshot_image]))
display(controller)


# Before closeing this notebook and shutdown the Python kernel for the notebook, we want to properly close the camera connection so that we can use the camera in other notebook.




camera.stop()


# ### Conclusion
# 
# That's it for this example, have fun!

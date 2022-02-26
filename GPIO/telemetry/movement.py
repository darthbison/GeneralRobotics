
def getPitch(sense):
   o = sense.get_orientation()
   pitch = o["pitch"]
   pitch = round(pitch, 1)
   return pitch

def getRoll(sense):
   o = sense.get_orientation()
   roll = o["roll"]
   roll = round(roll, 1)
   return roll

def getYaw(sense):
    o = sense.get_orientation()
    yaw = o["yaw"]
    yaw = round(yaw, 1)
    return yaw


def getOrientation(sense):
     o = sense.get_orientation()
     return o




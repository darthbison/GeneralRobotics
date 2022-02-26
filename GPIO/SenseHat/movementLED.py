from sense_hat import SenseHat
sense = SenseHat()
sense.clear()

edge = [0, 1, 2, 3, 4, 5, 6, 7, 15, 23, 31, 39, 47, 55, 63, 62, 61, 60, 59, 58, 57, 56, 48, 40, 32, 24, 16, 8]
length = len(edge)
ratio = length / 360.0

while True:
    o = sense.get_orientation()
    pitch = o["pitch"]
    roll = o["roll"]
    yaw = o["yaw"]
    yaw_list_position = int(yaw * ratio)
    yaw_pixel_number = edge[yaw_list_position]
    y = yaw_pixel_number // 8
    x = yaw_pixel_number % 8
    sense.set_pixel(x, y, 255, 255, 255)

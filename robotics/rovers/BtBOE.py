import bluetooth

target_name = "RN42-E6C0"
target_address = '00:06:66:83:E6:C0' 

port = 1
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((target_address, port))
while 1:
    text = input() 
    if text == "quit":
        break
    s.send(text)
s.close()

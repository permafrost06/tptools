from time import sleep
from tptools import Instance

x = Instance("192.168.0.1", "admin", "admin")

while True:
    if x.GetChannel() != "7":
        x.SetChannel(7)
    sleep(60)
from tptools import Instance
import sys

x = Instance()

if sys.argv[1] == "off":
	x.qosoff()
else:
	x.qoson()
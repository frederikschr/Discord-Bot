from phue import Bridge
import os
from dotenv import load_dotenv

load_dotenv()

bridge_ip = os.environ["BRIDGE_IP"]

b = Bridge(bridge_ip)

color = 10000
sat = 100

fredi_light_list = [14, 4]

def access_lights():
    b = Bridge(bridge_ip)
    light_name_list = b.get_light_objects("name")
    return light_name_list

def all_lights():
    lights = access_lights()
    for light in lights:
        lights[light].on = True
        if lights[light].type == "Color Light":
            lights[light].hue = 30000
            lights[light].saturation = 100

def turn_lights_off():
    lights = access_lights()
    for light in lights: 
        lights[light].on = False

def get_lights():
    b = Bridge(bridge_ip)
    lights = b.lights
    for l in lights:
        print(l.name)

def fredi_lights_on():
    b = Bridge(bridge_ip)
    for fredi_light in fredi_light_list:
        b.set_light(fredi_light, "on", True)

def fredi_lights_off():
    b = Bridge(bridge_ip)
    for fredi_light in fredi_light_list:
        b.set_light(fredi_light, "on", False)


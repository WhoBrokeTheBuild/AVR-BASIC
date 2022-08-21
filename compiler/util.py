
import math

def rad2brad(rad):
    return round((math.degrees(rad) / 360) * 255)

def brad2rad(brad):
    return math.radians((brad / 255) * 360)

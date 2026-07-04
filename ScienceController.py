#! /usr/bin/python3

import rospy
from can_msgs.msg import Frame
import States
import science_teleop #ten plik z joystickem chb tez

class ScienceController:

# TU BEDZIE KONTROLA MISJI
# normalnie piszesz kod do joysticka
# apotem go automatyzujesz jakos
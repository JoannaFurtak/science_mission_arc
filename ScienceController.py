#! /usr/bin/python3

import rospy
from can_msgs.msg import Frame
from sensor_msgs.msg import JointState
import States
import curses
#science_teleop
#

class ScienceController:

    def __init__(self, stdscr) -> None:
        rospy.init_node("science_controller")
        self.state_subscriber = rospy.Subscriber("/science/state", JointState, 
                                                 self._joint_state_callback)
        self.state_publisher = rospy.Publisher("/science/command",
                                               JointState,
                                               queue_size=10)

        self.can_publisher = rospy.Publisher('/sent_canbus_messages',
                                             Frame,
                                             queue_size=10)
        
        #jeszcze subscribery i topici dla odczytow z czujnikow

#SPRAWDZ TOPIICICIICIICICIICICI

        #historia stanow
        self.state = {}
        self.rate = rospy.Rate(10) #10 razy na sekunde, stosowane do petli, wiadomosci 

        #polaczenie z ekranem
        self.stdscr = stdscr
        #czekanie na wcisniety klawisz przez 300ms
        #potem zeby nie blokowac, bo funkcja getch 
        stdscr.timeout(300)

        #flagi dla klawiszy
        self.key_pressed = False #do czego mi jest self.key_pressed?
        self.deep_key_pressed = False
        #dodanie klawiszy dla trybow
        self.manual_key_pressed = False
        self.autonomy_key_pressed = False

        #pojemniki dla manuala i autonomii
        self.container1 = 1 #manual
        self.container2 = 2 #autonomy

        #stany poczatkowe 
        self.active_container_open = False
        self.active_container_pushed_in = False

        self.drill_current = 0
        self.drill_lift_position = 0
        self.drill_lift_current = 0
        self.module_position = 0
        self.module_current = 0

    def joint_state_callback(self, msg):

        for i, joint in enumerate(msg.name):
            if joint == 'module_lift':
                self.module_position = msg.position[i]
                self.module_effrort = msg.effort[i]
            if joint == 'drill_lift':
                self.drill_lift_position = msg.position[i]
                self.drill_lift_current = msg.effort[i]
            if joint == 'drill_spin':
                self.drill_current = msg.effort[i]

    def set_state(self, new_state):
        self.state = new_state
        self.state._context = self
        self.state.setup()

    def run(self):
        pass

    def command_servos(self, msg_id):
        if msg_id == 0:
            cmd = 0x00d0
            if self.surface_container_pushed_in:
                cmd = 0x01a0

        elif msg_id == 2:
            cmd = 0x0200
            if self.deep_container_pushed_in:
                cmd = 0x00d0

        elif msg_id == 1:
            cmd = 0x0300
            if self.shovel_in:
                cmd = 0x00d0

            if self.shovel_emptying:
                cmd = 0x0150

        msg = Frame()
        msg.dlc = 2
        msg.id = (0x30 << 5) | msg_id
        msg.data = [cmd >> 8, cmd & 0b11111111, 0, 0, 0, 0, 0, 0]
        self.can_publisher.publish(msg)

        

    def move_joint(self, joint, effort):
        msg = JointState()
        msg.header.stamp = rospy.Time.now()
        msg.name = [joint]
        msg.effort = [effort]
        self.state_publisher.publish(msg)


    #funkcja na odczyty z czujnikow
    #zapisujaca odczyty do pliku json
    #autonomy

    






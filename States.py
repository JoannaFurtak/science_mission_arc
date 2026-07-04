#! /usr/bin/python3

from State_Interface import State
import rospy


class StateIdle(State):

    def setup(self):
        rospy.loginfo("Idle")

    def step(self):
        if self.context.start_deep_drilling == True:
            rospy.loginfo("lowering module")
            self.context.set_state(LoweringModule())
            return

        self.context.move_joint("module_lift", 0)
        self.context.move_joint("drill_lift", 0)
        self.context.move_joint("drill_spin", 0)
        self.context.deep_container_pushed_in = False

    def __repr__(self):
        return "Idle"
    

class LoweringModule(State):
    
    def setup(self):
        rospy.loginfo("started lowering")
        self.start_time = rospy.Time.now() 

    def step(self):
        current_limit = -0.2
        module_limit = -200 #ZOBACZ LIMITY CZY SA OKEJ!!!!!!

        time = rospy.Time.now() 

        if ((time - self.start_time).to_sec > 2 and 
            (current_limit > self.context.module_current or module_limit > self.context.module_position)):
            rospy.loginfo("starting drilling")
            self.context.set_state(StartDeepDrilling())
            return
        
        self.context.move_joint("module_lift", -0.4)

    
    def __repr__(self):
        return "LoweringModule"


class StartDeepDrilling(State):

    def setup(self):
        rospy.loginfo("started drilling")
        self.start_time = rospy.Time.now()

    def step(self):
        time = rospy.Time.now()
        current_limit = 5
        drill_limit = -1000 #NO WLASNIE, SKAD MASZ WIEDZIEC
        #jak gleboko? ta zmienna definitywnie popraw

        if ((time - self.start_time).to_sec() > 2 and
            ((current_limit < self.context.drill_current) or
            (drill_limit > self.context.drill_lift_position))):
            self.context.set_state(DeepDrillRetraction()) 
            return
        
        self.context.move_joint("module_lift", 0.0)
        self.context.move_joint("drill_lift", -0.4)
        self.context.move_joint("drill_spin", 1.0)
    

    def __repr__(self):
        return "Deep Drilling"

class DeepDrillRetraction(State):
    def setup(self):
        rospy.loginfo("drill retraction")
        self.context.move_joint("drill_spin", 0.0)
        self.context.move_joint("drill_lift", 0.0)
        self.start_time = rospy.Time.now()


    def step(self):
        
        current_limit = -5
        drill_limit = 10
        time = rospy.Time.now()

        if ((time - self.start_time).to_sec() > 2 and 
            ((current_limit > self.context.drill_current) or
            (drill_limit < self.context.drill_lift_position))):
            self.context.set_state(LiftingModule())
            return
        
        self.context.move_joint("drill_lift", 0.4)

    def __repr__(self):
        return "DeepDrillRetraction"

"""class LiftingModule(State):

class PushingContainer(State):

class EmptyingDrill(State):

class ShakingContainer(State):

class PushingContainerAway(State):"""
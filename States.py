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
        drill_limit = 10.000000 #sprawdz te limity!!!!!
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
    

class LiftingModule(State):
    def setup(self):
        rospy.loginfo("lifting module")
        self.start_time = rospy.Time.now()
        self.context.move_joint("drill_lift", 0.0)

    def step(self):
        current_limit = 5 #CHECK LIMITS
        module_limit = 0 #CHECK ALL OF THOSE LIMITSS

        time = rospy.Time.now()

        if ((time - self.start_time).to_sec() > 2 and 
            (current_limit < self.context.module_current or 
             module_limit < self.context.module_position)):
            self.context.set_state(PushingContainer())
            return

        self.context.move_joint("module_lift", 0.4)

    
    def __repr__(self):
        return "LiftingModule"


class PushingContainer(State):

    def setup(self):
        rospy.loginfo("pushing container in")
        self.start_time = rospy.Time.now()
        self.context.move_joint("module_lift", 0.0) #zatrzymujemy go

    def step(self):
        time = rospy.Time.now()
        if (time - self.start_time).to_sec() > 2:
            self.context.set_state(EmptyingDrill())
            return
        self.context.deep_container_open = True 
        self.context.deep_container_pushed_in = True 

    def __repr__(self):
        return "PushingContainer"


class EmptyingDrill(State):
    def setup(self):
        rospy.loginfo("emptying drill")
        self.start_time = rospy.Time.now()

    def step(self):
        time = rospy.Time.now()
        if (time - self.start_time).to_sec() > 4:
            self.context.set_state(PushingContainerAway())
            #self.context.set_state(ShakingContainer())
            return
        self.context.move_joint("drill_spin", -1.0)

    def __repr__(self):
        return "EmtyingDrill"


class PushingContainerAway(State):

    def setup(self):
        rospy.loginfo("Pushing Container Away")
        self.start_time = rospy.Time.now()
        self.context.move_joint("drill_spin", 0.0)

    def step(self):
        time = rospy.Time.now()
        if (time - self.start_time).to_sec() > 2:
            self.context.set_state(StateIdle())
            return
        
        self.context.active_container_open = False
        self.context.active_container_pushed_in = False

    def __repr__(self):
        return "PushingContainerAway"


"""class ShakingContainer(State):

    def setup(self):
        rospy.loginfo("Shaking container)
        self.start_time = rospy.Time.now()

    def step(self):
        time = rospy.Time.now()
        if (time - self.start_time).to_sec() > 20:
            self.context.set_state(PushingContainerAway())
            return
        self.context.active_container_pushed_in = True
        rospy.sleep(0.1)
        self.context.active_container_pushed_in = False
        rospy.sleep(0.1)

    def __repr__(self):
        return "ShakingContainer" """

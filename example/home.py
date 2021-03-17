import datetime;

from component.alarm import Alarm;
from flow.entities import TimeRecurring, Sensor, Light, Cover;


task.sleep(10);

# Global
sun = Sensor("sun.sun");

fiveMinutes = TimeRecurring(5);


###################
##### HELPERS #####
###################

class Window:
  def __init__(self):
    self.Cover = None;
    self.Contact = None;
    return self;

class Room:
  
  def __init__(self, room):
    self.Scene = Sensor('input_select.' + room + '_scene')
    self.Motion = Sensor('binary_sensor.' + room + '_motion');
    self.Light = Light('light.yeelight_' + room + '_ceiling');
    self.NightLight = Light('light.yeelight_' + room + '_ceiling_nightlight');

    self.Window = Window();
    self.Window.Cover = Cover('cover.' + room + '_window_blind');

    self.Door = Window()
    self.Door.Cover = Cover('cover.' + room + '_door_blind');

  def AutomateLight(self, timeout):
    self.Scene.Is("Normal").And(self.Motion.Is("on")).Then( self.Light.On );
    self.Motion.Is("off").For(timeout).And( self.Scene.Is("Normal") ).Then(self.Light.Off);
    pass;
  
  def AutomateNightLight(self, timeout):
    self.Scene.Is("Night").And(self.Motion.Is("on")).Then( self.NightLight.On );
    self.Motion.Is("off").For(timeout).And( self.Scene.Is("Night") ).Then(self.NightLight.Off)
    pass;
  
  def AutomateManualOverride(self, timeout):
    def SetManual(value, arguments):
      self.Scene.SetEnumValue("Manual");
    self.Light.Attribute("external_call").Is(True).Or( self.NightLight.Attribute("external_call").Is(True)).Then(SetManual).Otherwise().For(timeout).And(self.Scene.Is("Manual")).Then(self.Scene.SetEnumToPrevious);

  def AutomateDayNightMode(self, morning, evening):
    def compareTime(value, arguments):
        morning_time = datetime.datetime.now().replace(hour=morning["hour"], minute=morning["minute"]).timestamp();
        evening_time = datetime.datetime.now().replace(hour=evening["hour"], minute=evening["minute"]).timestamp();
        if value == None:
          return False;
        return value > morning_time and value < evening_time;
    
    def SetNight(value, arguments):
      self.Scene.SetEnumValue("Night");
    def SetNormal(value, arguments):
      self.Scene.SetEnumValue("Normal");
    
    fiveMinutes.Is(compareTime).And( self.Scene.Is(lambda val, args: val in ["Normal", "Night"]) ).Then(SetNormal).Else(SetNight);
  
  def AutomateWindow(self, condition):
    condition.Then(self.Window.Cover.Open).Else(self.Window.Cover.Close);
    
  def AutomateDoor(self, condition):
    condition.Then(self.Door.Cover.Open).Else(self.Door.Cover.Close);


################
##### MAIN #####
################

log.error("------------------START SETTING UP PYSCRIPT--------------------");


# Kitchen
log.error("Init kitchen");
kitchen = Room("kitchen");
kitchen.AutomateLight(180);
kitchen.AutomateNightLight(60);
kitchen.AutomateManualOverride(1800);
kitchen.AutomateWindow(sun.Is("above_horizon"));
kitchen.AutomateDayNightMode({"hour": 7, "minute": 0}, {"hour": 21, "minute": 0})


# Bedroom
log.error("Init bedroom");
bedroom = Room("bedroom");
bedroom.AutomateWindow(sun.Is("above_horizon"));
bedroom.AutomateDoor(sun.Is("above_horizon"));


# Corridor
log.error("Init corridor");
corridor = Room("corridor");
corridor.AutomateLight(180);
corridor.AutomateNightLight(60);
corridor.AutomateManualOverride(900);
corridor.AutomateDayNightMode({"hour": 7, "minute": 0}, {"hour": 21, "minute": 0})


# Office
log.error("Init office");
office = Room("office");
office.AutomateLight(300);
office.AutomateDayNightMode({"hour": 7, "minute": 0}, {"hour": 21, "minute": 0})


# Bath
log.error("Init bath");
bath = Room("bath");
bath.AutomateLight(180);
bath.AutomateNightLight(60);
bath.AutomateManualOverride(1800);
bath.AutomateDayNightMode({"hour": 7, "minute": 0}, {"hour": 21, "minute": 0})


log.error("------------------PYSCRIPT SETUP FINISHED--------------------");


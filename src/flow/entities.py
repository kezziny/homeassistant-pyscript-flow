from homeassistant.util.dt import now as dt_now, get_time_zone
from flow.core import Observable;

def TimeRecurring(minute):
  o = Observable();
  
  @time_trigger('period(now, '+ str(minute) +'min)')
  def time_trigger():
      o.SetValue(dt_now(hass.config.time_zone).timestamp(), None)
      
  o.source = time_trigger;
  return o;


def Sensor(entity):
  try:
    test = state.get(entity);
  except:
    log.error("Failed to create sensor: " + str(entity));
    return None;
    
  o = Observable();
  
  @time_trigger('once(now + 3s)')
  @state_trigger(entity, state_check_now=True)
  def state_trigger():
    value = state.get(entity);
    arguments = state.getattr(entity);
    o.SetValue(value, arguments);
  
  def SetEnumValue(value, *args):
    service.call("input_select", "select_option", entity_id=entity, option=value);
  
  def SetEnumToPrevious(*args):
    service.call("input_select", "select_option", entity_id=entity, option=o.LastValue);
  
  o.Source = state_trigger;
  o.SetEnumValue = SetEnumValue;
  o.SetEnumToPrevious = SetEnumToPrevious;
  return o;

def Light(entity):
  try:
    test = state.get(entity);
  except:
    log.error("Failed to create light: " + str(entity));
    return None;
    
  o = Observable();
  o.last_changed = None;
  
  @time_trigger('once(now + 3s)')
  @state_trigger(entity, state_check_now=True)
  def state_trigger():
    value = state.get(entity);
    arguments = state.getattr(entity);
    now = dt_now(hass.config.time_zone).timestamp();
    
    if o.last_changed == None:
      o.last_changed = now;
    
    arguments["external_call"] = False;
    if now - o.last_changed > 1:
      arguments["external_call"] = True;
              
    
    o.SetValue(value, arguments);
  
  def TurnOn(*args):
    o.last_changed = dt_now(hass.config.time_zone).timestamp();
    params = {};
    if len(args) > 0 and isinstance(args[0], dict):
      val = args[0]["value"];
      if isinstance(val, dict):
        for key in ["brightness", "kelvin"]:
          if key in val:
            params[key] = val[key];

    service.call("light", "turn_on", entity_id=entity, **params);
  
  def TurnOff(*args):
    service.call("light", "turn_off", entity_id=entity);
  
  o.Source = state_trigger;
  o.On = TurnOn;
  o.Off = TurnOff;
  return o;

def Cover(entity):
  try:
    test = state.get(entity);
  except:
    log.error("Failed to create cover: " + str(entity));
    return None;
  
  o = Observable();
  o.last_changed = None;
  
  @time_trigger('once(now + 3s)')
  @state_trigger(entity, state_check_now=True)
  def state_trigger():
    value = state.get(entity);
    arguments = state.getattr(entity);
    now = dt_now(hass.config.time_zone).timestamp();
    
    if o.last_changed == None:
      o.last_changed = now;
    
    arguments["external_call"] = False;
    if now - o.last_changed > 1:
      arguments["external_call"] = True;
              
    o.SetValue(value, arguments);
  
  def Open(*args):
    o.last_changed = dt_now(hass.config.time_zone).timestamp();
    service.call("cover", "open_cover", entity_id=entity);
  
  def Close(*args):
    service.call("cover", "close_cover", entity_id=entity);
  
  o.Source = state_trigger;
  o.Open = Open;
  o.Close = Close;
  return o;
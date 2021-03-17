
class SubscriptionType:
  Update = 1;
  Change = 2;
  Positive = 3;
  Negative = 4;


class Observable:
  def __init__(self):
    self.Value = None;
    self.IsTrueish = False;
    self.Arguments = None;
    self.LastValue = None;
    self.Subscriptions = [];

  def SetValue(self, value, arguments):
    positive = self.Condition(value, arguments);
    if not positive:
      value = None;
    
    changed = self.Value != value;

    if changed:
      self.LastValue = self.Value;
      self.Value = value;
      self.Arguments = arguments;

    for subscription in self.Subscriptions:
      if subscription['type'] == SubscriptionType.Update:
        subscription['callback'](value, arguments);
      elif subscription['type'] == SubscriptionType.Change and changed:
        subscription['callback'](value, arguments);
      elif subscription['type'] == SubscriptionType.Positive and positive:
        subscription['callback'](value, arguments);
      elif subscription['type'] == SubscriptionType.Negative and not positive:
        subscription['callback'](value, arguments);
  
  def Condition(self, value, arguments):
    return True;
    
  
  def Updated(self, callback, ref = None):
    self.Subscriptions.append({ 'callback': callback, 'type': SubscriptionType.Update, 'ref': ref });
    
  def Then(self, callback, ref = None):
    self.Subscriptions.append({ 'callback': callback, 'type': SubscriptionType.Positive, 'ref': ref });
    return self;
    
  def Else(self, callback, ref = None):
    self.Subscriptions.append({ 'callback': callback, 'type': SubscriptionType.Negative, 'ref': ref });
    return self;
    
  def Changed(self, callback, ref = None):
    self.Subscriptions.append({ 'callback': callback, 'type': SubscriptionType.Change, 'ref': ref });
    return self;
  
  def Is(self, target):
    def Equal(value, argument):
        return value == target;
        
    o = Observable();
    
    if callable(target):
      o.Condition = target;
    else:
      o.Condition = Equal;
    
    self.Updated(o.SetValue, o);
    return o;
  
  def Otherwise(self):
    o = Observable();
    
    def Not(value, arguments):
      return not self.Condition(value, arguments);
    
    o.Condition = Not;
    
    self.Updated(o.SetValue, o);
    return o;
  
  def IsBelow(self, target):
    def Below(value, argument):
        return value < target;
        
    o = Observable();
    o.Condition = IsBelow;
    
    self.Updated(o.SetValue, o);
    return o;
  
  def IsAbove(self, target):
    def Below(value, argument):
        return value > target;
        
    o = Observable();
    o.Condition = IsAbove;
    
    self.Updated(o.SetValue, o);
    return o;
  
  def IsBetween(self, low, high):
    def Between(value, argument):
        return value < high and value > low;
        
    o = Observable();
    o.Condition = Between;
    
    self.Updated(o.SetValue, o);
    return o;
  
  def Attribute(self, attribute):
    o = Observable();
    
    def UnpackAttribute(value, arguments):
      o.SetValue(arguments[attribute], None);
    
    self.Updated(UnpackAttribute, o);
    return o;
  
  def For(self, seconds):
    o = Observable();
    
    def timeCondition(value, arguments):
      if value != None:
        task.unique(str(self));
        task.sleep(seconds);
        return True;
      else:
        task.unique(str(self));
        return False;
    
    o.Condition = timeCondition;
    self.Updated(o.SetValue, o);
    return o;

  def And(self, observable):
    o = Observable();
    
    def AndCondition(value, arguments):
      return self.Condition(self.Value, self.Arguments) and observable.Condition(observable.Value, observable.Arguments);
    
    
    o.Condition = AndCondition; 
    self.Updated(o.SetValue, o);
    observable.Updated(o.SetValue, o);
    return o;
  
  def Or(self, observable):
    o = Observable();
    
    def OrCondition(value, arguments):
      return self.Condition(self.Value, self.Arguments) or observable.Condition(observable.Value, observable.Arguments);
    
    o.Condition = OrCondition;
    
    self.Updated(o.SetValue, o);
    observable.Updated(o.SetValue, o);
    return o;
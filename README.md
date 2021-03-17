# Install
Copy the content of the **src** folder into **pyscript/modules**

# Usage

```python
from flow.entities import TimeRecurring, Sensor, Light, Cover;

sun = Sensor("sun.sun");

# sun based cover control
cover = Cover('cover.entity_id');
sun.Is('above_horizon').Then(cover.Open).Else(cover.Close);

# motion controlled lighting
motion = Sensor('binary_sensor._motion');
light = Light('light.entity_id');

motion.Is('on').Then(light.TurnOn).Otherwise().For(180).Then(light.TurnOff);

# time based night lights
fiveMinutes = TimeRecurring(5); # not ideal for this purpose but for presentation only :)
nightlight = Light('light.entity_id');

def compareTime(value, arguments):
    morning_time = datetime.datetime.now().replace(hour=7, minute=0).timestamp();
    evening_time = datetime.datetime.now().replace(hour=19, minute=0).timestamp();
    return value != None and (value < morning_time or value > evening_time);

fiveMinutes.Is(compareTime).Then(nightlight.TurnOn).Else(nightlight.TurnOff);
```
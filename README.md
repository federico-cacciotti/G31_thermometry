# G31_thermometry
A Python package useful to convert thermometer readout voltage to temperature for the G31 Cosmology Group at La Sapienza University of Rome.

# Supported thermometers
- Lakeshore DT670 D6068043

# How to add new thermometers
For now it is possible to add only Lakeshore thermometer calibration files, just go to [Lakeshore website](https://www.lakeshore.com/products/categories/temperature-products/cryogenic-temperature-sensors), insert the serial number of a thermometer and download the zip file. Extract the zip file and copy/paste the extracted directory as a subfolder of thermometer model directory.

# How to install
Just open terminal and type
```
pip install G31-thermometry
```

# Example
In this example we define a DT670 thermometer with serial number D6068043 and plot its calibration curve.
```Python
import G31_thermometry as G31t

DT670 = G31t.Thermometer(model='DT670', serial_no='D6068043')
DT670.plotCalibrationCurve()
```
The calibration curve is shown below.

With the following code instead we want to convert measured voltages into temperatures.
```Python
import G31_thermometry as G31t
import numpy as np

DT670 = G31t.Thermometer(model='DT670', serial_no='D6068043')

voltage = np.array([0.5  , 0.625, 0.75 , 0.875, 1.   ])
DT670.temperature()
```
Output (in kelvin):
```
np.array([324.73716731, 270.61138912, 214.82655846, 156.39544034,
        92.6566496 ])
```

## Updates
- 22/07/2022: added DT670 - D6068043

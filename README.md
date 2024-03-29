# G31_thermometry
A Python package useful to convert thermometer readout voltage to temperature for the G31 Cosmology Group at La Sapienza University of Rome.

# Supported thermometers
- Lakeshore DT670 D6068043
- and many others :]

# How to add new thermometers
You can add Lakeshore thermometer calibration files, just go to [Lakeshore website](https://www.lakeshore.com/products/categories/temperature-products/cryogenic-temperature-sensors), insert the serial number of a thermometer and download the zip file. Extract the zip file and copy/paste the extracted directory in the same directory of the script. You can also add text calibration files.

# How to install
WARNING: this is deprecated. Download the latest version from github!
From ipython:
```Python
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
<br/>
<img src="https://github.com/federico-cacciotti/G31_thermometry/blob/main/DT670_D6068043.png" alt="DT670_D6068043_calibration_curve" width="500"/>

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

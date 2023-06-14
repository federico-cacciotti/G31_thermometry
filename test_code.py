import G31_thermometry as G31t

# plot the calibration curve
DT670 = G31t.Thermometer(model='DT670', serial_no='D6068043')
DT670.plotCalibrationCurve()

# convert voltages to temperatures
import numpy as np
voltage = np.array([0.5  , 0.625, 0.75 , 0.875, 1.   ])
DT670.temperature()
import G31_thermometry as G31t

DT670 = G31t.Thermometer(model='DT670', serial_no='D6068043')
DT670.plotCalibrationCurve()
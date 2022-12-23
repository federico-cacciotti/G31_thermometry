from pathlib import Path
import numpy as np

class Thermistor():
    
    def __init__(self, model, serial_no=None):
        # check the existance of the selected thermometer
        self.model = Path(model)
        
        if serial_no != None:
            self.serial_no = Path(serial_no)
            path_to_calibration = Path(__file__).parent.absolute() / self.model / self.serial_no
        else:
            self.serial_no = None
            path_to_calibration = Path(__file__).parent.absolute() / self.model
        
        if not path_to_calibration.exists():
            print('Cannot find the selected thermometer.')
            return
        
        calibration_file = path_to_calibration / (self.model.as_posix()+'.txt')
        calib_temperature, calib_voltage = np.loadtxt(calibration_file, unpack=True)
        self.calibration_data = {'temperature': calib_temperature, 'voltage': calib_voltage}
        
    def readValue(self, file):
        val = file.readline()
        val = val.split(sep=None)
        try:
            val = int(val[-1])
            return val
        except:
            try: 
                val = float(val[-1])
                return val
            except:
                return val[-1]
            
    def temperature(self, voltage):
        voltage = np.asarray(voltage)
        
        V_min_cal = np.min(self.calibration_data['voltage'])
        V_max_cal = np.max(self.calibration_data['voltage'])
        
        if np.min(voltage) < V_min_cal:
            print("There are values lower than the minimum allowed [{:f}]...".format(V_min_cal))
            voltage = voltage[voltage>=V_min_cal]
                
        if np.max(voltage) > V_max_cal:
            print("There are values higher than the minimum allowed [{:f}]...".format(V_max_cal))
            voltage = voltage[voltage<=V_max_cal]
        
    
        # linear interpolation
        from scipy.interpolate import interp1d
        interpolation = interp1d(self.calibration_data['voltage'], self.calibration_data['temperature'], kind='linear')
        temperature = interpolation(voltage)
                
        return temperature
        
    def plotCalibrationCurve(self, ax=None, linestyle='solid', color='black', linewidth=1, label=None):
        V = self.calibration_data['voltage']
        T = self.calibration_data['temperature']
        
        import matplotlib.pyplot as plt
        if ax == None:
            fig = plt.figure(figsize=(7,7))
            ax = fig.gca()
            
        if label == None:
            if self.serial_no == None:
                label = self.model.as_posix()
            else:
                label = self.model.as_posix()+' '+self.serial_no.as_posix()
                
        ax.plot(T, V, linestyle=linestyle, color=color, linewidth=linewidth, label=label)
        ax.set_xlabel('Temperature [K]')
        ax.set_ylabel('Resistance [Ohm]')
        ax.grid(alpha=0.5)
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.legend(loc='best')
        
        plt.show()
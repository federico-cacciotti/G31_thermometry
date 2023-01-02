from pathlib import Path
import numpy as np

class Thermistor():
    
    def __init__(self, model, serial_no=None, label=None):
        # check the existance of the selected thermometer
        self.model = Path(model)
        
        if serial_no != None:
            self.serial_no = Path(serial_no)
            path_to_calibration = Path(__file__).parent.absolute() / self.model / self.serial_no
        else:
            self.serial_no = None
            path_to_calibration = Path(__file__).parent.absolute() / self.model
            
        print("Searching thermometer data at", path_to_calibration)
        
        if label == None:
            self.label = self.model
        else:
            self.label = label
        
        if not path_to_calibration.exists():
            print('Cannot find the selected thermometer.')
            return
        
        calibration_file = path_to_calibration / (self.model.as_posix()+'.txt')
        calib_temperature, calib_voltage = np.loadtxt(calibration_file, unpack=True)
        self.calibration_data = {'temperature': calib_temperature, 'resistance': calib_voltage}
        
            
    def temperature(self, resistance):
        
        R_calib_min = self.calibration_data['resistance'].min()
        R_calib_max = self.calibration_data['resistance'].max()
        
        # replace with nan values outside the calibrated range
        resistance = np.asarray(resistance)
        if resistance.size == 1:
            resistance = [resistance]
        resistance = np.asarray([np.nan if v_i < R_calib_min or v_i > R_calib_max else v_i for v_i in resistance])
        
        if any(np.isnan(resistance)):
            print(self.label+": one ore more values are outside of the calibration range. Replaced with NaN values.")
        
        # linear interpolation
        from scipy.interpolate import interp1d
        interpolation = interp1d(self.calibration_data['resistance'], self.calibration_data['temperature'], kind='linear')
        temperature = interpolation(resistance)
                
        if temperature.size == 1:
            return temperature.item()
        else:
            return temperature
        
    def plotCalibrationCurve(self, ax=None, linestyle='solid', color='black', linewidth=1, label=None):
        R = self.calibration_data['resistance']
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
                
        ax.plot(T, R, linestyle=linestyle, color=color, linewidth=linewidth, label=label)
        ax.set_xlabel('Temperature [K]')
        ax.set_ylabel('Resistance [Ohm]')
        ax.grid(alpha=0.5)
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.legend(loc='best')
        
        plt.show()
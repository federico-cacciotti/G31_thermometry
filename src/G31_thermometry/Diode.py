from pathlib import Path
import numpy as np

class Diode():
    
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
        
        # open the calibration file
        try:
            calibration_file = path_to_calibration / (self.serial_no.as_posix()+'.cof')
            cal_file = open(calibration_file, 'r')
            
            fit_range = []
            fit_type = []
            fit_order = []
            Z_lower = []
            Z_upper = []
            V_lower = []
            V_upper = []
            cheb_coeffs = []
            
            # read the number of fit ranges
            number_of_fit_ranges = self.readValue(cal_file)
            self.calibration_data = {'number_of_fit_ranges': number_of_fit_ranges}
            
            for n_fit in range(number_of_fit_ranges):
                fit_range.append(self.readValue(cal_file))
                fit_type.append(self.readValue(cal_file))
                fit_order.append(self.readValue(cal_file))
                Z_lower.append(self.readValue(cal_file))
                Z_upper.append(self.readValue(cal_file))
                
                # voltage limits
                V_lower.append(self.readValue(cal_file))
                V_upper.append(self.readValue(cal_file))
                
                # chebichev coefficients
                c = []
                for i in range(fit_order[-1]+1):
                    c.append(self.readValue(cal_file))
                cheb_coeffs.append(c)
            
            self.calibration_data['fit_range'] = fit_range
            self.calibration_data['fit_type'] = fit_type
            self.calibration_data['fit_order'] = fit_order
            self.calibration_data['Z_lower'] = Z_lower
            self.calibration_data['Z_upper'] = Z_upper
            self.calibration_data['V_upper'] = V_upper
            self.calibration_data['V_lower'] = V_lower
            self.calibration_data['cheb_coeffs'] = cheb_coeffs
            
            cal_file.close()
        except:
            pass
        
        try:
            calibration_file = path_to_calibration / (self.model.as_posix()+'.txt')
            calib_temperature, calib_voltage = np.loadtxt(calibration_file, unpack=True)
            self.calibration_data = {'temperature': calib_temperature, 'voltage': calib_voltage}
        except:
            pass
        
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
        
        try:
            V_min_cal = np.min(self.calibration_data['V_lower'])
            V_max_cal = np.max(self.calibration_data['V_upper'])
        except:
            pass
        
        try:
            V_min_cal = np.min(self.calibration_data['voltage'])
            V_max_cal = np.max(self.calibration_data['voltage'])
        except:
            pass
        
        if np.min(voltage) < V_min_cal:
            print("There are values lower than the minimum allowed [{:f}]...".format(V_min_cal))
            voltage = voltage[voltage>=V_min_cal]
                
        if np.max(voltage) > V_max_cal:
            print("There are values higher than the minimum allowed [{:f}]...".format(V_max_cal))
            voltage = voltage[voltage<=V_max_cal]
        
        
        try:
            temperature = np.zeros(voltage.size)
            # from chebychev polynomials
            for cal in range(self.calibration_data['number_of_fit_ranges']):
                v_min = self.calibration_data['V_lower'][cal]
                v_max = self.calibration_data['V_upper'][cal]
                
                keep = np.logical_and(voltage>=v_min, voltage<=v_max)
                Z = voltage[keep]
                if Z.size != 0:
                    ZL = self.calibration_data['Z_lower'][cal]
                    ZU = self.calibration_data['Z_upper'][cal]
                    k = self.__k__(Z, ZL, ZU)
                    
                    temperature[keep] = 0.0
                    for i,c in enumerate(self.calibration_data['cheb_coeffs'][cal]):
                        temperature[keep] += c*np.cos(i*np.arccos(k))
        except:
            pass
        
        try:
            # linear interpolation
            from scipy.interpolate import interp1d
            interpolation = interp1d(self.calibration_data['voltage'], self.calibration_data['temperature'], kind='linear')
            temperature = interpolation(voltage)
        except:
            pass
                
        return temperature
    
    def __k__(self, Z, ZL, ZU):
        return ((Z-ZL)-(ZU-Z))/(ZU-ZL)
    
        
    def plotCalibrationCurve(self, ax=None, linestyle='solid', color='black', linewidth=1, label=None):
        try:
            V_min = np.min(self.calibration_data['V_lower'])
            V_max = np.max(self.calibration_data['V_upper'])
            V = np.linspace(V_min, V_max, num=500)
            T = self.temperature(V)
        except:
            pass
        
        try:
            V = self.calibration_data['voltage']
            T = self.calibration_data['temperature']
        except:
            pass
        
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
        ax.set_ylabel('Voltage [V]')
        ax.grid(alpha=0.5)
        #ax.set_xscale('log')
        ax.legend(loc='best')
        
        plt.show()
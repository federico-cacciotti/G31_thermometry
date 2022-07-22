from pathlib import Path
import numpy as np

class Thermometer():
    
    def __init__(self, model, serial_no):
        # check the existance of the selected thermometer
        self.model = Path(model)
        self.serial_no = Path(serial_no)
        path_to_calibration = Path(__file__).parent.absolute() / self.model / self.serial_no
        
        if not path_to_calibration.exists():
            print('Cannot find the selected thermometer.')
            return
        
        # open the calibration file
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
        
        V_min_cal = np.min(self.calibration_data['V_lower'])
        V_max_cal = np.max(self.calibration_data['V_upper'])
        
        if np.min(voltage) < V_min_cal:
            print("There are values lower than the minimum allowed [{:f}]...".format(V_min_cal))
            voltage = voltage[voltage>=V_min_cal]
            return None
                
        if np.max(voltage) > V_max_cal:
            print("There are values higher than the minimum allowed [{:f}]...".format(V_max_cal))
            voltage = voltage[voltage<=V_max_cal]
            return None
        
        temperature = np.zeros(voltage.size)
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
                
        return temperature
    
    def __k__(self, Z, ZL, ZU):
        return ((Z-ZL)-(ZU-Z))/(ZU-ZL)
    
        
    def plotCalibrationCurve(self):
        T = []
        V_min = np.min(self.calibration_data['V_lower'])
        V_max = np.max(self.calibration_data['V_upper'])
        V = np.linspace(V_min, V_max, num=500)
        
        T = self.temperature(V)
        
        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(7,7))
        
        plt.title('model: '+self.model.as_posix()+' serial_no: '+self.serial_no.as_posix())
        ax0 = plt.subplot(111)
        ax0.plot(T, V, linestyle='-', color='black')
        ax0.set_xlabel('Temperature [K]')
        ax0.set_ylabel('Voltage [V]')
        ax0.grid(alpha=0.5)
        ax0.set_xscale('log')
        
        plt.show()
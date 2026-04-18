#Patch validator JH

import psutil
import subprocess
import datetime
import json
import time
from tabulate import tabulate

class HardwareValidator:
    def __init__(self):
        self.results = []
        self.report_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def log_result(self, Test_name, Status, Details):
        """Save the test result for the final report."""
        self.results.append ([Test_name, Status, Details])

    def check_cpu(self):
        try:
            cmd = "lscpu | grep 'Model name' | cut -d ':' -f 2"
            cpu_model = subprocess.check_output(cmd, shell=True).decode().strip()

            if 'Intel' in cpu_model:
                self.log_result('CPU Identification', 'PASS', cpu_model)
            else:
                self.log_result('CPU Identification', 'WARNING', f'Non-Intel: {cpu_model}')
        except Exception as e:
            self.log_result('CPU Identification', 'FAIL', str(e))

    def ram_check(self, expected_gb):
        try:
            total_ram = round(psutil.virtual_memory().total / (1024**3))

            if total_ram >= expected_gb -1:
                self.log_result('RAM Capacity', 'PASS', f'{total_ram}GB Detected')
            else:
                self.log_result('RAM Capacity', 'Fail', f'Expected {expected_gb}GB, found {total_ram}GB')
        except Exception as e:
            self.log_result('RAM Capacity', 'Error', f'Unespected error:{str(e)}')

    def ssd_check(self, limit_percentage=95):
        try:
            disk_info = psutil.disk_usage('/')
            total_gb = round(disk_info.total / (1024**3))
            used_percent = disk_info.percent

            if used_percent >= limit_percentage:
                self.log_result('SSD Capacity', 'WARNING', f'Disk nearly full{used_percent}% used')
            else:
                self.log_result('SSD Capacity', 'PASS', f'{used_percent}% used of total {total_gb}GB')
        except Exception as e:
            self.log_result('SSD Capacity', 'Error', f'Unespected error:{str(e)}')
    
    def temp_check(self, limit_temp=80):
        try:
            current_temp = self.get_current_temp()

            if current_temp >= limit_temp:
                self.log_result('CPU Temperature', 'WARNING', f'High Temperature: {current_temp}°C')
            elif current_temp == 0:
                self.log_result('CPU Temperature', 'FAIL', 'Could not read sensor')
            else:
                self.log_result('CPU Temperature', 'PASS', f'{current_temp}°C(Stable)')
        except Exception as e:
            self.log_result('CPU Temperature', 'Error', f'Unespected error:{str(e)}')

    def get_current_temp(self):
        temps = psutil.sensors_temperatures()
        if 'k10temp' in temps:
            return temps['k10temp'][0].current
        elif 'coretemp' in temps:
            return temps['coretemp'][0].current
        return 0

    def cpu_stress_test(self, duration=10):
        try:
            start_temp = self.get_current_temp()

            print(f'[ACTION] Starting CPU Stress Test for {duration} seconds. . .')
            end_time = time.time() + duration
            while time.time() < end_time:
                _ = [x**2 for x in range(10000)]

            final_temp = self.get_current_temp()
            delta = final_temp - start_temp
            
            if delta < 25:
                status = 'PASS'
                detail = f'Cooling efficient. Delta: +{round(delta, 1)}°C'
            elif delta < 35:
                status = 'WARNING'
                detail = f'High thermal load. Delta +{round(delta, 1)}°C'
            else:
                status = 'FAIL'
                detail = f'Thermal runaway detected! Delta +{round(delta, 1)}°C'

            self.log_result('CPU Stress Test', status, detail)

        except Exception as e:
            self.log_result('CPU Stress Test', 'Error', str(e))

    def generate_report(self):
        print('\n' + '='*50)
        print(f'INTEL SYSTEM VALIDATION REPORT')
        print(f'Date: {self.report_time}')
        print('='*50)

        if not self.results:
            print('No test results found')
            return
        
        headers = ['Test Case', 'Status', 'Details/Measurment']
        print(tabulate(self.results, headers=headers, tablefmt='grid'))
        print('='*50 + '\n')

    def save_to_json(self, filename = 'report.json'):
        try:
            report_data = {
                'report_date': self.report_time,
                'test_results': self.results
            }
            
            with open(filename, 'w') as f:
                json.dump(report_data, f, indent=4)

            print(f'[INFO] Report saved successfully to {filename}')

        except Exception as e:
            print(f'[ERROR] Could not save report: {e}')

if __name__ == '__main__':
    tester = HardwareValidator()
    tester.check_cpu()
    tester.ram_check(32)
    tester.ssd_check(95)
    tester.temp_check(80)
    tester.cpu_stress_test(duration=10)

    tester.generate_report()
    tester.save_to_json()
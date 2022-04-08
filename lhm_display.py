
from time import sleep
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import requests

global lhm_data
global error
lhm_data = {}
error = None

class Config:
    lhm_url = 'http://localhost:8092/data.json'
    refresh_interval = 1
    stay_on_top = True
    background_color =  'black'
    font_color = 'white'

def format_lhm_data(data):
    output = {}
    output['system_name'] = data['Children'][0]['Text']
    data = data['Children'][0]
    output['cpu_name'] = data['Children'][1]['Text']
    output['cpu_temp'] = data['Children'][1]['Children'][3]['Children'][0]['Value']
    output['cpu_load'] = data['Children'][1]['Children'][4]['Children'][0]['Value']
    output['memory_load'] = data['Children'][2]['Children'][0]['Children'][0]['Value']
    output['gpu_name'] = data['Children'][3]['Text']
    output['gpu_temp'] = data['Children'][3]['Children'][2]['Children'][0]['Value']
    output['gpu_load'] = data['Children'][3]['Children'][3]['Children'][0]['Value']
    output['eth_download'] = data['Children'][8]['Children'][2]['Children'][0]['Value']
    output['eth_upload'] = data['Children'][8]['Children'][2]['Children'][1]['Value']
    
    for k,v in output.items():
        output[k] = v.replace('°','')

    return output

class Scraper(QThread):

    def  __init__(self, win_updater, url=Config.lhm_url, refresh_interval=Config.refresh_interval):
        super().__init__()
        self._do_loop = True
        self._url = url
        self._interval = refresh_interval
        self._wu = win_updater

    def run(self):
        while self._do_loop:
            self.get_lhm_data()
            sleep(self._interval)

    def stop(self):
        self._do_loop = False

    def get_lhm_data(self):
        global lhm_data
        global error
        try:
            r = requests.get(self._url)
            if r.status_code == 200:
                lhm_data = r.json()
                self._wu.update()
            else:
                raise Exception(f'Web request error: {r.status_code}')
        except Exception as e:
            print(e)
            error = e

class WindowUpdater(object):

    def __init__(self, win) -> None:
        self._win = win
    
    def update(self):
        global lhm_data
        global error
        data = format_lhm_data(lhm_data)
        self._win.lbl_val_sys_name.setText(data['system_name'])
        self._win.lbl_val_cpu_name.setText(data['cpu_name'])
        self._win.lbl_val_cpu_temp.setText(data['cpu_temp'])
        self._win.lbl_val_cpu_load.setText(data['cpu_load'])
        self._win.lbl_val_memory_load.setText(data['memory_load'])
        self._win.lbl_val_gpu_name.setText(data['gpu_name'])
        self._win.lbl_val_gpu_temp.setText(data['gpu_temp'])
        self._win.lbl_val_gpu_load.setText(data['gpu_load'])
        self._win.lbl_val_eth_down.setText(data['eth_download'])
        self._win.lbl_val_eth_up.setText(data['eth_upload'])

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        stylesheet = f'background-color: {Config.background_color};color: {Config.font_color};'
        self.setStyleSheet(stylesheet)

        self.setWindowTitle('LHM Viewer')

        layout = QGridLayout()
        self.setLayout(layout)

        self.lbl_ttl_sys_name = QLabel('System')
        self.lbl_val_sys_name = QLabel('')
        layout.addWidget(self.lbl_ttl_sys_name,0,0)
        layout.addWidget(self.lbl_val_sys_name,0,1)

        self.lbl_spacer_1 = QLabel('')
        layout.addWidget(self.lbl_spacer_1,1,0)

        self.lbl_ttl_cpu_name = QLabel('CPU')
        self.lbl_val_cpu_name = QLabel('')
        layout.addWidget(self.lbl_ttl_cpu_name,2,0)
        layout.addWidget(self.lbl_val_cpu_name,2,1)

        self.lbl_ttl_cpu_temp = QLabel('Temp')
        self.lbl_val_cpu_temp = QLabel('')
        layout.addWidget(self.lbl_ttl_cpu_temp,3,0)
        layout.addWidget(self.lbl_val_cpu_temp,3,1)

        self.lbl_ttl_cpu_load = QLabel('Load')
        self.lbl_val_cpu_load = QLabel('')
        layout.addWidget(self.lbl_ttl_cpu_load,4,0)
        layout.addWidget(self.lbl_val_cpu_load,4,1)

        self.lbl_spacer_5 = QLabel('')
        layout.addWidget(self.lbl_spacer_5,5,0)

        self.lbl_ttl_memory_load = QLabel('RAM')
        self.lbl_val_memory_load = QLabel('')
        layout.addWidget(self.lbl_ttl_memory_load,6,0)
        layout.addWidget(self.lbl_val_memory_load,6,1)

        self.lbl_spacer_7 = QLabel('')
        layout.addWidget(self.lbl_spacer_7,7,0)

        self.lbl_ttl_gpu_name = QLabel('GPU')
        self.lbl_val_gpu_name = QLabel('')
        layout.addWidget(self.lbl_ttl_gpu_name,8,0)
        layout.addWidget(self.lbl_val_gpu_name,8,1)

        self.lbl_ttl_gpu_temp = QLabel('Temp')
        self.lbl_val_gpu_temp = QLabel('')
        layout.addWidget(self.lbl_ttl_gpu_temp,9,0)
        layout.addWidget(self.lbl_val_gpu_temp,9,1)

        self.lbl_ttl_gpu_load = QLabel('Load')
        self.lbl_val_gpu_load = QLabel('')
        layout.addWidget(self.lbl_ttl_gpu_load,10,0)
        layout.addWidget(self.lbl_val_gpu_load,10,1)

        self.lbl_spacer_11 = QLabel('')
        layout.addWidget(self.lbl_spacer_11,11,0)

        self.lbl_ttl_eth_down = QLabel('Eth Down')
        self.lbl_val_eth_down = QLabel('')
        layout.addWidget(self.lbl_ttl_eth_down,12,0)
        layout.addWidget(self.lbl_val_eth_down,12,1)

        self.lbl_ttl_eth_up = QLabel('Eth Up')
        self.lbl_val_eth_up = QLabel('')
        layout.addWidget(self.lbl_ttl_eth_up,13,0)
        layout.addWidget(self.lbl_val_eth_up,13,1)

        if Config.stay_on_top:
            self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
            #self.setWindowFlags(Qt.FramelessWindowHint)

        self.win_updater = WindowUpdater(self)
        self.scraper = Scraper(win_updater=self.win_updater)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos() 

app = QApplication(sys.argv)
screen = Window()
screen.show()
screen.scraper.start()

sys.exit(app.exec_())



# Import Modules
import tkinter as tk
import sv_ttk as sv
from tkinter import ttk, font, IntVar

# Read JSON file and Store Data
import json
with open('./config_gui.json', 'r') as file:
    data = json.load(file)

# Import Python Files
from GUIs.LiveButtons import *
from GUIs.LiveHome import *
from GUIs.LiveCam import *
from GUIs.LiveGraph import *
from GUIs.LiveLabels import registerLiveLabel, registerLiveBar, updateLiveLabel

    
class Tab1(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        class Menu_Bar(ttk.Frame):
            def __init__(self, parent):
                super().__init__(parent, padding=data['paddingSize']['frame'])
                
                # Toggle GUI & Quit GUI
                root.toggle_switch_gui = IntVar()
                menu_controls(self)

                # Toggle Monitor Switch
                self.toggle_switch_1 = IntVar()
                self.switch_1 = ttk.Checkbutton(self, style='Switch.TCheckbutton', variable=self.toggle_switch_1, text='Monitor', command=lambda: switchODrive(root, self.toggle_switch_1))

                # Toggle Control Loop Switch
                self.toggle_switch_2 = IntVar()
                self.switch_2 = ttk.Checkbutton(self, style='Switch.TCheckbutton', variable=self.toggle_switch_2, text='Control Loop', command=lambda: switchControlLoop(self.toggle_switch_2))
                
                # Layout
                self.switch_1.pack(padx=(4, 4), side='left')
                self.switch_2.pack(padx=(4, 4), side='left')
  
        class Box_1(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='ODrive', padding=data['paddingSize']['labelFrame'])

                class add_widgets_top(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        for index in range(2):
                            self.columnconfigure(index, weight=1, uniform='1')
                        for index in (0, 2, 4):
                            self.rowconfigure(index, weight=1, minsize=data['rowSize']['label'])
                        for index in (1, 3, 5):
                            self.rowconfigure(index, weight=1, minsize=data['rowSize']['progressBar'])

                        # MOSFET M1
                        self.label_1 = ttk.Label(self, text='MOSFET M0')
                        self.output_1 = ttk.Label(self, text='°C')
                        self.progress_1 = ttk.Progressbar(self, mode='determinate', value=0)

                        # Live Labels & Bars
                        registerLiveLabel('MF0Temp', self.output_1, self.output_1['text'])
                        registerLiveBar('MF0TempBar', self.progress_1, self.progress_1['value'])

                        # MOSFET M2
                        self.label_2 = ttk.Label(self, text='MOSFET M1')
                        self.output_2 = ttk.Label(self, text='°C')    
                        self.progress_2 = ttk.Progressbar(self, mode='determinate', value=0)
                        
                        # Live Labels & Bars
                        registerLiveLabel('MF1Temp', self.output_2, self.output_2['text'])
                        registerLiveBar('MF1TempBar', self.progress_2, self.progress_2['value'])
                        
                        # MOSFET BRAKES
                        self.label_3 = ttk.Label(self, text='MOSFET BRAKES')
                        self.output_3 = ttk.Label(self, text='°C')
                        self.progress_3 = ttk.Progressbar(self, mode='determinate', value=0)
                        
                        # Live Labels & Bars
                        registerLiveLabel('MFBrakesTemp', self.output_3, self.output_3['text'])
                        registerLiveBar('MFBrakesTempBar', self.progress_3, self.progress_3['value'])

                        # Layout
                        self.label_1.grid(row=0, column=0, pady=(4, 4), sticky='W')
                        self.output_1.grid(row=0, column=1, pady=(4, 4), sticky='E')
                        self.progress_1.grid(row=1, columnspan=2, sticky='NEW')

                        self.label_2.grid(row=2, column=0, pady=(4, 4), sticky='W')
                        self.output_2.grid(row=2, column=1, pady=(4, 4), sticky='E')
                        self.progress_2.grid(row=3, columnspan=2, sticky='NEW')

                        self.label_3.grid(row=4, column=0, pady=(4, 4), sticky='W')
                        self.output_3.grid(row=4, column=1, pady=(4, 4), sticky='E')
                        self.progress_3.grid(row=5, columnspan=2, sticky='NEW')

                class add_widgets_bot(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        # Stop Button
                        self.button_1 = ttk.Button(self, text='Stop', style='Toggle.TButton', command=stopODrive)

                        # Calibrate Button
                        self.button_2 = ttk.Button(self, text='Calibrate ODrive', style='Toggle.TButton', command=lambda: calibrateControls('ODrive'))

                        # Layout
                        self.button_1.pack(fill='x', pady=(0, 4))
                        self.button_2.pack(fill='x', pady=(4, 0))

                add_widgets_top(self).pack(fill='x', side='top')
                add_widgets_bot(self).pack(fill='x', side='bottom')

        class Box_2(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Motors', padding=data['paddingSize']['labelFrame'])

                class add_widgets_top(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        for index in range(3):
                            self.columnconfigure(index, weight=1, uniform='1')
                        for index in range(6):
                            self.rowconfigure(index, weight=1, uniform='1', minsize=data['rowSize']['label'])

                        # Side Labels
                        self.label_1 = ttk.Label(self, text='Status')
                        self.label_2 = ttk.Label(self, text='State')
                        self.label_3 = ttk.Label(self, text='Current')
                        self.label_4 = ttk.Label(self, text='Velocity')
                        self.label_5 = ttk.Label(self, text='Temperature')

                        # M1 Display Values
                        self.label_01 = ttk.Label(self, text='M0')
                        self.output_11 = ttk.Label(self, text='-')
                        self.output_21 = ttk.Label(self, text='A')
                        self.output_31 = ttk.Label(self, text='-')
                        self.output_41 = ttk.Label(self, text='°C')
                        self.progress_1 = ttk.Progressbar(self, mode='determinate', value=0)
                        
                        # Live Labels & Bars
                        registerLiveLabel('M0State', self.output_11, self.output_11['text'])
                        registerLiveLabel('M0Current', self.output_21, self.output_21['text'])
                        registerLiveLabel('M0Velocity', self.output_31, self.output_31['text'])
                        registerLiveLabel('M0Temp', self.output_41, self.output_41['text'])
                        registerLiveBar('M0TempBar', self.progress_1, self.progress_1['value'])

                        # M2 Display Values
                        self.label_02 = ttk.Label(self, text='M1')
                        self.output_12 = ttk.Label(self, text='-')
                        self.output_22 = ttk.Label(self, text='A')
                        self.output_32 = ttk.Label(self, text='-')
                        self.output_42 = ttk.Label(self, text='°C')
                        self.progress_2 = ttk.Progressbar(self, mode='determinate', value=0)
                        
                        # Live Labels & Bars
                        registerLiveLabel('M1State', self.output_12, self.output_12['text'])
                        registerLiveLabel('M1Current', self.output_22, self.output_22['text'])
                        registerLiveLabel('M1Velocity', self.output_32, self.output_32['text'])
                        registerLiveLabel('M1Temp', self.output_42, self.output_42['text'])
                        registerLiveBar('M1TempBar', self.progress_2, self.progress_2['value'])

                        # Layout Column 1
                        self.label_1.grid(row=0, column=0, padx=(0, 4), sticky='EW')
                        self.label_2.grid(row=1, column=0, padx=(0, 4), sticky='EW')
                        self.label_3.grid(row=2, column=0, padx=(0, 4), sticky='EW')
                        self.label_4.grid(row=3, column=0, padx=(0, 4), sticky='EW')
                        self.label_5.grid(row=4, column=0, padx=(0, 4), sticky='EW')

                        # Layout Column 2
                        self.label_01.grid(row=0, column=1, padx=(4, 4), sticky='E')
                        self.output_11.grid(row=1, column=1, padx=(4, 4), sticky='E')
                        self.output_21.grid(row=2, column=1, padx=(4, 4), sticky='E')
                        self.output_31.grid(row=3, column=1, padx=(4, 4), sticky='E')
                        self.output_41.grid(row=4, column=1, padx=(4, 4), sticky='E')
                        self.progress_1.grid(row=5, column=1, padx=(4, 4), sticky='NEW')

                        # Layout Column 3
                        self.label_02.grid(row=0, column=2, padx=(4, 0), sticky='E')
                        self.output_12.grid(row=1, column=2, padx=(4, 0), sticky='E')
                        self.output_22.grid(row=2, column=2, padx=(4, 0), sticky='E')
                        self.output_32.grid(row=3, column=2, padx=(4, 0), sticky='E')
                        self.output_42.grid(row=4, column=2, padx=(4, 0), sticky='E')
                        self.progress_2.grid(row=5, column=2, padx=(4, 0), sticky='NEW')

                class add_widgets_bot(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        for index in range(3):
                            self.columnconfigure(index, weight=1, uniform='1')

                        # Calibrate
                        self.button_1 = ttk.Button(self, style='Toggle.TButton', text='Calibrate Both', command=lambda: calibrateControls('M1'))
                        self.button_2 = ttk.Button(self, style='Toggle.TButton', text='Calibrate M0', command=lambda: calibrateControls('M2'))
                        self.button_3 = ttk.Button(self, style='Toggle.TButton', text='Calibrate M1', command=lambda: calibrateControls('Both'))

                        # Layout
                        self.button_1.grid(row=0, column=0, padx=(0, 4), sticky='EW')
                        self.button_2.grid(row=0, column=1, padx=(4, 4), sticky='EW')
                        self.button_3.grid(row=0, column=2, padx=(4, 0), sticky='EW')

                add_widgets_top(self).pack(fill='x', side='top')
                add_widgets_bot(self).pack(fill='x', side='bottom')

        class Box_3(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Dashboard', padding=data['paddingSize']['labelFrame'])

                for index in range(5):
                    self.columnconfigure(index, weight=1, uniform='1')
                for index in range(5):
                    self.rowconfigure(index, weight=1, uniform='1', minsize=data['rowSize']['label'])
                
                # System Labels
                self.system_label_0 = ttk.Label(self, text='Controllers')
                self.system_label_1 = ttk.Label(self, text='RPI')
                self.system_label_2 = ttk.Label(self, text='JETSON')
                self.system_label_3 = ttk.Label(self, text='ODRIVE')
                self.system_label_4 = ttk.Label(self, text='ARDUINO')

                # Status Labels
                self.status_label_0 = ttk.Label(self, text='System')
                self.status_label_1 = ttk.Label(self, text='-')
                self.status_label_2 = ttk.Label(self, text='-')
                self.status_label_3 = ttk.Label(self, text='-')
                self.status_label_4 = ttk.Label(self, text='-')
                
                # Live Labels & Bars
                registerLiveLabel('raspberryStatus', self.status_label_1, self.status_label_1['text'])
                registerLiveLabel('jetsonStatus', self.status_label_2, self.status_label_2['text'])
                registerLiveLabel('odriveStatus', self.status_label_3, self.status_label_3['text'])
                registerLiveLabel('arduinoStatus', self.status_label_4, self.status_label_4['text'])

                # Side Labels
                self.label_0 = ttk.Label(self, text='Errors')
                self.label_1 = ttk.Label(self, text='System')
                self.label_2 = ttk.Label(self, text='Motor')
                self.label_3 = ttk.Label(self, text='Controller')
                self.label_4 = ttk.Label(self, text='Encoder')

                # Axis 1 Display Values
                self.label_01 = ttk.Label(self, text='Axis 0')
                self.output_11 = ttk.Label(self, text='-')
                self.output_21 = ttk.Label(self, text='-')
                self.output_31 = ttk.Label(self, text='-')
                self.output_41 = ttk.Label(self, text='-')

                # Live Labels & Bars
                registerLiveLabel('A0AxisError', self.output_11, self.output_11['text'])
                registerLiveLabel('A0MotorError', self.output_21, self.output_21['text'])
                registerLiveLabel('A0ControllerError', self.output_31, self.output_31['text'])
                registerLiveLabel('A0EncoderError', self.output_41, self.output_41['text'])

                # Axis 2 Display Values
                self.label_02 = ttk.Label(self, text='Axis 1')
                self.output_12 = ttk.Label(self, text='-')
                self.output_22 = ttk.Label(self, text='-')
                self.output_32 = ttk.Label(self, text='-')
                self.output_42 = ttk.Label(self, text='-')
                
                # Live Labels & Bars
                registerLiveLabel('A1AxisError', self.output_12, self.output_12['text'])
                registerLiveLabel('A1MotorError', self.output_22, self.output_22['text'])
                registerLiveLabel('A1ControllerError', self.output_32, self.output_32['text'])
                registerLiveLabel('A1EncoderError', self.output_42, self.output_42['text'])
                
                # System Status Layout
                self.system_label_0.grid(row=0, column=0, padx=(0, 4), sticky='EW')
                self.system_label_1.grid(row=1, column=0, padx=(0, 4), sticky='EW')
                self.system_label_2.grid(row=2, column=0, padx=(0, 4), sticky='EW')
                self.system_label_3.grid(row=3, column=0, padx=(0, 4), sticky='EW')
                self.system_label_4.grid(row=4, column=0, padx=(0, 4), sticky='EW')

                self.status_label_0.grid(row=0, column=1, padx=(4, 0), sticky='W')
                self.status_label_1.grid(row=1, column=1, padx=(4, 0), sticky='W')
                self.status_label_2.grid(row=2, column=1, padx=(4, 0), sticky='W')
                self.status_label_3.grid(row=3, column=1, padx=(4, 0), sticky='W')
                self.status_label_4.grid(row=4, column=1, padx=(4, 0), sticky='W')

                # Left & Right - Odrive Status Layout
                self.label_0.grid(row=0, column=2, padx=(0, 4), sticky='EW')
                self.label_1.grid(row=1, column=2, padx=(0, 4), sticky='EW')
                self.label_2.grid(row=2, column=2, padx=(0, 4), sticky='EW')
                self.label_3.grid(row=3, column=2, padx=(0, 4), sticky='EW')
                self.label_4.grid(row=4, column=2, padx=(0, 4), sticky='EW')

                self.label_01.grid(row=0, column=3, padx=(4, 4), sticky='EW')
                self.output_11.grid(row=1, column=3, padx=(4, 4), sticky='EW')
                self.output_21.grid(row=2, column=3, padx=(4, 4), sticky='EW')
                self.output_31.grid(row=3, column=3, padx=(4, 4), sticky='EW')
                self.output_41.grid(row=4, column=3, padx=(4, 4), sticky='EW')

                self.label_02.grid(row=0, column=4, padx=(4, 0), sticky='EW')
                self.output_12.grid(row=1, column=4, padx=(4, 0), sticky='EW')
                self.output_22.grid(row=2, column=4, padx=(4, 0), sticky='EW')
                self.output_32.grid(row=3, column=4, padx=(4, 0), sticky='EW')
                self.output_42.grid(row=4, column=4, padx=(4, 0), sticky='EW')

        class Box_4(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Battery', padding=data['paddingSize']['labelFrame'])

                for index in range(2):
                    self.columnconfigure(index, weight=1, uniform='1')
                for index in range(2):
                    self.rowconfigure(index, weight=1, uniform='1', minsize=data['rowSize']['label'])
                self.rowconfigure(2, weight=1, minsize=data['rowSize']['progressBar'])
                        
                # Battery
                self.label_1 = ttk.Label(self, text='Voltage')
                self.label_2 = ttk.Label(self, text='Temperature')

                # Battery Display Values
                self.output_1 = ttk.Label(self, text='V')
                self.output_2 = ttk.Label(self, text='°C')
                self.progress_2 = ttk.Progressbar(self, mode='determinate')
                
                # Live Labels & Bars
                registerLiveLabel('batteryVoltage', self.output_1, self.output_1['text'])
                registerLiveLabel('batteryTemp', self.output_2, self.output_2['text'])
                registerLiveBar('batteryTempBar', self.progress_2, self.progress_2['value'])

                # Layout
                self.label_1.grid(row=0, column=0, sticky='EW')
                self.label_2.grid(row=1, column=0, sticky='EW')
                self.output_1.grid(row=0, column=1, sticky='E')
                self.output_2.grid(row=1, column=1, sticky='E')
                self.progress_2.grid(row=2, column=0, columnspan=2, sticky='NEW')

        class Box_5(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Speed & Steering', padding=data['paddingSize']['labelFrame'])

                class add_widgets_top(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        for index in range(2):
                            self.columnconfigure(index, weight=1, uniform='1')
                        for index in (0, 2):
                            self.rowconfigure(index, weight=1, minsize=data['rowSize']['label'])
                        for index in (1, 3):
                            self.rowconfigure(index, weight=1, minsize=data['rowSize']['progressBar'])

                        # Speed
                        self.label_1 = ttk.Label(self, text='Speed')
                        self.output_1 = ttk.Label(self, text='-')
                        self.progress_1 = ttk.Progressbar(self, value=50, mode='indeterminate')
                        
                        # Live Labels & Bars
                        registerLiveLabel('speed', self.output_1, self.output_1['text'])
                        registerLiveBar('speedBar', self.progress_1, self.progress_1['value'])

                        # Steering
                        self.label_2 = ttk.Label(self, text='Steering')
                        self.output_2 = ttk.Label(self, text='-')
                        self.progress_2 = ttk.Progressbar(self, value=50, mode='indeterminate')
                        
                        # Live Labels & Bars
                        registerLiveLabel('steerAngle', self.output_2, self.output_2['text'])
                        registerLiveBar('steerAngleBar', self.progress_2, self.progress_2['value'])

                        # Layout
                        self.label_1.grid(row=0, column=0, sticky='EW')
                        self.output_1.grid(row=0, column=1, sticky='E')
                        self.progress_1.grid(row=1, column=0, columnspan=2, sticky='NEW')
                        self.label_2.grid(row=2, column=0, sticky='EW')
                        self.output_2.grid(row=2, column=1, sticky='E')
                        self.progress_2.grid(row=3, column=0, columnspan=2, sticky='NEW')

                class add_widgets_bot(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        # Steering Button
                        self.button_steering = ttk.Button(self, text='Calibrate Steering', style='Toggle.TButton', command=lambda: calibrateControls('steering'))

                        # Layout
                        self.button_steering.pack(fill='x', pady=(8, 0))

                add_widgets_top(self).pack(fill='x', side='top')
                add_widgets_bot(self).pack(fill='x', side='bottom')

        class Box_6(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Controls', padding=data['paddingSize']['labelFrame'])
                
                # Choose Control Type == 'keyboard' or 'controller'
                if data['controlSettings']['controlType'] == 'keyboard':

                    class add_widgets_left(ttk.Frame):
                        def __init__(self, parent):
                            super().__init__(parent, padding=data['paddingSize']['frame'])

                            for index in range(0, 6, 2):
                                self.columnconfigure(index, weight=1, uniform='1', minsize=36)
                            for index in range(1, 5, 2):
                                self.columnconfigure(index, weight=0, minsize=6)
                            for index in range(0, 3, 2):
                                self.rowconfigure(index, weight=1, uniform='1', minsize=36)
                            self.rowconfigure(1, weight=1, minsize=6)

                            # Keyboard Buttons
                            self.label_key_w = ttk.Button(self, style='Toggle.TButton', text=data['keyboardKeybinds']['speedUp'].upper(), command=lambda: movementControls('up'))
                            self.label_key_s = ttk.Button(self, style='Toggle.TButton', text=data['keyboardKeybinds']['speedDown'].upper(), command=lambda: movementControls('down'))
                            self.label_key_a = ttk.Button(self, style='Toggle.TButton', text=data['keyboardKeybinds']['steerLeft'].upper(), command=lambda: movementControls('left'))
                            self.label_key_d = ttk.Button(self, style='Toggle.TButton', text=data['keyboardKeybinds']['steerRight'].upper(), command=lambda: movementControls('right'))

                            # Layout
                            self.label_key_w.grid(row=0, column=2, sticky='NSEW')
                            self.label_key_a.grid(row=2, column=0, sticky='NSEW')
                            self.label_key_s.grid(row=2, column=2, sticky='NSEW')
                            self.label_key_d.grid(row=2, column=4, sticky='NSEW')

                            self.bindings()

                        def bindings(self):
                            root.bind(keyState(data['keyboardKeybinds']['speedUp'], True), lambda event: keyPress(self.label_key_w, True))
                            root.bind(keyState(data['keyboardKeybinds']['speedUp'], False), lambda event: keyPress(self.label_key_w, False))
                            root.bind(keyState(data['keyboardKeybinds']['speedDown'], True), lambda event: keyPress(self.label_key_s, True))
                            root.bind(keyState(data['keyboardKeybinds']['speedDown'], False), lambda event: keyPress(self.label_key_s, False))
                            root.bind(keyState(data['keyboardKeybinds']['steerLeft'], True), lambda event: keyPress(self.label_key_a, True))
                            root.bind(keyState(data['keyboardKeybinds']['steerLeft'], False), lambda event: keyPress(self.label_key_a, False))
                            root.bind(keyState(data['keyboardKeybinds']['steerRight'], True), lambda event: keyPress(self.label_key_d, True))
                            root.bind(keyState(data['keyboardKeybinds']['steerRight'], False), lambda event: keyPress(self.label_key_d, False))

                    class add_widgets_right(ttk.Frame):
                        def __init__(self, parent):
                            super().__init__(parent, padding=data['paddingSize']['frame'])

                            self.columnconfigure(0, weight=1, uniform='1', minsize=36*2)
                            for index in range(0, 3, 2):
                                self.rowconfigure(index, weight=1, uniform='1', minsize=36)
                            self.rowconfigure(1, minsize=6)

                            # Keyboard Buttons
                            self.label_key_x = ttk.Button(self, style='Toggle.TButton', text=data['keyboardKeybinds']['speedBrake'].upper(), command=lambda: movementControls('brake'))

                            # Layout
                            self.label_key_x.grid(row=2, sticky='NSEW')

                            self.bindings()

                        def bindings(self):
                            root.bind(keyState(data['keyboardKeybinds']['speedBrake'], True), lambda event: keyPress(self.label_key_x, True))
                            root.bind(keyState(data['keyboardKeybinds']['speedBrake'], False), lambda event: keyPress(self.label_key_x, False))

                    add_widgets_left(self).pack(side='left')
                    add_widgets_right(self).pack(side='right')

                if data['controlSettings']['controlType'] == 'controller':
                    
                    class add_widgets_top(ttk.Frame):
                        def __init__(self, parent):
                            super().__init__(parent, padding=data['paddingSize']['frame'])
                            
                            # Controller Buttons
                            self.label_key_lt = ttk.Button(self, style='Toggle.TButton', text='LT', command=lambda: movementControls('lt'))
                            self.label_key_lb = ttk.Button(self, style='Toggle.TButton', text='LB', command=lambda: movementControls('lb'))
                            self.label_key_rt = ttk.Button(self, style='Toggle.TButton', text='RT', command=lambda: movementControls('rt'))
                            self.label_key_rb = ttk.Button(self, style='Toggle.TButton', text='RB', command=lambda: movementControls('rb'))
                            
                            # # Layout
                            self.label_key_lt.pack(padx=(0, 2), side='left')
                            self.label_key_lb.pack(padx=(2, 0), side='left')
                            self.label_key_rt.pack(padx=(2, 0), side='right')
                            self.label_key_rb.pack(padx=(0, 2), side='right')
                            
                            self.bindings()
                            
                        def bindings(self):
                            registerKeybinds(data['controllerKeybinds']['LT'], lambda state: keyPress(self.label_key_lt, state))
                            registerKeybinds(data['controllerKeybinds']['LB'], lambda state: keyPress(self.label_key_lb, state))
                            registerKeybinds(data['controllerKeybinds']['RT'], lambda state: keyPress(self.label_key_rt, state))
                            registerKeybinds(data['controllerKeybinds']['RB'], lambda state: keyPress(self.label_key_rb, state))
                        
                    class add_widgets_left(ttk.Frame):
                        def __init__(self, parent):
                            super().__init__(parent, padding=data['paddingSize']['frame'])

                            # Controller Buttons
                            self.label_key_up = ttk.Button(self, style='Toggle.TButton', text='  ')
                            self.label_key_down = ttk.Button(self, style='Toggle.TButton', text='  ')
                            self.label_key_left = ttk.Button(self, style='Toggle.TButton', text='  ')
                            self.label_key_right = ttk.Button(self, style='Toggle.TButton', text='  ')

                            # Layout
                            self.label_key_left.pack(padx=(0, 3), side='left')
                            self.label_key_right.pack(padx=(3, 0), side='right')
                            self.label_key_up.pack(pady=(0, 2), side='top')
                            self.label_key_down.pack(pady=(2, 0), side='top')

                            self.bindings()

                        def bindings(self):
                            registerKeybinds(data['controllerKeybinds']['UP'], lambda state: keyPress(self.label_key_up, state))
                            registerKeybinds(data['controllerKeybinds']['DOWN'], lambda state: keyPress(self.label_key_down, state))
                            registerKeybinds(data['controllerKeybinds']['LEFT'], lambda state: keyPress(self.label_key_left, state))
                            registerKeybinds(data['controllerKeybinds']['RIGHT'], lambda state: keyPress(self.label_key_right, state))

                    class add_widgets_right(ttk.Frame):
                        def __init__(self, parent):
                            super().__init__(parent, padding=data['paddingSize']['frame'])

                            # Keyboard Buttons
                            self.label_key_x = ttk.Button(self, style='Toggle.TButton', text='  ', command=lambda: movementControls('x'))
                            self.label_key_y = ttk.Button(self, style='Toggle.TButton', text='  ', command=lambda: movementControls('y'))
                            self.label_key_a = ttk.Button(self, style='Toggle.TButton', text='  ', command=lambda: movementControls('a'))
                            self.label_key_b = ttk.Button(self, style='Toggle.TButton', text='  ', command=lambda: movementControls('b'))

                            # Layout
                            self.label_key_x.pack(padx=(0, 3), side='left')
                            self.label_key_b.pack(padx=(3, 0), side='right')
                            self.label_key_y.pack(pady=(0, 2), side='top')
                            self.label_key_a.pack(pady=(2, 0), side='top')

                            self.bindings()

                        def bindings(self):
                            registerKeybinds(data['controllerKeybinds']['Y'], lambda state: keyPress(self.label_key_y, state))
                            registerKeybinds(data['controllerKeybinds']['B'], lambda state: keyPress(self.label_key_b, state))
                            registerKeybinds(data['controllerKeybinds']['A'], lambda state: keyPress(self.label_key_a, state))
                            registerKeybinds(data['controllerKeybinds']['X'], lambda state: keyPress(self.label_key_x, state))

                    class add_widgets_bot(ttk.Frame):
                        def __init__(self, parent):
                            super().__init__(parent, padding=data['paddingSize']['frame'])
                            
                            # Controller Buttons
                            self.label_key_start = ttk.Button(self, style='Toggle.TButton', text='START', command=lambda: movementControls('up'))
                            
                            # # Layout
                            self.label_key_start.pack(padx=(0, 2), side='top')
                            
                            self.bindings()
                            
                        def bindings(self):
                            registerKeybinds(data['controllerKeybinds']['START'], lambda state: keyPress(self.label_key_start, state))

                    add_widgets_top(self).pack(fill='x', side='top')
                    add_widgets_bot(self).pack(fill='x', side='bottom')
                    add_widgets_left(self).pack(expand=1, side='left')
                    add_widgets_right(self).pack(expand=1, side='right')

        # Set Layout UI Boxes
        self.columnconfigure(0, weight=1, uniform='1')
        self.columnconfigure(1, weight=2, uniform='1')
        self.columnconfigure(2, weight=1, uniform='1')
        for index in (1, 2, 3):
            self.rowconfigure(index, weight=1)

        Menu_Bar(self).grid(row=0, columnspan=3, sticky='EW')
        Box_1(self).grid(row=1, rowspan=2, column=0, padx=(0, 4), pady=(4, 4), sticky='NSEW')
        Box_2(self).grid(row=1, rowspan=2, column=1, padx=(4, 4), pady=(4, 4), sticky='NSEW')
        Box_3(self).grid(row=3, column=0, columnspan=2, padx=(0, 4), pady=(4, 0), sticky='NSEW')
        Box_4(self).grid(row=1, column=2, padx=(4, 0), pady=(4, 4), sticky='NSEW')
        Box_5(self).grid(row=2, column=2, padx=(4, 0), pady=(4, 4), sticky='NSEW')
        Box_6(self).grid(row=3, column=2, padx=(4, 0), pady=(4, 0), sticky='NSEW')


class Tab2(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        class Menu_Bar(ttk.Frame):
            def __init__(self, parent):
                super().__init__(parent, padding=data['paddingSize']['frame'])
                
                # Toggle GUI & Quit GUI
                menu_controls(self)

                # Toggle Camera Switch
                self.toggle_switch_1 = IntVar()
                self.switch_1 = ttk.Checkbutton(self, style='Switch.TCheckbutton', variable=self.toggle_switch_1, text='Display Cam', command=lambda: switchCamera(self.master.opencv.label, self.toggle_switch_1))

                # Layout
                self.switch_1.pack(padx=(4, 4), side='left')

        class Box_1(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Settings', padding=data['paddingSize']['labelFrame'])

                for index in range(2):
                    self.columnconfigure(index, weight=1, uniform='1')
                for index in range(5):
                    self.rowconfigure(index, weight=1, minsize=data['rowSize']['label'])

                # Settings Labels
                self.label_1 = ttk.Label(self, text='Camera Resolution')
                self.label_2 = ttk.Label(self, text='Target FPS')
                self.label_3 = ttk.Label(self, text='Image Resolution')
                self.label_4 = ttk.Label(self, text='Image FPS')

                # LiveLabels
                self.output_1 = ttk.Label(self, text='-')
                registerLiveLabel('camResolution', self.output_1, self.output_1['text'])
                self.output_2 = ttk.Label(self, text='-')
                registerLiveLabel('camFPS', self.output_2, self.output_2['text'])
                self.output_3 = ttk.Label(self, text='-')
                registerLiveLabel('imageResolution', self.output_3, self.output_3['text'])
                self.output_4 = ttk.Label(self, text='-')
                registerLiveLabel('imageFPS', self.output_4, self.output_4['text'])

                # Layout
                self.label_1.grid(row=0, column=0, sticky='EW')
                self.label_2.grid(row=1, column=0, sticky='EW')
                self.label_3.grid(row=3, column=0, sticky='EW')
                self.label_4.grid(row=4, column=0, sticky='EW')
                self.output_1.grid(row=0, column=1, sticky='E')
                self.output_2.grid(row=1, column=1, sticky='E')
                self.output_3.grid(row=3, column=1, sticky='E')
                self.output_4.grid(row=4, column=1, sticky='E')  
                
        class Box_2(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Camera', padding=data['paddingSize']['labelFrame'])

                self.label = ttk.Label(self)
                self.label.pack(expand=1)

        # Set Layout UI Boxes
        self.columnconfigure(0, weight=1, uniform='1')
        self.columnconfigure(1, weight=3, uniform='1')
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)

        Menu_Bar(self).grid(row=0, columnspan=2, sticky='EW')
        Box_1(self).grid(row=1, column=0, padx=(0, 4), pady=(4, 4), sticky='NSEW')
        self.opencv = Box_2(self)
        self.opencv.grid(row=1, rowspan=2, column=1, padx=(4, 0), pady=(4, 0), sticky='NSEW')


class Tab3(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        class Menu_Bar(ttk.Frame):
            def __init__(self, parent):
                super().__init__(parent, padding=data['paddingSize']['frame'])
                
                # Toggle GUI & Quit GUI
                menu_controls(self)

                # Toggle Monitor Temperature Switch
                self.toggle_switch_1 = IntVar()
                self.switch_1 = ttk.Checkbutton(self, style='Switch.TCheckbutton', variable=self.toggle_switch_1, text='Monitor', command=lambda: switchMonitor(root, self.toggle_switch_1))

                # Toggle Temperature Graph Switch
                self.toggle_switch_2 = IntVar()
                self.switch_2 = ttk.Checkbutton(self, style='Switch.TCheckbutton', variable=self.toggle_switch_2, text='Graph', command=lambda: switchGraph(self.master.graph.label, self.toggle_switch_2))

                # Layout
                self.switch_1.pack(padx=(4, 4), side='left')
                self.switch_2.pack(padx=(4, 4), side='left')

        class Box_1(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Sensor', padding=data['paddingSize']['labelFrame'])

                self.columnconfigure(0, weight=0, uniform='1', minsize=36)
                self.columnconfigure(1, weight=1)
                for index in range(6):
                    self.rowconfigure(index, weight=1, minsize=data['rowSize']['label'])

                # Sensor Buttons
                self.var = IntVar()
                self.radio_1 = ttk.Radiobutton(self, style='Toggle.TButton', variable=self.var, value=0, text='1', command=lambda: selectSensor(self.var))
                self.radio_2 = ttk.Radiobutton(self, style='Toggle.TButton', variable=self.var, value=1, text='2', command=lambda: selectSensor(self.var))
                self.radio_3 = ttk.Radiobutton(self, style='Toggle.TButton', variable=self.var, value=2, text='3', command=lambda: selectSensor(self.var))
                self.radio_4 = ttk.Radiobutton(self, style='Toggle.TButton', variable=self.var, value=3, text='4', command=lambda: selectSensor(self.var))
                self.radio_5 = ttk.Radiobutton(self, style='Toggle.TButton', variable=self.var, value=4, text='5', command=lambda: selectSensor(self.var))
                self.radio_6 = ttk.Radiobutton(self, style='Toggle.TButton', variable=self.var, value=5, text='6', command=lambda: selectSensor(self.var))

                # Sensor Labels
                self.label_1 = ttk.Label(self, text='Sensor 1')
                self.label_2 = ttk.Label(self, text='Sensor 2')
                self.label_3 = ttk.Label(self, text='Sensor 3')
                self.label_4 = ttk.Label(self, text='Sensor 4')
                self.label_5 = ttk.Label(self, text='Sensor 5')
                self.label_6 = ttk.Label(self, text='Sensor 6')

                # Layout
                self.radio_1.grid(row=0, column=0, pady=(0, 4), sticky='EW')
                self.radio_2.grid(row=1, column=0, pady=(4, 4), sticky='EW')
                self.radio_3.grid(row=2, column=0, pady=(4, 4), sticky='EW')
                self.radio_4.grid(row=3, column=0, pady=(4, 4), sticky='EW')
                self.radio_5.grid(row=4, column=0, pady=(4, 4), sticky='EW')
                self.radio_6.grid(row=5, column=0, pady=(4, 0), sticky='EW')

                self.label_1.grid(row=0, column=1, padx=(8, 0), pady=(0, 4), sticky='W')
                self.label_2.grid(row=1, column=1, padx=(8, 0), pady=(4, 4), sticky='W')
                self.label_3.grid(row=2, column=1, padx=(8, 0), pady=(4, 4), sticky='W')
                self.label_4.grid(row=3, column=1, padx=(8, 0), pady=(4, 4), sticky='W')
                self.label_5.grid(row=4, column=1, padx=(8, 0), pady=(4, 4), sticky='W')
                self.label_6.grid(row=5, column=1, padx=(8, 0), pady=(4, 0), sticky='W')
                
        class Box_2(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Monitor', padding=data['paddingSize']['labelFrame'])

                class add_widgets_top(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        for index in range(2):
                            self.columnconfigure(index, weight=1, uniform='1')
                        for index in range(4):
                            self.rowconfigure(index, weight=1, minsize=data['rowSize']['label'])

                        # Temperature
                        self.label_1 = ttk.Label(self, text='Current Temp')
                        self.label_2 = ttk.Label(self, text='Highest Temp')
                        self.label_3 = ttk.Label(self, text='Lowest Temp')

                        # LiveLabels
                        self.output_1 = ttk.Label(self, text='°C')
                        registerLiveLabel('currentTemp', self.output_1, self.output_1['text'])
                        self.output_2 = ttk.Label(self, text='°C')
                        registerLiveLabel('highestTemp', self.output_2, self.output_2['text'])
                        self.output_3 = ttk.Label(self, text='°C')
                        registerLiveLabel('lowestTemp', self.output_3, self.output_3['text'])

                        # Layout
                        self.label_1.grid(row=0, column=0, sticky='EW')
                        self.label_2.grid(row=2, column=0, sticky='EW')
                        self.label_3.grid(row=3, column=0, sticky='EW')
                        self.output_1.grid(row=0, column=1, sticky='E')
                        self.output_2.grid(row=2, column=1, sticky='E')
                        self.output_3.grid(row=3, column=1, sticky='E')

                class add_widgets_bot(ttk.Frame):
                    def __init__(self, parent):
                        super().__init__(parent, padding=data['paddingSize']['frame'])

                        # Clear Temperature Button
                        self.button_1 = ttk.Button(self, style='Toggle.TButton', text='Clear', command=lambda: clearTemp())
                        self.button_1.pack(fill='x')

                add_widgets_top(self).pack(fill='x', side='top')
                add_widgets_bot(self).pack(fill='x', side='bottom')

        class Box_3(ttk.Labelframe):
            def __init__(self, parent):
                super().__init__(parent, text='Graph', padding=data['paddingSize']['labelFrame'])

                self.label = ttk.Label(self)
                self.label.pack(expand=1)

        # Set Layout UI Boxes
        self.columnconfigure(0, weight=1, uniform='1')
        self.columnconfigure(1, weight=3, uniform='1')
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)

        Menu_Bar(self).grid(row=0, columnspan=2, sticky='EW')
        Box_1(self).grid(row=1, column=0, padx=(0, 4), pady=(4, 4), sticky='NSEW')
        Box_2(self).grid(row=2, column=0, padx=(0, 4), pady=(4, 0), sticky='NSEW')
        self.graph = Box_3(self)
        self.graph.grid(row=1, rowspan=2, column=1, padx=(4, 0), pady=(4, 0), sticky='NSEW')


class App(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create Notebook & Tabs as Frames
        self.notebook = ttk.Notebook(self, style='TNotebook')
        self.tab_1 = ttk.Frame(self.notebook, padding=data['paddingSize']['appFrame'])
        self.tab_2 = ttk.Frame(self.notebook, padding=data['paddingSize']['appFrame'])
        self.tab_3 = ttk.Frame(self.notebook, padding=data['paddingSize']['appFrame'])

        # Add Tabs in Notebook
        self.notebook.add(self.tab_1, text='Home')
        self.notebook.add(self.tab_2, text='Cam')
        self.notebook.add(self.tab_3, text='Graph')
        self.notebook.pack(expand=1, fill='both')

        # Layout for Each Tab Frame
        Tab1(self.tab_1).pack(expand=1, fill='both')
        Tab2(self.tab_2).pack(expand=1, fill='both')
        Tab3(self.tab_3).pack(expand=1, fill='both')

        # Initialise All Buttons to be Disabled Except Power & Close Button (shouldToggle = False)
        toggleAllChildren(self, False)


def main():
    global root
    root = tk.Tk()

    # Configure the root window
    root.title('GUI')
    w = data['windowSettings']['width']     # 1024px
    h = data['windowSettings']['height']    # 600px

    # Calculate Starting X and Y coordinates for Window
    x = (root.winfo_screenwidth()/2) - (w/2)
    y = (root.winfo_screenheight()/2) - (h/2)

    # Open window at the center of the screen and is borderless
    root.geometry('%dx%d+%d+%d'%(w, h, x, y))
    root.overrideredirect(data['windowSettings']['borderless'])
    root.resizable(width=data['windowSettings']['resizable'], height=data['windowSettings']['resizable'])

    # Set theme
    sv.set_theme('dark')
    
    # Set Default Fonts (TkDefaultFont/SunValleyBodyFont/SunValleyBodyStrongFont)
    default_font = font.nametofont('SunValleyBodyFont')
    default_font.configure(family=data['fontSettings']['family'], size=data['fontSettings']['size'])
    default_font = font.nametofont('SunValleyBodyStrongFont')
    default_font.configure(family=data['fontSettings']['family'], size=data['fontSettings']['size'], weight=data['fontSettings']['weight'])

    # Load GUI
    App(root).pack(expand=1, fill='both')

    # Initialise Registered Labels
    updateLiveLabel(root)
    root.mainloop()


def menu_controls(self):
    # Toggle GUI
    self.button_0 = ttk.Checkbutton(self, style='Switch.TCheckbutton', variable=root.toggle_switch_gui, text='GUI', command=lambda: systemGUI(root, root.toggle_switch_gui))
    self.button_0.shouldToggle = False
    
    # Quit GUI
    self.button_1 = ttk.Button(self, style='Toggle.TButton', text='❌', command=lambda: systemShutdown(root))
    self.button_1.shouldToggle = False
    
    # Layout
    self.button_0.pack(padx=(0, 4), side='left')
    self.button_1.pack(padx=(4, 0), side='right')
    
    # Bind Keys
    root.bind('<KeyPress-Escape>', lambda event: keyPress(self.button_1, True))
    registerKeybinds('BTN_BACK', lambda state: keyPress(self.button_1, state))


if __name__ == '__main__':
    main()
  

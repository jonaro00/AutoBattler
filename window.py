import tkinter as tk
import tkinter.font as tkf
from tkinter import ttk

import config
from arduino import USBSerial, TimerWorker
from scripts import scripts


class Window(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.create_widgets()
        self.pack()
        self.after_idle(self.data_init)

    def data_init(self):
        self.config_keys = {
            'A1Port':  {'type':'external','short_name':'A1P','entry':self.sbx_a1_port,  'default':  5,'peek_command':''  },
            'A1Rest':  {'type':'external','short_name':'A1R','entry':self.sbx_a1_rest,  'default':  0,'peek_command':'S1'},
            'A1Untap': {'type':'external','short_name':'A1U','entry':self.sbx_a1_untap, 'default': 10,'peek_command':'S1'},
            'A1Tap':   {'type':'external','short_name':'A1T','entry':self.sbx_a1_tap,   'default': 20,'peek_command':'S1'},
            'A2Port':  {'type':'external','short_name':'A2P','entry':self.sbx_a2_port,  'default':  6,'peek_command':''  },
            'A2Rest':  {'type':'external','short_name':'A2R','entry':self.sbx_a2_rest,  'default':  0,'peek_command':'S2'},
            'A2Untap': {'type':'external','short_name':'A2U','entry':self.sbx_a2_untap, 'default': 10,'peek_command':'S2'},
            'A2Tap':   {'type':'external','short_name':'A2T','entry':self.sbx_a2_tap,   'default': 20,'peek_command':'S2'},
            'A3Port':  {'type':'external','short_name':'A3P','entry':self.sbx_a3_port,  'default':  7,'peek_command':''  },
            'A3Rest':  {'type':'external','short_name':'A3R','entry':self.sbx_a3_rest,  'default':180,'peek_command':'S3'},
            'A3Untap': {'type':'external','short_name':'A3U','entry':self.sbx_a3_untap, 'default':170,'peek_command':'S3'},
            'A3Tap':   {'type':'external','short_name':'A3T','entry':self.sbx_a3_tap,   'default':160,'peek_command':'S3'},
            'TapDelay':{'type':'external','short_name':'TD' ,'entry':self.sbx_tap_delay,'default':140,'peek_command':''  },
            'Timing':  {'type':'internal',                   'entry':self.sbx_timing,   'default':300,'peek_command':''  },
        }
        self.config = config.load()
        self.parse_config()

        self.serial = None
        self.scripts = scripts
        self.worker = None

        self.cbx_script.configure(values=[sc['name'] for sc in self.scripts])
        self.cbx_script.current(0)

    def create_widgets(self):
        self.font_H1 = tkf.Font(font=("Arial", 14))
        self.font_H2 = tkf.Font(font=("Arial", 12))
        self.font_H3 = tkf.Font(font=("Arial", 10))
        # self.font_it = tkf.Font(font=("Arial", 10, "italic"))

        self.style = ttk.Style()
        self.style.configure("TLabelframe", padding=(5,0,5,5))
        self.style.configure("TButton", padding=4)
        self.style.configure("TSpinbox", padding=2)
        self.style.configure("TLabel", font=self.font_H3)

        def enable(self):
            self.state(statespec=('!disabled',))
        ttk.Widget.enable = enable
        def disable(self):
            self.state(statespec=('disabled', '!focus'))
        ttk.Widget.disable = disable

        # >FRAME: CONSOLE
        self.frm_console = ttk.Frame(self)
        self.frm_console.grid(row=0, column=0, padx=2, pady=2, sticky='NESW')
        self.lbl_console = ttk.Label(self.frm_console, text='Output', font=self.font_H1)
        self.lbl_console.pack(side=tk.TOP)
        ttk.Separator(self.frm_console, orient='horizontal').pack(fill=tk.BOTH)
        self.lbx_console = tk.Listbox(self.frm_console, width=40, height=32)
        self.lbx_console.pack(fill=tk.BOTH, expand=True)

        # >FRAME: CONTROLS
        self.frm_control = ttk.Frame(self)
        self.frm_control.grid(row=0, column=1, padx=2, pady=2, sticky='NESW')
        self.lbl_control = ttk.Label(self.frm_control, text='Controls', font=self.font_H1)
        self.lbl_control.pack()
        # >>FRAME: CONNECTION
        ttk.Separator(self.frm_control, orient='horizontal').pack(fill=tk.BOTH)
        self.lfm_connect = ttk.Labelframe(self.frm_control, text='Connection')
        self.lfm_connect.pack(fill=tk.BOTH)
        self.lbl_port = ttk.Label(self.lfm_connect, text='Port ID:')
        self.lbl_port.grid(       row=0, column=0, sticky='E')
        self.tbx_port_content = tk.StringVar(value='COM4')
        self.tbx_port = ttk.Entry(self.lfm_connect, textvariable=self.tbx_port_content, width=12)
        self.tbx_port.bind('<Key-Return>', self.btn_connect_click)
        self.tbx_port.grid(       row=0, column=1)
        self.lbl_connected = ttk.Label(self.lfm_connect, text='Not Connected', background='red', width=14)
        self.lbl_connected.grid(  row=0, column=10, rowspan=2, sticky='NS', padx=2, pady=2)
        self.btn_connect = ttk.Button(self.lfm_connect, text='Connect', command=self.btn_connect_click)
        self.btn_connect.grid(    row=1, column=0)
        self.btn_connect.bind('<Key-Return>', lambda *_: self.btn_connect_click())
        self.btn_disconnect = ttk.Button(self.lfm_connect, text='Disconnect', command=self.btn_disconnect_click)
        self.btn_disconnect.grid( row=1, column=1)
        self.btn_disconnect.bind('<Key-Return>', lambda *_: self.btn_disconnect_click())
        # SETTINGS
        self.lfm_settings = ttk.Labelframe(self.frm_control, text='Settings')
        self.lfm_settings.pack(fill=tk.BOTH)
        self.lbl_a1_port = ttk.Label(self.lfm_settings, text='A1 Port:')
        self.lbl_a1_port.grid(    row=11, column=0)
        self.sbx_a1_port = ttk.Spinbox(self.lfm_settings, from_=2, to=13, format='%.0f', width=2)
        self.sbx_a1_port.grid(    row=11, column=1)
        self.lbl_a1_rest = ttk.Label(self.lfm_settings, text='A1 Rest:')
        self.lbl_a1_rest.grid(    row=11, column=2)
        self.sbx_a1_rest = ttk.Spinbox(self.lfm_settings, from_=0, to=180, format='%.0f', width=4, command=(lambda *_: self.sbx_change('A1Rest')))
        self.sbx_a1_rest.bind('<Key-Return>', lambda *_: self.sbx_change('A1Rest'))
        self.sbx_a1_rest.grid(    row=11, column=3)
        self.lbl_a1_untap = ttk.Label(self.lfm_settings, text='A1 Untap:')
        self.lbl_a1_untap.grid(   row=11, column=4)
        self.sbx_a1_untap = ttk.Spinbox(self.lfm_settings, from_=0, to=180, format='%.0f', width=4, command=(lambda *_: self.sbx_change('A1Untap')))
        self.sbx_a1_untap.bind('<Key-Return>', lambda *_: self.sbx_change('A1Untap'))
        self.sbx_a1_untap.grid(   row=11, column=5)
        self.lbl_a1_tap = ttk.Label(self.lfm_settings, text='A1 Tap:')
        self.lbl_a1_tap.grid(     row=11, column=6)
        self.sbx_a1_tap = ttk.Spinbox(self.lfm_settings, from_=0, to=180, format='%.0f', width=4, command=(lambda *_: self.sbx_change('A1Tap')))
        self.sbx_a1_tap.bind('<Key-Return>', lambda *_: self.sbx_change('A1Tap'))
        self.sbx_a1_tap.grid(     row=11, column=7)

        self.lbl_a2_port = ttk.Label(self.lfm_settings, text='A2 Port:')
        self.lbl_a2_port.grid(    row=12, column=0)
        self.sbx_a2_port = ttk.Spinbox(self.lfm_settings, from_=2, to=13, format='%.0f', width=2)
        self.sbx_a2_port.grid(    row=12, column=1)
        self.lbl_a2_rest = ttk.Label(self.lfm_settings, text='A2 Rest:')
        self.lbl_a2_rest.grid(    row=12, column=2)
        self.sbx_a2_rest = ttk.Spinbox(self.lfm_settings, from_=0, to=180, format='%.0f', width=4, command=(lambda *_: self.sbx_change('A2Rest')))
        self.sbx_a2_rest.bind('<Key-Return>', lambda *_: self.sbx_change('A2Rest'))
        self.sbx_a2_rest.grid(    row=12, column=3)
        self.lbl_a2_untap = ttk.Label(self.lfm_settings, text='A2 Untap:')
        self.lbl_a2_untap.grid(   row=12, column=4)
        self.sbx_a2_untap = ttk.Spinbox(self.lfm_settings, from_=0, to=180, format='%.0f', width=4, command=(lambda *_: self.sbx_change('A2Untap')))
        self.sbx_a2_untap.bind('<Key-Return>', lambda *_: self.sbx_change('A2Untap'))
        self.sbx_a2_untap.grid(   row=12, column=5)
        self.lbl_a2_tap = ttk.Label(self.lfm_settings, text='A2 Tap:')
        self.lbl_a2_tap.grid(     row=12, column=6)
        self.sbx_a2_tap = ttk.Spinbox(self.lfm_settings, from_=0, to=180, format='%.0f', width=4, command=(lambda *_: self.sbx_change('A2Tap')))
        self.sbx_a2_tap.bind('<Key-Return>', lambda *_: self.sbx_change('A2Tap'))
        self.sbx_a2_tap.grid(     row=12, column=7)

        self.lbl_a3_port = ttk.Label(self.lfm_settings, text='A3 Port:')
        self.lbl_a3_port.grid(    row=13, column=0)
        self.sbx_a3_port = ttk.Spinbox(self.lfm_settings, from_=2, to=13, format='%.0f', width=2)
        self.sbx_a3_port.grid(    row=13, column=1)
        self.lbl_a3_rest = ttk.Label(self.lfm_settings, text='A3 Rest:')
        self.lbl_a3_rest.grid(    row=13, column=2)
        self.sbx_a3_rest = ttk.Spinbox(self.lfm_settings, from_=0, to=180, format='%.0f', width=4, command=(lambda *_: self.sbx_change('A3Rest')))
        self.sbx_a3_rest.bind('<Key-Return>', lambda *_: self.sbx_change('A3Rest'))
        self.sbx_a3_rest.grid(    row=13, column=3)
        self.lbl_a3_untap = ttk.Label(self.lfm_settings, text='A3 Untap:')
        self.lbl_a3_untap.grid(   row=13, column=4)
        self.sbx_a3_untap = ttk.Spinbox(self.lfm_settings, from_=0, to=180, format='%.0f', width=4, command=(lambda *_: self.sbx_change('A3Untap')))
        self.sbx_a3_untap.bind('<Key-Return>', lambda *_: self.sbx_change('A3Untap'))
        self.sbx_a3_untap.grid(   row=13, column=5)
        self.lbl_a3_tap = ttk.Label(self.lfm_settings, text='A3 Tap:')
        self.lbl_a3_tap.grid(     row=13, column=6)
        self.sbx_a3_tap = ttk.Spinbox(self.lfm_settings, from_=0, to=180, format='%.0f', width=4, command=(lambda *_: self.sbx_change('A3Tap')))
        self.sbx_a3_tap.bind('<Key-Return>', lambda *_: self.sbx_change('A3Tap'))
        self.sbx_a3_tap.grid(     row=13, column=7)

        self.lbl_timing = ttk.Label(self.lfm_settings, text='Timing (ms):')
        self.lbl_timing.grid(     row=14, column=0, columnspan=2)
        self.sbx_timing = ttk.Spinbox(self.lfm_settings, from_=0, to=1000, increment=10, format='%.0f', width=4, command=(lambda *_: self.sbx_change('Timing')))
        self.sbx_timing.bind('<Key-Return>', lambda *_: self.sbx_change('Timing'))
        self.sbx_timing.grid(     row=14, column=2)
        self.lbl_tap_delay = ttk.Label(self.lfm_settings, text='Tap delay (ms):')
        self.lbl_tap_delay.grid(  row=14, column=3, columnspan=2)
        self.sbx_tap_delay = ttk.Spinbox(self.lfm_settings, from_=0, to=500, increment=5, format='%.0f', width=4, command=(lambda *_: self.sbx_change('TapDelay')))
        self.sbx_timing.bind('<Key-Return>', lambda *_: self.sbx_change('TapDelay'))
        self.sbx_tap_delay.grid(  row=14, column=5)
        self.btn_save_config = ttk.Button(self.lfm_settings, text='Save current settings', command=self.btn_save_config_click)
        self.btn_save_config.grid(row=20, column=0, columnspan=8)
        self.btn_save_config.bind('<Key-Return>', lambda *_: self.btn_save_config_click())
        # RUN
        self.lfm_run = ttk.Labelframe(self.frm_control, text='Run')
        self.lfm_run.pack(fill=tk.BOTH)
        self.lbl_script = ttk.Label(self.lfm_run, text='Script:')
        self.lbl_script.grid(     row=0, column=0, sticky='E')
        self.cbx_script = ttk.Combobox(self.lfm_run, state='readonly', width=14)
        self.cbx_script.grid(     row=0, column=1, sticky='W')
        self.lbl_times = ttk.Label(self.lfm_run, text='Times:')
        self.lbl_times.grid(      row=1, column=0, sticky='E')
        self.sbx_times = ttk.Spinbox(self.lfm_run, from_=-1, to=99, format='%.0f', width=3)
        self.sbx_times.grid(      row=1, column=1, sticky='W')
        self.sbx_times.set(-1)
        self.btn_start_timer = ttk.Button(self.lfm_run, text='Start TimerWorker', command=self.btn_start_timer_click)
        self.btn_start_timer.grid(row=0, column=5, rowspan=2)
        self.btn_start_timer.disable()
        self.btn_start_timer.bind('<Key-Return>', lambda *_: self.btn_start_timer_click())
        self.btn_stop = ttk.Button(self.lfm_run, text='Stop', command=self.btn_stop_click)
        self.btn_stop.grid(       row=0, column=6, rowspan=2)
        self.btn_stop.bind('<Key-Return>', lambda *_: self.btn_stop_click())

        self.center_root()

    def btn_connect_click(self, *args, **kwargs):
        self.serial = USBSerial(self.tbx_port_content.get(), 9600)
        self.update_connection_led()
        if self.connection_active:
            self.serial_out(self.build_config_str())
            self.btn_connect.disable()
            self.sbx_a1_port.disable()
            self.sbx_a2_port.disable()
            self.sbx_a3_port.disable()
            self.btn_start_timer.enable()
    def btn_disconnect_click(self, *args, **kwargs):
        self.btn_stop_click()
        if self.serial:
            self.serial.close()
        self.serial = None
        self.update_connection_led()
        self.btn_connect.enable()
        self.sbx_a1_port.enable()
        self.sbx_a2_port.enable()
        self.sbx_a3_port.enable()
        self.btn_start_timer.disable()
    def update_connection_led(self):
        if self.connection_active:
            self.lbl_connected.configure(background='green1', text='Connected')
        else:
            self.lbl_connected.configure(background='red', text='Not Connected')
    @property
    def connection_active(self):
        return getattr(self.serial, 'connection', None)
    def serial_out(self, message):
        print('Control: Sending ' + message)
        self.serial.write(message)

    def sbx_change(self, config_key):
        # BUG!!!!! config values not updated when typed manually
        # Temporary FIX: Return is now bound here.
        props = self.config_keys[config_key]
        new_val = props['entry'].get()
        self.config[config_key] = new_val
        if props['type'] == 'external':
            if self.connection_active:
                pc = props['peek_command']
                command = self.build_config_str(config_key)
                if pc: # Optional command to send to serial with the new value
                    command += f'{pc}:{new_val};'
                self.serial_out(command)

    def btn_save_config_click(self, *args, **kwargs):
        config.save(self.config)

    def btn_start_timer_click(self, *args, **kwargs):
        sc = self.scripts[self.cbx_script.current()]
        self.start_timer_worker(self.serial, script=sc, log=print)
        self.btn_start_timer.disable()
    def btn_stop_click(self, *args, **kwargs):
        self.end_worker()
        self.btn_start_timer.enable()

    def lbx_console_write(self, *items):
        for item in items:
            if not item.strip():
                return # if item is whitespace, don't print it
            self.lbx_console.insert(tk.END, item)
            self.lbx_console.yview(tk.END) # scroll to bottom

    def parse_config(self):
        assert isinstance(self.config, dict)
        default = {ck:props['default'] for ck, props in self.config_keys.items()}
        for k, v in default.items():
            if not self.config.get(k):
                self.config[k] = v
        for k, entry in ((ck, props['entry']) for ck, props in self.config_keys.items()):
            entry.set(self.config[k])
    
    def build_config_str(self, params='all'):
        """
        params = 'all' => all values in names
        params = 'A1Rest,A3Tap' => 'CONF:A1R=xxx,A3T=xxx,;'
        """
        names = {ck:props['short_name'] for ck, props in self.config_keys.items() if props['type'] == 'external'}
        conf_str = 'CONF:'
        if params == 'all':
            for fn, sn in names.items():
                conf_str += f'{sn}={self.config[fn]},'
        else:
            for fn in params.split(','):
                sn = names[fn]
                conf_str += f'{sn}={self.config[fn]},'
        conf_str += ';'
        return conf_str

    def center_root(self):
        w, h = self.master.winfo_width(), self.master.winfo_height()
        if w <= 500 and h <= 500:
            # delay the centering until the window is big
            self.after(10, self.center_root)
            return
        sw, sh = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        x, y = (sw - w) // 2, (sh - h) // 2 - 20
        self.master.geometry(f'{w}x{h}+{x}+{y}')

    def start_timer_worker(self, *args, **kwargs):
        self.worker = TimerWorker(*args, **kwargs)
        self.worker.start_loop(tk_root=self, delay=self.config['Timing'], times=int(self.sbx_times.get()))

    def end_worker(self):
        if self.worker:
            self.worker.cancel_loop()
            self.worker = None

    def exit(self):
        self.end_worker()
        self.btn_disconnect_click()
        self.master.quit()


class Writer:
    """Wraps a function to act like a .write()-able object"""
    def __init__(self, writer):
        self.writer = writer
    def write(self, line):
        self.writer(line)

# def inspect_widget(widget): # tkinter debug purposes
#     for i in widget.keys():
#         print(i, ':', widget.cget(i))
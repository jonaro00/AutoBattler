import serial # pip install pyserial

class USBSerial:
    def __init__(self, portname, baudrate):
        self.portname = portname
        self.baudrate = baudrate
        self.open()

    def open(self):
        try:
            self.connection = serial.Serial(self.portname, self.baudrate, timeout=0.1, write_timeout=1)
            print('Connected to', self.portname)
            self.wait4ready()
        except:
            print('Connention to', self.portname, 'failed')
            self.connection = None
    
    def close(self):
        if self.connection:
            self.connection.close()
            print('Closed', self.portname)
        self.connection = None

    def wait4ready(self):
        print('Waiting for Ready:', end='')
        while not self.read():
            print('.', end='')
        print('Ready!')
        return True

    def read(self, byts=100):
        if self.connection:
            return self.connection.read(byts)
        return b''

    def write(self, message):
        if self.connection:
            return self.connection.write(str(message).encode())
        return 0

class Worker:
    def __init__(self, serialhandler, log=None):
        assert getattr(serialhandler, 'write')
        self.serial = serialhandler
        self.log = log or (lambda *_: None)

        self.log('Created Worker')

class TimerWorker(Worker):
    def __init__(self, serialhandler, log=None, script=None):
        super().__init__(serialhandler, log)
        self.script = script
        self.sequence = self.script['sequence'].split('\n')
        self.onend = self.script['onend']
        self.queue = []
        self.loop_count = 0
        self.tk_root = None
        self.delay = None
        self.cancel_id = None

    def serial_out(self, message):
        self.log(f'Worker: Sending {message}')
        self.serial.write(message)

    def start_loop(self, tk_root, delay, times):
        assert times >= -1
        self.tk_root = tk_root
        self.delay = delay

        self.log('Worker: Starting loop')
        self.loop_count = 0
        self.loop(times)

    def loop(self, times=-1):
        if not self.queue:
            if self.sequence:
                if times != 0:
                    self.queue = self.sequence.copy()
                    self.log('Worker: Queue refilled')
                    if times > 0:
                        self.log(f'Worker: {times} loops remaining')
                        times -= 1
                else:
                    self.cancel_loop()
                    return

        if self.queue:
            instruction = self.queue.pop(0)
            self.serial_out(instruction)
            if len(self.queue) == 0:
                self.log('Worker: Queue exhausted')
                self.loop_count += 1
                self.log(f'Worker: {self.loop_count} loops completed')

        self.cancel_id = self.tk_root.after(self.delay, self.loop, times)

    def cancel_loop(self):
        self.tk_root.after_cancel(self.cancel_id)
        self.serial_out(self.onend)
        print('Worker: Ended loop')

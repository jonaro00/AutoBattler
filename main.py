import tkinter as tk
from contextlib import redirect_stdout

from window import Window, Writer
from arduino import USBSerial, Worker


if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(300, 300)
    root.title('Auto Battler Console')
    # root.iconbitmap('favicon.ico')

    main_window = Window(root)
    root.bind('<Escape>', lambda _: main_window.exit())

    with redirect_stdout(Writer(main_window.lbx_console_write)):
        root.mainloop()

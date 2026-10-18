"""Cookie AutoClicker - app local para Windows (sin telemetría ni red)."""
import ctypes
from ctypes import wintypes
import queue
import threading
import time
import tkinter as tk
from tkinter import font as tkfont, messagebox

if not hasattr(ctypes, 'windll'):
    raise SystemExit('Esta aplicación solo funciona en Windows.')

user32 = ctypes.windll.user32
VK_F6 = 0x75
VK_ESCAPE = 0x1B
user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
user32.GetAsyncKeyState.restype = ctypes.c_short
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

class POINT(ctypes.Structure):
    _fields_ = [('x', wintypes.LONG), ('y', wintypes.LONG)]

class AutoClicker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Cookie AutoClicker')
        self.geometry('440x475')
        self.minsize(420, 455)
        self.configure(bg='#111827')
        self.active = threading.Event()
        self.closed = threading.Event()
        self.messages = queue.SimpleQueue()
        self.total = 0
        self.target = None
        self.cps = 10
        self.fixed = tk.BooleanVar(value=False)
        self.fixed_enabled = False
        self.cps_var = tk.IntVar(value=10)
        self.status_var = tk.StringVar(value='DETENIDO')
        self.count_var = tk.StringVar(value='0')
        self.position_var = tk.StringVar(value='Sin posición seleccionada')
        self.f6_down = bool(user32.GetAsyncKeyState(VK_F6) & 0x8000)
        self._make_ui()
        self.worker = threading.Thread(target=self._click_loop, daemon=True)
        self.worker.start()
        self.after(30, self._poll)
        self.protocol('WM_DELETE_WINDOW', self._close)

    def _make_ui(self):
        bg, surface, fg, muted, accent = '#111827', '#1f2937', '#f9fafb', '#9ca3af', '#34d399'
        self.ui_font = tkfont.Font(root=self, family='Arial', size=10)
        self.option_add('*Font', self.ui_font.name)
        self.columnconfigure(0, weight=1)
        tk.Label(self, text='COOKIE AUTOCLICKER', font=('Arial', 18, 'bold'),
                 fg=fg, bg=bg).pack(pady=(20, 3))
        tk.Label(self, text='Simple, local y gratuito · Windows', fg=muted, bg=bg).pack()

        panel = tk.Frame(self, bg=surface, padx=20, pady=16)
        panel.pack(fill='x', padx=22, pady=(18, 10))
        tk.Label(panel, text='CLICS POR SEGUNDO', fg=muted, bg=surface,
                 font=('Arial', 9, 'bold')).pack(anchor='w')
        self.speed_label = tk.Label(panel, text='10 CPS', fg=accent, bg=surface,
                                    font=('Arial', 23, 'bold'))
        self.speed_label.pack(anchor='w')
        slider = tk.Scale(panel, from_=1, to=50, orient='horizontal', variable=self.cps_var,
                          command=self._change_speed, bg=surface, fg=fg,
                          activebackground=accent, troughcolor='#374151',
                          highlightthickness=0, showvalue=False, length=340)
        slider.pack(fill='x')
        tk.Label(panel, text='1 CPS                                      50 CPS',
                 fg=muted, bg=surface, font=('Arial', 8)).pack(fill='x')

        pos = tk.Frame(self, bg=surface, padx=20, pady=13)
        pos.pack(fill='x', padx=22, pady=(0, 10))
        tk.Checkbutton(pos, text='Hacer clic en una posición fija', variable=self.fixed,
                       command=self._change_fixed, fg=fg, bg=surface, selectcolor=bg,
                       activeforeground=fg, activebackground=surface,
                       highlightthickness=0).pack(anchor='w')
        tk.Label(pos, textvariable=self.position_var, fg=muted, bg=surface).pack(anchor='w', pady=(4, 8))
        self.select_btn = tk.Button(pos, text='Elegir posición (3 segundos)',
                                    command=self._capture_position, fg=fg, bg='#374151',
                                    activebackground='#4b5563', activeforeground=fg,
                                    bd=0, padx=12, pady=8)
        self.select_btn.pack(fill='x')

        stats = tk.Frame(self, bg=bg)
        stats.pack(fill='x', padx=25, pady=(0, 6))
        tk.Label(stats, text='Estado:', bg=bg, fg=muted).pack(side='left')
        self.status_label = tk.Label(stats, textvariable=self.status_var,
                                     bg=bg, fg='#fbbf24', font=('Arial', 10, 'bold'))
        self.status_label.pack(side='left', padx=(7, 0))
        tk.Label(stats, text='Clics:', bg=bg, fg=muted).pack(side='left', padx=(22, 5))
        tk.Label(stats, textvariable=self.count_var, bg=bg, fg=fg,
                 font=('Arial', 10, 'bold')).pack(side='left')
        tk.Button(stats, text='Reiniciar', command=self._reset_count, bd=0,
                  bg=bg, fg=accent, activebackground=bg, activeforeground=fg).pack(side='right')

        self.toggle_btn = tk.Button(self, text='INICIAR  ·  F6', command=self._toggle,
                                    bg=accent, fg='#052e21', activebackground='#6ee7b7',
                                    font=('Arial', 13, 'bold'), bd=0, pady=13)
        self.toggle_btn.pack(fill='x', padx=22, pady=(9, 6))
        hotkey_msg = 'F6: iniciar / detener · Esc: parada de emergencia (en algunos teclados: Fn + F6)'
        tk.Label(self, text=hotkey_msg, bg=bg, fg=muted, wraplength=390,
                 font=('Arial', 9)).pack(pady=(3, 0))

    def _change_speed(self, value):
        self.cps = int(float(value))
        self.speed_label.configure(text=f'{self.cps} CPS')

    def _change_fixed(self):
        if self.fixed.get() and self.target is None:
            self.fixed.set(False)
            messagebox.showinfo('Falta posición', 'Pulsa «Elegir posición» y coloca el cursor sobre el objetivo durante la cuenta regresiva.')
        self.fixed_enabled = self.fixed.get()

    def _capture_position(self):
        self.select_btn.configure(state='disabled')
        self._countdown(3)

    def _countdown(self, seconds):
        if seconds:
            self.position_var.set(f'Coloca el cursor en el objetivo... {seconds}')
            self.after(1000, lambda: self._countdown(seconds - 1))
        else:
            point = POINT()
            if user32.GetCursorPos(ctypes.byref(point)):
                self.target = (point.x, point.y)
                self.fixed.set(True)
                self.fixed_enabled = True
                self.position_var.set(f'Posición fija: X={point.x}, Y={point.y}')
            else:
                self.position_var.set('No se pudo obtener la posición')
            self.select_btn.configure(state='normal')

    def _toggle(self):
        if self.active.is_set():
            self._stop()
        else:
            if self.fixed.get() and self.target is None:
                messagebox.showwarning('Posición', 'Primero selecciona una posición fija.')
                return
            self.active.set()
            self.status_var.set('ACTIVO')
            self.status_label.configure(fg='#34d399')
            self.toggle_btn.configure(text='DETENER  ·  F6', bg='#fb7185')

    def _stop(self):
        self.active.clear()
        self.status_var.set('DETENIDO')
        self.status_label.configure(fg='#fbbf24')
        self.toggle_btn.configure(text='INICIAR  ·  F6', bg='#34d399')

    def _reset_count(self):
        self.messages.put(('reset', None))

    def _click_loop(self):
        next_click = time.perf_counter()
        while not self.closed.is_set():
            self._check_keys()
            if not self.active.is_set():
                next_click = time.perf_counter()
                self.closed.wait(0.015)
                continue
            if self.fixed_enabled and self.target is not None:
                x, y = self.target
                user32.SetCursorPos(x, y)
            user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            self.messages.put(('click', None))
            interval = 1.0 / max(1, self.cps)
            next_click = max(next_click + interval, time.perf_counter())
            # Check emergency keys frequently even at 1 click per second.
            while not self.closed.is_set() and self.active.is_set():
                remaining = next_click - time.perf_counter()
                if remaining <= 0:
                    break
                self.closed.wait(min(0.01, remaining))
                self._check_keys()

    def _check_keys(self):
        f6_down = bool(user32.GetAsyncKeyState(VK_F6) & 0x8000)
        if user32.GetAsyncKeyState(VK_ESCAPE) & 0x8000:
            # Stop in the worker without waiting for Tkinter to process events.
            if self.active.is_set():
                self.active.clear()
                self.messages.put(('stop', None))
        elif f6_down and not self.f6_down:
            if self.active.is_set():
                self.active.clear()
                self.messages.put(('stop', None))
            else:
                self.messages.put(('toggle', None))
        self.f6_down = f6_down

    def _poll(self):
        change = False
        while True:
            try:
                action, _ = self.messages.get_nowait()
            except queue.Empty:
                break
            if action == 'reset':
                self.total = 0
            elif action == 'click':
                self.total += 1
            elif action == 'stop':
                self._stop()
            elif action == 'toggle':
                if not user32.GetAsyncKeyState(VK_ESCAPE) & 0x8000:
                    self._toggle()
            change = True
        if change:
            self.count_var.set(f'{self.total:,}')
        if not self.closed.is_set():
            self.after(30, self._poll)

    def _close(self):
        self.active.clear()
        self.closed.set()
        self.destroy()

if __name__ == '__main__':
    AutoClicker().mainloop()

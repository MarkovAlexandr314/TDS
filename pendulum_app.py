import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint
import tkinter as tk
from tkinter import ttk

class DoublePendulumApp:
    def __init__(self, master):
        self.master = master
        master.title("Double Pendulum Simulator")
        
        # Инициализация двух маятников
        self.pendulum1 = DoublePendulum(color='blue')
        self.pendulum2 = DoublePendulum(color='green')
        
        self.traj1_x, self.traj1_y = [], []
        self.traj2_x, self.traj2_y = [], []
        self.anim = None
        
        self.create_widgets()
        self.setup_plot()
        
    def create_widgets(self):
        control_frame = ttk.Frame(self.master, padding=10)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Панель управления для первого маятника
        frame1 = ttk.LabelFrame(control_frame, text="Маятник 1", padding=10)
        frame1.pack(fill=tk.X, pady=5)
        self.L1_slider, self.L1_label = self.create_slider(
            frame1, 'L1 (m):', 0.1, 3.0, 1.0, "{:.1f}")
        self.L2_slider, self.L2_label = self.create_slider(
            frame1, 'L2 (m):', 0.1, 3.0, 1.0, "{:.1f}")
        self.theta1_slider, self.theta1_label = self.create_slider(
            frame1, 'θ1 (deg):', 0, 180, 90, "{:.0f}")
        self.theta2_slider, self.theta2_label = self.create_slider(
            frame1, 'θ2 (deg):', 0, 180, 90, "{:.0f}")
        
        # Панель управления для второго маятника
        frame2 = ttk.LabelFrame(control_frame, text="Маятник 2", padding=10)
        frame2.pack(fill=tk.X, pady=5)
        self.L1_slider2, self.L1_label2 = self.create_slider(
            frame2, 'L1 (m):', 0.1, 3.0, 1.0, "{:.1f}")
        self.L2_slider2, self.L2_label2 = self.create_slider(
            frame2, 'L2 (m):', 0.1, 3.0, 1.0, "{:.1f}")
        self.theta1_slider2, self.theta1_label2 = self.create_slider(
            frame2, 'θ1 (deg):', 0, 180, 90, "{:.0f}")
        self.theta2_slider2, self.theta2_label2 = self.create_slider(
            frame2, 'θ2 (deg):', 0, 180, 90, "{:.0f}")
        
        # Кнопка запуска
        self.start_button = ttk.Button(control_frame, text="Запуск", command=self.start_animation)
        self.start_button.pack(pady=10)
    
    def create_slider(self, parent, label, min_val, max_val, init_val, format_str):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(frame, text=label).pack(side=tk.LEFT)
        value_label = ttk.Label(frame, text=format_str.format(init_val))
        value_label.pack(side=tk.RIGHT)
        
        slider = ttk.Scale(
            frame,
            from_=min_val,
            to=max_val,
            value=init_val,
            orient=tk.HORIZONTAL,
            command=lambda v, lbl=value_label, fmt=format_str: lbl.config(text=fmt.format(float(v)))
        )
        slider.pack(fill=tk.X, expand=True)
        
        return slider, value_label
    
    def setup_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.ax.set_xlim(-6, 6)
        self.ax.set_ylim(-6, 6)
        self.ax.grid()
        
        # Элементы для первого маятника
        self.pendulum_line1, = self.ax.plot([], [], 'o-', lw=2, color='blue')
        self.trajectory1, = self.ax.plot([], [], '-', lw=1, color='blue', alpha=0.3)
        
        # Элементы для второго маятника
        self.pendulum_line2, = self.ax.plot([], [], 'o-', lw=2, color='green')
        self.trajectory2, = self.ax.plot([], [], '-', lw=1, color='green', alpha=0.3)
        
        self.time_text = self.ax.text(0.02, 0.95, '', transform=self.ax.transAxes)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def start_animation(self):
        if self.anim is not None:
            self.anim.event_source.stop()
        
        # Обновление параметров для первого маятника
        self.update_pendulum_params(self.pendulum1, 
                                  self.L1_label['text'],
                                  self.L2_label['text'],
                                  self.theta1_label['text'],
                                  self.theta2_label['text'])
        
        # Обновление параметров для второго маятника
        self.update_pendulum_params(self.pendulum2,
                                  self.L1_label2['text'],
                                  self.L2_label2['text'],
                                  self.theta1_label2['text'],
                                  self.theta2_label2['text'])
        
        # Сброс траекторий
        self.traj1_x, self.traj1_y = [], []
        self.traj2_x, self.traj2_y = [], []
        
        # Запуск анимации
        self.anim = FuncAnimation(
            self.fig,
            self.update,
            frames=1500,
            init_func=self.init_animation,
            blit=True,
            interval=20,
            repeat=False
        )
        self.canvas.draw()
    
    def update_pendulum_params(self, pendulum, L1, L2, theta1, theta2):
        pendulum.L1 = float(L1)
        pendulum.L2 = float(L2)
        pendulum.state = [
            np.deg2rad(float(theta1)),
            0,
            np.deg2rad(float(theta2)),
            0
        ]
    
    def init_animation(self):
        self.pendulum_line1.set_data([], [])
        self.trajectory1.set_data([], [])
        self.pendulum_line2.set_data([], [])
        self.trajectory2.set_data([], [])
        self.time_text.set_text('')
        return (self.pendulum_line1, self.trajectory1,
                self.pendulum_line2, self.trajectory2,
                self.time_text)
    
    def update(self, frame):
        # Обновление первого маятника
        self.update_pendulum(self.pendulum1, self.traj1_x, self.traj1_y, 'blue')
        # Обновление второго маятника
        self.update_pendulum(self.pendulum2, self.traj2_x, self.traj2_y, 'green')
        
        self.time_text.set_text(f'Время: {frame * self.pendulum1.dt:.2f} с')
        return (self.pendulum_line1, self.trajectory1,
                self.pendulum_line2, self.trajectory2,
                self.time_text)
    
    def update_pendulum(self, pendulum, traj_x, traj_y, color):
        t = np.linspace(0, pendulum.dt, 2)
        sol = odeint(pendulum.equations, pendulum.state, t)
        pendulum.state = sol[-1]
        
        x1 = pendulum.L1 * np.sin(pendulum.state[0])
        y1 = -pendulum.L1 * np.cos(pendulum.state[0])
        x2 = x1 + pendulum.L2 * np.sin(pendulum.state[2])
        y2 = y1 - pendulum.L2 * np.cos(pendulum.state[2])
        
        traj_x.append(x2)
        traj_y.append(y2)
        if len(traj_x) > 500:
            traj_x.pop(0)
            traj_y.pop(0)
        
        if color == 'blue':
            self.pendulum_line1.set_data([0, x1, x2], [0, y1, y2])
            self.trajectory1.set_data(traj_x, traj_y)
        else:
            self.pendulum_line2.set_data([0, x1, x2], [0, y1, y2])
            self.trajectory2.set_data(traj_x, traj_y)

class DoublePendulum:
    def __init__(self, color='blue'):
        self.L1 = 1.0
        self.L2 = 1.0
        self.m1 = 2.0
        self.m2 = 1.0
        self.g = 9.81
        self.dt = 0.02
        self.state = np.array([np.pi/2, 0, np.pi/2, 0])
        self.color = color
        
    def equations(self, y, t):
        theta1, omega1, theta2, omega2 = y
        delta = theta2 - theta1
        
        denom = (self.m1 + self.m2 - self.m2*np.cos(delta)**2)
        domega1 = ((self.m2 * self.L1 * omega1**2 * np.sin(delta) * np.cos(delta)
                   + self.m2 * self.g * np.sin(theta2) * np.cos(delta) + 
                   self.m2 * self.L2 * omega2**2 * np.sin(delta) - (self.m1 + self.m2)*self.g*np.sin(theta1))
                    / (self.L1 * denom))
        domega2 = ((-self.m2 * self.L2 * omega2**2 * np.sin(delta) * np.cos(delta)
                   + (self.m2 + self.m2)*(self.g * np.sin(theta1) * np.cos(delta)
                    - self.L1 * omega1**2 * np.sin(delta) - self.g*np.sin(theta2)))
                    / (self.L2 * denom))

        return [omega1, domega1, omega2, domega2]

if __name__ == "__main__":
    root = tk.Tk()
    app = DoublePendulumApp(root)
    root.mainloop()
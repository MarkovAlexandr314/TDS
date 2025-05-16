import tkinter as tk
from tkinter import ttk
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D

class HopfBifurcationApp:
    def __init__(self, master):
        self.master = master
        master.title("Бифуркация Андронова-Хопфа")

        # Параметры системы
        self.mu = 0.0
        self.omega = 1.0
        self.lambda_z = 1.0

        # Настройка GUI
        self.setup_gui()

    def setup_gui(self):
        # Создание графика Matplotlib
        self.fig = plt.figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Слайдер для параметра mu
        self.slider = ttk.Scale(
            self.master,
            from_=-1.0,
            to=1.0,
            orient=tk.HORIZONTAL,
            command=self.update
        )
        self.slider.pack(side=tk.BOTTOM, fill=tk.X)
        self.slider.set(0.0)

        # Метка для значения mu
        self.label = ttk.Label(self.master, text="μ = 0.00")
        self.label.pack(side=tk.BOTTOM)

    def hopf_system(self, t, state):
        x, y, z = state
        r_squared = x**2 + y**2
        dxdt = (self.mu - r_squared)*x - self.omega*y
        dydt = self.omega*x + (self.mu - r_squared)*y
        dzdt = -self.lambda_z*z
        return [dxdt, dydt, dzdt]

    def update(self, event=None):
        self.mu = float(self.slider.get())
        self.label.config(text=f"μ = {self.mu:.2f}")
        self.ax.clear()

        # Начальные условия
        initial_conditions = [
            [0.5, 0.0, 0.5],
            [1.0, 0.0, 1.0],
            [0.0, 0.5, 0.0],
            [0.0, 1.0, 1.0]
        ]

        # Интеграция траекторий
        for ic in initial_conditions:
            sol = solve_ivp(
                self.hopf_system,
                [0, 20],
                ic,
                t_eval=np.linspace(0, 20, 1000)
            )
            self.ax.plot(
                sol.y[0], 
                sol.y[1], 
                sol.y[2], 
                lw=0.8,
                alpha=0.7
            )

        # Настройка графика
        self.ax.set_xlim(-1.5, 1.5)
        self.ax.set_ylim(-1.5, 1.5)
        self.ax.set_zlim(0, 1.5)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title(f"Бифуркация Андронова-Хопфа (μ = {self.mu:.2f})")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = HopfBifurcationApp(root)
    root.mainloop()
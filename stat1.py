import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


# Calculate functions
def calculate_functions(values):
    continuous_outputs = [
        1.94 * values["mu_o"] ** -0.07 - 0.995,
        -0.13 * values["k"] ** 0.24 + 1.16,
        -0.36 * values["TDS"] ** 0.13 + 1.72,
        -27.32 * values["T"] ** 0.02 + 29.87
    ]
    discrete_outputs = [
        0.1 if values["CC"] == "yes" else 0.9,
        0.21 if values["DP"] == "yes" else 0.79,
        0.14 if values["GC"] == "yes" else 0.86,
        0.24 if values["Aq"] == "yes" else 0.76
    ]
    return continuous_outputs, discrete_outputs


# Calculate EFF
def calculate_eff(continuous_outputs, discrete_outputs):
    continuous_weights = [0.1742, 0.1894, 0.1313, 0.1187]
    discrete_weights = [0.1035, 0.1540, 0.0556, 0.073]
    total_weights = continuous_weights + discrete_weights

    eff1 = sum([f * w for f, w in zip(continuous_outputs, continuous_weights)]) * 100
    eff2 = sum([f * w for f, w in zip(discrete_outputs, discrete_weights)]) * 100
    eff = sum([f * w for f, w in zip(continuous_outputs + discrete_outputs, total_weights)]) * 100

    return eff1, eff2, eff


# Plotting function
def plot(continuous_values, continuous_outputs, input_values):
    x_ranges = [
        np.linspace(0.1, 100, 100),  # Viscosity
        np.linspace(0.1, 500, 100),  # Permeability
        np.linspace(0, 10000, 100),  # TDS
        np.linspace(0, 100, 100)  # Temperature (Adjusted range)
    ]
    labels = ["Viscosity", "Permeability", "TDS", "Temperature"]
    functions = [
        lambda x: 1.94 * x ** -0.07 - 0.995,
        lambda x: -0.13 * x ** 0.24 + 1.16,
        lambda x: -0.36 * x ** 0.13 + 1.72,
        lambda x: -27.32 * x ** 0.02 + 29.87
    ]
    fig, axs = plt.subplots(1, 4, figsize=(12, 3))
    for i, ax in enumerate(axs):
        func_value = functions[i](input_values[i])
        ax.plot(x_ranges[i], functions[i](x_ranges[i]), label=f"f(x) = {func_value:.2f}")
        ax.scatter(continuous_values[i], continuous_outputs[i], color='red')
        ax.set_title(labels[i])
        ax.legend()
        ax.grid(True)
    plt.tight_layout()
    return fig


# Main program logic
def on_calculate():
    # Extract values
    values = {
        "mu_o": float(mu_o_entry.get()),
        "k": float(k_entry.get()),
        "TDS": float(tds_entry.get()),
        "T": float(t_entry.get()),
        "CC": cc_value.get(),
        "DP": dp_value.get(),
        "GC": gc_value.get(),
        "Aq": aq_value.get()
    }

    continuous_outputs, discrete_outputs = calculate_functions(values)
    eff1_value, eff2_value, eff_value = calculate_eff(continuous_outputs, discrete_outputs)

    eff1_value, eff2_value, eff_value = calculate_eff(continuous_outputs, discrete_outputs)

    eff1_label.config(text=f"EFF1 Value: {eff1_value:.2f}%")
    eff2_label.config(text=f"EFF2 Value: {eff2_value:.2f}%")
    eff_label.config(text=f"EFF Value: {eff_value:.2f}%")

    fig_new = plot(
        [values["mu_o"], values["k"], values["TDS"], values["T"]],
        continuous_outputs,
        [values["mu_o"], values["k"], values["TDS"], values["T"]]
    )

    # Clear the previous canvas
    for widget in output_frame.winfo_children():
        widget.destroy()

    canvas_new = FigureCanvasTkAgg(fig_new, master=output_frame)
    canvas_widget_new = canvas_new.get_tk_widget()
    canvas_widget_new.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

    # Add the navigation toolbar (zoom buttons and scroll)
    toolbar_frame = ttk.Frame(output_frame)
    toolbar_frame.grid(row=1, column=0, sticky=tk.W + tk.E)
    toolbar_new = NavigationToolbar2Tk(canvas_new, toolbar_frame)

    canvas_new.draw()


# GUI setup
window = tk.Tk()
window.title("Novel Integrated Methodology")

# Continuous inputs
ttk.Label(window, text="Oil viscosity (μo) in cP:").grid(column=0, row=0)
mu_o_entry = ttk.Entry(window)
mu_o_entry.grid(column=1, row=0)

ttk.Label(window, text="Reservoir permeability (k) in mD:").grid(column=0, row=1)
k_entry = ttk.Entry(window)
k_entry.grid(column=1, row=1)

ttk.Label(window, text="Total dissolved solids (TDS) in ppm:").grid(column=0, row=2)
tds_entry = ttk.Entry(window)
tds_entry.grid(column=1, row=2)

ttk.Label(window, text="Reservoir temperature (T) in °C:").grid(column=0, row=3)
t_entry = ttk.Entry(window)
t_entry.grid(column=1, row=3)

# Discrete inputs
ttk.Label(window, text="Clay content:").grid(column=0, row=4)
cc_value = tk.StringVar(value="no")
ttk.Radiobutton(window, text="Yes", variable=cc_value, value="yes").grid(column=1, row=4, sticky=tk.W)
ttk.Radiobutton(window, text="No", variable=cc_value, value="no").grid(column=1, row=4, sticky=tk.E)

ttk.Label(window, text="Reservoir heterogeneity:").grid(column=0, row=5)
dp_value = tk.StringVar(value="no")
ttk.Radiobutton(window, text="Yes", variable=dp_value, value="yes").grid(column=1, row=5, sticky=tk.W)
ttk.Radiobutton(window, text="No", variable=dp_value, value="no").grid(column=1, row=5, sticky=tk.E)

ttk.Label(window, text="Presence of gas cap:").grid(column=0, row=6)
gc_value = tk.StringVar(value="no")
ttk.Radiobutton(window, text="Yes", variable=gc_value, value="yes").grid(column=1, row=6, sticky=tk.W)
ttk.Radiobutton(window, text="No", variable=gc_value, value="no").grid(column=1, row=6, sticky=tk.E)

ttk.Label(window, text="Presence of aquifer:").grid(column=0, row=7)
aq_value = tk.StringVar(value="no")
ttk.Radiobutton(window, text="Yes", variable=aq_value, value="yes").grid(column=1, row=7, sticky=tk.W)
ttk.Radiobutton(window, text="No", variable=aq_value, value="no").grid(column=1, row=7, sticky=tk.E)

# EFF1, EFF2 and EFF output
# EFF1, EFF2 and EFF output
eff1_label = ttk.Label(window, text="EFF1 (Continuous) Value:")
eff1_label.grid(column=0, row=13, columnspan=2)

eff2_label = ttk.Label(window, text="EFF2 (Discrete) Value:")
eff2_label.grid(column=0, row=14, columnspan=2)

eff_label = ttk.Label(window, text="EFF Value: ", font=('Helvetica', 12, 'bold'))
eff_label.grid(column=0, row=15, columnspan=2)

# Create a frame to hold the plot and toolbar
output_frame = ttk.Frame(window)
output_frame.grid(column=0, row=11, columnspan=2)

# Calculate button
calculate_button = ttk.Button(window, text="Calculate", command=on_calculate)
calculate_button.grid(column=0, row=12, columnspan=2)

# Run the main application loop
window.mainloop()

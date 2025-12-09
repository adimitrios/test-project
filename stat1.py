"""
Professional Reservoir Analysis Tool
======================================
A comprehensive application for analyzing reservoir parameters and calculating
efficiency metrics using integrated mathematical models.

Author: Reservoir Engineering Team
Version: 2.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Tuple, Callable
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


# ============================================================================
# CONSTANTS AND CONFIGURATION
# ============================================================================

@dataclass
class ModelCoefficients:
    """Mathematical model coefficients for reservoir analysis."""

    # Continuous parameter coefficients [a, b, c] for f(x) = a * x^b + c
    VISCOSITY_COEF: Tuple[float, float, float] = (1.94, -0.07, -0.995)
    PERMEABILITY_COEF: Tuple[float, float, float] = (-0.13, 0.24, 1.16)
    TDS_COEF: Tuple[float, float, float] = (-0.36, 0.13, 1.72)
    TEMPERATURE_COEF: Tuple[float, float, float] = (-27.32, 0.02, 29.87)

    # Discrete parameter values [yes_value, no_value]
    CLAY_CONTENT_VALS: Tuple[float, float] = (0.1, 0.9)
    HETEROGENEITY_VALS: Tuple[float, float] = (0.21, 0.79)
    GAS_CAP_VALS: Tuple[float, float] = (0.14, 0.86)
    AQUIFER_VALS: Tuple[float, float] = (0.24, 0.76)

    # Weighting factors
    CONTINUOUS_WEIGHTS: Tuple[float, ...] = (0.1742, 0.1894, 0.1313, 0.1187)
    DISCRETE_WEIGHTS: Tuple[float, ...] = (0.1035, 0.1540, 0.0556, 0.073)


@dataclass
class InputRanges:
    """Valid ranges for input parameters."""
    VISCOSITY: Tuple[float, float] = (0.1, 100.0)
    PERMEABILITY: Tuple[float, float] = (0.1, 500.0)
    TDS: Tuple[float, float] = (0.0, 10000.0)
    TEMPERATURE: Tuple[float, float] = (0.0, 100.0)


@dataclass
class PlotConfig:
    """Configuration for plot visualization."""
    FIGSIZE: Tuple[int, int] = (16, 4)
    DPI: int = 100
    MAIN_COLOR: str = '#2E86AB'
    POINT_COLOR: str = '#A23B72'
    GRID_ALPHA: float = 0.3
    LINE_WIDTH: float = 2.5
    POINT_SIZE: int = 100
    FONT_SIZE_TITLE: int = 11
    FONT_SIZE_LABEL: int = 10


# Global configuration instances
COEF = ModelCoefficients()
RANGES = InputRanges()
PLOT_CFG = PlotConfig()


# ============================================================================
# MATHEMATICAL MODEL
# ============================================================================

class ReservoirModel:
    """
    Mathematical model for reservoir efficiency calculations.

    This class implements the integrated methodology for evaluating
    reservoir parameters and computing efficiency metrics.
    """

    @staticmethod
    def viscosity_function(mu_o: float) -> float:
        """Calculate viscosity contribution: f₁(μₒ) = 1.94 × μₒ^(-0.07) - 0.995"""
        a, b, c = COEF.VISCOSITY_COEF
        return a * mu_o ** b + c

    @staticmethod
    def permeability_function(k: float) -> float:
        """Calculate permeability contribution: f₂(k) = -0.13 × k^(0.24) + 1.16"""
        a, b, c = COEF.PERMEABILITY_COEF
        return a * k ** b + c

    @staticmethod
    def tds_function(tds: float) -> float:
        """Calculate TDS contribution: f₃(TDS) = -0.36 × TDS^(0.13) + 1.72"""
        a, b, c = COEF.TDS_COEF
        return a * tds ** b + c

    @staticmethod
    def temperature_function(t: float) -> float:
        """Calculate temperature contribution: f₄(T) = -27.32 × T^(0.02) + 29.87"""
        a, b, c = COEF.TEMPERATURE_COEF
        return a * t ** b + c

    @classmethod
    def calculate_continuous_outputs(cls, mu_o: float, k: float,
                                     tds: float, t: float) -> List[float]:
        """
        Calculate all continuous parameter contributions.

        Args:
            mu_o: Oil viscosity (cP)
            k: Reservoir permeability (mD)
            tds: Total dissolved solids (ppm)
            t: Reservoir temperature (°C)

        Returns:
            List of continuous output values [f₁, f₂, f₃, f₄]
        """
        return [
            cls.viscosity_function(mu_o),
            cls.permeability_function(k),
            cls.tds_function(tds),
            cls.temperature_function(t)
        ]

    @staticmethod
    def calculate_discrete_outputs(clay: bool, heterogeneity: bool,
                                   gas_cap: bool, aquifer: bool) -> List[float]:
        """
        Calculate all discrete parameter contributions.

        Args:
            clay: Presence of clay content
            heterogeneity: Reservoir heterogeneity
            gas_cap: Presence of gas cap
            aquifer: Presence of aquifer

        Returns:
            List of discrete output values [d₁, d₂, d₃, d₄]
        """
        return [
            COEF.CLAY_CONTENT_VALS[0] if clay else COEF.CLAY_CONTENT_VALS[1],
            COEF.HETEROGENEITY_VALS[0] if heterogeneity else COEF.HETEROGENEITY_VALS[1],
            COEF.GAS_CAP_VALS[0] if gas_cap else COEF.GAS_CAP_VALS[1],
            COEF.AQUIFER_VALS[0] if aquifer else COEF.AQUIFER_VALS[1]
        ]

    @staticmethod
    def calculate_efficiency(continuous_outputs: List[float],
                           discrete_outputs: List[float]) -> Tuple[float, float, float]:
        """
        Calculate efficiency metrics (EFF1, EFF2, EFF).

        EFF1 = Σ(fᵢ × wᵢ) × 100  [Continuous parameters]
        EFF2 = Σ(dᵢ × wᵢ) × 100  [Discrete parameters]
        EFF  = Σ(all × wᵢ) × 100 [Combined]

        Args:
            continuous_outputs: List of continuous function outputs
            discrete_outputs: List of discrete function outputs

        Returns:
            Tuple of (EFF1, EFF2, EFF) as percentages
        """
        eff1 = sum(f * w for f, w in zip(continuous_outputs, COEF.CONTINUOUS_WEIGHTS)) * 100
        eff2 = sum(d * w for d, w in zip(discrete_outputs, COEF.DISCRETE_WEIGHTS)) * 100

        all_outputs = continuous_outputs + discrete_outputs
        all_weights = COEF.CONTINUOUS_WEIGHTS + COEF.DISCRETE_WEIGHTS
        eff = sum(val * w for val, w in zip(all_outputs, all_weights)) * 100

        return eff1, eff2, eff


# ============================================================================
# VISUALIZATION
# ============================================================================

class ReservoirVisualizer:
    """Handles all visualization and plotting functionality."""

    @staticmethod
    def create_plots(continuous_values: List[float],
                    continuous_outputs: List[float]) -> Figure:
        """
        Create professional visualization of continuous parameters.

        Args:
            continuous_values: Input parameter values [μₒ, k, TDS, T]
            continuous_outputs: Calculated function outputs [f₁, f₂, f₃, f₄]

        Returns:
            Matplotlib Figure object
        """
        # Configure matplotlib style
        plt.style.use('seaborn-v0_8-darkgrid')

        # Define parameter ranges and metadata
        params = [
            {
                'range': np.linspace(RANGES.VISCOSITY[0], RANGES.VISCOSITY[1], 200),
                'function': ReservoirModel.viscosity_function,
                'label': 'Oil Viscosity (μₒ)',
                'unit': 'cP',
                'equation': r'$f_1 = 1.94 \times \mu_o^{-0.07} - 0.995$'
            },
            {
                'range': np.linspace(RANGES.PERMEABILITY[0], RANGES.PERMEABILITY[1], 200),
                'function': ReservoirModel.permeability_function,
                'label': 'Permeability (k)',
                'unit': 'mD',
                'equation': r'$f_2 = -0.13 \times k^{0.24} + 1.16$'
            },
            {
                'range': np.linspace(RANGES.TDS[0], RANGES.TDS[1], 200),
                'function': ReservoirModel.tds_function,
                'label': 'Total Dissolved Solids',
                'unit': 'ppm',
                'equation': r'$f_3 = -0.36 \times TDS^{0.13} + 1.72$'
            },
            {
                'range': np.linspace(RANGES.TEMPERATURE[0], RANGES.TEMPERATURE[1], 200),
                'function': ReservoirModel.temperature_function,
                'label': 'Temperature (T)',
                'unit': '°C',
                'equation': r'$f_4 = -27.32 \times T^{0.02} + 29.87$'
            }
        ]

        # Create figure
        fig, axes = plt.subplots(1, 4, figsize=PLOT_CFG.FIGSIZE, dpi=PLOT_CFG.DPI)
        fig.suptitle('Continuous Parameter Response Functions',
                     fontsize=14, fontweight='bold', y=1.02)

        for i, (ax, param) in enumerate(zip(axes, params)):
            # Plot the function curve
            x_range = param['range']
            y_range = param['function'](x_range)

            ax.plot(x_range, y_range,
                   color=PLOT_CFG.MAIN_COLOR,
                   linewidth=PLOT_CFG.LINE_WIDTH,
                   label='Response Function',
                   zorder=2)

            # Plot the current point
            ax.scatter(continuous_values[i], continuous_outputs[i],
                      color=PLOT_CFG.POINT_COLOR,
                      s=PLOT_CFG.POINT_SIZE,
                      zorder=3,
                      edgecolors='white',
                      linewidths=2,
                      label=f'Current: {continuous_outputs[i]:.3f}')

            # Styling
            ax.set_title(f'{param["label"]}',
                        fontsize=PLOT_CFG.FONT_SIZE_TITLE,
                        fontweight='bold',
                        pad=10)
            ax.set_xlabel(f'{param["label"]} ({param["unit"]})',
                         fontsize=PLOT_CFG.FONT_SIZE_LABEL)
            ax.set_ylabel('Function Output',
                         fontsize=PLOT_CFG.FONT_SIZE_LABEL)

            # Add equation as text
            ax.text(0.05, 0.95, param['equation'],
                   transform=ax.transAxes,
                   fontsize=8,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

            # Grid and legend
            ax.grid(True, alpha=PLOT_CFG.GRID_ALPHA, linestyle='--', linewidth=0.5)
            ax.legend(loc='best', fontsize=8, framealpha=0.9)

            # Formatting
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        plt.tight_layout()
        return fig


# ============================================================================
# INPUT VALIDATION
# ============================================================================

class InputValidator:
    """Validates user inputs and provides error messages."""

    @staticmethod
    def validate_continuous_input(name: str, value: str,
                                  min_val: float, max_val: float) -> float:
        """
        Validate continuous parameter input.

        Args:
            name: Parameter name for error messages
            value: String value from entry widget
            min_val: Minimum allowed value
            max_val: Maximum allowed value

        Returns:
            Validated float value

        Raises:
            ValueError: If validation fails
        """
        try:
            float_val = float(value)
        except ValueError:
            raise ValueError(f"{name} must be a valid number.")

        if not (min_val <= float_val <= max_val):
            raise ValueError(
                f"{name} must be between {min_val} and {max_val}.\n"
                f"You entered: {float_val}"
            )

        return float_val

    @classmethod
    def validate_all_inputs(cls, entries: Dict[str, str]) -> Dict[str, float]:
        """
        Validate all continuous inputs.

        Args:
            entries: Dictionary of parameter names to string values

        Returns:
            Dictionary of validated float values

        Raises:
            ValueError: If any validation fails
        """
        return {
            'mu_o': cls.validate_continuous_input(
                'Oil viscosity', entries['mu_o'],
                RANGES.VISCOSITY[0], RANGES.VISCOSITY[1]
            ),
            'k': cls.validate_continuous_input(
                'Permeability', entries['k'],
                RANGES.PERMEABILITY[0], RANGES.PERMEABILITY[1]
            ),
            'tds': cls.validate_continuous_input(
                'TDS', entries['tds'],
                RANGES.TDS[0], RANGES.TDS[1]
            ),
            't': cls.validate_continuous_input(
                'Temperature', entries['t'],
                RANGES.TEMPERATURE[0], RANGES.TEMPERATURE[1]
            )
        }


# ============================================================================
# GUI APPLICATION
# ============================================================================

class ReservoirAnalysisApp:
    """Main application class for the Reservoir Analysis GUI."""

    def __init__(self, root: tk.Tk):
        """Initialize the application."""
        self.root = root
        self.root.title("Reservoir Analysis Tool - Professional Edition")
        self.root.geometry("1400x900")

        # Configure style
        self.setup_styles()

        # Initialize variables
        self.continuous_entries = {}
        self.discrete_vars = {}
        self.result_labels = {}

        # Build GUI
        self.create_gui()

    def setup_styles(self):
        """Configure ttk styles for professional appearance."""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure colors
        bg_color = '#F0F0F0'
        accent_color = '#2E86AB'

        style.configure('Title.TLabel',
                       font=('Helvetica', 16, 'bold'),
                       foreground=accent_color)
        style.configure('Section.TLabel',
                       font=('Helvetica', 12, 'bold'),
                       foreground=accent_color,
                       background=bg_color)
        style.configure('Input.TLabel',
                       font=('Helvetica', 10),
                       padding=5)
        style.configure('Result.TLabel',
                       font=('Helvetica', 11, 'bold'),
                       padding=5)
        style.configure('Calculate.TButton',
                       font=('Helvetica', 12, 'bold'),
                       padding=10)
        style.configure('Input.TEntry',
                       padding=5)

    def create_gui(self):
        """Build the complete GUI layout."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title = ttk.Label(main_frame,
                         text="Novel Integrated Reservoir Analysis Methodology",
                         style='Title.TLabel')
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Input sections
        self.create_continuous_inputs(main_frame)
        self.create_discrete_inputs(main_frame)

        # Calculate button
        calc_btn = ttk.Button(main_frame,
                             text="Calculate Efficiency Metrics",
                             style='Calculate.TButton',
                             command=self.on_calculate)
        calc_btn.grid(row=8, column=0, columnspan=2, pady=20)

        # Results section
        self.create_results_section(main_frame)

        # Plots section
        self.create_plots_section(main_frame)

    def create_continuous_inputs(self, parent):
        """Create continuous parameter input section."""
        section_label = ttk.Label(parent,
                                 text="Continuous Parameters",
                                 style='Section.TLabel')
        section_label.grid(row=1, column=0, columnspan=2, pady=(10, 5), sticky=tk.W)

        # Create labeled frame
        frame = ttk.LabelFrame(parent, text="", padding="10")
        frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        inputs = [
            ('mu_o', 'Oil Viscosity (μₒ)', 'cP', '0.1 - 100'),
            ('k', 'Reservoir Permeability (k)', 'mD', '0.1 - 500'),
            ('tds', 'Total Dissolved Solids (TDS)', 'ppm', '0 - 10000'),
            ('t', 'Reservoir Temperature (T)', '°C', '0 - 100')
        ]

        for i, (key, label, unit, range_str) in enumerate(inputs):
            # Label
            lbl = ttk.Label(frame, text=f"{label}:", style='Input.TLabel')
            lbl.grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)

            # Entry
            entry = ttk.Entry(frame, width=20, style='Input.TEntry')
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.continuous_entries[key] = entry

            # Unit label
            unit_lbl = ttk.Label(frame, text=unit, style='Input.TLabel')
            unit_lbl.grid(row=i, column=2, sticky=tk.W, padx=5, pady=5)

            # Range label
            range_lbl = ttk.Label(frame, text=f"Range: {range_str}",
                                 font=('Helvetica', 8, 'italic'))
            range_lbl.grid(row=i, column=3, sticky=tk.W, padx=10, pady=5)

    def create_discrete_inputs(self, parent):
        """Create discrete parameter input section."""
        section_label = ttk.Label(parent,
                                 text="Discrete Parameters",
                                 style='Section.TLabel')
        section_label.grid(row=3, column=0, columnspan=2, pady=(20, 5), sticky=tk.W)

        frame = ttk.LabelFrame(parent, text="", padding="10")
        frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        inputs = [
            ('cc', 'Clay Content'),
            ('dp', 'Reservoir Heterogeneity'),
            ('gc', 'Presence of Gas Cap'),
            ('aq', 'Presence of Aquifer')
        ]

        for i, (key, label) in enumerate(inputs):
            # Label
            lbl = ttk.Label(frame, text=f"{label}:", style='Input.TLabel')
            lbl.grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)

            # Radio buttons
            var = tk.StringVar(value="no")
            self.discrete_vars[key] = var

            radio_frame = ttk.Frame(frame)
            radio_frame.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)

            yes_radio = ttk.Radiobutton(radio_frame, text="Yes",
                                       variable=var, value="yes")
            yes_radio.grid(row=0, column=0, padx=(0, 20))

            no_radio = ttk.Radiobutton(radio_frame, text="No",
                                      variable=var, value="no")
            no_radio.grid(row=0, column=1)

    def create_results_section(self, parent):
        """Create results display section."""
        section_label = ttk.Label(parent,
                                 text="Efficiency Metrics",
                                 style='Section.TLabel')
        section_label.grid(row=9, column=0, columnspan=2, pady=(10, 5), sticky=tk.W)

        frame = ttk.LabelFrame(parent, text="", padding="15")
        frame.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # EFF1
        eff1_lbl = ttk.Label(frame,
                            text="EFF1 (Continuous): Awaiting calculation...",
                            style='Result.TLabel',
                            foreground='#1E5F8C')
        eff1_lbl.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.result_labels['eff1'] = eff1_lbl

        # EFF2
        eff2_lbl = ttk.Label(frame,
                            text="EFF2 (Discrete): Awaiting calculation...",
                            style='Result.TLabel',
                            foreground='#1E5F8C')
        eff2_lbl.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.result_labels['eff2'] = eff2_lbl

        # EFF (Total)
        eff_lbl = ttk.Label(frame,
                           text="EFF (Total): Awaiting calculation...",
                           font=('Helvetica', 14, 'bold'),
                           foreground='#A23B72')
        eff_lbl.grid(row=2, column=0, sticky=tk.W, pady=10)
        self.result_labels['eff'] = eff_lbl

    def create_plots_section(self, parent):
        """Create section for plots."""
        self.plot_frame = ttk.LabelFrame(parent,
                                        text="Parameter Response Curves",
                                        padding="10")
        self.plot_frame.grid(row=11, column=0, columnspan=2,
                            sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        parent.rowconfigure(11, weight=1)

    def get_efficiency_color(self, eff: float) -> str:
        """Return color based on efficiency value."""
        if eff >= 80:
            return '#27AE60'  # Green - Excellent
        elif eff >= 60:
            return '#F39C12'  # Orange - Good
        elif eff >= 40:
            return '#E67E22'  # Dark orange - Fair
        else:
            return '#E74C3C'  # Red - Poor

    def get_efficiency_rating(self, eff: float) -> str:
        """Return text rating based on efficiency value."""
        if eff >= 80:
            return "Excellent"
        elif eff >= 60:
            return "Good"
        elif eff >= 40:
            return "Fair"
        else:
            return "Poor"

    def on_calculate(self):
        """Handle calculate button click."""
        try:
            # Get and validate inputs
            entries = {
                'mu_o': self.continuous_entries['mu_o'].get(),
                'k': self.continuous_entries['k'].get(),
                'tds': self.continuous_entries['tds'].get(),
                't': self.continuous_entries['t'].get()
            }

            validated = InputValidator.validate_all_inputs(entries)

            # Get discrete inputs
            discrete = {
                'cc': self.discrete_vars['cc'].get() == 'yes',
                'dp': self.discrete_vars['dp'].get() == 'yes',
                'gc': self.discrete_vars['gc'].get() == 'yes',
                'aq': self.discrete_vars['aq'].get() == 'yes'
            }

            # Perform calculations
            continuous_outputs = ReservoirModel.calculate_continuous_outputs(
                validated['mu_o'], validated['k'],
                validated['tds'], validated['t']
            )

            discrete_outputs = ReservoirModel.calculate_discrete_outputs(
                discrete['cc'], discrete['dp'],
                discrete['gc'], discrete['aq']
            )

            eff1, eff2, eff = ReservoirModel.calculate_efficiency(
                continuous_outputs, discrete_outputs
            )

            # Update result labels with colors
            self.result_labels['eff1'].config(
                text=f"EFF1 (Continuous): {eff1:.2f}% - {self.get_efficiency_rating(eff1)}",
                foreground=self.get_efficiency_color(eff1)
            )
            self.result_labels['eff2'].config(
                text=f"EFF2 (Discrete): {eff2:.2f}% - {self.get_efficiency_rating(eff2)}",
                foreground=self.get_efficiency_color(eff2)
            )
            self.result_labels['eff'].config(
                text=f"EFF (Total): {eff:.2f}% - {self.get_efficiency_rating(eff)}",
                foreground=self.get_efficiency_color(eff)
            )

            # Generate plots
            self.update_plots(
                [validated['mu_o'], validated['k'], validated['tds'], validated['t']],
                continuous_outputs
            )

            # Show success message
            messagebox.showinfo("Success",
                              "Calculations completed successfully!\n\n"
                              f"Overall Efficiency: {eff:.2f}% ({self.get_efficiency_rating(eff)})")

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")

    def update_plots(self, continuous_values: List[float],
                    continuous_outputs: List[float]):
        """Update the plot display."""
        # Clear previous plots
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Generate new plots
        fig = ReservoirVisualizer.create_plots(continuous_values, continuous_outputs)

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Add toolbar
        toolbar = NavigationToolbar2Tk(canvas, self.plot_frame)
        toolbar.update()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = ReservoirAnalysisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

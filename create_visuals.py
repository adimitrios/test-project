"""
Standalone visualization generator - creates beautiful graphs without GUI.
"""

from typing import List, Tuple
from dataclasses import dataclass
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


# Configuration
@dataclass
class ModelCoefficients:
    """Mathematical model coefficients for reservoir analysis."""
    VISCOSITY_COEF: Tuple[float, float, float] = (1.94, -0.07, -0.995)
    PERMEABILITY_COEF: Tuple[float, float, float] = (-0.13, 0.24, 1.16)
    TDS_COEF: Tuple[float, float, float] = (-0.36, 0.13, 1.72)
    TEMPERATURE_COEF: Tuple[float, float, float] = (-27.32, 0.02, 29.87)
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
    DPI: int = 150
    MAIN_COLOR: str = '#2E86AB'
    POINT_COLOR: str = '#A23B72'
    GRID_ALPHA: float = 0.3
    LINE_WIDTH: float = 2.5
    POINT_SIZE: int = 120
    FONT_SIZE_TITLE: int = 11
    FONT_SIZE_LABEL: int = 10


COEF = ModelCoefficients()
RANGES = InputRanges()
PLOT_CFG = PlotConfig()


# Mathematical Functions
def viscosity_function(mu_o: float) -> float:
    """f₁(μₒ) = 1.94 × μₒ^(-0.07) - 0.995"""
    a, b, c = COEF.VISCOSITY_COEF
    return a * mu_o ** b + c


def permeability_function(k: float) -> float:
    """f₂(k) = -0.13 × k^(0.24) + 1.16"""
    a, b, c = COEF.PERMEABILITY_COEF
    return a * k ** b + c


def tds_function(tds: float) -> float:
    """f₃(TDS) = -0.36 × TDS^(0.13) + 1.72"""
    a, b, c = COEF.TDS_COEF
    return a * tds ** b + c


def temperature_function(t: float) -> float:
    """f₄(T) = -27.32 × T^(0.02) + 29.87"""
    a, b, c = COEF.TEMPERATURE_COEF
    return a * t ** b + c


def create_professional_plot(continuous_values: List[float],
                            continuous_outputs: List[float],
                            title_suffix: str = "") -> Figure:
    """Create professional visualization."""

    # Configure style
    plt.style.use('seaborn-v0_8-darkgrid')

    params = [
        {
            'range': np.linspace(RANGES.VISCOSITY[0], RANGES.VISCOSITY[1], 200),
            'function': viscosity_function,
            'label': 'Oil Viscosity (μₒ)',
            'unit': 'cP',
            'equation': r'$f_1 = 1.94 \times \mu_o^{-0.07} - 0.995$'
        },
        {
            'range': np.linspace(RANGES.PERMEABILITY[0], RANGES.PERMEABILITY[1], 200),
            'function': permeability_function,
            'label': 'Permeability (k)',
            'unit': 'mD',
            'equation': r'$f_2 = -0.13 \times k^{0.24} + 1.16$'
        },
        {
            'range': np.linspace(RANGES.TDS[0], RANGES.TDS[1], 200),
            'function': tds_function,
            'label': 'Total Dissolved Solids',
            'unit': 'ppm',
            'equation': r'$f_3 = -0.36 \times TDS^{0.13} + 1.72$'
        },
        {
            'range': np.linspace(RANGES.TEMPERATURE[0], RANGES.TEMPERATURE[1], 200),
            'function': temperature_function,
            'label': 'Temperature (T)',
            'unit': '°C',
            'equation': r'$f_4 = -27.32 \times T^{0.02} + 29.87$'
        }
    ]

    fig, axes = plt.subplots(1, 4, figsize=PLOT_CFG.FIGSIZE, dpi=PLOT_CFG.DPI)
    fig.suptitle(f'Continuous Parameter Response Functions{title_suffix}',
                 fontsize=14, fontweight='bold', y=1.02)

    for i, (ax, param) in enumerate(zip(axes, params)):
        x_range = param['range']
        y_range = param['function'](x_range)

        # Plot curve
        ax.plot(x_range, y_range,
               color=PLOT_CFG.MAIN_COLOR,
               linewidth=PLOT_CFG.LINE_WIDTH,
               label='Response Function',
               zorder=2)

        # Plot current point
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

        # Add equation
        ax.text(0.05, 0.95, param['equation'],
               transform=ax.transAxes,
               fontsize=8,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        ax.grid(True, alpha=PLOT_CFG.GRID_ALPHA, linestyle='--', linewidth=0.5)
        ax.legend(loc='best', fontsize=8, framealpha=0.9)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    plt.tight_layout()
    return fig


# Generate examples
print("=" * 70)
print("GENERATING PROFESSIONAL RESERVOIR ANALYSIS VISUALIZATIONS")
print("=" * 70)

# Example 1: Light Oil Reservoir
print("\n📊 Example 1: Light Oil Reservoir (Good Conditions)")
print("-" * 70)
mu_o, k, tds, t = 2.5, 150.0, 5000.0, 75.0
outputs = [viscosity_function(mu_o), permeability_function(k), tds_function(tds), temperature_function(t)]
eff = sum(o * w for o, w in zip(outputs, COEF.CONTINUOUS_WEIGHTS)) * 100

print(f"Inputs:  μₒ={mu_o} cP, k={k} mD, TDS={tds} ppm, T={t}°C")
print(f"Outputs: f₁={outputs[0]:.4f}, f₂={outputs[1]:.4f}, f₃={outputs[2]:.4f}, f₄={outputs[3]:.4f}")
print(f"EFF1:    {eff:.2f}% ({'Excellent' if eff >= 80 else 'Good' if eff >= 60 else 'Fair'})")

fig = create_professional_plot([mu_o, k, tds, t], outputs, " - Light Oil Reservoir")
fig.savefig('visualization_example1_light_oil.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close(fig)
print("✓ Saved: visualization_example1_light_oil.png")

# Example 2: Heavy Oil Reservoir
print("\n📊 Example 2: Heavy Oil Reservoir (Challenging Conditions)")
print("-" * 70)
mu_o, k, tds, t = 50.0, 20.0, 8500.0, 45.0
outputs = [viscosity_function(mu_o), permeability_function(k), tds_function(tds), temperature_function(t)]
eff = sum(o * w for o, w in zip(outputs, COEF.CONTINUOUS_WEIGHTS)) * 100

print(f"Inputs:  μₒ={mu_o} cP, k={k} mD, TDS={tds} ppm, T={t}°C")
print(f"Outputs: f₁={outputs[0]:.4f}, f₂={outputs[1]:.4f}, f₃={outputs[2]:.4f}, f₄={outputs[3]:.4f}")
print(f"EFF1:    {eff:.2f}% ({'Excellent' if eff >= 80 else 'Good' if eff >= 60 else 'Fair'})")

fig = create_professional_plot([mu_o, k, tds, t], outputs, " - Heavy Oil Reservoir")
fig.savefig('visualization_example2_heavy_oil.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close(fig)
print("✓ Saved: visualization_example2_heavy_oil.png")

# Example 3: Optimal Conditions
print("\n📊 Example 3: Optimal Reservoir Conditions")
print("-" * 70)
mu_o, k, tds, t = 1.0, 300.0, 1000.0, 90.0
outputs = [viscosity_function(mu_o), permeability_function(k), tds_function(tds), temperature_function(t)]
eff = sum(o * w for o, w in zip(outputs, COEF.CONTINUOUS_WEIGHTS)) * 100

print(f"Inputs:  μₒ={mu_o} cP, k={k} mD, TDS={tds} ppm, T={t}°C")
print(f"Outputs: f₁={outputs[0]:.4f}, f₂={outputs[1]:.4f}, f₃={outputs[2]:.4f}, f₄={outputs[3]:.4f}")
print(f"EFF1:    {eff:.2f}% ({'Excellent' if eff >= 80 else 'Good' if eff >= 60 else 'Fair'})")

fig = create_professional_plot([mu_o, k, tds, t], outputs, " - Optimal Conditions")
fig.savefig('visualization_example3_optimal.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close(fig)
print("✓ Saved: visualization_example3_optimal.png")

print("\n" + "=" * 70)
print("✅ ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
print("=" * 70)
print("\n📁 Generated Files:")
print("   • visualization_example1_light_oil.png")
print("   • visualization_example2_heavy_oil.png")
print("   • visualization_example3_optimal.png")
print("\n🎨 Visual Features:")
print("   ✓ Professional blue (#2E86AB) curves")
print("   ✓ Magenta (#A23B72) current value points")
print("   ✓ Mathematical equations displayed on each plot")
print("   ✓ Grid lines with transparency")
print("   ✓ White-bordered scatter points")
print("   ✓ High-resolution output (150 DPI)")
print("   ✓ Clean, professional styling")
print("\n💡 To see the interactive GUI with all features, run:")
print("   python3 stat1.py")
print("   (requires a display/X11 server)")
print("=" * 70)

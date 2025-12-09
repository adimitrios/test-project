"""
Standalone script to demonstrate the enhanced comprehensive dashboard.
"""

from typing import List, Tuple
from dataclasses import dataclass
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


# Configuration
@dataclass
class ModelCoefficients:
    VISCOSITY_COEF: Tuple[float, float, float] = (1.94, -0.07, -0.995)
    PERMEABILITY_COEF: Tuple[float, float, float] = (-0.13, 0.24, 1.16)
    TDS_COEF: Tuple[float, float, float] = (-0.36, 0.13, 1.72)
    TEMPERATURE_COEF: Tuple[float, float, float] = (-27.32, 0.02, 29.87)
    CONTINUOUS_WEIGHTS: Tuple[float, ...] = (0.1742, 0.1894, 0.1313, 0.1187)
    DISCRETE_WEIGHTS: Tuple[float, ...] = (0.1035, 0.1540, 0.0556, 0.073)


@dataclass
class InputRanges:
    VISCOSITY: Tuple[float, float] = (0.1, 100.0)
    PERMEABILITY: Tuple[float, float] = (0.1, 500.0)
    TDS: Tuple[float, float] = (0.0, 10000.0)
    TEMPERATURE: Tuple[float, float] = (0.0, 100.0)


@dataclass
class PlotConfig:
    FIGSIZE_FULL: Tuple[int, int] = (18, 12)
    DPI: int = 100
    MAIN_COLOR: str = '#2E86AB'
    POINT_COLOR: str = '#A23B72'
    COLOR_EXCELLENT: str = '#27AE60'
    COLOR_GOOD: str = '#F39C12'
    COLOR_FAIR: str = '#E67E22'
    COLOR_POOR: str = '#E74C3C'
    COLOR_CONTINUOUS: str = '#3498DB'
    COLOR_DISCRETE: str = '#9B59B6'


COEF = ModelCoefficients()
RANGES = InputRanges()
PLOT_CFG = PlotConfig()


# Mathematical Functions
def viscosity_function(mu_o):
    a, b, c = COEF.VISCOSITY_COEF
    return a * mu_o ** b + c


def permeability_function(k):
    a, b, c = COEF.PERMEABILITY_COEF
    return a * k ** b + c


def tds_function(tds):
    a, b, c = COEF.TDS_COEF
    return a * tds ** b + c


def temperature_function(t):
    a, b, c = COEF.TEMPERATURE_COEF
    return a * t ** b + c


def get_efficiency_color(eff):
    if eff >= 80:
        return PLOT_CFG.COLOR_EXCELLENT
    elif eff >= 60:
        return PLOT_CFG.COLOR_GOOD
    elif eff >= 40:
        return PLOT_CFG.COLOR_FAIR
    else:
        return PLOT_CFG.COLOR_POOR


def create_comprehensive_dashboard(continuous_values, continuous_outputs, discrete_outputs, eff1, eff2, eff):
    """Create comprehensive visualization dashboard."""
    plt.style.use('seaborn-v0_8-darkgrid')

    fig = plt.figure(figsize=PLOT_CFG.FIGSIZE_FULL, dpi=PLOT_CFG.DPI)
    gs = fig.add_gridspec(3, 4, hspace=0.4, wspace=0.3)

    fig.suptitle('Comprehensive Reservoir Analysis Dashboard',
                 fontsize=18, fontweight='bold', y=0.98)

    # ROW 1: Continuous Parameter Response Functions
    param_configs = [
        {'range': np.linspace(RANGES.VISCOSITY[0], RANGES.VISCOSITY[1], 200),
         'function': viscosity_function,
         'label': 'Viscosity (μₒ)', 'unit': 'cP',
         'equation': r'$f_1 = 1.94\mu_o^{-0.07} - 0.995$'},
        {'range': np.linspace(RANGES.PERMEABILITY[0], RANGES.PERMEABILITY[1], 200),
         'function': permeability_function,
         'label': 'Permeability (k)', 'unit': 'mD',
         'equation': r'$f_2 = -0.13k^{0.24} + 1.16$'},
        {'range': np.linspace(RANGES.TDS[0], RANGES.TDS[1], 200),
         'function': tds_function,
         'label': 'TDS', 'unit': 'ppm',
         'equation': r'$f_3 = -0.36TDS^{0.13} + 1.72$'},
        {'range': np.linspace(RANGES.TEMPERATURE[0], RANGES.TEMPERATURE[1], 200),
         'function': temperature_function,
         'label': 'Temperature (T)', 'unit': '°C',
         'equation': r'$f_4 = -27.32T^{0.02} + 29.87$'}
    ]

    for i, param in enumerate(param_configs):
        ax = fig.add_subplot(gs[0, i])
        x_range = param['range']
        y_range = param['function'](x_range)

        ax.plot(x_range, y_range, color=PLOT_CFG.MAIN_COLOR, linewidth=2, label='Response', zorder=2)
        ax.scatter(continuous_values[i], continuous_outputs[i], color=PLOT_CFG.POINT_COLOR,
                  s=120, zorder=3, edgecolors='white', linewidths=2,
                  label=f'Current: {continuous_outputs[i]:.3f}')

        ax.set_title(param['label'], fontsize=11, fontweight='bold', pad=8)
        ax.set_xlabel(f'{param["unit"]}', fontsize=9)
        ax.set_ylabel('Output', fontsize=9)
        ax.text(0.05, 0.95, param['equation'], transform=ax.transAxes, fontsize=7, va='top',
               bbox=dict(boxstyle='round', fc='wheat', alpha=0.5))
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.legend(fontsize=7, loc='best')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    # ROW 2: Efficiency Bar Chart
    ax_eff = fig.add_subplot(gs[1, 0:2])
    efficiencies = [eff1, eff2, eff]
    labels = ['EFF1\n(Continuous)', 'EFF2\n(Discrete)', 'EFF\n(Total)']
    colors = [get_efficiency_color(eff1), get_efficiency_color(eff2), get_efficiency_color(eff)]

    bars = ax_eff.bar(labels, efficiencies, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax_eff.set_ylabel('Efficiency (%)', fontsize=11, fontweight='bold')
    ax_eff.set_title('Efficiency Metrics Comparison', fontsize=12, fontweight='bold', pad=10)
    ax_eff.set_ylim(0, 100)
    ax_eff.axhline(y=80, color='green', linestyle='--', linewidth=1, alpha=0.5, label='Excellent (80%)')
    ax_eff.axhline(y=60, color='orange', linestyle='--', linewidth=1, alpha=0.5, label='Good (60%)')
    ax_eff.axhline(y=40, color='red', linestyle='--', linewidth=1, alpha=0.5, label='Fair (40%)')
    ax_eff.grid(True, axis='y', alpha=0.3)
    ax_eff.legend(fontsize=8, loc='upper right')

    for bar, val in zip(bars, efficiencies):
        height = bar.get_height()
        ax_eff.text(bar.get_x() + bar.get_width()/2., height, f'{val:.2f}%',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Weight Distribution
    ax_weights = fig.add_subplot(gs[1, 2:4])
    param_names = ['μₒ', 'k', 'TDS', 'T', 'Clay', 'Hetero', 'Gas', 'Aquifer']
    all_weights = list(COEF.CONTINUOUS_WEIGHTS) + list(COEF.DISCRETE_WEIGHTS)
    weight_percentages = [w * 100 for w in all_weights]
    colors_weights = [PLOT_CFG.COLOR_CONTINUOUS] * 4 + [PLOT_CFG.COLOR_DISCRETE] * 4

    bars_w = ax_weights.barh(param_names, weight_percentages, color=colors_weights, alpha=0.7, edgecolor='black')
    ax_weights.set_xlabel('Weight (%)', fontsize=11, fontweight='bold')
    ax_weights.set_title('Parameter Weight Distribution', fontsize=12, fontweight='bold', pad=10)
    ax_weights.grid(True, axis='x', alpha=0.3)
    ax_weights.invert_yaxis()

    for bar, val in zip(bars_w, weight_percentages):
        width = bar.get_width()
        ax_weights.text(width, bar.get_y() + bar.get_height()/2., f' {val:.1f}%',
                       ha='left', va='center', fontsize=8)

    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=PLOT_CFG.COLOR_CONTINUOUS, alpha=0.7, label='Continuous'),
        Patch(facecolor=PLOT_CFG.COLOR_DISCRETE, alpha=0.7, label='Discrete')
    ]
    ax_weights.legend(handles=legend_elements, fontsize=9, loc='lower right')

    # ROW 3: Contributions
    ax_cont = fig.add_subplot(gs[2, 0:2])
    cont_labels = ['Viscosity\n(f₁)', 'Permeability\n(f₂)', 'TDS\n(f₃)', 'Temperature\n(f₄)']
    cont_contributions = [output * weight * 100 for output, weight in zip(continuous_outputs, COEF.CONTINUOUS_WEIGHTS)]

    bars_cont = ax_cont.bar(cont_labels, cont_contributions, color=PLOT_CFG.COLOR_CONTINUOUS,
                           alpha=0.7, edgecolor='black', linewidth=1.5)
    ax_cont.set_ylabel('Contribution to EFF (%)', fontsize=11, fontweight='bold')
    ax_cont.set_title('Continuous Parameter Contributions', fontsize=12, fontweight='bold', pad=10)
    ax_cont.grid(True, axis='y', alpha=0.3)
    ax_cont.axhline(y=0, color='black', linewidth=0.8)

    for bar, val in zip(bars_cont, cont_contributions):
        height = bar.get_height()
        ax_cont.text(bar.get_x() + bar.get_width()/2., height, f'{val:.2f}%',
                    ha='center', va='bottom' if height >= 0 else 'top',
                    fontsize=9, fontweight='bold')

    ax_disc = fig.add_subplot(gs[2, 2:4])
    disc_labels = ['Clay\nContent', 'Reservoir\nHeterogeneity', 'Gas\nCap', 'Aquifer\nPresence']
    disc_contributions = [output * weight * 100 for output, weight in zip(discrete_outputs, COEF.DISCRETE_WEIGHTS)]

    bars_disc = ax_disc.bar(disc_labels, disc_contributions, color=PLOT_CFG.COLOR_DISCRETE,
                           alpha=0.7, edgecolor='black', linewidth=1.5)
    ax_disc.set_ylabel('Contribution to EFF (%)', fontsize=11, fontweight='bold')
    ax_disc.set_title('Discrete Parameter Contributions', fontsize=12, fontweight='bold', pad=10)
    ax_disc.grid(True, axis='y', alpha=0.3)
    ax_disc.axhline(y=0, color='black', linewidth=0.8)

    for bar, val in zip(bars_disc, disc_contributions):
        height = bar.get_height()
        ax_disc.text(bar.get_x() + bar.get_width()/2., height, f'{val:.2f}%',
                    ha='center', va='bottom' if height >= 0 else 'top',
                    fontsize=9, fontweight='bold')

    plt.tight_layout()
    return fig


# Generate demo
print("=" * 70)
print("GENERATING ENHANCED COMPREHENSIVE DASHBOARD")
print("=" * 70)

mu_o, k, tds, t = 10.0, 200.0, 4000.0, 70.0
continuous_outputs = [viscosity_function(mu_o), permeability_function(k),
                     tds_function(tds), temperature_function(t)]
discrete_outputs = [0.9, 0.79, 0.14, 0.76]  # No clay, No hetero, Yes gas, Yes aquifer

eff1 = sum(o * w for o, w in zip(continuous_outputs, COEF.CONTINUOUS_WEIGHTS)) * 100
eff2 = sum(o * w for o, w in zip(discrete_outputs, COEF.DISCRETE_WEIGHTS)) * 100
all_out = continuous_outputs + discrete_outputs
all_w = list(COEF.CONTINUOUS_WEIGHTS) + list(COEF.DISCRETE_WEIGHTS)
eff = sum(o * w for o, w in zip(all_out, all_w)) * 100

print(f"\n📊 Inputs: μₒ={mu_o} cP, k={k} mD, TDS={tds} ppm, T={t}°C")
print(f"🎯 EFF1={eff1:.2f}%, EFF2={eff2:.2f}%, EFF={eff:.2f}%")

fig = create_comprehensive_dashboard([mu_o, k, tds, t], continuous_outputs, discrete_outputs,
                                    eff1, eff2, eff)
fig.savefig('ENHANCED_COMPREHENSIVE_DASHBOARD.png', dpi=120, bbox_inches='tight', facecolor='white')
plt.close()

print("\n✅ Generated: ENHANCED_COMPREHENSIVE_DASHBOARD.png")
print("\n🎨 Dashboard includes:")
print("   ✓ 4 Parameter response curves with equations")
print("   ✓ Color-coded efficiency bar chart")
print("   ✓ Parameter weight distribution")
print("   ✓ Continuous & discrete contribution breakdowns")
print("=" * 70)

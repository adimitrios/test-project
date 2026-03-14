#!/usr/bin/env python3
"""Simple CLI calculator for EOR screening efficiency metrics.

Example:
    python stat_cli.py --mu-o 10 --k 100 --tds 5000 --temp 60 --cc no --dp no --gc no --aq no
"""

from __future__ import annotations

import argparse


CONTINUOUS_WEIGHTS = [0.1742, 0.1894, 0.1313, 0.1187]
DISCRETE_WEIGHTS = [0.1035, 0.1540, 0.0556, 0.0730]


def calculate_functions(mu_o: float, k: float, tds: float, temp: float, cc: bool, dp: bool, gc: bool, aq: bool):
    continuous_outputs = [
        1.94 * mu_o ** -0.07 - 0.995,
        -0.13 * k ** 0.24 + 1.16,
        -0.36 * tds ** 0.13 + 1.72,
        -27.32 * temp ** 0.02 + 29.87,
    ]

    discrete_outputs = [
        0.1 if cc else 0.9,
        0.21 if dp else 0.79,
        0.14 if gc else 0.86,
        0.24 if aq else 0.76,
    ]

    return continuous_outputs, discrete_outputs


def calculate_eff(continuous_outputs, discrete_outputs):
    all_weights = CONTINUOUS_WEIGHTS + DISCRETE_WEIGHTS
    all_outputs = continuous_outputs + discrete_outputs

    eff1 = sum(f * w for f, w in zip(continuous_outputs, CONTINUOUS_WEIGHTS)) * 100
    eff2 = sum(f * w for f, w in zip(discrete_outputs, DISCRETE_WEIGHTS)) * 100
    eff = sum(f * w for f, w in zip(all_outputs, all_weights)) * 100
    return eff1, eff2, eff


def parse_yes_no(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"yes", "y", "true", "1"}:
        return True
    if normalized in {"no", "n", "false", "0"}:
        return False
    raise argparse.ArgumentTypeError("Expected yes/no (or true/false, 1/0)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="EOR screening calculator (non-web)")

    parser.add_argument("--mu-o", type=float, default=10.0, help="Oil viscosity (cP), default: 10")
    parser.add_argument("--k", type=float, default=100.0, help="Permeability (mD), default: 100")
    parser.add_argument("--tds", type=float, default=5000.0, help="TDS (ppm), default: 5000")
    parser.add_argument("--temp", type=float, default=60.0, help="Temperature (°C), default: 60")

    parser.add_argument("--cc", type=parse_yes_no, default=False, help="Clay content present? yes/no")
    parser.add_argument("--dp", type=parse_yes_no, default=False, help="Reservoir heterogeneity? yes/no")
    parser.add_argument("--gc", type=parse_yes_no, default=False, help="Gas cap present? yes/no")
    parser.add_argument("--aq", type=parse_yes_no, default=False, help="Aquifer present? yes/no")

    return parser


def main() -> None:
    args = build_parser().parse_args()

    continuous_outputs, discrete_outputs = calculate_functions(
        mu_o=args.mu_o,
        k=args.k,
        tds=args.tds,
        temp=args.temp,
        cc=args.cc,
        dp=args.dp,
        gc=args.gc,
        aq=args.aq,
    )

    eff1, eff2, eff = calculate_eff(continuous_outputs, discrete_outputs)

    print("EOR Screening Results")
    print("-" * 24)
    print(f"EFF1 (Continuous): {eff1:.2f}%")
    print(f"EFF2 (Discrete):   {eff2:.2f}%")
    print(f"EFF (Total):       {eff:.2f}%")


if __name__ == "__main__":
    main()

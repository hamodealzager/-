"""Forex Intellect - Smart Forex Analysis & Signal Engine (starter implementation).

This module provides a command-style script that:
- Defines covered markets (majors/minors/exotics/commodities)
- Runs a lightweight technical + sentiment + event scoring pipeline
- Generates trade signals with RR >= 1:2
- Supports three trading plans (scalping/day/swing)

Run:
    python3 src/forex_intellect.py --symbol EUR/USD --price 1.0842 --plan day
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import argparse
import json


class MarketClass(str, Enum):
    MAJORS = "majors"
    MINORS = "minors"
    EXOTICS = "exotics"
    COMMODITIES = "commodities"


class PlanType(str, Enum):
    SCALPING = "scalping"
    DAY = "day"
    SWING = "swing"


@dataclass(frozen=True)
class Instrument:
    symbol: str
    market_class: MarketClass


@dataclass
class AnalysisInput:
    symbol: str
    current_price: float
    rsi: float
    macd_histogram: float
    bollinger_position: float
    trend_score: float
    event_impact: float
    sentiment_buy_ratio: float
    atr_percent: float


@dataclass
class TradingSignal:
    symbol: str
    side: str
    entry: float
    stop_loss: float
    take_profit_1: float
    take_profit_2: float
    risk_reward_tp1: float
    risk_reward_tp2: float
    confidence: float
    plan: PlanType


COVERED_INSTRUMENTS = [
    Instrument("EUR/USD", MarketClass.MAJORS),
    Instrument("GBP/USD", MarketClass.MAJORS),
    Instrument("USD/JPY", MarketClass.MAJORS),
    Instrument("EUR/GBP", MarketClass.MINORS),
    Instrument("AUD/JPY", MarketClass.MINORS),
    Instrument("USD/TRY", MarketClass.EXOTICS),
    Instrument("USD/SAR", MarketClass.EXOTICS),
    Instrument("XAU/USD", MarketClass.COMMODITIES),
    Instrument("XAG/USD", MarketClass.COMMODITIES),
    Instrument("WTI", MarketClass.COMMODITIES),
]

PLAN_SETTINGS = {
    PlanType.SCALPING: {"tp1_mult": 1.0, "tp2_mult": 2.2, "sl_mult": 0.8, "min_conf": 0.55},
    PlanType.DAY: {"tp1_mult": 1.3, "tp2_mult": 2.6, "sl_mult": 1.0, "min_conf": 0.60},
    PlanType.SWING: {"tp1_mult": 1.8, "tp2_mult": 3.2, "sl_mult": 1.2, "min_conf": 0.62},
}


def _normalize(val: float, min_v: float, max_v: float) -> float:
    if max_v == min_v:
        return 0.5
    return max(0.0, min(1.0, (val - min_v) / (max_v - min_v)))


def compute_confidence(data: AnalysisInput) -> float:
    """Aggregate technical + fundamental + sentiment factors to confidence [0..1]."""
    rsi_score = 1.0 - abs(data.rsi - 50) / 50
    macd_score = _normalize(data.macd_histogram, -2.0, 2.0)
    bb_score = 1.0 - abs(data.bollinger_position - 0.5) * 2
    trend_score = _normalize(data.trend_score, -1.0, 1.0)
    event_score = _normalize(1.0 - data.event_impact, 0.0, 1.0)
    sentiment_score = _normalize(abs(data.sentiment_buy_ratio - 0.5), 0.0, 0.5)

    confidence = (
        0.23 * rsi_score
        + 0.18 * macd_score
        + 0.17 * bb_score
        + 0.20 * trend_score
        + 0.12 * event_score
        + 0.10 * sentiment_score
    )
    return round(max(0.0, min(1.0, confidence)), 4)


def choose_side(data: AnalysisInput) -> str:
    momentum = data.macd_histogram + data.trend_score
    sentiment = data.sentiment_buy_ratio - 0.5
    return "buy" if (momentum + sentiment) >= 0 else "sell"


def generate_signal(data: AnalysisInput, plan: PlanType) -> TradingSignal | None:
    settings = PLAN_SETTINGS[plan]
    confidence = compute_confidence(data)
    if confidence < settings["min_conf"]:
        return None

    side = choose_side(data)
    entry = data.current_price

    risk_points = entry * data.atr_percent * settings["sl_mult"]
    reward1 = risk_points * max(2.0, settings["tp1_mult"] * 2.0)
    reward2 = risk_points * max(reward1 / risk_points + 0.5, settings["tp2_mult"])

    if side == "buy":
        stop_loss = entry - risk_points
        tp1 = entry + reward1
        tp2 = entry + reward2
    else:
        stop_loss = entry + risk_points
        tp1 = entry - reward1
        tp2 = entry - reward2

    risk = abs(entry - stop_loss)
    rr1 = abs(tp1 - entry) / risk
    rr2 = abs(tp2 - entry) / risk

    return TradingSignal(
        symbol=data.symbol,
        side=side,
        entry=round(entry, 6),
        stop_loss=round(stop_loss, 6),
        take_profit_1=round(tp1, 6),
        take_profit_2=round(tp2, 6),
        risk_reward_tp1=round(rr1, 2),
        risk_reward_tp2=round(rr2, 2),
        confidence=confidence,
        plan=plan,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Forex Intellect signal generator")
    parser.add_argument("--symbol", required=True, help="Instrument symbol e.g., EUR/USD")
    parser.add_argument("--price", required=True, type=float, help="Current market price")
    parser.add_argument("--plan", choices=[p.value for p in PlanType], default="day")
    parser.add_argument("--rsi", type=float, default=54.0)
    parser.add_argument("--macd", type=float, default=0.4)
    parser.add_argument("--bb", type=float, default=0.55, help="Bollinger position in [0..1]")
    parser.add_argument("--trend", type=float, default=0.3, help="Trend score in [-1..1]")
    parser.add_argument("--event-impact", type=float, default=0.35, help="News impact in [0..1]")
    parser.add_argument("--sentiment", type=float, default=0.61, help="Buy ratio in [0..1]")
    parser.add_argument("--atr-percent", type=float, default=0.0045, help="ATR as percentage of price")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    known_symbols = {i.symbol for i in COVERED_INSTRUMENTS}
    if args.symbol not in known_symbols:
        print(json.dumps({
            "error": f"Unsupported symbol: {args.symbol}",
            "supported": sorted(known_symbols),
        }, ensure_ascii=False, indent=2))
        return 2

    signal = generate_signal(
        AnalysisInput(
            symbol=args.symbol,
            current_price=args.price,
            rsi=args.rsi,
            macd_histogram=args.macd,
            bollinger_position=args.bb,
            trend_score=args.trend,
            event_impact=args.event_impact,
            sentiment_buy_ratio=args.sentiment,
            atr_percent=args.atr_percent,
        ),
        PlanType(args.plan),
    )

    if signal is None:
        print(json.dumps({
            "status": "no-trade",
            "reason": "confidence below threshold",
            "plan": args.plan,
        }, ensure_ascii=False, indent=2))
        return 0

    print(json.dumps(signal.__dict__, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import unittest

from src.forex_intellect import AnalysisInput, PlanType, generate_signal


class TestForexIntellect(unittest.TestCase):
    def test_generate_signal_respects_rr_minimum(self):
        data = AnalysisInput(
            symbol="EUR/USD",
            current_price=1.085,
            rsi=54,
            macd_histogram=0.5,
            bollinger_position=0.52,
            trend_score=0.35,
            event_impact=0.2,
            sentiment_buy_ratio=0.6,
            atr_percent=0.004,
        )
        signal = generate_signal(data, PlanType.DAY)
        self.assertIsNotNone(signal)
        self.assertGreaterEqual(signal.risk_reward_tp1, 2.0)

    def test_low_confidence_returns_none(self):
        data = AnalysisInput(
            symbol="EUR/USD",
            current_price=1.085,
            rsi=50,
            macd_histogram=0.0,
            bollinger_position=0.5,
            trend_score=0.0,
            event_impact=1.0,
            sentiment_buy_ratio=0.5,
            atr_percent=0.004,
        )
        signal = generate_signal(data, PlanType.SWING)
        self.assertIsNone(signal)


if __name__ == "__main__":
    unittest.main()

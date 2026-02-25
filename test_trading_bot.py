import unittest
import asyncio
from trading_bot import TradingBot

class TestTradingBot(unittest.TestCase):
    def test_bot_initialization(self):
        """Test that the TradingBot initializes without errors."""
        try:
            bot = TradingBot()
            # If initialization is successful, the test passes.
            self.assertIsInstance(bot, TradingBot)
        except Exception as e:
            self.fail(f"TradingBot initialization failed with an exception: {e}")

if __name__ == '__main__':
    unittest.main()

import ccxt.async_support as ccxt
import os

class ExchangeManager:
    def __init__(self, exchange_name='hyperliquid'):
        self.exchange_name = exchange_name
        self.exchange = None

    async def initialize(self):
        """Initializes the exchange connection."""
        exchange_class = getattr(ccxt, self.exchange_name)
        self.exchange = exchange_class({
            'apiKey': os.getenv('HYPERLIQUID_API_KEY'),
            'secret': os.getenv('HYPERLIQUID_SECRET'),
            'options': {
                'defaultType': 'swap',
            },
        })

    async def close(self):
        """Closes the exchange connection."""
        if self.exchange:
            await self.exchange.close()

    async def fetch_eligible_symbols(self, config):
        """Fetches and filters symbols based on price."""
        if not self.exchange:
            await self.initialize()

        markets = await self.exchange.load_markets()
        symbols = []
        for symbol in markets:
            ticker = await self.exchange.fetch_ticker(symbol)
            if ticker['last'] and config['min_coin_price'] < ticker['last'] < config['max_coin_price']:
                symbols.append({'symbol': symbol})
        return symbols

    async def open_position(self, symbol, side, amount):
        """Opens a position."""
        if not self.exchange:
            await self.initialize()

        try:
            order = await self.exchange.create_order(symbol, 'market', side, amount)
            return order
        except Exception as e:
            print(f"Error opening position: {e}")
            return False

    async def close_position(self, symbol, side, amount):
        """Closes a position."""
        if not self.exchange:
            await self.initialize()

        try:
            # To close a position, we need to create an order in the opposite direction.
            close_side = 'sell' if side == 'long' else 'buy'
            order = await self.exchange.create_order(symbol, 'market', close_side, amount, {'reduceOnly': True})
            return order
        except Exception as e:
            print(f"Error closing position: {e}")
            return False

    async def fetch_ticker(self, symbol):
        """Fetches the ticker for a symbol."""
        if not self.exchange:
            await self.initialize()

        return await self.exchange.fetch_ticker(symbol)

    async def fetch_positions(self, symbols, params):
        """Fetches open positions."""
        if not self.exchange:
            await self.initialize()

        return await self.exchange.fetch_positions(symbols, params)

"""Trading Bot Package"""

__version__ = "1.0.0"
__author__ = "Trading Bot Developer"

from bot.client import BinanceTestnetClient
from bot.orders import OrderManager

__all__ = ["BinanceTestnetClient", "OrderManager"]
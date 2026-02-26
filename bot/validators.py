"""Input validation for trading orders"""

from typing import Tuple
from enum import Enum

class OrderSide(str, Enum):
    """Order side enumeration"""
    BUY = "BUY"
    SELL = "SELL"

class OrderType(str, Enum):
    """Order type enumeration"""
    MARKET = "MARKET"
    LIMIT = "LIMIT"

class OrderValidator:
    """Validator for order parameters"""
    
    # List of valid trading pairs
    VALID_SYMBOLS = [
        "BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "DOGEUSDT",
        "LTCUSDT", "XRPUSDT", "LINKUSDT", "UNIUSDT", "MATICUSDT"
    ]
    
    @staticmethod
    def validate_symbol(symbol: str) -> str:
        """Validate trading symbol"""
        symbol = symbol.upper().strip()
        if not symbol:
            raise ValueError("Symbol cannot be empty")
        if not symbol.endswith("USDT"):
            raise ValueError(f"Symbol must end with USDT. Got: {symbol}")
        return symbol
    
    @staticmethod
    def validate_side(side: str) -> OrderSide:
        """Validate order side"""
        side = side.upper().strip()
        try:
            return OrderSide(side)
        except ValueError:
            raise ValueError(f"Order side must be BUY or SELL. Got: {side}")
    
    @staticmethod
    def validate_order_type(order_type: str) -> OrderType:
        """Validate order type"""
        order_type = order_type.upper().strip()
        try:
            return OrderType(order_type)
        except ValueError:
            raise ValueError(f"Order type must be MARKET or LIMIT. Got: {order_type}")
    
    @staticmethod
    def validate_quantity(quantity: str) -> float:
        """Validate quantity"""
        try:
            qty = float(quantity)
            if qty <= 0:
                raise ValueError("Quantity must be greater than 0")
            return qty
        except ValueError as e:
            if "greater than" in str(e):
                raise
            raise ValueError(f"Invalid quantity: {quantity}. Must be a positive number")
    
    @staticmethod
    def validate_price(price: str) -> float:
        """Validate price"""
        try:
            p = float(price)
            if p <= 0:
                raise ValueError("Price must be greater than 0")
            return p
        except ValueError as e:
            if "greater than" in str(e):
                raise
            raise ValueError(f"Invalid price: {price}. Must be a positive number")
    
    @staticmethod
    def validate_order_params(
        symbol: str,
        side: str,
        order_type: str,
        quantity: str,
        price: str = None
    ) -> Tuple[str, OrderSide, OrderType, float, float]:
        """
        Validate all order parameters together
        
        Returns:
            Tuple of (symbol, side, order_type, quantity, price)
        """
        validated_symbol = OrderValidator.validate_symbol(symbol)
        validated_side = OrderValidator.validate_side(side)
        validated_type = OrderValidator.validate_order_type(order_type)
        validated_qty = OrderValidator.validate_quantity(quantity)
        
        if validated_type == OrderType.LIMIT and not price:
            raise ValueError("Price is required for LIMIT orders")
        
        validated_price = OrderValidator.validate_price(price) if price else None
        
        return validated_symbol, validated_side, validated_type, validated_qty, validated_price

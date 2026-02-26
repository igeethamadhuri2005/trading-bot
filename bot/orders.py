"""Order management and execution"""

from typing import Dict, Any
from bot.client import BinanceTestnetClient
from bot.validators import OrderValidator, OrderSide, OrderType
from bot.logging_config import logger

class OrderManager:
    """Manages order placement and execution"""
    
    def __init__(self, client: BinanceTestnetClient):
        """
        Initialize OrderManager
        
        Args:
            client: BinanceTestnetClient instance
        """
        self.client = client
        self.validator = OrderValidator()
        logger.info("Initialized OrderManager")
    
    def execute_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: str,
        price: str = None
    ) -> Dict[str, Any]:
        """
        Execute a trading order with validation
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Price (required for LIMIT orders)
        
        Returns:
            Order response from API
        
        Raises:
            ValueError: If validation fails
            Exception: If API call fails
        """
        # Validate inputs
        validated_symbol, validated_side, validated_type, validated_qty, validated_price = \
            self.validator.validate_order_params(symbol, side, order_type, quantity, price)
        
        logger.info(f"Validated order parameters: {validated_symbol} {validated_side.value} {validated_type.value} {validated_qty}")
        
        try:
            # Place the order
            response = self.client.place_order(
                symbol=validated_symbol,
                side=validated_side.value,
                type_=validated_type.value,
                quantity=validated_qty,
                price=validated_price
            )
            
            # Log success
            self._log_order_success(response, validated_symbol, validated_side, validated_type, validated_qty, validated_price)
            
            return response
            
        except Exception as e:
            logger.error(f"Order execution failed: {str(e)}")
            raise
    
    def _log_order_success(
        self,
        response: Dict[str, Any],
        symbol: str,
        side: OrderSide,
        order_type: OrderType,
        quantity: float,
        price: float = None
    ) -> None:
        """Log successful order details"""
        order_id = response.get('orderId')
        status = response.get('status')
        executed_qty = response.get('executedQty', '0')
        avg_price = response.get('avgPrice', 'N/A')
        
        log_message = (
            f"\n{'='*60}\n"
            f"ORDER PLACED SUCCESSFULLY\n"
            f"{'='*60}\n"
            f"Symbol: {symbol}\n"
            f"Side: {side.value}\n"
            f"Type: {order_type.value}\n"
            f"Quantity: {quantity}\n"
        )
        
        if order_type == OrderType.LIMIT:
            log_message += f"Price: {price}\n"
        
        log_message += (
            f"Order ID: {order_id}\n"
            f"Status: {status}\n"
            f"Executed Qty: {executed_qty}\n"
            f"Avg Price: {avg_price}\n"
            f"{'='*60}\n"
        )
        
        logger.info(log_message)
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """Cancel an open order"""
        validated_symbol = self.validator.validate_symbol(symbol)
        
        logger.info(f"Attempting to cancel order {order_id} for {validated_symbol}")
        
        response = self.client.cancel_order(validated_symbol, order_id)
        logger.info(f"Order {order_id} cancelled successfully")
        
        return response

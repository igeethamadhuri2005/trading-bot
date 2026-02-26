"""Binance Futures Testnet Client"""

import requests
from typing import Dict, Any, Optional
from bot.logging_config import logger

class BinanceTestnetClient:
    """Client for interacting with Binance Futures Testnet"""
    
    BASE_URL = "https://testnet.binancefuture.com"
    
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize Binance Testnet client
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        
        logger.info(f"Initialized BinanceTestnetClient")
    
    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """Generate HMAC SHA256 signature for authenticated requests"""
        import hmac
        import hashlib
        from urllib.parse import urlencode
        
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        authenticated: bool = False
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Binance API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Request parameters
            authenticated: Whether request requires authentication
        
        Returns:
            Response JSON as dictionary
        
        Raises:
            requests.RequestException: If request fails
        """
        url = f"{self.BASE_URL}{endpoint}"
        headers = {"X-MBX-APIKEY": self.api_key} if authenticated else {}
        
        if params is None:
            params = {}
        
        # Add timestamp for authenticated requests
        if authenticated:
            from time import time
            params['timestamp'] = int(time() * 1000)
            params['signature'] = self._generate_signature(params)
        
        try:
            logger.debug(f"{method} {endpoint} with params: {params}")
            
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                timeout=10
            )
            
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Response: {data}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise
    
    def place_order(
        self,
        symbol: str,
        side: str,
        type_: str,
        quantity: float,
        price: Optional[float] = None,
        time_in_force: str = "GTC"
    ) -> Dict[str, Any]:
        """
        Place an order on Binance Futures Testnet
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            type_: MARKET or LIMIT
            quantity: Order quantity
            price: Price (required for LIMIT orders)
            time_in_force: GTC, IOC, or FOK (default: GTC)
        
        Returns:
            Order response from API
        """
        params = {
            'symbol': symbol,
            'side': side,
            'type': type_,
            'quantity': quantity,
        }
        
        if type_ == 'LIMIT':
            params['price'] = price
            params['timeInForce'] = time_in_force
        
        logger.info(f"Placing {type_} {side} order: {symbol} qty={quantity}")
        
        return self._request(
            method="POST",
            endpoint="/fapi/v1/order",
            params=params,
            authenticated=True
        )
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information"""
        logger.info("Fetching account information")
        
        return self._request(
            method="GET",
            endpoint="/fapi/v2/account",
            authenticated=True
        )
    
    def get_open_orders(self, symbol: Optional[str] = None) -> list:
        """Get open orders"""
        params = {}
        if symbol:
            params['symbol'] = symbol
        
        logger.info(f"Fetching open orders for symbol: {symbol or 'all'}")
        
        return self._request(
            method="GET",
            endpoint="/fapi/v1/openOrders",
            params=params,
            authenticated=True
        )
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """Cancel an open order"""
        params = {
            'symbol': symbol,
            'orderId': order_id
        }
        
        logger.info(f"Cancelling order {order_id} for {symbol}")
        
        return self._request(
            method="DELETE",
            endpoint="/fapi/v1/order",
            params=params,
            authenticated=True
        )

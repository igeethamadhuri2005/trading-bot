"""Command Line Interface for Trading Bot"""

import typer
from typing import Optional
from bot.client import BinanceTestnetClient
from bot.orders import OrderManager
from bot.logging_config import logger
import os

app = typer.Typer(
    help="Trading Bot for Binance Futures Testnet",
    rich_markup_mode="rich"
)

def get_credentials() -> tuple:
    """Get API credentials from environment variables"""
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        typer.echo(
            "[red]Error: BINANCE_API_KEY and BINANCE_API_SECRET environment variables are required[/red]",
            err=True
        )
        raise typer.Exit(code=1)
    
    return api_key, api_secret

@app.command()
def place_order(
    symbol: str = typer.Option(..., help="Trading pair (e.g., BTCUSDT)"),
    side: str = typer.Option(..., help="BUY or SELL"),
    order_type: str = typer.Option(..., help="MARKET or LIMIT"),
    quantity: float = typer.Option(..., help="Order quantity"),
    price: Optional[float] = typer.Option(None, help="Price (required for LIMIT orders)")
):
    """
    Place a market or limit order on Binance Futures Testnet
    
    Example:
        python cli.py place-order --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01
    """
    try:
        api_key, api_secret = get_credentials()
        
        typer.echo("\n[cyan]Initializing trading bot...[/cyan]")
        client = BinanceTestnetClient(api_key, api_secret)
        order_manager = OrderManager(client)
        
        typer.echo(f"[cyan]Placing {order_type} {side} order:[/cyan]")
        typer.echo(f"  Symbol: {symbol}")
        typer.echo(f"  Quantity: {quantity}")
        if price:
            typer.echo(f"  Price: {price}")
        
        response = order_manager.execute_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=str(quantity),
            price=str(price) if price else None
        )
        
        # Display response
        typer.echo("\n[green]Order Details:[/green]")
        typer.echo(f"  Order ID: {response.get('orderId')}")
        typer.echo(f"  Status: {response.get('status')}")
        typer.echo(f"  Executed Qty: {response.get('executedQty')}")
        
        if response.get('avgPrice'):
            typer.echo(f"  Avg Price: {response.get('avgPrice')}")
        
        typer.echo("\n[green]✓ Order placed successfully![/green]\n")
        
    except ValueError as e:
        typer.echo(f"\n[red]Validation Error: {str(e)}[/red]\n", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"\n[red]Error: {str(e)}[/red]\n", err=True)
        raise typer.Exit(code=1)

@app.command()
def market_order(
    symbol: str = typer.Option(..., help="Trading pair (e.g., BTCUSDT)"),
    side: str = typer.Option(..., help="BUY or SELL"),
    quantity: float = typer.Option(..., help="Order quantity")
):
    """Place a market order (shortcut)"""
    place_order(symbol=symbol, side=side, order_type="MARKET", quantity=quantity)

@app.command()
def limit_order(
    symbol: str = typer.Option(..., help="Trading pair (e.g., BTCUSDT)"),
    side: str = typer.Option(..., help="BUY or SELL"),
    quantity: float = typer.Option(..., help="Order quantity"),
    price: float = typer.Option(..., help="Order price")
):
    """Place a limit order (shortcut)"""
    place_order(symbol=symbol, side=side, order_type="LIMIT", quantity=quantity, price=price)

@app.command()
def account():
    """Display account information"""
    try:
        api_key, api_secret = get_credentials()
        
        client = BinanceTestnetClient(api_key, api_secret)
        account_info = client.get_account_info()
        
        typer.echo("\n[cyan]Account Information:[/cyan]")
        typer.echo(f"  Total Wallet Balance: {account_info.get('totalWalletBalance')} USDT")
        typer.echo(f"  Available Balance: {account_info.get('availableBalance')} USDT")
        typer.echo(f"  Total Margin Balance: {account_info.get('totalMarginBalance')} USDT\n")
        
    except Exception as e:
        typer.echo(f"\n[red]Error: {str(e)}[/red]\n", err=True)
        raise typer.Exit(code=1)

@app.command()
def open_orders(symbol: Optional[str] = typer.Option(None, help="Trading pair (optional)")):
    """Display open orders"""
    try:
        api_key, api_secret = get_credentials()
        
        client = BinanceTestnetClient(api_key, api_secret)
        orders = client.get_open_orders(symbol)
        
        if not orders:
            typer.echo("\n[yellow]No open orders[/yellow]\n")
            return
        
        typer.echo(f"\n[cyan]Open Orders: {len(orders)}[/cyan]\n")
        for order in orders:
            typer.echo(f"  Order ID: {order.get('orderId')}")
            typer.echo(f"  Symbol: {order.get('symbol')}")
            typer.echo(f"  Side: {order.get('side')}")
            typer.echo(f"  Type: {order.get('type')}")
            typer.echo(f"  Price: {order.get('price')}")
            typer.echo(f"  Quantity: {order.get('origQty')}")
            typer.echo()
        
    except Exception as e:
        typer.echo(f"\n[red]Error: {str(e)}[/red]\n", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()

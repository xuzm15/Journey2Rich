from __future__ import annotations

from typing import List

import typer

from journey2rich.data import YFinanceProvider
from journey2rich.engine.push import run_push
from journey2rich.engine.scheduler import run_daily_scheduler
from journey2rich.engine.paper import run_paper
from journey2rich.backtest.simple_backtest import run_backtest
from journey2rich.strategies.fundamental_quality import generate_signal

app = typer.Typer(add_completion=False)


@app.command()
def backtest(tickers: str, start: str, end: str) -> None:
    provider = YFinanceProvider()
    for t in [x.strip() for x in tickers.split(",") if x.strip()]:
        result = run_backtest(provider, t, start, end)
        typer.echo(result)


@app.command()
def signal(tickers: str, start: str, end: str) -> None:
    provider = YFinanceProvider()
    for t in [x.strip() for x in tickers.split(",") if x.strip()]:
        result = generate_signal(provider, t, start, end)
        typer.echo(result)


@app.command()
def push() -> None:
    """Build and push the daily brief to Discord once."""
    run_push()
    typer.echo("push sent")


@app.command()
def schedule() -> None:
    """Run a blocking scheduler that sends the brief daily at 08:00 in configured timezone."""
    run_daily_scheduler()


@app.command()
def paper(tickers: str, quantity: int = 1) -> None:
    """Place paper trades based on the current signal (IBKR paper)."""
    result = run_paper([x.strip() for x in tickers.split(",") if x.strip()], quantity)
    for row in result:
        typer.echo(row)


if __name__ == "__main__":
    app()

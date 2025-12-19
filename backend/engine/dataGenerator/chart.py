import pandas as pd
import mplfinance as mpf
from datetime import datetime, timedelta
from engine.dataGenerator.candle import Candle
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Chart:
    def __init__(self):
        pass

    def plot_instant_image(self, candles):
        if not candles:
            return
        
        if isinstance(candles[0], Candle):
            df = self._from_candle(candles)
            mpf.plot(df, type="candle", style='charles')
        elif isinstance(candles[0], list) or isinstance(candles[0], tuple):
            df = self._from_list(candles)
            mpf.plot(df, type='candle', style='classic')
        else:
            raise ValueError("Unsupported candle format")
        
        return df

    def _from_list(self, candles):
        # Create timestamps for each candle
        start = datetime.now()
        times = [start + timedelta(minutes=i) for i in range(len(candles))]

        # Convert to DataFrame
        df = pd.DataFrame(candles, columns=["open", "high", "low", "close"], index=times)

        return df
    
    def _from_candle(self, candles):
        # Generate timestamps (1 per candle)
        start = datetime.now()
        times = [start + timedelta(minutes=c.time) for c in candles]

        rows = []
        for c in candles:
            rows.append({
                "time": c.time,
                "open": c.open,
                "high": c.high,
                "low": c.low,
                "close": c.close,
                "volume": c.volume,
            })

        df = pd.DataFrame(rows, index=times)
        return df

    def plot_instant_web(self, candles):
        if not candles:
            return
        
        if isinstance(candles[0], Candle):
            df = self._from_candle(candles)
            # mpf.plot(df, type="candle", style='charles')
        elif isinstance(candles[0], list) or isinstance(candles[0], tuple):
            df = self._from_list(candles)
            # mpf.plot(df, type='candle', style='classic')
        else:
            raise ValueError("Unsupported candle format")

        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.7, 0.3]
        )

        # --- Candles ---
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                increasing_line_color='green',
                decreasing_line_color='red'
            ),
            row=1, col=1
        )

        # --- Volume ---
        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df['volume'],
            ),
            row=2, col=1
        )

        fig.update_layout(
            title="Candlestick with Volume",
            xaxis_rangeslider_visible=False,
            height=900
        )
        
        fig.show()

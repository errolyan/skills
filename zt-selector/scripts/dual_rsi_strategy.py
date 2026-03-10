"""
双RSI离散交易策略 (Dual RSI Divergence Strategy)

核心逻辑：
- 使用RSI(13)蓝色 和 RSI(42)红色
- 多头：两RSI都下降 + 差值约-20
- 空头：两RSI都上升 + 差值约+20
- 适合5分钟/15分钟周期，也可应用于日线分析
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class DualRSIStrategy:
    """双RSI离散策略"""

    def __init__(self,
                 fast_period=13,
                 slow_period=42,
                 divergence_threshold=20.0,
                 large_timeframe_threshold=16.0,
                 trend_lookback=3):
        """
        参数:
            fast_period: 快速RSI周期
            slow_period: 慢速RSI周期
            divergence_threshold: 小周期差值阈值
            large_timeframe_threshold: 大周期差值阈值（4H/D）
            trend_lookback: 趋势回看周期
        """
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.divergence_threshold = divergence_threshold
        self.large_timeframe_threshold = large_timeframe_threshold
        self.trend_lookback = trend_lookback

    def calculate_rsi(self, prices, period):
        """计算RSI指标"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def generate_signals(self, df, timeframe='1d'):
        """
        生成交易信号

        参数:
            df: 包含OHLCV数据的DataFrame
            timeframe: 时间周期 ('5m', '15m', '1h', '4h', '1d')

        返回:
            添加了信号列的DataFrame
        """
        # 复制数据避免修改原始数据
        data = df.copy()

        # 确保有close列
        if 'close' not in data.columns and 'Close' in data.columns:
            data['close'] = data['Close']
        elif 'close' not in data.columns and '收盘' in data.columns:
            data['close'] = data['收盘']

        # 计算RSI
        data['rsi_fast'] = self.calculate_rsi(data['close'], self.fast_period)
        data['rsi_slow'] = self.calculate_rsi(data['close'], self.slow_period)

        # 计算差值
        data['rsi_diff'] = data['rsi_fast'] - data['rsi_slow']

        # 选择阈值（大周期使用较小阈值）
        threshold = self.large_timeframe_threshold if timeframe in ['4h', '1d'] else self.divergence_threshold

        # 判断趋势
        data['fast_falling'] = data['rsi_fast'].rolling(self.trend_lookback + 1).apply(
            lambda x: all(x[i] > x[i+1] for i in range(len(x)-1)) if len(x) > 1 else False,
            raw=True
        )

        data['fast_rising'] = data['rsi_fast'].rolling(self.trend_lookback + 1).apply(
            lambda x: all(x[i] < x[i+1] for i in range(len(x)-1)) if len(x) > 1 else False,
            raw=True
        )

        data['slow_falling'] = data['rsi_slow'].rolling(self.trend_lookback + 1).apply(
            lambda x: all(x[i] > x[i+1] for i in range(len(x)-1)) if len(x) > 1 else False,
            raw=True
        )

        data['slow_rising'] = data['rsi_slow'].rolling(self.trend_lookback + 1).apply(
            lambda x: all(x[i] < x[i+1] for i in range(len(x)-1)) if len(x) > 1 else False,
            raw=True
        )

        # 生成交易信号
        # 多头信号：两RSI都下降 + 差值约-threshold
        data['long_signal'] = (
            (data['fast_falling'] == 1) &
            (data['slow_falling'] == 1) &
            (data['rsi_diff'] <= -threshold) &
            (data['rsi_diff'] >= -(threshold + 5))
        )

        # 空头信号：两RSI都上升 + 差值约+threshold
        data['short_signal'] = (
            (data['fast_rising'] == 1) &
            (data['slow_rising'] == 1) &
            (data['rsi_diff'] >= threshold) &
            (data['rsi_diff'] <= (threshold + 5))
        )

        # 信号列（1=做多, -1=做空, 0=无信号）
        data['signal'] = 0
        data.loc[data['long_signal'], 'signal'] = 1
        data.loc[data['short_signal'], 'signal'] = -1

        return data

    def get_latest_signal(self, df, timeframe='1d'):
        """
        获取最新的交易信号

        返回:
            dict: {
                'signal': 1/-1/0,
                'signal_text': '做多'/'做空'/'观望',
                'rsi_fast': float,
                'rsi_slow': float,
                'rsi_diff': float,
                'fast_trend': 'rising'/'falling'/'neutral',
                'slow_trend': 'rising'/'falling'/'neutral'
            }
        """
        signals = self.generate_signals(df, timeframe)
        if len(signals) == 0:
            return None

        latest = signals.iloc[-1]

        # 判断趋势方向
        fast_trend = 'falling' if latest['fast_falling'] else ('rising' if latest['fast_rising'] else 'neutral')
        slow_trend = 'falling' if latest['slow_falling'] else ('rising' if latest['slow_rising'] else 'neutral')

        signal_map = {1: '做多', -1: '做空', 0: '观望'}

        return {
            'signal': int(latest['signal']),
            'signal_text': signal_map[int(latest['signal'])],
            'rsi_fast': round(float(latest['rsi_fast']), 2),
            'rsi_slow': round(float(latest['rsi_slow']), 2),
            'rsi_diff': round(float(latest['rsi_diff']), 2),
            'fast_trend': fast_trend,
            'slow_trend': slow_trend
        }

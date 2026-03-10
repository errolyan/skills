#!/usr/bin/env python3
"""
A股RSI信号分析器

功能：
1. 对选定的股票进行双RSI技术分析
2. 生成交易信号（做多/做空/观望）
3. 支持批量分析
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

try:
    from dual_rsi_strategy import DualRSIStrategy
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from dual_rsi_strategy import DualRSIStrategy


class AStockRSIAnalyzer:
    """A股RSI分析器"""

    def __init__(self):
        self.strategy = DualRSIStrategy(
            fast_period=13,
            slow_period=42,
            divergence_threshold=16.0,  # A股日线建议用较小阈值
            trend_lookback=3
        )

    def get_stock_data(self, stock_code, period='daily', days=100):
        """
        获取股票历史数据

        参数:
            stock_code: 股票代码
            period: 周期 ('daily', '5', '15', '30', '60')
            days: 获取天数/条数

        返回:
            DataFrame
        """
        try:
            # 获取前复权数据
            df = ak.stock_zh_a_hist(
                symbol=stock_code,
                period=period,
                adjust="qfq"
            )

            if df is None or len(df) == 0:
                return None

            # 只取最近N天
            df = df.tail(days)

            # 重命名列名以适配策略
            df = df.rename(columns={
                '日期': 'date',
                '开盘': 'open',
                '收盘': 'close',
                '最高': 'high',
                '最低': 'low',
                '成交量': 'volume'
            })

            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)

            return df

        except Exception as e:
            print(f"获取股票数据失败 ({stock_code}): {e}")
            return None

    def analyze_single_stock(self, stock_code, stock_name=None):
        """
        分析单只股票

        返回:
            dict: 分析结果
        """
        # 获取日线数据
        df = self.get_stock_data(stock_code, period='daily', days=100)

        if df is None or len(df) < 50:
            return {
                'code': stock_code,
                'name': stock_name or stock_code,
                'status': 'error',
                'message': '数据不足或获取失败'
            }

        # 获取最新信号
        signal_info = self.strategy.get_latest_signal(df, timeframe='1d')

        if signal_info is None:
            return {
                'code': stock_code,
                'name': stock_name or stock_code,
                'status': 'error',
                'message': '信号计算失败'
            }

        # 获取当前价格
        current_price = float(df['close'].iloc[-1])

        return {
            'code': stock_code,
            'name': stock_name or stock_code,
            'status': 'success',
            'current_price': round(current_price, 2),
            'signal': signal_info['signal'],
            'signal_text': signal_info['signal_text'],
            'rsi_fast': signal_info['rsi_fast'],
            'rsi_slow': signal_info['rsi_slow'],
            'rsi_diff': signal_info['rsi_diff'],
            'fast_trend': signal_info['fast_trend'],
            'slow_trend': signal_info['slow_trend']
        }

    def analyze_stock_list(self, stock_list):
        """
        批量分析股票列表

        参数:
            stock_list: list of dict, 每个dict包含 {'code': '000001', 'name': '平安银行'}

        返回:
            DataFrame: 分析结果
        """
        results = []

        print(f"\n开始RSI技术分析 ({len(stock_list)}只股票)...")
        print("="*60)

        for i, stock in enumerate(stock_list):
            code = stock['code'] if isinstance(stock, dict) else stock
            name = stock.get('name', code) if isinstance(stock, dict) else code

            print(f"[{i+1}/{len(stock_list)}] 分析 {name}({code})...", end='\r')

            result = self.analyze_single_stock(code, name)
            results.append(result)

        print("\n" + "="*60)

        # 转换为DataFrame
        df = pd.DataFrame(results)

        # 过滤掉错误的记录
        df_success = df[df['status'] == 'success'].copy()

        if len(df_success) == 0:
            print("❌ 所有股票分析失败")
            return pd.DataFrame()

        # 只保留有用的列
        df_result = df_success[[
            'code', 'name', 'current_price',
            'signal_text', 'rsi_fast', 'rsi_slow', 'rsi_diff',
            'fast_trend', 'slow_trend'
        ]].copy()

        return df_result

    def print_analysis_report(self, df):
        """打印分析报告"""
        if len(df) == 0:
            print("无分析结果")
            return

        print("\n📊 双RSI技术分析报告")
        print("="*80)

        # 统计信号分布
        signal_counts = df['signal_text'].value_counts()
        print(f"\n信号分布:")
        for signal, count in signal_counts.items():
            print(f"   {signal}: {count}只")

        # 做多信号
        long_stocks = df[df['signal_text'] == '做多']
        if len(long_stocks) > 0:
            print(f"\n🟢 做多信号 ({len(long_stocks)}只):")
            print(long_stocks.to_string(index=False))

        # 做空信号
        short_stocks = df[df['signal_text'] == '做空']
        if len(short_stocks) > 0:
            print(f"\n🔴 做空信号 ({len(short_stocks)}只):")
            print(short_stocks.to_string(index=False))

        # 观望信号
        neutral_stocks = df[df['signal_text'] == '观望']
        if len(neutral_stocks) > 0:
            print(f"\n⚪ 观望 ({len(neutral_stocks)}只):")
            print(neutral_stocks.to_string(index=False))

        print("\n" + "="*80)
        print("💡 说明:")
        print("   - RSI(13)和RSI(42)同时下降 + 差值约-16 → 做多信号")
        print("   - RSI(13)和RSI(42)同时上升 + 差值约+16 → 做空信号")
        print("   - 其他情况 → 观望")
        print("   - 日线级别分析，建议结合其他指标综合判断")
        print("="*80)


def analyze_from_csv(csv_file):
    """
    从CSV文件读取股票列表并分析

    参数:
        csv_file: CSV文件路径，需包含 '代码' 和 '名称' 列
    """
    try:
        df = pd.read_csv(csv_file, encoding='utf-8-sig')

        if '代码' not in df.columns:
            print(f"❌ CSV文件缺少'代码'列")
            return

        stock_list = []
        for _, row in df.iterrows():
            stock_list.append({
                'code': str(row['代码']),
                'name': row.get('名称', row['代码'])
            })

        # 执行分析
        analyzer = AStockRSIAnalyzer()
        result_df = analyzer.analyze_stock_list(stock_list)

        # 打印报告
        analyzer.print_analysis_report(result_df)

        # 保存结果
        if len(result_df) > 0:
            output_file = f"RSI分析结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"\n💾 分析结果已保存至: {output_file}")

    except Exception as e:
        print(f"❌ 分析失败: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # 从CSV文件分析
        csv_file = sys.argv[1]
        print(f"📂 读取文件: {csv_file}")
        analyze_from_csv(csv_file)
    else:
        # 示例：分析几只热门股票
        print("🎯 示例：分析热门股票的RSI信号")
        print("="*60)

        sample_stocks = [
            {'code': '600036', 'name': '招商银行'},
            {'code': '000001', 'name': '平安银行'},
            {'code': '600519', 'name': '贵州茅台'},
            {'code': '000858', 'name': '五粮液'},
            {'code': '601318', 'name': '中国平安'}
        ]

        analyzer = AStockRSIAnalyzer()
        result_df = analyzer.analyze_stock_list(sample_stocks)
        analyzer.print_analysis_report(result_df)

        if len(result_df) > 0:
            output_file = f"RSI分析结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"\n💾 结果已保存至: {output_file}")

        print("\n💡 提示：")
        print("   可以用选股结果CSV作为输入：")
        print("   python rsi_analyzer.py 选股结果_20260310_143000.csv")

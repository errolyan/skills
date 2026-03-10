#!/usr/bin/env python3
"""
涨停敢死队选股工具 - 优化版
优化策略：先从今日涨停池筛选，大幅提升速度
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ZTSelectorFast:
    def __init__(self):
        self.today = datetime.now().strftime('%Y%m%d')

    def get_index_prediction(self):
        """分析上证指数"""
        try:
            df = ak.stock_zh_index_daily(symbol="sh000001")
            if df is None or len(df) < 20:
                return None

            recent = df.tail(20)
            ma5 = recent['close'].tail(5).mean()
            ma10 = recent['close'].tail(10).mean()
            trend = "看涨" if ma5 > ma10 else "看跌"

            return {
                'trend': trend,
                'ma5': ma5,
                'ma10': ma10,
                'current': recent['close'].iloc[-1]
            }
        except Exception as e:
            print(f"⚠️  指数分析失败: {e}")
            return None

    def get_zt_pool_with_sectors(self):
        """获取今日涨停池，返回(hot_sectors列表, zt_codes集合, zt_sector字典)"""
        try:
            print("   获取今日涨停池...")
            zt_pool = ak.stock_zt_pool_em(date=self.today)

            if zt_pool is None or len(zt_pool) == 0:
                print("   ⚠️  今日无涨停股票")
                return [], set(), {}

            print(f"   今日涨停股票: {len(zt_pool)} 只")

            # 统计各板块涨停数
            sector_counts = zt_pool['所属行业'].value_counts()
            hot_sectors = sector_counts[sector_counts >= 3].index.tolist()

            print(f"   热门板块（≥3只涨停）: {len(hot_sectors)} 个")
            for sector in hot_sectors[:10]:
                print(f"      - {sector}: {sector_counts[sector]}只涨停")

            # 构建 code -> sector 的映射
            code_sector_map = dict(zip(zt_pool['代码'], zt_pool['所属行业']))

            # 涨停股票代码集合（用于快速查找同板块股票）
            zt_codes = set(zt_pool['代码'].tolist())

            return hot_sectors, zt_codes, code_sector_map
        except Exception as e:
            print(f"   ⚠️  获取涨停池失败: {e}")
            return [], set(), {}

    def check_uptrend_simple(self, stock_code):
        """简化的趋势检查"""
        try:
            df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", adjust="qfq")
            if df is None or len(df) < 20:
                return False, None, 0

            recent = df.tail(20)

            # 计算均线
            ma5 = recent['收盘'].tail(5).mean()
            ma10 = recent['收盘'].tail(10).mean()
            ma20 = recent['收盘'].mean()
            current_price = recent['收盘'].iloc[-1]

            # 判断上扬
            uptrend = current_price > ma5 > ma10 > ma20

            # 统计10日涨停次数
            zt_count = int((recent.tail(10)['涨跌幅'] >= 9.9).sum())

            return uptrend, {
                'current': current_price,
                'ma5': ma5,
                'ma10': ma10,
                'ma20': ma20
            }, zt_count
        except Exception as e:
            return False, None, 0

    def select_stocks_fast(self, limit=20):
        """快速选股"""
        print("="*60)
        print("🎯 涨停敢死队选股系统启动（优化版）")
        print(f"📅 日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)

        # 1. 检查大盘
        print("\n【1/4】分析上证指数...")
        index_info = self.get_index_prediction()
        if index_info:
            print(f"   上证指数: {index_info['current']:.2f}")
            print(f"   MA5: {index_info['ma5']:.2f} | MA10: {index_info['ma10']:.2f}")
            print(f"   预判: {index_info['trend']}")
            if index_info['trend'] == "看跌":
                print("   ⚠️  大盘偏弱，建议谨慎")

        # 2. 获取热门板块 + 涨停池
        print("\n【2/4】识别热门板块...")
        hot_sectors, zt_codes, code_sector_map = self.get_zt_pool_with_sectors()

        if len(hot_sectors) == 0:
            print("\n❌ 今日无符合条件的热门板块")
            return

        # 3. 通过板块行情接口获取热门板块的股票
        print(f"\n【3/4】筛选热门板块股票...")
        candidate_pool = []
        try:
            for sector in hot_sectors:
                try:
                    sector_df = ak.stock_board_industry_cons_em(symbol=sector)
                    if sector_df is not None and len(sector_df) > 0:
                        for _, row in sector_df.iterrows():
                            candidate_pool.append({
                                '代码': row['代码'],
                                '名称': row['名称'],
                                '行业': sector
                            })
                except Exception:
                    pass

            # 去重
            candidate_df = pd.DataFrame(candidate_pool).drop_duplicates(subset='代码')

            # 过滤ST和价格为0
            candidate_df = candidate_df[
                ~candidate_df['名称'].str.contains('ST', na=False)
            ]

            print(f"   热门板块股票池: {len(candidate_df)} 只")
        except Exception as e:
            print(f"❌ 获取板块股票失败: {e}")
            return

        # 4. 详细筛选
        print(f"\n【4/4】深度分析（根据5大规则）...")
        candidates = []
        total = len(candidate_df)

        for i, (_, row) in enumerate(candidate_df.iterrows()):
            stock_code = row['代码']
            stock_name = row['名称']
            sector = row['行业']

            print(f"   [{i+1}/{total}] 检查 {stock_name}({stock_code})...", end='\r')

            # 检查K线和涨停
            uptrend, ma_info, zt_count = self.check_uptrend_simple(stock_code)

            if not uptrend or zt_count == 0:
                continue

            # 符合条件
            candidates.append({
                '代码': stock_code,
                '名称': stock_name,
                '行业': sector,
                '10日涨停次数': zt_count,
                'MA5': round(ma_info['ma5'], 2),
                'MA10': round(ma_info['ma10'], 2),
                'MA20': round(ma_info['ma20'], 2),
                '当前价': round(ma_info['current'], 2)
            })

            if len(candidates) >= limit:
                break

        # 5. 输出结果
        print("\n\n" + "="*60)
        print(f"✅ 筛选完成！符合条件的股票: {len(candidates)} 只\n")

        if len(candidates) == 0:
            print("❌ 未找到符合全部条件的股票")
            print("💡 可能原因：")
            print("   - 热门板块股票未形成上扬趋势")
            print("   - 近期无涨停记录")
            print("   - 建议调整筛选条件或等待更好时机")
            return

        # 按涨停次数排序
        result_df = pd.DataFrame(candidates)
        result_df = result_df.sort_values('10日涨停次数', ascending=False)

        print("📊 选股结果（按涨停次数排序）：\n")
        print(result_df.to_string(index=False))

        # 保存结果
        output_file = f"选股结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n💾 结果已保存至: {output_file}")

        # 简单分析
        print("\n" + "="*60)
        print("📈 数据分析:")
        print(f"   平均涨停次数: {result_df['10日涨停次数'].mean():.1f} 次")
        print(f"   涉及板块: {result_df['行业'].nunique()} 个")

        print("\n⚠️  风险提示：")
        print("   1. 本工具仅供模拟盘娱乐使用")
        print("   2. 股市有风险，投资需谨慎")
        print("   3. 历史数据不代表未来表现")
        print("   4. 14:30尾盘建议观察成交量和资金流向")
        print("="*60)


if __name__ == "__main__":
    selector = ZTSelectorFast()
    selector.select_stocks_fast(limit=20)

import numpy as np

def main():
    # 初始化参数
    initial_capital = 10000000
    num_stocks = 500
    initial_stock_price = 1
    num_days = 500
    initial_stock_holdings = initial_capital * 0.5 / num_stocks / initial_stock_price
    stock_prices = np.ones(num_stocks)

    # 概率分布设置
    probabilities = [0.3, 0.4, 0.2, 0.1]
    change_intervals = [(0, 0.01), (0.01, 0.03), (0.03, 0.08), (0.08, 0.1)]

    # 生成股价变动
    np.random.seed(0)
    price_changes = np.array([
        [
            1 + np.random.choice([-1, 1]) * np.random.uniform(*change_intervals[
                np.random.choice(len(probabilities), p=probabilities)
            ])
            for _ in range(num_stocks)
        ]
        for _ in range(num_days)
    ])

    # 实现交易策略
    capital = initial_capital
    holdings = np.full(num_stocks, initial_stock_holdings)

    for day_changes in price_changes:
        stock_prices *= day_changes
        for i in range(num_stocks):
            if stock_prices[i] > 1.05:
                sold_quantity = holdings[i] * 0.05
                holdings[i] -= sold_quantity
                capital += stock_prices[i] * sold_quantity
            elif stock_prices[i] < 0.95 and holdings[i] < 2 * initial_stock_holdings:
                additional_quantity = holdings[i] * 0.05
                holdings[i] += additional_quantity
                capital -= stock_prices[i] * additional_quantity

    # 计算性能指标
    final_portfolio_value = np.sum(holdings * stock_prices) + capital
    profit = final_portfolio_value - initial_capital
    return_rate = profit / (initial_capital * 0.5)

    # 输出结果
    print(f"Final Portfolio Value: {final_portfolio_value:.2f}")
    print(f"Return Rate: {return_rate * 100:.2f}%")

if __name__ == "__main__":
    main()
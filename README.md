# Journey2Rich

面向美股正股 + 期权的基本面交易代理（IBKR 模拟盘），支持每日中文简报推送（Discord）。

## 当前能力
- 数据层：`yfinance` 获取基本面、价格、期权链（后续可替换为付费数据源）。
- 策略层：基本面评分 + 趋势过滤，输出买入/观望/卖出。
- 期权层：方向性 + 收益型建议（带流动性过滤）。
- 简报层：每日结论表 + 资讯要点 + 模型解读（简短/详细）。
- 执行层：IBKR 模拟盘（`ib_insync`）。

## 快速开始
1. 安装依赖
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python3 -m pip install -U pip setuptools wheel
   pip install -e .
   ```

2. 配置环境变量
   ```bash
   cp .env.example .env
   ```
   在 `.env` 中填写：
   - `DISCORD_WEBHOOK_URL`
   - `OPENAI_API_KEY`（如需模型解读）
   - 其他默认保持即可

3. 运行一次推送
   ```bash
   journey2rich push
   ```

4. 每日定时推送（08:00，TIMEZONE 默认 Europe/London）
   ```bash
   journey2rich schedule
   ```

## 主要命令
- 回测：
  ```bash
  journey2rich backtest --tickers AAPL,MSFT,GOOGL --start 2019-01-01 --end 2024-01-01
  ```
- 生成信号：
  ```bash
  journey2rich signal --tickers AAPL,MSFT --start 2019-01-01 --end 2024-01-01
  ```
- 推送简报：
  ```bash
  journey2rich push
  ```

## 说明
- LLM 仅用于中文解读，不直接生成交易信号。
- 期权建议仅作参考，不构成交易建议。
- `yfinance` 适合原型验证，生产建议换成更稳定的数据源。

## IBKR（模拟盘）配置
- 安装 TWS 或 IB Gateway。
- 开启 API 访问并配置可信 IP。
- 默认端口一般为 `7497`。

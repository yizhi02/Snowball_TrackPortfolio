# Snowball Portfolio Tracker

Track portfolio rebalancing events from xueqiu.com and receive real-time notifications via Telegram.

## Features
- **Automated Tracking**: Monitors Xueqiu portfolio updates and detects new rebalancing events.
- **Telegram Notifications**: Sends alerts with detailed rebalancing information, and pins important messages for quick access.
- **Configurable Setup**: Easily customize settings through a `config.json` file, ensuring a streamlined and secure experience.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yizhi02/Snowball_TrackPortfolio.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your settings in `config.json`:
   ```json
   {
       "telegram_bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
       "telegram_chat_id": "YOUR_TELEGRAM_CHAT_ID",
       "portfolio_code": "YOUR_PORTFOLIO_CODE",
       "headers": {
           "cookie": "YOUR_COOKIE",
           "user_agent": "YOUR_USER_AGENT"
       }
   }
   ```

## Usage
Run the script to start tracking:
```bash
python main.py
```

The script will continuously monitor your Xueqiu portfolio and notify you of any changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
Please just open an issue or submit a pull request for any improvements or new features :)

## Disclaimer
Use this tool at your own risk. Ensure the json file is securely managed.

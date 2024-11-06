# Telegram Notification Bot

A simple Telegram bot that sends notifications and reminders at specific times or after a set duration. This bot is ideal for anyone who wants to use Telegram as a centralized platform for reminders and timed notifications.

## Project Overview
This bot was created to help users receive scheduled messages directly within Telegram. Telegram’s cross-device functionality allows users to access these notifications on any device, ensuring messages remain visible as unread until checked.

This project is a Minimum Viable Product (MVP), with basic functionalities. New features and enhancements will be added in future iterations.

## Features
- Notifications at Specific Times: Schedule a notification message to be sent at an exact time or date.
- Timer: Set a countdown timer that sends a message after the specified duration.
- Time Zone Support: Set your timezone using IANA format to receive accurate local-time notifications.

## Getting Started

### Prerequsites

Telegram Bot Token: You’ll need a token from BotFather to run the bot.

### Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```
2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Configure environment variables

```env
TELEGRAM_BOT_TOKEN=<your-telegram-bot-token>
DB_PATH=data/users.db # optional
```

4. Run the bot

```bash
python main.py
```

## Commands and Usage

- /settimezone: Set the timezone to receive notifications in your local time. Use IANA timezone format, e.g., Asia/Tbilisi.
- /timer: Set a countdown timer that will send a message after a specified time.
- /reminder: Schedule a message to be sent at a specific time and date.
Note: /settimezone must be used before setting reminders for accurate scheduling.

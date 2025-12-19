# AutoDailies

A Python script to automate daily tasks on [GenshinDrop.io](https://genshindrop.io)

## Requirements

* You need Python 3.x installed for this script to work.
* Also any latest Chromium-based browser.
* And [latest ChromeDriver version](https://googlechromelabs.github.io/chrome-for-testing/)

## Installation

1. Clone the repository using:

    ```bash
    git clone https://github.com/kitfc-dev/autodailies.git
    ```

2. Install python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Place your ChromeDriver and Chromium binary in the `res` directory.

4. Add account .pkl files to the `accounts` directory, that contain cookies needed to login to the website.

5. You can also customize the `config.py` if you need.

## Usage

```text
usage: main.py [-h] [-H] [-c] [-g] [-cs] [-w WAIT_AFTER] [--accounts [ACCOUNTS ...]] [--webhook_url WEBHOOK_URL]

AutoDailies

options:
  -h, --help            show this help message and exit
  -H, --headless        Starts the browser in headless mode.
  -c, --checkin         Runs the daily check-in.
  -g, --giveaway        Runs the giveaway.
  -cs, --cases          Open cases.
  -w WAIT_AFTER, --wait-after WAIT_AFTER
                        Number of seconds to wait before closing the browser.
  --accounts [ACCOUNTS ...]
                        Specify which accounts to process. If empty, all accounts will be processed.
  --webhook_url WEBHOOK_URL
                        Discord webhook URL to send logs to.
```

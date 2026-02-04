# AutoDailies

![AutoDailies Thumbnail](https://10ku.net/autodailies/auto-dailies-thumbnail-icon.png)

AutoDailies is automated selenium script for [GenshinDrop.io](https://genshindrop.io) to automate tasks like daily check-in, opening cases or joining giveaways on multiple accounts. It can earn in-game items in hoyo games such as primogems, welkin moon and others.

You can add your telegram account's cookies using pickle and put them in accounts folder. After that just create cron job for the script and let it run everyday. You may also add a discord webhook or telegram bot to receive notifications. Please follow the tutorial below on how to set up AutoDailies.

## Requirements

* You need Python 3.11+ installed for this script to work.
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

3. Place your ChromeDriver and Chromium binary in the default `res` or directory you choose.

4. Add account `.pkl` files to the `accounts` or directory you choose, that contain pickle files needed to login to the website. (check [Adding a new account](#adding-a-new-account) to learn how to create a pickle file)

5. Rename the `example_config.toml` to `config.toml` and edit it to your needs.

6. Run the script using `python main.py`

### Running in Docker

1. Clone the repository using:

    ```bash
    git clone https://github.com/kitfc-dev/autodailies.git
    ```

2. Add account `.pkl` files to the `accounts` or directory you choose, that contain pickle files needed to login to the website.

3. Rename the `example_config.toml` to `config.toml` and edit it to your needs.

4. Build the docker image using: `docker compose build`

5. Run docker: `docker compose run --rm main`

### Adding a new account

1. Run the script `main.py` with the `--new_account=10987654321` argument that has your phone number you want to add.

2. Wait for confirmation message in telegram, and accept it.

3. `.pkl` file will be automatically added to the `accounts` directory.

4. Send `/start` to new bot that appeared in your telegram account, send `/channel` and subscribe to channel, send `/verify` and then click `Start` button then send the secretcode you got in message during logging in, it should look like: `[SUCCESS] Login successful, secret code: ...`.

## Usage

```text
usage: main.py [-h] [-H] [-d] [-c] [-g] [-cs] [-si] [-w WAIT_AFTER] [--webhook_url WEBHOOK_URL] [--chromium_path CHROMIUM_PATH]
               [--chromedriver_path CHROMEDRIVER_PATH] [--config_path CONFIG_PATH] [--new_account NEW_ACCOUNT]

AutoDailies

options:
  -h, --help            show this help message and exit
  -H, --headless        Starts the browser in headless mode.
  -d, --debug           Enables debug.
  -c, --checkin         Runs the daily check-in.
  -g, --giveaway        Runs the giveaway.
  -cs, --cases          Opens the cases.
  -si, --sell_inventory
                        Sell items from inventory.
  -w, --wait-after WAIT_AFTER
                        Number of seconds to wait before closing the browser.
  --webhook_url WEBHOOK_URL
                        Discord webhook URL to send logs to.
  --chromium_path CHROMIUM_PATH
                        Path to the browser binary.
  --chromedriver_path CHROMEDRIVER_PATH
                        Path to the Chromedriver.
  --config_path CONFIG_PATH
                        Path to the config file.
  --new_account NEW_ACCOUNT
                        Phone number (with country code, only numbers) of the new telegram account to be added.
```

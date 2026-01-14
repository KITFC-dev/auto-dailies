# AutoDailies

![AutoDailies Thumbnail](https://10ku.net/autodailies/auto-dailies-thumbnail.png)

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

4. Add account `.pkl` files to the `accounts` or directory you choose, that contain pickle files needed to login to the website.

5. Rename the `example_config.toml` to `config.yaml` and edit it to your needs.

6. Run the script using `python main.py`

### Adding a new account

1. Run the script `main.py` with the `--new_account=accountname` flag.

2. You will be given 90 seconds to login in to the account.

3. Click the login button on top right, you will be redirected to telegram oauth.

4. After logging in with telegram oauth, refresh the initial browser tab and wait for the script to finish.

5. `.pkl` file will be automatically added to the `accounts` directory.

## Usage

```text
usage: main.py [-h] [-H] [-c] [-g] [-cs] [-w WAIT_AFTER] [--webhook_url WEBHOOK_URL] [--chromium_path CHROMIUM_PATH] [--chromedriver_path CHROMEDRIVER_PATH] [--config_path CONFIG_PATH] [--new_account NEW_ACCOUNT]

AutoDailies

options:
  -h, --help            show this help message and exit
  -H, --headless        Starts the browser in headless mode.
  -c, --checkin         Runs the daily check-in.
  -g, --giveaway        Runs the giveaway.
  -cs, --cases          Opens the cases.
  -w WAIT_AFTER, --wait-after WAIT_AFTER
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
                        Name of the new account, use to create a new pkl file.
```

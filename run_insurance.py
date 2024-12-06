import platform
import subprocess
import os
from datetime import datetime
from setup import utils


def main():
    num_terminals = int(input("Enter the number of terminals to open: "))
    num_repetition = int(
        input("How many times do you want to run the test? (Max: 1000): "))

    # Create the log file when the run_instance starts
    ad_click_log_file = utils.create_ad_click_log()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    terminal_log_file = f"log/terminal_run_log_{timestamp}.log"

    os.makedirs('log', exist_ok=True)

    # Prepare the command to execute
    system_platform = platform.system()
    working_directory = os.getcwd()

    for i in range(num_terminals):
        terminal_number = i + 1

        if system_platform == "Windows":
            command = f"python main.py {num_repetition} {terminal_number} {ad_click_log_file} {terminal_log_file}"
        else:
            command = f"python3 main.py {num_repetition} {terminal_number} {ad_click_log_file} {terminal_log_file}"

        try:
            if system_platform == "Windows":
                subprocess.Popen(["cmd", "/c", command], shell=True)

            elif system_platform == "Darwin":
                subprocess.Popen(["osascript", "-e", f"""
                tell application "Terminal"
                    do script "cd {working_directory} && {command}; exit"
                end tell
                """])

            else:
                subprocess.Popen(["bash", "-c", f"{command}; exit"])
        except Exception as e:
            print(f"Error launching terminal #{terminal_number}: {e}")


if __name__ == "__main__":
    main()

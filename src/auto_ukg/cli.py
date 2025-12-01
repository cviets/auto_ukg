import click
import subprocess
from pathlib import Path

from .action_modules import _login, _signin, _signout

@click.group()
def main():
    """
    Automate UKG Dimensions actions with Okta.
    """
    pass

@main.command()
def install_browsers():
    """
    Install Playwright browser binaries.
    """
    click.echo("Installing Playwright browsers...")
    subprocess.run(["playwright", "install"], check=True)

@main.command()
def install_cron():
    """
    Install cron jobs for 8:30 AM and 5:00 PM on weekdays.
    """
    
    python_path = subprocess.check_output(["which", "python3"]).decode().strip()
    signin_cmd = f"{python_path} -m auto_ukg signin"
    signout_cmd = f"{python_path} -m auto_ukg signout"
    log_file = Path.home() / ".auto_ukg.log"

    cron_entry = (
        f"30 8 * * 1-5 {signin_cmd} >> {log_file} 2>&1\n"
        f"0 17 * * 1-5 {signout_cmd} >> {log_file} 2>&1\n"
    )

    # Read existing crontab
    existing = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    current_cron = existing.stdout if existing.returncode == 0 else ""

    # Avoid duplicate entries
    if "auto_ukg" in current_cron:
        click.echo("Cron jobs already installed.")
        return

    new_cron = current_cron + "\n" + cron_entry

    # Install new crontab
    p = subprocess.Popen(["crontab"], stdin=subprocess.PIPE, text=True)
    p.communicate(new_cron)

    click.echo("Cron jobs installed:")
    click.echo(cron_entry)

@main.command()
def login():
    """
    Perform initial Okta login (manual)
    """
    _login()

@main.command()
def signin():
    """
    Automatically clock in
    """
    _signin()

@main.command()
def signout():
    """
    Automatically clock out
    """
    _signout()

if __name__ == '__main__':
    main()
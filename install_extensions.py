import json
import os
import subprocess
import sys


def install_python_packages(requirements_file):
    """Install Python packages from requirements file."""
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", requirements_file]
        )
        print("Python packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Python packages: {e}")


def get_installed_plugins():
    """Get list of installed PyCharm plugins."""
    config_dir = os.path.expanduser("~/.config/JetBrains/IdeaIC2023.1")
    plugins_file = os.path.join(config_dir, "plugins.json")

    if not os.path.exists(plugins_file):
        return []

    with open(plugins_file, "r") as file:
        plugins = json.load(file)
        installed_plugins = [plugin["id"] for plugin in plugins]

    return installed_plugins


def install_pycharm_plugin(plugin_id):
    """Install a PyCharm plugin by ID."""
    try:
        subprocess.check_call(["ide-scripting", "install-plugin", plugin_id])
        print(f"Plugin {plugin_id} installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install plugin {plugin_id}: {e}")


def install_pycharm_plugins(plugins_file):
    """Install PyCharm plugins from plugins file."""
    with open(plugins_file, "r") as file:
        plugins = file.read().splitlines()

    installed_plugins = get_installed_plugins()

    for plugin in plugins:
        if plugin not in installed_plugins:
            install_pycharm_plugin(plugin)
        else:
            print(f"Plugin {plugin} is already installed.")


if __name__ == "__main__":
    requirements_file = "requirements.txt"
    plugins_file = "plugins.txt"

    # Install Python packages
    if os.path.exists(requirements_file):
        install_python_packages(requirements_file)
    else:
        print(f"{requirements_file} not found.")

    # Install PyCharm plugins
    if os.path.exists(plugins_file):
        install_pycharm_plugins(plugins_file)
    else:
        print(f"{plugins_file} not found.")

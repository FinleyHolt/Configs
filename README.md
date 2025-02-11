# Configs CLI

A command-line tool for setting up development environments and managing dotfiles across different systems.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/configs-cli.git
cd configs-cli
```

2. Install the package:
```bash
pip install -e .
```

## Usage

The CLI provides several commands:

### Setup

Install dependencies and create symlinks:

```bash
configs-cli setup --system [ubuntu|arch|macos|windows] --repo /path/to/configs
```

IMPORTANT: Two arguments are required:
1. The `setup` command itself must be specified
2. The `--repo` argument must point to where you cloned this repository

For example:
```bash
# Correct usage:
configs-cli setup --system arch --repo ~/Github/Configs  # Points to cloned repo

# Common mistakes:
configs-cli --system arch                    # Wrong! Missing 'setup' command
configs-cli setup --system arch              # Wrong! Missing --repo argument
configs-cli setup --repo ~/Github/Configs    # Wrong! Missing --system argument
```

Options:
- `setup`: (Required) The command to run the setup process
- `--system`: (Required) Specify your operating system
- `--repo`: (Required) Path to your configs repository
- `--repo-url`: Git URL to clone if repo doesn't exist

### Help

Show detailed help information:

```bash
configs-cli help
```

### Source

Show commands to source your configuration:

```bash
configs-cli source
```

## Environment Variables

- `CONFIGS_REPO`: Set default repository path

## Features

- Automatic installation of common development tools
- Oh My Zsh installation and configuration
- Dotfiles management (zsh, tmux, neovim, i3)
- Cross-platform support (Ubuntu, Arch Linux, macOS, Windows)
- Plugin management (zsh-autosuggestions, syntax highlighting)

## Requirements

### Base Requirements
- Python 3.6 or higher
- Git
- Internet connection for downloading dependencies

### Before Running the CLI
On Arch Linux, install these prerequisites first:
```bash
# Install python and git
sudo pacman -S python python-pip git base-devel

# Install the CLI tool
git clone <your-repo-url>
cd configs-cli
pip install -e .
```

### Additional Requirements for KDE Setup
If you plan to use KDE Plasma as your desktop environment (--de kde), ensure these are installed first:
```bash
sudo pacman -S sddm sddm-kcm
sudo systemctl enable sddm
```

## License

MIT License

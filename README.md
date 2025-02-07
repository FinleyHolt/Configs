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
configs-cli setup --system [ubuntu|arch|macos|windows]
```

Options:
- `--system`: (Required) Specify your operating system
- `--repo`: Path to your configs repository (default: ~/.configs)
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

- Python 3.6 or higher
- Git
- Internet connection for downloading dependencies

## License

MIT License

#!/bin/bash

# Exit on any error
set -e

# Function to print status messages
print_status() {
    echo -e "\n\033[1;34m===> $1\033[0m"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please do not run as root"
    exit 1
fi

# Install git if not present
if ! command -v git &> /dev/null; then
    print_status "Installing git..."
    sudo pacman -S --noconfirm git
fi

# Install python and pip if not present
if ! command -v python &> /dev/null; then
    print_status "Installing python..."
    sudo pacman -S --noconfirm python python-pip
fi

# Install yay if not present
if ! command -v yay &> /dev/null; then
    print_status "Installing yay..."
    git clone https://aur.archlinux.org/yay.git /tmp/yay
    cd /tmp/yay
    makepkg -si --noconfirm
    cd -
    rm -rf /tmp/yay
fi

# Clone configs repository if not already present
REPO_PATH="$HOME/Github/Configs"
if [ ! -d "$REPO_PATH" ]; then
    print_status "Cloning configs repository..."
    mkdir -p "$HOME/Github"
    git clone https://github.com/YOUR_USERNAME/Configs.git "$REPO_PATH"
fi

# Install configs-cli
print_status "Installing configs-cli..."
cd "$REPO_PATH"
pip install --user -e .

# Run configs-cli setup
print_status "Running configs-cli setup..."
configs-cli setup --system arch --repo "$REPO_PATH"

print_status "Setup complete! Please log out and back in for all changes to take effect."

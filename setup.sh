#!/bin/bash
# setup.sh: Create symlinks for zsh, tmux, Neovim, and i3 configuration files

# Define the repository directory
REPO_DIR="$HOME/Github/Configs"

# Define directories for dotfiles and config files
DOTFILES_DIR="$REPO_DIR/dotfiles"
CONFIG_DIR="$REPO_DIR/config"

# Ensure the ~/.config directory exists
mkdir -p "$HOME/.config"

# Create symlink for .zshrc
echo "Linking zshrc..."
ln -sfv "$DOTFILES_DIR/zshrc" "$HOME/.zshrc"

# Create symlink for tmux config
echo "Linking tmux.conf..."
ln -sfv "$DOTFILES_DIR/tmux.conf" "$HOME/.tmux.conf"

# Create symlink for Neovim config
echo "Linking Neovim configuration..."
ln -sfv "$CONFIG_DIR/nvim" "$HOME/.config/nvim"

# Create symlink for i3 config
echo "Linking i3 configuration..."
ln -sfv "$CONFIG_DIR/i3" "$HOME/.config/i3"

echo "Symlinks created successfully!"

#!/usr/bin/env python3
import argparse
import subprocess
import os
import sys
import shutil

def install_oh_my_zsh_theme():
    """Install the Catppuccin theme and zsh plugins"""
    # Create directories
    themes_dir = os.path.expanduser("~/.oh-my-zsh/custom/themes")
    zsh_dir = os.path.expanduser("~/.zsh")
    plugins_dir = os.path.expanduser("~/.oh-my-zsh/custom/plugins")
    os.makedirs(themes_dir, exist_ok=True)
    os.makedirs(zsh_dir, exist_ok=True)
    os.makedirs(plugins_dir, exist_ok=True)
    
    # Clone Catppuccin theme repository
    catppuccin_dir = os.path.expanduser("~/.zsh/catppuccin-zsh-syntax-highlighting")
    if not os.path.exists(catppuccin_dir):
        print_step("Installing Catppuccin syntax highlighting theme")
        subprocess.run(["git", "clone", 
                       "https://github.com/catppuccin/zsh-syntax-highlighting.git",
                       catppuccin_dir], check=True)
        
        # Copy the mocha theme file
        subprocess.run(["cp", 
                       f"{catppuccin_dir}/themes/catppuccin_mocha-zsh-syntax-highlighting.zsh",
                       f"{zsh_dir}/"], check=True)

    # Install zsh-autosuggestions
    autosuggestions_dir = os.path.expanduser("~/.oh-my-zsh/custom/plugins/zsh-autosuggestions")
    if not os.path.exists(autosuggestions_dir):
        print_step("Installing zsh-autosuggestions plugin")
        subprocess.run(["git", "clone",
                       "https://github.com/zsh-users/zsh-autosuggestions.git",
                       autosuggestions_dir], check=True)

def install_oh_my_zsh():
    """Install Oh My Zsh if not already installed"""
    oh_my_zsh_dir = os.path.expanduser("~/.oh-my-zsh")
    zshrc_backup = os.path.expanduser("~/.zshrc.pre-oh-my-zsh")
    
    if not os.path.exists(oh_my_zsh_dir):
        print_step("Installing Oh My Zsh")
        
        # Backup existing .zshrc if it exists
        zshrc_path = os.path.expanduser("~/.zshrc")
        if os.path.exists(zshrc_path):
            print(f"Backing up existing .zshrc to {zshrc_backup}")
            shutil.copy2(zshrc_path, zshrc_backup)
        # First verify zsh version
        try:
            zsh_version = subprocess.check_output(["zsh", "--version"]).decode()
            print(f"Found ZSH: {zsh_version.strip()}")
        except subprocess.CalledProcessError:
            print("Error: ZSH is not properly installed")
            sys.exit(1)

        # Download the install script first for inspection
        install_script = "/tmp/install_ohmyzsh.sh"
        alternative_url = "https://install.ohmyz.sh"
        
        try:
            print_step("Downloading Oh My Zsh installer")
            print("Downloading from:", alternative_url)
            subprocess.run(["wget", "-O", install_script, alternative_url], check=True)
            print("Download completed successfully")
        except subprocess.CalledProcessError:
            backup_url = "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
            print("Failed to download from primary URL")
            print("Trying backup URL:", backup_url)
            subprocess.run(["wget", "-O", install_script, backup_url], check=True)
            print("Download completed successfully from backup URL")

        # Make the script executable
        os.chmod(install_script, 0o755)
        
        # Run the installer
        try:
            print_step("Running Oh My Zsh installer")
            subprocess.run([install_script, "--unattended"], check=True)
            
            # Remove the default .zshrc created by oh-my-zsh installation
            zshrc_path = os.path.expanduser("~/.zshrc")
            if os.path.exists(zshrc_path):
                # Compare with backup to see if it's the default oh-my-zsh config
                if os.path.exists(zshrc_backup):
                    with open(zshrc_path, 'r') as f1, open(zshrc_backup, 'r') as f2:
                        if f1.read() != f2.read():
                            print("Oh My Zsh created a new config, removing it")
                            os.remove(zshrc_path)
                        else:
                            print("Restoring original .zshrc")
                            shutil.copy2(zshrc_backup, zshrc_path)
                else:
                    os.remove(zshrc_path)
                
            # Clean up the installer
            os.remove(install_script)
        except subprocess.CalledProcessError as e:
            print(f"Error installing Oh My Zsh: {e}")
            sys.exit(1)
    else:
        print("Oh My Zsh is already installed")
        install_oh_my_zsh_theme()

def check_dependency(pkg):
    """Check if a package is installed"""
    if shutil.which(pkg):
        return True
    
    # Additional check for system packages
    if os.name != 'nt':  # Not Windows
        try:
            if subprocess.run(["which", pkg], 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE).returncode == 0:
                return True
        except:
            pass
    return False

def install_dependencies(system):
    dependencies = ["zsh", "tmux", "neovim", "i3", "curl", "git", "wget", "picom"]
    system = system.lower()
    
    # Filter out already installed dependencies
    to_install = [dep for dep in dependencies if not check_dependency(dep)]
    
    if not to_install:
        print("All core dependencies are already installed")
        return
        
    print(f"Installing missing dependencies: {', '.join(to_install)}")
    if system in ["ubuntu", "debian"]:
        print_step("Installing dependencies on Ubuntu/Debian")
        subprocess.check_call(["sudo", "apt-get", "update"])
        subprocess.check_call(["sudo", "apt-get", "install", "-y"] + dependencies)
    elif system in ["arch", "archlinux"]:
        print_step("Installing dependencies on Arch Linux")
        # For Arch, add Ruby and required dependencies for colorls
        arch_dependencies = dependencies + ["ruby", "ruby-rake", "gcc"]
        # Explicitly install i3-wm and i3status to avoid group selection prompt
        i3_deps = ["i3-wm", "i3status", "i3blocks", "i3lock"]
        all_deps = arch_dependencies + i3_deps
        # Remove i3 from the list since we're installing specific i3 packages
        all_deps.remove("i3")
        # Only install packages that aren't already installed
        to_install = []
        for pkg in all_deps:
            result = subprocess.run(["pacman", "-Qq", pkg], capture_output=True)
            if result.returncode != 0:
                to_install.append(pkg)
        
        # Add zsh plugins to the installation
        for plugin in ["zsh-syntax-highlighting", "zsh-autocomplete", "zsh-autosuggestions"]:
            if subprocess.run(["pacman", "-Qq", plugin], 
                            capture_output=True).returncode != 0:
                to_install.append(plugin)
        
        if to_install:
            print(f"Installing packages: {', '.join(to_install)}")
            subprocess.check_call(["sudo", "pacman", "-S", "--noconfirm"] + to_install)
        else:
            print("All required packages are already installed")
        
        # Now install the colorls gem with proper permissions
        print_step("Installing colorls gem")
        subprocess.check_call(["gem", "install", "colorls", "--user-install"])
    elif system in ["macos", "mac"]:
        print_step("Installing dependencies on macOS using Homebrew")
        subprocess.check_call(["brew", "update"])
        subprocess.check_call(["brew", "install"] + dependencies)
    elif system in ["windows"]:
        print_step("Installing dependencies on Windows")
        for pkg in dependencies:
            subprocess.check_call(["choco", "install", pkg, "-y"])
    else:
        print("Unknown system type. Please specify one of: ubuntu, arch, macos, or windows.")
        sys.exit(1)

def ensure_line_in_file(file_path, line):
    """
    Helper function to ensure a given line is present in file_path.
    If not, appends it.
    """
    try:
        with open(file_path, "r+") as f:
            content = f.read()
            if line not in content:
                f.write("\n" + line + "\n")
                print(f"Appended line to {file_path}: {line}")
            else:
                print(f"Line already present in {file_path}: {line}")
    except Exception as e:
        print(f"Error updating {file_path}: {e}")

def ensure_local_bin_in_zshrc(zshrc_path):
    local_bin_line = 'export PATH="$HOME/.local/bin:$PATH"'
    ensure_line_in_file(zshrc_path, local_bin_line)

def ensure_ruby_gem_bin_in_zshrc(zshrc_path):
    """
    Detects the Ruby gem bin directories and ensures they are added to the PATH
    in the dotfile (the source for ~/.zshrc).
    It uses two methods:
      1. The gem environment.
      2. Checks a local path under $HOME/.local/share/gem.
    """
    # First, try the gem environment.
    try:
        gem_dir = subprocess.check_output(["gem", "environment", "gemdir"]).decode().strip()
        gem_bin_dir = os.path.join(gem_dir, "bin")
        line = f'export PATH="{gem_bin_dir}:$PATH"'
        ensure_line_in_file(zshrc_path, line)
        print(f"Added Ruby gems bin directory to PATH (from gem environment): {gem_bin_dir}")
    except Exception as e:
        print(f"Skipping gem environment PATH update: {e}")

    # Next, check for a local gem installation directory.
    try:
        # Determine Ruby version
        ruby_version = subprocess.check_output(["ruby", "-e", "print RUBY_VERSION"]).decode().strip()
        local_gem_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "gem", "ruby", ruby_version)
        local_gem_bin_dir = os.path.join(local_gem_dir, "bin")
        if os.path.isdir(local_gem_bin_dir):
            line = f'export PATH="{local_gem_bin_dir}:$PATH"'
            ensure_line_in_file(zshrc_path, line)
            print(f"Added local Ruby gems bin directory to PATH: {local_gem_bin_dir}")
    except Exception as e:
        print(f"Skipping local gem PATH update: {e}")

def create_symlinks(repo_dir):
    home = os.path.expanduser("~")
    dotfiles_dir = os.path.join(repo_dir, "dotfiles")
    config_dir = os.path.join(repo_dir, "config")

    # Verify that the dotfiles directory exists.
    if not os.path.isdir(dotfiles_dir):
        print(f"Error: {dotfiles_dir} does not exist. Please check your repository.")
        sys.exit(1)
    
    # Create symlink for .zshrc.
    zshrc_src = os.path.abspath(os.path.join(dotfiles_dir, "zshrc"))
    zshrc_dest = os.path.join(home, ".zshrc")
    if os.path.exists(zshrc_dest) or os.path.islink(zshrc_dest):
        os.remove(zshrc_dest)
    os.symlink(zshrc_src, zshrc_dest)
    print(f"Created symlink: {zshrc_dest} -> {zshrc_src}")
    
    # Update the source dotfile to include PATH updates.
    ensure_local_bin_in_zshrc(zshrc_src)
    ensure_ruby_gem_bin_in_zshrc(zshrc_src)
    
    # Create symlink for .tmux.conf.
    tmux_src = os.path.abspath(os.path.join(dotfiles_dir, "tmux.conf"))
    tmux_dest = os.path.join(home, ".tmux.conf")
    if os.path.exists(tmux_dest) or os.path.islink(tmux_dest):
        os.remove(tmux_dest)
    os.symlink(tmux_src, tmux_dest)
    print(f"Created symlink: {tmux_dest} -> {tmux_src}")

    # Create symlink for Neovim config (placed in ~/.config/nvim).
    nvim_src = os.path.abspath(os.path.join(config_dir, "nvim"))
    nvim_dest = os.path.join(home, ".config", "nvim")
    os.makedirs(os.path.join(home, ".config"), exist_ok=True)
    if os.path.exists(nvim_dest) or os.path.islink(nvim_dest):
        if os.path.islink(nvim_dest):
            os.remove(nvim_dest)
        else:
            shutil.rmtree(nvim_dest)
    os.symlink(nvim_src, nvim_dest)
    print(f"Created symlink: {nvim_dest} -> {nvim_src}")

    # Create symlink for i3 config (placed in ~/.config/i3).
    i3_src = os.path.abspath(os.path.join(config_dir, "i3"))
    i3_dest = os.path.join(home, ".config", "i3")
    if os.path.exists(i3_dest) or os.path.islink(i3_dest):
        if os.path.islink(i3_dest):
            os.remove(i3_dest)
        else:
            shutil.rmtree(i3_dest)
    os.symlink(i3_src, i3_dest)
    print(f"Created symlink: {i3_dest} -> {i3_src}")

    # Create symlink for picom config (placed in ~/.config/picom).
    picom_src = os.path.abspath(os.path.join(config_dir, "picom"))
    picom_dest = os.path.join(home, ".config", "picom")
    if os.path.exists(picom_dest) or os.path.islink(picom_dest):
        if os.path.islink(picom_dest):
            os.remove(picom_dest)
        else:
            shutil.rmtree(picom_dest)
    os.symlink(picom_src, picom_dest)
    print(f"Created symlink: {picom_dest} -> {picom_src}")

def set_default_shell(shell):
    if os.name != 'nt':
        # Get the current shell from /etc/passwd instead of environment
        try:
            import pwd
            current_shell = pwd.getpwuid(os.getuid()).pw_shell
            if shell == current_shell:
                print(f"Default shell is already {shell}")
            else:
                print_step(f"Changing default shell to {shell}")
                subprocess.check_call(["chsh", "-s", shell])
        except ImportError:
            print("Could not import pwd module, falling back to environment check")
            current_shell = os.environ.get("SHELL", "")
            if shell not in current_shell:
                print_step(f"Changing default shell to {shell}")
                subprocess.check_call(["chsh", "-s", shell])
            else:
                print(f"Default shell is already {shell}")
    else:
        print("Skipping default shell change on Windows.")

def print_source_commands():
    home = os.path.expanduser("~")
    print(f"source {os.path.join(home, '.zshrc')}")
    print("Also, if new executables are not found, try running 'rehash' in your shell.")

def print_step(message):
    """Print a formatted step message"""
    print("\n" + "="*80)
    print(f">>> {message}")
    print("="*80 + "\n")

def main():
    print_step("Starting configs-cli setup tool")
    parser = argparse.ArgumentParser(
        description="Setup Configs and Dependencies CLI Tool"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: setup.
    setup_parser = subparsers.add_parser("setup", help="Install dependencies and create symlinks")
    setup_parser.add_argument("--system", required=True, choices=["ubuntu", "arch", "macos", "windows"],
                              help="Specify your operating system")
    # Use CONFIGS_REPO environment variable if set; otherwise, default to ~/.configs.
    default_repo = os.environ.get("CONFIGS_REPO", os.path.join(os.path.expanduser("~"), ".configs"))
    setup_parser.add_argument("--repo", default=default_repo,
                              help="Path to your Configs repository (or set CONFIGS_REPO)")
    setup_parser.add_argument("--repo-url", default=None,
                              help="Git URL of your repository (if not already cloned)")
    
    # Subcommand: source.
    subparsers.add_parser("source", help="Output commands to source your configuration")
    
    # Subcommand: help.
    help_parser = subparsers.add_parser("help", help="Show detailed help information")
    
    args = parser.parse_args()

    if args.command == "help":
        print("""
Configs CLI - Configuration Management Tool

Commands:
  setup   Install dependencies and create symlinks
    --system    Required. Choose: ubuntu, arch, macos, windows
    --repo      Path to configs repository (default: ~/.configs)
    --repo-url  Git URL to clone if repo doesn't exist
    
  source  Show commands to source your configuration
    
  help    Show this help message

Environment Variables:
  CONFIGS_REPO  Set default repository path

Examples:
  # Setup on Arch Linux (correct usage)
  configs-cli setup --system arch
  
  # Setup with custom repository
  configs-cli setup --system ubuntu --repo ~/my-configs
  
  # Show source commands
  configs-cli source

Common Mistakes:
  ❌ configs-cli --system arch        # Wrong! Missing 'setup' command
  ✅ configs-cli setup --system arch  # Correct!
""")
        return

    if args.command == "setup":
        # If the repository doesn't exist, attempt to clone it if --repo-url is provided.
        if not os.path.isdir(args.repo):
            if args.repo_url:
                print_step(f"Cloning repository from {args.repo_url}")
                subprocess.check_call(["git", "clone", args.repo_url, args.repo])
            else:
                print(f"Error: repository directory {args.repo} does not exist. "
                      f"Either clone it there or provide --repo-url to auto-clone it.")
                sys.exit(1)
        install_dependencies(args.system)
        if args.system != "windows":
            install_oh_my_zsh()
        create_symlinks(args.repo)
        if args.system != "windows":
            zsh_path = shutil.which("zsh")
            if zsh_path:
                set_default_shell(zsh_path)
            else:
                print("zsh not found; please install it!")
        else:
            print("Default shell change skipped on Windows.")
    elif args.command == "source":
        print_source_commands()

if __name__ == "__main__":
    main()


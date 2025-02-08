#!/bin/bash
# i3-setup.sh
# This script sets up your default workspace layout by launching:
#  - Workspace 1: A terminal
#  - Workspace 2: Firefox
#  - Workspace 3: Discord
#  - Workspace 4: Slack
# Adjust the sleep durations as needed for your system.

# Wait a bit for i3 to fully start up.
sleep 2


# Workspace 2: Firefox
i3-msg 'workspace 2: Firefox'
sleep 1
i3-msg 'exec firefox'
sleep 1

# Workspace 3: Discord
i3-msg 'workspace 3: Discord'
sleep 1
i3-msg 'exec discord'
sleep 10

# Workspace 4: Slack
i3-msg 'workspace 4: Slack'
sleep 1
i3-msg 'exec slack'
sleep 5

# Finally, switch back to workspace 1.
i3-msg 'workspace 1: Terminal'


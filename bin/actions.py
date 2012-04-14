#! /usr/bin/env python

"""A program to help manage action lists."""

# Standard library imports.
import ConfigParser
import os
import sys

# Local imports.
import cmdline

# Module constants.
CONFIG_PATH = '~/.actions'

app = cmdline.App()

@app.command
def setup(actions_dir='~/actions'):
    """Set up the current user's environment to use this command.

    If the config file exists, no changes are made.

    """

    config_path = os.path.expanduser(CONFIG_PATH)
    if os.path.exists(config_path):
        return

    actions_dir = os.path.expanduser(actions_dir)
    if not os.path.isdir(actions_dir):
        if os.path.exists(actions_dir):
            raise Exception('%s exists and is not a directory.' % actions_dir)

        os.mkdir(actions_dir)

    config = ConfigParser.ConfigParser()

    config.add_section('core')
    config.set('core', 'actions_dir', actions_dir)

    f = open(config_path, 'w')
    config.write(f)
    f.close()

def main():
    """Run from command line."""

    app.run()

if __name__ == '__main__':
    main()

#! /usr/bin/env python

"""A program to help manage action lists."""

# Standard library imports.
import os
import sys

# Local imports.
import cmdline

# Module constants.
CONFIG_PATH = '~/.actions'

app = cmdline.App()

@app.command
def setup(actions_dir='~'):
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

    # DEBUG What format should this file be in? This is basically .ini...
    f = open(config_path, 'w')
    f.write('actions_dir=%s%s' % (actions_dir, os.linesep))
    f.close()

def main():
    """Run from command line."""

    app.run()

if __name__ == '__main__':
    main()

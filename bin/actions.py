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
default_action_files = ['todo.txt', 'delegated.txt', 'review.txt']

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

# DEBUG mkdir is a pretty bad name for this tool. What should it actually
# be called?
# There should be a corresponding delete command, too, though I imagine it would
# only rarely be used.
@app.command
def mkdir(path):
    """Create an action directory at `path`."""

    # GRIPE Reading config values is basically setting global options - seems
    # like they should be read from the app object. For now, this works.
    config = ConfigParser.ConfigParser()
    config.read(os.path.expanduser(CONFIG_PATH))

    actions_dir = config.get('core', 'actions_dir')

    path = os.path.abspath(path)
    if os.path.exists(path):
        raise Exception('%s already exists.' % path)

    unused_path = os.path.dirname(path)
    symlink_name = os.path.basename(unused_path)
    while os.path.exists(os.path.join(actions_dir, symlink_name)):
        # GRIPE Dot-separated path fragments is not a great way to ensure
        # uniqueness, but it seems better than nesting directories. Improvements
        # welcome.
        unused_path = os.path.dirname(unused_path)
        symlink_name = os.path.basename(unused_path) + '.' + symlink_name

    symlink_path = os.path.join(actions_dir, symlink_name)
    print symlink_path

    os.mkdir(path)
    os.symlink(path, symlink_path)

    # Touch the three standard action files.
    for filename in default_action_files:
        f = open(os.path.join(path, filename), 'w')
        f.close()

def main():
    """Run from command line."""

    app.run()

if __name__ == '__main__':
    main()

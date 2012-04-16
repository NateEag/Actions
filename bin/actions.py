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
        raise Exception('A .actions file already exists.')

    actions_dir = os.path.expanduser(actions_dir)
    if not os.path.isdir(actions_dir):
        if os.path.exists(actions_dir):
            raise Exception('%s exists and is not a directory.' % actions_dir)

        os.mkdir(actions_dir)
        _mk_action_files(actions_dir)

        config = ConfigParser.ConfigParser()

        config.add_section('core')
        config.set('core', 'actions_dir', actions_dir)

        f = open(config_path, 'w')
        config.write(f)
        f.close()

# GRIPE There should be a corresponding delete command, too, though I imagine
# it would only rarely be used.
@app.command
def new(path):
    """Create an action directory at `path`."""

    # GRIPE Reading config values is basically setting global options - seems
    # like they should be read from the app object. For now, this works.
    config = ConfigParser.ConfigParser()
    config.read(os.path.expanduser(CONFIG_PATH))

    actions_dir = config.get('core', 'actions_dir')

    path = os.path.abspath(path)
    if os.path.exists(path):
        raise Exception('%s already exists.' % path)

    os.mkdir(path)
    _symlink_from_actions(path)

    # Create the standard action files.
    _mk_action_files(path)

def _mk_action_files(path):
    """Create default action files in `path`.

    `path` should be a directory.

    """

    if not os.path.isdir(path):
        raise Exception('%s is not a directory.' % path)

    for filename in default_action_files:
        f = open(os.path.join(path, filename), 'w')
        f.close()

def _symlink_from_actions(path):
    """Make a symlink to `path` from the main actions directory.

    Note that every symlink in the actions directory will have

    Dot-separated path fragments for symlink names are not a great way
    to ensure uniqueness, but they seem better than nesting directories.
    Improvements welcome.

    """

    # GRIPE Reading config values is basically setting global options - they
    # should be read from some central locale. For now, this works.
    config = ConfigParser.ConfigParser()
    config.read(os.path.expanduser(CONFIG_PATH))
    actions_dir = config.get('core', 'actions_dir')

    path = os.path.abspath(path)

    unused_path = os.path.dirname(path)
    symlink_name = os.path.basename(unused_path)
    while os.path.exists(os.path.join(actions_dir, symlink_name)):
        unused_path = os.path.dirname(unused_path)
        symlink_name = os.path.basename(unused_path) + '.' + symlink_name

    symlink_path = os.path.join(actions_dir, symlink_name)
    os.symlink(path, symlink_path)

def main():
    """Run from command line."""

    app.run()

if __name__ == '__main__':
    main()

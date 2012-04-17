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
default_action_files = ['goals.txt',
                        'todo.txt',
                        'done.txt',
                        'delegated.txt',
                        'review.txt']

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
# GRIPE `path` should probably have a default value of 'actions'. How can I
# distinguish between 'optional arguments' and 'options'? Maybe arguments to
# @app.command decorator?
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
    _mk_action_files(path)
    _hardlink_action_files(path)

def _mk_action_files(path):
    """Create default action files in `path`.

    `path` should be a directory.

    """

    if not os.path.isdir(path):
        raise Exception('%s is not a directory.' % path)

    for filename in default_action_files:
        f = open(os.path.join(path, filename), 'w')
        f.close()

def _hardlink_action_files(path):
    """Hardlink action files in `path` from the main actions directory.

    Creates a dir in the main actions dir to store the hardlinks in. The
    directory's name is guaranteed to be unique within the main actions dir.

    The hardlink container is named with the minimum-needed dot-separated
    components from `os.abspath(path)` to ensure a unique name.

    This means if you move the dir at `path`, the container dir will
    wind up with an out-of-date name. It'd be possible to synchronize
    names on demand, if it proved useful.

    """

    # GRIPE Reading config values is basically setting global options - they
    # should be read from some central locale. For now, this works.
    config = ConfigParser.ConfigParser()
    config.read(os.path.expanduser(CONFIG_PATH))
    actions_dir = config.get('core', 'actions_dir')

    path = os.path.abspath(path)

    unused_path = os.path.dirname(path)
    hardlink_name = os.path.basename(unused_path)
    while os.path.exists(os.path.join(actions_dir, hardlink_name)):
        unused_path = os.path.dirname(unused_path)
        hardlink_name = os.path.basename(unused_path) + '.' + hardlink_name

    hardlink_path = os.path.join(actions_dir, hardlink_name)
    os.mkdir(hardlink_path)

    # Make the actual hardlinks.
    for filename in default_action_files:
        source = os.path.join(path, filename)
        target = os.path.join(hardlink_path, filename)
        os.link(source, target)

def main():
    """Run from command line."""

    app.run()

if __name__ == '__main__':
    main()

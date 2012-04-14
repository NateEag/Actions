"""A module for writing command-line Python programs.

The command-line interface is defined by writing functions and using
decorators to mark them as commands supported by the program.

This is a proof-of-concept and extremely incomplete.

It may also be a bad idea - I imagine this approach would be fairly
confusing to Python newbies, and I don't see a sane way to handle
optional args. It can be argued that there are no such things, since
options are the optional entity, but git uses them, and I've gotten used
to it.

Still, I failed to resist it, because it seemed to have potential.

If it seems to be worth pursuing, check out

https://github.com/anandology/subcommand/blob/master/subcommand.py
http://jimmyg.org/blog/2009/python-command-line-interface-(cli)-with-sub-commands.html
http://code.google.com/p/cmdln/

All of them could be useful in massively improving this code, by way of
how they work and demonstrating what features should be supported.

Remember, too, that not all programs use subcommands, even though that's
all this currently supports.

"""

# Standard library imports.
import inspect
import sys

class InvalidInput(Exception):
    """Indicates that invalid input was given.

    self.value is a string explaining the problem with the input.

    """

    def __init__(self, value):
        self.value = value

def parse_opts(inputs):
    """Return a tuple of (`args`, `opts`) constructed from `inputs`.

    `inputs` should be a list of arguments like sys.argv[1:].
    `args` will be a list of arguments.
    `opts` will be a dict mapping option names to values.

    GRIPE All args and option values will be returned as strings.
    It would be nice to let users specify parsing algs for them,
    and to provide a few built-in ones (datetime, int, float, etc).

    That might work better outside this function, though. Before you
    bother with heavy parsing, make sure your input thus far is valid.

    """

    args = []
    opts = {}
    num_inputs = len(inputs)
    i = 0
    while i < num_inputs:
        item = inputs[i]
        if item.startswith('-'):
            # item is an option.
            item = item.lstrip('-')

            if '=' in item:
                # The option and value are both in this string.
                opt, junk, val = item.partition('=')
            else:
                # The next item is the value for this option.
                # DEBUG How do we deal with it when there is no next item?
                opt = item
                i += 1
                val = inputs[i]

            opts[opt] = val
        else:
            args.append(item)

        i += 1

    return (args, opts)

class App(object):
    """Handle interface-related state for a command-line app."""

    def __init__(self):

        self.args = []
        self.opts = {}
        self.cmd = None
        self.func = None

        self.commands = {}
        self.script_name = None
        self.argv = []

    def command(self, func):
        """A decorator for functions to be used as app commands."""

        cmd_name = func.__name__.replace('_', '-')
        self.commands[cmd_name] = func

    def _parse_input(self, argv):
        """Set self.args, self.opts, and self.cmd based on `argv`."""

        self.argv = argv[:]
        self.script_name = argv[0]

        inputs = argv[1:]

        args, opts = parse_opts(inputs)

        if len(self.commands) > 0:
            # This program uses subcommands, and the first arg must therefore
            # be one.
            # GRIPE Better error handling here would be just dandy.
            if len(args) < 1:
                raise InvalidInput('You must enter a command.')

            self.cmd = args[0]
            args = args[1:]

        self.args = args
        self.opts = opts

        if self.cmd not in self.commands:
            # GRIPE There should be more advanced error handling here.
            # Like printing a usage message if one is defined.
            raise InvalidInput('"%s" is not a known command.' % self.cmd)

        self.func = self.commands[self.cmd]

        # Validate inputs to func.
        # GRIPE Add value parsing after this, once we know the basics are
        # ship-shape.
        args, varargs, varkw, defaults = inspect.getargspec(self.func)
        num_opts = len(defaults)
        num_args = len(args) - num_opts

        if len(self.args) != num_args:
            raise InvalidInput('%s takes %d arguments.' % (self.cmd, num_args))

        opt_names = args[num_args:]

        for key in self.opts:
            # GRIPE Replacing hyphens with underscores should happen only once.
            if key.replace('-', '_') not in opt_names:
                raise InvalidInput('%s does not accept the %s option.' %
                                   (self.cmd, key))


    def run(self, argv=None):
        """Run the app with `argv` as command-line input.

        `argv` defaults to sys.argv.

        """

        if argv is None:
            argv = sys.argv

        try:
            self._parse_input(argv)

            opts = {}
            for key in self.opts:
                # Convert hyphens to underscores, for passing to function.
                # GRIPE There is probably a better way to do this.
                # DEBUG Document that opt_name counts as opt-name.
                opts[key.replace('-', '_')] = self.opts[key]

            # GRIPE It's sort of ugly to have self.func be populated by
            # self._parse_input(). It's not crystal clear where it comes from.
            return self.func(*self.args, **opts)
        except InvalidInput as exc:
            print >> sys.stderr, exc.value

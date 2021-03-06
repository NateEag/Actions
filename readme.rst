=======
Actions
=======

An approach to organizing life based on *Getting Things Done*, by
David Allen.

The point is to make your commitments explicit by tracking the actions that
will fulfill them, rather than trying to remember them all.

For those of us who are not natural reductionists or have sloppy memories, this
could be helpful.


Definitions
===========

Action
  A concrete, specific act to be performed.

Project
  A desired outcome that takes more than one action to achieve.

Current projects
  The list of all projects you are currently committed to making progress on.

Possible projects
  The list of projects you are not committed to but are interested in.

Calendar
  The collection of your date-specific actions and information.

Todo list
  A list of actions that must be done before the project they are for can be
  finished.

Delegated actions
  A list of actions you have delegated to other entities and are waiting to
  hear back about.

Inbox
  A source of data that someone wants you to look at. An inbox forms an
  implicit commitment with the world that you will consider and act
  appropriately on anything in it.

Reviewbox
  A source of data that you want to look at again. Only you may put things in
  it, so it involves no commitments to anyone other than yourself.

Reference Library
  An organized collection of information and documents that will likely be
  useful in the future.

Context
  An environment or environmental trait that enables or prevents the
  performance of some actions. Theoretically used to annotate actions for more
  efficient batch processing and for pre-planning actions for specialized
  contexts. Currently largely unused in this document.

  Examples: @phone, @internet, @staff-meeting, @grocery-store.


Algorithms
==========

There are several useful algorithms that can be described using the terminology
from Definitions.


Triaging Possible Actions
-------------------------

When you think of an action you could do, you should triage it.

The first step in the triage process is to decide whether it's worth thinking
about this possible action right now. There are two useful tests for this:

1. Will it damage important mental state?
2. Will it take longer to defer it than to do it?

If it's not worth thinking about, either let it go, or put a note of less than
twenty words in a reviewbox, so that you'll remember it once it is worth
dealing with.

If it is worth dealing with::

    Decide whether the action stands alone or is part of a project.

        If it is part of a project, decide whether it relates to any of your
        projects.

        If it is not, consider whether you care about the projects it impacts.

            If you do not, throw the action out. You're done.

            If you do, decide whether it's worth tracking the project formally,
            and continue with the triage process based on that.

    Guess how long the action will take.

    If you can do it faster than you can defer or delegate it, do so.

    Otherwise, defer it or delegate it.


Deferring Actions
-----------------

Everyone thinks of things they need to do later.

If you decide to defer an action, it belongs in one of two places:

1. A todo list
2. Your calendar

An action goes on your calendar *only* if the date/time it is done is intrinsic
to the action.

Otherwise, it belongs on a todo list.


Delegating Actions
------------------

Sometimes, it's better to ask someone else to do something rather than doing it
yourself.

To do that, you can ask them in person, or you can put something in one of
their inboxes.

If the act of delegating will take more than two minutes, you should defer delegating this action.

When you delegate, you should also add an item to a delegated actions list.

By doing so, you provide yourself with a concrete reminder of things you're
waiting for others to do. Regular review of your delegated actions will keep
you from being surprised by one that wasn't done.


Inbox Processing
----------------

The goal of inbox processing is to decide what to do with each new piece of
information, then to **take the first action that decision requires**.

Otherwise, your inbox becomes a tangled web of half-forgotten actions,
reference data, and unread information.

For each item in your inbox, in order::

    Read through it.

    For each action the item suggests, triage the possible action.

    If the item contains any date/time-specific info relevant to you, add it to
    your calendar.

    If the item contains anything worth having in your reference library,
    file it.

    If the item seems to be worth reviewing again at some point, put it in
    a reviewbox.

    If the item is no longer needed, discard it.

Note that a processed item may not go back in an inbox. The inbox is for new
inputs. If you think you'll need to look at this item again, put it in a
reviewbox (with annotations).


Processing Reviewboxes
----------------------

Reviewboxes only serve their purpose when you review their contents. For a
current project's reviewbox, once a week is a good minimum. For a general
reviewbox, you can probably let it go longer, but at least once a month is
probably necessary to reap any real benefits from it. Every two weeks would
probably be better.

Since you control what goes into the reviewbox, you know how overloaded it is -
if you toss some things in it through the course of a day, you might want to
take a few minutes at the end of the day to process them, while they're still
semi-fresh in your mind.

A reviewbox can be processed like an inbox, with one exception: it is
permissible to put items back in the reviewbox unaltered.

This is allowed because reviewboxes exist mainly to let things ferment while
your subconscious decides what to do with them.

Keeping a "times reviewed" counter of on any item you put back might be a good
way to keep yourself honest.

More complex ways to deal with reviewboxes are probably possible (and
probably a bad idea).


Project Review
--------------

Reviewing a project is meant to give you an idea of where it stands, and to
give you a chance to consider the bigger picture.

A review is just a quick skim through all of the following a project
has:

* Todo lists
* Delegated action lists
* Reviewboxes

accompanied by any updates to these files that seem appropriate.

Glance over deferred actions to get an idea of where you stand, what you
should be doing next, and what actions you may not have realized you needed.

See if you need to follow up on any delegated actions. Mostly you want to be
reminded they exist, and to catch any that have gone too long.

Reviewboxes you need to be careful with - it's easy to get sucked in if a lot has piled up. Still, occasionally something will click, and you'll be able to turn the review item into actions or a project.

A quick look through these should give you a passable sense of where the
project stands relative to the desired outcome that defines it.


Full Review
-----------

It's a good idea to look over all your current commitments regularly, so you
know where things stand and what you should be focusing on.

Once a week is probably about the right frequency. Your mind should be fresh
and your schedule clear. Try it with your morning beverage of choice on a day
off.

A full review entails:

* a project review for each current project
* a skim through your misc. deferred actions
* a skim through your misc. delegated actions
* a skim through your misc. reviewbox
* a glance over the calendar for the next week

It may be helpful to put full reviews on the calendar regularly, to block out a
space when you are committed to doing it.


Data Structures
===============


Following are several data structures that may be helpful in implementing the
above algorithms.


Action File
-----------

A text file containing a list of actions, formatted for use by Gina Trapani's
todo.sh script.

A line specifies an action. The line may use the following metadata fields::

    [priority ][creation-date] Action summary. [contexts]

where the fields are formatted as follows::

    priority: ([A-Z])
    creation-date: YYYY-MM-DD
    contexts: @context1 @context2 ...

For further details, read the docs_. Since we store completed actions in their
own file, and since each project gets its own files, the completion and
project fields are not used.

When you create an action file, you should hardlink it from the main Actions
directory.

The standard action files are:

* goals.txt, an outline of the project's goals.
* todo.txt, a todo list.
* delegated.txt, a delegated action list.
* review.txt, a reviewbox.
* done.txt, a list of finished actions.

(Note: Emacs users may find the built-in uniquify library helpful for making
buffer names usefully distinct. See section 16.7.1 of the Emacs manual for
details.)

.. _docs: https://github.com/ginatrapani/todo.txt-cli/wiki/The-Todo.txt-Format


Action Directory
----------------

An action directory holds action files specific to a project.

They should have their own instances of the standard action files.

Whenever an action directory is created, a corresponding directory should be
added to ~/actions, and the new action dir's contents should be hardlinked
from it. There is a script to do that; see the Actions Directory for details.

For collaborative projects that do not use this workflow, it may be
convenient to create an action directory inside the project directory and
exclude it from version control, so that you can apply it to your own tasks on
the project.


Actions Directory
-----------------

The actions directory implements the project list described in the Definitions
section.

It exists to make whole-system reviews easier, while still letting project
data stand alone.

It also contains general versions of the standard action files, for
miscellaneous actions that do not merit a standalone project.

To ensure it serves this purpose, when you create an action directory, make a
directory in here and hardlink the new action directory's contents from it. If
for some reason you have standalone action lists, hardlink them from here.

That isn't hard to handle manually, but it's easier with a script. A very
primitive one has been written, and lives at bin/actions.py. It doesn't even
have a usage statement yet - the 'setup' command will set up your environment
for using the script, while the 'new' command will create an action directory
and do the attendant housework.

In theory, the actions directory should enable the creation of tools that rely
on access to all actions.

Some such hypothetical tools:

* contextual action lister ("What did I want to do at the library?")
* Mobile device syncer (combine with contextual lister and GPS for epic win)
* Full review handler

The expected location of the actions directory is ~/actions.

Note: Emacs users may not know that by default, their editor will break
hardlinks on every save. See the Emacs docs on `backup copying`_.

.. _backup copying: http://www.gnu.org/software/emacs/manual/html_node/emacs/Backup-Copying.html

Current projects
----------------

Implement this any way you like. It's there for you.

A directory with symlinks to action directories at ~/actions/current would work
just fine, and might be useful in crafting those custom tools I hear so much
about.

# Concept: functions and code blocks

## Functions and Decorators

In the last chapter the following code was used:

``` python
@board.register
def on_setup(self):
    board.fps = 1
    board.speed = 3
```

* The second line defines a function that performs certain instructions (more on this later).

* In the first line, this function is given a decorator. This decorator "attaches" the function to the board. Whenever the system wants to call the function `board.on_setup`, the function you defined will be called.
  This way you can later define functions that react to arbitrary events, e.g. keystrokes, ...

## Indentation and code blocks

The third and fourth lines of the program code above are indented. This means that when called, the two indented lines will be called.

Code blocks are always used in Python to define when a particular branch in your program begins and when it ends. Everything that is indented the same distance belongs to a common code block.

## Coding standards How far should be indented?

The Python programming language itself does not define how far a code block should be indented, whether you use three, four or five characters does not matter - what matters is that all lines are indented *equally*.

However, there are certain coding standards in Python that programmers have agreed upon so that code always looks similar.

For example, it was agreed that code should always be indented 4 characters. You can of course handle this differently for yourself - but at the latest when you work in a team, it is helpful to stick to such conventions.

In Python functions and conventions are defined in so called PEPs ("Python Enhancement Proposal). Style guides can be found e.g. in [PEP 8](https://www.python.org/dev/peps/pep-0008/).

Besides the indentation you will find much more there, e.g. you write `a = a + 3` instead of `a=a+3`, because the former is easier to read. The programming language does not force you to do this, but this way the code is easier to read for other programmers.

Many modern editors can help you write **clean** code by auto-formatting and linting.


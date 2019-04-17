GUI elements
============

You can offer different GUI elements to your miniworld. 

Some of the GUI elements help you as designer and programmer, others you can integrate as user interface directly into your miniworld.


### The Toolbar

The toolbar is a list of buttons.

You initialize a new toolbar like this:

```
        toolbar = self.window.add_container(Toolbar(), dock="right")
        toolbar.add_widget(ToolbarButton("Spin"))
```

You can add the following widgets at this time:

  * ToolbarButton: A button. When you click on the button, the Event button will be called. 
  For data the text of the button is provided (in the example above e.g. "Spin").
  
  * A label is used to display text.

See also the example [spinning_wheel](https://github.com/asbl/miniworldmaker/blob/master/examples/gui/spinning_wheel.py) on Github.
  
![_images/roboanimation.gif](_images/spinning_wheel.gif)

### The console

The console is used to output information.

The console is initialized as follows.

```
        self.console = self._window.add_container(Console(), "bottom")
```

Then you can write output to the console as follows:
```
                self.board.console.print("You're lighting the fire.")
```

### The Event Console

The Event bar is a special console that outputs events that are sent.
You can initialize the console as follows:

```
        self.window.add_container(event_console, dock="right", size=400)
```

You will find that the output is quickly confusing. So you can decide what kind of events you want the console to respond to.
```
        event_console.register_events = {"key pressed"}
```

This line of code means, for example, that the console only responds to the key_pressed event. 

### The action bar

With the Action Bar you can analyze the program flow by running the program step by step.
This is how you initialize the Actionbar:

```
        self.window.add_container(ActionBar(self), dock="bottom")
```

### The ActiveActorToolbar

The ActiveActorToolbar shows you all current information about an actor (position, direction, borders touched, ...).

You can initialize the token toolbar as follows:

```
        actor_toolbar = ActiveActorToolbar(self)
        self.window.add_container(actor_toolbar, dock="right", size=400)
```

The actor that is displayed with the toolbar can be selected by clicking on the corresponding actor.
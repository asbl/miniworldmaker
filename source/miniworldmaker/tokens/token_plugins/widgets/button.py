import miniworldmaker.tokens.token_plugins.widgets.buttonwidget as widget


class Button(widget.ButtonWidget):
    def on_clicked_left(self, mouse_pos):
        """This event is called when the button is clicked -

        By default, a message with the button text is then sent to the board.

        Examples:

            Send a event on button-click:

            .. code-block:: python

                toolbar = Toolbar()
                button = ToolbarButton("Start Rocket")
                toolbar.add_widget(button)
                board.add_container(toolbar, "right")

                @board.register
                def on_message(self, message):
                    if message == "Start Rocket":
                        rocket.started = True
        """
        self.send_message(self.value)


class ToolbarButton(Button):
    # deprecated
    pass

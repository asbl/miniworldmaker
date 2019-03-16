import easygui
import sys

class GUIGrid():
    """
    Das GUI-Grid erlaubt es Pop-Up Fenster mit GUI Elementen einzublenden.
    """

    def button_box(self, message: str, choices: list) -> str:
        """
        Zeigt ein Pop-Up mit selbst gewählten Buttons an.

        Parameters
        ----------
        message : int
            Die Nachricht, die angezeigt werden soll.
        choices : list
            Texte, die in Auswahlmöglichkeiten übersetzt werden.

        Returns
        -------
        str
            Die gewählte Antwortmöglichkeit als Text.

        """
        reply = easygui.buttonbox(message, choices=choices)
        return reply

    def integer_box(self, message: str, title="", min: int = 0, max: int = sys.maxsize, image=None) -> str:
        """
        Zeigt ein Pop-Up zur Eingabe einer Zahl ein.

        Parameters
        ----------
        message : int
            Die Nachricht, die angezeigt werden soll
        title: String
            Der Fenster-Titel.
        min : int
            Der minimale Wert
        max : int
            Der maximale Wert
        image : str
            Optional: Pfad zu einem Bild.


        Returns
        -------
        int
            Der Wert, der eingegeben wurde.

        """
        reply = easygui.integerbox(message, title=title, lowerbound=min, upperbound=max, image=image)
        return reply

    def string_box(self, message: str, default="", title="", strip=False, image=None) -> str:
        """
        Zeigt ein Pop-Up zur Eingabe einer Zahl ein.

        Parameters
        ----------
        message : int
            Die Nachricht, die angezeigt werden soll.
        title: String
            Der Fenster-Titel.
        strip : bool
            Sollen Whitespaces (Leerzeichen) aus dem String herausgelöscht werden?
        image : str
            Optional: Pfad zu einem Bild.

        Returns
        -------
        str
            Der eingegebene Wert als String.
        """
        reply = easygui.enterbox(message, title=title, default=default, strip=strip, image=image)
        return reply

    def message_box(self, message):
        """
        Zeigt eine Nachrichtenbox
        Parameters
        ----------
        message
            Die Nachricht, die angezeigt werden soll.

        Returns
        -------

        """
        easygui.msgbox(message)
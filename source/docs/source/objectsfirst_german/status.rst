Status: Spielstand/Spielende/Levels
***********************************

Spielende / Levelwechsel
========================

Zum Spielende/Levelwechsel sind folgendes typische Aktionen:

* Das Spielfeld löschen
* Das Spielfeld anhalten.

Dafür gibt es folgende Befehle:

* `board.stop()`: Stoppt das Spielfeld. Es werden keine Aktionen mehr ausgeführt und keine Events abgefragt.
* `board.start()`: Dies hebt einen Stop-Befehl auf.
* `board.is_running`:  Mit dieser Variable kannst du den Status des Spielfelds abfragen.
* `board.clear()`: Die Funktion entfernt alle Figuren vom Spielfeld.
* `board.reset()`: Die Funktion löscht das aktuelle Spielfeld und erstellt ein neues Spielfeld mit allen Figuren so wie sie in `board.on_setup()` erzeugt wurden.


Status/Punktestand
==================

* Oft willst du den aktuellen Punktestand oder ähnliches anzeigen.

Hierfür bietet dir der **miniworldmaker** spezielle Tokens an, z.B. TextTokens oder NumberTokens.

  
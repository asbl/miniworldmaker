Ereignisse
===========

Events sind ein zentrales Konept des Miniworldmakers:

  * Mit Events kannst du Eingaben abfragen (z.B. Mausklicks oder Tastatureingaben)
  
  * Mit Events können Objekte miteinander kommunizieren (z.B. über Nachrichten)

### Ein Ereignis registrieren

Damit das Board oder ein Player auf ein Ereignis reagiert, muss dieses registriert werden.
Dies funktioniert genauso wie bei der act()-Methode:

```
@player.register
def on_key_down_w(self):
    self.move()
 ```
 
 Hier wird die Methode **on_key_down_w** registriert, die überprüft, ob die Taste w gedrückt wurde.
 Sobald dies registriert wird, bewegt sich das Token player um einen Schritt nach vorne.
 
 --> Mehr Infos über Richtungen: [Events](../key_concepts/events.md)
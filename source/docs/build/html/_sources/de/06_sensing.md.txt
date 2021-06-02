Kollisionen und Sensoren
=================

Zusätzlich zu den Reaktionen auf Ereignisse können Tokens auch über Sensoren den Status des Boards überprüfen und ob z.B. andere Tokens sich an gleicher Stelle befinden.

Dies geht z.B. mit folgender Funktion:

### Ein Objekt aufspüren

Du kannst ein Token folgendermaßen aufspüren:

```
@player.register
def on_sensing_token(self, token):
    print("Damage!!!!!")
    self.remove()
```

> ➥ Mehr über Sensoren: [Key Concept: Sensors](../key_concepts/sensors.md)
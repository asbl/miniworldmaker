Kollisionen und Sensoren
************************

Zusätzlich zu den Reaktionen auf Ereignisse können Tokens auch über **Sensoren** überprüfen, ob sich z.B. andere Tokens an der gleichen Stelle befinden.

Ein Objekt aufspüren
====================

Ein `Token` kann ein anderes `Token` am selben Ort folgendermaßen aufspüren:

.. code-block:: python

  @player.register
  def on_sensing_token(self, other):
      print("Damage!!!!!")
      self.remove()

Was passiert hier?
------------------

* Die Funktion `on_sensing_token` wird dann aufgerufen, wenn das Token ein anderes Objekt am selben Ort aufspürt. 
* Der Parameter `other` ist ein Verweis auf das gefundene Objekt, so dass du direkt auf Attribute und Methoden dieses Objektes zugreifen kannst (z.B. mit `other.move()`)

Vergleichen mit gefundenem Objekt
==================================

Oft soll eine Aktion nur ausgeführt werden, wenn ein *bestimmtes* Objekt aufgespürt wird. 

Dies geht z.B. so:

.. code-block:: python
  :emphasize-lines: 1,5,6
  :lineno-start: 1

  player 2 = miniworldmaker.Token()
  #...
  @player1.register
  def on_sensing_token(self, other):
      global player2
      if other == player2:
        print("I found you, player2!")


Der Vergleich in Zeile 6 überprüft, ob das Objekt **dasselbe** Objekt ist wie `player2`. 

.. note:: 
   **Exkurs Globale Variablen**: Normalerweise sind Variablen nur innerhalb einer Methode bekannt, damit z.B. verhindert wird, 
   dass es zu Seiteneffekten kommt, wenn man an verschiedenen Stellen auf die gleiche Variable zugreift. 
   
   Der Ansatz mit dem hier auf Variablen aus anderen Programmteilen zugegriffen wird ist zwar einfach und intuitiv - 
   Später wird man aber versuchen dies zu vermeiden.

Grenzen des Spielfelds überprüfen
---------------------------------

Du kannst auch überprüfen, ob eine Spielfigur an den Grenzen des Spielfelds ist (oder darüber hinaus):

*Ist die Figur nicht auf dem Spielfeld?*

.. code-block:: python

   @player3.register
   def on_sensing_not_on_board(self):
     print("Warning: I'm not on the board!!!")


*Ist die Figur an den Grenzen des Spielfelds?*

.. code-block:: python

  @player4.register
  def on_sensing_borders(self, borders):
    print("Borders are here!", str(borders))


Befindet sich eine Spielfigur an der Position (0,0) wird folgendes ausgegeben: `Borders are here! ['right', 'top']`

FAQ
====
  * Meine Kollisionen werden nicht erkannt, was kann ich tun?
    * Teste zunächst, ob die Methode überhaupt aufgerufen wird, z.B. mit:

    .. code-block:: python
    
      @player.register
      def on_sensing_token(self, token):
        print(token)
        ...
    

    Wenn die `print`-Anweisung nicht aufgerufen wird, dann funktioniert der Sensor nicht.


Ausblick
=========


* --> Mehr Informationen. Siehe :doc:`Key Concepts: Sensors <../key_concepts/sensors>`.
* Die Objekte können auf unterschiedliche Art aufgespürt werden. 
  Dies kann über die Eigenschaft `collision_type` des aufspürenden Objekts eingestellt werden, 
  z.B. "mask" für einen pixelgenauen Vergleich oder 'rect' wenn nur die umschließenden Rechtecke verglichen werden.
  




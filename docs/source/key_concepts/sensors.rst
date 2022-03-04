Sensors
*******

With sensors, tokens can sense their environment.

Listeners
=========

Register any of these listener methods, to catch a sensor-event:

sensing_on_board
-----------------

.. automethod:: miniworldmaker.tokens.token.Token.on_sensing_on_board
   :noindex:

sensing_not_on_board
--------------------

.. automethod:: miniworldmaker.tokens.token.Token.on_sensing_not_on_board
   :noindex:

sensing_borders
---------------

.. automethod:: miniworldmaker.tokens.token.Token.on_sensing_borders
   :noindex:

token
---------------

.. automethod:: miniworldmaker.tokens.token.Token.on_sensing_token
   :noindex:


Active Sensors
===============

sensing_token
-------------

.. automethod:: miniworldmaker.tokens.token.Token.sensing_token
   :noindex:

sensing_tokens
--------------

.. automethod:: miniworldmaker.tokens.token.Token.sensing_tokens
   :noindex:

sensing_borders
---------------

.. automethod:: miniworldmaker.tokens.token.Token.sensing_borders
   :noindex:


sensing specific border
-----------------------

  * **sensing_left_border(distance)**, 
  * **sensing_right_border(distance)**, 
  * **sensing_top_border(distance)**, 
  * **sensing_bottom_border(distance)**
  
    Returns True if token is sensing the border (when moving distance steps forward)
    
sensing_colors
--------------

.. automethod:: miniworldmaker.tokens.token.Token.sensing_colors
   :noindex:

sensing_point
-------------

.. automethod:: miniworldmaker.tokens.token.Token.sensing_point
   :noindex:
import miniworldmaker as mwm


class MyBoard(mwm.TiledBoard):
    def on_setup(self):
        self.add_image("images/rasen.jpg")
        player1 = Player((4, 4))
        ball = Ball((6, 6))


class Player(mwm.Token):
    def on_setup(self):
        self.add_image("images/player.png")
        self.orientation = -90

    def on_key_down(self, keys):
      print(keys)
      if 'A' in keys:
        self.direction = "left"
      elif 'S' in keys:
        self.direction = "down"
      elif 'W' in keys:
        self.direction = "up"
      elif 'D' in keys:
        self.direction = "right"
      self.move()

    def get_event(self, event, data):
      print(event, data)

    def on_sensing_ball(self, ball):
      ball.direction = self.direction
      ball.move(2)

class Ball(mwm.Token):
  def on_setup(self):
    self.add_image("images/ball.png")

def main():
    myboard = MyBoard(10, 10, 40, 0)
    myboard.show()

if __name__ == '__main__':
    main()




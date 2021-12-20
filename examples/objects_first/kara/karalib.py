import miniworldmaker

class KaraBoard(miniworldmaker.TiledBoard):
   
    def read_file(self, filename):
        with open(filename, 'r') as level:
            max_length = 0 # columns
            lines = list()
            for row_number, line in enumerate(level):
                lines.append(line)
                if len(line)>max_length:
                    max_length = len(line)
            return lines, max_length
                    
    def on_setup(self):
        self.speed = 30
        self.storages = []
        self.boxes = []
        lines, max_length = self.read_file("level01.lvl")
        # create board
        player = '@'
        player_on_storage = '+'
        box = '$'
        box_on_storage = '*'
        storage = '.'
        wall = '#'
        empty = ' '
        self.size = len(lines), max_length
        self.add_background((100,200,100,255))
        for row_number, line in enumerate(lines):
            for column_number, char in enumerate(line):
                if char == box:
                    Box((row_number, column_number))            
                if char == wall:
                    Wall((row_number, column_number))
                if char == storage:
                    Storage((row_number, column_number))
                if char == player:
                    self.kara = Kara((row_number, column_number))
                if char == player_on_storage:
                    Storage((row_number, column_number))
                    self.kara = Kara((row_number, column_number))
                    
    def act(self):
        all_boxes_on_storage = True
        for box in self.boxes:
            if not box.on_storage:
                all_boxes_on_storage = False
        for box in self.boxes:
            print(box, box.on_storage)
        if all_boxes_on_storage:
            print("All boxes are on storage")
            
    
class Kara(miniworldmaker.Token):
    def on_setup(self):
        self.add_costume("images/kara.png")
        self.orientation = -90
        
    def push(self, method):
        tokens = self.sensing_tokens()
        if tokens:
            for token in tokens:
                if isinstance(token, Box):
                    box = token
                    getattr(box, method)()
                    tokens = box.sensing_tokens()
                    for next_token in tokens:
                        obstacle = next_token
                        if isinstance(obstacle, Wall) or (isinstance(obstacle, Box) and obstacle != box):
                            self.move_back()
                            box.move_back()
                            return 
    
    def check_for_wall(self):
         tokens = self.sensing_tokens()
         for next_token in tokens:
             if isinstance(next_token, Wall):
                 self.move_back()
                 print("Can't move - There is a wall!")
    
    def move_right(self):
        super().move_right(1)
        self.push("move_right")

    def move_up(self):
        super().move_up(1)
        self.push("move_up")

    def move_left(self):
        super().move_left(1)
        self.push("move_left")

    def move_down(self):
        super().move_down(1)
        self.push("move_down")
        
        
class Storage(miniworldmaker.Token):
    def on_setup(self):
        self.add_costume("images/leaf.png")
        self.board.storages.append(self)
        self.filled = False
        

class Box(miniworldmaker.Token):
    def on_setup(self):
        self.add_costume("images/mushroom.png")
        self.board.boxes.append(self)
        self.costume.is_rotatable = False
        self.layer = 5
        self.on_storage = False
    
    def on_sensing_storage(self, storage):
        self.on_storage = True
        
    def on_not_sensing_storage(self):
        self.on_storage = False

class Wall(miniworldmaker.Token):
    def on_setup(self):
        self.add_costume("images/tree.png")

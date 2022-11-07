class Color():
    def __init__(self,value):
        self.color_tuple = value

    @classmethod
    def create(cls, value):
        if type(value) == tuple:
            if len(value) == 1:
                value = (value[0], value[0], value[0])
        if type(value) in [int, float]:
                value = (value, value, value)
        return cls(value)
        
    def get(self):
        return self.color_tuple
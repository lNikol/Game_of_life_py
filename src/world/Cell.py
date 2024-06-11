class Cell:
    def __init__(self, y=-1, x=-1, organism=None, is_hex=False):
        self.__is_hex = is_hex
        self.__org = organism
        self.__y = y
        self.__x = x
        self.__hexagon = None

    def set_org(self, organism):
        self.__org = organism
        if(self.__is_hex):
            size = 40
        return None
    def get_pos(self):
        return self.__y, self.__x
    def get_org(self):
        return self.__org



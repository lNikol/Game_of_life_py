class Cell:
    def __init__(self, y=-1, x=-1, is_hex=False, organism=None):
        self.__is_hex = is_hex
        self.__org = organism
        self.__y = y
        self.__x = x
        self.__hexagon = None

    def set_org(self, organism, is_hex=False):
        self.__org = organism
        if self.__is_hex:
            size = 40
        return None

    def get_position(self):
        return self.__y, self.__x

    def get_org(self):
        return self.__org

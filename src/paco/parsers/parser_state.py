class ParserState(object):

    def __init__(self, pos : int, text : str) -> None:
        self.target = list(text)
        self.pos = pos
        self.text = text

    def in_bound(self, ind = None) -> bool:
        if ind is None:
            return (len(self.target) > self.pos)
        return (len(self.target) > ind)
    
    def __repr__(self) -> str:
        items = ( f" {k} : {v!r}" for k, v in self.__dict__.items())
        return "{{\n{} \n}}".format(",\n".join(items))
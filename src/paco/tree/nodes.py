from typing import Any

class Node(object):

    def __init__(self, ignore = False) -> None:
        self.ntype = "Node"
        self.children = list()
        self._data = None
        self._ignore = ignore

    def get_child(self, ind : int):
        return self.children[ind]
    
    def add_child(self, child):
        if child.not_ignored():
            self.children.append(child)
    
    def add_children(self, *children):
        for child in children:
            if child.not_ignored():
                self.children.append(child)

    def __getitem__(self, key):
        return self.children[key]
    
    def __setitem__(self, key, child):
        self.children[key] = child

    def is_an(self, node_type) -> bool:
        return isinstance(self, node_type)

    def ignore(self) -> None:
        self._ignore = True

    def is_ignored(self) -> bool:
        return self._ignore
    
    def not_ignored(self) -> bool:
        return not self._ignore

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, to_set):
        self._data = to_set

    def __str__(self, level=0) -> str:
        indent = level*' '
        str_type = indent + 'type : ' + self.ntype + ',\n'
        ret = indent + '{\n' + str_type
        if self.data is not None:
            ret += indent + 'data : ' + str(self.data) + ',\n'
        if len(self.children) != 0:
            ret += indent + 'children :\n'
            for child in self.children:
                ret += child.__str__(level + 4) + ',\n'
        return ret + indent + '}'
    
class Parsed(Node):

    def __init__(self, start : int, end : int, data = None, ntype = "Parsed", ignore = False) -> None:
        super().__init__(ignore)
        self.ntype = ntype
        self.start = start
        self.end = end
        self._data = data
    
    def __str__(self, level=0) -> str:
        indent = level*' '
        str_start = indent + 'start : ' + str(self.start) + ',\n'
        str_end = indent + 'end : ' + str(self.end) + ',\n'
        str_type = indent + 'type : ' + self.ntype + ',\n'
        ret = indent + '{\n' + str_type + str_start + str_end
        if self.data is not None:
            ret += indent + 'data : ' + str(self.data) + ',\n'
        if len(self.children) != 0:
            ret += indent + 'children :\n'
            for child in self.children:
                ret += child.__str__(level + 4) + ',\n'
        return ret + indent + '}'


class Error(Node):

    def __init__(self, start : int, end : int, er_msg : str, p, ntype = "Error") -> None:
        super().__init__(False)
        self.ntype = ntype
        self.start = start
        self.end = end
        self.parser = p
        self.er_str = f"@{self.start},{self.end}: {er_msg}."
    
    def set_error(self, msg):
        self.er_str = msg
    
    def get_error(self):
        return self.er_str

    def log_error(self):
        print(self.er_str)

    def get_parser(self):
        return self.parser    
    
    def __str__(self, level=0) -> str:
        indent = level*' '
        str_start = indent + 'start : ' + str(self.start) + ',\n'
        str_end = indent + 'end : ' + str(self.end) + ',\n'
        str_type = indent + 'type : ' + self.ntype + ',\n'
        str_err = indent + 'error : ' + self.er_str + ',\n'
        ret = indent + '{\n' + str_type + str_start + str_end + str_err
        return ret + indent + '}'

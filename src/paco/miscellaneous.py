from .combinators import (Regex)

letters = Regex("[a-zA-Z]+")
letter = Regex("[a-zA-Z]")
numbers = Regex("[0-9]+")
number = Regex("[0-9]")
optSpace = Regex(" *").ignore()
spacep = Regex(" +").ignore()
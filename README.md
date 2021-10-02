# Paco

> This is a small library that implements various parser combinators. It is written out of curiosity to learn parser combinators and use them to parse user defined grammars. Parser combinators are capable of recognizing LL(0) grammars and the limitation about these parsers is that they cannot parse left recursive rules. So if you want to be able to parse left recursive grammars like; ``E -> E + T; T -> T * F; F -> (E) | "id"`` you have to eliminate left recursion with the [Elimination of Left Recursion Algorithm](https://www.wikiwand.com/en/Left_recursion#/Removing_left_recursion).

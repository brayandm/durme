from typing import Any, Dict

import ply.lex as lex  # type: ignore


class Lexer:
    def __init__(self) -> None:
        self.tokens = [
            "INT",
            "ID",
            "ASSIGN",
            "NUMBER",
            "IF",
            "LPAREN",
            "RPAREN",
            "LBRACE",
            "RBRACE",
            "LT",
            "INCREMENT",
            "SEMICOLON",
        ]
        self.reserved: Dict[str, str] = {"int": "INT", "if": "IF"}
        self.t_ignore = " \t"
        self.t_ASSIGN = r"="
        self.t_LPAREN = r"\("
        self.t_RPAREN = r"\)"
        self.t_LBRACE = r"\{"
        self.t_RBRACE = r"\}"
        self.t_LT = r"<"
        self.t_INCREMENT = r"\+\+"
        self.t_SEMICOLON = r";"

        self.lexer = lex.lex(module=self)

    def t_ID(self, t: Any) -> Any:
        r"[a-zA-Z_][a-zA-Z0-9_]*"
        t.type = self.reserved.get(t.value, "ID")
        return t

    def t_NUMBER(self, t: Any) -> Any:
        r"\d+"
        t.value = int(t.value)
        return t

    def t_newline(self, t: Any) -> None:
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_error(self, t: Any) -> None:
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def input(self, data: str) -> None:
        self.lexer.input(data)

    def token(self) -> Any:
        return self.lexer.token()

    def save_tokens(self, output_file: str) -> None:
        """Save the tokens to a file."""
        with open(output_file, "w") as f:
            while token := self.token():
                f.write(f"{token}\n")

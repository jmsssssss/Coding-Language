class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.current = 0

    def tokenize(self):
        while self.current < len(self.code):
            char = self.code[self.current]

            # Space skip
            if char.isspace():
                self.current += 1
                continue

            # String Processing
            if char == '"':
                self.current += 1
                start = self.current
                while self.current < len(self.code) and self.code[self.current] != '"':
                    self.current += 1
                if self.current >= len(self.code):
                    raise ValueError(f"Unterminated string starting at index {start}")
                self.tokens.append(("STRING", self.code[start:self.current]))
                self.current += 1
                continue

            # Keyword or Identifier Processing
            if char.isalpha() or char == "@":  # '@' 처리 포함
                start = self.current
                while self.current < len(self.code) and (self.code[self.current].isalnum() or self.code[self.current] in {"@", "_"}):
                    self.current += 1
                self.tokens.append(("IDENTIFIER", self.code[start:self.current]))
                continue

            # Number Processing
            if char.isdigit():
                start = self.current
                while self.current < len(self.code) and self.code[self.current].isdigit():
                    self.current += 1
                self.tokens.append(("NUMBER", self.code[start:self.current]))
                continue

            # Colon Processing
            if char == ":":
                self.tokens.append(("EQUALS", ":"))
                self.current += 1
                continue

            # Pipe Processing
            if char == "|":
                self.tokens.append(("PIPE", "|"))
                self.current += 1
                continue

            # Error Code
            raise ValueError(f"Unexpected character: {char}")

        return self.tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
    
    def consume(self, expected_type):
        token = self.tokens[self.current]
        if token[0] != expected_type:
            raise ValueError(f"Expected { expected_type }, but got {token[0]}")
        self.current += 1
        return token

    def statement(self):
        token = self.tokens[self.current]
        if token[0] == "IDENTIFIER":
            if token[1] == "Const":
                self.current += 1
                const_name = self.consume("IDENTIFIER")[1]
                self.consume("EQUALS")
                value_token = self.tokens[self.current]
                self.current += 1
                if value_token[0] == "NUMBER":
                    return {"type": "assignment", "name": const_name, "value": int(value_token[1])}
                elif value_token[0] == "STRING":
                    return {"type": "assignment", "name": const_name, "value": value_token[1]}
                else:
                    raise ValueError(f"Invalid value for Const at index {self.current}: {value_token}")
            elif token[1] == "@Emit":
                self.current += 1
                self.consume("PIPE")
                return {"type": "print", "value": self.consume("STRING")[1]}

    def parse(self):
        ast = []
        while self.current < len(self.tokens):
            ast.append(self.statement())
        return ast
    
class Interpreter:
    def __init__(self):
        self.variables = {}

    def execute(self, ast):
        for statement in ast:
            if statement["type"] == "assignment":
                self.variables[statement["name"]] = statement["value"]
            elif statement["type"] == "print":
                print(statement["value"])
                continue
        return self.variables
    

if __name__ == "__main__":
    with open('main.jms', 'r') as file:
        code = file.read()

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter = interpreter.execute(ast)

    print(tokens)
    print('---------------')
    print(ast)

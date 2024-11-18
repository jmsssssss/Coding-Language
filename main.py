class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.current = 0

    def tokenize(self):
        while self.current < len(self.code):
            char = self.code[self.current]

            # 공백 건너뛰기
            if char.isspace():
                self.current += 1
                continue

            # 문자열 처리
            if char == '"' or char == "'":
                self.current += 1
                start = self.current
                while self.current < len(self.code) and self.code[self.current] != '"':
                    self.current += 1
                self.tokens.append(("STRING", self.code[start:self.current]))
                self.current += 1
                continue

            # 키워드 및 변수 처리
            if char.isalpha():
                start = self.current
                while self.current < len(self.code) and self.code[self.current].isalnum():
                    self.current += 1
                self.tokens.append(("IDENTIFIER", self.code[start:self.current]))
                continue

            # 숫자 처리
            if char.isdigit():
                start = self.current
                while self.current < len(self.code) and self.code[self.current].isdigit():
                    self.current += 1
                self.tokens.append(("NUMBER", self.code[start:self.current]))
                continue

            # 기타 처리
            if char == "=":
                self.tokens.append(("EQUALS", "="))
                self.current += 1
                continue

            # 인식하지 못한 문자
            raise ValueError(f"Unexpected character: {char}")

        return self.tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        ast = []
        while self.current < len(self.tokens):
            ast.append(self.statement())
        return ast

    def statement(self):
        token = self.tokens[self.current]

        if token[0] == "IDENTIFIER":
            if token[1] == "print":
                self.current += 1
                return {"type": "print", "value": self.consume("STRING")[1]}
            elif token[1] == "":
                self.current += 1
                var_name = self.consume("IDENTIFIER")[1]
                self.consume("EQUALS")
                value = self.consume("NUMBER")[1]
                return {"type": "assignment", "name": var_name, "value": int(value)}
            elif token[1] == "add":
                self.current += 1
                left = self.consume("IDENTIFIER")[1]
                right = self.consume("IDENTIFIER")[1]
                return {"type": "add", "left": left, "right": right}
        raise ValueError(f"Unexpected token: {token}")

    def consume(self, expected_type):
        token = self.tokens[self.current]
        if token[0] != expected_type:
            raise ValueError(f"Expected {expected_type}, got {token[0]}")
        self.current += 1
        return token

class Interpreter:
    def __init__(self):
        self.variables = {}

    def execute(self, ast):
        for node in ast:
            if node["type"] == "print":
                print(node["value"])
            elif node["type"] == "assignment":
                self.variables[node["name"]] = node["value"]
            elif node["type"] == "add":
                left = self.variables.get(node["left"], 0)
                right = self.variables.get(node["right"], 0)
                print(left + right)

if __name__ == "__main__":
    # main.ms 파일 읽기
    with open("main.jms", "r") as file:
        code = file.read()

    # 단계별 실행
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)

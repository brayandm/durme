from modules.lexer import Lexer  # type: ignore
from modules.parser import Parser  # type: ignore
from modules.transpiler import Transpiler  # type: ignore

if __name__ == "__main__":
    input_code = """
    int a = 3;
    if (a < 7) {
        a++;
    }
    """
    lexer = Lexer()
    parser = Parser(lexer)
    ast = parser.parse(input_code)

    if ast is None:
        raise Exception("Error: The analysis process failed.")
    else:
        print("AST: generated successfully.")

    transpiler = Transpiler()
    cpp_code = transpiler.transpile(ast)

    print("Generated C++ code:")
    print(cpp_code)

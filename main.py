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
    lexer.input(input_code)
    lexer.save_tokens("debug/tokens.out")

    parser = Parser(lexer)
    ast = parser.parse(input_code)

    if ast is None:
        raise Exception("Error: The analysis process failed.")
    else:
        print("AST: generated successfully.")
        with open("debug/ast.out", "w") as ast_file:
            ast_file.write(str(ast))

    transpiler = Transpiler()
    cpp_code = transpiler.transpile(ast)

    print("Generated C++ code:")
    print(cpp_code)

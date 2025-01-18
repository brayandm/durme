from modules.parser import parser  # type: ignore
from modules.transpiler import transpile_ast  # type: ignore

if __name__ == "__main__":
    input_code = """
    int a = 3;
    if (a < 7) {
        a++;
    }
    """
    ast = parser.parse(input_code)
    cpp_code = transpile_ast(ast)
    print("Generated C++ code:")
    print(cpp_code)

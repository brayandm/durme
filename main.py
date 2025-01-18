import argparse
import os

from modules.lexer import Lexer  # type: ignore
from modules.parser import Parser  # type: ignore
from modules.transpiler import Transpiler  # type: ignore


def main(input_file: str, output_file: str, debug_dir: str) -> None:
    with open(input_file, "r") as file:
        input_code = file.read()

    lexer = Lexer()
    lexer.input(input_code)
    lexer.save_tokens(f"{debug_dir}/tokens.out")

    parser = Parser(lexer)
    ast = parser.parse(input_code)

    if ast is None:
        raise Exception("Error: The analysis process failed.")
    else:
        print("AST: generated successfully.")
        with open(f"{debug_dir}/ast.out", "w") as ast_file:
            ast_file.write(ast.to_string())

    transpiler = Transpiler()
    cpp_code = transpiler.transpile(ast)

    print("Generated C++ code:")
    with open(output_file, "w") as cpp_file:
        cpp_file.write(cpp_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process and transpile a custom language to C++."
    )
    parser.add_argument("input", type=str, help="Path to the input file.")
    parser.add_argument(
        "output", type=str, help="Path to the output C++ file."
    )
    parser.add_argument(
        "--debug",
        type=str,
        default="debug",
        help="Directory to store debug information (tokens and AST).",
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise Exception("Error: The input file does not exist.")

    if not os.path.exists(args.output):
        os.makedirs(os.path.dirname(args.output))

    if not os.path.exists(args.debug):
        os.makedirs(args.debug)

    main(args.input, args.output, args.debug)

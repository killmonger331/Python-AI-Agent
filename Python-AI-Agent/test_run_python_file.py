from functions.run_python_file import run_python_file

def print_test(title, result):
    print(f"\n=== {title} ===")
    print(result)

def main():
    print_test(
        "Run calculator main.py (no args)",
        run_python_file("calculator", "main.py")
    )
    print_test(
        "Run calculator main.py with args",
        run_python_file("calculator", "main.py", ["3 + 5"])
    )
    print_test(
        "Run calculator tests.py",
        run_python_file("calculator", "tests.py")
    )
    print_test(
        "Attempt to run file outside working directory",
        run_python_file("calculator", "../main.py")
    )
    print_test(
        "Run nonexistent file",
        run_python_file("calculator", "nonexistent.py")
    )
    print_test(
        "Run non-Python file",
        run_python_file("calculator", "lorem.txt")
    )

if __name__ == "__main__":
    main()

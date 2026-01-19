from functions.write_file import write_file

def run_tests():
    print("Test 1:")
    result = write_file(
        "calculator",
        "lorem.txt",
        "wait, this isn't lorem ipsum"
    )
    print(result)
    print()

    print("Test 2:")
    result = write_file(
        "calculator",
        "pkg/morelorem.txt",
        "lorem ipsum dolor sit amet"
    )
    print(result)
    print()

    print("Test 3:")
    result = write_file(
        "calculator",
        "/tmp/temp.txt",
        "this should not be allowed"
    )
    print(result)
    print()


if __name__ == "__main__":
    run_tests()

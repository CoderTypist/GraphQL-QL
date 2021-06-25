
def print_file(file_path: str) -> None:

    with open(file_path, 'r') as file:

        line = file.readline()

        while line:
            line = line.rstrip()
            print(line)
            line = file.readline()


def str_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return ''.join(file.readlines())

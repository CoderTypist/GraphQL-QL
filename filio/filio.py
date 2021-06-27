import re


def print_file(file_path: str) -> None:

    with open(file_path, 'r') as file:

        line = file.readline()

        while line:
            line = line.rstrip()
            print(line)
            line = file.readline()


def str_file(file_path: str, l_strip = False, l_omit: str = None, l_omit_strip=True) -> str:

    '''
    :param file_path: file to read in text from
    :param l_strip: strip whitespace from the beginning of each line
    :param l_omit: do not include lines that start with l_omit
    :param l_omit_strip: do not include whitespace when determining if a line starts with l_omit
    :return: str containing all text in a file
    '''

    with open(file_path, 'r') as file:

        text = None
        line = file.readline()

        while line:

            if l_strip:
                line = line.lstrip()

            # omit lines that start with l_omit
            if l_omit:

                start_str = r"^{}".format(l_omit)
                match_line = line

                # remove leading whitespace temporarily before finding match
                if l_omit_strip:
                    match_line = match_line.lstrip()

                m = re.match(start_str, match_line)

                if m:
                    line = file.readline()
                    continue

            if text:
                text += line
            else:
                text = line

            line = file.readline()

        return text

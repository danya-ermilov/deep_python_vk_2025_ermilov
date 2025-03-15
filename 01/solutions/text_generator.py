def file_line_generator(file, search_words, stop_words):
    search_words = {word.lower() for word in search_words}
    stop_words = {word.lower() for word in stop_words}

    if isinstance(file, str):
        with open(file) as f:
            yield from process_file(f, search_words, stop_words)
    else:
        yield from process_file(file, search_words, stop_words)


def process_file(file, search_words, stop_words):
    for line in file:
        words_in_line = set(line.lower().split())

        if words_in_line & stop_words:
            continue

        if words_in_line & search_words:
            yield line.rstrip()


if __name__ == "__main__":
    filename = "text.txt"

    search_words = ["роза", "лапа"]

    stop_words = ["азора", "упала"]

    for line in file_line_generator(filename, search_words, stop_words):
        print(line)

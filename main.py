from parsers.met.met_parser import METParser


if __name__ == '__main__':
    registered_parsers = [METParser()]
    for parser in registered_parsers:
        parser.start()

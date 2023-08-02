from configparser import ConfigParser
import os


def config(filename="database.ini", section="postgresql") -> dict:
    """
    Конвертирует раздел ini файла в словарь
    """
    # create a parser
    file = os.path.join(os.path.dirname(__file__), filename)
    parser = ConfigParser()
    # read config file
    parser.read(file)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, file))
    return db

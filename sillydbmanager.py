import os, copy, json, csv

license = """
Copyright © 2023 PanForPancakes

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the “Software”), to deal in the Software without
restriction, including without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

class AbstractDictionaryDB:
    data_dict: dict = {}

    def load(self) -> None:
        raise NotImplementedError()

    def save(self, lazy: bool = True) -> None:
        raise NotImplementedError()

class AbstractListDB:
    data_list: list = []

    def load(self) -> None:
        raise NotImplementedError()

    def save(self, lazy: bool = True) -> None:
        raise NotImplementedError()

class JsonDictionaryDB(AbstractDictionaryDB):
    __last_dict: dict = None

    __filename: str = None
    __compact: bool = None

    def __init__(self, filename: str, compact: bool = False) -> None:
        self.__filename = filename
        self.__compact = compact

        if not os.path.exists(self.__filename):
            with open(self.__filename, "x") as file:
                file.write("{}")
        
        self.load()

    def load(self) -> None:
        with open(self.__filename) as file:
            self.__last_dict = json.load(file)
            self.data_dict = copy.deepcopy(self.__last_dict)

    def save(self, lazy: bool = True) -> None:
        if lazy and self.__last_dict == self.data_dict:
            return

        with open(self.__filename, "w" if os.path.exists(self.__filename) else "x") as file:
            self.__last_dict = copy.deepcopy(self.data_dict)
            json.dump(self.__last_dict, file, indent = None if self.__compact else 4)

class JsonListDB(AbstractListDB):
    __last_list: list = None

    __filename: str = None
    __compact: bool = None

    def __init__(self, filename: str, compact: bool = False) -> None:
        self.__filename = filename
        self.__compact = compact

        if not os.path.exists(self.__filename):
            with open(self.__filename, "x") as file:
                file.write("[]")
        
        self.load()

    def load(self) -> None:
        with open(self.__filename) as file:
            self.__last_list = json.load(file)
            self.data_list = copy.deepcopy(self.__last_list)

    def save(self, lazy: bool = True) -> None:
        if lazy and self.__last_list == self.data_list:
            return

        with open(self.__filename, "w" if os.path.exists(self.__filename) else "x") as file:
            self.__last_list = copy.deepcopy(self.data_list)
            json.dump(self.__last_list, file, indent = None if self.__compact else 4)

class CsvListDB(AbstractListDB):
    __last_list: list = None

    __filename: str = None
    __separator: str = None
    __terminator: str = None

    def __init__(self, filename: str, separator: str = ";", terminator: str = "\n") -> None:
        self.__filename = filename
        self.__separator = separator
        self.__terminator = terminator

        if not os.path.exists(self.__filename):
            with open(self.__filename, "x"):
                pass
        
        self.load()

    def load(self) -> None:
        with open(self.__filename) as file:
            self.__last_list = list(csv.reader(file, escapechar = "\\", delimiter = self.__separator, lineterminator = self.__terminator))
            self.data_list = copy.deepcopy(self.__last_list)

    def save(self, lazy: bool = True) -> None:
        if lazy and self.__last_list == self.data_list:
            return

        with open(self.__filename, "w" if os.path.exists(self.__filename) else "x") as file:
            self.__last_list = copy.deepcopy(self.data_list)
            csv.writer(file, escapechar = "\\", delimiter = self.__separator, lineterminator = self.__terminator).writerows(self.__last_list)
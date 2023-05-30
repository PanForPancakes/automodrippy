import os, copy, json, csv

license = """
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
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
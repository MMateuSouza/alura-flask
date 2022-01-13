class Game:
    def __init__(self, name, category, console, pk=None) -> None:
        self.pk = pk
        self.name = name
        self.category = category
        self.console = console


class User:
    def __init__(self, username, password, pk=None) -> None:
        self.pk = pk
        self.username = username
        self.password = password

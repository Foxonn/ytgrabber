class PageNotFound(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.message:
            return 'Page {}, not found or does not exist!'.format(self.message)
        else:
            return 'Page not found or does not exist!'


class PageOops(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.message:
            return 'Page {}, not found!'.format(self.message)
        else:
            return 'Page not found!'


if __name__ == '__main__':
    if True:
        raise PageNotFound

from src.interfaces.abstract_view import AbstractView


class PrintView(AbstractView):

    def update(self, info):
        print(info)

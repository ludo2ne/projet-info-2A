import pyfiglet
from random import randint


class headers:
    def print_header(self):
        header_list = ["Gandalf", "Bilbo", "Aragorn",
                       "Gimli", "Legolas", "Sauron", "Gollum", "Saruman", "Frodo", "Meriadoc",
                       "Peregrin", "Boromir", "Faramir", "Samsagace", "Arwen", "Denethor", "Elrond",
                       "Eowyn", "Faramir", "Sylvebarbe", "Theoden", "Tom Bombadil"]
        k = randint(0, len(header_list)-1)
        result = pyfiglet.figlet_format(header_list[k])

        return (result)


if __name__ == "__main__":
    print(headers().print_header())

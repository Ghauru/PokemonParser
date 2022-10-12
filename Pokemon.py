class Pokemon:
    # вес, ссылка, рост, пол, вид, имя
    def __init__(self):
        self.weight = None
        self.href = None
        self.height = None
        self.gender = None
        self.kind = None
        self.name = None

    def pretty_info(self):
        print("Name: " + self.name, "Weight: " + self.weight, "Link: " + self.href, "Height: " + self.height, "Gender: " + self.gender,
              "Kind: " + self.kind, sep='\n')
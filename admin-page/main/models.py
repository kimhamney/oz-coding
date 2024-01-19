class Product():
    def __init__(self, data):
        self = self
        self.id = data[0]
        self.name = data[1]
        self.category = data[2]
        self.url = data[4]
        self.image_url = data[5]
        self.price = f"{format(data[3], ',')}원"
        self.review = format(data[6], ',')
        self.sales = format(data[7], ',')
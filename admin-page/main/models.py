class Product():
    def __init__(self, data):
        self = self
        self.id = data['id']
        self.name = data['name']
        self.category = data['category']
        self.url = data['url']
        self.image_url = data['image_url']
        self.price = f"{format(data['price'], ',')}원"
        self.review = format(data['review'], ',')
        self.sales = format(data['sales'], ',')
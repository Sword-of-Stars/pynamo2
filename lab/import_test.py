class BigBrain():
    value = 10
    
    @classmethod
    def load_images(cls, path):
        print(f"loading images from {path}")
        cls.value = path
    
    def __init__(self):
        print("running this code too")
        print(f"my images are stored in {self.value}")

BigBrain.load_images(6)
b = BigBrain()
c = BigBrain()
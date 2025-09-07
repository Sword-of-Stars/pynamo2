db = []

class A():
    def __init__(self):
        print(f"Is A in the database? {self in db}")
        self.am_i_alive()

    @classmethod
    def am_i_alive(cls):
        print(f"Is A in the database now? {cls in db}")

class B(A):
    def __init__(self):
        super().__init__()
        print("running here")
        self.am_i_alive()

    @classmethod
    def am_i_alive(cls):
        print(f"Is B in the database now? {cls in db}")



db.append(B)
B()
print(db)



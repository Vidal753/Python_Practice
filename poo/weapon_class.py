class Weapons:
    def __init__(self, damage, bullets, name):
        self.damage = damage
        self.bullets = bullets
        self.name = name

    def shoot(self, sub=10):
        if self.bullets < 1:
            print("You dont have bullets, reload")
        else:
            print("Bang Bang Bang")
            self.bullets -= sub

    def reload(self):
        self.bullets = 30


class Pistol(Weapons):
    def __init__(self, damage=20, bullets=30, name="Pistol"):
        super().__init__(damage, bullets, name)

    def shoot(self):
        return super().shoot(30)

    def info(self):
        print("Damage: " + str(self.damage))
        print("Bullets: " + str(self.bullets))
        print("Name: " + str(self.name))

    @classmethod
    def show(cls):
        print(f"This is a pistol ")


glop = Pistol()

glop.shoot()

Pistol.show()


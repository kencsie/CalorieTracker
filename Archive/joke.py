class ChiyoChichi:
    def __init__(self):
        self.name = 'Chiyo-chichi'
        self.color = 'yellow-orange'
        self.characteristics = 'cat-like creature'
        self.is_bullet_proof = False
        self.is_baseball_player = False
        self.is_santa_claus = False
        self.dislikes_red = True
        self.is_cat = False
        self.dislikes_tomatoes = True

if __name__ == "__main__":

    chiyo_chichi = ChiyoChichi()
    print("----------------------------------")
    print("Hello Everynyan!\nHow are you?\nFine, thank you!!!")
    print("Oh my god!")
    print("I wish I were a bird.")
    print("Why are you speaking english?")
    print("My daugther is going to America.")
    print("----------------------------------")

    assert chiyo_chichi.is_cat, "You are not a bird."
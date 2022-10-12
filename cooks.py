class Cook:
    def __init__(self, rank, proficiency, name, catch_phrase):
        self.rank = rank
        self.proficiency = proficiency
        self.name = name
        self.catch_phrase = catch_phrase

## cooks list
cook1 = Cook(3, 4, "Peter Jameson", "Enjoy your meal from a great cook!")
cook2 = Cook(2, 3, "Klaus Smith", "Use secret ingredients!")
cook3 = Cook(2, 2, "John Wilhelmsen", "Be creatiive!")
cook4 = Cook(1, 2, "Olaf Norskeberg", "Please have some patience!")

cooks = [cook1, cook2, cook3, cook4]

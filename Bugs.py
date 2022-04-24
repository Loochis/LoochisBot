# MANAGES BEAN ACCOUNT (BOT CURRENCY)

KILLED_SYNONYMS = ["OBLITERATED", "DEMOLISHED", "EVISCERATED", "BOILED", "ATE", "ATOMIZED", "INVERTED", "BLASTED", "SHOT", "PUNCHED", "GAMERED ON", "NO-JUTSU'D"]

class BugAccount:
    id = 0
    sightings = 0
    kills = 0

    def __init__(self, id, kills, sightings):
        self.id = id
        self.kills = kills
        self.sightings = sightings


class BugHandler:
    bugAccount = None

    # Gets an account from ID
    # 0 - Account was created
    # 1 - Account was succesfully opened
    def account_from_id(self, id):
        bugFile = open("AccountFiles/BugAccs.txt", "r")
        for line in bugFile:
            args = line.split(',')
            if int(args[0]) == int(id):
                self.bugAccount = BugAccount(int(args[0]), int(args[1]), int(args[2]))
                bugFile.close()
                return 1
        bugFile.close()
        self.create_account(id, 0, 0)
        return 0

    def create_account(self, id, kills, sightings):
        beanFile = open("AccountFiles/BugAccs.txt", "a")
        beanFile.write(str(id) + "," + str(kills) + "," + str(sightings) + "\n")
        beanFile.close()
        self.bugAccount = BugAccount(int(id), kills, sightings)

    def add_kills(self, amount):
        self.bugAccount.kills += amount
        self.save_account()

    def add_sightings(self, amount):
        self.bugAccount.sightings += amount
        self.save_account()

    def save_account(self):
        with open('AccountFiles/BugAccs.txt', 'r') as file:
            # read a list of lines into data
            lines = file.readlines()

        for i in range(len(lines)):
            args = lines[i].split(',')
            if int(args[0]) == self.bugAccount.id:
                lines[i] = str(self.bugAccount.id) + "," + str(self.bugAccount.kills) + "," + str(self.bugAccount.sightings) + "\n"
                print(lines)
                # and write everything back
                with open('AccountFiles/BugAccs.txt', 'w') as file:
                    file.writelines(lines)
                file.close()
                return 1
        file.close()

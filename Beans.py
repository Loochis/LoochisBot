# MANAGES BEAN ACCOUNT (BOT CURRENCY)

class BeanAccount:
    id = 0
    beans = 0

    def __init__(self, id, beans):
        self.id = id
        self.beans = beans


class BeanHandler:
    beanAccount = None

    # Gets an account from ID
    # 0 - Account was created
    # 1 - Account was succesfully opened
    def account_from_id(self, id):
        beanFile = open("BeanAccs.txt", "r")
        for line in beanFile:
            args = line.split(',')
            if int(args[0]) == int(id):
                self.beanAccount = BeanAccount(int(args[0]), int(args[1]))
                beanFile.close()
                return 1
        beanFile.close()
        self.create_account(id, 0)
        return 0

    def create_account(self, id, amount):
        beanFile = open("BeanAccs.txt", "a")
        beanFile.write(str(id) + "," + str(amount) + "\n")
        beanFile.close()
        self.beanAccount = BeanAccount(int(id), amount)

    def add_beans(self, amount):
        self.beanAccount.beans += amount
        self.save_account()

    def save_account(self):
        with open('BeanAccs.txt', 'r') as file:
            # read a list of lines into data
            lines = file.readlines()

        for i in range(len(lines)):
            args = lines[i].split(',')
            if int(args[0]) == self.beanAccount.id:
                lines[i] = str(self.beanAccount.id) + "," + str(self.beanAccount.beans) + "\n"
                print(lines)
                # and write everything back
                with open('BeanAccs.txt', 'w') as file:
                    file.writelines(lines)
                file.close()
                return 1
        file.close()

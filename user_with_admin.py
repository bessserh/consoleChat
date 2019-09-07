import json
import time
import pickle
from bes_frame import FunctionFramework

class User(object):


    def __init__(self, email, password, name = None, is_moderator = False, is_admin = False):
        self.email = email
        self.__password = password
        self.name = name
        self.is_moderator = is_moderator
        self.is_admin = is_admin
        self.__id = None

    def __setid(self):  # использовал ID чтоб записывался правильный JSON файл, без ошибок по ключам
        try:
            with open('baseJ.json', 'r') as f:
                pass
        except FileNotFoundError:
            self.__id = 0
        else:
            with open('baseJ.json', 'r') as f:
                js_d = (json.load(f))
                self.__id = int(max(list(dict.keys(js_d))))+1

    def register(self):
        self.__setid()
        form = {'email': self.email, 'password': self.__password,
                'name': self.name, 'moderator': self.is_moderator, 'admin': self.is_admin}
        try:
            with open('baseJ.json', 'r') as f:
                pass
        except FileNotFoundError:
            with open('baseJ.json', 'w') as f:
                form_full = {self.__id: form}
                json.dump(form_full, f, indent=2)
        else:
            with open('baseJ.json', 'r') as f:
                form_full = (json.load(f))
            # единственное что много памяти тратится на перезапись если файл большой
            with open('baseJ.json', 'w') as f:
                form_full[self.__id] = form
                json.dump(form_full, f, indent=2)

    def login(self):
        try:
            with open('baseJ.json', 'r') as f:
                pass
        except FileNotFoundError:
            print('No registered USERS')
        else:
            with open('baseJ.json', 'r') as f:
                login_dict = json.load(f)
                for item in login_dict.items():
                    if item[1]['email'] == self.email and item[1]['password'] == self.__password:
                        self.__id = item[0]
                        self.name = item[1]['name']
                        self.is_moderator = item[1]['moderator']
                        self.is_admin = item[1]['admin']
                        break
            if self.__id == None:
                print('You are not REGISTERED! Please register...')

    def message_print(self, message):
        if self.__id != None:
            try:
                with open('chatJ.json', 'r') as f:
                    pass
            except FileNotFoundError:
                chat = ['-={0}=-({1}): {2}'.format(self.name, time.asctime(), message)]
                with open('chatJ.json', 'w') as f:
                    json.dump(chat, f)
            else:
                with open('chatJ.json', 'r') as f:
                    chat = json.load(f)
                    chat.append('-={0}=-({1}): {2}'.format(self.name, time.asctime(), message))
                with open('chatJ.json', 'w') as f:
                    json.dump(chat, f)
        else:
            print('No USER found, register to WRITE')


class Moderator(User):

    def __init__(self, email, password, name = None, is_moderator = False, is_admin = False):
        User.__init__(self, email, password, name, is_moderator, is_admin)


    def make_notice(self, index, message):
        try:
           with open('chatJ.json', 'r') as f:
                    chat = json.load(f)
                    notice = '!----{0}({1}): {2}'.format(self.name, time.asctime(), message)
                    chat.insert(int(index)+1, notice)
           with open('chatJ.json', 'w') as f:
                    json.dump(chat, f)

        except FileNotFoundError:
            print('No messages in CHAT')
        except IndexError:
            print('Wrong INDEX, make NOTICE again!')
        except ValueError:
            print('Wrong INPUT')
        else:
            print('! -- DONE')

    def delete_message(self, index):
        try:
            with open('chatJ.json', 'r') as f:
                chat = json.load(f)
                chat.pop(int(index))
            with open('chatJ.json', 'w') as f:
                json.dump(chat, f)

        except FileNotFoundError:
            print('No messages in CHAT')
        except IndexError:
            print('Wrong INDEX, try DELETE again!')
        except ValueError:
            print('Wrong INPUT')
        else:
            print('! -- DONE')


class Admin(Moderator):

    def __init__(self, email, password, name = None, is_moderator = False, is_admin = False):
        Moderator.__init__(self, email, password, name, is_moderator, is_admin)

    def delete_user(self):
        try:
            with open('baseJ.json', 'r') as f:
                us_dict = json.load(f)
                print('Registered USERS:')
                for item in us_dict.items():
                    print('ID: {} = {}'.format(item[0], item[1]))
                index = input('Delete USER, ID:')
                us_dict.pop(index)
            with open('baseJ.json', 'w') as f:
                json.dump(us_dict, f, indent=2)

        except KeyError:
            print('Index ERROR')
        except FileNotFoundError:
            print('No registered USERS')
        else:
            print('! -- DONE')


# скажем main программы, объемно получилось со всеми проверками
while True:
    FunctionFramework.user_menu_print()
    choise = input('Your CHOISE: ')

    if choise == '1':
        print('NEW User:')
        email = input('E-mail: ')
        passw1 = input('Password: ')
        passw2 = input('Repeat password: ')

        if FunctionFramework.is_email(email) == True \
                and FunctionFramework.check_pass(passw1, passw2) == True:
            name = input('Your Name: ')
            u_new = User(email, passw1, name)
            u_new.register()
            print('{} registered, now you can write messages'.format(name))
        else:
            print('WRONG Input(not E-mail or Password mismatch)')
    elif choise == '2':
        FunctionFramework.show_chat()
    elif choise == '3':
        email = input('Your Email:')
        password = input('Your password:')
        u_log = User(email, password)
        u_log.login()
        if u_log.name != None:
            print('{} write your message:'.format(u_log.name))
            mess = input()
            u_log.message_print(mess)
    elif choise == '4':
        FunctionFramework.root_menu_print()
        choise = input('Your choise:')
        if choise == '1':
            try:
                with open('master.pickle', 'rb') as f:
                    pass
            except FileNotFoundError:
                FunctionFramework.master_pass()
            else:
                print('Master PASS was SETTED earlier, contact BES(developer) to change')
        elif choise == '2':
            masster = input('MASTER PASS:')
            try:
                with open('master.pickle', 'rb') as f:
                    mass_check = pickle.load(f)
            except FileNotFoundError:
                print('MASTERPASS not setted')
            else:
                if masster == mass_check:
                    print('Moderator or admin REGISTER(M or A):')
                    adm_mod = input('Who: ')
                    if adm_mod == 'M':
                        print('NEW MODERATOR:')
                        email = input('E-mail: ')
                        passw1 = input('Password: ')
                        passw2 = input('Repeat password: ')

                        if FunctionFramework.is_email(email) == True \
                                and FunctionFramework.check_pass(passw1, passw2) == True:
                            name = input('Your Name: ')
                            mod_new = Moderator(email, passw1, name, True, False)
                            mod_new.register()
                            print('Moderator {} registered, now you can manage chat'.format(name))
                        else:
                            print('WRONG Input(not E-mail or Password mismatch)')
                    elif adm_mod == 'A':
                        print('NEW ADMIN:')
                        email = input('E-mail: ')
                        passw1 = input('Password: ')
                        passw2 = input('Repeat password: ')

                        if FunctionFramework.is_email(email) == True \
                                and FunctionFramework.check_pass(passw1, passw2) == True:
                            name = input('Your Name: ')
                            adm_new = Admin(email, passw1, name, True, True)
                            adm_new.register()
                            print('ADMIN {} registered, now you can manage ALL'.format(name))
                        else:
                            print('WRONG Input(not E-mail or Password mismatch)')
                    else:
                        print('Wrong input M or A!')
                else:
                    print('USE MASTER PASS')
        elif choise == '3':
            print('Moderator enter')
            email = input('Email:')
            password = input('Password:')
            mod = Moderator(email, password)
            mod.login()
            if mod.name != None and mod.is_moderator == True:
                print('Moderator {} is IN'.format(mod.name))
                while True:
                    print('1 - Make notice')
                    print('2 - delete MESSAGE')
                    print('3 - LOG out')
                    what = input('Choise')
                    if what == '1':
                        FunctionFramework.show_chat(True)
                        ind = input('Message index: ')
                        message = input('Notice message: ')
                        mod.make_notice(ind, message)
                    elif what == '2':
                        FunctionFramework.show_chat(True)
                        ind = input('Message index to DELETE')
                        mod.delete_message(ind)
                    elif what == '3':
                        break
                    else:
                        print('Wrong INPUT!')


        elif choise == '4':
            print('ADMIN enter')
            email = input('Email:')
            password = input('Password:')
            adm = Admin(email, password)
            adm.login()
            if adm.name != None and adm.is_moderator == True and adm.is_admin == True:

                while True:
                    print('ADMIN {} is IN'.format(adm.name))
                    print('1 - delete MESSAGE')
                    print('2 - delete USER')
                    print('3 - LOG out')
                    what = input('Your CHOISE: ')
                    if what == '1':
                        FunctionFramework.show_chat(True)
                        ind = input('Message INDEX: ')
                        adm.delete_message(ind)
                    elif what == '2':
                        adm.delete_user()
                    elif what == '3':
                        break
                    else:
                        print('Wrong INPUT!')




    elif choise == '5':
        print('-----YOU ARE EXITING NOW-----')
        break


print('------------------Chat by BES (built 2.1)------------------')

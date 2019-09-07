import pickle
import json


class SetMasterPass(object):
    __masterPass = None

    @staticmethod
    def _setMasterPass(innerPass):
        __masterPass = innerPass

        with open('master.pickle', 'wb') as f:
            pickle.dump(__masterPass, f)


class FunctionFramework(object):

    @staticmethod
    def user_menu_print():
        print('---------------Chat---------------')
        print('1 - Register NEW User')
        print('2 - Show ALL chat')
        print('3 - LogIN and write message')
        print('    (only for registered Users)')
        print('4 - root(only for mod or admin)')
        print('5 - EXIT')

    @staticmethod
    def root_menu_print():
        print('-------------root-------------')
        print('1 - SET MASTER PASS')
        print('2 - Register new ADMIN or Moderator')
        print('3 - Moderator LOGin')
        print('4 - Admin LOGin')
        print('Any key to EXIT root')



    @staticmethod
    def show_chat(is_moder = False):
        try:
            with open('chatJ.json', 'r') as f:
                pass
        except FileNotFoundError:
            print('No Chat messages')
        else:
            with open('chatJ.json', 'r') as f:
                chat = json.load(f)
                if is_moder == False:
                    for message in chat:
                        print(message)
                else:
                    for i in range(len(chat)):
                        print('{}:'.format(i))
                        print(chat[i])

    @staticmethod
    def check_pass(*args):
        if args[0] == args[1]:
            return True
        else:
            return False

    @staticmethod
    def is_email(login):  # рабочая функция из прошлого занятия
        if login[0].isalpha() == True or login[0].isdigit() == True:
            if login[len(login) - 1].isalpha() == True:
                counter = [False, 0, False]
                for i in range(1, len(login) - 1):
                    if login[i] == '@':
                        counter[0] = True
                        counter[1] += 1
                    if login[i] == '.' and counter[1] == 1:
                        counter[2] = True
                if counter[0] == True and counter[1] == 1 and counter[2] == True:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    @staticmethod
    def master_pass():
        print('----root master pass----')
        print('You have 3 times to set CORRECT password')
        for i in range(3):
            passw = input('Set master pass:')
            passwr = input('Repeat master pass:')

            if FunctionFramework.check_pass(passw, passwr) == True:
                SetMasterPass._setMasterPass(passw)
                print('PASSWORD WAS SETTED')
                break
            else:
                print('ERROR! Mistake in password')







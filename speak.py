import os

def espaek_english(words):
    '''
    :param words:需要输入的话
    :return: void
    '''
    os.system('espeak '+words)


def espeak_chinese(words):
    '''
    :param words:需要输入的话
    :return: void
    '''
    os.system('espeak -vzh+f2 '+words)

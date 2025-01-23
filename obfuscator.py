# Copyright © 2025 Alexei Bezborodov. Contacts: <AlexeiBv+obfuscator@narod.ru>
# License: Public domain: http://unlicense.org/

import enum
from enum import auto

# Настройки

pyton_guard = dir(__builtins__)
pyton_guard += ["__init__", "items", "self"]

html_guard_s = "checked n t h1 h2 h3 h4 h5 h6 h7 h8 br html head body title bgcolor text link vlink alink pre h1 h6 b i tt cite em font size color a href img src name align p blockquote dl dt dd li div border hr table tr td th cellspacing width valign colspan rowspan frameset rows  cols frame noframes  marginwidth marginheight scrolling noresize select multiple option textarea input checkbox radio value submit reset image"
html_guard = html_guard_s.split()

start_guard = "#start_guard"
stop_guard = "#stop_guard"


class VarType(enum.Enum):
    LOCAL_VAR = auto()
    MEMBER_VAR = auto()
    CLASS_NAME = auto()
    FUNCTION_NAME = auto()
    FOR_VAR = auto()
    FUNCTION_PARAM1 = auto()
    FUNCTION_PARAM2 = auto()
    FUNCTION_PARAM3 = auto()
    FUNCTION_PARAM4 = auto()
    FUNCTION_PARAM5 = auto()
    FUNCTION_PARAM6 = auto()
    FUNCTION_PARAM7 = auto()

import re

# Слова под замену для языка python

func_prefix = r'(?:\A|;)\s*def\s*\w+\s*\('
skip_param = r'\s*\w+\s*[,]'
match_param = r'\s*(\w+)\s*(?:,|\))'

python_templates = {
    VarType.LOCAL_VAR:      r'(?:\A|;)\s*(\w+)\s*\=',
    VarType.MEMBER_VAR:     r'(?:\A|;)\s*self\.(\w+)\s*\=',
    VarType.CLASS_NAME:     r'(?:\A|;)\s*class\s*(\w+)\s*[:(]',
    VarType.FUNCTION_NAME:  r'(?:\A|;)\s*def\s*(\w+)\s*\(',
    VarType.FOR_VAR:        r'(?:\A|;)\s*for\s*(\w+)\s*in',
    VarType.FUNCTION_PARAM1: func_prefix + match_param,
    VarType.FUNCTION_PARAM2: func_prefix + skip_param*1 + match_param,
    VarType.FUNCTION_PARAM3: func_prefix + skip_param*2 + match_param,
    VarType.FUNCTION_PARAM4: func_prefix + skip_param*3 + match_param,
    VarType.FUNCTION_PARAM5: func_prefix + skip_param*4 + match_param,
    VarType.FUNCTION_PARAM6: func_prefix + skip_param*5 + match_param,
    VarType.FUNCTION_PARAM7: func_prefix + skip_param*6 + match_param,
}

def PythonFindAll(text):
    result = [];
    for t in VarType:
        result += PythonFind(t, text)
    return result

def PythonFind(var_type, text):
    return re.findall(python_templates.get(var_type), text)

def Test():
    def isEqualArray(a, b):
        return str(a) == str(b)

    text = "\tx   = 234 ; yD1 = 123;a3=1;\tself.d31 = 23;"
    text1 = "\t   def   Test1(sdfd,wer1): return;"
    text2 = "\t   class   Test2 (enum):"
    text3 = "\t   class   Test3 :"
    text4 = "\t   for  id3 in dfd :"
    text5 = ";\t def   Test5(  p1, p2 , p3,p4,p5,p6,p7,p8): return;"

    matches_var = PythonFind(VarType.LOCAL_VAR, text)
    matches_class_var = PythonFind(VarType.MEMBER_VAR, text)
    matches_func = PythonFind(VarType.FUNCTION_NAME, text1)
    matches_class1 = PythonFind(VarType.CLASS_NAME, text2)
    matches_class2 = PythonFind(VarType.CLASS_NAME, text3)
    matches_for = PythonFind(VarType.FOR_VAR, text4)
    matches_param1 = PythonFind(VarType.FUNCTION_PARAM1, text1)
    matches_param2 = PythonFind(VarType.FUNCTION_PARAM2, text1)

    matches_all = PythonFindAll(text + text1 + text2 + text5)

    assert isEqualArray(matches_var, ['x', 'yD1', 'a3']), matches_var
    assert isEqualArray(matches_class_var, ['d31'])
    assert isEqualArray(matches_func, ['Test1'])
    assert isEqualArray(matches_class1, ['Test2'])
    assert isEqualArray(matches_class2, ['Test3'])
    assert isEqualArray(matches_for, ['id3'])
    assert isEqualArray(matches_param1, ['sdfd']), matches_param1
    assert isEqualArray(matches_param2, ['wer1']), matches_param2
    assert isEqualArray(matches_all, ['x', 'yD1', 'a3', 'd31', 'Test2', 'Test1', 'Test5', 'sdfd', 'p1', 'wer1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7']), matches_all

Test()


import sys
import random

def MakeRandomName(size):
    rand_word = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm_"
    rand_dig = "1234567890"
    def RandWord(s):
        return random.choice(s)
    
    result = RandWord(rand_word)
    for i in range(size - 1):
        result += RandWord(rand_word + rand_dig)
    return result

class Guard:
    def __init__(self):
        self.guard_regexp_list = [];

    def GetGuardRegExpList(self):
        result = []
        for l in self.guard_regexp_list:
            if l != "":
                result += [l]
        return result

    def Update(self, cur_str):
        start = cur_str.find(start_guard)
        if start != -1:
            self.guard_regexp_list += [cur_str[start + len(start_guard):].strip()]
        elif cur_str.find(stop_guard) != -1:
            self.guard_regexp_list = self.guard_regexp_list[:-1]
        
        return len(self.guard_regexp_list) == len(self.GetGuardRegExpList())

def Obfuscator(in_file):
    f = open(in_file, 'r')
    lines = f.readlines()
    f.close()

    g = Guard()
    key_word_matches = []
    key_word_guard = []
    for l in lines:
        if g.Update(l):
            key_word_matches += PythonFindAll(l)
        guard_regexp_list = g.GetGuardRegExpList()
        for gr in guard_regexp_list:
            key_word_guard += re.findall(gr, l)

    key_word_matches = list(set(key_word_matches) - set(pyton_guard) - set(html_guard) - set(key_word_guard))

    new_matches = []
    for m in key_word_matches:
        if len(m) > 2:
            new_matches += [m]
    key_word_matches = new_matches

    rand_matches = []
    for m in key_word_matches:
        rand_matches += [MakeRandomName(16)]

    f = open(in_file+".map.txt", 'wb')
    for i in range(len(key_word_matches)):
        l = rand_matches[i] + '=' + key_word_matches[i] + "\n"
        f.write(l.encode('utf-8'))
    f.close()

    in_file_ext = in_file[in_file.rfind('.') + 1:]

    f = open(in_file+".ob." + in_file_ext, 'wb')
    g = Guard()
    for l in lines:
        if g.Update(l):
            for i in range(len(key_word_matches)):
                l = re.sub(r"\b%s\b" % key_word_matches[i], rand_matches[i], l)

        f.write(l.encode('utf-8'))
    f.close()

files_to_work = []

if __name__ == "__main__":
    for i in range(len(sys.argv)):
        param = sys.argv[i]
        if i > 0:
            files_to_work.append(param)

for f in files_to_work:
    Obfuscator(f)



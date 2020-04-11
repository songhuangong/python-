import importlib
from . import tt

t = 6
# 注意： 主框架对包的重启只能识别主py的改变，如果想让其识别到副py的改变，必须手动重启副py
importlib.reload(tt)


def p(a):
    global t
    r = (tt.t + a)
    print(r)
    print("t:", t)
    t = t + 1
    return r

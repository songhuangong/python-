import pkgutil
import importlib


class OnePyModule:
    """
    根据包名，文件名（模块名），方法名，调用到改方法
    """
    def __init__(self, pk_name, py_name):
        self.pk_name = pk_name
        self.py_name = py_name
        self.obj = self.get_obj()

    def get_obj(self):
        """根据包名称和文件名称得到一个实例"""
        return importlib.import_module(f"{self.pk_name}.{self.py_name}")

    def call_func(self, func_name, kw={}):
        """函数调用"""
        try:
            if hasattr(self.obj, func_name):
                func = getattr(self.obj, func_name)
                if type(kw).__name__ == 'dict':
                    if kw == {}:
                        return func()
                    else:
                        return func(**kw)
                elif type(kw).__name__ == 'list' or type(kw).__name__ == 'tuple':
                    if type(kw).__name__ == 'list':
                        kw = tuple(kw)
                    if kw == ():
                        return func()
                    else:
                        return func(*kw)
            else:
                return "该模块没有此方法"
        except Exception as e:
            return str(e)

    def reload(self):
        """重新加载模块"""
        print(f"重启{self.pk_name}.{self.py_name}")
        importlib.reload(self.obj)


class CallWithStatus:
    """
    主要为了完成有状态的调用，在下次调用同一个py时,不会重新加载。
    注意点： 只能调用主py里的函数，主py在第一次初始化的时候确定。
    """
    def __init__(self):
        # 包名称：包句柄
        self.pk_handles = {}
        # 包名称：主py( 一个pk里包含多个py文件，我们只能调用main_py里的函数！)
        self.main_pys = {}
        self.pk_name = None

    @staticmethod
    def create_cmd(pk_name, py_name, func_name, kw={}):
        return dict(
            path=dict(
                pk_name=pk_name,
                py_name=py_name,
            ),
            func_name=func_name,
            kw=kw,
        )

    def _get_pk_handle(self, pk_name, py_name):
        try:
            if self.pk_name not in self.pk_handles.keys():
                # 实例化
                py_module = OnePyModule(pk_name, py_name)
                # 向句柄字典里添加实例
                self.pk_handles[self.pk_name] = py_module
                # 向主py字典里添加值,当第一次初始化时的使用的py_name被认为是main_py！
                self.main_pys[self.pk_name] = py_module.py_name
            return self.pk_handles[self.pk_name]
        except Exception as e:
            return str(e)

    def call_func(self, cmd):
        try:
            pk_handle = self._get_pk_handle(**cmd['path'])
            if type(pk_handle).__name__ != 'str':
                if cmd['path']['py_name'] != self.main_pys[self.pk_name]:
                    return False, f"注意您调用的方法不再主py里，当前主py为:{self.main_pys[self.pk_name]}"
                return True, pk_handle.call_func(cmd['func_name'], cmd['kw'])
            else:
                # 如果为字符串类型，说明句柄获取失败
                return False, pk_handle
        except Exception as e:
            return False, str(e)

    def reload(self, pk_name, py_name):
        try:
            pk_handle = self._get_pk_handle(pk_name, py_name)
            pk_handle.reload()
            return True, ""
        except Exception as e:
            return False, f"{str(pk_handle)}:{e}"



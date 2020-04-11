from remote_call import CallWithStatus
import time

if __name__ == '__main__':
    cmd = CallWithStatus.create_cmd(pk_name="my_pks.pk1", py_name="main", func_name='p', kw=(1, ))
    cws = CallWithStatus()
    r = cws.call_func(cmd)
    print(r)
    # 查看是否带状态
    r = cws.call_func(cmd)
    print(r)
    # 休息，趁机修改t的值，
    time.sleep(5)
    # reload之前调用一次
    r = cws.call_func(cmd)
    print("reload之前的值：", r)
    # reload
    cws.reload(**cmd['path'])
    # 看reload是否有效。
    r = cws.call_func(cmd)
    print("reload之后的值：", r)


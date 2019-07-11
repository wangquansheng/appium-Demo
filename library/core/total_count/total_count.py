def _init():  # 初始化
    global total_count
    total_count = 0


def get_value():
    """ 取值 """
    return total_count


def add_value():
    """ 自加 """
    global total_count
    total_count += 1

def sub_value():
    """ 自减 """
    global total_count
    total_count -= 1

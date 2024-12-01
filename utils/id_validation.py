# utils/id_validation.py
import random


def id_check(id_number: str) -> bool:
    """
    驗證台灣身份證字號的格式與檢查碼。
    
    :param id_number: str, 要檢查的身份證字號
    :return: bool, 身份證是否有效
    """
    # 身份證對應的英文字母數值表
    local_table = {
        'A': 1, 'B': 0, 'C': 9, 'D': 8, 'E': 7, 'F': 6, 'G': 5, 'H': 4, 'I': 9,
        'J': 3, 'K': 2, 'L': 2, 'M': 1, 'N': 0, 'O': 8, 'P': 9, 'Q': 8, 'R': 7,
        'S': 6, 'T': 5, 'U': 4, 'V': 3, 'W': 1, 'X': 3, 'Y': 2, 'Z': 0
    }

    if len(id_number) != 10:
        return False  # 身份證長度不正確
    
    if id_number[0] not in local_table:
        return False  # 首碼英文字母不合法

    try:
        sex = int(id_number[1])
    except ValueError:
        return False  # 第二碼不是數字

    if sex not in {1, 2}:
        return False  # 第二碼性別碼不正確
    
    # 計算檢查碼
    check_num = local_table[id_number[0]]
    for i in range(1, 9):
        check_num += int(id_number[i]) * (9 - i)
    check_num += int(id_number[9])

    # 身份證合法則回傳 True
    return check_num % 10 == 0

def id_generator():
    local_table = {'A':1,'B':0,'C':9,'D':8,'E':7,'F':6,'G':5,'H':4,'I':9,
                    'J':3,'K':2,'L':2,'M':1,'N':0,'O':8,'P':9,'Q':8,'R':7,
                    'S':6,'T':5,'U':4,'V':3,'W':1,'X':3,'Y':2,'Z':0}

    local = random.choice(list(local_table.keys()))
    sex = random.randint(1,2)
    total = local_table[local]+sex*8
    result = f'{local}{sex}'

    for i in range(1,8):
            num = random.randint(0,9)
            total = total + num*(8-i)
            result = f'{result}{num}'

    num10 = 10 - total%10
    if num10 == 10 : num10 = 0
    result = f'{result}{num10}'
    return result
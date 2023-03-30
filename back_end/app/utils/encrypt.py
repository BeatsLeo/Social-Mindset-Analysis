from back_end.settings import SECRET_KEY
import hashlib

# 按md5标准进行加密
def md5(data_string: str):
    # 对明文进行加密算法是固定的, 因此需要加盐进行一次预处理
    obj = hashlib.md5(SECRET_KEY.encode('utf8'))

    # 对加盐后的对象与明文进行二次加密
    obj.update(data_string.encode('utf-8'))
    
    # 返回以十六进制表示的密文
    return obj.hexdigest()  
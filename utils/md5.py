# -*-coding:utf-8 -*-

import hashlib


def get_md5(data):
    m5 = hashlib.md5()
    # TypeError: Unicode-objects must be encoded before hashing
    m5.update(data.encode("utf-8"))
    return m5.hexdigest()


if __name__ == "__main__":
    print(get_md5('ksh3200000454'))

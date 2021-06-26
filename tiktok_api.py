from TikTokApi import TikTokApi
import string
import random


def get_tiktoks(username):
    did = ''.join(random.choice(string.digits) for num in range(19))
    verifyFp = "verify_kplpzttg_6nayW7u7_VmC6_4YxB_9YGv_akURZFo3jTSk"

    api = TikTokApi.get_instance(custom_verifyFp=verifyFp,
                                 custom_did=did)

    count = 1990
    # скачивает х последних тиктоков юзера
    tiktoks = api.byUsername(username, count=count)
    return tiktoks

if __name__ == '__main__':
    get_tiktoks(username)

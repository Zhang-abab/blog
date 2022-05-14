

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
}


def get_ip(request):
    # 判断是否使用代理
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # 代理
        ip = x_forwarded_for.split(',')[0]
    else:
        # 获取真实ip
        ip = request.META.get('REMOTE_ADDR')
    return ip


if __name__ == '__mian__':
    print(get_ip('12.0.0.14'))


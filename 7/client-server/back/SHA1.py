def rotate_left(n, b):# битвый сдвиг влево на b
    return ((n << b) | (n >> (32 - b))) & 0xffffffff


def hash_block(block, h0, h1, h2, h3, h4):
    assert len(block) == 64

    w = [0] * 80

    for i in range(16):
        w[i] = int.from_bytes(block[i * 4:i * 4 + 4], byteorder='big')

    for i in range(16, 80):
        w[i] = rotate_left(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)

    a = h0
    b = h1
    c = h2
    d = h3
    e = h4

    for i in range(80):
        if 0 <= i <= 19:
            f = d ^ (b & (c ^ d))
            k = 0x5A827999
        elif 20 <= i <= 39:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        elif 40 <= i <= 59:
            f = (b & c) | (b & d) | (c & d)
            k = 0x8F1BBCDC
        elif 60 <= i <= 79:
            f = b ^ c ^ d
            k = 0xCA62C1D6

        a, b, c, d, e = ((rotate_left(a, 5) + f + e + k + w[i]) & 0xffffffff,
                         a, rotate_left(b, 30), c, d)

    h0 = (h0 + a) & 0xffffffff
    h1 = (h1 + b) & 0xffffffff
    h2 = (h2 + c) & 0xffffffff
    h3 = (h3 + d) & 0xffffffff
    h4 = (h4 + e) & 0xffffffff

    return h0, h1, h2, h3, h4

def update(arg, unprocessed, message_byte_length, h):
    reader_position = 64 - len(unprocessed) # сколько байтов нам не хватает в конце6 в последнем блоке
    block = unprocessed + arg[0:reader_position] # берем первый блок

    while len(block) == 64: # проверяем что он 512 бит, то есть 64 байта и хэшируем его
        h = hash_block(block, *h) 
        message_byte_length += 64 # прибавляем длину в байтах
        block = arg[reader_position:reader_position + 64] # берем новый блок
        reader_position += 64 # сдвигаем, чтобы попасть на дальнейшей блок

    unprocessed = block # последний блок, у которого может быть меньше чем 512 бит

    return (unprocessed, message_byte_length, h)

def digest(unprocessed, message_byte_length, h):
    res = 0
    step = 32 * 4 # сдвигаем каждый блок на 32 бита влево, чтобы соединить вместе
    for h in produce_digest(unprocessed, message_byte_length, h):
        res += (h << step)
        step -= 32
    return res

def hexdigest(unprocessed, message_byte_length, h):
    return '%08x%08x%08x%08x%08x' % produce_digest(unprocessed, message_byte_length, h) # перевод в 16-ый вид

def produce_digest(unprocessed, message_byte_length, h): # хэширует наш последний блок, в котором может быть меньше 512 бит
    message = unprocessed
    message_byte_length = message_byte_length + len(message) # считает еще раз длину

    message += b'\x80' # прибавляем сначала единицу

    message += b'\x00' * ((56 - (message_byte_length + 1) % 64) % 64) # прибавляем нули, дополнение сообщения

    message_bit_length = message_byte_length * 8 # длина сообщения в битах

    message += message_bit_length.to_bytes(8, byteorder='big') # переводим длину в байтовый вид
    h = hash_block(message[:64], *h) # хэшируем блок
    if len(message) == 64:
        return h
    return hash_block(message[64:], *h) # если длина получилась 2*512 бит, то хэшируем оставшуюся часть


def sha1(data):
    h = (
        0x67452301,
        0xEFCDAB89,
        0x98BADCFE,
        0x10325476,
        0xC3D2E1F0,
    )

    unprocessed = b''
    message_byte_length = 0

    data = bytes(data, encoding='utf-8')

    unprocessed, message_byte_length, h = update(data, unprocessed, message_byte_length, h)
    return hexdigest(unprocessed, message_byte_length, h)


if __name__ == '__main__':
    result = sha1(input())
    # result = int.from_bytes(result, byteorder='big', signed=False)
    print(result)
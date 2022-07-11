ACCENT_STRING = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
NON_ACCENT_STRING = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'


def remove_accents_to_ascii(input_str):
    string_after_filtered = ''.join(NON_ACCENT_STRING[ACCENT_STRING.index(
        char)] if char in ACCENT_STRING else char for char in input_str)

    ascii_values = [ord(character) for character in string_after_filtered]

    for code in ascii_values:
        if code >= 768 and code <= 879:
            ascii_values.remove(code)

    return ascii_values


def remove_accents(input_str):
    string_after_filtered = ''.join(NON_ACCENT_STRING[ACCENT_STRING.index(
        char)] if char in ACCENT_STRING else char for char in input_str)

    ascii_values = [ord(character) for character in string_after_filtered]

    for code in ascii_values:
        if code >= 768 and code <= 879:
            ascii_values.remove(code)

    return ''.join(map(chr, ascii_values))


def compare_ascii_string(string_1: str, string_2: str):
    list_1 = remove_accents_to_ascii(string_1.lower())
    list_2 = remove_accents_to_ascii(string_2.lower())

    filtered_word1 = ''.join(map(chr, list_1))
    filtered_word2 = ''.join(map(chr, list_2))

    return [filtered_word1 in filtered_word2, filtered_word1, filtered_word2]

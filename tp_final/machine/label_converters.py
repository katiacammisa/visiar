def label_to_int(string_label):
    if string_label == 'Bulbasor': return 1
    if string_label == 'Dugtrio': return 2
    if string_label == 'Golbat': return 3
    if string_label == 'Venonat': return 4
    if string_label == 'Slowpoke': return 5
    else:
        raise Exception('unkown class_label')


def int_to_label(string_label):
    if string_label == 1: return 'Bulbasor'
    if string_label == 2: return 'Dugtrio'
    if string_label == 3: return 'Golbat'
    if string_label == 4: return 'Venonat'
    if string_label == 5: return 'Slowpoke'
    else:
        raise Exception('unkown class_label')

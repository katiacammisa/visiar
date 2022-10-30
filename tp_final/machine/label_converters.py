def label_to_int(string_label):
    if string_label == 'Bulbasor': return 1
    if string_label == 'Ivysaur':
        return 2
    else:
        raise Exception('unkown class_label')


def int_to_label(string_label):
    if string_label == 1: return 'Bulbasor'
    if string_label == 2:
        return 'Ivysaur'
    else:
        raise Exception('unkown class_label')

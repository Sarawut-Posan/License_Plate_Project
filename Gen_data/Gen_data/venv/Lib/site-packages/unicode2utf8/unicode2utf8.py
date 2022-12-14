
def unicode2utf8(input=None):
    """
        Takes in any type of object and if it finds unicode formatted data in it, it changes to utf-8.
        Input can be nay type of object, keep in mind that the modification occurs in place, no new object is returned.
    """
    data_type = type(input)
    if data_type == type(u''):
        return input.encode('utf-8')
    elif data_type == type({}):
        keys = input.keys()
        for key in keys:
            value = input[key]
            del(input[key])
            input[str(unicode2utf8(key))] = unicode2utf8(value)
        return input
    elif data_type == type([]):
        for i in range(len(input)):
            input[i] = unicode2utf8(input[i])
        return input
    else:
        return input

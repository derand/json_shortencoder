# -*- coding: utf-8 -*-

import json

class LitsHolder(object):
    """docstring for LitsHolder"""
    def __init__(self, l):
        super(LitsHolder, self).__init__()
        self.l = l

    def converted(self):
        if len(self.l) < 3:
            return self.l

        #return [self.l[0], '..{}itms..'.format(len(self.l)-2), self.l[-1]]
        return [self.l[0], '...', self.l[-1]]
        

class ShortEncoder(json.JSONEncoder):
    def _preprocess_dict(self, obj):
        if isinstance(obj, dict):
            return {k: self._preprocess_dict(v) for k,v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return LitsHolder([self._preprocess_dict(el) for el in obj])
        return obj

    def default(self, obj):
        if isinstance(obj, LitsHolder):
            #return [json.JSONEncoder.default(self, el) for el in obj.converted()]
            return obj.converted()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

    def iterencode(self, obj, **kwargs):
        tmp = super().iterencode(self._preprocess_dict(obj), **kwargs)
        return [''.join(tmp).replace('"...",', '...,')]


def main():
    j = {
        "name": "John",
        "zage": 2+1,
        "married": True,
        "divorced": False,
        "children": ("Ann","Billy", "Suzan", "Jane"),
        "pets": None,
        "cars": [
            {"model": "BMW 230", "mpg": 27.5},
            {"model": "Nissan Leaf", "mpg": 21.6},
            {"model": "Ford Edge", "mpg": 24.1}
        ]
    }

    s = json.dumps(j, cls=ShortEncoder)
    #s = ShortEncoder().encode(j)
    print(s)


if __name__=='__main__':
    main()



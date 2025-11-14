#
# Copyright (C) 2025 pdnguyen of HCMC University of Technology VNU-HCM.
# All rights reserved.
# This file is part of the CO3093/CO3094 course.
#
# WeApRous release
#
# The authors hereby grant to Licensee personal permission to use
# and modify the Licensed Source Code for the sole purpose of studying
# while attending the course
#

from collections.abc import MutableMapping

class CaseInsensitiveDict(MutableMapping):
    """The :class:`CaseInsensitiveDict<MutableMapping>` object, which 
    contains a custom behavior of MutuableMapping.

    Usage::

      >>> import tools
      >>> word = CaseInsensitiveDict(status_code='404', msg="Not found")
      >>> code = word['status_code']
      >>> code 
      404

      >>> msg = word['msg']
      >>> s.send(r)
      Not found

      >>> print(word)
      {'status_code': '404', 'msg': 'Not found'}

    """

    def __init__(self, *args, **kwargs):
        self.store = {k.lower(): v for k, v in dict(*args, **kwargs).items()}

    def __getitem__(self, key):
        return self.store[key.lower()]

    def __setitem__(self, key, value):
        self.store[key.lower()] = value

    def __delitem__(self, key):
        del self.store[key.lower()]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)
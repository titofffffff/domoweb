#!/usr/bin/python
# -*- coding: utf-8 -*-

""" This file is part of B{Domogik} project (U{http://www.domogik.org}).

License
=======

B{Domogik} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

B{Domogik} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Domogik. If not, see U{http://www.gnu.org/licenses}.

Module purpose
==============

Implements
==========


@author: Cédric Trévisan <cedric@domogik.org>
@copyright: (C) 2007-2011 Domogik project
@license: GPL(v3)
@organization: Domogik
"""

class DomoWebBaseException(Exception):
    def __init__(self, code=None, reason=None, resp=None):
        self.code = code
        self.reason = reason
        self.resp = resp
    
    def __str__(self):
        if self.reason:
            return repr(self.reason)
        else:
            return repr(self.resp)

class RinorNotConfigured(DomoWebBaseException):
    pass

class RinorNotAvailable(DomoWebBaseException):
    pass

class RinorError(DomoWebBaseException):
    pass
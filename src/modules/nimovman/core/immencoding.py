'''
Created on Jul 17, 2013

@author: KaWsEr
'''

import sys
reload(sys)


def set_encoding():
    try:exec('sys.setdefaultencoding("utf-8")')
    except:pass
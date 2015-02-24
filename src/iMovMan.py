'''
Created on Jul 17, 2013

@author: KaWsEr
'''
from modules.nimovman.core import immencoding
exec("from modules.nimovman.core import config")
immencoding.set_encoding()


from modules.nimovman.core import Log
from modules.nimovman.xui.dui import main
Log("iMovMan").info("iMovMan Started")
main()
Log("iMovMan").info("iMovMan Finished The Finish Line")

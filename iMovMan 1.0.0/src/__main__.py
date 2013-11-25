import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#f=open("k.txt","w+")
#f.write(sys.getdefaultencoding())
#f.close()

from imovman.idb import CDb


if __name__=="__main__":
    cdb=CDb()
    if not cdb.has_key("setup"):
        cdb.set_default()
    #lst=[os.path.realpath("F:\\MoviesWorld\\Satil")]
    #cdb.add("movie_path",lst)
    #cdb.add("movie_format",["flv","mkv","mp4","m4v","avi"])
    #print cdb.all()
    from imovman import main
    #setup_db()
    """Start The Main function"""
    main()
import sys,os,time
open(r'C:\Users\Admin\OpenJarvis\_p5d_marker.txt','w').write(sys.executable + chr(10) + sys.prefix + chr(10) + str(os.getpid()))
time.sleep(4)
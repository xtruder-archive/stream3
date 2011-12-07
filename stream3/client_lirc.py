import xmlrpclib
import pylirc

from time import sleep
from optparse import OptionParser

from daemon import createDaemon
from rocketeer. app import AppStatus

def main():
    usage = "usage: pstream3_client_lirc [options]"
    parser = OptionParser(usage)
    parser.add_option("--daemon",
                      help="Run me as daemon", action="store_true", dest="daemon")
    parser.add_option("--ip",
                      help="Ip where should i listen", dest="ip")
    parser.add_option("--port",
                      help="Port where should i bind", dest="port")
    parser.add_option("--dump",
                      help="Folder where should i dump", dest="dump")
    parser.add_option("--lirc-config",
                      help="Path to lirc config", dest="lirc_config")
    parser.add_option("--pid",
                      help="Process pid", dest="pid")
    (options, args) = parser.parse_args()

    if options.daemon:
        ret= createDaemon()

        if options.pid:
            pid= os.getpid()
            f= open(options.pid, "w")
            f.write(str(pid))
            f.close()

    if options.ip and options.port:
        ip= options.ip
        port= options.port
    else:
        ip= "localhost"
        port= str(8400)

    client = xmlrpclib.ServerProxy("http://%s:%s/" % (ip, port))
    h264_client= None

    blocking= 1
    if options.lirc_config:
        lirc_path= options.lirc_config
    else:
        lirc_path="/etc/pstream/conf"
    if(pylirc.init("pylirc", lirc_path, blocking)):
        code= {"config": ""}
        while(code["config"] != "quit"):
            #Read next code
            s= pylirc.nextcode(1)
            #Right now i don't care what you press on remote.
            code["config"]= "start_stream"

            status= None
            if(code["config"] == "start_stream"):
                try:
                    status=h264_client.GetAppRunStatus()
                except:
                    status=None

                if (status!=AppStatus.RUNNING) or not status:
                    print("Creating new app")
                    h264= client.CreateApp("h264Stream")
                    notifyCopyProcess= client.CreateApp("NotifyCopyProcess")
                    notifyCopyProcess_client= xmlrpclib.ServerProxy("http://%s:%s/" % (ip,port) + str(notifyCopyProcess))
                    print h264, client.GetAppInstances()
                    h264_client= xmlrpclib.ServerProxy("http://%s:%s/" % (ip,port) + str(h264))
                    h264_client.SetAppValue("auto_restart", 1)
                    if options.dump:
                        h264_client.SetAppValue("dumpfolder", options.dump)
                    else:
                        h264_client.SetAppValue("dumpfolder", "/home/recode/dump")
                    h264_client.StartApp()
                else:
                    print("Stoping stream")
                    client.DestroyInstance(h264)
                    client.DestroyInstance(notifyCopyProcess)
                    continue

                while h264_client.GetAppRunStatus()!=AppStatus.RUNNING:
                    print "here"
                    sleep(.5)
                print("Next code")
 

        client.DestroyInstances()
        pylirc.exit()

if __name__ == "__main__":
    main()

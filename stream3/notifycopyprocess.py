import os
import paramiko
import os.path 
import time

from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, ProcessEvent

from rocketeer.app import AppStatusUpdate, AppStatus
from rocketeer.process import StatusUpdateNode

class NotifyCopyProcess(StatusUpdateNode, AppStatusUpdate, ProcessEvent):
    def __init__(self):
        StatusUpdateNode.__init__(self)
        AppStatusUpdate.__init__(self)

	mask = EventsCodes.ALL_FLAGS["IN_CREATE"]  # watched events

	self.wm = WatchManager()
	self.notifier = Notifier(self.wm, self)

	if self.GetAppValue("src"):
	    self.src=self.GetAppValue("src")
	else:
	    self.src="/tmp/motion/"

	self.wdd = self.wm.add_watch(self.src, mask, rec=True)

	if self.GetAppValue("host"):
	    self.host=self.GetAppValue("host")
        else:
	    self.host="dogbert"

	if self.GetAppValue("username"):
	    self.username=self.GetAppValue("username")
        else:
	    self.username="arhivar"

	if self.GetAppValue("password"):
	    self.password=self.GetAppValue("password")
        else:
	    self.password="nomorebacklog"

	if self.GetAppValue("dst"):
	    self.dst=self.GetAppValue("dst")
        else:
	    self.dst="/home/arhivar/static_html/live/slides4"

	try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.host, username=self.username, password=self.password)

            self.ftp = self.ssh.open_sftp()
	except:
	    self.error= True
	    print "Cannot connect"

    def UpdateStatus(self):
        if not StatusUpdateNode.UpdateStatus(self):
            return False

        self._SetAppRunStatus(AppStatus.RUNNING)

	self.notifier.process_events()
	if self.notifier.check_events(timeout=.1):
            self.notifier.read_events()

        return True

    def process_IN_CREATE(self, event):
	print "Event", os.path.join(event.path, event.name)
	self.copyover(os.path.join(event.path, event.name))
	
    def copyover(self, file):
        outfile = "%s/%s" % (self.dst, os.path.basename(file))
	self.ftp.put(file, outfile)

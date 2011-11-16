import time

from rocketeer.app import AppProcess, AppStatus
from rocketeer.process import StatusUpdateProcess

class FFMpegProcess(StatusUpdateProcess, AppProcess):
    def __init__(self, bootstrap):
        StatusUpdateProcess.__init__(self, bootstrap)
        AppProcess.__init__(self)

        self.updateTime= time.time() # For knowing if something went wrong.

    def UpdateStatus(self):
        if not StatusUpdateProcess.UpdateStatus(self):
            return None

        lines= self.ReadLines()
        result= self._ParseStatus(lines)

        if not result:
            if (time.time()-self.updateTime)>30:
                self._SetAppRunStatus(AppStatus.ERROR)

            return None

        print("running")
        self._SetAppRunStatus(AppStatus.RUNNING)

        #Store last update time for knowing if there was
        #an error.
        self.updateTime= time.time()

        self._SetAppStatus(result)

        return result

    def _ParseStatus(self, lines):
        result= []
        for line in lines:
            if "frame=" in line:
                params= line.split("=")
                for i, param in enumerate(params):
                    if i==len(params)-1:
                        break
                    if i==0:
                        k=param
                        v=params[1].split()[0]
                    else:
                        k=param.split()[1]
                        v=params[i+1].split()[0]
                    result+=[[k,v]]

        return result


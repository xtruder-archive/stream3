from time import sleep

from rocketeer.process import TemplateCommand, ConfigTemplateTemplateCommand
from ffmpegprocess import FFMpegProcess
from rocketeer.staticprocess import StaticProcess
from notifycopyprocess import NotifyCopyProcess

from rocketeer.server import Server, AppsHandler

from templates.stream_h264 import h264Tpl
from templates.stream_webm import webmTpl
from templates.stream_prosojnice import prosojniceTpl
from templates.stream_test import testTpl
from templates.stream_motion import motionTpl
from templates.stream_motion_conf import motionConfTpl

class h264Stream(FFMpegProcess):
    def __init__(self):
        FFMpegProcess.__init__(self,bootstrap=TemplateCommand(h264Tpl, "stream_h264.tpl"))

class webmStream(FFMpegProcess):
    def __init__(self):
        FFMpegProcess.__init__(self,bootstrap=TemplateCommand(webmTpl, "stream_webm.tpl"))

class prosojniceStream(FFMpegProcess):
    def __init__(self):
        FFMpegProcess.__init__(self,bootstrap=TemplateCommand(prosojniceTpl, "stream_prosojnice.tpl"))

class testStream(FFMpegProcess):
    def __init__(self):
        FFMpegProcess.__init__(self,bootstrap=TemplateCommand(testTpl, "stream_test.tpl"))

class motionDetect(StaticProcess):
    def __init__(self):
        StaticProcess.__init__(self,bootstrap=ConfigTemplateTemplateCommand(motionTpl, motionConfTpl, \
                                "stream_motion.tpl", "stream_motion_conf.tpl"))

def CreateServer(ip="127.0.0.1", port=8400):
    srv= Server(AppsHandler, ip, port)
    appsHandler= srv.GetRequestHandler()
    appsHandler.RegisterApp(h264Stream)
    appsHandler.RegisterApp(webmStream)
    appsHandler.RegisterApp(prosojniceStream)
    appsHandler.RegisterApp(motionDetect)
    appsHandler.RegisterApp(testStream)
    appsHandler.RegisterApp(NotifyCopyProcess)
    srv.start()

    return srv

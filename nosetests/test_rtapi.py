#!/usr/bin/env python
import os,time

from nose import with_setup
from machinekit.nosetests.realtime import setup_module ,teardown_module

from machinekit import rtapi,hal

import ConfigParser

def test_get_uuid():
    global uuid, rt
    cfg = ConfigParser.ConfigParser()
    cfg.read(os.getenv("MACHINEKIT_INI"))
    uuid = cfg.get("MACHINEKIT", "MKUUID")

def test_rtapi_connect():
    global rt
    rt = rtapi.RTAPIcommand(uuid=uuid)

def test_loadrt_or2():
    global rt
    rt.loadrt("or2")
    rt.newthread("servo-thread",1000000,use_fp=True)
    hal.addf("or2.0","servo-thread")
    hal.start_threads()
    time.sleep(0.2)

def test_unloadrt_or2():
    hal.stop_threads()
    rt.delthread("servo-thread")
    rt.unloadrt("or2")

(lambda s=__import__('signal'):
     s.signal(s.SIGTERM, s.SIG_IGN))()

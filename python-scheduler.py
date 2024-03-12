#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
별도 스케쥴러, log는 공유하되, 별도 프로세스로 기동
'''

import sys
import os
import time
import datetime

import getopt

import traceback

import schedule
import json
import subprocess



from scheduler_main_app import *


#스케쥴러 등록
def doAddScheduleJob(strJsonConfigPath, monitorMainApp):


    if None == strJsonConfigPath or False == os.path.exists(strJsonConfigPath):
        print("json config file not exist {}".format(strJsonConfigPath))
        return False

    #json config 설정 정보를 읽어들임

    dictJsonInfo = dict()

    fJsonData = open(strJsonConfigPath, encoding="utf-8")
    strJsonData = fJsonData.read()
    
    #json config 설정정보를 읽어서, 저장
    dictJsonInfo = json.loads(strJsonData)
    fJsonData.close() #file close


    second_schedule = dictJsonInfo.get("second_schedule")
    min_schedule = dictJsonInfo.get("min_schedule")
    hour_schedule = dictJsonInfo.get("hour_schedule")
    day_schedule = dictJsonInfo.get("day_schedule")

    #초단위 스케쥴 
    if None != second_schedule:

        for items in second_schedule:

            nUse = items["use"] #사용여부

            nInterval = items["interval"] #주기
            strMethodName = items["method"] #실행 모듈명

            strShellScriptArgs = items["call_schell_script"] #실행시 부가 인자

            if 0 == nUse:
                print("skip add second schedule, interval={}, method={}, shell_script={}".format(nInterval, strMethodName, strShellScriptArgs))
                continue

            scheduleCallBack = getattr(monitorMainApp, strMethodName)
            schedule.every(nInterval).seconds.do(scheduleCallBack, strShellScriptArgs)

            print("add second schedule, interval={}, method={}, shell_script={}".format(nInterval, strMethodName, strShellScriptArgs))

    #분단위 스케쥴
    if None != min_schedule:
    
        for items in min_schedule:

            nUse = items["use"] #사용여부
            nInterval = items["interval"] #주기
            strMethodName = items["method"] #실행 모듈명

            strShellScriptArgs = items["call_schell_script"]

            if 0 == nUse:
                print("skip add minute schedule, interval={}, method={}, shell_script={}".format(nInterval, strMethodName, strShellScriptArgs))
                continue

            scheduleCallBack = getattr(monitorMainApp, strMethodName)
            schedule.every(nInterval).minutes.do(scheduleCallBack, strShellScriptArgs)

            print("add minute schedule, interval={}, method={}, shell_script={}".format(nInterval, strMethodName, strShellScriptArgs))

    #시간단위 스케쥴
    if None != hour_schedule:
    
        for items in hour_schedule:

            nUse = items["use"] #사용여부
            nInterval = items["interval"] #주기
            strMethodName = items["method"] #실행 모듈명

            strShellScriptArgs = items["call_schell_script"]

            if 0 == nUse:
                print("skip add hour schedule, interval={}, method={}, shell_script={}".format(nInterval, strMethodName, strShellScriptArgs))
                continue

            scheduleCallBack = getattr(monitorMainApp, strMethodName)
            schedule.every(nInterval).hours.do(scheduleCallBack, strShellScriptArgs)

            print("add hour schedule, interval={}, method={}, shell_script={}".format(nInterval, strMethodName, strShellScriptArgs))

    #일단위 스케쥴
    if None != day_schedule:

        for items in day_schedule:

            nUse = items["use"]
            nInterval = items["interval"] #주기
            strAtTime = items["at_time"]
            strMethodName = items["method"]

            strShellScriptArgs = items["call_schell_script"] 

            if 0 == nUse:
                print("skip add day schedule, interval={}, method={}, shell_script={}".format(nInterval, strMethodName, strShellScriptArgs))
                continue
            scheduleCallBack = getattr(monitorMainApp, strMethodName)
            schedule.every(nInterval).days.at(str(strAtTime)).do(scheduleCallBack, strShellScriptArgs)

            print("add day schedule, at_time={}, method={}, shell_script={}".format(strMethodName, strMethodName, strShellScriptArgs))

    return ERR_OK

#main, 시작점
def main():

    try:

        dictOpt = dict()

        opts,args = getopt.getopt(sys.argv[1:], "", 
        ["config="])

        for o, arg in opts:        

            if o in ("--config"): 
                dictOpt["config"] = arg 

            else:
                assert False, "unhandled option"
                sys.exit()
                return False

        print("start process pid = {}, argc = {}, argv = {}".format(os.getpid(), len(sys.argv), str(sys.argv)))


        #스케쥴러 호출 인터페이스는 MonitorSchedulerMainApp 로 통일
        monitorMainApp = MergeSchedulerMainApp()

        bInitializeMainApp = monitorMainApp.Initialize()

        if True == bInitializeMainApp:
            print("Fail Initialize Main App, Exit")
            return False

        #strJsonConfigPath = dictOpt.get("config")
        strJsonConfigPath = "./modules/config/scheduler_config.json"
        
        doAddScheduleJob(strJsonConfigPath, monitorMainApp)

        while True:
            schedule.run_pending()
            time.sleep(1)

        print("end process pid = {}".format(os.getpid()))

        return ERR_OK

    except Exception as err: 
        print(str(err))        
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    main()    

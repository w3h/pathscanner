#!/usr/bin/python env
#coding=utf-8
from optparse import OptionParser 
from core.shellpara import ShellPara
import core.configpara as ConfigPara
import core.common as common
import copy
import sys,os
from core.utils.threadpuul import ThreadPool

g_scan_sum = 0
g_scan_currnum = 0

def banner():
    info = '''......................................................................
         (__)
         (oo) 
   /------\/ ------ PathScanner V1.0 by W.HHH ------
  / |    ||   
 *  /\---/\ 
    ~~   ~~   
.... Good Luck for you today .......
......................................................................'''
    print info

def usage():
    MSG_USAGE = "pathscanner.py [-t <url>] [-s <script-type>] [-d <datafile> ] " \
                "[--thread <thread num defult:10>] [--timeout <timeout defult:10>]  " \
                "[--delay <delay time defult:5>]"
    parser = OptionParser(MSG_USAGE) 
    parser.add_option("-t", "--target", dest="target", default=False, help="Scanning the target")
    parser.add_option("-s", "--script", dest="script", default="", help="Scanning the type of script (jsp | asp | aspx | php | all)")
    parser.add_option("-d", "--data", dest="data", help="Scanning the data")   
    parser.add_option("--thread", dest="thread", default="10", help="Scanning the number of threads (default:10)")
    parser.add_option("--timeout", dest="timeout", default="10", help="Scanning the timeout (default:10)") 
    parser.add_option("--delay", dest="delay", default="5", help="Scanning the delay time (default:5)")
    (options, args) = parser.parse_args()

    if not options.target:
        parser.error("incorrect the target")
        sys.exit(1)
    if not CheckTarget(options.target):
        parser.error("incorrect the target")  
        sys.exit(1)
    if options.data:
        if not os.path.exists(options.data):
            parser.error("incorrect the data file ")  
            sys.exit(1)
    if int(options.delay) < 1 or int(options.delay) > 100:
        parser.error("incorrect the delay")
        sys.exit(1)
    if int(options.thread) < 1 or int(options.thread) > 100:
        parser.error("incorrect the thread number")
        sys.exit(1)
    if int(options.timeout) < 1 or int(options.timeout) > 100:
        parser.error("incorrect the timeout")
        sys.exit(1)
    return options

def CheckTarget(target):
    st = common.CheckHostOnline(target)
    if not st: return False
    return True

def GetScriptType(script, target):
    ret = []
    if script.strip() == "":
        stype = common.GetScriptType(target)
        if not stype: 
            ret = ['common']
        else:
            ret = ['common', stype]
        return ret

    if script.find("all") >= 0:
        ret = copy.copy(ConfigPara.DICT_TABLE_NAME)
        return ret

    ret.append("common")
    if script.find("aspx") >= 0:
        script = script.replace("aspx", "xoxo")
        ret.append("aspx")

    for i in ConfigPara.DICT_TABLE_NAME:
        if i in script:
            ret.append(i)

    if not ret:
        parser.error("incorrect the target")  
        sys.exit(1)

    return ret

def output(args):
    global g_scan_currnum
    global g_scan_sum
    g_scan_currnum += 1 

    code = int(args[2])
    if code != 404 and code > 0:
        info = "\r\b [+] %d : %s" % (code, args[1])
        if len(args[1]) < 10:
            info += " "*30
        info += "\n [P] %d / %d" % (g_scan_currnum, g_scan_sum)
        sys.stdout.write(info) 
        sys.stdout.flush()
    else:
        info = "\r\b [P] %d / %d" % (g_scan_currnum, g_scan_sum)
        sys.stdout.write(info)  
        sys.stdout.flush()

    url = args[0] + args[1]
    common.WriteLog(url, code)

def GetCmdPara(options):
    para = ShellPara()
    para.Init()
    para.thread = int(options.thread)
    para.target = options.target
    para.timeout = int(options.timeout)
    para.data = options.data   

    stype = GetScriptType(options.script, options.target)
    para.SetDBScriptType(stype)
    para.script = stype
    para.servertype = common.GetServerType(options.target)

    global g_scan_sum
    g_scan_sum = para.GetScanNum()
    return para

def Task_Fun(qp):
    for i in qp.GetList():
        qp.Run(i)
        info = qp.GetCode()
        args = [qp.Target(), i, info]
        output(args)

def run():
    para = ShellPara()
    pool = ThreadPool(int(para.thread))
    for t in para.script:
        lts = []
        common.AddTasksToList(para.target, t, lts)
        for tt in lts:
            pool.add_task(Task_Fun, tt)
        pool.wait_completion()

def main(options):
    op = GetCmdPara(options)
    print " [ Target]:", options.target
    print(" [ Server]: %s" % op.servertype)
    print " [ Script]:", str(op.script)
    print " [   data]:", options.data
    print " [ Thread]:", options.thread
    print " [TimeOut]:", options.timeout
    print " [Numbers]:", g_scan_sum
    print " [ Output]:", os.getcwd() + common.GetHostFilename(options.target)
    print

    common.InitLog(options.target)
    run()

if __name__ == "__main__":
    banner()
    main(usage())

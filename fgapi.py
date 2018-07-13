import requests, json, pprint, argparse
import logging, logging.handlers
from strgen import StringGenerator as SG
import FortigateApi

def funcstrGen():
    randStr = SG("[\d\w]{12}").render()
    return randStr


#FG connection
serialNumberFGT = "xxxxxxxxxxxx"
fgtVdom = "root"
fg = FortigateApi.Fortigate('xxxipx.x.x.x', fgtVdom, 'xxxxusernamexxxxx', 'xxxxpassxxxxxxxxxxx')

#FG connection END

#Arg
fgApiArgParser = argparse.ArgumentParser(description='FortigateAPI commands')
fgApiArgParser.add_argument('-a', '--action', help='action: fwAddAddr, fwDelAddr ', required=True)
fgApiArgParser.add_argument('-n', '--nameaddr', required=False)
fgApiArgParser.add_argument('-i', '--ipaddr', required=False)
fgApiArgParser.add_argument('-m', '--maskaddr', required=False)
fgApiArgs = fgApiArgParser.parse_args()
#Arg END

#Logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

def logThrow(eventID, logContent, logdebug):
	log.debug( " fgapieventid=" + eventID + logContent +", fgapidebug=" + logdebug)
#Logging END

#FW address adding

def fwAddAddr(nameAddr, ipAddr, maskAddr):
    eventID = funcstrGen()
    ipMaskAddr = ipAddr+"/"+maskAddr
    ipMaskAddrws = ipAddr+" "+maskAddr
    ipObj = [['name', nameAddr], ['subnet', ipMaskAddrws]]
    def getAddr(opt):
        getFwAddr = fg.GetFwAddress(nameAddr)
        if opt == "js":
            tmp = getFwAddrjsl = json.loads(getFwAddr)
            return tmp
        if opt == "str":
            tmp2 = fg.GetFwAddress(nameAddr)
            return tmp2



    # Debug things
    print "\n", "\n", getAddr("str")
    print "__\n"
    # Debug things end

    if getAddr("js")["http_status"] != '404' \
            and getAddr("js")["serial"] == serialNumberFGT \
            and getAddr("js")["vdom"] == fgtVdom:

        if not fg.Exists('cmdb/firewall/address/', ipObj):
            fg.AddFwAddress(nameAddr, ipMaskAddr)
            logThrow(eventID, "fgapistatus=\""+ str(ipObj[0]) +"IP object successfully added\" ", getAddr("str"))

        else:logThrow(eventID, "fgapistatus=\""+ str(ipObj[0]) +"IP object already exist\",  ", getAddr("str"))

    else:logThrow(eventID, "fgapistatus=\"API Connection Failed\" ", getAddr("str"))

if fgApiArgs.action == 'fwAddAddr':
    fwAddAddr(str(fgApiArgs.nameaddr), str(fgApiArgs.ipaddr), str(fgApiArgs.maskaddr))
#FW address adding end

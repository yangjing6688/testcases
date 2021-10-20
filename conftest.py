import pytest
from pytest import fixture
from pytest_testconfig import config
import threading
import queue
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Utilities.Firmware.pytestLoadFirmware import PlatformLoadFirmware
from ExtremeAutomation.Utilities.EconClient.econ_request_api import econAPI
from ExtremeAutomation.Utilities.Framework.test_case_inventory import PytestItems
from ExtremeAutomation.Utilities.Framework.test_case_inventory import PathTools
#
# @fixture(scope='session')
# def apiUdks():
    # defaultLibrary = DefaultLibrary()
    # api = defaultLibrary.apiUdks
    # return api
    #
# @fixture(scope='session')
# def apiLowLevelApis():
    # defaultLibrary = DefaultLibrary()
    # api = defaultLibrary.apiLowLevelApis
    # return api
    #
# @fixture(scope='session')
# def apiLowLevelTrafficApis():
    # defaultLibrary = DefaultLibrary()
    # api = defaultLibrary.apiLowLevelTrafficApis
    # return api
    #
# @fixture(scope='session')
# def deviceEndSystem():
    # defaultLibrary = DefaultLibrary()
    # api = defaultLibrary.deviceEndSystem
    # return api
    #
# @fixture(scope='session')
# def deviceVirtualMachine():
    # defaultLibrary = DefaultLibrary()
    # api = defaultLibrary.deviceNetworkElement
    # return api
    #
# @fixture(scope='session')
# def deviceNetworkElement():
    # defaultLibrary = DefaultLibrary()
    # api = defaultLibrary.deviceVirtualMachine
    # return api

# @fixture(params=[webdriver.Chrome, webdriver.Firefox, webdriver.Edge])
# def browser(request):
    # driver = request.param
    # drvr = driver()
    # yield drvr
    #
    # # teardown
    # drvr.quit()

def pytest_addoption(parser):
    parser.addoption("--cfg", action="store", default=None, help="yaml cfg file. Auto path search used")
    parser.addoption("--tftpserver", action="store", default=None)
    parser.addoption("--imageFamilies", action="store", default=None)
    parser.addoption("--images", action="store", default=None)
    parser.addoption("--imageTarget", action="store", default=None)
    parser.addoption("--loadImage", action="store", default=None)
    parser.addoption("--build", action="store", default=None)
    parser.addoption("--testModule_uuid", action="store", default=None)
    parser.addoption("--tftp", action="store", default=None)
    parser.addoption("--if", action="store", default=None, help="pipe seperated image family names")
    parser.addoption("--i", action="store", default=None, help="pipe seperated image names")
    parser.addoption("--p", action="store", default=None, help="install partition")
    parser.addoption("--l", action="store", default=None, help="load image method")
    parser.addoption("--b", action="store", default=None, help="build string for verification")
    parser.addoption("--u", action="store", default=None, help="job platform test module UUID")
    parser.addoption("--get_test_info", action="store", default=None, help="Dump checkdb or insert mod info")


def pytest_configure(config):
    if config.option.cfg is not None:
        from pytest_testconfig import load_yaml
        pt = PathTools()
        cfg = config.getoption("--cfg")
        print(f"TRYING TO LOAD YAML: {cfg}")
        fCfg = pt.locateCfg(cfg)
        print(f"FOUND YAML: {fCfg}")
        load_yaml(fCfg, encoding='utf-8')

def pytest_collection_finish(session):
    if session.config.option.get_test_info is not None:
        PI = PytestItems(session)
        PI.get_inventory_info()
        pytest.exit('Done!')

@fixture(scope='session', autouse=True)
def loadTestBedFirmware(request):
    status    = 'skipped'
    tftp      = request.config.getoption("--tftpserver")
    families  = request.config.getoption("--imageFamilies")
    ifiles    = request.config.getoption("--images")
    target    = request.config.getoption("--imageTarget")
    load      = request.config.getoption("--loadImage")
    build     = request.config.getoption("--build")
    uuid      = request.config.getoption("--testModule_uuid")

    if not tftp:
        tftp = request.config.getoption("--tftp")
    if not families:
        families = request.config.getoption("--if")
    if not ifiles:
        ifiles = request.config.getoption("--i")
    if not target:
        target = request.config.getoption("--p")
    if not load:
        load   = request.config.getoption("--l")
    if not build:
        build  = request.config.getoption("--b")
    if not uuid:
        uuid   = request.config.getoption("--u")

    # silently bypass download if no variables submitted
    if not families or not ifiles:
        print("[+] Load Firmware Skipped. CLI Variables not submitted")
        return

    tb = PytestConfigHelper(config)
    if not tftp and tb.lab:
        # if the lab_config.yaml file matches a 'lab' from the tb yaml, use the lab tftpserver if non-passed in.
        tb.loadAdditionalConfig(config, 'lab_config.yaml', 'econ')
        try:
            tftp = config[tb.lab]['tftpserver']
        except:
            print("[+] Load Firmware Skipped. tftp server variable not set correctly from lab_config.yaml")
            return status

    if not target:
        target = "secondary"

    if families and ifiles:
        fam_list = families.split("|")
        i_list = ifiles.split("|")
        print("\nloadFirmware has variables set to run")
        print("tftpserver: {}".format(tftp))
        print("imageFamily list: {}".format(fam_list))
        print("image list: {}".format(i_list))
        print("imageTarget: {}".format(target))
        print("loadImage: {}".format(load))
        print("build: {}".format(build))
        print("uuid: {}".format(uuid))
    else:
        print("[+] Load Firmware Skipped. CLI Variables not submitted")
        return status

    print("Test Bed - node count: {} dutlist: {} tftp: {}".format(tb.node_count, tb.dut_list, tftp))

    goDl = 1
    dl = {}
    threads = []
    q = queue.Queue()
    result = []
    xx = 0
    try:
        for dut in tb.dut_list:
            d = getattr(tb, dut)
            n = d['name']
            ip = d['ip']
            mv = d['mgmt_vlan']
            ipath = None
            try:
                tbfam = d['image_family']
                i = 0
                print("tbfam {}".format(tbfam))
                for arg_family in fam_list:
                    if tbfam == arg_family:
                        ipath = i_list[i]
                        break
                    else:
                        i += 1
            except:
                if len(i_list) == 1:
                    ipath = i_list[0]
                else:
                    print("multiple image families passed in and no 'family' variable in yaml file")
            if not ipath:
                goDl = 0

            if goDl:
                print("download n:{} tftp:{} buildpath:{} build:{} mgmtvlan:{} ip:{} tgt: {}".\
                                format(n,tftp,ipath,build,mv,ip,target))
                dl[xx] = PlatformLoadFirmware()
                t = threading.Thread(target=dl[xx].Upgrade_Netelem_Firmware, args=(str(n), str(tftp), str(ipath), \
                                                                 str(mv), str(ip), str(target), str(build), q))
                threads.append(t)
                t.start()
                xx += 1
        if goDl:
            for dt in threads:
                dt.join(600)
            for dt in threads:
                result.append(q.get_nowait())
        else:
            result = {"status": "failed"}
    except Exception as e:
        pytest.skip("Download Firmware Failed. {} res {}".format(e, result))
    if "failed" in result:
        print("[+] download result Queue contains failed")
        if uuid:
            ec = econAPI()
            getData = {
                "fieldname": "jobPlatforms_id",
                "fieldname2": "testbed_id",
                "table": "jobPlatformTestModules",
                "name": "jobPlatformTestModules_uuid",
                "value": uuid
            }
            res = ec.econRequest('tbedmgr/jobmgr/jobConfig/getTableField',
                                           rtype='post', payload=getData)
            if 'jobPlatforms_id' in res:
                jobPlat_uuid = None
                testbed_uuid = None
                jobPlat_id = res['jobPlatforms_id']
                tbed_id    = res['testbed_id']
                if jobPlat_id and jobPlat_id != "null" and jobPlat_id != "" and jobPlat_id > 0 and tbed_id > 0:
                    getData = {
                        "fieldname": "testbed_uuid",
                        "table": "testbeds",
                        "name": "testbed_id",
                        "value": tbed_id
                    }
                    res = ec.econRequest('tbedmgr/jobmgr/jobConfig/getTableField',
                                                   rtype='post', payload=getData)
                    if 'testbed_uuid' in res:
                        testbed_uuid = res['testbed_uuid']
                    getData = {
                        "fieldname": "jobPlatforms_uuid",
                        "table": "jobPlatforms",
                        "name": "jobPlatforms_id",
                        "value": jobPlat_id
                    }
                    res = ec.econRequest('tbedmgr/jobmgr/jobConfig/getTableField',
                                                   rtype='post', payload=getData)
                    if 'jobPlatforms_uuid' in res:
                        jobPlatforms_uuid = res['jobPlatforms_uuid']
                    if 'jobPlatforms_uuid' in res:
                        jobPlat_uuid = res['jobPlatforms_uuid']
                    if jobPlat_uuid and testbed_uuid:
                        tbldata = {
                            "testbed_uuid": testbed_uuid,
                            "logStatus": "downloadlocked",
                            "logStatusText": "failed download",
                            "logSource": "agent",
                            "jobPlatforms_uuid": jobPlat_uuid,
                            "jobPlatformTestModules_uuid": uuid
                        }
                        logres = ec.econRequest('tbedmgr/testbed/log', rtype='post',
                                                payload=tbldata)
                        upData = {
                            'table': 'jobPlatformTestModules',
                            'uuid': uuid,
                            'testStatus': 'downloadFailed',
                            'testbed_id': None,
                            'initialStartTimestamp': '0000-00-00 00:00:00',
                            'lastUpdatedBy': 'executor'
                        }
                        res = ec.econRequest('tbedmgr/jobmgr/jobPlatformTestModules',
                                             rtype='put', payload=upData)

                        upData = {
                            'table': 'jobPlatforms',
                            'uuid': jobPlat_uuid,
                            'status': 'downloadFailed',
                            'lastUpdatedBy': 'executor'
                        }
                        res = ec.econRequest('tbedmgr/jobmgr/jobPlatforms',
                                             rtype='put', payload=upData)

        pytest.skip("Download Firmware Failed.")
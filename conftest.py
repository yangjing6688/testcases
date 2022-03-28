import pytest
import inspect
from pytest import fixture
from pytest_testconfig import config
import threading
import queue
import logging
import sys
import requests.adapters
from datetime import datetime
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Utilities.Firmware.pytestLoadFirmware import PlatformLoadFirmware
from ExtremeAutomation.Utilities.EconClient.econ_request_api import econAPI
from ExtremeAutomation.Utilities.Framework.test_case_inventory import PytestItems
from ExtremeAutomation.Utilities.Framework.test_case_inventory import PathTools
from ExtremeAutomation.Utilities.Framework.test_selection import CheckExecution
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
    parser.addoption("--testbed", action="store", default=None, help="yaml testbed file Auto search")
    parser.addoption("--cfg", action="store", default=None, help="dup arg same as --testbed")
    parser.addoption("--env", action="store", default=None, help="yaml env file. Auto path search used")
    parser.addoption("--topo", action="store", default=None, help="yaml topo file. Auto path search used")
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
    parser.addoption("--customReportDate", action="store_true", default=False, help="Adds a report date to the report_<%m-%d-%Y_%H.%M.%S>.html file")

@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    terminal_reporter = config.pluginmanager.getplugin('terminalreporter')
    config.pluginmanager.register(TestDescriptionPlugin(terminal_reporter), 'testdescription')

def pytest_configure(config):
    # Set log levels for 3rd party packages
    # Disable all child loggers of urllib3, e.g. urllib3.connectionpool
    # logging.getLogger("urllib3").propagate = False
    patch_https_connection_pool(maxsize=100)
    patch_http_connection_pool(maxsize=100)

    if config.option.customReportDate is not None:
        config._metadata = None
        # set the timestamp
        report_date = datetime.now().strftime("%m-%d-%Y_%H.%M.%S")
        # update the pytest-html path
        config.option.htmlpath = config.option.htmlpath.replace('.html', "_" + report_date + ".html")
        print("Custom HTML Report: " + config.option.htmlpath)

    if config.option.testbed is not None or config.option.cfg is not None or config.option.env is not None or \
            config.option.topo is not None:
        from pytest_testconfig import load_yaml
        pt = PathTools()

    if config.option.cfg is not None:
        cfg = config.getoption("--cfg")
        print(f"TRYING TO LOAD CFG YAML: {cfg}")
        fCfg = pt.locateCfg(cfg)
        print(f"FOUND YAML: {fCfg}")
        if fCfg:
            load_yaml(fCfg, encoding='utf-8')
        else:
            sys.exit()
    if config.option.testbed is not None:
        cfg = config.getoption("--testbed")
        print(f"TRYING TO LOAD TESTBED YAML: {cfg}")
        fCfg = pt.locateCfg(cfg)
        print(f"FOUND YAML: {fCfg}")
        if fCfg:
            load_yaml(fCfg, encoding='utf-8')
        else:
            sys.exit()
    if config.option.env is not None:
        env = config.getoption("--env")
        print(f"TRYING TO LOAD ENV YAML: {env}")
        fEnv = pt.locateEnv(env)
        print(f"FOUND ENV YAML: {fEnv}")
        if fEnv:
            load_yaml(fEnv, encoding='utf-8')
        else:
            sys.exit()
    if config.option.topo is not None:
        topo = config.getoption("--topo")
        print(f"TRYING TO LOAD TOPO YAML: {topo}")
        fTopo = pt.locateTopo(topo)
        print(f"FOUND TOPO YAML: {fTopo}")
        if fTopo:
            load_yaml(fTopo, encoding='utf-8')
        else:
            sys.exit()

def pytest_collection_finish(session):
    if session.config.option.get_test_info is not None:
        PI = PytestItems(session)
        PI.get_inventory_info()
        pytest.exit('Done!')

@pytest.fixture(autouse=True)
def skip_check(request):
    # @mark.required_platform('Stack')
    # @mark.skip_platform('Stack', 'VPEX')
    # @mark.required_capability('Fabric')
    # @mark.required_capability_dutlist('Fabric', '1,2,3')   TO BE DEVELOPED
    # @mark.start_version('EXOS 31.1')    TO BE DEVELOPED
    # @mark.end_version('EXOS 40.1')     TO BE DEVELOPED
    if request.node.get_closest_marker('skip_platform'):
        chkExec = CheckExecution(request, config)
        out = chkExec.skipPlatform()
        if out:
            pytest.skip(f"skipped {request.node.name} on this platform: {out}")
    if request.node.get_closest_marker('required_platform'):
        chkExec = CheckExecution(request, config)
        out = chkExec.requiredPlatform()
        if out[0]:
            pass
        else:
            pytest.skip(f"Skipped {request.node.name}. {out[1][0]} platform is required on DUT1")
    if request.node.get_closest_marker('required_capability'):
        chkExec = CheckExecution(request, config)
        out = chkExec.requiredCapability()
        if out[0]:
            pass
        else:
            pytest.skip(f"skipped {request.node.name} on this platform: No support for {out[1]}")
    if request.node.get_closest_marker('start_version'):
        chkExec = CheckExecution(request, config)
        out = chkExec.startVersion()
        if out:
            pytest.skip(f"skipped {request.node.name} on this verions: {out}")
    if request.node.get_closest_marker('end_version'):
        chkExec = CheckExecution(request, config)
        out = chkExec.endVersion()
        if out:
            pytest.skip(f"skipped {request.node.name} on this version: {out}")
    if request.node.get_closest_marker('required_nos'):
        chkExec = CheckExecution(request, config)
        out = chkExec.requiredNos()
        if not out[0]:
            pytest.skip(f"skipped {request.node.name} DUT1 must be NOS: {out[1]}")
    if request.node.get_closest_marker('skip_nos'):
        chkExec = CheckExecution(request, config)
        out = chkExec.skipNos()
        if out[0]:
            pytest.skip(f"skipped {request.node.name} NOS is not supported: {out[1]}")

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

class TestDescriptionPlugin:

    def __init__(self, terminal_reporter):
        self.terminal_reporter = terminal_reporter
        self.logger =  logging.getLogger('HEADER')
        self.desc = None

        self.BLUE = '\033[94m'
        self.BOLD = '\033[1m'
        self.END = '\033[0m'

    def pytest_runtest_protocol(self, item):
        self.desc = inspect.getdoc(item.obj)

    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_runtest_setup(self, item):
        if self.terminal_reporter.verbosity == 0:
            yield
        else:
            self.logger.info(self.BLUE + self.BOLD + f'**********************************************************************************************' + self.END)
            self.logger.info(self.BLUE + self.BOLD + f'*****************  Test Case SETUP '+ self.END)
            self.logger.info(self.BLUE + self.BOLD + f'*****************  Test Case: {item.location[2]}' + self.END)
            self.logger.info(self.BLUE + self.BOLD + f'**********************************************************************************************\n'+ self.END)
            yield

    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_runtest_teardown(self, item, nextitem):
        if self.terminal_reporter.verbosity == 0:
            yield
        else:
            self.logger.info(self.BLUE + self.BOLD + f'**********************************************************************************************'+ self.END)
            self.logger.info(self.BLUE + self.BOLD + f'****************  Test Case TEARDOWN '+ self.END)
            self.logger.info(self.BLUE + self.BOLD + f'****************  Test Case: {item.location[2]}' + self.END)
            self.logger.info(self.BLUE + self.BOLD + f'**********************************************************************************************\n'+ self.END)
            yield

    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_runtest_logstart(self, nodeid, location):
        if self.terminal_reporter.verbosity == 0:
            yield
        else:
            self.logger.info(self.BLUE + self.BOLD + f'**********************************************************************************************'+ self.END)
            self.logger.info(self.BLUE + self.BOLD + f'****************  Test Case: {location[2]} START' + self.END)
            if self.desc:
                self.logger.info(self.BLUE + self.BOLD + f'****************  '+ self.END)
                self.logger.info(self.BLUE + self.BOLD + f'****************  Description: {self.desc}'+ self.END)
            self.logger.info(self.BLUE + self.BOLD + f'**********************************************************************************************\n'+ self.END)
            yield

    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_runtest_logfinish(self, nodeid, location):
        if self.terminal_reporter.verbosity == 0:
            yield
        else:
            self.logger.info(self.BLUE + self.BOLD + f'**********************************************************************************************' + self.END)
            self.logger.info(self.BLUE + self.BOLD + f'****************  Test Case: {location[2]} END' + self.END)
            self.logger.info(self.BLUE + self.BOLD + f'**********************************************************************************************\n' + self.END)
            yield

def patch_http_connection_pool(**constructor_kwargs):
    """
    This allows to override the default parameters of the
    HTTPConnectionPool constructor.
    For example, to increase the poolsize to fix problems
    with "HttpConnectionPool is full, discarding connection"
    call this function with maxsize=16 (or whatever size
    you want to give to the connection pool)
    """
    from urllib3 import connectionpool, poolmanager

    class MyHTTPConnectionPool(connectionpool.HTTPConnectionPool):
        def __init__(self, *args,**kwargs):
            kwargs.update(constructor_kwargs)
            super(MyHTTPConnectionPool, self).__init__(*args,**kwargs)
    poolmanager.pool_classes_by_scheme['http'] = MyHTTPConnectionPool

def patch_https_connection_pool(**constructor_kwargs):
    """
    This allows to override the default parameters of the
    HTTPConnectionPool constructor.
    For example, to increase the poolsize to fix problems
    with "HttpSConnectionPool is full, discarding connection"
    call this function with maxsize=16 (or whatever size
    you want to give to the connection pool)
    """
    from urllib3 import connectionpool, poolmanager

    class MyHTTPSConnectionPool(connectionpool.HTTPSConnectionPool):
        def __init__(self, *args,**kwargs):
            kwargs.update(constructor_kwargs)
            super(MyHTTPSConnectionPool, self).__init__(*args,**kwargs)
    poolmanager.pool_classes_by_scheme['https'] = MyHTTPSConnectionPool
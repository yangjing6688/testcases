# Built-in imports
from collections import defaultdict
from dataclasses import dataclass
from email.policy import default
import inspect
import logging
import queue
import sys
import threading
from datetime import datetime
from pprint import pformat
import time
import os
import re
import string
import random
import subprocess
from ExtremeAutomation.Apis.NetworkElement.GeneratedApis.CommandApis.CLI import policy


from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from contextlib import contextmanager
# Our imports
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Utilities.EconClient.econ_request_api import econAPI
from ExtremeAutomation.Utilities.Firmware.pytestLoadFirmware import PlatformLoadFirmware
from ExtremeAutomation.Utilities.Framework.test_case_inventory import (
    PathTools,
    PytestItems)
from ExtremeAutomation.Utilities.Framework.test_selection import CheckExecution

# 3rd party imports
import pytest
from pytest import (
    fixture,
    hookimpl)
from pytest_testconfig import config
from yaml import safe_load as yaml_safe_load


@fixture()
# used to skip test cases
def test_case_skip_check(request):
    request.instance.executionHelper.testSkipCheck()
    yield

@fixture()
# Test case setup and tear down
def test_case_started_ended_print(request):
    print("TEST STARTED")
    yield
    print("TEST END")
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
    parser.addoption("--tftp", "--tftpserver", dest="tftpServer", action="store", default=None)
    parser.addoption("--if", "--imageFamilies", dest="imageFamilies", action="store", default=None, help="pipe seperated image family names")
    parser.addoption("--i", "--images", dest="images", action="store", default=None, help="pipe seperated image names")
    parser.addoption("--p", "--imageTarget", dest="imageTarget", action="store", default=None, help="install partition")
    parser.addoption("--l", "--loadImage", dest="loadImage", action="store", default=None, help="load image method")
    parser.addoption("--b", "--build", dest="build", action="store", default=None, help="build string for verification")
    parser.addoption("--u", "--testModule_uuid", dest="testModule_uuid", action="store", default=None, help="job platform test module UUID")
    parser.addoption("--get_test_info", action="store", default=None, help="Dump checkdb or insert mod info")
    parser.addoption("--customReportDate", action="store_true", default=False, help="Adds a report date to the report_<date>.html file")
    parser.addoption("--customReportTitle", action="store", default=None, help="Adds a Custom title to the report htmls file")

def pytest_html_report_title(report):
    # Update title on web page
    global custom_report_title
    if custom_report_title:
        report.title = custom_report_title

def pytest_sessionfinish(session):
    # Update title in browser tab
    global custom_report_title
    if custom_report_title:
        htmlfile = session.config.getoption('htmlpath')
        with open(htmlfile) as readFile:
            text = readFile.read().replace('<title>Test Report</title>', '<title>' + custom_report_title +'</title>')
        with open(htmlfile, "w") as writeFile:
            writeFile.write(text)

@hookimpl(trylast=True)
def pytest_configure(config):
    terminal_reporter = config.pluginmanager.getplugin('terminalreporter')
    config.pluginmanager.register(TestDescriptionPlugin(terminal_reporter), 'testdescription')

def pytest_configure(config):
    try:
        global custom_report_title
        # Set log levels for 3rd party packages
        # Disable all child loggers of urllib3, e.g. urllib3.connectionpool
        # logging.getLogger("urllib3").propagate = False
        patch_https_connection_pool(maxsize=100)
        patch_http_connection_pool(maxsize=100)

        if config.option.customReportDate:
            # set the timestamp
            report_date = datetime.now().strftime("%m-%d-%Y_%H.%M.%S")
            # update the pytest-html path
            config.option.htmlpath = config.option.htmlpath.replace('.html', "_" + report_date + ".html")
            print("Custom HTML Report: " + config.option.htmlpath)

        custom_report_title = config.option.customReportTitle

        # Grab testbed/topo info if ran with --tc-file option
        #
        if config.option.testconfig:
            # testconfig is a list of test config files
            for item in config.option.testconfig:
                try:
                    if "TestBeds" in item:
                        header = "Testbed"
                    elif "Environments" in item and "topo" in item:
                        header = "Topology"
                    else:
                        continue

                    # Grab info for HTML report
                    with open(item, 'r', encoding='utf-8') as f:
                        cfg_file = yaml_safe_load(f.read())

                    config._metadata[f"{header} - File Path"] = item
                    for keyword, value in cfg_file.items():
                        # Trim tgen & e-mail info from testbeds
                        if header == "Testbed":
                            if not keyword.startswith("tgen") and keyword != "mails":
                                config._metadata[f"{header} - {keyword}"] = pformat(value, depth=1)
                        else:
                            config._metadata[f"{header} - {keyword}"] = value
                except Exception as e:
                    # Quietly bypass errors
                    print(e)

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
                # Grab info for HTML report
                with open(fCfg, 'r', encoding='utf-8') as f:
                    testbed = yaml_safe_load(f.read())

                config._metadata["Testbed - File Path"] = fCfg
                for keyword, value in testbed.items():
                    if not keyword.startswith("tgen") and keyword != "mails":
                        config._metadata[f"Testbed - {keyword}"] = pformat(value, depth=1)

                # Load testbed into pytest
                load_yaml(fCfg, encoding='utf-8')
            else:
                sys.exit()

        if config.option.env is not None:
            env = config.getoption("--env")
            print(f"TRYING TO LOAD ENV YAML: {env}")
            fEnv = pt.locateEnv(env)
            print(f"FOUND ENV YAML: {fEnv}")
            if fEnv:
                # Load environment into pytest
                load_yaml(fEnv, encoding='utf-8')
            else:
                sys.exit()

        if config.option.topo is not None:
            topo = config.getoption("--topo")
            print(f"TRYING TO LOAD TOPO YAML: {topo}")
            fTopo = pt.locateTopo(topo)
            print(f"FOUND TOPO YAML: {fTopo}")
            if fTopo:
                # Grab info for HTML report
                with open(fTopo, 'r', encoding='utf-8') as f:
                    topology = yaml_safe_load(f.read())

                config._metadata["Topology - File Path"] = fTopo
                for keyword, value in topology.items():
                    config._metadata[f"Topology - {keyword}"] = value

                # Load topology into pytest
                load_yaml(fTopo, encoding='utf-8')
            else:
                sys.exit()
    except Exception as e:
        print('Warning pytest_configure: ' +str(e))

def pytest_collection_finish(session):
    if session.config.option.get_test_info is not None:
        PI = PytestItems(session)
        PI.get_inventory_info()
        pytest.exit('Done!')

@fixture(autouse=True)
def skip_check(request):
    try:
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
            if not out[0]:
                pytest.skip(f"Skipped {request.node.name}. {out[1][0]} platform is required on DUT1")
        if request.node.get_closest_marker('required_capability'):
            chkExec = CheckExecution(request, config)
            out = chkExec.requiredCapability()
            if not out[0]:
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
    except Exception as e:
        print("Warning skip_check: " +str(e))

@fixture(scope='session', autouse=True)
def loadTestBedFirmware(request):
    try:
        status    = 'skipped'
        tftp      = request.config.option.tftpServer
        families  = request.config.option.imageFamilies
        ifiles    = request.config.option.images
        target    = request.config.option.imageTarget
        load      = request.config.option.loadImage
        build     = request.config.option.build
        uuid      = request.config.option.testModule_uuid

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
    except Exception as e:
        print("Warning loadTestBedFirmware: " + str(e))

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

    @hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_runtest_setup(self, item):
        if self.terminal_reporter.verbosity == 0:
            yield
        else:
            self.logger.info(self.BLUE + self.BOLD + f'**********************************************************************************************' + self.END)
            self.logger.info(self.BLUE + self.BOLD + f'*****************  Test Case SETUP '+ self.END)
            self.logger.info(self.BLUE + self.BOLD + f'*****************  Test Case: {item.location[2]}' + self.END)
            self.logger.info(self.BLUE + self.BOLD + f'**********************************************************************************************\n'+ self.END)
            yield

    @hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_runtest_teardown(self, item, nextitem):
        if self.terminal_reporter.verbosity == 0:
            yield
        else:
            self.logger.info(self.BLUE + self.BOLD + f'**********************************************************************************************'+ self.END)
            self.logger.info(self.BLUE + self.BOLD + f'****************  Test Case TEARDOWN '+ self.END)
            self.logger.info(self.BLUE + self.BOLD + f'****************  Test Case: {item.location[2]}' + self.END)
            self.logger.info(self.BLUE + self.BOLD + f'**********************************************************************************************\n'+ self.END)
            yield

    @hookimpl(hookwrapper=True, tryfirst=True)
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

    @hookimpl(hookwrapper=True, tryfirst=True)
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


@pytest.fixture(scope="session")
def login_xiq(loaded_config, utils):

    @contextmanager
    def func(username=loaded_config['tenant_username'],
             password=loaded_config['tenant_password'],
             url=loaded_config['test_url'],
             capture_version=False, code="default", incognito_mode="False"):

        xiq = XiqLibrary()
        time.sleep(5)

        try:
            assert xiq.login.login_user(
                username, password, capture_version=capture_version, code=code, url=url, incognito_mode=incognito_mode)
            yield xiq
        except Exception as exc:
            print(repr(exc))
            from extauto.common.CloudDriver import CloudDriver
            CloudDriver().close_browser()
            raise exc
        finally:
            try:
                xiq.login.logout_user()
                xiq.login.quit_browser()
            except:
                pass
    return func


@pytest.fixture(scope="session")
def enter_switch_cli(network_manager, close_connection):

    @contextmanager
    def func(dut):
        try:
            network_manager.connect_to_network_element_name(dut.name)
            yield
        finally:
            close_connection(dut)
    return func


def change_device_management_settings(xiq, option, platform, retries=5, step=5):
    
    for _ in range(retries):
        try:
            xiq.xflowsglobalsettingsGlobalSetting.change_exos_device_management_settings(
                option=option, platform=platform)
        except Exception as exc:
            print(repr(exc))
            time.sleep(step)
        else:
            xiq.xflowscommonNavigator.navigate_to_devices()
            break
    else:
        pytest.fail("Failed to change exos device management settings")


def deactivate_xiq_libraries_and_logout(xiq):
    xiq.login.logout_user()
    xiq.login.quit_browser()


def create_location(xiq, location):
    xiq.xflowsmanageLocation.delete_location_building_floor(*location.split(","))
    xiq.xflowsmanageLocation.create_location_building_floor(*location.split(","))


def generate_template_for_given_model(platform, model, slots=""):

    if platform.lower() == 'stack':
        if not slots:
            return -1

        model_list = []
        sw_model = ""
        model_units = None

        for eachslot in slots:
            if "SwitchEngine" in eachslot:
                mat = re.match('(.*)(Engine)(.*)', eachslot)
                model_md = mat.group(1) + ' ' + mat.group(2) + ' ' + mat.group(3).replace('_', '-')
                switch_type=re.match('(\d+).*', mat.group(3).split('_')[0]).group(1)
                sw_model = 'Switch Engine ' + switch_type + '-Series-Stack'

            else:
                model_act = eachslot.replace('10_G4', '10G4')
                m = re.match(r'(X\d+)(G2)(.*)', model_act)
                model_md = m.group(1) + '-' + m.group(2) + m.group(3).replace('_', '-')
                sw_model = m.group(1) + '-' + m.group(2) + '-Series-Stack'
            model_list.append(model_md)

        model_units = ','.join(model_list)
        return sw_model,model_units

    elif "Engine" in model:
        mat = re.match('(.*)(Engine)(.*)', model)
        sw_model = mat.group(1) + ' ' + mat.group(2) + ' ' + mat.group(3).replace('_', '-')

    elif "G2" in model:
        model_act = model.replace('10_G4', '10G4')
        m = re.match(r'(X\d+)(G2)(.*)', model_act)
        sw_model = m.group(1) + '-' + m.group(2) + m.group(3).replace('_', '-')

    else:
        sw_model = model.replace('_', '-')
    return sw_model


@pytest.fixture(scope="session")
def close_connection(network_manager):
    def func(dut):
        try:
            network_manager.device_collection.remove_device(dut.name)
            network_manager.close_connection_to_network_element(dut.name)
        except Exception as exc:
            print(exc)
    return func


def get_virtual_router(dev_cmd, dut):
    
    result = dev_cmd.send_cmd(dut.name, 'show vlan', max_wait=10, interval=2)
    output = result[0].cmd_obj.return_text
    pattern = f'(\w+)(\s+)(\d+)(\s+)({dut.ip})(\s+)(\/.*)(\s+)(\w+)(\s+/)(.*)(VR-\w+)'
    match = re.search(pattern, output)

    if match:
        print(f"Mgmt Vlan Name : {match.group(1)}")
        print(f"Vlan ID        : {match.group(3)}")
        print(f"Mgmt IPaddress : {match.group(5)}")
        print(f"Active ports   : {match.group(9)}")
        print(f"Total ports    : {match.group(11)}")
        print(f"Virtual router : {match.group(12)}")

        if int(match.group(9)) > 0:
            return match.group(12)
        else:
            print(f"There is no active port in the mgmt vlan {match.group(1)}")
            return -1
    else:
        print("Pattern not found, unable to get virtual router info!")
        return -1


@pytest.fixture(scope="session")
def navigator():
    from extauto.xiq.flows.common.Navigator import Navigator
    return Navigator()


@pytest.fixture(scope="session")
def utils():
    from extauto.common.Utils import Utils
    return Utils()


@pytest.fixture(scope="session")
def browser():
    from extauto.common.CloudDriver import CloudDriver
    return CloudDriver()


@pytest.fixture(scope="session")
def auto_actions():
    from common.AutoActions import AutoActions
    return AutoActions()


@pytest.fixture(scope="session")
def configure_iq_agent(dev_cmd, loaded_config, enter_switch_cli):
    
    def func(duts):
        
        def worker(dut):
            with enter_switch_cli(dut):
                if dut.cli_type.upper() == "EXOS":
                    dev_cmd.send_cmd_verify_output(
                        dut.name, 'show process iqagent', 'Ready', max_wait=30, interval=10)
                    dev_cmd.send_cmd(
                        dut.name, 'disable iqagent', max_wait=10, interval=2,
                        confirmation_phrases='Do you want to continue?', confirmation_args='y')
                    
                    dev_cmd.send_cmd(dut.name, 'configure iqagent server ipaddress none', max_wait=10, interval=2)
                    vr_name = get_virtual_router(dev_cmd, dut)
                    if vr_name == -1:
                        print("Error: Can't extract Virtual Router information")
                        # return -1
                    dev_cmd.send_cmd(dut.name, f'configure iqagent server vr {vr_name}', max_wait=10, interval=2)
                
                    dev_cmd.send_cmd(
                        dut.name, 'configure iqagent server ipaddress ' + loaded_config['sw_connection_host'],
                        max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)
                
                elif dut.cli_type.upper() == "VOSS":
                    dev_cmd.send_cmd(dut.name, 'enable', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'configure terminal', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'application', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'no iqagent enable', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'iqagent server ' + loaded_config['sw_connection_host'],
                                    max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'iqagent enable', max_wait=10, interval=2)
                    dev_cmd.send_cmd_verify_output(dut.name, 'show application iqagent', 'true', max_wait=30,
                                                    interval=10)
                    dev_cmd.send_cmd(dut.name, 'exit', max_wait=10, interval=2)

                elif dut.cli_type.upper() == "AH-FASTPATH":
                    try:
                        dev_cmd.send_cmd(dut.name, "enable")
                    except:
                        dev_cmd.send_cmd(dut.name, "exit")
                    dev_cmd.send_cmd(
                        dut.name, f'hivemanager address {loaded_config["sw_connection_host"]}', max_wait=10, interval=2)
                    dev_cmd.send_cmd(
                        dut.name, 'application start hiveagent', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, "exit")
                time.sleep(10)
        
        threads = []
        try:
            for dut in duts:
                thread = threading.Thread(target=worker, args=(dut, ))
                threads.append(thread)
                thread.start()
        finally:
            for thread in threads:
                thread.join()
    return func


@pytest.fixture(scope="session")
def get_default_password(navigator, utils, auto_actions):
    
    def func(xiq):
        xiq.xflowscommonDevices._goto_devices()
        navigator.navigate_to_global_settings_page()
        
        menu, _ = utils.wait_till(
            func=xiq.xflowsglobalsettingsGlobalSetting.get_device_management_settings_menu,
            silent_failure=True,
            delay=4
        )
        assert menu, "Failed to get the device management settings menu"
        
        utils.wait_till(func=lambda: auto_actions.click(menu) == 1)
        
        password, _ = utils.wait_till(
            func=xiq.xflowsglobalsettingsGlobalSetting.get_device_management_settings_password,
            silent_failure=True,
            delay=4
        )
        assert password, "Failed to get the default device passowrd"
        return password.get_attribute('value')
    return func


@pytest.fixture(scope="session", autouse=True)
def onboarding_location():
    pool = list(string.ascii_letters) + list(string.digits)
    return f"Salem_{''.join(random.sample(pool, k=4))},Northeastern_{''.join(random.sample(pool, k=4))}," \
           f"Floor_{''.join(random.sample(pool, k=4))}"


@pytest.fixture(scope="session")
def check_duts_are_reachable(utils):
    
    results = []
    
    def func(duts, results=results, retries=3):
        def worker(dut):
            
            for _ in range(retries):
                try:
                    ping_response = subprocess.Popen(
                        ["ping", "-c 1", dut.ip], stdout=subprocess.PIPE).stdout.read().decode()
                    utils.print_info(ping_response)
                    if re.search("0% packet loss", ping_response):
                        results.append(f"({dut.ip}): Successfully verified that this dut is reachable: {dut}")
                        return
                except:
                    time.sleep(1)
            else:
                results.append(f"({dut.ip}): This dut is not reachable: {dut}\n{ping_response}")

        threads = []
        try:
            for dut in duts:
                thread = threading.Thread(target=worker, args=(dut, ))
                threads.append(thread)
                thread.start()
        finally:
            for thread in threads:
                thread.join()
        
        for message in results:
            utils.print_info(message)
        
        if any(re.search("The chosen dut is not reachable", message) for message in results):
            pytest.fail(f"Not all the duts are reachable:\n{results}")
        else:
            utils.print_info("All the duts are reachable!")
    return func


def get_dut(tb, os, platform=""):
    for dut_index in [f"dut{i}" for i in range(3)]:
        if getattr(tb, dut_index, {}).get("cli_type", "").upper() == os.upper():
            current_platform = getattr(tb, dut_index).get("platform", "").upper()
            
            if platform.upper() == "STACK":
                if current_platform == "STACK":
                    return getattr(tb, dut_index) 
            else:
                if current_platform != "STACK":
                    return getattr(tb, dut_index) 


@pytest.fixture(scope="session")
def network_manager():
    from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import \
        NetworkElementConnectionManager
    return NetworkElementConnectionManager()


@pytest.fixture(scope="session")
def testbed():
    return PytestConfigHelper(config)


@pytest.fixture(scope="session")
def loaded_config():
    config['${TEST_NAME}'] = "onboarding"
    config['${OUTPUT DIR}'] = os.getcwd()
    for word in ["tenant_username", "tenant_password", "test_url"]:
        config[f"${{{word.upper()}}}"] = config[word]
    return config


@pytest.fixture(scope="session")
def dev_cmd():
    from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
    defaultLibrary = DefaultLibrary()
    return defaultLibrary.deviceNetworkElement.networkElementCliSend


@pytest.fixture(scope="session")
def check_devices_are_onboarded(utils):
    def func(xiq, dut_list, timeout=180):
        
        xiq.xflowscommonDevices.column_picker_select("MAC Address")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                
                xiq.xflowsmanageDevices.refresh_devices_page()
                utils.wait_till(timeout=5)

                devices, _ = utils.wait_till(
                    func=xiq.xflowscommonDeviceCommon.get_device_grid_rows,
                    exp_func_resp=True,
                    silent_failure=True
                )
                assert devices, "Did not find any onboarded devices in the XIQ"

                found = True
                for dut in dut_list:
                    for device in devices:
                        if any([dut.mac.upper() in device.text, dut.mac.lower() in device.text]):
                            utils.print_info(f"Successfully found device with mac='{dut.mac}'")
                            break
                    else:
                        utils.print_info(f"Did not find device with mac='{dut.mac}'")
                        found = False
                assert found, 'Not all devices are found in the Devices list'
                
                try:
                    for dut in dut_list:
                        xiq.xflowscommonDevices.wait_until_device_online(dut.mac)
                        res = xiq.xflowscommonDevices.get_device_status(device_serial=dut.mac)
                        assert res == 'green', f"The device did not come up successfully in the XIQ; Device: {dut}"
                except Exception as exc:
                    utils.print_info(repr(exc))
                else:
                    break
            except Exception as err:
                utils.print_info(f"Not all the devices are up yet: {repr(err)}")
                utils.wait_till(timeout=10)
        else:
            pytest.fail("Not all the devices are up in XIQ")

    return func


def cleanup(xiq, duts=[], onboarding_location='', network_policies=[], templates_switch=[], slots=1):

    try:
        for dut in duts:
            xiq.xflowscommonDevices._goto_devices()
            xiq.xflowscommonDevices.delete_device(
                device_mac=dut.mac)
        if onboarding_location:
            xiq.xflowsmanageLocation.delete_location_building_floor(*onboarding_location.split(","))
        for network_policy in network_policies:
            xiq.xflowsconfigureNetworkPolicy.delete_network_policy(network_policy)
        for template_switch in templates_switch:
            for _ in range(slots):
                xiq.xflowsconfigureCommonObjects.delete_switch_template(template_switch)
    except Exception as exc:
        print(repr(exc))


@pytest.fixture(scope="session")
def configure_network_policies(utils):
    
    def func(xiq, dut_config):
        for dut, data in dut_config.items():
            
            network_policy = data['policy_name']
            template_switch = data['template_name']
            dut_info = data['info']
            
            assert xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                network_policy), \
                f"Policy {network_policy} wasn't created successfully "
            
            if dut_info.platform.upper() == "STACK":
                xiq.xflowsconfigureSwitchTemplate.add_5520_sw_stack_template(
                    dut_info.model_units, network_policy,
                    dut_info.model_template, template_switch)
            else:
                sw_model_template = generate_template_for_given_model(
                    dut_info.platform, dut_info.model)
                xiq.xflowsconfigureSwitchTemplate.add_sw_template(
                    network_policy, sw_model_template, template_switch)
                assert xiq.xflowsmanageDevices.assign_network_policy_to_switch(
                    policy_name=network_policy, serial=dut_info.serial) == 1, \
                    f"Couldn't assign policy {network_policy} to device {dut}"
    return func


@pytest.fixture(scope="session")
def dut_stack_model_update(utils):
    
    def func(dut, stack_dict):
        if ("Series Stack" in dut.model) and (dut.model_units is not None or dut.model_units != ""):
            utils.print_info("Conftest with Stack: ", dut.model, " and units: ", dut.model_units)
        else:
            utils.print_info("Try to update Stack Template Model and Units")
            
            dut.model_template = ""
            if dut.cli_type.upper() == "EXOS":
                dut.model_template = "Switch Engine "
                if "Engine" in dut.model:
                    dut.model_template += dut.model.split("Engine", 1)[1].replace('_', '-')
                    dut.model_template = dut.model_template.split("-", 1)[0]
                    if not dut.model_template[-1].isdigit():
                        dut.model_template = dut.model_template[0:len(dut.model_template) - 1]
                else:
                    dut.model_template += dut.model.replace('_', '-')
                dut.model_template += "-Series-Stack"

                stack_units_model = []
                for key in stack_dict.keys():
                    slot_keys = stack_dict[key]
                    if slot_keys and 'model' in slot_keys:
                        if slot_keys['model'] is not None:
                            stack_units_model.append(slot_keys['model'])
                print(f"Switch model list is {stack_units_model}")

                dut.model_units = ""
                for model in stack_units_model:
                    model_unit = "Switch Engine "
                    if "Engine" in model:
                        model_unit += model.split("Engine", 1)[1].replace('_', '-')
                    else:
                        model_unit += model.replace('_', '-')
                    dut.model_units += model_unit + ","
                dut.model_units = dut.model_units.strip(",")
                print(f"Dut model units are {dut.model_units}")
            utils.print_info("Conftest with Stack: ", dut.model_template, " and units: ", dut.model_units)
    return func


onboard_one_node_flag = False
onboard_two_node_flag = False
onboard_stack_flag = False


def pytest_collection_modifyitems(session, items):
    
    global onboard_one_node_flag
    global onboard_two_node_flag
    global onboard_stack_flag
    
    testbed = PytestConfigHelper(config)
    nodes = list(filter(lambda d: d is not None, [getattr(testbed, f"dut{i}", None) for i in range(1, 5)]))
    temp_items = items[:]

    standalone_nodes = [node for node in nodes if node.get("platform", "").upper() != "STACK"]
    stack_nodes = [node for node in nodes if node not in standalone_nodes]

    onboard_stack_flag = bool(stack_nodes)
    if not onboard_stack_flag:
        temp_items = [
            item for item in temp_items if 'testbed_stack' not in [marker.name for marker in item.own_markers]]

    onboard_two_node_flag = len(standalone_nodes) > 1
    if not onboard_two_node_flag:
        temp_items = [
            item for item in temp_items if 'testbed_2_node' not in [marker.name for marker in item.own_markers]]
    
    onboard_one_node_flag = len(standalone_nodes) >= 1
    if not onboard_one_node_flag:
        temp_items = [
            item for item in temp_items if 'testbed_1_node' not in [marker.name for marker in item.own_markers]]
    items[:] = temp_items


@pytest.fixture(scope="session")
def nodes(testbed):
    return list(filter(lambda d: d is not None, [getattr(testbed, f"dut{i}", None) for i in range(1, 5)]))


@pytest.fixture(scope="session")
def onboard(request):

    onboarding_location = request.getfixturevalue("onboarding_location")
    configure_iq_agent = request.getfixturevalue("configure_iq_agent")
    check_devices_are_onboarded = request.getfixturevalue("check_devices_are_onboarded")
    loaded_config = request.getfixturevalue("loaded_config")
    check_duts_are_reachable = request.getfixturevalue("check_duts_are_reachable")
    utils = request.getfixturevalue("utils")
    close_connection = request.getfixturevalue("close_connection")
    configure_network_policies = request.getfixturevalue("configure_network_policies")
    dut_stack_model_update = request.getfixturevalue("dut_stack_model_update")
    login_xiq = request.getfixturevalue("login_xiq")
    nodes = request.getfixturevalue("nodes")
    standalone_nodes = [node for node in nodes if node.get("platform", "").upper() != "STACK"]
    stack_nodes = [node for node in nodes if node not in standalone_nodes]

    dut_list = []
    stack_dut = None

    if onboard_two_node_flag:
        dut_list.extend(standalone_nodes[:2])
    elif onboard_one_node_flag:
        dut_list.append(standalone_nodes[0])
    
    if onboard_stack_flag:
        stack_dut = stack_nodes[0]
        dut_list.append(stack_dut)
        dut_stack_model_update(stack_dut, stack_dut.stack)

    check_duts_are_reachable(dut_list)
    configure_iq_agent(dut_list)
    
    dut_config = defaultdict(lambda: {})
    pool = list(string.ascii_letters) + list(string.digits)
    
    for dut in dut_list:
        dut_config[dut.name]["policy_name"] = f"np_{''.join(random.sample(pool, k=7))}"
        dut_config[dut.name]['template_name'] = f"template_{''.join(random.sample(pool, k=7))}"
        dut_config[dut.name]['info'] = dut

    try:
        
        with login_xiq(
                username=loaded_config['tenant_username'],
                password=loaded_config['tenant_password'],
                url=loaded_config['test_url']) as xiq:

            change_device_management_settings(
                xiq, option="disable", platform=dut.cli_type.upper())
            
            cleanup(xiq=xiq, duts=dut_list)
            create_location(xiq, onboarding_location)

            for dut in dut_list:
                xiq.xflowsmanageSwitch.onboard_switch(
                    dut.serial, device_os=dut.cli_type,
                    location=onboarding_location)

            check_devices_are_onboarded(xiq, dut_list)
            
            configure_network_policies(xiq, dut_config)

        yield dut_list, dut_config

    finally:
        with login_xiq(
                username=loaded_config['tenant_username'],
                password=loaded_config['tenant_password'],
                url=loaded_config['test_url']) as xiq:
        
            try:
                cleanup(
                    xiq=xiq, 
                    duts=dut_list, 
                    network_policies=[dut_info['policy_name'] for dut_info in dut_config.values()],
                    templates_switch=[dut_info['template_name'] for dut_info in dut_config.values()],
                    onboarding_location=onboarding_location,
                    slots=len(stack_dut.stack) if stack_dut is not None else 1
                )
                close_connection(dut)
            except Exception as exc:
                utils.print_info(repr(exc))


@pytest.fixture(scope="session")
def onboarded_one_node(request):
    if onboard_one_node_flag or onboard_two_node_flag:
        dut_list, _ = request.getfixturevalue("onboard")
        return [dut for dut in dut_list if dut.platform.upper() != "STACK"][0]
    return


@pytest.fixture(scope="session")
def onboarded_two_node(request):
    if onboard_two_node_flag:
        dut_list, _ = request.getfixturevalue("onboard")
        return [dut for dut in dut_list if dut.platform.upper() != "STACK"][:2]
    return


@pytest.fixture(scope="session")
def onboarded_stack(request):
    if onboard_stack_flag:
        dut_list, _ = request.getfixturevalue("onboard")
        return [dut for dut in dut_list if dut.platform.upper() == "STACK"][0]
    return


@pytest.fixture(scope="session")
def policy_config(request):
    if onboard_one_node_flag or onboard_two_node_flag or onboard_stack_flag:
        _, policy_config = request.getfixturevalue("onboard")
        return policy_config
    return


@pytest.fixture(scope="session")
def dut_list(request):
    if onboard_one_node_flag or onboard_two_node_flag or onboard_stack_flag:
        dut_list, _ = request.getfixturevalue("onboard")
        return dut_list
    return
 
 
@pytest.fixture(scope="session")
def dut_ports(enter_switch_cli, dev_cmd, dut_list):
    
    ports = {}
    
    def worker(dut):
        with enter_switch_cli(dut):
            if dut.cli_type.upper() == "VOSS":
                dev_cmd.send_cmd(
                    dut.name, 'enable', max_wait=10, interval=2)
                output = dev_cmd.send_cmd(
                    dut.name, 'show int gig int | no-more',
                    max_wait=10, interval=2)[0].return_text
                
                p = re.compile(r'^\d+\/\d+', re.M)
                match_port = re.findall(p, output)

                p2 = re.compile(r'\d+\/\d+\/\d+', re.M)
                filtered = [port for port in match_port if not p2.match(port)]
                ports[dut.name] = filtered
            
            elif dut.cli_type.upper() == "EXOS":
                
                dev_cmd.send_cmd(
                    dut.name, 'disable cli paging', max_wait=10, interval=2)
                output = dev_cmd.send_cmd(
                    dut.name, 'show ports info', max_wait=20, interval=5)[0].return_text
                p = re.compile(r'^\d+:\d+', re.M)
                match_port = re.findall(p, output)
                is_stack = True
                if len(match_port) == 0:
                    is_stack = False
                    p = re.compile(r'^\d+', re.M)
                    match_port = re.findall(p, output)

                p_notPresent = re.compile(r'^\d+:\d+.*NotPresent.*$', re.M) if is_stack else re.compile(r'^\d+.*NotPresent.*$', re.M)
                parsed_info = re.findall(p_notPresent, output)

                for port in parsed_info:
                    port_num = re.findall(p, port)
                    match_port.remove(port_num[0])
                ports[dut.name] = match_port

    threads = []
    try:
        for dut in dut_list:
            thread = threading.Thread(target=worker, args=(dut, ))
            threads.append(thread)
            thread.start()
    finally:
        for thread in threads:
            thread.join()
    return ports


@pytest.fixture(scope="session")
def bounce_iqagent(dev_cmd, enter_switch_cli):
    
    def func(dut, xiq=None, wait=False):
        
        with enter_switch_cli(dut):
            if dut.cli_type.upper() == "EXOS":
                dev_cmd.send_cmd(
                    dut.name, 'disable iqagent', max_wait=10, interval=2,
                    confirmation_phrases='Do you want to continue?',
                    confirmation_args='Yes')
                dev_cmd.send_cmd(
                    dut.name, 'enable iqagent', max_wait=10, interval=2)
        
            elif dut.cli_type.upper() == "VOSS":
                dev_cmd.send_cmd(dut.name, 'enable', max_wait=10, interval=2)
                dev_cmd.send_cmd(
                    dut.name, 'configure terminal', max_wait=10, interval=2)
                dev_cmd.send_cmd(
                    dut.name, 'application', max_wait=10, interval=2)
                dev_cmd.send_cmd(
                    dut.name, 'no iqagent enable', max_wait=10, interval=2)
                dev_cmd.send_cmd(
                    dut.name, 'iqagent enable', max_wait=10, interval=2)
        if wait is True and xiq is not None:
            xiq.xflowscommonDevices.wait_until_device_online(dut.mac)
    return func

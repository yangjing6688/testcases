# Built-in imports
from collections import defaultdict
import inspect
import logging
import queue
import json
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
import traceback

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
def login_xiq(loaded_config, utils, cloud_driver):

    @contextmanager
    def func(username=loaded_config['tenant_username'],
             password=loaded_config['tenant_password'],
             url=loaded_config['test_url'],
             capture_version=False, code="default", incognito_mode="False"):

        xiq = XiqLibrary()

        try:
            assert xiq.login.login_user(
                username, password, capture_version=capture_version, code=code, url=url, incognito_mode=incognito_mode)
            yield xiq
        except Exception as exc:
            utils.print_info(repr(exc))
            cloud_driver.close_browser()
            raise exc
        finally:
            try:
                xiq.login.logout_user()
                xiq.login.quit_browser()
            except:
                pass
    return func


@pytest.fixture(scope="session")
def enter_switch_cli(network_manager, close_connection, dev_cmd):

    @contextmanager
    def func(dut):
        try:
            close_connection(dut)
            network_manager.connect_to_network_element_name(dut.name)
            yield dev_cmd
        finally:
            close_connection(dut)
    return func


@pytest.fixture(scope="session")
def change_device_management_settings(utils, standalone_nodes, stack_nodes, screen):
    
    def func(xiq, option, retries=5, step=5):
        
        platform = "EXOS" if any(node.cli_type.upper() == "EXOS" for node in standalone_nodes + stack_nodes) else "VOSS"
        for _ in range(retries):
            try:
                xiq.xflowsglobalsettingsGlobalSetting.change_exos_device_management_settings(
                    option=option, platform=platform)
                screen.save_screen_shot()
            except Exception as exc:
                utils.print_info(repr(exc))
                screen.save_screen_shot()
                utils.wait_till(timeout=step)
            else:
                xiq.xflowscommonNavigator.navigate_to_devices()
                break
        else:
            pytest.fail("Failed to change exos device management settings")
    return func


@pytest.fixture(scope="session")
def create_location(onboarding_location, utils, screen):
    
    def func(xiq, location=onboarding_location):
        
        utils.print_info(f"Try to delete this location: '{location}'")
        xiq.xflowsmanageLocation.delete_location_building_floor(*location.split(","))
        screen.save_screen_shot()
        
        utils.print_info(f"Create this location: '{location}'")
        xiq.xflowsmanageLocation.create_location_building_floor(*location.split(","))
        screen.save_screen_shot()
        
    return func


def generate_template_for_given_model(dut):

    model = dut.model
    platform = dut.platform
    slots = dut.get("stack")
    
    if platform.lower() == 'stack':
        if not slots:
            pytest.fail("No slots available in current stack")

        model_list = []
        sw_model = ""

        for slot in slots.values():
            
            slot_model = slot.model
            
            if "SwitchEngine" in slot_model:
                mat = re.match('(.*)(Engine)(.*)', slot_model)
                model_md = mat.group(1) + ' ' + mat.group(2) + ' ' + mat.group(3).replace('_', '-')
                switch_type=re.match('(\d+).*', mat.group(3).split('_')[0]).group(1)
                sw_model = 'Switch Engine ' + switch_type + '-Series-Stack'

            else:
                model_act = slot_model.replace('10_G4', '10G4')
                m = re.match(r'(X\d+)(G2)(.*)', model_act)
                model_md = m.group(1) + '-' + m.group(2) + m.group(3).replace('_', '-')
                sw_model = m.group(1) + '-' + m.group(2) + '-Series-Stack'
            model_list.append(model_md)

        model_units = ','.join(model_list)
        return sw_model, model_units

    elif "Engine" in model:
        mat = re.match('(.*)(Engine)(.*)', model)
        sw_model = mat.group(1) + ' ' + mat.group(2) + ' ' + mat.group(3).replace('_', '-')

    elif "G2" in model:
        model_act = model.replace('10_G4', '10G4')
        m = re.match(r'(X\d+)(G2)(.*)', model_act)
        sw_model = m.group(1) + '-' + m.group(2) + m.group(3).replace('_', '-')

    else:
        sw_model = model.replace('_', '-')
    return sw_model, ""


@pytest.fixture(scope="session")
def close_connection(network_manager, utils):
    def func(dut):
        try:
            network_manager.close_connection_to_network_element(dut.name)
        except Exception as exc:
            utils.print_info(exc)
    return func


@pytest.fixture(scope="session")
def virtual_routers(enter_switch_cli, dut_list, utils):
    
    vrs = {}
    
    def worker(dut):
        with enter_switch_cli(dut) as dev_cmd:
            try:
                output = dev_cmd.send_cmd(
                    dut.name, 'show vlan', max_wait=10, interval=2)[0].return_text
                pattern = f'(\w+)(\s+)(\d+)(\s+)({dut.ip})(\s+)(\/.*)(\s+)(\w+)(\s+/)(.*)(VR-\w+)'
                match = re.search(pattern, output)

                assert match, "Pattern not found, unable to get virtual router info!"
                assert int(match.group(9)) > 0, f"There is no active port in the mgmt vlan {match.group(1)}"
                
                vrs[dut.name] = match.group(12)
            except Exception as exc:
                utils.print_info(repr(exc))
                vrs[dut.name] = ""
            
    threads = []
    try:
        for dut in dut_list:
            thread = threading.Thread(target=worker, args=(dut, ))
            threads.append(thread)
            thread.start()
    finally:
        for thread in threads:
            thread.join()
    return vrs


@pytest.fixture(scope="session")
def screen():
    from extauto.common.Screen import Screen
    return Screen()


@pytest.fixture(scope="session")
def navigator():
    from extauto.xiq.flows.common.Navigator import Navigator
    return Navigator()


@pytest.fixture(scope="session")
def utils():
    from extauto.common.Utils import Utils
    return Utils()


@pytest.fixture(scope="session")
def wait_till(utils):
    return utils.wait_till


@pytest.fixture(scope="session")
def cloud_driver():
    from extauto.common.CloudDriver import CloudDriver
    return CloudDriver()


@pytest.fixture(scope="session")
def auto_actions():
    from extauto.common.AutoActions import AutoActions
    return AutoActions()


@pytest.fixture(scope="session")
def configure_iq_agent(loaded_config, enter_switch_cli, virtual_routers, utils, dut_list, screen):
    
    def func(duts=dut_list, ipaddress=loaded_config['sw_connection_host']):
        
        utils.print_info(f"Configure IQAGENT with ipaddress='{ipaddress}' on these devices: {', '.join([d.name for d in dut_list])}")
        def worker(dut):
            with enter_switch_cli(dut) as dev_cmd:
                if dut.cli_type.upper() == "EXOS":
                    dev_cmd.send_cmd_verify_output(
                        dut.name, 'show process iqagent', 'Ready', max_wait=30, interval=10)
                    dev_cmd.send_cmd(
                        dut.name, 'disable iqagent', max_wait=10, interval=2,
                        confirmation_phrases='Do you want to continue?', confirmation_args='y')
                    
                    dev_cmd.send_cmd(dut.name, 'configure iqagent server ipaddress none', max_wait=10, interval=2)
                    if len(vr_name := virtual_routers[dut.name]) > 0:
                        dev_cmd.send_cmd(dut.name, f'configure iqagent server vr {vr_name}', max_wait=10, interval=2)
                    else:    
                        utils.print_info("Did not find Virtual Router information")
                
                    dev_cmd.send_cmd(
                        dut.name, f'configure iqagent server ipaddress {ipaddress}',
                        max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)
                
                elif dut.cli_type.upper() == "VOSS":
                    dev_cmd.send_cmd(dut.name, 'enable', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'configure terminal', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'application', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'no iqagent enable', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, f'iqagent server {ipaddress}',
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
                        dut.name, f'hivemanager address {ipaddress}', max_wait=10, interval=2)
                    dev_cmd.send_cmd(
                        dut.name, 'application start hiveagent', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, "exit")
        
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
        screen.save_screen_shot()
        assert menu, "Failed to get the device management settings menu"
        
        utils.wait_till(func=lambda: auto_actions.click(menu) == 1)
        screen.save_screen_shot()
        
        password, _ = utils.wait_till(
            func=xiq.xflowsglobalsettingsGlobalSetting.get_device_management_settings_password,
            silent_failure=True,
            delay=4
        )
        screen.save_screen_shot()
        assert password, "Failed to get the default device passowrd"
        return password.get_attribute('value')
    return func


@pytest.fixture(scope="session", autouse=True)
def onboarding_location():
    pool = list(string.ascii_letters) + list(string.digits)
    return f"Salem_{''.join(random.sample(pool, k=8))},Northeastern_{''.join(random.sample(pool, k=8))}," \
           f"Floor_{''.join(random.sample(pool, k=8))}"


@pytest.fixture(scope="session")
def check_duts_are_reachable(utils):
    
    results = []
    from platform import system
    
    def func(duts, results=results, retries=3, step=1, windows=system() == "Windows"):
        def worker(dut):
            
            for _ in range(retries):
                try:
                    ping_response = subprocess.Popen(
                        ["ping", f"{'-n' if windows else '-c'} 1", dut.ip], stdout=subprocess.PIPE).stdout.read().decode()
                    utils.print_info(ping_response)
                    if re.search("100% loss" if windows else "100% packet loss" , ping_response):
                        utils.wait_till(timeout=1)
                    else:
                        results.append(f"({dut.ip}): Successfully verified that this dut is reachable: {dut.name}")
                        break
                except:
                    time.sleep(step)
            else:
                results.append(f"({dut.ip}): This dut is not reachable: {dut.name}\n{ping_response}")

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
        
        if any(re.search("This dut is not reachable", message) for message in results):
            error_msg = "Failed! Not all the duts are reachable.\n" + '\n'.join(results)
            utils.print_error(error_msg)
            pytest.fail(error_msg)
        else:
            utils.print_info("The chosen devices are reachable.")
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


@pytest.fixture(scope="session", autouse=True)
def loaded_config():
    config['${TEST_NAME}'] = "onboarding"
    config['${OUTPUT DIR}'] = os.getcwd()
    config['${MAX_CONFIG_PUSH_TIME}'] = 300
    for word in ["tenant_username", "tenant_password", "test_url"]:
        config[f"${{{word.upper()}}}"] = config[word]
    return config


@pytest.fixture(scope="session")
def update_test_name(loaded_config):
    def func(test_name):
        loaded_config['${TEST_NAME}'] = test_name
    return func


@pytest.fixture(scope="session")
def default_library():
    from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
    return DefaultLibrary()


@pytest.fixture(scope="session")
def udks(default_library):
    return default_library.apiUdks


@pytest.fixture(scope="session")
def dev_cmd(default_library):
    return default_library.deviceNetworkElement.networkElementCliSend


@pytest.fixture(scope="session")
def check_devices_are_onboarded(utils, dut_list):
    def func(xiq, dut_list=dut_list, timeout=180):
        
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


@pytest.fixture(scope="session")
def cleanup(utils, screen):

    def func(xiq, duts=[], location='', network_policies=[], templates_switch=[], slots=1):
            
            xiq.xflowscommonDevices._goto_devices()
            
            for dut in duts:
                try:
                    screen.save_screen_shot()
                    utils.print_info(f"Delete this device: '{dut.name}', '{dut.mac}'")
                    xiq.xflowscommonDevices._goto_devices()
                    xiq.xflowscommonDevices.delete_device(
                        device_mac=dut.mac)
                    screen.save_screen_shot()
                except Exception as exc:
                    screen.save_screen_shot()
                    utils.print_warning(repr(exc))
                    
            if location:
                try:
                    utils.print_info(f"Delete this location: '{location}'")
                    xiq.xflowsmanageLocation.delete_location_building_floor(
                        *location.split(","))
                    screen.save_screen_shot()
                except Exception as exc:
                    screen.save_screen_shot()
                    utils.print_warning(repr(exc))   
                                    
            for network_policy in network_policies:
                try:
                    screen.save_screen_shot()
                    utils.print_info(f"Delete this network policy: '{network_policy}'")
                    xiq.xflowsconfigureNetworkPolicy.delete_network_policy(
                        network_policy)
                    screen.save_screen_shot()
                except Exception as exc:
                    screen.save_screen_shot()
                    utils.print_warning(repr(exc))   
                    
            for template_switch in templates_switch:
                utils.print_info(f"Delete this switch template: '{template_switch}'")
                for _ in range(slots):
                    try:
                        screen.save_screen_shot()
                        xiq.xflowsconfigureCommonObjects.delete_switch_template(
                            template_switch)
                        screen.save_screen_shot()
                    except Exception as exc:
                        screen.save_screen_shot()
                        utils.print_warning(repr(exc))   
    return func


@pytest.fixture(scope="session")
def configure_network_policies(utils, dut_list, policy_config, screen):
    
    def func(xiq, dut_config=policy_config):
        
        for dut, data in dut_config.items():
        
            utils.print_info(f"Configuring the network policy and switch template for dut '{dut}'")
            network_policy = data['policy_name']
            template_switch = data['template_name']
            model_template = data['dut_model_template']
            units_model = data['units_model']

            utils.print_info(f"Create this network policy for '{dut}' dut: '{network_policy}'")
            assert xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                network_policy), \
                f"Policy {network_policy} wasn't created successfully "
            screen.save_screen_shot()
            
            [dut_info] = [dut_iter for dut_iter in dut_list if dut_iter.name == dut]

            utils.print_info(f"Create and attach this switch template to '{dut}' dut: '{template_switch}'")
            if dut_info.platform.upper() == "STACK":
                xiq.xflowsconfigureSwitchTemplate.add_5520_sw_stack_template(
                    units_model, network_policy,
                    model_template, template_switch)
            else:
                xiq.xflowsconfigureSwitchTemplate.add_sw_template(
                    network_policy, model_template, template_switch)
                screen.save_screen_shot()
                
            assert xiq.xflowsmanageDevices.assign_network_policy_to_switch(
                policy_name=network_policy, serial=dut_info.mac) == 1, \
                f"Couldn't assign policy {network_policy} to device '{dut}'"
            screen.save_screen_shot()
            utils.print_info(f"Successfully configured the network policy and switch template for dut '{dut}'")
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
    return list(filter(lambda d: d is not None, [getattr(testbed, f"dut{i}", None) for i in range(1, 10)]))


@pytest.fixture(scope="session")
def standalone_nodes(nodes):
    return [node for node in nodes if node.get("platform", "").upper() != "STACK"]


@pytest.fixture(scope="session")
def stack_nodes(nodes):
    return [node for node in nodes if node.get("platform", "").upper() == "STACK"]

    
@pytest.fixture(scope="session")
def policy_config(dut_list):

    dut_config = defaultdict(lambda: {})
    pool = list(string.ascii_letters) + list(string.digits)

    for dut in dut_list:
        model, units_model = generate_template_for_given_model(dut)
        dut_config[dut.name]["policy_name"] = f"np_{''.join(random.sample(pool, k=8))}"
        dut_config[dut.name]['template_name'] = f"template_{''.join(random.sample(pool, k=8))}"
        dut_config[dut.name]['dut_model_template'] = model
        dut_config[dut.name]['units_model'] = units_model
    return dut_config


@pytest.fixture(scope="session")
def dut_list(standalone_nodes, stack_nodes, check_duts_are_reachable):
    
    duts = []

    if onboard_two_node_flag:
        duts.extend(standalone_nodes[:2])
    elif onboard_one_node_flag:
        duts.append(standalone_nodes[0])
    
    if onboard_stack_flag:
        duts.append(stack_nodes[0])

    check_duts_are_reachable(duts)
    
    return duts


@pytest.fixture(scope="session")
def update_devices(utils, dut_list, policy_config):
    
    def func(xiq, duts=dut_list):
        
        utils.wait_till(timeout=5)
        xiq.xflowscommonDevices._goto_devices()
        utils.wait_till(timeout=5)

        for dut in duts:
            policy_name = policy_config[dut.name]['policy_name']
            utils.print_info(f"Select switch row with serial '{dut.mac}'")
            if not xiq.xflowscommonDevices.select_device(dut.mac):
                error_msg = f"Switch '{dut.mac}' is not present in the grid"
                utils.print_error(error_msg)
                pytest.fail(error_msg)
            utils.wait_till(timeout=2)
            xiq.xflowscommonDevices._update_switch(
                update_method="PolicyAndConfig")

        for dut in duts:
            policy_name = policy_config[dut.name]['policy_name']
            assert xiq.xflowscommonDevices._check_update_network_policy_status(
                policy_name, dut.mac) == 1

    return func


@pytest.fixture(scope="session")
def onboard_devices(dut_list, utils, screen, onboarding_location):
    def func(xiq, duts=dut_list):
        for dut in duts:
            if xiq.xflowsmanageSwitch.onboard_switch(
                    dut.serial, device_os=dut.cli_type, location=onboarding_location) == 1:
                utils.print_info(f"Successfully onboarded this device: '{dut}'")
                screen.save_screen_shot()
            else:
                error_msg = f"Failed to onboard this device: '{dut}'"
                utils.print_info(error_msg)
                screen.save_screen_shot()
                pytest.fail(error_msg)
    return func


def dump_data(data):
    return json.dumps(data, indent=4)


@pytest.fixture(scope="session")
def onboard(request):

    utils = request.getfixturevalue("utils")
    configure_network_policies = request.getfixturevalue("configure_network_policies")
    login_xiq = request.getfixturevalue("login_xiq")
    stack_nodes = request.getfixturevalue("stack_nodes")
    change_device_management_settings = request.getfixturevalue("change_device_management_settings")
    check_devices_are_onboarded = request.getfixturevalue("check_devices_are_onboarded")
    cleanup = request.getfixturevalue("cleanup")
    create_location = request.getfixturevalue("create_location")
    onboard_devices = request.getfixturevalue("onboard_devices")
    configure_iq_agent = request.getfixturevalue("configure_iq_agent")
    update_devices = request.getfixturevalue("update_devices")

    onboarding_location = request.getfixturevalue("onboarding_location")
    utils.print_info(f"This location will be used for the onboarding: '{onboarding_location}'")

    dut_list = request.getfixturevalue("dut_list")
    utils.print_info(f"These are the devices that will be onboarded ({len(dut_list)} devices): "
                     f"{', '.join([dut.name for dut in dut_list])}")

    policy_config = request.getfixturevalue("policy_config")
    utils.print_info(f"These are the policies and switch templates that will be applied to the onboarded devices:"
                     f"\n{dump_data(policy_config)}")
    
    try:
        
        configure_iq_agent()
        
        with login_xiq() as xiq:
                
            change_device_management_settings(xiq, option="disable")
            
            cleanup(xiq=xiq, duts=dut_list)
            create_location(xiq)
            onboard_devices(xiq)

            check_devices_are_onboarded(xiq)

            configure_network_policies(xiq)

            update_devices(xiq)

        yield dut_list, policy_config
        
    except Exception as exc:
        utils.print_error(repr(exc))
        utils.print_error(traceback.format_exc())
        pytest.fail(f"The onboarding failed for these devices: {dut_list}\n{traceback.format_exc()}")
    
    finally:
        
        with login_xiq() as xiq:

            cleanup(
                xiq=xiq, 
                duts=dut_list, 
                network_policies=[dut_info['policy_name'] for dut_info in policy_config.values()],
                templates_switch=[dut_info['template_name'] for dut_info in policy_config.values()],
                location=onboarding_location,
                slots=len(stack_nodes[0].stack) if len(stack_nodes) > 0 else 1
            )


@pytest.fixture(scope="session")
def onboarded_one_node(request):
    if onboard_one_node_flag or onboard_two_node_flag:
        dut_list, _ = request.getfixturevalue("onboard")
        return [dut for dut in dut_list if dut.platform.upper() != "STACK"][0]
    pytest.fail("Testbed does not have a standalone node.")


@pytest.fixture(scope="session")
def onboarded_two_node(request):
    if onboard_two_node_flag:
        dut_list, _ = request.getfixturevalue("onboard")
        return [dut for dut in dut_list if dut.platform.upper() != "STACK"][:2]
    pytest.fail("Testbed does not have two standalone nodes.")


@pytest.fixture(scope="session")
def onboarded_stack(request):
    if onboard_stack_flag:
        dut_list, _ = request.getfixturevalue("onboard")
        return [dut for dut in dut_list if dut.platform.upper() == "STACK"][0]
    pytest.fail("Testbed does not have a stack node.")

 
@pytest.fixture(scope="session")
def dut_ports(enter_switch_cli, dut_list):
    
    ports = {}
    
    def worker(dut):
        with enter_switch_cli(dut) as dev_cmd:
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
                p = re.compile(r'^(\d+:\d+)\s+', re.M)
                match_port = re.findall(p, output)
                is_stack = True
                if len(match_port) == 0:
                    is_stack = False
                    p = re.compile(r'^(\d+)\s+', re.M)
                    match_port = re.findall(p, output)

                p_notPresent = re.compile(r'^\d+:\d+.*NotPresent.*$', re.M) if is_stack \
                    else re.compile(r'^\d+.*NotPresent.*$', re.M)
                parsed_info = re.findall(p_notPresent, output)

                for port in parsed_info:
                    port_num = re.findall(p, port)
                    match_port.remove(port_num[0])
                ports[dut.name] = match_port
            
            elif dut.cli_type.upper() == "AH-FASTPATH":
                try:
                    dev_cmd.send_cmd(dut.name, "enable")
                except:
                    dev_cmd.send_cmd(dut.name, "exit")
                output = dev_cmd.send_cmd(
                    dut.name, "show port all", max_wait=10, interval=2)[0].return_text
                output = re.findall(r"\r\n(\d+/\d+/\d+)\s+", output)
                ports[dut.name] = output
                dev_cmd.send_cmd(dut.name, "exit")

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
def bounce_iqagent(enter_switch_cli):
    
    def func(dut, xiq=None, wait=False):
        
        with enter_switch_cli(dut) as dev_cmd:
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


@pytest.fixture(scope="session")
def reboot_device(dut_list, enter_switch_cli, utils):
    
    def func(duts=dut_list):
        
        def worker(dut):
            with enter_switch_cli(dut) as dev_cmd:
                try:
                    
                    if dut.cli_type.upper() == "EXOS":
                        dev_cmd.send_cmd(
                            dut.name, 'reboot all', max_wait=10, interval=2,
                            confirmation_phrases='Are you sure you want to reboot the switch?',
                            confirmation_args='y'
                        )
                    elif dut.cli_type.upper() == "VOSS":
                        dev_cmd.send_cmd(dut.name, 'reset -y', max_wait=10, interval=2)
                        
                    elif dut.cli_type.upper() == "AH-FASTPATH":
                        try:
                            dev_cmd.send_cmd(dut.name, "enable")
                        except:
                            dev_cmd.send_cmd(dut.name, "exit")
                            
                        dev_cmd.send_cmd(
                            dut.name, 'reload', max_wait=10, interval=2,
                            confirmation_phrases='Would you like to save them now? (y/n)', confirmation_args='y'
                        )
                except Exception as exc:
                    error_msg = f"Failed to reboot this dut: '{dut.name}'\n{repr(exc)}"
                    utils.print_error(error_msg)
                    utils.wait_till(timeout=5)
                    pytest.fail(error_msg)
                else:
                    utils.wait_till(timeout=120)
    
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
def reboot_stack_unit(utils, enter_switch_cli):
    
    def func(dut, slot=1, save_config='n'):
        
        if not (dut.platform.upper() == "STACK" and dut.cli_type.upper() == "EXOS"):
            pytest.fail(f"Given device is not an EXOS stack: '{dut}'")

        with enter_switch_cli(dut) as dev_cmd:
            try:
                dev_cmd.send_cmd(
                    dut.name, f'reboot slot {slot}', max_wait=10, interval=2,
                    confirmation_phrases='Do you want to save configuration changes to currently selected configuration',
                    confirmation_args=save_config
                )
            except Exception as exc:
                error_msg = f"Failed to reboot slot '{slot}' of dut: '{dut.name}'\n{repr(exc)}"
                utils.print_error(error_msg)
                utils.wait_till(timeout=5)
                pytest.fail(error_msg)
            else:
                utils.wait_till(timeout=120)
    return func


@pytest.fixture(scope="session")
def get_stack_slots(utils, enter_switch_cli):
    
    def func(dut):
        
        if not (dut.platform.upper() == "STACK" and dut.cli_type.upper() == "EXOS"):
            pytest.fail(f"Given device is not an EXOS stack: '{dut}'")

        slots_info = {}
        with enter_switch_cli(dut) as dev_cmd:
            output = dev_cmd.send_cmd(dut.name, 'show stacking', max_wait=10, interval=2)[0].return_text
            utils.print_info(output)
            rows = re.findall(r'((?:[0-9a-fA-F]:?){12})\s+(\d+)\s+(\w+)\s+(\w+)\s+(.*)\r\n', output, re.IGNORECASE)
            
            for row in rows:
                slots_info[row[1]] = dict(zip(["Node MAC Address", "Slot", "Stack State", "Role", "Flags"], row))
            utils.print_info(f"Found these slots on the stack device '{dut.name}': {dump_data(slots_info)}")
            return slots_info
    return func


@pytest.fixture(scope="session")
def modify_stacking_node(enter_switch_cli, reboot_device):
    
    def func(dut, node_mac_address, op):
        if not (dut.platform.upper() == "STACK" and dut.cli_type.upper() == "EXOS"):
            pytest.fail(f"Given device is not an EXOS stack: '{dut}'")

        assert op in ["enable", "disable"], "Op argument should be 'enbale' or 'disable'"
        
        with enter_switch_cli(dut) as dev_cmd:
            cmd = f"{op} stacking node-address {node_mac_address}"
            dev_cmd.send_cmd(dut.name, cmd, max_wait=10, interval=2)
        
        reboot_device(dut)
    return func


@pytest.fixture(scope="session")
def set_lldp(enter_switch_cli):
    
    def func(dut, ports, action="enable"):
        with enter_switch_cli(dut) as dev_cmd:
            if dut.cli_type.upper() == "EXOS":
                if action == "enable":
                    dev_cmd.send_cmd(dut.name, 'enable cdp ports all', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'enable edp ports all', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'enable lldp ports all', max_wait=10, interval=2)
                elif action == "disable":
                    dev_cmd.send_cmd(dut.name, 'disable cdp ports all', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'disable edp ports all', max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, 'disable lldp ports all', max_wait=10, interval=2)

            elif dut.cli_type.upper() == "VOSS":
                dev_cmd.send_cmd(dut.name, "enable", max_wait=10, interval=2)
                dev_cmd.send_cmd(dut.name, "configure terminal", max_wait=10, interval=2)
                dev_cmd.send_cmd(
                    dut.name, f"interface gigabitEthernet {ports[0]}-{ports[-1]}", max_wait=10, interval=2)
                cmd_action = f"lldp port {ports[0]}-{ports[-1]} cdp enable"
                if action == "enable":
                    dev_cmd.send_cmd(dut.name, "no auto-sense enable", max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, "no fa enable", max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, cmd_action, max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, "fa enable", max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, "auto-sense enable", max_wait=10, interval=2)
                elif action == "disable":
                    dev_cmd.send_cmd(dut.name, "no " + cmd_action, max_wait=10, interval=2)
    return func


@pytest.fixture(scope="session")
def clear_traffic_counters(enter_switch_cli):
    def func(dut, *ports):
        with enter_switch_cli(dut) as dev_cmd:
            if dut.cli_type.upper() == "EXOS":
                    dev_cmd.send_cmd(
                    dut.name, f"clear counters ports {','.join(ports)}", max_wait=10, interval=2)
            elif dut.cli_type.upper() == "VOSS":
                dev_cmd.send_cmd(
                    dut.name, f"clear-stats port {','.join(ports)}", max_wait=10, interval=2)
    return func

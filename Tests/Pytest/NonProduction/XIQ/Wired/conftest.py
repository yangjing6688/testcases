import json
import threading
import time
import os
import re
import string
import random
import subprocess
import traceback
import pytest

import platform

from collections import defaultdict
from pytest_testconfig import config
from contextlib import contextmanager

from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Library.Logger.PytestLogger import PytestLogger
from ExtremeAutomation.Library.Logger.Colors import Colors


@pytest.fixture(scope="session")
def debug(logger):
    def debug_func(func):
        def wrapped_func(*args, **kwargs):
            start_time = time.time()
            try:
                logger.step(f"Calling '{func.__name__}' function with args='{args}' and kwargs='{kwargs}'")
                result = func(*args, **kwargs)
            except Exception as exc:
                logger.error(f"Failed during '{func.__name__}' function call with args='{args}' and kwargs='{kwargs}' after {int(time.time()-start_time)} seconds: {repr(exc)}")
                raise exc
            else:
                logger.info(f"Call for '{func.__name__}' with args='{args}' and kwargs='{kwargs}' ended after {int(time.time()-start_time)} seconds")
                return result
        return wrapped_func
    return debug_func


@pytest.fixture(scope="session")
def logger():
    return logger_obj


_testbed: PytestConfigHelper = None
_nodes = []
_standalone_nodes = []
_stack_nodes = []
onboard_one_node_flag = False
onboard_two_node_flag = False
onboard_stack_flag = False
logger_obj = PytestLogger()


def pytest_cmdline_preparse(config, args):
    args.append(os.path.join(os.path.dirname(__file__), "conftest.py"))


def pytest_collection_modifyitems(session, items):
    
    global onboard_one_node_flag
    global onboard_two_node_flag
    global onboard_stack_flag
    global _nodes
    global _standalone_nodes
    global _stack_nodes
    global _testbed

    onboarding_test_name = "tcxm_xiq_onboarding"
    onboarding_cleanup_test_name = "tcxm_xiq_onboarding_cleanup"

    collected_items = []
    for item in items:
        if onboarding_test_name in [m.name for m in item.own_markers]:
            if not [it for it in collected_items if item if onboarding_test_name in [m.name for m in it.own_markers]]:
                collected_items.append(item)
        elif onboarding_cleanup_test_name in [m.name for m in item.own_markers]:
            if not [it for it in collected_items if item if onboarding_cleanup_test_name in [m.name for m in it.own_markers]]:
                collected_items.append(item)
        else:
            collected_items.append(item)

    for item in collected_items:
        logger_obj.info(f"Collected this test function: '{item.nodeid}'.")

    [item_onboarding] = [
        it for it in collected_items if item if onboarding_test_name in [m.name for m in it.own_markers]]
    [item_onboarding_cleanup] = [
        it for it in collected_items if item if onboarding_cleanup_test_name in [m.name for m in it.own_markers]]
    
    collected_items.remove(item_onboarding)
    collected_items.remove(item_onboarding_cleanup)
    
    _testbed = PytestConfigHelper(config)
    _nodes = list(filter(lambda d: d is not None, [getattr(_testbed, f"dut{i}", None) for i in range(1, 10)]))

    logger_obj.step("Check the capabilities of the testbed.")
    _standalone_nodes = [node for node in _nodes if node.get("platform", "").upper() != "STACK"]
    logger_obj.info(f"Found {len(_standalone_nodes)} standalone node(s).")

    _stack_nodes = [node for node in _nodes if node not in _standalone_nodes]
    logger_obj.info(f"Found {len(_stack_nodes)} stack node(s).")

    temp_items = collected_items[:]

    onboard_stack_flag = len(_stack_nodes) >= 1
    if not onboard_stack_flag:
        logger_obj.warning(
            "There is no stack device in the provided yaml file. The stack test cases will be unselected.")
        temp_items = [
            item for item in temp_items if 'testbed_stack' not in [marker.name for marker in item.own_markers]]

    onboard_two_node_flag = len(_standalone_nodes) > 1
    if not onboard_two_node_flag:
        logger_obj.warning(
            "There are not enough standalone devices in the provided yaml file. "
            "The testbed two node test cases will be unselected.")
        temp_items = [
            item for item in temp_items if 'testbed_2_node' not in [marker.name for marker in item.own_markers]]
    
    onboard_one_node_flag = len(_standalone_nodes) >= 1
    if not onboard_one_node_flag:
        logger_obj.warning("There is no standalone device in the provided yaml file. "
                           "The testbed one node test cases will be unselected.")
        temp_items = [
            item for item in temp_items if 'testbed_1_node' not in [marker.name for marker in item.own_markers]]
    
    temp_items = [
        item for item in temp_items if any(
            [testbed_marker in [marker.name for marker in item.own_markers] for testbed_marker in [
                "testbed_1_node", "testbed_2_node", "testbed_stack", "testbed_none"
        ]]
    )]
    
    for item in collected_items:
        if item not in temp_items:
            logger_obj.info(
                f"This test function is unselected: '{item.nodeid}' (markers: '{[m.name for m in item.own_markers]}').")
    
    item_tcxm_mapping = defaultdict(lambda: [])
    tcxm_item_mapping = defaultdict(lambda: [])
    items_without_tcxm_markers = []
    items_without_priority_markers = []

    for item in temp_items:
        tcxm_codes = [m.name for m in item.own_markers if re.search("^tcxm_", m.name)]
        priority = [m.name for m in item.own_markers if str(m.name) in ["p1", "p2", "p3", "p4", "p5"]]

        if not priority:
            items_without_priority_markers.append(
                f"This function does not have a priority marker: '{item.nodeid}'.")

        if not tcxm_codes:
            items_without_tcxm_markers.append(
                f"This function does not have a TCXM marker: '{item.nodeid}'.")

        for tcxm_code in tcxm_codes:
            item_tcxm_mapping[tcxm_code].append(item.nodeid)
    
        tcxm_item_mapping[item] = tcxm_codes

    if items_without_tcxm_markers:
        error = '\n' + '\n'.join(items_without_tcxm_markers)
        logger_obj.error(error)
        pytest.fail(error)
    
    if items_without_priority_markers:
        error = '\n' + '\n'.join(items_without_priority_markers)
        logger_obj.error(error)
        pytest.fail(error)
    
    for tcxm_code, functions in item_tcxm_mapping.items():
        if len(functions) > 1:
            error = f"Marker '{tcxm_code}' is used as marker for more than one test function:\n" + "\n".join(functions)
            logger_obj.error(error)
            pytest.fail(error)

    for item, tcxm_markers in tcxm_item_mapping.items():
        if len(tcxm_markers) > 1:
            error = f"\nThis test function has more than one TCXM marker: " \
                    f"{item.nodeid} (markers: '{tcxm_markers}')."
            logger_obj.error(error)
            pytest.fail(error)

    all_tcs = [onboarding_test_name, onboarding_cleanup_test_name]
    for item in temp_items:
        [tcxm_code] = [m.name for m in item.own_markers if re.search("^tcxm_", m.name)]
        all_tcs.append(tcxm_code)

    found_tcs = [onboarding_test_name, onboarding_cleanup_test_name]
    for item in temp_items:
        [tcxm_code] = [m.name for m in item.own_markers if re.search("^tcxm_", m.name)]
        found_tcs.append(tcxm_code)
        item_markers = item.own_markers
        for marker in item_markers:
            if marker.name == "dependson":
                temp_markers = marker.args
                if not len(temp_markers):
                    logger_obj.warning(
                        f"The dependson marker of '{tcxm_code}' testcase does not have any arguments "
                        f"(test function: '{item.nodeid}'.")
                for temp_marker in temp_markers:
                    if temp_marker == tcxm_code:
                        logger_obj.warning(
                            f"'{tcxm_code}' is marked as depending on itself (test function: '{item.nodeid}'.")
                    elif temp_marker not in all_tcs:
                        item.add_marker(
                            pytest.mark.skip(f"'{tcxm_code}' depends on '{', '.join(temp_markers)}' but '{temp_marker}'"
                                             f" is not in the current list of testcases to be run. It will be skipped.")
                        )
                    elif temp_marker not in found_tcs:
                        item.add_marker(
                            pytest.mark.skip(
                                f"Please modify the order of the test cases. '{tcxm_code}' "
                                f"depends on '{', '.join(temp_markers)}' but the order is not correct. "
                                f"It will be skipped.")
                        )
    if temp_items:
        temp_items.insert(0, item_onboarding)
        temp_items.append(item_onboarding_cleanup)
        for item in temp_items:
            logger_obj.info(f"This test function is selected to run this session: '{item.nodeid}' "
                            f"(markers: '{[m.name for m in item.own_markers]}').")
    else:
        message = "Did not find any test function to run this session."
        logger_obj.warning(message)
    items[:] = temp_items


def pytest_sessionstart(session):
    session.results = dict()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    
    outcome = yield
    result = outcome.get_result()

    [current_test_marker] = [m.name for m in item.own_markers if re.search("^tcxm_", m.name)]

    if result.when == 'call':
        item.session.results[item] = result

        if outcome := result.outcome: 
            if outcome == "passed":
                logger_obj.info(
                    f"\n{Colors.Bg.GREEN}{Colors.Style.BRIGHT}{Colors.Fg.WHITE} --> {current_test_marker.upper()} PASSED <--"
                    f" {Colors.Bg.RESET}{Colors.Style.RESET_ALL}")
            elif outcome == "failed":
                logger_obj.info(
                    f"\n{Colors.Bg.RED}{Colors.Style.BRIGHT}{Colors.Fg.WHITE} --> {current_test_marker.upper()} FAILED <-- "
                    f"{Colors.Bg.RESET}{Colors.Style.RESET_ALL}")
    
    elif result.when == "setup":
        
        if (outcome := result.outcome) == "skipped":
            logger_obj.info(f"\n{Colors.Bg.BLUE}{Colors.Style.BRIGHT}{Colors.Fg.WHITE} --> {current_test_marker.upper()} SKIPPED "
                  f"<-- {Colors.Bg.RESET}{Colors.Style.RESET_ALL}")

    if result.when == 'call' and result.outcome != "passed":
        for it in item.session.items:
            [temp_tcxm_marker] = [m.name for m in it.own_markers if re.search("^tcxm_", m.name)]
            for mk in it.own_markers:
                if mk.name == "dependson":
                    if len(mk.args) > 0:
                        if current_test_marker in mk.args:                            
                            it.add_marker(
                                pytest.mark.skip(
                                    f"'{temp_tcxm_marker}' depends on '{current_test_marker}' but "
                                    f"'{current_test_marker}' failed. '{temp_tcxm_marker}' "
                                    f"test case will be skipped."))

    if "skip" in [m.name for m in item.own_markers]:
        for it in item.session.items:
            [temp_tcxm_marker] = [m.name for m in it.own_markers if re.search("^tcxm_", m.name)]
            for mk in it.own_markers:
                if mk.name == "dependson":
                    if current_test_marker in mk.args:
                        it.add_marker(
                            pytest.mark.skip(
                                f"'{temp_tcxm_marker}' depends on '{current_test_marker}' but "
                                f"'{current_test_marker}' is skipped. '{temp_tcxm_marker}' "
                                f"test case will be skipped."))


def pytest_runtest_call(item):
    [current_test_marker] = [m.name for m in item.own_markers if re.search("^tcxm_", m.name)]
    config['${TEST_NAME}'] = current_test_marker
    logger_obj.step(f"Start test function of '{current_test_marker}': '{item.nodeid}'.")


@pytest.mark.tcxm_xiq_onboarding
def test_xiq_onboarding(request, logger):
    if not any([onboard_one_node_flag, onboard_two_node_flag, onboard_stack_flag]):
        logger.info(
            "Currently there are no devices given in the yaml files so the onboarding test won't configure anything.")
        return
    request.getfixturevalue("onboard")


@pytest.mark.tcxm_xiq_onboarding_cleanup
def test_xiq_onboarding_cleanup(request, logger):
    if not any([onboard_one_node_flag, onboard_two_node_flag, onboard_stack_flag]):
        logger.info(
            "Currently there are no devices given in the yaml files so "
            "the onboarding cleanup test won't unconfigure anything.")
        return
    request.getfixturevalue("onboard_cleanup")


@pytest.fixture(scope="session")
def login_xiq(loaded_config, logger, cloud_driver, debug):

    @contextmanager
    @debug
    def login_xiq_func(
        username=loaded_config['tenant_username'],
        password=loaded_config['tenant_password'],
        url=loaded_config['test_url'],
        capture_version=False, code="default", incognito_mode="False"
    ):

        xiq = XiqLibrary()

        try:
            assert xiq.login.login_user(
                username, password, capture_version=capture_version, code=code, url=url, incognito_mode=incognito_mode)
            yield xiq
        except Exception as exc:
            logger.error(repr(exc))
            cloud_driver.close_browser()
            raise exc
        finally:
            try:
                xiq.login.logout_user()
                xiq.login.quit_browser()
            except:
                pass
    return login_xiq_func


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
def cli():
    from extauto.common.Cli import Cli
    return Cli()


@pytest.fixture(scope="session")
def open_spawn(cli):
    
    @contextmanager
    def func(dut):
        try:
            spawn_connection = cli.open_spawn(
                dut.ip, dut.port, dut.username, dut.password, dut.cli_type)
            yield spawn_connection
        finally:          
            cli.close_spawn(spawn_connection)
    return func


@pytest.fixture(scope="session")
def connect_to_all_devices(network_manager, dev_cmd):
    
    @contextmanager
    def func():
        try:
            network_manager.connect_to_all_network_elements()
            yield dev_cmd
        finally:
            network_manager.close_connection_to_all_network_elements()
    return func


@pytest.fixture(scope="session")
def create_location(logger, screen, debug):
    
    @debug
    def create_location_func(xiq, location):
        
        logger.step(f"Try to delete this location: '{location}'.")
        xiq.xflowsmanageLocation.delete_location_building_floor(*location.split(","))
        screen.save_screen_shot()
        
        logger.step(f"Create this location: '{location}'.")
        xiq.xflowsmanageLocation.create_location_building_floor(*location.split(","))
        screen.save_screen_shot()
        
    return create_location_func


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
def close_connection(network_manager, logger):
    def func(dut):
        try:
            network_manager.close_connection_to_network_element(dut.name)
        except Exception as exc:
            logger.info(exc)
    return func


@pytest.fixture(scope="session")
def virtual_routers(enter_switch_cli, dut_list, logger):
    
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
                logger.warning(repr(exc))
                vrs[dut.name] = ""
            
    threads = []
    try:
        for dut in [d for d in dut_list if d.cli_type.upper() == "EXOS"]:
            thread = threading.Thread(target=worker, args=(dut, ))
            threads.append(thread)
            thread.start()
    finally:
        for thread in threads:
            thread.join()
    return vrs


@pytest.fixture(scope="session")
def configure_iq_agent(loaded_config, logger, dut_list, debug, open_spawn, cli, request):
    
    @debug
    def configure_iq_agent_func(duts=dut_list, ipaddress=loaded_config['sw_connection_host']):
        
        virtual_routers = request.getfixturevalue("virtual_routers")

        logger.step(
            f"Configure IQAGENT with ipaddress='{ipaddress}' on these devices: {', '.join([d.name for d in dut_list])}.")

        def worker(dut):
            
            with open_spawn(dut) as spawn_connection:
                if loaded_config.get("lab", "").upper() == "SALEM":
                    cli.downgrade_iqagent(dut.cli_type, spawn_connection)
                
                cli.configure_device_to_connect_to_cloud(
                    dut.cli_type, loaded_config['sw_connection_host'],
                    spawn_connection, vr=virtual_routers.get(dut.name, 'VR-Mgmt'), retry_count=30
                )

        threads = []
        try:
            for dut in duts:
                thread = threading.Thread(target=worker, args=(dut, ))
                threads.append(thread)
                thread.start()
        finally:
            for thread in threads:
                thread.join()
    return configure_iq_agent_func


@pytest.fixture(scope="session")
def onboarding_locations(nodes, logger):
    
    ret = {}
    
    hardcoded_locations = [
        "San Jose,building_01,floor_01",
    ]
    
    for node in nodes:
        locations = node.get("location", [])
        if locations:
            logger.info(f"Found location(s) attached to '{node.name}': {locations}.")
            
            logger.step("Choose one of them.")
            found_location = random.choice(list(locations.values()))
            logger.info(f"The chosen location for '{node.name}' is '{found_location}'.")
            ret[node.name] = found_location
        else:
            logger.info(f"Did not find any location attached to '{node.name}'.")

            logger.step(f"Will choose a location out of these: {hardcoded_locations}.")
            found_location = random.choice(hardcoded_locations)
            logger.info(f"The chosen location for '{node.name}' is '{found_location}'.")
            ret[node.name] = found_location
    return ret


@pytest.fixture(scope="session")
def check_duts_are_reachable(logger, debug, wait_till):
    
    @debug
    def check_duts_are_reachable_func(duts, retries=3, step=1, windows=platform.system() == "Windows"):
        results = []
        def worker(dut):
            
            for _ in range(retries):
                try:
                    ping_response = subprocess.Popen(
                        ["ping", f"{'-n' if windows else '-c'} 1", dut.ip],
                        stdout=subprocess.PIPE).stdout.read().decode()
                    logger.cli(ping_response)
                    if re.search("100% loss" if windows else "100% packet loss" , ping_response):
                        wait_till(timeout=1)
                    else:
                        results.append(f"({dut.ip}): Successfully verified that this dut is reachable: '{dut.name}'.")
                        break
                except:
                    wait_till(timeout=step)
            else:
                results.append(f"({dut.ip}): This dut is not reachable: '{dut.name}.'\n{ping_response}")

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
            logger.info(message)
        
        if any(re.search("This dut is not reachable", message) for message in results):
            error_msg = "Failed! Not all the duts are reachable.\n" + '\n'.join(results)
            logger.error(error_msg)
            pytest.fail(error_msg)

    return check_duts_are_reachable_func


@pytest.fixture(scope="session")
def testbed():
    return _testbed


@pytest.fixture(scope="session", autouse=True)
def loaded_config():
    
    config['${TEST_NAME}'] = "onboarding"
    config['${OUTPUT DIR}'] = os.getcwd()
    config['${MAX_CONFIG_PUSH_TIME}'] = 300
    config['${EXIT_LEVEL}'] = -600

    for word in ["tenant_username", "tenant_password", "test_url"]:
        config[f"${{{word.upper()}}}"] = config[word]

    return config


@pytest.fixture(scope="session")
def dev_cmd(default_library):
    return default_library.deviceNetworkElement.networkElementCliSend


@pytest.fixture(scope="session")
def check_devices_are_onboarded(logger, dut_list, debug, wait_till):
    
    @debug
    def check_devices_are_onboarded_func(xiq, dut_list=dut_list, timeout=240):
        
        xiq.xflowscommonDevices.column_picker_select("MAC Address")
        
        start_time = time.time()
        
        devices_appeared_in_xiq = False
        devices_are_online = False
        devices_are_managed = False

        while time.time() - start_time < timeout:
            try:
                xiq.xflowsmanageDevices.refresh_devices_page()
                wait_till(timeout=5)

                if not devices_appeared_in_xiq:
                    devices, _ = wait_till(
                        func=xiq.xflowscommonDeviceCommon.get_device_grid_rows,
                        exp_func_resp=True,
                        silent_failure=True
                    )
                    assert devices, "Did not find any onboarded devices in the XIQ."

                    found_all = True
                    for dut in dut_list:
                        for device in devices:
                            if any([dut.mac.upper() in device.text, dut.mac.lower() in device.text]):
                                logger.info(f"Successfully found device with mac='{dut.mac}'.")
                                break
                        else:
                            logger.warning(f"Did not find device with mac='{dut.mac}'.")
                            found_all = False
                    assert found_all, "Not all the devices were found in the Manage -> Devices menu."
                    devices_appeared_in_xiq = True

                if not devices_are_online:
                    for dut in dut_list:
                        
                        device_online = xiq.xflowscommonDevices.wait_until_device_online(dut.mac)
                        assert device_online == 1, f"This device did not come online in the XIQ: {dut}."
                        logger.info(f"This device did come online in the XIQ: {dut}.")
                        
                        res = xiq.xflowscommonDevices.get_device_status(device_serial=dut.mac)
                        assert res == 'green', f"This device does not have green status in the XIQ: {dut}."
                        logger.info(f"This device does have green status in the XIQ: {dut}.")

                    devices_are_online = True
                
                if not devices_are_managed:
                    
                    for dut in dut_list:
                        res = xiq.xflowscommonDevices.wait_until_device_managed(device_serial=dut.mac)
                        assert res == 1, f"The device does not appear as Managed in the XIQ; Device: {dut}."
                        logger.info(f"This device does appear as Managed in the XIQ: {dut}.")

                    devices_are_managed = True

            except Exception as err:
                logger.warning(f"Not all the devices are up yet: {repr(err)}")
                wait_till(timeout=10)
            else:
                break
        else:
            pytest.fail("Not all the devices are up in XIQ")

    return check_devices_are_onboarded_func


@pytest.fixture(scope="session")
def cleanup(logger, screen, debug):

    @debug
    def cleanup_func(xiq, duts=[], location='', network_policies=[], templates_switch=[], slots=1):
            
            xiq.xflowscommonDevices._goto_devices()
            
            for dut in duts:
                try:
                    screen.save_screen_shot()
                    logger.info(f"Delete this device: '{dut.name}', '{dut.mac}'.")
                    xiq.xflowscommonDevices._goto_devices()
                    xiq.xflowscommonDevices.delete_device(
                        device_mac=dut.mac)
                    screen.save_screen_shot()
                except Exception as exc:
                    screen.save_screen_shot()
                    logger.warning(repr(exc))
                    
            if location:
                try:
                    logger.info(f"Delete this location: '{location}'.")
                    xiq.xflowsmanageLocation.delete_location_building_floor(
                        *location.split(","))
                    screen.save_screen_shot()
                except Exception as exc:
                    screen.save_screen_shot()
                    logger.warning(repr(exc))   
                                    
            for network_policy in network_policies:
                try:
                    screen.save_screen_shot()
                    logger.info(f"Delete this network policy: '{network_policy}'.")
                    xiq.xflowsconfigureNetworkPolicy.delete_network_policy(
                        network_policy)
                    screen.save_screen_shot()
                except Exception as exc:
                    screen.save_screen_shot()
                    logger.warning(repr(exc))   
                    
            for template_switch in templates_switch:
                logger.info(f"Delete this switch template: '{template_switch}'.")
                for _ in range(slots):
                    try:
                        screen.save_screen_shot()
                        xiq.xflowsconfigureCommonObjects.delete_switch_template(
                            template_switch)
                        screen.save_screen_shot()
                    except Exception as exc:
                        screen.save_screen_shot()
                        logger.warning(repr(exc))   
    return cleanup_func


@pytest.fixture(scope="session")
def configure_network_policies(logger, dut_list, policy_config, screen, debug):
    
    @debug
    def configure_network_policies_func(xiq, dut_config=policy_config):
        
        for dut, data in dut_config.items():
        
            logger.step(f"Configuring the network policy and switch template for dut '{dut}'.")
            network_policy = data['policy_name']
            template_switch = data['template_name']
            model_template = data['dut_model_template']
            units_model = data['units_model']

            logger.step(f"Create this network policy for '{dut}' dut: '{network_policy}'.")
            assert xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                network_policy), \
                f"Policy {network_policy} wasn't created successfully "
            screen.save_screen_shot()
            
            [dut_info] = [dut_iter for dut_iter in dut_list if dut_iter.name == dut]

            logger.step(f"Create and attach this switch template to '{dut}' dut: '{template_switch}'.")
            if dut_info.platform.upper() == "STACK":
                xiq.xflowsconfigureSwitchTemplate.add_5520_sw_stack_template(
                    units_model, network_policy,
                    model_template, template_switch)
            else:
                xiq.xflowsconfigureSwitchTemplate.add_sw_template(
                    network_policy, model_template, template_switch)
                screen.save_screen_shot()
                
            # assert xiq.xflowsmanageDevices.assign_network_policy_to_switch(
            #     policy_name=network_policy, serial=dut_info.mac) == 1, \
            #     f"Couldn't assign policy {network_policy} to device '{dut}'"
            
            _temporary_fix_assign_policy(xiq, network_policy, dut_info)
            
            screen.save_screen_shot()
            logger.info(f"Successfully configured the network policy and switch template for dut '{dut}'.")
    return configure_network_policies_func


def _temporary_fix_assign_policy(xiq, policy_name, dut):
    
    import selenium
    from extauto.common.AutoActions import AutoActions

    devices = xiq.xflowscommonDevices
    auto_actions = AutoActions()

    time.sleep(10)
    xiq.xflowscommonDevices._goto_devices()
    time.sleep(10)

    assert devices.select_device(dut.mac)
    time.sleep(2)

    auto_actions.click(devices.devices_web_elements.get_manage_device_actions_button())
    time.sleep(3)

    logger_obj.info("Click on Assign Network policy action for selected switch.")
    auto_actions.click(devices.devices_web_elements.get_actions_assign_network_policy_combo_switch())
    time.sleep(4)

    logger_obj.info("Click on network policy drop down.")
    try:
        drop_down_button = devices.devices_web_elements.get_actions_assign_network_policy_drop_down()
        drop_down_button.click()
    except selenium.common.exceptions.ElementNotInteractableException as exc:
        logger_obj.warning(repr(exc))
        [drop_down_button] = [btn for btn in devices.devices_web_elements.weh.get_elements(
            {"XPATH": '//tbody[@role="presentation"]'}) if btn.text == '--Select--']

        auto_actions.click(drop_down_button)
        time.sleep(5)

    network_policy_items = devices.devices_web_elements.get_actions_network_policy_drop_down_items()
    time.sleep(2)

    if auto_actions.select_drop_down_options(network_policy_items, policy_name):
        logger_obj.info(f"Selected Network policy from drop down: '{policy_name}'.")
    else:
        logger_obj.info("Network policy is not present in drop down.")

    time.sleep(5)

    logger_obj.info("Click on network policy assign button.")
    auto_actions.click(devices.devices_web_elements.get_actions_network_policy_assign_button())
    time.sleep(10)


@pytest.fixture(scope="session")
def nodes():
    return _nodes


@pytest.fixture(scope="session")
def standalone_nodes():
    return _standalone_nodes


@pytest.fixture(scope="session")
def stack_nodes():
    return _stack_nodes

    
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
def dut_list(standalone_nodes, stack_nodes):
    
    duts = []

    if onboard_two_node_flag:
        duts.extend(standalone_nodes[:2])
    elif onboard_one_node_flag:
        duts.append(standalone_nodes[0])
    
    if onboard_stack_flag:
        duts.append(stack_nodes[0])

    return duts


@pytest.fixture(scope="session")
def update_devices(logger, dut_list, policy_config, debug, wait_till):
    
    @debug
    def update_devices_func(xiq, duts=dut_list):
        
        wait_till(timeout=5)
        xiq.xflowscommonDevices._goto_devices()
        wait_till(timeout=5)

        for dut in duts:
            policy_name = policy_config[dut.name]['policy_name']
            
            logger.step(f"Select switch row with serial '{dut.mac}'.")
            if not xiq.xflowscommonDevices.select_device(dut.mac):
                error_msg = f"Switch '{dut.mac}' is not present in the grid."
                logger.error(error_msg)
                pytest.fail(error_msg)
            wait_till(timeout=2)
            
            logger.step(f"Update the switch: '{dut.mac}'.")
            if xiq.xflowscommonDevices._update_switch(update_method="PolicyAndConfig") != 1:
                error_msg = f"Failed to push the update to this switch: '{dut.mac}'."
                logger.error(error_msg)
                pytest.fail(error_msg)
            wait_till(timeout=2)

        for dut in duts:
            policy_name = policy_config[dut.name]['policy_name']
            if xiq.xflowscommonDevices._check_update_network_policy_status(policy_name, dut.mac) != 1:
                error_msg = f"It look like the update failed this switch: '{dut.mac}'."
                logger.error(error_msg)
                pytest.fail(error_msg) 

    return update_devices_func


@pytest.fixture(scope="session")
def onboard_devices(dut_list, logger, screen, debug, request):
    
    @debug
    def onboard_devices_func(xiq, duts=dut_list):
        onboarding_locations = request.getfixturevalue("onboarding_locations")
        for dut in duts:
            if xiq.xflowscommonDevices.onboard_device(
                device_serial=dut.serial, device_make=dut.cli_type,
                    location=onboarding_locations[dut.name]) == 1:
                logger.info(f"Successfully onboarded this device: '{dut}'.")
                screen.save_screen_shot()
            else:
                error_msg = f"Failed to onboard this device: '{dut}'."
                logger.error(error_msg)
                screen.save_screen_shot()
                pytest.fail(error_msg)
                
    return onboard_devices_func


def dump_data(data):
    return json.dumps(data, indent=4)


@pytest.fixture(scope="session")
def dump_switch_logs(enter_switch_cli, check_duts_are_reachable, dut_list, logger):
    
    exos_cmds = [
        "show mgmt",
        "show ssh2",
        "show iproute",
        "show system",
        "show iqagent",
        "show stacking",
        "show stacking-support",
        "show vlan",
        "show vr",
        "show virtual-network",
        "show ports info",
        "show dns-client",
        "show memory",
        "show session",
        "show cli journal"
    ]
    voss_cmds = [
        "show mgmt interface",
        "show sys-info | no-more",
        "show application iqagent",
        "show ssh session",
        "show vlan members",
        "show ip dns",
        "show int gig int | no-more",
        "show boot config flags",
        "show history",
        "show clock"
    ]

    def func():
        
        def worker(dut):
            try:
                check_duts_are_reachable([dut])
            except:
                logger.warning(f"'{dut.name}' is not reachable so won't dump any info for it.")
                return
        
            with enter_switch_cli(dut) as dev_cmd:
                
                if dut.cli_type.upper() == "EXOS":
                    dev_cmd.send_cmd(dut.name, "disable cli paging", max_wait=10, interval=2)
                    cmds = exos_cmds
                
                elif dut.cli_type.upper() == "VOSS":
                    dev_cmd.send_cmd(dut.name, "enable", max_wait=10, interval=2)
                    dev_cmd.send_cmd(dut.name, "configure terminal", max_wait=10, interval=2)
                    cmds = voss_cmds
                    
                for cmd in cmds:
                    try:
                        output = dev_cmd.send_cmd(dut.name, cmd, max_wait=10, interval=2)[0].return_text
                        logger.cli("*" * 20 + f" {dut.name}: '{cmd.upper()}' " + "*" * 20)
                        logger.cli(output)
                        logger.cli("*" * 20 + f" {dut.name}: '{cmd.upper()}' " + "*" * 20)
                    except Exception:
                        logger.warning(f"Failed to get output of this command from '{dut.name}': '{cmd}'.")
                        
        for dut in dut_list:
            worker(dut)
    return func

  
@pytest.fixture(scope="session")
def onboard(request):

    check_duts_are_reachable = request.getfixturevalue("check_duts_are_reachable")
    configure_network_policies = request.getfixturevalue("configure_network_policies")
    login_xiq = request.getfixturevalue("login_xiq")
    change_device_management_settings = request.getfixturevalue("change_device_management_settings")
    check_devices_are_onboarded = request.getfixturevalue("check_devices_are_onboarded")
    cleanup = request.getfixturevalue("cleanup")
    onboard_devices = request.getfixturevalue("onboard_devices")
    configure_iq_agent = request.getfixturevalue("configure_iq_agent")
    dump_switch_logs = request.getfixturevalue("dump_switch_logs")
    update_devices = request.getfixturevalue("update_devices")
    logger = request.getfixturevalue("logger")
    
    dut_list = request.getfixturevalue("dut_list")
    logger.info(f"These are the devices that will be onboarded ({len(dut_list)} device(s)): " + "'" +
                '\', \''.join([dut.name for dut in dut_list]) + "'.")

    check_duts_are_reachable(dut_list)

    onboarding_locations = request.getfixturevalue("onboarding_locations")
    logger.info(f"These locations will be used for the onboarding:\n'{dump_data(onboarding_locations)}'")
    
    policy_config = request.getfixturevalue("policy_config")
    logger.info(f"These are the policies and switch templates that will be applied to the onboarded devices:"
                f"\n{dump_data(policy_config)}")
    
    try:
        
        configure_iq_agent(duts=dut_list)
        
        with login_xiq() as xiq:
                
            change_device_management_settings(xiq, option="disable")
            
            cleanup(xiq=xiq, duts=dut_list)
            onboard_devices(xiq)
            
            check_devices_are_onboarded(xiq)

            configure_network_policies(xiq)

            update_devices(xiq)

        yield dut_list, policy_config
        
    except Exception as exc:
        logger.error(repr(exc))
        dump_switch_logs()
        logger.error(traceback.format_exc())
        pytest.fail(f"The onboarding failed for these devices: {dut_list}\n{traceback.format_exc()}")
    

@pytest.fixture(scope="session")
def onboard_cleanup(request):
    
    login_xiq = request.getfixturevalue("login_xiq")
    stack_nodes = request.getfixturevalue("stack_nodes")
    cleanup = request.getfixturevalue("cleanup")
    dut_list = request.getfixturevalue("dut_list")
    policy_config = request.getfixturevalue("policy_config")
    
    with login_xiq() as xiq:

        cleanup(
            xiq=xiq, 
            duts=dut_list, 
            network_policies=[dut_info['policy_name'] for dut_info in policy_config.values()],
            templates_switch=[dut_info['template_name'] for dut_info in policy_config.values()],
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
def dut_ports(enter_switch_cli, dut_list, debug):
    
    ports = {}
    
    @debug
    def dut_ports_worker(dut):
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
            thread = threading.Thread(target=dut_ports_worker, args=(dut, ))
            threads.append(thread)
            thread.start()
    finally:
        for thread in threads:
            thread.join()
    return ports


@pytest.fixture(scope="session")
def bounce_iqagent(enter_switch_cli, debug):
    
    @debug
    def bounce_iqagent_func(dut, xiq=None, wait=False):
        
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
    return bounce_iqagent_func


@pytest.fixture(scope="session")
def reboot_device(dut_list, enter_switch_cli, logger, debug, wait_till):
    
    @debug
    def reboot_device_func(duts=dut_list):
        
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
                    logger.error(error_msg)
                    wait_till(timeout=5)
                    pytest.fail(error_msg)
                else:
                    wait_till(timeout=120)
    
        threads = []
        try:
            for dut in duts:
                thread = threading.Thread(target=worker, args=(dut, ))
                threads.append(thread)
                thread.start()
        finally:
            for thread in threads:
                thread.join()
    return reboot_device_func


@pytest.fixture(scope="session")
def reboot_stack_unit(wait_till, enter_switch_cli, debug, logger):
    
    @debug
    def reboot_stack_unit_func(dut, slot=1, save_config='n'):
        
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
                logger.error(error_msg)
                wait_till(timeout=5)
                pytest.fail(error_msg)
            else:
                wait_till(timeout=120)
    return reboot_stack_unit_func


@pytest.fixture(scope="session")
def get_stack_slots(logger, enter_switch_cli, debug):
    
    @debug
    def get_stack_slots_func(dut):
        
        if not (dut.platform.upper() == "STACK" and dut.cli_type.upper() == "EXOS"):
            pytest.fail(f"Given device is not an EXOS stack: '{dut}'")

        slots_info = {}
        with enter_switch_cli(dut) as dev_cmd:
            output = dev_cmd.send_cmd(dut.name, 'show stacking', max_wait=10, interval=2)[0].return_text
            logger.cli(output)
            rows = re.findall(r'((?:[0-9a-fA-F]:?){12})\s+(\d+)\s+(\w+)\s+(\w+)\s+(.*)\r\n', output, re.IGNORECASE)
            
            for row in rows:
                slots_info[row[1]] = dict(zip(["Node MAC Address", "Slot", "Stack State", "Role", "Flags"], row))
            logger.info(f"Found these slots on the stack device '{dut.name}': {dump_data(slots_info)}.")
            return slots_info
    return get_stack_slots_func


@pytest.fixture(scope="session")
def modify_stacking_node(enter_switch_cli, reboot_device, debug):
    
    @debug
    def modify_stacking_node_func(dut, node_mac_address, op):
        if not (dut.platform.upper() == "STACK" and dut.cli_type.upper() == "EXOS"):
            pytest.fail(f"Given device is not an EXOS stack: '{dut}'")

        assert op in ["enable", "disable"], "Op argument should be 'enbale' or 'disable'"
        
        with enter_switch_cli(dut) as dev_cmd:
            cmd = f"{op} stacking node-address {node_mac_address}"
            dev_cmd.send_cmd(dut.name, cmd, max_wait=10, interval=2)
        
        reboot_device(dut)
    return modify_stacking_node_func


@pytest.fixture(scope="session")
def set_lldp(enter_switch_cli, debug):
    
    @debug
    def set_lldp_func(dut, ports, action="enable"):
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
    return set_lldp_func


@pytest.fixture(scope="session")
def clear_traffic_counters(enter_switch_cli, debug):
    
    @debug
    def clear_traffic_counters_func(dut, *ports):
        with enter_switch_cli(dut) as dev_cmd:
            if dut.cli_type.upper() == "EXOS":
                    dev_cmd.send_cmd(
                    dut.name, f"clear counters ports {','.join(ports)}", max_wait=10, interval=2)
            elif dut.cli_type.upper() == "VOSS":
                dev_cmd.send_cmd(
                    dut.name, f"clear-stats port {','.join(ports)}", max_wait=10, interval=2)
    return clear_traffic_counters_func


@pytest.fixture(scope="session")
def change_device_management_settings(logger, standalone_nodes, stack_nodes, screen, debug, wait_till):
    
    @debug
    def change_device_management_settings_func(xiq, option, retries=5, step=5):
        
        platform = "EXOS" if any(node.cli_type.upper() == "EXOS" for node in standalone_nodes + stack_nodes) else "VOSS"
        for _ in range(retries):
            try:
                xiq.xflowsglobalsettingsGlobalSetting.change_exos_device_management_settings(
                    option=option, platform=platform)
                screen.save_screen_shot()
            except Exception as exc:
                logger.warning(repr(exc))
                screen.save_screen_shot()
                wait_till(timeout=step)
            else:
                xiq.xflowscommonNavigator.navigate_to_devices()
                break
        else:
            pytest.fail("Failed to change exos device management settings.")
    return change_device_management_settings_func


@pytest.fixture(scope="session")
def get_default_password(navigator, auto_actions, debug, screen, wait_till):
    
    @debug
    def get_default_password_func(xiq):
        xiq.xflowscommonDevices._goto_devices()
        navigator.navigate_to_global_settings_page()
        
        menu, _ = wait_till(
            func=xiq.xflowsglobalsettingsGlobalSetting.get_device_management_settings_menu,
            silent_failure=True,
            delay=4
        )
        screen.save_screen_shot()
        assert menu, "Failed to get the device management settings menu"
        
        wait_till(func=lambda: auto_actions.click(menu) == 1)
        screen.save_screen_shot()
        
        password, _ = wait_till(
            func=xiq.xflowsglobalsettingsGlobalSetting.get_device_management_settings_password,
            silent_failure=True,
            delay=4
        )
        screen.save_screen_shot()
        assert password, "Failed to get the default device passowrd"
        return password.get_attribute('value')
    return get_default_password_func


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
def dut1(testbed, logger):
    try:
        return getattr(testbed, "dut1")
    except AttributeError as err:
        logger.error(f"The testbed does not have the 'dut1' netelem.")
        raise err


@pytest.fixture(scope="session")
def dut2(testbed, logger):
    try:
        return getattr(testbed, "dut2")
    except AttributeError as err:
        logger.error(f"The testbed does not have the 'dut2' netelem.")
        raise err


@pytest.fixture(scope="session")
def dut3(testbed, logger):
    try:
        return getattr(testbed, "dut3")
    except AttributeError as err:
        logger.error(f"The testbed does not have the 'dut3' netelem.")
        raise err


@pytest.fixture(scope="session")
def network_manager():
    from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import \
        NetworkElementConnectionManager
    return NetworkElementConnectionManager()


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

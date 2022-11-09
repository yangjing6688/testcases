import string
import pytest
import time
import os
import random
import re

from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import \
    NetworkElementConnectionManager
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary


def init_xiq_libraries_and_login(
        username, password, capture_version=False, code="default", url="default", incognito_mode="False"):
    xiq = XiqLibrary()
    time.sleep(5)

    try:
        assert xiq.login.login_user(
            username, password, capture_version=capture_version, code=code, url=url, incognito_mode=incognito_mode)
    except Exception as exc:
        print(repr(exc))
        from extauto.common.CloudDriver import CloudDriver
        CloudDriver().close_browser()
        raise exc

    return xiq


def delete_create_location_organization(xiq, location):
    try:
        xiq.xflowsmanageLocation.create_first_organization("Extreme", "broadway", "newyork", "Romania")
    except:
        pass
    xiq.xflowsmanageLocation.delete_location_building_floor(*location.split(","))
    xiq.xflowsmanageLocation.create_location_building_floor(*location.split(","))


def deactivate_xiq_libraries_and_logout(xiq):
    xiq.login.logout_user()
    xiq.login.quit_browser()


def delete_device(xiq, dut):
    xiq.xflowscommonDevices._goto_devices()
    xiq.xflowscommonDevices.delete_device(device_mac=dut.mac)


def get_dut(tb, os):
    for dut_index in [f"dut{i}" for i in range(10)]:
        if getattr(tb, dut_index, {}).get("cli_type") == os and getattr(tb, dut_index, {}).get("platform").upper() == "STACK":
            return dut_index
    return None


def close_connection_with_error_handling(dut, network_manager):
    try:
        network_manager.device_collection.remove_device(dut.name)
        network_manager.close_connection_to_network_element(dut.name)
    except Exception as exc:
        print(exc)


def netelement_iqagent_config(devCmd, dutName, xiq_ip_address):
    devCmd.send_cmd(dutName, 'disable iqagent', max_wait=10, interval=2,
                    confirmation_phrases='Do you want to continue?', confirmation_args='Yes')

    devCmd.send_cmd(dutName, 'configure iqagent server ipaddress none', max_wait=10, interval=2)
    devCmd.send_cmd(dutName, 'configure iqagent server vr none', max_wait=10, interval=2)

    devCmd.send_cmd_verify_output(dutName, 'show process iqagent', 'Ready', max_wait=30, interval=10)

    devCmd.send_cmd(dutName, 'configure iqagent server ipaddress ' + xiq_ip_address, max_wait=10, interval=2)
    devCmd.send_cmd(dutName, 'configure iqagent server vr vr-Mgmt', max_wait=10, interval=2)
    devCmd.send_cmd(dutName, 'enable iqagent', max_wait=10, interval=2)

    devCmd.send_cmd_verify_output_regex(dutName, 'show iqagent', 'Status*.*CONNECTED TO XIQ', max_wait=180,
                                        interval=10)


def netelement_iqagent_restart(devCmd, dutName):
    devCmd.send_cmd(dutName, 'disable iqagent', max_wait=10, interval=2,
                    confirmation_phrases='Do you want to continue?', confirmation_args='Yes')
    devCmd.send_cmd(dutName, 'enable iqagent', max_wait=10, interval=2)

    devCmd.send_cmd_verify_output_regex(dutName, 'show iqagent', 'Status*.*CONNECTED TO XIQ', max_wait=180,
                                        interval=10)


def check_stack_status_in_xiq(xiq, dutMac):
    time.sleep(120)

    xiq.xflowsmanageDevices.refresh_devices_page()
    time.sleep(10)

    result = xiq.xflowscommonDevices.get_device_stack_status(device_mac=dutMac)
    max_wait = 300
    time_elapsed = 0
    while result != "blue" and max_wait >= 0:
        print(f"\nINFO \tTime elaspsed in waiting for the stack formation is {time_elapsed} seconds \n")
        time.sleep(10)
        max_wait -= 10
        time_elapsed += 10
        result = xiq.xflowscommonDevices.get_device_stack_status(device_mac=dutMac)
        if (result == "red" or result == -1) and max_wait == 0:
            print("\nFAILED \t Stack not formed properly, please check.\n")
            pytest.fail('Expected stack icon colour is blue but found {}, stack not formed properly'.format(result))


def get_master_mac(devCmd, dut):
    output = devCmd.send_cmd(dut.name, 'show stacking', max_wait=10, interval=2)[0].return_text.split("\r\n")
    for row in output:
        if "Master" in row:
            return re.search(r'(?:[0-9a-fA-F]:?){12}', row).group(0)


@pytest.fixture(scope="package", autouse=True)
def onboarding_location():
    pool = list(string.ascii_letters) + list(string.digits)
    return f"Salem_{''.join(random.sample(pool, k=4))},Northeastern_{''.join(random.sample(pool, k=4))}," \
           f"Floor_{''.join(random.sample(pool, k=4))}"


@pytest.fixture(scope="package", autouse=True)
def onboarded_stack(onboarding_location):
    tb = PytestConfigHelper(config)
    config['${TEST_NAME}'] = "onboarding"
    config['${OUTPUT DIR}'] = os.getcwd()
    for word in ["tenant_username", "tenant_password", "test_url"]:
        config[f"${{{word.upper()}}}"] = config[word]

    defaultLibrary = DefaultLibrary()
    devCmd = defaultLibrary.deviceNetworkElement.networkElementCliSend
    network_manager = NetworkElementConnectionManager()

    dut_index = get_dut(tb, os="exos")
    assert dut_index, "Failed to find a dut in tb"
    dut = getattr(tb, dut_index)

    xiq = init_xiq_libraries_and_login(config['tenant_username'], config['tenant_password'], config['test_url'])

    try:
        delete_create_location_organization(xiq, onboarding_location)
    except Exception as exc:
        print(repr(exc))
        deactivate_xiq_libraries_and_logout(xiq)
        raise exc

    try:

        try:
            close_connection_with_error_handling(dut, network_manager)
            network_manager.connect_to_network_element_name(dut.name)

            xiq.xflowscommonDevices.delete_device(device_mac=dut.mac)

            assert xiq.xflowscommonDevices.onboard_device_quick(dut) == 1
            time.sleep(5)

            netelement_iqagent_config(devCmd, dut.name, config['sw_connection_host'])

            check_stack_status_in_xiq(xiq, dut.mac)

            time.sleep(5)
            netelement_iqagent_restart(devCmd, dut.name)

            xiq.xflowscommonDevices.wait_until_device_online(device_mac=dut.mac)
            res = xiq.xflowscommonDevices.get_device_status(device_mac=dut.mac)
            assert res == 'green', f"The Stack device did not come up successfully in the XIQ; Device: {dut}"

        finally:

            deactivate_xiq_libraries_and_logout(xiq)

        yield dut

    finally:

        xiq = init_xiq_libraries_and_login(config['tenant_username'], config['tenant_password'], config['test_url'])

        try:
            close_connection_with_error_handling(dut, network_manager)
            delete_device(xiq, dut)
            xiq.xflowsmanageLocation.delete_location_building_floor(*onboarding_location.split(","))
        finally:
            deactivate_xiq_libraries_and_logout(xiq)

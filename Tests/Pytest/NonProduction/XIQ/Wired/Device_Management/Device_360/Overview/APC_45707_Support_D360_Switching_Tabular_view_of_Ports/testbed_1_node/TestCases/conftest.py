import pytest
import time
import os
import random
import string

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


def deactivate_xiq_libaries_and_logout(xiq):
    xiq.login.logout_user()
    xiq.login.quit_browser()


def delete_device(xiq, dut):
    try:
        xiq.xflowscommonDevices._goto_devices()
        xiq.xflowscommonDevices.delete_device(device_serial=dut.serial)
    except Exception as exc:
        print(repr(exc))


def get_dut(tb, os):
    for dut_index in [f"dut{i}" for i in range(3)]:
        if getattr(tb, dut_index, {}).get("cli_type", "").upper() == os.upper():
            return getattr(tb, dut_index)


def close_connection_with_error_handling(dut, network_manager):
    try:
        network_manager.device_collection.remove_device(dut.name)
        network_manager.close_connection_to_network_element(dut.name)
    except Exception as exc:
        print(exc)


def delete_create_location_organization(xiq, location):
    try:
        xiq.xflowsmanageLocation.create_first_organization("Extreme", "broadway", "newyork", "Romania")
    except:
        pass
    xiq.xflowsmanageLocation.delete_location_building_floor(*location.split(","))
    xiq.xflowsmanageLocation.create_location_building_floor(*location.split(","))


@pytest.fixture(scope="package", autouse=True)
def onboarding_location():
    pool = list(string.ascii_letters) + list(string.digits)
    return f"Salem_{''.join(random.sample(pool, k=4))},Northeastern_{''.join(random.sample(pool, k=4))}," \
           f"Floor_{''.join(random.sample(pool, k=4))}"


def deactivate_xiq_libraries_and_logout(xiq):
    xiq.login.logout_user()
    xiq.login.quit_browser()


@pytest.fixture(scope="package", autouse=True)
def onboarded_switch(onboarding_location, pytestconfig):

    tb = PytestConfigHelper(config)
    config['${TEST_NAME}'] = "onboarding"
    config['${OUTPUT DIR}'] = os.getcwd()
    for word in ["tenant_username", "tenant_password", "test_url"]:
        config[f"${{{word.upper()}}}"] = config[word]

    defaultLibrary = DefaultLibrary()
    devCmd = defaultLibrary.deviceNetworkElement.networkElementCliSend
    network_manager = NetworkElementConnectionManager()

    markers = pytestconfig.getoption('-m')
    
    if "EXOS" in markers:
        dut = get_dut(tb, "EXOS")
    elif "VOSS" in markers:
        dut = get_dut(tb, "VOSS")
    else:
        dut = tb.dut1

    assert dut, "Failed to get a dut from tb"

    xiq = init_xiq_libraries_and_login(config['tenant_username'], config['tenant_password'], config['test_url'])

    try:
        delete_create_location_organization(xiq, onboarding_location)
    except Exception as exc:
        print(repr(exc))
        deactivate_xiq_libraries_and_logout(xiq)
        raise exc
    
    try:
        try:
            network_manager.connect_to_network_element_name(dut.name)

            xiq.xflowscommonDevices.delete_device(device_serial=dut.serial)

            assert xiq.xflowsmanageSwitch.onboard_switch(
                dut.serial, device_os=dut.cli_type, location=onboarding_location) == 1, \
                f"Failed to onboard this dut to XiQ: {dut}"

            if dut.cli_type.upper() == "EXOS":
                devCmd.send_cmd_verify_output(dut.name, 'show process iqagent', 'Ready', max_wait=30, interval=10)
                devCmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2,
                                confirmation_phrases='Do you want to continue?', confirmation_args='y')
                devCmd.send_cmd(dut.name, 'configure iqagent server ipaddress none', max_wait=10, interval=2)
                devCmd.send_cmd(dut.name, 'configure iqagent server ipaddress ' + config['sw_connection_host'],
                                max_wait=10, interval=2)
                devCmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)
                time.sleep(10)

            elif dut.cli_type.upper() == "VOSS":
                devCmd.send_cmd(dut.name, 'configure terminal', max_wait=10, interval=2)
                devCmd.send_cmd(dut.name, 'application', max_wait=10, interval=2)
                devCmd.send_cmd(dut.name, 'no iqagent enable', max_wait=10, interval=2)
                devCmd.send_cmd(dut.name, 'iqagent server ' + config['sw_connection_host'],
                                max_wait=10, interval=2)
                devCmd.send_cmd(dut.name, 'iqagent enable', max_wait=10, interval=2)
                devCmd.send_cmd_verify_output(dut.name, 'show application iqagent', 'true', max_wait=30,
                                                interval=10)
                devCmd.send_cmd(dut.name, 'exit', max_wait=10, interval=2)
                time.sleep(10)

            xiq.xflowscommonDevices.wait_until_device_online(dut.serial)
            res = xiq.xflowscommonDevices.get_device_status(device_serial=dut.serial)
            assert res == 'green', f"The device did not come up successfully in the XIQ; Device: {dut}"

        finally:
            deactivate_xiq_libraries_and_logout(xiq)

        yield dut

    finally:

        xiq = init_xiq_libraries_and_login(config['tenant_username'], config['tenant_password'], config['test_url'])

        try:
            xiq.xflowsmanageLocation.delete_location_building_floor(*onboarding_location.split(","))
        except Exception as exc:
            print(repr(exc))

        try:
            close_connection_with_error_handling(dut, network_manager)
            delete_device(xiq, dut)
        finally:
            deactivate_xiq_libraries_and_logout(xiq)

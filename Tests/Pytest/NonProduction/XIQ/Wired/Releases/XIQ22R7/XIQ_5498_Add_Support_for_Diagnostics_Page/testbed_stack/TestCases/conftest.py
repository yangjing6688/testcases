import pytest
import time
import os
import re
import random
import string

from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import \
    NetworkElementConnectionManager
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from extauto.common.CloudDriver import CloudDriver
from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R7.XIQ_5498_Add_Support_for_Diagnostics_Page.testbed_stack.Resources.SuiteUdks import SuiteUdk


def init_xiq_libraries_and_login(
        username, password, capture_version=False, code="default", url="default", incognito_mode="False"):
    xiq = XiqLibrary()
    time.sleep(4)
    res = xiq.login.login_user(
        username=username, password=password, capture_version=capture_version, code=code, url=url,
        incognito_mode=incognito_mode)

    if res != 1:
        pytest.fail('Could not Login')

    return xiq

def cleanup(xiq, dut=None, onboarding_location=''):
    try:
        if dut:
            xiq.xflowscommonDevices._goto_devices()
            xiq.xflowscommonDevices.delete_device(device_mac=dut.mac)
        if onboarding_location:
            xiq.xflowsmanageLocation.delete_location_building_floor(*onboarding_location.split(","))
    except Exception as exc:
        print(repr(exc))

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


def delete_create_location_organization(xiq, location):
    try:
        xiq.xflowsmanageLocation.create_first_organization("Extreme", "broadway", "newyork", "Romania")
    except:
        pass
    xiq.xflowsmanageLocation.delete_location_building_floor(*location.split(","))
    xiq.xflowsmanageLocation.create_location_building_floor(*location.split(","))


def close_connection_with_error_handling(dut, network_manager):
    try:
        network_manager.device_collection.remove_device(dut.name)
        network_manager.close_connection_to_network_element(dut.name)
    except Exception as exc:
        print(exc)
    else:
        time.sleep(30)


def configure_iq_agent(dut, devCmd, config):
    localsuiteudks = SuiteUdk()
    if dut.cli_type.upper() == "EXOS":
        devCmd.send_cmd_verify_output(dut.name, 'show process iqagent', 'Ready', max_wait=30, interval=10)
        devCmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2,
                        confirmation_phrases='Do you want to continue?', confirmation_args='y')
        vr_name = localsuiteudks.get_virtual_router(dut)
        if vr_name == -1:
            print("Error: Can't extract Virtual Router information")
            return -1
        devCmd.send_cmd(dut.name, f'configure iqagent server vr {vr_name}', max_wait=10, interval=2)

        devCmd.send_cmd(dut.name, 'configure iqagent server ipaddress ' + config['sw_connection_host'],
                        max_wait=10, interval=2)
        devCmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)
    elif dut.cli_type.upper() == "VOSS":
        pytest.skip("Configure iqagent if cli type is VOSS - To be done - Other platform than EXOS is not yet supported")
    time.sleep(10)


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

    dut = tb.dut1
    assert dut is not None, "Failed to get the dut from tb"
    network_manager.connect_to_network_element_name(dut.name)

    xiq = init_xiq_libraries_and_login(config['tenant_username'], config['tenant_password'], config['test_url'])
    change_device_management_settings(xiq, option="disable", platform=dut.cli_type.upper())

    try:
        cleanup(xiq, dut=dut)
        delete_create_location_organization(xiq, location=onboarding_location)
    except Exception as exc:
        print(repr(exc))
        deactivate_xiq_libraries_and_logout(xiq)
        raise exc

    try:
        try:
            if dut.platform.upper() != "STACK":
                pytest.skip("Other platform then STACK is not supported")
            if dut.cli_type.upper() != "EXOS":
                pytest.skip("Other platform than EXOS is not yet supported")


            assert xiq.xflowsmanageSwitch.onboard_switch(
                dut.serial, device_os=dut.cli_type,
                location=onboarding_location) == 1, f"Failed to onboard this dut to XiQ: {dut}"


            configure_iq_agent(dut, devCmd, config)

            assert xiq.xflowscommonDevices.wait_until_device_online(device_mac=dut.mac) == 1, \
                f"Device {dut} didn't get online"

            res = xiq.xflowscommonDevices.wait_until_device_managed(device_serial=dut.mac)
            assert res == 1, f"The device does not appear as Managed in the XIQ; Device: {dut}."

        finally:
            deactivate_xiq_libraries_and_logout(xiq)
        yield dut

    finally:
        xiq = init_xiq_libraries_and_login(config['tenant_username'], config['tenant_password'], config['test_url'])

        try:
            cleanup(xiq=xiq, dut=dut,onboarding_location=onboarding_location)
            xiq.xflowsmanageLocation.delete_location_building_floor(*onboarding_location.split(","))
        except Exception as exc:
            print(repr(exc))
        finally:
            deactivate_xiq_libraries_and_logout(xiq)
        close_connection_with_error_handling(dut, network_manager)
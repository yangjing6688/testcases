import pytest
import time
import re
import os
import random
import string
import datetime

from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import \
    NetworkElementConnectionManager
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from Tests.Pytest.NonProduction.XIQ.XIQ_1365.testbed_1_node.Resources.SuiteUdks import SuiteUdk


def init_xiq_libraries_and_login(
        username, password, capture_version=False, code="default", url="default", incognito_mode="False"):
    xiq = XiqLibrary()
    time.sleep(4)
    assert xiq.login.login_user(
        username=username, password=password, capture_version=capture_version, code=code, url=url,
        incognito_mode=incognito_mode)
    return xiq


def deactivate_xiq_libraries_and_logout(xiq):
    xiq.login.logout_user()
    xiq.login.quit_browser()


def delete_device(xiq, dut):
    xiq.xflowscommonDevices._goto_devices()
    xiq.xflowscommonDevices.delete_device(device_serial=dut.serial)


def get_dut(tb, os):
    for dut_index in [f"dut{i}" for i in range(10)]:
        if getattr(tb, dut_index, {}).get("cli_type") == os:
            return dut_index
    return None

def close_connection_with_error_handling(dut, network_manager):
    try:
        network_manager.device_collection.remove_device(dut.name)
        network_manager.close_connection_to_network_element(dut.name)
    except Exception as exc:
        print(exc)
    else:
        time.sleep(30)


@pytest.fixture(scope="session", autouse=True)
def onboarding_location():
    pool = list(string.ascii_letters) + list(string.digits)
    return f"Salem_{''.join(random.sample(pool, k=4))},Northeastern_{''.join(random.sample(pool, k=4))},Floor_{''.join(random.sample(pool, k=4))}"

@pytest.fixture(scope="session", autouse=True)
def setup_switch(onboarding_location):
    tb = PytestConfigHelper(config)
    config['${TEST_NAME}'] = "onboarding"
    config['${OUTPUT DIR}'] = os.getcwd()
    for word in ["tenant_username", "tenant_password", "test_url"]:
        config[f"${{{word.upper()}}}"] = config[word]

    defaultLibrary = DefaultLibrary()
    devCmd = defaultLibrary.deviceNetworkElement.networkElementCliSend
    network_manager = NetworkElementConnectionManager()
    suite_udk = SuiteUdk()

    dut_index = random.choice([d for d in [get_dut(tb, os="exos"), get_dut(tb, os="voss")] if d])
    assert dut_index, "Failed to find a dut in tb"
    dut = getattr(tb, dut_index)
    dut.location = onboarding_location

    if tb.config.netelem1.cli_type.upper() != "EXOS":
        assert -1, "Other platform then EXOS is not supported"

    xiq_ip_address = config['sw_connection_host']

    try:
        close_connection_with_error_handling(dut, network_manager)
        network_manager.connect_to_network_element_name(dut.name)

        xiq = init_xiq_libraries_and_login(config['tenant_username'], config['tenant_password'], config['test_url'])
        xiq.xflowscommonDevices.delete_device(device_serial=dut.serial)

        xiq.xflowsmanageLocation.delete_location_building_floor(*onboarding_location.split(","))
        xiq.xflowsmanageLocation.create_location_building_floor(*onboarding_location.split(","))

        xiq.xflowsglobalsettingsGlobalSetting.change_exos_device_management_settings(option="disable",
                                                                                     platform=tb.config.netelem1.cli_type)

        image_version = ""
        ga_version = r".*version\s+(\d+\.\d+\.\d+\.\d+)\s+by"
        patch_version = r".*version\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+-patch.*)\s+by"

        output_cmd = devCmd.send_cmd(dut.name, 'show version', max_wait=10, interval=2)[0].return_text
        args = re.findall(patch_version, output_cmd)
        if len(args) == 1:
            image_version = args[0][1]
        else:
            args = re.findall(ga_version, output_cmd)
            if len(args) == 1:
                image_version = args[0]
            else:
                assert -1, f"Image pattern didn't match"
        print(f"Initial image version on device is {image_version}")

        deactivate_xiq_libraries_and_logout(xiq)

        close_connection_with_error_handling(dut, network_manager)

        yield dut

    finally:
        try:
            close_connection_with_error_handling(dut, network_manager)
            network_manager.connect_to_network_element_name(dut.name)

            # Onboard the switch to put the initial image back
            xiq = init_xiq_libraries_and_login(config['tenant_username'], config['tenant_password'], config['test_url'])

            onboarding_is_successful = xiq.xflowscommonDevices.onboard_device(device_serial=dut.serial,
                                                                              device_make=dut.cli_type,
                                                                              device_mac=dut.mac,
                                                                              device_os=dut.cli_type,
                                                                              location=onboarding_location) == 1
            
            devCmd.send_cmd(dut.name, f'configure iqagent server ipaddress {xiq_ip_address}', max_wait=10, interval=2)

            vrName = suite_udk.get_virtual_router(dut)
            devCmd.send_cmd(dut.name, f'configure iqagent server vr {vrName}', max_wait=10, interval=2)

            devCmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)

            devCmd.send_cmd_verify_output(dut.name, 'show process iqagent', 'Ready', max_wait=30,
                                          interval=10)

            assert xiq.xflowscommonDevices.wait_until_device_online(dut.serial) == 1, \
                f"Device {dut} didn't get online"
            time.sleep(5)
            assert xiq.xflowscommonDevices.wait_until_device_managed(dut.serial) == 1, \
                f"Device {dut} didn't get in MANAGED state"
            time.sleep(5)

            # res = xiq.xflowscommonDevices.get_device_status(device_serial=dut.serial)
            res = suite_udk.get_device_status_debug(dut, 'green')
            assert res == 'green', f"The EXOS device did not come up successfully in the XIQ; Device: {dut}"

            if onboarding_is_successful:
                assert xiq.xflowscommonDevices.upgrade_device(dut, version=image_version) != -1, f"Failed to update device back to the initial firmware version"

                # Checking for the update column to reflect the firmware update status
                status_after = xiq.xflowscommonDevices.get_device_updated_status(device_serial=dut.serial)
                count = 0
                max_wait = 900
                current_date = datetime.datetime.now()
                update_text = str(current_date).split()[0]
                while update_text not in status_after:
                    time.sleep(10)
                    count += 10
                    status_after = xiq.xflowscommonDevices.get_device_updated_status(device_serial=dut.serial)
                    print(
                        f"\nINFO \t Time elapsed in the update column to reflect the firmware updating is '{count} seconds'\n")
                    if ("Failed" in status_after) or ("failed" in status_after) or (count > max_wait):
                        pytest.fail("Device Update Failed for the device with serial {}".format(dut.serial))

                assert xiq.xflowscommonDevices.wait_until_device_online(dut.serial) == 1, \
                    f"Device {dut} didn't get online"
                assert xiq.xflowscommonDevices.wait_until_device_managed(dut.serial) == 1, \
                    f"Device {dut} didn't get in MANAGED state"
                # res = xiq.xflowscommonDevices.get_device_status(device_serial=dut.serial)
                res = suite_udk.get_device_status_debug(dut, 'green')
                assert res == 'green', f"The EXOS device did not come up successfully in the XIQ; Device: {dut}"

        finally:
            try:
                delete_device(xiq, dut)
                xiq.xflowsmanageLocation.delete_location_building_floor(*onboarding_location.split(","))
            finally:
                deactivate_xiq_libraries_and_logout(xiq)

            close_connection_with_error_handling(dut, network_manager)


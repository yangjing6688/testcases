import os
import random
import re
from time import sleep

import pytest
from pytest_testconfig import config

from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import \
    NetworkElementConnectionManager


def init_xiq_libraries_and_login(
        username, password, capture_version=False, code="default", url="default", incognito_mode="False"):
    xiq = XiqLibrary()
    sleep(4)
    assert xiq.login.login_user(
        username, password, capture_version=capture_version, code=code, url=url, incognito_mode=incognito_mode)
    return xiq


def deactivate_xiq_libraries_and_logout(xiq):
    xiq.login.logout_user()
    xiq.login.quit_browser()


def delete_device(xiq, dut):
    xiq.xflowscommonNavigator.navigate_to_devices()
    xiq.xflowscommonDevices.delete_device(device_serial=dut.serial)


def get_dut(tb, platform):
    for dut_index in [f"dut{i}" for i in range(10)]:
        if getattr(tb, dut_index, {}).get("cli_type") == platform:
            return dut_index
    return None


def close_connection_with_error_handling(dut, network_manager):
    try:
        network_manager.device_collection.remove_device(dut.name)
        network_manager.close_connection_to_network_element(dut.name)
    except Exception as exc:
        print(exc)
    else:
        sleep(2)


def cleanup_before_run(xiq, dut=None, onboarding_location='', network_policy='', template_switch=''):
    if dut:
        xiq.xflowscommonDevices.delete_device(device_serial=dut.serial)
    if network_policy:
        xiq.xflowsconfigureNetworkPolicy.delete_network_policy(network_policy)
    if template_switch:
        xiq.xflowsconfigureCommonObjects.delete_switch_template(template_switch)
    if onboarding_location:
        xiq.xflowsmanageLocation.delete_location_building_floor(*onboarding_location.split(","))


def netelement_iqagent_enable_disable(dev_cmd, dut_name, op):
    if op == "enable" or op == "disable":
        op_string = op
    else:
        return -1
    op_string = op_string + ' iqagent'
    return dev_cmd.send_cmd(dut_name, op_string, max_wait=10, interval=2,
                            confirmation_phrases='Do you want to continue?', confirmation_args='Yes')


def configure_iqagent(dev_cmd, dut, xiq_ip_address):
    dev_cmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2)
    dev_cmd.send_cmd(dut.name, f'configure iqagent server ipaddress {xiq_ip_address}', max_wait=10, interval=2)

    vr_name = get_virtual_router(dev_cmd, dut)
    if vr_name == -1:
        print("Error: Can't extract Virtual Router information")
        return -1
    dev_cmd.send_cmd(dut.name, f'configure iqagent server vr {vr_name}', max_wait=10, interval=2)

    dev_cmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)
    dev_cmd.send_cmd_verify_output(dut.name, 'show process iqagent', 'Ready', max_wait=30, interval=10)


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


@pytest.fixture(scope="package", autouse=True)
def network_policy():
    np = f"NP_XIQ_1157_stdln"
    return np


@pytest.fixture(scope="package", autouse=True)
def template_switch():
    template_sw = f"ST_XIQ_1157_stdln"
    return template_sw


@pytest.fixture(scope="package", autouse=True)
def onboarding_location():
    return f"Salem_XIQ_1157_stdln,Northeastern_XIQ_1157_stdln," \
               f"Floor_XIQ_1157_stdln"


@pytest.fixture(scope="package", autouse=True)
def onboarded_dut(onboarding_location, network_policy, template_switch):
    tb = PytestConfigHelper(config)
    config['${TEST_NAME}'] = "onboarding"
    config['${OUTPUT DIR}'] = os.getcwd()
    for word in ["tenant_username", "tenant_password", "test_url"]:
        config[f"${{{word.upper()}}}"] = config[word]

    default_library = DefaultLibrary()

    dev_cmd = default_library.deviceNetworkElement.networkElementCliSend
    network_manager = NetworkElementConnectionManager()

    dut_index = random.choice([d for d in [get_dut(tb, platform="exos"), get_dut(tb, platform="voss")] if d])
    assert dut_index, "Failed to find a dut in tb"
    dut = getattr(tb, dut_index)

    if "5520" not in dut.model:
        pytest.skip(f"Feature supported only on 5520 EXOS switched. invalid platform {dut.model}")

    xiq_ip_address = config['sw_capwap_url']
    xiq = None
    onboarding_is_successful = False

    try:
        network_manager.connect_to_network_element_name(dut.name)
        netelement_iqagent_enable_disable(dev_cmd, dut.name, "disable")

        xiq = init_xiq_libraries_and_login(config['tenant_username'], config['tenant_password'], config['test_url'])

        xiq.xflowsglobalsettingsGlobalSetting.change_exos_device_management_settings(option="disable",
                                                                                     platform=dut.cli_type.upper())
        xiq.xflowscommonNavigator.navigate_to_devices()
        sleep(1)

        cleanup_before_run(xiq=xiq, dut=dut, onboarding_location=onboarding_location,
                           network_policy=network_policy, template_switch=template_switch)

        xiq.xflowsmanageLocation.create_location_building_floor(*onboarding_location.split(","))
        sleep(5)

        onboarding_is_successful = xiq.xflowscommonDevices.onboard_device(device_serial=dut.serial,
                                                                          device_make=dut.os,
                                                                          entry_type="Manual",
                                                                          location=onboarding_location) == 1
        assert onboarding_is_successful, f"onboarding failed for dut serial: {dut.serial}"

        try:
            try:
                print(f"configure EXOS Dut")
                if dut.cli_type.upper() == "EXOS":
                    configure_iqagent(dev_cmd, dut, xiq_ip_address)
                else:
                    pytest.fail(f'Device is not EXOS')
            except Exception as e:
                pytest.fail(e)

            xiq.xflowscommonDevices.wait_until_device_online(dut.serial)
            res = xiq.xflowscommonDevices.get_device_status(device_serial=dut.serial)
            assert res == 'green', f"The EXOS device did not come up successfully in the XIQ; Device: {dut}"

            # Check for VIM module
            xiq.xflowscommonNavigator.navigate_to_device360_page_with_mac(dut.mac)
            sleep(5)
            if not xiq.xflowsmanageDevice360.d360_check_if_vim_is_installed():
                xiq.Utils.print_info("Error: Invalid setup, no actual VIM module installed")
                pytest.skip("Invalid setup: no actual VIM module installed")
            xiq.xflowsmanageDevice360.close_device360_window()
            sleep(1)

            create_np = xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(network_policy)
            assert create_np == 1, f"Policy {network_policy} wasn't created successfully "
            sw_model_template = "Switch Engine "
            if "Engine" in dut.model:
                sw_model_template += dut.model.split("Engine", 1)[1].replace('_', '-')
            else:
                sw_model_template += dut.model.replace('_', '-')
            xiq.xflowsconfigureSwitchTemplate.\
                add_sw_template(network_policy, sw_model_template, template_switch)
            assert xiq.xflowsmanageDevices.\
                assign_network_policy_to_switch(policy_name=network_policy, serial=dut.serial) == 1, \
                f"Couldn't assign policy {network_policy} to device {dut}"
        except Exception as e:
            pytest.fail(e)
        finally:
            deactivate_xiq_libraries_and_logout(xiq)

        close_connection_with_error_handling(dut, network_manager)

        yield dut

    except Exception as e:
        if xiq:
            deactivate_xiq_libraries_and_logout(xiq)
        pytest.fail(e)
    finally:

        close_connection_with_error_handling(dut, network_manager)

        if onboarding_is_successful:
            xiq = init_xiq_libraries_and_login(config['tenant_username'], config['tenant_password'], config['test_url'])

            delete_device(xiq, dut)
            xiq.xflowsconfigureNetworkPolicy.delete_network_policy(network_policy)
            xiq.xflowsconfigureCommonObjects.delete_switch_template(template_switch)
            xiq.xflowsmanageLocation.delete_location_building_floor(*onboarding_location.split(","))
            deactivate_xiq_libraries_and_logout(xiq)

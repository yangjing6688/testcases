import os
import random
import re
import time

import pytest
from pytest_testconfig import config

from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import \
    NetworkElementConnectionManager
from extauto.common.AutoActions import AutoActions


def init_xiq_libraries_and_login(
        username, password, capture_version=False, code="default", url="default", incognito_mode="False"):
    xiq = XiqLibrary()
    time.sleep(5)
    assert xiq.login.login_user(
        username, password, capture_version=capture_version, code=code, url=url, incognito_mode=incognito_mode)
    return xiq


def deactivate_xiq_libraries_and_logout(xiq):
    xiq.login.logout_user()
    xiq.login.quit_browser()


def delete_device(xiq, dut):
    xiq.xflowscommonNavigator.navigate_to_devices()
    xiq.xflowscommonDevices.delete_device(device_mac=dut.mac)


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
        time.sleep(30)


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


def netelement_iqagent_config(dev_cmd, dut, xiq_ip_address):

    vr_name = get_virtual_router(dev_cmd, dut)
    if vr_name == -1:
        print("Error: Can't extract Virtual Router information")
        return -1

    dev_cmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2,
                     confirmation_phrases='Do you want to continue?', confirmation_args='Yes')

    # An existing iqagent configs will be removed from device prior to configure the iqagent
    dev_cmd.send_cmd(dut.name, 'configure iqagent server ipaddress none', max_wait=10, interval=2)
    dev_cmd.send_cmd(dut.name, 'configure iqagent server vr none', max_wait=10, interval=2)

    # Verify the state of the XIQ agent is up/ready on the dut1(netelement-1)
    dev_cmd.send_cmd_verify_output(dut.name, 'show process iqagent', 'Ready', max_wait=30, interval=10)

    # Configuring and enabling iqagent on netlement-1 based on the environment passed to the test script
    dev_cmd.send_cmd(dut.name, 'configure iqagent server ipaddress ' + xiq_ip_address, max_wait=10, interval=2)
    dev_cmd.send_cmd(dut.name, f'configure iqagent server vr {vr_name}', max_wait=10, interval=2)
    dev_cmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)

    # Verify the iqagent status is connected within the time intervel of 60 seconds
    dev_cmd.send_cmd_verify_output_regex(dut.name, 'show iqagent', 'Status*.*CONNECTED TO XIQ', max_wait=180,
                                         interval=10)


def netelement_iqagent_restart(dev_cmd, dut_name):
    # Restart the iqagent process
    dev_cmd.send_cmd(dut_name, 'disable iqagent', max_wait=10, interval=2,
                     confirmation_phrases='Do you want to continue?', confirmation_args='Yes')
    dev_cmd.send_cmd(dut_name, 'enable iqagent', max_wait=10, interval=2)

    # Verify the iqagent status is connected within the time intervel of 60 seconds
    dev_cmd.send_cmd_verify_output_regex(dut_name, 'show iqagent', 'Status*.*CONNECTED TO XIQ', max_wait=180,
                                         interval=10)


def netelement_iqagent_disable(dev_cmd, dut_name):
    dev_cmd.send_cmd(dut_name, 'disable iqagent', max_wait=10, interval=2,
                     confirmation_phrases='Do you want to continue?', confirmation_args='Yes')


# Check for the stack onboarded is proper and and all the nodes are connected and managed
def check_stack_status_in_xiq(xiq, dut_mac):
    max_wait = 300
    time_elapsed = 0
    result = 0
    print(f"Wait for stack with mac: {dut_mac} to form ")
    while result != "blue" and max_wait >= 0:
        time.sleep(5)
        max_wait -= 5
        time_elapsed += 5
        result = xiq.xflowscommonDevices.get_device_stack_status(device_mac=dut_mac)
        # Once the max_wait time is elapsed it will be declared as not onboarded successfully
        if (result == "red" or result == -1) and max_wait == 0:
            print("\nFAILED \t Stack not formed properly, please check.\n")
            pytest.fail('Expected stack icon colour is blue but found {}, stack not formed properly'.format(result))
    print(f"\nINFO \tTime elapsed in waiting for the stack formation is {time_elapsed} seconds \n")


def assign_network_policy_to_stack(xiq, policy_name, mac):
    xiq.xflowscommonNavigator.navigate_to_devices()
    xiq.xflowscommonDevices.select_device(device_mac=mac)
    AutoActions().click(xiq.xflowscommonDevices.devices_web_elements.get_manage_device_actions_button())
    time.sleep(2)

    AutoActions().click(xiq.xflowscommonDevices.devices_web_elements.get_actions_assign_network_policy_combo())
    time.sleep(2)
    all_items = xiq.xflowscommonDevices.devices_web_elements.get_nw_policy_drop_v2()
    for i in all_items:
        if i.text == "--Select--":
            AutoActions().click(i)
            break

    try:
        network_policy_items = xiq.xflowscommonDevices.devices_web_elements.get_actions_network_policy_drop_down_items()
        time.sleep(2)
        if AutoActions().select_drop_down_options(network_policy_items, policy_name):
            print(f"Selected Network policy from drop down:{policy_name}")
        else:
            print("Network policy is not present in drop down")
            return -1
        AutoActions().click(xiq.xflowscommonDevices.devices_web_elements.get_actions_network_policy_assign_button())
        time.sleep(2)
    except Exception as e:
        print(f"Error:{e}")
        return -1
    return 1


@pytest.fixture(scope="session", autouse=True)
def network_policy():
    np = "NP_XIQ_1157"
    return np


@pytest.fixture(scope="session", autouse=True)
def template_stack():
    template_sw = "ST_XIQ_1157"
    return template_sw


def dut_stack_model_update(dut, stack_dict):
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


@pytest.fixture(scope="session", autouse=True)
def onboarded_dut(network_policy, template_stack):
    tb = PytestConfigHelper(config)
    config['${TEST_NAME}'] = "onboarding"
    config['${OUTPUT DIR}'] = os.getcwd()
    for word in ["tenant_username", "tenant_password", "test_url"]:
        config[f"${{{word.upper()}}}"] = config[word]

    default_library = DefaultLibrary()
    dev_cmd = default_library.deviceNetworkElement.networkElementCliSend
    network_manager = NetworkElementConnectionManager()
    onboarding_is_successful = False

    dut_index = random.choice([d for d in [get_dut(tb, platform="exos"), get_dut(tb, platform="voss")] if d])
    assert dut_index, "Failed to find a dut in tb"
    dut = getattr(tb, dut_index)

    location = "Salem_XIQ_1157,Northeastern_XIQ_1157,Floor_XIQ_1157"
    xiq_ip_address = config['sw_connection_host']
    xiq = None

    # Skipping the setup and test case execution in case the platform is not an exos-stack
    if (dut.platform.lower() != 'stack') or ("5520" not in dut.model):
        pytest.skip("This platform {} is not supported for this feature!".format(tb.dut1.cli_type))

    try:
        network_manager.connect_to_network_element_name(dut.name)

        xiq = init_xiq_libraries_and_login(config['tenant_username'], config['tenant_password'], config['test_url'])
        xiq.xflowsglobalsettingsGlobalSetting.change_exos_device_management_settings(option="disable",
                                                                                     platform=dut.cli_type.upper())
        xiq.xflowscommonNavigator.navigate_to_devices()
        xiq.xflowscommonDevices.delete_device(device_mac=dut.mac)

        xiq.xflowsmanageLocation.delete_location_building_floor(*location.split(","))
        xiq.xflowsmanageLocation.create_location_building_floor(*location.split(","))
        time.sleep(1)
        xiq.xflowsconfigureSwitchTemplate.delete_stack_switch_template(nw_policy=network_policy,
                                                                       sw_template_name=template_stack)
        xiq.xflowsconfigureSwitchTemplate.delete_stack_units_device_template(nw_policy=network_policy,
                                                                             sw_template_name=template_stack)
        xiq.xflowsconfigureNetworkPolicy.delete_network_policy(network_policy)
        netelement_iqagent_disable(dev_cmd, dut.name)

        xiq.xflowscommonNavigator.navigate_to_devices()
        # Onboarding the exos stack device dut from testbed.yaml file using serial numbers
        onboarding_is_successful = xiq.xflowscommonDevices.onboard_device(device_serial=dut.stack.slot1.serial,
                                                                          device_make=dut.cli_type,
                                                                          entry_type="Manual",
                                                                          location=location) == 1

        assert onboarding_is_successful, f"Failed to onboard this dut to XiQ: {dut}"

        onboarding_is_successful = xiq.xflowscommonDevices.onboard_device(device_serial=dut.stack.slot2.serial,
                                                                          device_make=dut.cli_type,
                                                                          entry_type="Manual",
                                                                          location=location) == 1

        assert onboarding_is_successful, f"Failed to onboard this dut to XiQ: {dut}"

        netelement_iqagent_config(dev_cmd, dut, xiq_ip_address)
        check_stack_status_in_xiq(xiq, dut.mac)

        if ("Series Stack" in dut.model) and (dut.model_units is not None or dut.model_units != ""):
            xiq.Utils.print_info("Conftest with Stack: ", dut.model, " and units: ", dut.model_units)
        else:
            xiq.Utils.print_info("Try to update Stack Template Model and Units")
            dut_stack_model_update(dut, dut.stack)
            xiq.Utils.print_info("Conftest with Stack: ", dut.model_template, " and units: ", dut.model_units)
        create_np = xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(network_policy)
        assert create_np == 1, f"Policy {network_policy} wasn't created successfully "
        add_stack_template = xiq.xflowsconfigureSwitchTemplate.add_5520_sw_stack_template(dut.model_units,
                                                                                          network_policy,
                                                                                          dut.model_template,
                                                                                          template_stack)
        assert add_stack_template == 1, f"Stack template {template_stack} wasn't created successfully "

        assert xiq.xflowsmanageDevices.update_network_policy_to_stack(device_mac=dut.mac, policy_name=network_policy,
                                                                      template_policy_name=template_stack) == 1, \
            f"Couldn't assign policy {network_policy} to device {dut}"

        deactivate_xiq_libraries_and_logout(xiq)
        close_connection_with_error_handling(dut, network_manager)

        yield dut

    except Exception as e:
        if xiq:
            xiq.Utils.print_info("Exit with Exception: ", e)
            deactivate_xiq_libraries_and_logout(xiq)
        close_connection_with_error_handling(dut, network_manager)
    finally:
        close_connection_with_error_handling(dut, network_manager)

        if onboarding_is_successful:
            xiq = init_xiq_libraries_and_login(config['tenant_username'], config['tenant_password'], config['test_url'])
            try:
                delete_device(xiq, dut)
                xiq.xflowsconfigureSwitchTemplate.delete_stack_switch_template(nw_policy=network_policy,
                                                                               sw_template_name=template_stack)
                xiq.xflowsconfigureSwitchTemplate.delete_stack_units_device_template(nw_policy=network_policy,
                                                                                     sw_template_name=template_stack)
                xiq.xflowsconfigureNetworkPolicy.delete_network_policy(network_policy)
                xiq.xflowsmanageLocation.delete_location_building_floor(*location.split(","))
            finally:
                deactivate_xiq_libraries_and_logout(xiq)

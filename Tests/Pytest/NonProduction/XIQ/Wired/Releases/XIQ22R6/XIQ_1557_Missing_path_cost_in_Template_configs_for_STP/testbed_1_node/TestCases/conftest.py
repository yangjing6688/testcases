import pytest
import time
import os
import re
import string
import random

from extauto.common.Utils import Utils
from common.AutoActions import AutoActions
from extauto.xiq.flows.common.Navigator import Navigator
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


def cleanup(xiq, dut=None, onboarding_location='', network_policy='', template_switch=''):

    try:
        if dut:
            xiq.xflowscommonDevices._goto_devices()
            xiq.xflowscommonDevices.delete_device(device_serial=dut.serial)
        if onboarding_location:
            xiq.xflowsmanageLocation.delete_location_building_floor(*onboarding_location.split(","))
        if network_policy:
            xiq.xflowsconfigureNetworkPolicy.delete_network_policy(network_policy)
        if template_switch:
            xiq.xflowsconfigureCommonObjects.delete_switch_template(template_switch)
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


def generate_template_for_given_model(platform, model, slots=""):

    if platform.lower() == 'stack':
        if not slots:
            return -1

        model_list = []
        sw_model = ""
        model_units=None

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


def configure_iq_agent(dut, devCmd, config):
    if dut.cli_type.upper() == "EXOS":
        devCmd.send_cmd_verify_output(dut.name, 'show process iqagent', 'Ready', max_wait=30, interval=10)
        devCmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2,
                        confirmation_phrases='Do you want to continue?', confirmation_args='y')
        
        devCmd.send_cmd(dut.name, 'configure iqagent server ipaddress none', max_wait=10, interval=2)
        vr_name = get_virtual_router(devCmd, dut)
        if vr_name == -1:
            print("Error: Can't extract Virtual Router information")
            return -1
        devCmd.send_cmd(dut.name, f'configure iqagent server vr {vr_name}', max_wait=10, interval=2)
    
        devCmd.send_cmd(dut.name, 'configure iqagent server ipaddress ' + config['sw_connection_host'],
                        max_wait=10, interval=2)
        devCmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)
    elif dut.cli_type.upper() == "VOSS":
        devCmd.send_cmd(dut.name, 'enable', max_wait=10, interval=2)
        devCmd.send_cmd(dut.name, 'configure terminal', max_wait=10, interval=2)
        devCmd.send_cmd(dut.name, 'application', max_wait=10, interval=2)
        devCmd.send_cmd(dut.name, 'no iqagent enable', max_wait=10, interval=2)
        devCmd.send_cmd(dut.name, 'iqagent server ' + config['sw_connection_host'],
                        max_wait=10, interval=2)
        devCmd.send_cmd(dut.name, 'iqagent enable', max_wait=10, interval=2)
        devCmd.send_cmd_verify_output(dut.name, 'show application iqagent', 'true', max_wait=30,
                                        interval=10)
        devCmd.send_cmd(dut.name, 'exit', max_wait=10, interval=2)
    elif dut.cli_type.upper() == "AH-FASTPATH":
        try:
            devCmd.send_cmd(dut.name, "enable")
        except:
            devCmd.send_cmd(dut.name, "exit")
        devCmd.send_cmd(dut.name, f'hivemanager address {config["sw_connection_host"]}', max_wait=10, interval=2)
        devCmd.send_cmd(dut.name, 'application start hiveagent', max_wait=10, interval=2)
        devCmd.send_cmd(dut.name, "exit")
    time.sleep(10)


def _temporary_fix_assign_policy(xiq, policy_name, dut):

    import selenium
    devices = xiq.xflowscommonDevices
    utils = Utils()
    auto_actions = AutoActions()

    time.sleep(10)
    xiq.xflowscommonDevices._goto_devices()
    time.sleep(10)

    assert devices.select_device(device_mac=dut.mac)
    time.sleep(2)

    auto_actions.click(devices.devices_web_elements.get_manage_device_actions_button())
    time.sleep(3)

    utils.print_info("Click on Assign Network policy action for selected switch")
    auto_actions.click(devices.devices_web_elements.get_actions_assign_network_policy_combo_switch())
    time.sleep(4)

    utils.print_info("Click on network policy drop down")
    try:
        drop_down_button = devices.devices_web_elements.get_actions_assign_network_policy_drop_down()
        drop_down_button.click()
    except selenium.common.exceptions.ElementNotInteractableException as exc:
        utils.print_warning(repr(exc))
        [drop_down_button] = [btn for btn in devices.devices_web_elements.weh.get_elements(
            {"XPATH": '//tbody[@role="presentation"]'}) if btn.text == '--Select--']

        auto_actions.click(drop_down_button)
        time.sleep(5)

    network_policy_items = devices.devices_web_elements.get_actions_network_policy_drop_down_items()
    time.sleep(2)

    if auto_actions.select_drop_down_options(network_policy_items, policy_name):
        utils.print_info(f"Selected Network policy from drop down:{policy_name}")
    else:
        utils.print_info("Network policy is not present in drop down")

    time.sleep(5)

    utils.print_info("Click on network policy assign button")
    auto_actions.click(devices.devices_web_elements.get_actions_network_policy_assign_button())
    time.sleep(10)


def get_default_password(xiq):
    
    xiq.xflowscommonDevices._goto_devices()
    Navigator().navigate_to_global_settings_page()
    
    menu, _ = Utils().wait_till(
        func=xiq.xflowsglobalsettingsGlobalSetting.get_device_management_settings_menu,
        silent_failure=True,
        delay=4
    )
    assert menu, "Failed to get the device management settings menu"
    
    Utils().wait_till(func=lambda: AutoActions().click(menu) == 1)
    
    password, _ = Utils().wait_till(
        func=xiq.xflowsglobalsettingsGlobalSetting.get_device_management_settings_password,
        silent_failure=True,
        delay=4
    )
    assert password, "Failed to get the default device passowrd"
    return password.get_attribute('value')


@pytest.fixture(scope="package", autouse=True)
def network_policy():
    pool = list(string.ascii_letters) + list(string.digits)
    return f"np_{''.join(random.sample(pool, k=6))}"


@pytest.fixture(scope="package", autouse=True)
def template_switch():
    pool = list(string.ascii_letters) + list(string.digits)
    return f"template_{''.join(random.sample(pool, k=6))}"


@pytest.fixture(scope="package", autouse=True)
def onboarding_location():
    pool = list(string.ascii_letters) + list(string.digits)
    return f"Salem_{''.join(random.sample(pool, k=4))},Northeastern_{''.join(random.sample(pool, k=4))}," \
           f"Floor_{''.join(random.sample(pool, k=4))}"


def pytest_configure():
    pytest.default_device_password = ""


@pytest.fixture(scope="package", autouse=True)
def onboarded_switch(onboarding_location, template_switch, network_policy):

    tb = PytestConfigHelper(config)
    config['${TEST_NAME}'] = "onboarding"
    config['${OUTPUT DIR}'] = os.getcwd()
    for word in ["tenant_username", "tenant_password", "test_url"]:
        config[f"${{{word.upper()}}}"] = config[word]

    defaultLibrary = DefaultLibrary()
    devCmd = defaultLibrary.deviceNetworkElement.networkElementCliSend
    network_manager = NetworkElementConnectionManager()

    dut = tb.dut1

    if dut.get("platform", "").upper() == "STACK":
        pytest.skip("These test cases should run on standalone device.")

    xiq = init_xiq_libraries_and_login(config['tenant_username'], config['tenant_password'], config['test_url'])

    change_device_management_settings(xiq, option="disable", platform=dut.cli_type.upper())

    if dut.cli_type.upper() == "AH-FASTPATH":
        pytest.default_device_password = get_default_password(xiq)

    try:
        cleanup(xiq, dut=dut, network_policy=network_policy, template_switch=template_switch)
        delete_create_location_organization(xiq, location=onboarding_location)
    except Exception as exc:
        print(repr(exc))
        deactivate_xiq_libraries_and_logout(xiq)
        raise exc

    try:
        try:
            network_manager.connect_to_network_element_name(dut.name)
            configure_iq_agent(dut, devCmd, config)

            assert xiq.xflowsmanageSwitch.onboard_switch(
                dut.serial, device_os=dut.cli_type, location=onboarding_location) == 1, f"Failed to onboard this dut to XiQ: {dut}"

            xiq.xflowscommonDevices.wait_until_device_online(dut.serial)
            res = xiq.xflowscommonDevices.get_device_status(device_serial=dut.serial)
            assert res == 'green', f"The device did not come up successfully in the XIQ; Device: {dut}"

            create_np = xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(network_policy)
            assert create_np == 1, f"Policy {network_policy} wasn't created successfully "
            sw_model_template = generate_template_for_given_model(dut.platform, dut.model)
            xiq.xflowsconfigureSwitchTemplate.\
                add_sw_template(network_policy, sw_model_template, template_switch, dut.cli_type)
            # assert xiq.xflowsmanageDevices.\
                # assign_network_policy_to_switch(policy_name=network_policy, serial=dut.serial) == 1, \
                # f"Couldn't assign policy {network_policy} to device {dut}"
            _temporary_fix_assign_policy(xiq, network_policy, dut)
        finally:
            deactivate_xiq_libraries_and_logout(xiq)
        yield dut

    finally:

        xiq = init_xiq_libraries_and_login(config['tenant_username'], config['tenant_password'], config['test_url'])

        try:
            cleanup(xiq=xiq, dut=dut, network_policy=network_policy, template_switch=template_switch, onboarding_location=onboarding_location)
            close_connection_with_error_handling(dut, network_manager)
        except Exception as exc:
            print(repr(exc))
        finally:
            deactivate_xiq_libraries_and_logout(xiq)

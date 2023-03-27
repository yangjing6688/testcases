import time
import datetime
import re
import pytest

from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from extauto.common.AutoActions import AutoActions
from extauto.common.Screen import Screen
from extauto.xiq.elements.ClientWebElements import ClientWebElements
from extauto.xiq.elements.DeviceUpdate import DeviceUpdate
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import NetworkElementConnectionManager

# ----------------------------------------------------------------------------------------------------------
#   Setup/Teardown Keywords
# ---------------------------------------testcase_base.py-------------------------------------------------------------------

class SuiteUdk():

    def __init__(self):
        self.defaultLibrary = DefaultLibrary()
        self.tb = PytestConfigHelper(config)
        self.xiq = XiqLibrary()
        self.devCmd = self.defaultLibrary.deviceNetworkElement.networkElementCliSend

    def get_switch_model_name(self, dut):
        try:
            for attempts in range(3):
                time.sleep(5)
                self.devCmd.send_cmd(dut.name, 'disable cli paging',
                                     max_wait=10, interval=2)

                output = self.devCmd.send_cmd(dut.name,'show system',
                                                      max_wait=10,
                                                      interval=2)
                print(output[0].return_text)
                output_traffic = output[0].return_text

                p = re.compile(r'(System Type:\s+)+(.*-)', re.M)

                match_port = re.findall(p, output[0].return_text)
                print(f"{match_port}")

                sw_model = []
                sw_model.append(match_port[0][1])

                print(f"switch model is {match_port[0][1]} Switch Engine")

                return match_port[0][1]
        finally:
            time.sleep(3)

    def get_virtual_router(self, dut):
        global vrName

        result = self.devCmd.send_cmd(dut.name, 'show vlan', max_wait=10, interval=2)

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
                return -1;
        else:
            print("Pattern not found, unable to get virtual router info!")
            return -1;

    def configure_iqagent(self, dut, xiq_ip_address):
        self.devCmd.send_cmd(dut.name, f'configure iqagent server ipaddress {xiq_ip_address}', max_wait=10, interval=2)

        vrName = self.get_virtual_router(dut)
        self.devCmd.send_cmd(dut.name, f'configure iqagent server vr {vrName}', max_wait=10, interval=2)

        self.devCmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)
        self.devCmd.send_cmd_verify_output(dut.name, 'show process iqagent', 'Ready', max_wait=30, interval=10)

    def add_sw_template_adv_settings_tab_tcxm_20574(self, nw_policy, sw_model, sw_template_name):
        """
        - Checks the given switch template present already in the switch Templates Grid
        - If it is not there add to the sw_template
        - Keyword Usage
         - ``Add SW Template  ${NW_POLICY}  ${SW_MODEL}   ${SW_TEMPLATE_NAME}``

        :param nw_policy: network policy
        :param sw_model: Switch Model ie SR2348P
        :param sw_template_name: Switch Template Name ie template_SR2348P

        :return: 1 if Switch Template Configured Successfully else -1
        """
        print("Navigating Network Policies")

        self.xiq.xflowscommonNavigator.navigate_configure_network_policies()
        time.sleep(1)

        self.xiq.xflowsconfigureNetworkPolicy.select_network_policy_in_card_view(nw_policy)

        time.sleep(2)

        print("Click on Device Template tab button")
        AutoActions().click(self.xiq.xflowsconfigureDeviceTemplate.device_template_web_elements.get_add_device_template_menu())

        time.sleep(2)

        tab = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_tab_button()

        if tab.is_displayed():
            print("Click on Switch Templates tab")
            AutoActions().click(tab)
            time.sleep(2)

        if self.xiq.xflowsconfigureSwitchTemplate.check_sw_template(sw_model, ignore_failure=True):
            print("Template already present in the template grid")
            return 1

        add_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_add_button()

        time.sleep(2)

        print("add_btn: ", add_btns)
        for add_btn in add_btns:
            if add_btn.is_displayed():
                print("Click on sw Template Add button")

                AutoActions().click(add_btn)
                time.sleep(2)

                print("select the sw: ", sw_model)
                sw_list_items = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_platform_from_drop_down()

                time.sleep(2)
                for el in sw_list_items:
                    if not el:
                        continue
                    if el.text == "":
                        continue
                    print("Switch template names: ", el.text.upper())
                    print("Looking for: ", sw_model.upper())
                    if sw_model.upper() in el.text.upper():
                        print("    -switch template match")
                        print("the element was found in the list")
                        AutoActions().click(el)
                        break

                time.sleep(3)

                print("Go to the advanced settings tab")

                ok = 1
                if AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()) == -1:
                    print("Unable to click on Verify advanced settings button")
                    ok = 0
                else:
                    print("Click on Verify advanced settings button")

                assert ok == 1, "Unable to click on Verify advanced settings button"

                AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab())

                print("Verify advanced settings button")

                adv_btn = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()
                assert adv_btn.text in "Advanced Settings", print("The button is not present or has incorrect name")

                time.sleep(5)
                print("Get Template Field and enter the switch Template Name: ", sw_template_name)
                AutoActions().send_keys(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_tab_textfield(),sw_template_name)

                time.sleep(5)
                print("Get Template Save Button")
                save_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_save_button_adv_tab()

                rc = -1
                for save_btn in save_btns:
                    if save_btn.is_displayed():
                        print("Click on the save template button")
                        AutoActions().click(save_btn)
                        time.sleep(10)
                        break

                time.sleep(3)
                print("Click on network policy exit button")
                AutoActions().click(self.xiq.xflowsconfigureNetworkPolicy.np_web_elements.get_np_exit_button())
                time.sleep(2)

                return 1

    def add_sw_template_adv_settings_tab_tcxm_20576(self, nw_policy, sw_model, sw_template_name):
        """
        - Checks the given switch template present already in the switch Templates Grid
        - If it is not there add to the sw_template
        - Keyword Usage
         - ``Add SW Template  ${NW_POLICY}  ${SW_MODEL}   ${SW_TEMPLATE_NAME}``

        :param nw_policy: network policy
        :param sw_model: Switch Model ie SR2348P
        :param sw_template_name: Switch Template Name ie template_SR2348P

        :return: 1 if Switch Template Configured Successfully else -1
        """
        print("Navigating Network Policies")

        self.xiq.xflowscommonNavigator.navigate_configure_network_policies()
        time.sleep(1)

        self.xiq.xflowsconfigureNetworkPolicy.select_network_policy_in_card_view(nw_policy)

        time.sleep(2)

        print("Click on Device Template tab button")
        AutoActions().click(self.xiq.xflowsconfigureDeviceTemplate.device_template_web_elements.get_add_device_template_menu())

        time.sleep(2)

        tab = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_tab_button()

        if tab.is_displayed():
            print("Click on Switch Templates tab")
            AutoActions().click(tab)
            time.sleep(2)

        if self.xiq.xflowsconfigureSwitchTemplate.check_sw_template(sw_model, ignore_failure=True):
            print("Template already present in the template grid")
            return 1

        add_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_add_button()

        time.sleep(2)

        print("add_btn: ", add_btns)
        for add_btn in add_btns:
            if add_btn.is_displayed():
                print("Click on sw Template Add button")

                AutoActions().click(add_btn)
                time.sleep(2)

                print("select the sw: ", sw_model)
                sw_list_items = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_platform_from_drop_down()

                time.sleep(2)
                for el in sw_list_items:
                    if not el:
                        continue
                    if el.text == "":
                        continue
                    print("Switch template names: ", el.text.upper())
                    print("Looking for: ", sw_model.upper())
                    if sw_model.upper() in el.text.upper():
                        print("    -switch template match")
                        print("the element was found in the list")
                        AutoActions().click(el)
                        break

                time.sleep(3)

                print(" Go to the advanced settings tab ")

                ok = 1
                if AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()) == -1:
                    print("Unable to click on Verify advanced settings button")
                    ok = 0
                else:
                    print("Click on Verify advanced settings button")

                assert ok == 1, "Unable to click on Verify advanced settings button"

                AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab())

                print(" Verify advanced settings button ")

                adv_btn = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()

                assert adv_btn.text in "Advanced Settings", print("The button is not present or has incorrect name")

                time.sleep(5)
                print("Get Template Field and enter the switch Template Name: ", sw_template_name)
                AutoActions().send_keys(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_tab_textfield(),sw_template_name)

                print("Verify if the Upgrade device firmware upon device authentication button is off by default")

                assert self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button().is_selected() == 0, print("the button is not off by default")

                if self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button() == -1:
                    print("Unable to click on Upgrade device firmware upon device authentication button ")
                    return -1
                else:
                    print("Click on Upgrade device firmware upon device authentication button")
                    AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button())

                AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button())

                time.sleep(3)
                print("Get Template Save Button")
                save_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_save_button_adv_tab()

                rc = -1
                for save_btn in save_btns:
                    if save_btn.is_displayed():
                        print("Click on the save template button")
                        AutoActions().click(save_btn)
                        time.sleep(10)
                        break

                time.sleep(3)
                print("Click on network policy exit button")
                AutoActions().click(self.xiq.xflowsconfigureNetworkPolicy.np_web_elements.get_np_exit_button())

                time.sleep(2)

                return 1

    def add_sw_template_adv_settings_tab_tcxm_20579(self, nw_policy, sw_model, sw_template_name):
        """
        - Checks if the given switch template is already present in the Switch Templates grid
        - If it is not there, add it to the Switch Templates
        - Keyword Usage
         - ``Add SW Template  ${NW_POLICY}  ${SW_MODEL}   ${SW_TEMPLATE_NAME}``

        :param nw_policy: network policy
        :param sw_model: Switch Model ie SR2348P
        :param sw_template_name: Switch Template Name ie template_SR2348P

        :return: 1 if Switch Template Configured Successfully else -1
        """
        print("Navigating Network Policies")

        self.xiq.xflowscommonNavigator.navigate_configure_network_policies()
        time.sleep(1)

        self.xiq.xflowsconfigureNetworkPolicy.select_network_policy_in_card_view(nw_policy)

        time.sleep(2)

        print("Click on Device Template tab button")
        AutoActions().click(self.xiq.xflowsconfigureDeviceTemplate.device_template_web_elements.get_add_device_template_menu())

        time.sleep(2)

        tab = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_tab_button()

        if tab.is_displayed():
            print("Click on Switch Templates tab")
            AutoActions().click(tab)
            time.sleep(2)

        if self.xiq.xflowsconfigureSwitchTemplate.check_sw_template(sw_model, ignore_failure=True):
            print("Template already present in the Switch Templates grid")
            return 1

        add_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_add_button()

        time.sleep(2)

        print("add_btn: ", add_btns)
        for add_btn in add_btns:
            if add_btn.is_displayed():
                print("Click on Switch Templates Add button")

                AutoActions().click(add_btn)
                time.sleep(2)

                print("select the sw: ", sw_model)
                sw_list_items = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_platform_from_drop_down()

                time.sleep(2)
                for el in sw_list_items:
                    if not el:
                        continue
                    if el.text == "":
                        continue
                    print("Switch template names: ", el.text.upper())
                    print("Looking for: ", sw_model.upper())
                    if sw_model.upper() in el.text.upper():
                        print("    -switch template match")
                        print("the element was found in the list")
                        AutoActions().click(el)
                        break

                time.sleep(3)

                print("Go to Advanced Settings tab")

                ok = 1
                if AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()) == -1:
                    print("Unable to click on Verify advanced settings button")
                    ok = 0
                else:
                    print("Clicked on Verify advanced settings button")

                assert ok == 1, "Unable to click on Verify advanced settings button"

                print("Verify advanced settings button")
                adv_btn = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()
                assert adv_btn.text in "Advanced Settings", print("The button is not present or has incorrect name")

                time.sleep(5)
                print("Get Template Field and enter the switch Template Name: ", sw_template_name)
                AutoActions().send_keys(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_tab_textfield(), sw_template_name)

                print("Verify if Upload configuration automatically button is off by default")
                assert self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upload_configuration_on_off_button().is_selected() == 0, print(
                    "the button is not off by default")

                print("Click on Upload configuration automatically button")
                AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upload_configuration_on_off_button())

                time.sleep(3)
                print("Get Template Save Button")
                save_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_save_button_adv_tab()

                rc = -1
                for save_btn in save_btns:
                    if save_btn.is_displayed():
                        print("Click on the save template button")
                        AutoActions().click(save_btn)
                        time.sleep(10)
                        break

                time.sleep(3)

                print("Click on network policy exit button")
                AutoActions().click(self.xiq.xflowsconfigureNetworkPolicy.np_web_elements.get_np_exit_button())
                time.sleep(2)

                return 1

    def add_sw_template_adv_settings_tab_tcxm_20580(self, nw_policy, sw_model, sw_template_name):
        """
        - Checks the given switch template present already in the switch Templates Grid
        - If it is not there add to the sw_template
        - Keyword Usage
         - ``Add SW Template  ${NW_POLICY}  ${SW_MODEL}   ${SW_TEMPLATE_NAME}``

        :param nw_policy: network policy
        :param sw_model: Switch Model ie SR2348P
        :param sw_template_name: Switch Template Name ie template_SR2348P

        :return: 1 if Switch Template Configured Successfully else -1
        """
        print("Navigating Network Policies")

        self.xiq.xflowscommonNavigator.navigate_configure_network_policies()
        time.sleep(1)

        self.xiq.xflowsconfigureNetworkPolicy.select_network_policy_in_card_view(nw_policy)

        time.sleep(2)

        print("Click on Device Template tab button")
        AutoActions().click(self.xiq.xflowsconfigureDeviceTemplate.device_template_web_elements.get_add_device_template_menu())

        time.sleep(2)

        tab = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_tab_button()

        if tab.is_displayed():
            print("Click on Switch Templates tab")
            AutoActions().click(tab)
            time.sleep(2)

        if self.xiq.xflowsconfigureSwitchTemplate.check_sw_template(sw_model, ignore_failure=True):
            print("Template Already present in the template grid")
            return 1

        add_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_add_button()

        time.sleep(2)

        print("add_btn: ", add_btns)
        for add_btn in add_btns:
            if add_btn.is_displayed():
                print("Click on sw Template Add button")

                AutoActions().click(add_btn)
                time.sleep(2)

                print("select the sw: ", sw_model)
                sw_list_items = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_platform_from_drop_down()

                time.sleep(2)
                for el in sw_list_items:
                    if not el:
                        continue
                    if el.text == "":
                        continue
                    print("Switch template names: ", el.text.upper())
                    print("Looking for: ", sw_model.upper())
                    if sw_model.upper() in el.text.upper():
                        print("    -switch template match")
                        print("the element was found in the list")
                        AutoActions().click(el)
                        break

                time.sleep(3)

                print(" Go to the advanced settings tab ")

                ok = 1
                if AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()) == -1:
                    print("Unable to click on Verify advanced settings button")
                    ok = 0
                else:
                    print("Click on Verify advanced settings button")

                assert ok == 1, "Unable to click on Verify advanced settings button"

                AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab())

                print(" Verify advanced settings button ")

                adv_btn = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()

                assert adv_btn.text in "Advanced Settings", print("The button is not present or has incorrect name")

                time.sleep(5)
                print("Get Template Field and enter the switch Template Name: ", sw_template_name)
                AutoActions().send_keys(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_tab_textfield(),sw_template_name)

                print("Verify if the Upgrade device firmware upon device authentication button is off by default")

                assert self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button().is_selected() == 0, print("the button is not off by default")

                if self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button() == -1:
                    print("Unable to click on Upgrade device firmware upon device authentication button ")
                    return -1
                else:
                    print("Click on Upgrade device firmware upon device authentication button")
                    AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button())

                AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button())

                time.sleep(3)
                print("Get Template Save Button")
                save_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_save_button_adv_tab()

                rc = -1
                for save_btn in save_btns:
                    if save_btn.is_displayed():
                        print("Click on the save template button")
                        AutoActions().click(save_btn)
                        time.sleep(10)
                        break

                time.sleep(3)
                print("Click on network policy exit button")
                AutoActions().click(self.xiq.xflowsconfigureNetworkPolicy.np_web_elements.get_np_exit_button())

                time.sleep(2)

                return 1

    def add_sw_template_adv_settings_tab_tcxm_20582(self, nw_policy, sw_model, sw_template_name):
        """
        - Checks the given switch template present already in the switch Templates Grid
        - If it is not there add to the sw_template
        - Keyword Usage
         - ``Add SW Template  ${NW_POLICY}  ${SW_MODEL}   ${SW_TEMPLATE_NAME}``

        :param nw_policy: network policy
        :param sw_model: Switch Model ie SR2348P
        :param sw_template_name: Switch Template Name ie template_SR2348P

        :return: 1 if Switch Template Configured Successfully else -1
        """
        print("Navigating Network Policies")

        self.xiq.xflowscommonNavigator.navigate_configure_network_policies()
        time.sleep(1)

        self.xiq.xflowsconfigureNetworkPolicy.select_network_policy_in_card_view(nw_policy)

        time.sleep(2)

        print("Click on Device Template tab button")
        AutoActions().click(self.xiq.xflowsconfigureDeviceTemplate.device_template_web_elements.get_add_device_template_menu())

        time.sleep(2)

        tab = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_tab_button()

        if tab.is_displayed():
            print("Click on Switch Templates tab")
            AutoActions().click(tab)
            time.sleep(2)

        if self.xiq.xflowsconfigureSwitchTemplate.check_sw_template(sw_model, ignore_failure=True):
            print("Template already present in the template grid")
            return 1

        add_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_add_button()

        time.sleep(2)

        print("add_btn: ", add_btns)
        for add_btn in add_btns:
            if add_btn.is_displayed():
                print("Click on sw Template Add button")

                AutoActions().click(add_btn)
                time.sleep(2)

                print("select the sw: ", sw_model)
                sw_list_items = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_platform_from_drop_down()

                time.sleep(2)
                for el in sw_list_items:
                    if not el:
                        continue
                    if el.text == "":
                        continue
                    print("Switch template names: ", el.text.upper())
                    print("Looking for: ", sw_model.upper())
                    if sw_model.upper() in el.text.upper():
                        print("    -switch template match")
                        print("the element was found in the list")
                        AutoActions().click(el)
                        break

                time.sleep(3)

                print(" Go to the advanced settings tab ")

                ok = 1
                if AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()) == -1:
                    print("Unable to click on Verify advanced settings button")
                    ok = 0
                else:
                    print("Click on Verify advanced settings button")

                assert ok == 1, "Unable to click on Verify advanced settings button"

                AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab())

                print(" Verify advanced settings button ")

                adv_btn = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()

                assert adv_btn.text in "Advanced Settings", print("The button is not present or has incorrect name")

                time.sleep(5)
                print("Get Template Field and enter the switch Template Name: ", sw_template_name)
                AutoActions().send_keys(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_tab_textfield(),sw_template_name)

                print("Verify if the Upgrade device firmware upon device authentication button is off by default")
                assert self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button().is_selected() == 0, print("the button is not off by default")

                if self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button() == -1:
                    print("Unable to click on Upgrade device firmware upon device authentication button ")
                    return -1
                else:
                    print("Click on Upgrade device firmware upon device authentication button (and default on Upgrade firmware to the latest version)")
                    AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button())
                time.sleep(2)

                print("Verify if the Upload configuration automatically button is off by default")
                assert self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upload_configuration_on_off_button().is_selected() == 0, print(
                    "the button is not off by default")

                if self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upload_configuration_on_off_button() == -1:
                    print("Unable to click on Upload configuration automatically button button")
                    return -1
                else:
                    print("Click on Upload configuration automatically button button")
                    AutoActions().click(
                        self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upload_configuration_on_off_button())

                time.sleep(3)
                print("Get Template Save Button")
                save_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_save_button_adv_tab()

                rc = -1
                for save_btn in save_btns:
                    if  save_btn.is_displayed():
                        print("Click on the save template button")
                        AutoActions().click(save_btn)
                        time.sleep(10)

                        break;
                time.sleep(3)
                print("Click on network policy exit button")
                AutoActions().click(self.xiq.xflowsconfigureNetworkPolicy.np_web_elements.get_np_exit_button())

                time.sleep(2)

                return 1

    def add_upgrade_firmware_latest_version_sw_template_adv_settings_tab(self, nw_policy, sw_model, sw_template_name):
        """
        - Checks the given switch template present already in the switch Templates Grid
        - If it is not there add to the sw_template with option "Upgrade device firmware upon device authentication"
        on and option "Upgrade firmware to the latest version" selected and also check there presence in page.
        - Keyword Usage
         - ``Add SW Template  ${NW_POLICY}  ${SW_MODEL}   ${SW_TEMPLATE_NAME}``

        :param nw_policy: network policy
        :param sw_model: Switch Model ie SR2348P
        :param sw_template_name: Switch Template Name ie template_SR2348P

        :return: 1 if Switch Template Configured Successfully else -1
        """
        print("Navigating Network Policies")

        self.xiq.xflowscommonNavigator.navigate_configure_network_policies()
        time.sleep(1)

        self.xiq.xflowsconfigureNetworkPolicy.select_network_policy_in_card_view(nw_policy)

        time.sleep(2)

        print("Click on Device Template tab button")
        AutoActions().click(self.xiq.xflowsconfigureDeviceTemplate.device_template_web_elements.get_add_device_template_menu())

        time.sleep(2)

        tab = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_tab_button()

        if tab.is_displayed():
            print("Click on Switch Templates tab")
            AutoActions().click(tab)
            time.sleep(2)

        if self.xiq.xflowsconfigureSwitchTemplate.check_sw_template(sw_model, ignore_failure=True):
            print("Template Already present in the template grid")
            return 1

        add_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_add_button()

        time.sleep(2)

        print("add_btn: ", add_btns)
        for add_btn in add_btns:
            if add_btn.is_displayed():
                print("Click on sw Template Add button")

                AutoActions().click(add_btn)
                time.sleep(2)

                print("select the sw: ", sw_model)
                sw_list_items = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_platform_from_drop_down()

                time.sleep(2)
                for el in sw_list_items:
                    if not el:
                        continue
                    if el.text == "":
                        continue
                    print("Switch template names: ", el.text.upper())
                    print("Looking for: ", sw_model.upper())
                    if sw_model.upper() in el.text.upper():
                        print("    -switch template match")
                        print("the element was found in the list")
                        AutoActions().click(el)
                        break

                time.sleep(3)

                print(" Go to the advanced settings tab ")

                ok = 1
                if AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()) == -1:
                    print("Unable to click on Verify advanced settings button")
                    ok = 0
                else:
                    print("Click on Verify advanced settings button")

                assert ok == 1, "Unable to click on Verify advanced settings button"

                AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab())

                print(" Verify advanced settings button ")

                adv_btn = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()

                assert adv_btn.text in "Advanced Settings", print("The button is not present or has incorrect name")

                time.sleep(5)
                print("Get Template Field and enter the switch Template Name: ", sw_template_name)
                AutoActions().send_keys(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_tab_textfield(),sw_template_name)

                print("Verify if the Upgrade device firmware upon device authentication button is off by default")
                assert self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button().is_selected() == 0, print(
                    "the button is not off by default")

                if self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button() == -1:
                    print("Unable to click on Upgrade device firmware upon device authentication button ")
                    return -1
                else:
                    print("Click on Upgrade device firmware upon device authentication button")
                    AutoActions().click(
                        self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button())

                if self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgr_firm_latest_button() == -1:
                    print("Unable to click on Upgrade firmware to the latest version button ")
                    return -1
                else:
                    print("Click on Upgrade firmware to the latest version button")
                    AutoActions().click(
                        self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgr_firm_latest_button())

                time.sleep(5)
                print("Get Template Save Button")
                save_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_save_button_adv_tab()

                rc = -1
                for save_btn in save_btns:
                    if  save_btn.is_displayed():
                        print("Click on the save template button")
                        AutoActions().click(save_btn)
                        time.sleep(10)
                        break;

                time.sleep(3)
                print("Click on network policy exit button")
                AutoActions().click(self.xiq.xflowsconfigureNetworkPolicy.np_web_elements.get_np_exit_button())

                time.sleep(2)

                return 1

    def add_upgrade_firmware_specific_version_sw_template_adv_settings_tab(self, nw_policy, sw_model, sw_template_name, image_version):
        """
        - Checks the given switch template present already in the switch Templates Grid
        - If it is not there add to the sw_template
        - Keyword Usage
         - ``Add SW Template  ${NW_POLICY}  ${SW_MODEL}   ${SW_TEMPLATE_NAME}``

        :param nw_policy: network policy
        :param sw_model: Switch Model ie SR2348P
        :param sw_template_name: Switch Template Name ie template_SR2348P

        :return: 1 if Switch Template Configured Successfully else -1
        """
        print("Navigating Network Policies")

        self.xiq.xflowscommonNavigator.navigate_configure_network_policies()
        time.sleep(1)

        self.xiq.xflowsconfigureNetworkPolicy.select_network_policy_in_card_view(nw_policy)

        time.sleep(2)

        print("Click on Device Template tab button")
        AutoActions().click(self.xiq.xflowsconfigureDeviceTemplate.device_template_web_elements.get_add_device_template_menu())

        time.sleep(2)

        tab = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_tab_button()

        if tab.is_displayed():
            print("Click on Switch Templates tab")
            AutoActions().click(tab)
            time.sleep(2)

        if self.xiq.xflowsconfigureSwitchTemplate.check_sw_template(sw_model, ignore_failure=True):
            print("Template Already present in the template grid")
            return 1

        add_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_add_button()

        time.sleep(2)

        print("add_btn: ", add_btns)
        for add_btn in add_btns:
            if add_btn.is_displayed():
                print("Click on sw Template Add button")

                AutoActions().click(add_btn)
                time.sleep(2)

                print("select the sw: ", sw_model)
                sw_list_items = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_platform_from_drop_down()

                time.sleep(2)
                for el in sw_list_items:
                    if not el:
                        continue
                    if el.text == "":
                        continue
                    print("Switch template names: ", el.text.upper())
                    print("Looking for: ", sw_model.upper())
                    if sw_model.upper() in el.text.upper():
                        print("    -switch template match")
                        print("the element was found in the list")
                        AutoActions().click(el)
                        break

                time.sleep(3)

                print(" Go to the advanced settings tab ")

                ok = 1
                if AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()) == -1:
                    print("Unable to click on Verify advanced settings button")
                    ok = 0
                else:
                    print("Click on Verify advanced settings button")

                assert ok == 1, "Unable to click on Verify advanced settings button"

                AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab())

                print(" Verify advanced settings button ")

                adv_btn = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()

                assert adv_btn.text in "Advanced Settings", print("The button is not present or has incorrect name")

                time.sleep(5)
                print("Get Template Field and enter the switch Template Name: ", sw_template_name)
                AutoActions().send_keys(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_tab_textfield(),sw_template_name)

                print("Verify if the Upgrade device firmware upon device authentication button is off by default")

                assert self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button().is_selected() == 0, print("the button is not off by default")

                if self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button() == -1:
                    print("Unable to click on Upgrade device firmware upon device authentication button ")
                    return -1
                else:
                    print("Click on Upgrade device firmware upon device authentication button")
                    AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button())

                if self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgr_firm_specific_button() == -1:
                    print("Unable to click on Upgrade firmware to the specific version button ")
                    return -1
                else:
                    print("Click on Upgrade firmware to the specific version button")
                    AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgr_firm_specific_button())

                if not self.select_specific_firmware_version_by_image(sw_model, image_version):
                    print("Selection of a specific firmware image failed")
                    return -1

                time.sleep(3)
                print("Get Template Save Button")
                save_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_save_button_adv_tab()

                rc = -1
                for save_btn in save_btns:
                    if save_btn.is_displayed():
                        print("Click on the save template button")
                        AutoActions().click(save_btn)
                        time.sleep(10)
                        break

                time.sleep(3)
                print("Click on network policy exit button")
                AutoActions().click(self.xiq.xflowsconfigureNetworkPolicy.np_web_elements.get_np_exit_button())

                time.sleep(2)

                return 1

    def add_upgrade_firmware_specific_version_and_upload_config_auto_sw_template_adv_settings_tab(self, nw_policy, sw_model, sw_template_name, image_version, test_name):
        """
        - Checks the given switch template present already in the switch Templates Grid
        - If it is not there add to the sw_template
        - Keyword Usage
         - ``Add SW Template  ${NW_POLICY}  ${SW_MODEL}   ${SW_TEMPLATE_NAME}``

        :param nw_policy: network policy
        :param sw_model: Switch Model ie SR2348P
        :param sw_template_name: Switch Template Name ie template_SR2348P

        :return: 1 if Switch Template Configured Successfully else -1
        """
        print("Navigating Network Policies")

        self.xiq.xflowscommonNavigator.navigate_configure_network_policies()
        time.sleep(1)

        self.xiq.xflowsconfigureNetworkPolicy.select_network_policy_in_card_view(nw_policy)

        time.sleep(2)

        print("Click on Device Template tab button")
        AutoActions().click(self.xiq.xflowsconfigureDeviceTemplate.device_template_web_elements.get_add_device_template_menu())

        time.sleep(2)

        tab = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_tab_button()

        if tab.is_displayed():
            print("Click on Switch Templates tab")
            AutoActions().click(tab)
            time.sleep(2)

        if self.xiq.xflowsconfigureSwitchTemplate.check_sw_template(sw_model, ignore_failure=True):
            print("Template Already present in the template grid")
            return 1

        add_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_add_button()

        time.sleep(2)

        print("add_btn: ", add_btns)
        for add_btn in add_btns:
            if add_btn.is_displayed():
                print("Click on sw Template Add button")

                AutoActions().click(add_btn)
                time.sleep(2)

                print("select the sw: ", sw_model)
                sw_list_items = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_platform_from_drop_down()

                time.sleep(2)
                for el in sw_list_items:
                    if not el:
                        continue
                    if el.text == "":
                        continue
                    print("Switch template names: ", el.text.upper())
                    print("Looking for: ", sw_model.upper())
                    if sw_model.upper() in el.text.upper():
                        print("    -switch template match")
                        print("the element was found in the list")
                        AutoActions().click(el)
                        break

                time.sleep(3)

                print(" Go to the advanced settings tab ")

                ok = 1
                if AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()) == -1:
                    print("Unable to click on Verify advanced settings button")
                    ok = 0
                else:
                    print("Click on Verify advanced settings button")

                assert ok == 1, "Unable to click on Verify advanced settings button"

                AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab())

                print(" Verify advanced settings button ")

                adv_btn = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()

                assert adv_btn.text in "Advanced Settings", print("The button is not present or has incorrect name")

                time.sleep(5)
                print("Get Template Field and enter the switch Template Name: ", sw_template_name)
                AutoActions().send_keys(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_tab_textfield(),sw_template_name)

                print("Verify if the Upload Configuration button is off by default")
                assert self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upload_configuration_on_off_button().is_selected() == 0, print("the button is not off by default")

                if self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upload_configuration_on_off_button() == -1:
                    print("Unable to click on Upload configuration automatically button ")
                    return -1
                else:
                    print("Click on Upload configuration automatically button")
                    AutoActions().click(
                        self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upload_configuration_on_off_button())

                print("Verify if the Upgrade device firmware upon device authentication button is off by default")
                assert self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button().is_selected() == 0, print("the button is not off by default")

                if self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button() == -1:
                    print("Unable to click on Upgrade device firmware upon device authentication button ")
                    return -1
                else:
                    print("Click on Upgrade device firmware upon device authentication button")
                    AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button())

                if self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgr_firm_specific_button() == -1:
                    print("Unable to click on Upgrade firmware to the specific version button ")
                    return -1
                else:
                    print("Click on Upgrade firmware to the specific version button")
                    AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgr_firm_specific_button())

                if test_name == "test_tcxm_20583":
                    if not self.select_specific_firmware_version_tcxm_20583(sw_model, image_version):
                        print("Selection of a specific firmware image failed")
                        return -1
                else:
                    if not self.select_specific_firmware_version_by_image(sw_model, image_version):
                        print("Selection of a specific firmware image failed")
                        return -1

                time.sleep(3)
                print("Get Template Save Button")
                save_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_save_button_adv_tab()

                rc = -1
                for save_btn in save_btns:
                    if save_btn.is_displayed():
                        print("Click on the save template button")
                        AutoActions().click(save_btn)
                        time.sleep(10)
                        break

                time.sleep(3)
                print("Click on network policy exit button")
                AutoActions().click(self.xiq.xflowsconfigureNetworkPolicy.np_web_elements.get_np_exit_button())

                time.sleep(2)

                return 1

    def add_upgrade_firmware_latest_version_and_upload_config_auto_sw_template_adv_settings_tab(self, nw_policy, sw_model, sw_template_name):
        """
        - Checks the given switch template present already in the switch Templates Grid
        - If it is not there add to the sw_template
        - Keyword Usage
         - ``Add SW Template  ${NW_POLICY}  ${SW_MODEL}   ${SW_TEMPLATE_NAME}``

        :param nw_policy: network policy
        :param sw_model: Switch Model ie SR2348P
        :param sw_template_name: Switch Template Name ie template_SR2348P

        :return: 1 if Switch Template Configured Successfully else -1
        """
        print("Navigating Network Policies")

        self.xiq.xflowscommonNavigator.navigate_configure_network_policies()
        time.sleep(1)

        self.xiq.xflowsconfigureNetworkPolicy.select_network_policy_in_card_view(nw_policy)

        time.sleep(2)

        print("Click on Device Template tab button")
        AutoActions().click(self.xiq.xflowsconfigureDeviceTemplate.device_template_web_elements.get_add_device_template_menu())

        time.sleep(2)

        tab = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_tab_button()

        if tab.is_displayed():
            print("Click on Switch Templates tab")
            AutoActions().click(tab)
            time.sleep(2)

        if self.xiq.xflowsconfigureSwitchTemplate.check_sw_template(sw_model, ignore_failure=True):
            print("Template Already present in the template grid")
            return 1

        add_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_add_button()

        time.sleep(2)

        print("add_btn: ", add_btns)
        for add_btn in add_btns:
            if add_btn.is_displayed():
                print("Click on sw Template Add button")

                AutoActions().click(add_btn)
                time.sleep(2)

                print("select the sw: ", sw_model)
                sw_list_items = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_platform_from_drop_down()

                time.sleep(2)
                for el in sw_list_items:
                    if not el:
                        continue
                    if el.text == "":
                        continue
                    print("Switch template names: ", el.text.upper())
                    print("Looking for: ", sw_model.upper())
                    if sw_model.upper() in el.text.upper():
                        print("    -switch template match")
                        print("the element was found in the list")
                        AutoActions().click(el)
                        break

                time.sleep(3)

                print(" Go to the advanced settings tab ")

                ok = 1
                if AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()) == -1:
                    print("Unable to click on Verify advanced settings button")
                    ok = 0
                else:
                    print("Click on Verify advanced settings button")

                assert ok == 1, "Unable to click on Verify advanced settings button"

                AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab())

                print(" Verify advanced settings button ")

                adv_btn = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()

                assert adv_btn.text in "Advanced Settings", print("The button is not present or has incorrect name")

                time.sleep(5)
                print("Get Template Field and enter the switch Template Name: ", sw_template_name)
                AutoActions().send_keys(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_tab_textfield(),sw_template_name)

                print("Verify if the Upload Configuration button is off by default")
                assert self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upload_configuration_on_off_button().is_selected() == 0, print("the button is not off by default")

                if self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upload_configuration_on_off_button() == -1:
                    print("Unable to click on Upload configuration automatically button ")
                    return -1
                else:
                    print("Click on Upload configuration automatically button")
                    AutoActions().click(
                        self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upload_configuration_on_off_button())

                print("Verify if the Upgrade device firmware upon device authentication button is off by default")
                assert self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button().is_selected() == 0, print("the button is not off by default")

                if self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button() == -1:
                    print("Unable to click on Upgrade device firmware upon device authentication button ")
                    return -1
                else:
                    print("Click on Upgrade device firmware upon device authentication button")
                    AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button())

                if self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgr_firm_latest_button() == -1:
                    print("Unable to click on Upgrade firmware to the latest version button ")
                    return -1
                else:
                    print("Click on Upgrade firmware to the latest version button")
                    AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgr_firm_latest_button())

                time.sleep(3)
                print("Get Template Save Button")
                save_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_save_button_adv_tab()

                rc = -1
                for save_btn in save_btns:
                    if save_btn.is_displayed():
                        print("Click on the save template button")
                        AutoActions().click(save_btn)
                        time.sleep(10)
                        break

                time.sleep(3)
                print("Click on network policy exit button")
                AutoActions().click(self.xiq.xflowsconfigureNetworkPolicy.np_web_elements.get_np_exit_button())

                time.sleep(2)

                return 1

    def delete_created_and_registered_switch_template(self, nw_policy, sw_template_name):
        """
        This function is used to delete a registered template from switch template list
       :param nw_policy:
       :param sw_template_name:
       :return: 1 if template was deleted or template doesn't exist; else -1
        """

        print("Navigating to Network Policies")
        self.xiq.xflowscommonNavigator.navigate_configure_network_policies()
        time.sleep(1)

        self.xiq.xflowsconfigureNetworkPolicy.select_network_policy_in_card_view(nw_policy)
        time.sleep(2)

        print("Click on Device Templates tab button")
        AutoActions().click(self.xiq.xflowsconfigureDeviceTemplate.device_template_web_elements.get_add_device_template_menu())
        time.sleep(2)

        tab = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_tab_button()
        if tab.is_displayed():
            print("Click on Switch Templates tab")
            AutoActions().click(tab)
            time.sleep(2)

        print("Click on Switch Templates select button")
        sel_btn = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_select_button()
        time.sleep(2)

        if sel_btn:
            AutoActions().click(sel_btn)
            time.sleep(2)
        else:
            print("Could not click Switch Template Select button")
            return -1

        print("Search for the switch template name: ", sw_template_name)
        AutoActions().send_keys(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_selection_search_textfield(),sw_template_name)
        AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_selection_search_button())
        time.sleep(3)

        print("Select all rows which contains sw_template_name")
        select_all_rows = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_select_all_rows()
        time.sleep(2)

        if select_all_rows:
            AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_select_all_rows())
            time.sleep(3)
        else:
            print("Could not select all rows")
            return -1

        print("Click on Delete button")
        del_btn = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_select_delete_button()
        time.sleep(2)

        if del_btn:
            AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_select_delete_button())
        else:
            print("Delete button was not found")
            return -1

        print("Click on Confirmation button")
        confirmation_btn = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_confirm_message_yes_button()
        time.sleep(2)

        if confirmation_btn:
            AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_confirm_message_yes_button())
        else:
            print("Confirmation button was not found")
            return -1

        AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_selection_close_button())
        return 1

    def get_latest_version_from_device_update(self, device_serial):
        """
        - This method update device(s) to latest version from the dropdown
        - Keyword Usage:
         - ``Upgrade Device To Latest Version   ${DEVICE_SERIAL}``

        :param device_serial: serial number(s) of the device(s)
        :return: 1 if success else -1
        """
        latest_version = -1
        time.sleep(5)
        if self.xiq.xflowscommonDevices.select_device(device_serial):
            def _click_update_devices_button():
                return AutoActions().click(DeviceUpdate().get_update_devices_button())
            self.xiq.Utils.wait_till(_click_update_devices_button, timeout=30, delay=20, msg="Selecting Update Devices button")

            Screen().save_screen_shot()

            # Check if the Upgrade IQ Engine and Extreme Network Switch Images checkbox is already checked
            checkbox_status = DeviceUpdate().get_upgrade_IQ_engine_and_extreme_network_switch_images_checkbox_status()

            if checkbox_status == "true":  # If checkbox is selected we get string "true" otherwise we get None
                print("Upgrade IQ Engine and Extreme Network Switch Images checkbox is already checked")
            else:
                def _click_upgrade_iq_engine_button():
                    return AutoActions().click(DeviceUpdate().get_upgrade_iq_engine_checkbox())

                self.xiq.Utils.wait_till(_click_upgrade_iq_engine_button, timeout=30, delay=20,
                                         msg="Selecting upgrade IQ Engine checkbox")
            Screen().save_screen_shot()

            print("Selecting upgrade to latest version checkbox")
            AutoActions().click(DeviceUpdate().get_upgrade_to_latest_version_radio())
            time.sleep(2)
            Screen().save_screen_shot()

            latest_version = DeviceUpdate().get_latest_version()

            print("Device Latest Version: ", latest_version)
            time.sleep(5)

            print("Selecting Close button...")
            AutoActions().click(ClientWebElements().get_client_dialog_window_close_button())
            time.sleep(5)

        return latest_version

    def check_update_column(self, device_serial, status_before):
        # Checking for the update column to reflect the firmware update status
        print(f"Status before: {status_before}")
        status_after = self.xiq.xflowscommonDevices.get_device_updated_status(device_serial=device_serial)
        count = 0
        max_wait = 900
        current_date = datetime.datetime.now()
        update_text = str(current_date).split()[0]

        while update_text not in status_after:
            time.sleep(10)
            count += 10
            status_after = self.xiq.xflowscommonDevices.get_device_updated_status(device_serial=device_serial)
            print(
                f"\nINFO \t Time elapsed in the update column to reflect the firmware updating is '{count} seconds'\n")
            if ("Failed" in status_after) or ("failed" in status_after) or (count > max_wait):
                pytest.fail("Device Update Failed for the device with serial {}".format(device_serial))

        print(f"Status after: {status_after}")
        if status_before != status_after:
            print("Column UPDATED has successfully changed")
        else:
            pytest.fail("Column UPDATED or column OS VERSION has not successfully changed")

    def check_update_column_2(self, device_serial):
        count = 0
        max_wait = 300
        status = self.xiq.xflowscommonDevices.get_device_updated_status(device_serial=device_serial)
        while not status and count < max_wait:
            time.sleep(10)
            count += 10
            status = self.xiq.xflowscommonDevices.get_device_updated_status(device_serial=device_serial)
            print(
                f"\nINFO \t Time elapsed in the update column to reflect the firmware updating is '{count} seconds'\n")

    def select_specific_firmware_version(self, sw_model):
        print("Click on upgrade to the specific device firmware version drop down")

        # Expand on drop down list
        AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_download_specific_firmware_drop_down_button())

        # Get all the images from drop down list
        specific_firmware_items = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_download_specific_firmware_drop_down_items()
        time.sleep(2)

        arm_templ = re.compile(r"Switch\sEngine\s(5320|5420|5520)")
        x_templ = re.compile(r"X4[4-6]0-G2")
        lite_templ = re.compile(r"X435")
        onie_templ = re.compile(r"(X465|Switch\sEngine\s5720)")

        img_pattern = ""
        if arm_templ.match(sw_model) is not None:
            prefix = "_arm"
        elif x_templ.match(sw_model) is not None:
            prefix = "X"
        elif lite_templ.match(sw_model) is not None:
            prefix = "lite"
        elif onie_templ.match(sw_model) is not None:
            img_pattern = r"onie-.*\.x86_64.xos"
        else:
            print(f"Switch model {sw_model} is invalid")
            return False

        if img_pattern == "":
            img_pattern = f"summit{prefix}" + r"-.*\.xos"

        if specific_firmware_items is None:
            print("No images present in drop down list")
            return False

        for item in specific_firmware_items:
            # Verify if all images are exos valid
            pattern = re.compile(img_pattern)

            if pattern.match(item.text) is None:
                print(f"Image {item.text} doesn't correspond with current template")
                return False

        if len(specific_firmware_items) > 0:
            AutoActions().click(specific_firmware_items[0])
        else:
            print("No images present in drop down list")
            return False

        return True

    def select_specific_firmware_version_tcxm_20583(self, sw_model, image_version):
        print("Click on upgrade to the specific device firmware version drop down")

        # Expand on drop down list
        AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_download_specific_firmware_drop_down_button())

        # Get all the images from drop down list
        specific_firmware_items = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_download_specific_firmware_drop_down_items()
        time.sleep(2)

        arm_templ = re.compile(r"Switch\sEngine\s(5320|5420|5520)")
        x_templ = re.compile(r"X4[3-6]0-G2")
        lite_templ = re.compile(r"X435")
        onie_templ = re.compile(r"(X465|Switch\sEngine\s5720)")

        img_pattern = ""
        if arm_templ.match(sw_model) is not None:
            prefix = "_arm"
        elif x_templ.match(sw_model) is not None:
            prefix = "X"
        elif lite_templ.match(sw_model) is not None:
            prefix = "lite"
        elif onie_templ.match(sw_model) is not None:
            img_pattern = r"onie-.*\.x86_64.xos"
        else:
            print(f"Switch model {sw_model} is invalid")
            return False

        if img_pattern == "":
            img_pattern = f"summit{prefix}" + r"-.*\.xos"

        if specific_firmware_items is None:
            print("No images present in drop down list")
            return False

        this_image_version = ''
        for item in specific_firmware_items:
            # Verify if all images are exos valid
            pattern = re.compile(img_pattern)

            if pattern.match(item.text) is None:
                print(f"Image {item.text} doesn't correspond with current template")
                return False

            if image_version in item.text:
                this_image_version = item
                print(f"Image {item.text} correspond with image version from dut")
                break

        if this_image_version != '':
            print("Selected image version is:" + str(this_image_version.text))
            AutoActions().click(this_image_version)
        else:
            print("No images present in drop down list")
            return False

        return True

    def select_specific_firmware_version_by_image(self, sw_model, image_version):
        print("Click on upgrade to the specific device firmware version drop down")

        # Expand on drop down list
        AutoActions().click(
            self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_download_specific_firmware_drop_down_button())

        # Get all the images from drop down list
        specific_firmware_items = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_download_specific_firmware_drop_down_items()
        time.sleep(2)

        arm_templ = re.compile(r"Switch\sEngine\s(5320|5420|5520)")
        x_templ = re.compile(r"X4[3-6]0-G2")
        lite_templ = re.compile(r"X435")
        onie_templ = re.compile(r"(X465|Switch\sEngine\s5720)")

        img_pattern = ""
        if arm_templ.match(sw_model) is not None:
            prefix = "_arm"
        elif x_templ.match(sw_model) is not None:
            prefix = "X"
        elif lite_templ.match(sw_model) is not None:
            prefix = "lite"
        elif onie_templ.match(sw_model) is not None:
            img_pattern = r"onie-.*\.x86_64.xos"
        else:
            print(f"Switch model {sw_model} is invalid")
            return False

        if img_pattern == "":
            img_pattern = f"summit{prefix}" + r"-.*\.xos"

        if specific_firmware_items is None:
            print("No images present in drop down list")
            return False

        this_image_version = ''
        for item in specific_firmware_items:
            # Verify if all images are exos valid
            pattern = re.compile(img_pattern)

            if pattern.match(item.text) is None:
                print(f"Image {item.text} doesn't correspond with current template")
                return False

            if image_version not in item.text:
                this_image_version = item
                print(f"Image {item.text} was selected")
                break

        if this_image_version != '':
            print("Selected image version is:" + str(this_image_version.text))
            AutoActions().click(this_image_version)
        else:
            print("No images present in drop down list")
            return False

        return True

    def select_sw_template_device_config_forw_delay(self, nw_policy, sw_template):
        """
        - This Keyword will Select the Switch Template on Network Policy and change the forward delay time from device configuration
        - Keyword Usage
         - ``Select SW Template  ${NW_POLICY_NAME}  ${SW_TEMPLATE_NAME}``

        :param nw_policy: Name of the Network Policy to select Switch Template
        :param sw_template: Name of the sw_template
        :return: 1 If successfully Selected Switch template
        """

        self.xiq.xflowsconfigureNetworkPolicy.navigate_to_np_edit_tab(nw_policy)
        time.sleep(5)
        print("Click on Device Template tab button")
        AutoActions().click(self.xiq.xflowsconfigureDeviceTemplate.device_template_web_elements.get_add_device_template_menu())
        time.sleep(2)

        tab = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_tab_button()
        if tab.is_displayed():
            print("Click on Switch Templates tab")
            AutoActions().click(tab)
            time.sleep(2)

        print("Switch Template: " + sw_template)
        row = self.xiq.xflowsconfigureSwitchTemplate.get_sw_template_row_hyperlink(sw_template)

        AutoActions().click(row)
        time.sleep(5)

        AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_device_sett_forward_delay_drop_down())
        time.sleep(2)

        container = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_device_sett_forward_delay_drop_down_container()
        container_val = container.text[:2]
        print(f"Default STP forward delay value in device template is {container_val}")

        AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_device_sett_forward_delay_drop_down_item16())
        container = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_device_sett_forward_delay_drop_down_container()
        container_val = container.text[:2]
        delay_container = container_val

        time.sleep(3)
        print("Get Template Save Button")
        save_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_save_button_adv_tab()

        rc = -1
        for save_btn in save_btns:
            if save_btn.is_displayed():
                print("Click on the save template button")
                AutoActions().click(save_btn)
                time.sleep(10)
                break;

        time.sleep(3)
        print("Click on network policy exit button")
        AutoActions().click(self.xiq.xflowsconfigureNetworkPolicy.np_web_elements.get_np_exit_button())
        time.sleep(2)

        return delay_container

    def get_nw_templ_device_config_forward_delay(self, dut):

        try:
            for attempts in range(3):
                time.sleep(5)
                self.devCmd.send_cmd(dut.name, 'disable cli paging',
                                     max_wait=10, interval=2)

                output = self.devCmd.send_cmd(dut.name, 'show stpd detail',
                                                      max_wait=10,
                                                      interval=2)
                print(output[0].return_text)
                output_traffic = output[0].return_text

                p = re.compile(r'(CfgBrForwardDelay:\s+)+(\d+)', re.M)

                match_text = re.findall(p, output[0].return_text)
                print(f"{match_text}")

                sw_model = []
                sw_model.append(match_text[0][1])

                print(f"forward delay is {match_text[0][1]} seconds")

                return match_text[0][1]
        finally:
            time.sleep(1)

    def set_nw_templ_device_config_forward_delay(self, dut):

        try:
            for attempts in range(3):
                time.sleep(5)
                self.devCmd.send_cmd(dut.name, 'configure stpd s0 forwarddelay 15',
                                     max_wait=10, interval=2)

                output = self.devCmd.send_cmd(dut.name, 'show stpd detail',
                                              max_wait=10,
                                              interval=2)
                print(output[0].return_text)
                output_traffic = output[0].return_text

                p = re.compile(r'(CfgBrForwardDelay:\s+)+(\d+)', re.M)

                match_text = re.findall(p, output[0].return_text)
                print(f"{match_text}")

                sw_model = []
                sw_model.append(match_text[0][1])

                print(f"forward delay is {match_text[0][1]} seconds")

                return match_text[0][1]
        finally:
            time.sleep(1)

    def press_upload_config_and_upgr_firm_button(self, nw_policy, sw_template):
        """
        - This Keyword will Select the Switch Template on Network Policy and change the forward delay time from device configuration
        - Keyword Usage
         - ``Select SW Template  ${NW_POLICY_NAME}  ${SW_TEMPLATE_NAME}``

        :param nw_policy: Name of the Network Policy to select Switch Template
        :param sw_template: Name of the sw_template
        :return: 1 If successfully Selected Switch template
        """

        self.xiq.xflowsconfigureNetworkPolicy.navigate_to_np_edit_tab(nw_policy)
        time.sleep(5)
        print("Click on Device Template tab button")
        AutoActions().click(
            self.xiq.xflowsconfigureDeviceTemplate.device_template_web_elements.get_add_device_template_menu())
        time.sleep(2)

        tab = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_tab_button()
        if tab.is_displayed():
            print("Click on Switch Templates tab")
            AutoActions().click(tab)
            time.sleep(2)

        print("Switch Template: " + sw_template)
        row = self.xiq.xflowsconfigureSwitchTemplate.get_sw_template_row_hyperlink(sw_template)

        AutoActions().click(row)
        time.sleep(5)

        print(" Go to the advanced settings tab ")

        ok = 1
        if AutoActions().click(
                self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab()) == -1:
            print("Unable to click on Verify adanced settings button")
            ok = 0
        else:
            print("Click on Verify adanced settings button")

        assert ok == 1, "Unable to click on Verify adanced settings button"

        AutoActions().click(
            self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_tab())

        time.sleep(2)

        print("Verify if the Upgrade device firmware upon device authentication button is off by default")

        assert self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button().is_selected() == 0, print(
            "the button is not off by default")

        if self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button() == -1:
            print("Unable to click on Upgrade device firmware upon device authentication button ")
            return -1
        else:
            print("Click on Upgrade device firmware upon device authentication button")
            AutoActions().click(
                self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upgrade_device_on_off_button())

        print("Click on upload configuration button")
        AutoActions().click(
            self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_adv_settings_upload_configuration_on_off_button())

        time.sleep(3)

        print("Get Template Save Button")
        save_btns = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_save_button_adv_tab()

        rc = -1
        for save_btn in save_btns:
            if save_btn.is_displayed():
                print("Click on the save template button")
                AutoActions().click(save_btn)
                time.sleep(10)

                break;
        time.sleep(3)
        print("Click on network policy exit button")
        AutoActions().click(self.xiq.xflowsconfigureNetworkPolicy.np_web_elements.get_np_exit_button())

        time.sleep(2)

    def get_device_updated_status(self, device_serial='default', device_name='default', device_mac='default'):
        """
        - This keyword returns the device updated status by searching device row using serial, name or mac address
        - Assumes that already navigated to the manage-->device page
        - Keyword Usage:
         - ``Get Device Updated Status   device_serial=${DEVICE_SERIAL}``
         - ``Get Device Updated Status   device_name=${DEVICE_NAME}``
         - ``Get Device Updated Status   device_mac=${DEVICE_MAC}``

        :param device_serial: device Serial
        :param device_name: device Name
        :param device_mac: device MAC
        :return: 'updated Time' if the device is updated correctly else return updating status message
        """
        device_row = -1

        self.xiq.xflowscommonDevices.refresh_devices_page()
        time.sleep(5)

        print('Getting device Updated Status using')
        if device_serial != 'default':
            print("Getting Updated status of device with serial: ", device_serial)
            device_row = self.xiq.xflowscommonDevices.get_device_row(device_serial=device_serial)

        if device_name != 'default':
            print("Getting Updated status of device with name: ", device_name)
            device_row = self.xiq.xflowscommonDevices.get_device_row(device_name=device_name)

        if device_mac != 'default':
            print("Getting Updated status of device with MAC: ", device_mac)
            device_row = self.xiq.xflowscommonDevices.get_device_row(device_mac=device_mac)

        if device_row:
            time.sleep(5)
            device_updated_status = self.xiq.xflowscommonDevices.devices_web_elements.get_updated_status_cell(device_row)

            if device_updated_status is None:
                print("Device Updating Status: None")
                return 'None'

            device_updated_status =self.xiq.xflowscommonDevices.devices_web_elements.get_updated_status_cell(device_row).text
            print("Device Updated Status is :", device_updated_status)
            if "Querying" in device_updated_status:
                print("Device Updating Status: Querying")
                return 'Querying'

            if "IQ Engine Firmware Updating" in device_updated_status:
                print("Device Updating Status: IQ Engine Firmware Updating")
                return 'IQ Engine Firmware Updating'

            if "User Configuration Updating" in device_updated_status:
                print("Device Updating Status: User Configuration Updating")
                return 'User Configuration Updating'

            if "Rebooting" in device_updated_status:
                print("Device Updating Status: Rebooting")
                return 'Rebooting'

            if "Certification Updating" in device_updated_status:
                print("Device Updating Status: Certification Updating")
                return 'Certification Updating'

            if "Application Signature Downloading" in device_updated_status:
                print("Device Updating Status: Application Signature Downloading")
                return 'Application Signature Downloading'
            if "Device Update Failed" in device_updated_status:
                print("Device updating status: Device update failed")
                return 'Device Update Failed'
            else:
                return device_updated_status

    def get_last_event_from_device360(self, dut, close_360_window=True):
        self.xiq.xflowscommonDevices._goto_devices()
        time.sleep(3)
        self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
        time.sleep(3)
        self.xiq.xflowsmanageDevice360.device360_select_events_view()
        time.sleep(3)

        count = 0
        if self.xiq.xflowsmanageDevice360.device360_search_event_and_confirm_event_description_contains("Download Config") != -1:
            count += 1

        if self.xiq.xflowsmanageDevice360.device360_search_event_and_confirm_event_description_contains("firmware successful") != -1:
            count += 1

        if close_360_window:
            self.xiq.xflowsmanageDevice360.close_device360_window()
        return count

    def managed_unmanaged(self, device_serial):
        time.sleep(1)
        self.xiq.xflowsmanageDevices.select_device(device_serial=device_serial)

        time.sleep(2)
        print("Click on actions button")
        AutoActions().click(self.xiq.xflowsmanageDevices.devices_web_elements.get_manage_device_actions_button())

        time.sleep(1)
        print("Click on Change Management Status")
        AutoActions().move_to_element(self.xiq.xflowsmanageDevices.devices_web_elements.get_manage_device_actions_change_management_status())

        time.sleep(1)
        print("Get device to unmanaged state")
        AutoActions().click(self.xiq.xflowsmanageDevices.devices_web_elements.get_manage_device_actions_change_management_status_unmanage())

        time.sleep(2)
        print("Press yes on dialog")
        AutoActions().click(
            self.xiq.xflowsmanageDevices.devices_web_elements.get_manage_device_actions_change_management_status_yes_button())

        time.sleep(2)
        print("Close dialog")
        AutoActions().click(
            self.xiq.xflowsmanageDevices.devices_web_elements.get_manage_device_actions_change_management_status_close_dialog())

        self.xiq.xflowscommonDevices.refresh_devices_page()

        time.sleep(5)
        self.xiq.xflowsmanageDevices.select_device(device_serial=device_serial)

        time.sleep(5)
        print("Click on actions button")
        AutoActions().click(self.xiq.xflowsmanageDevices.devices_web_elements.get_manage_device_actions_button())

        time.sleep(5)
        print("Click on Change Management Status")
        AutoActions().move_to_element(
            self.xiq.xflowsmanageDevices.devices_web_elements.get_manage_device_actions_change_management_status())

        time.sleep(5)
        print("Get device to managed state")
        AutoActions().click(self.xiq.xflowsmanageDevices.devices_web_elements.get_manage_device_actions_change_management_status_manage())

        time.sleep(2)
        print("Press yes on dialog")
        AutoActions().click(
            self.xiq.xflowsmanageDevices.devices_web_elements.get_manage_device_actions_change_management_status_yes_button())

        time.sleep(3)
        print("Close dialog")
        AutoActions().click(
            self.xiq.xflowsmanageDevices.devices_web_elements.get_manage_device_actions_change_management_status_close_dialog())

        time.sleep(2)
        self.xiq.xflowscommonDevices.refresh_devices_page()


    def get_device_status_debug(self, dut, message):
        """
        - This keyword was made to debug an intermitent isssue that makes it seem like the device is disconected and makes
        the test fail. This is a wrapper function for get_device_status.

        :param dut: device under testing
        :param message: message that check_device_status should return
        :return:
        - 'green' if device connected and config audit match
        - 'config audit mismatch' if device connected and config audit mismatch
        - 'disconnected' if device disconnected and unable to connect after 10 minutes
        - 'unknown' if device connection status is 'Unknown'
        """

        network_manager = NetworkElementConnectionManager()
        failed = False
        # This block is used to trigger problem
        # network_manager.connect_to_network_element_name(dut.name)
        # self.devCmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2,
        #                      confirmation_phrases='Do you want to continue?', confirmation_args='y')
        # network_manager.close_connection_to_network_element(dut.name)

        # This function logs the issue and the details associated. It was made to take up less code space
        def log_issue(res, dut, message):
            Screen().save_screen_shot()

            # Connect to CLI and check iqagent
            network_manager.connect_to_network_element_name(dut.name)
            iqagent_info = self.devCmd.send_cmd(dut.name, 'show iqagent', max_wait=0, interval=1)
            re_compiler = re.compile(r"Status\s*(.*)", re.M)
            connection_status = re.findall(re_compiler, iqagent_info[0].return_text)
            network_manager.close_connection_to_network_element(dut.name)

            print(f"Device status issue: chech_device_status() returned: {res} when it should be {message}!!!")
            print(f"Connections status in CLI is: {connection_status}")

        for repeat in range(10):
            res = self.xiq.xflowscommonDevices.get_device_status(device_serial=dut.serial)

            if res != message and not failed:
                failed = True
                log_issue(res, dut, message)
                print("Trying again")

            else:
                time.sleep(2)
                return res

            time.sleep(1)

        log_issue(res, dut, message)
        print("The issue persisted")

        return res

# Author        : Siva prasath
# Description   : This script run the below tests for voip story feature according with XIQ-1429 story
# Testcases     :TCXM_19696,TCXM_19689,TCXM_19692,TCXM_19684,TCXM_19498,TCXM_19496,TCXM_19703,TCXM_19687,
#                   TCXM_19506,TCXM_19742
#
# Pre-Requests  : First organization should be created in the XIQ prior to start this test script in case of AIO.
#                 In cloud it is not necessary.
# Comments      : This test is applicable for 1 node setup only, the script run for Exos standalone
import pytest
import os
import time
import re

from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import \
    NetworkElementConnectionManager
from extauto.common.Utils import Utils
from extauto.common.AutoActions import AutoActions
from ..Resources.SuiteUdks import SuiteUdk
from pytest import mark

current_exos_port = 0

@mark.testbed_1_node
class XIQ1429Tests:

    @classmethod
    def setup_class(cls):
        try:
            cls.executionHelper = PytestExecutionHelper()
            cls.tb = PytestConfigHelper(config)
            cls.cfg = config
            cls.cfg['${OUTPUT DIR}'] = os.getcwd()
            cls.cfg['${TEST_NAME}'] = 'SETUP'

            cls.defaultLibrary = DefaultLibrary()

            cls.udks = cls.defaultLibrary.apiUdks
            cls.devCmd = cls.defaultLibrary.deviceNetworkElement.networkElementCliSend
            cls.udks = cls.defaultLibrary.apiUdks
            cls.udks.setupTeardownUdks.networkElementConnectionManager.connect_to_all_network_elements()
            if cls.tb.dut1.cli_type == "voss" or cls.tb.dut1_platform.lower() == "stack":
                pytest.skip("This platform {} is not supported for this feature!".format(cls.tb.dut1.cli_type))
            cls.network_manager = NetworkElementConnectionManager()
            cls.utils = Utils()
            cls.auto_actions = AutoActions()
            cls.xiq = XiqLibrary()
            cls.xiq.login.login_user(cls.tb.config.tenant_username, cls.tb.config.tenant_password,
                                     url=cls.tb.config.test_url, IRV=True)

            cls.suite_udk = SuiteUdk(cls)
            cls.dut_location = cls.suite_udk.generate_random_onboarding_location()

            dut = cls.suite_udk.get_dut(os="exos")
            assert dut, "Failed to find a dut in tb"
            cls.dut = dut
            if cls.tb.dut1.make == "exos":
                cls.suite_udk.get_virtual_router(cls.tb.dut1_name, cls.tb.dut1.ip)

            cls.suite_udk.delete_create_location_organization(cls.dut_location)

            cls.xiq.xflowscommonDevices.delete_device(device_mac=dut.mac)
            cls.suite_udk.configure_iqagent(dut)

            assert cls.xiq.xflowsmanageSwitch.onboard_switch(
                dut.serial, device_os=dut.cli_type, entry_type="Manual", location=cls.dut_location) == 1

            assert cls.xiq.xflowscommonDevices.wait_until_device_online(
                device_mac=dut.mac) == 1, "Device didn't come online"

            cls.xiq.xflowsglobalsettingsGlobalSetting.change_exos_device_management_settings(
                option="disable", platform=dut.cli_type.upper())

        except Exception as e:
            cls.executionHelper.setSetupFailure(True)

    @classmethod
    def teardown_class(cls):

        cls.xiq.xflowscommonDevices.delete_device(device_mac=cls.dut.mac)
        cls.xiq.xflowsmanageLocation.delete_location_building_floor(*cls.dut_location.split(","))
        cls.xiq.login.logout_user()
        cls.xiq.login.quit_browser()

    def inc_port(cls):
        global current_exos_port
        current_exos_port += 1
        return current_exos_port

    @mark.tcxm_19696
    @mark.p2
    @mark.testbed_1_node
    @mark.itsanity
    def test_create_voip_port_type_at_device360_level(self):
        """
        TCXM-19696 - Create VOIP Port type at Device360 Level

        Author: vstefan
        """
        self.executionHelper.testSkipCheck()
        dut = self.dut
        exos_port = str(self.inc_port())
        port_type_name = self.suite_udk.generate_port_type_name()

        self.xiq.xflowsmanageDevice360.navigator.navigate_to_devices()

        try:

            self.suite_udk.go_to_device_360_port_config(dut)
            assert self.xiq.xflowsmanageDevice360.create_voice_port(
                port=exos_port, port_type_name=port_type_name, device_360=True) == 1, \
                f"Failed to create a voice port type named {port_type_name}"

            self.suite_udk.save_device_360_port_config()
            self.suite_udk.verify_port_type_is_created_in_device360(port=exos_port, port_type_name=port_type_name)

        finally:
            self.suite_udk.revert_port_configuration(exos_port, port_type_name)
            self.suite_udk.save_device_360_port_config()
            self.xiq.xflowsmanageDevice360.close_device360_window()
            self.xiq.xflowsconfigureCommonObjects.delete_port_type_profile(port_type_name)
            self.xiq.xflowsmanageDevice360.navigator.navigate_to_devices()

    @mark.tcxm_19689
    @mark.p3
    @mark.testbed_1_node
    @mark.itsanity
    def test_verify_voice_signaling_vlan_dscp_value_device_360(self):
        """
        TCXM-19689 - Device360 - Verify med Voice Signalling VLAN - DSCP value between 0-63

        Author: vstefan
        """
        self.executionHelper.testSkipCheck()

        dut = self.dut
        exos_port = str(self.inc_port())
        port_type_name = self.suite_udk.generate_port_type_name()

        self.xiq.xflowsmanageDevice360.navigator.navigate_to_devices()

        try:
            self.suite_udk.go_to_device_360_port_config(dut)

            self.suite_udk.open_new_port_type_editor(exos_port, device_360=True)
            self.suite_udk.configure_port_name_usage_tab(port_type_name=port_type_name)
            self.suite_udk.go_to_next_editor_tab()
            self.suite_udk.set_voice_vlan(voice_vlan="11")
            self.suite_udk.set_data_vlan(data_vlan="22")
            self.suite_udk.enable_lldp_voice_vlan_options(lldp_voice_options_flag=True)

            self.suite_udk.verify_dscp_values_validation(
                dscp_field="lldp_advertisment_of_med_voice_signaling_vlan_dscp_value",
                min_dscp=0,
                max_dscp=63,
                expected_error_message='Please enter a valid number between 0-63'
            )

        finally:
            cancel_port_type_editor_button = self.xiq.xflowsmanageDevice360.get_cancel_port_type_editor()
            if cancel_port_type_editor_button:
                self.auto_actions.click(cancel_port_type_editor_button)
            self.xiq.xflowsmanageDevice360.close_device360_window()

    @mark.tcxm_19692
    @mark.testbed_1_node
    @mark.p3
    @mark.itsanity
    def test_verify_voice_vlan_dscp_value_device_360(self):
        """
        TCXM-19692 - Verify Device360 Voice VLAN - DSCP value between 0-63

        Author: vstefan
        """
        self.executionHelper.testSkipCheck()

        dut = self.dut
        exos_port = str(self.inc_port())
        port_type_name = self.suite_udk.generate_port_type_name()

        self.xiq.xflowsmanageDevice360.navigator.navigate_to_devices()

        try:
            self.suite_udk.go_to_device_360_port_config(dut)

            self.suite_udk.open_new_port_type_editor(exos_port, device_360=True)
            self.suite_udk.configure_port_name_usage_tab(port_type_name=port_type_name)
            self.suite_udk.go_to_next_editor_tab()
            self.suite_udk.set_voice_vlan(voice_vlan="11")
            self.suite_udk.set_data_vlan(data_vlan="22")
            self.suite_udk.enable_lldp_voice_vlan_options(lldp_voice_options_flag=True)

            self.validation = self.suite_udk.verify_dscp_values_validation(
                dscp_field="lldp_advertisment_of_med_voice_vlan_dscp_value", min_dscp=0, max_dscp=63,
                expected_error_message='Please enter a valid number between 0-63')

        finally:
            cancel_port_type_editor_button = self.xiq.xflowsmanageDevice360.get_cancel_port_type_editor()
            if cancel_port_type_editor_button:
                self.auto_actions.click(cancel_port_type_editor_button)
            self.xiq.xflowsmanageDevice360.close_device360_window()

    @mark.tcxm_19684
    @mark.p3
    @mark.testbed_1_node
    @mark.itsanity
    def test_voice_data_should_not_be_the_same_device_360(self):
        """
        TCXM-19684 - Text Box validation - Voice and Data vlan should not be same

        Author: vstefan
        """
        self.executionHelper.testSkipCheck()

        dut = self.dut
        exos_port = str(self.inc_port())
        port_type_name = self.suite_udk.generate_port_type_name()

        self.xiq.xflowsmanageDevice360.navigator.navigate_to_devices()

        try:
            self.suite_udk.go_to_device_360_port_config(dut)

            self.suite_udk.open_new_port_type_editor(exos_port, device_360=True)
            self.suite_udk.configure_port_name_usage_tab(port_type_name=port_type_name)
            self.suite_udk.go_to_next_editor_tab()
            self.suite_udk.set_voice_vlan(voice_vlan="100")
            self.suite_udk.set_data_vlan(data_vlan="100")
            self.suite_udk.go_to_next_editor_tab()

            expected_error_message = "Please specify different values for Data VLAN and Voice VLAN"
            errors = self.xiq.xflowsmanageDevice360.get_select_element_port_type("form_errors")
            assert errors

            assert any(re.search(expected_error_message, e.text) for e in errors), \
                f"Failed to find this error: {expected_error_message}"

        finally:
            cancel_port_type_editor_button = self.xiq.xflowsmanageDevice360.get_cancel_port_type_editor()
            if cancel_port_type_editor_button:
                self.auto_actions.click(cancel_port_type_editor_button)
            self.xiq.xflowsmanageDevice360.close_device360_window()


    @mark.tcxm_19498
    @mark.p3
    @mark.testbed_1_node
    @mark.itsanity
    def test_verify_voice_signaling_vlan_dscp_value_template(self):
        """
        TCXM-19498 - Verify Template med Voice Signalling VLAN - DSCP value between 0-63

        Author: vstefan
        """
        self.executionHelper.testSkipCheck()

        dut = self.dut
        exos_port = str(self.inc_port())

        port_type_name = self.suite_udk.generate_port_type_name()
        template_name = self.suite_udk.generate_template_name()
        policy_name = self.suite_udk.generate_policy_name()

        try:
            assert self.xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                policy_name=policy_name) == 1, f"Failed to create this network policy: {policy_name}"
            time.sleep(3)
            model_act = []

            if self.tb.dut1_platform.lower() == "stack":
                device_serial_list = self.tb.dut1.serial.split(",")
                for i in range(1, len(device_serial_list) + 1):
                    slots = 'self.tb.dut1.stack.slot' + str(i) + '.model'
                    val = eval(slots)
                    model_act.append(val)
            sw_model, model_units = self.xiq.xflowsconfigureSwitchTemplate.generate_template_name(
                self.tb.dut1_platform.lower(),
                self.tb.dut1.serial, self.tb.dut1.model, model_act)
            self.xiq.xflowsconfigureSwitchTemplate.add_sw_template(policy_name, sw_model, template_name)
            self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(policy_name, template_name)
            self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()

            self.suite_udk.open_new_port_type_editor(exos_port, device_360=False)
            self.suite_udk.configure_port_name_usage_tab(port_type_name=port_type_name)
            self.suite_udk.go_to_next_editor_tab()
            self.suite_udk.set_voice_vlan(voice_vlan="11")
            self.suite_udk.set_data_vlan(data_vlan="22")
            self.suite_udk.enable_lldp_voice_vlan_options(lldp_voice_options_flag=True)

            self.suite_udk.verify_dscp_values_validation(
                dscp_field="lldp_advertisment_of_med_voice_signaling_vlan_dscp_value",
                min_dscp=0,
                max_dscp=63,
                expected_error_message='Please enter a valid number between 0-63'
            )

        finally:
            cancel_port_type_editor_button = self.xiq.xflowsmanageDevice360.get_cancel_port_type_editor()
            if cancel_port_type_editor_button:
                self.auto_actions.click(cancel_port_type_editor_button)
            self.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(policy_name)
            self.xiq.xflowsconfigureCommonObjects.delete_switch_template(template_name)
            self.xiq.xflowsmanageDevice360.navigator.navigate_to_devices()

    @mark.tcxm_19496
    @mark.p3
    @mark.testbed_1_node
    @mark.itsanity
    def test_verify_voice_vlan_dscp_value_template(self):
        """
        TCXM-19496 - Verify Template Voice VLAN - DSCP value between 0-63

        Author: vstefan
        """
        self.executionHelper.testSkipCheck()

        dut = self.dut
        exos_port = str(self.inc_port())

        port_type_name = self.suite_udk.generate_port_type_name()
        template_name = self.suite_udk.generate_template_name()
        policy_name = self.suite_udk.generate_policy_name()

        try:
            assert self.xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                policy_name=policy_name) == 1, f"Failed to create this network policy: {policy_name}"
            time.sleep(3)
            model_act = []

            if self.tb.dut1_platform.lower() == "stack":
                device_serial_list = self.tb.dut1.serial.split(",")
                for i in range(1, len(device_serial_list) + 1):
                    slots = 'self.tb.dut1.stack.slot' + str(i) + '.model'
                    val = eval(slots)
                    model_act.append(val)
            sw_model, model_units = self.xiq.xflowsconfigureSwitchTemplate.generate_template_name(
                self.tb.dut1_platform.lower(),
                self.tb.dut1.serial, self.tb.dut1.model, model_act)
            time.sleep(3)
            self.xiq.xflowsconfigureSwitchTemplate.add_sw_template(policy_name,sw_model, template_name)
            self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(policy_name, template_name)
            self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()

            self.suite_udk.open_new_port_type_editor(exos_port, device_360=False)
            self.suite_udk.configure_port_name_usage_tab(port_type_name=port_type_name)
            self.suite_udk.go_to_next_editor_tab()
            self.suite_udk.set_voice_vlan(voice_vlan="11")
            self.suite_udk.set_data_vlan(data_vlan="22")
            self.suite_udk.enable_lldp_voice_vlan_options(lldp_voice_options_flag=True)

            self.suite_udk.verify_dscp_values_validation(
                dscp_field="lldp_advertisment_of_med_voice_vlan_dscp_value",
                min_dscp=0,
                max_dscp=63,
                expected_error_message='Please enter a valid number between 0-63'
            )

        finally:
            cancel_port_type_editor_button = self.xiq.xflowsmanageDevice360.get_cancel_port_type_editor()
            if cancel_port_type_editor_button:
                self.auto_actions.click(cancel_port_type_editor_button)
            self.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(policy_name)
            self.xiq.xflowsconfigureCommonObjects.delete_switch_template(template_name)
            self.xiq.xflowsmanageDevice360.navigator.navigate_to_devices()

    @mark.tcxm_19703
    @mark.p3
    @mark.testbed_1_node
    @mark.itsanity
    def test_verify_device360_summary_when_lldp_cdp_are_disabled(self):
        """
        TCXM-19703 - Verify Device360 summary view - when lldp and cdp advertisements are disabled

        Author: vstefan
        """
        self.executionHelper.testSkipCheck()

        dut = self.dut
        exos_port = str(self.inc_port())
        port_type_name = self.suite_udk.generate_port_type_name()

        self.xiq.xflowsmanageDevice360.navigator.navigate_to_devices()

        try:
            self.suite_udk.go_to_device_360_port_config(dut)

            self.suite_udk.open_new_port_type_editor(exos_port, device_360=True)
            self.suite_udk.configure_port_name_usage_tab(port_type_name=port_type_name)
            self.suite_udk.go_to_next_editor_tab()

            default_voice_vlan = self.suite_udk.get_voice_vlan()
            assert default_voice_vlan.get_attribute("value") == "", \
                "Expected voice vlan to be empty by default"
            default_data_vlan = self.suite_udk.get_data_vlan()
            assert default_data_vlan.get_attribute("value") == "1", \
                "Expected data vlan to be 1 by default"

            assert self.suite_udk.get_lldp_voice_vlan_options() is False, \
                "Expected LLDP Voice VLAN Options to be disabled"
            assert self.suite_udk.get_cdp_voice_vlan_options() is False, \
                "Expected CDP Voice VLAN Options to be disabled"

            self.suite_udk.set_voice_vlan(voice_vlan="100")
            self.suite_udk.set_data_vlan(data_vlan="2")

            default_voice_vlan = self.suite_udk.get_voice_vlan()
            assert default_voice_vlan.get_attribute("value") == "100", "Expected voice vlan to be 100"
            default_data_vlan = self.suite_udk.get_data_vlan()
            assert default_data_vlan.get_attribute("value") == "2", "Expected data vlan to be 2"

            self.suite_udk.go_to_last_page()

            expected_summary = {
                "LLDP Advertisements": "OFF",
                "802.1 VLAN and port protocol": "OFF",
                "Med Voice VLAN DSCP Value": "OFF",
                "Med Voice Signaling DSCP Value": "OFF",
                "CDP Advertisement": "OFF",
                "CDP Voice VLAN": "OFF",
                "CDP Power Available": "OFF",
                "Voice VLAN": "100",
                "Data VLAN": "2"
            }

            summary = self.suite_udk.get_summary()

            assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                f"Not all the values of the summary are the expected ones. " \
                f"Expected summary: {expected_summary}\nFound summary: {summary}"

        finally:
            cancel_port_type_editor_button = self.xiq.xflowsmanageDevice360.get_cancel_port_type_editor()
            if cancel_port_type_editor_button:
                self.auto_actions.click(cancel_port_type_editor_button)
            self.xiq.xflowsmanageDevice360.close_device360_window()

    @mark.tcxm_19687
    @mark.p1
    @mark.testbed_1_node
    @mark.itsanity
    def test_verify_voice_and_data_vlan_can_be_created_device_360_level(self):
        """
        TCXM-19687 - Device360 - Check Voice VLAN and Data VLAN can be created

        Author: vstefan
        """
        self.executionHelper.testSkipCheck()

        dut = self.dut
        exos_port = str(self.inc_port())
        port_type_name = self.suite_udk.generate_port_type_name()

        self.xiq.xflowsmanageDevice360.navigator.navigate_to_devices()

        try:
            self.suite_udk.go_to_device_360_port_config(dut)

            self.suite_udk.open_new_port_type_editor(exos_port, device_360=True)
            self.suite_udk.configure_port_name_usage_tab(port_type_name=port_type_name)
            self.suite_udk.go_to_next_editor_tab()

            default_voice_vlan = self.suite_udk.get_voice_vlan()
            assert default_voice_vlan.get_attribute("value") == "", "Expected voice vlan to be empty by default"
            default_data_vlan = self.suite_udk.get_data_vlan()
            assert default_data_vlan.get_attribute("value") == "1", "Expected data vlan to be 1 by default"

            self.suite_udk.enable_lldp_voice_vlan_options(lldp_voice_options_flag=True)
            self.suite_udk.enable_cdp_voice_vlan_options(cdp_voice_options_flag=True)

            assert self.suite_udk.get_lldp_voice_vlan_options() is True, \
                "Expected LLDP Voice VLAN Options to be enabled"
            assert self.suite_udk.get_cdp_voice_vlan_options() is True, "Expected CDP Voice VLAN Options to be enabled"

            self.suite_udk.set_voice_vlan(voice_vlan="100")
            self.suite_udk.set_data_vlan(data_vlan="2")

            default_voice_vlan = self.suite_udk.get_voice_vlan()
            assert default_voice_vlan.get_attribute("value") == "100", "Expected voice vlan to be 100"
            default_data_vlan = self.suite_udk.get_data_vlan()
            assert default_data_vlan.get_attribute("value") == "2", "Expected data vlan to be 2"

            self.suite_udk.go_to_last_page()

            expected_summary = {
                "LLDP Advertisements": "ON",
                "802.1 VLAN and port protocol": "ON",
                "Med Voice VLAN DSCP Value": "OFF",
                "Med Voice Signaling DSCP Value": "OFF",
                "CDP Advertisement": "ON",
                "CDP Voice VLAN": "ON",
                "CDP Power Available": "ON",
                "Voice VLAN": "100",
                "Data VLAN": "2"
            }

            summary = self.suite_udk.get_summary()

            assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                f"Not all the values of the summary are the expected ones." \
                f" Expected summary: {expected_summary}\nFound summary: {summary}"

        finally:
            cancel_port_type_editor_button = self.xiq.xflowsmanageDevice360.get_cancel_port_type_editor()
            if cancel_port_type_editor_button:
                self.auto_actions.click(cancel_port_type_editor_button)
            self.xiq.xflowsmanageDevice360.close_device360_window()

    @mark.tcxm_19506
    @mark.p2
    @mark.testbed_1_node
    @mark.itsanity
    def test_verify_voice_and_data_vlan_can_be_created_template_level(self):
        """
        TCXM-19506 - Check Voice VLAN and Data VLAN can be created
        """
        self.executionHelper.testSkipCheck()

        dut = self.dut
        exos_port = str(self.inc_port())

        port_type_name = self.suite_udk.generate_port_type_name()
        template_name = self.suite_udk.generate_template_name()
        policy_name = self.suite_udk.generate_policy_name()

        try:
            assert self.xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                policy_name=policy_name) == 1, f"Failed to create this network policy: {policy_name}"
            time.sleep(3)
            model_act = []

            if self.tb.dut1_platform.lower() == "stack":
                device_serial_list = self.tb.dut1.serial.split(",")
                for i in range(1, len(device_serial_list) + 1):
                    slots = 'self.tb.dut1.stack.slot' + str(i) + '.model'
                    val = eval(slots)
                    model_act.append(val)
            sw_model, model_units = self.xiq.xflowsconfigureSwitchTemplate.generate_template_name(
                self.tb.dut1_platform.lower(),
                self.tb.dut1.serial, self.tb.dut1.model, model_act)
            self.xiq.xflowsconfigureSwitchTemplate.add_sw_template(policy_name, sw_model, template_name)
            self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(policy_name, template_name)
            self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()

            self.suite_udk.open_new_port_type_editor(exos_port, device_360=False)
            self.suite_udk.configure_port_name_usage_tab(port_type_name=port_type_name)
            self.suite_udk.go_to_next_editor_tab()

            default_voice_vlan = self.suite_udk.get_voice_vlan()
            assert default_voice_vlan.get_attribute("value") == "", "Expected voice vlan to be empty by default"
            default_data_vlan = self.suite_udk.get_data_vlan()
            assert default_data_vlan.get_attribute("value") == "1", "Expected data vlan to be 1 by default"

            self.suite_udk.enable_lldp_voice_vlan_options(lldp_voice_options_flag=True)
            self.suite_udk.enable_cdp_voice_vlan_options(cdp_voice_options_flag=True)

            assert self.suite_udk.get_lldp_voice_vlan_options() is True, "Expected LLDP Voice VLAN Options to be enabled"
            assert self.suite_udk.get_cdp_voice_vlan_options() is True, "Expected CDP Voice VLAN Options to be enabled"

            self.suite_udk.set_voice_vlan(voice_vlan="100")
            self.suite_udk.set_data_vlan(data_vlan="2")

            default_voice_vlan = self.suite_udk.get_voice_vlan()
            assert default_voice_vlan.get_attribute("value") == "100", "Expected voice vlan to be 100"
            default_data_vlan = self.suite_udk.get_data_vlan()
            assert default_data_vlan.get_attribute("value") == "2", "Expected data vlan to be 2"

            self.suite_udk.go_to_last_page()

            expected_summary = {
                "LLDP Advertisements": "ON",
                "802.1 VLAN and port protocol": "ON",
                "Med Voice VLAN DSCP Value": "OFF",
                "Med Voice Signaling DSCP Value": "OFF",
                "CDP Advertisement": "ON",
                "CDP Voice VLAN": "ON",
                "CDP Power Available": "ON",
                "Voice VLAN": "100",
                "Data VLAN": "2"
            }

            summary = self.suite_udk.get_summary()

            assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                f"Not all the values of the summary are the expected ones." \
                f" Expected summary: {expected_summary}\nFound summary: {summary}"

        finally:
            cancel_port_type_editor_button = self.xiq.xflowsmanageDevice360.get_cancel_port_type_editor()
            if cancel_port_type_editor_button:
                self.auto_actions.click(cancel_port_type_editor_button)
            self.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(policy_name)
            self.xiq.xflowsconfigureCommonObjects.delete_switch_template(template_name)
            self.xiq.xflowsmanageDevice360.navigator.navigate_to_devices()

    @mark.tcxm_19742
    @mark.p3
    @mark.testbed_1_node
    @mark.itsanity
    def test_verify_voip_port_type_not_available_for_voss_template(self):
        """
        TCXM-19742 - Negative scenario - Voip port type is not available in VOSS

        Author: vstefan
        """
        self.executionHelper.testSkipCheck()

        dut = self.dut
        voss_port = "1/1"

        template_name = self.suite_udk.generate_template_name()
        policy_name = self.suite_udk.generate_policy_name()

        try:
            assert self.xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                policy_name=policy_name) == 1, f"Failed to create this network policy: {policy_name}"
            time.sleep(3)

            self.xiq.xflowsconfigureSwitchTemplate.add_sw_template(policy_name, "Fabric Engine 5320-16P-4XE", template_name)
            self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(policy_name, template_name)
            time.sleep(4)
            self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            time.sleep(10)
            self.suite_udk.open_new_port_type_editor(voss_port, device_360=False)

            phone_port_element = self.xiq.xflowsmanageDevice360.get_select_element_port_type(
                "port usage", "phone port")
            assert not phone_port_element.is_displayed(), \
                "Failed! Expected not to find the phone port type on a VOSS switch"

        finally:
            cancel_port_type_editor_button = self.xiq.xflowsmanageDevice360.get_cancel_port_type_editor()
            if cancel_port_type_editor_button:
                self.auto_actions.click(cancel_port_type_editor_button)
            self.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(policy_name)
            self.xiq.xflowsconfigureCommonObjects.delete_switch_template(template_name)
            self.xiq.xflowsmanageDevice360.navigator.navigate_to_devices()

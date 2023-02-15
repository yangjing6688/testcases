import time
import datetime
import re

from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from extauto.common.AutoActions import AutoActions
from extauto.common.Utils import Utils


# --------------------------------------------------------------------------------------------------------
#   Setup/Teardown Keywords
# --------------------------------------------testcase_base.py--------------------------------------------

def dut_model_edit(sw_model):
    if ('SwitchEngine' in sw_model or 'FabricEngine' in sw_model) and sw_model.count('_') == 1:
        return re.sub(r'(^[A-Z][a-z]*)([A-Z][a-z]*)(\d*[A-Z]|\d*)_(\d*[A-Z]*)$', r'\1 \2 \3-\4', sw_model)
    elif ('SwitchEngine' in sw_model or 'FabricEngine' in sw_model) and sw_model.count('_') == 2:
        return re.sub(r'(^[A-Z][a-z]*)([A-Z][a-z]*)(\d*[A-Z]|\d*)_(\d*[A-Z]*)_(\d*[A-Z]*)$',
                      r'\1 \2 \3-\4-\5', sw_model)
    elif ('SwitchEngine' in sw_model or 'FabricEngine' in sw_model) and sw_model.count('_') == 3:
        return re.sub(r'(^[A-Z][a-z]*)([A-Z][a-z]*)(\d*[A-Z]|\d*)_(\d*[A-Z]*)_(\d*[A-Z]*)_(\d*[A-Z]*)$',
                      r'\1 \2 \3-\4-\5-\6', sw_model)
    elif ('SwitchEngine' not in sw_model or 'FabricEngine' not in sw_model) and sw_model.count('_') == 1:
        return re.sub(r'(^[A-Z][a-z]*)([A-Z][a-z]*)(\d*[A-Z]|\d*)_(\d*[A-Z]*)$', r'\1 \2 \3-\4', sw_model)
    elif ('SwitchEngine' not in sw_model or 'FabricEngine' not in sw_model) and sw_model.count('_') == 2:
        return re.sub(r'(^[A-Z][a-z]*\d*)_(\d*[A-Z]*|\d*)_(\d*[A-Z]*|\d*)$', r'\1-\2-\3', sw_model)
    elif ('SwitchEngine' in sw_model or 'FabricEngine' in sw_model) and sw_model.count('_') == 3:
        return re.sub(r'(^[A-Z][a-z]*)([A-Z][a-z]*)(\d*[A-Z]|\d*)_(\d*[A-Z]*)_(\d*[A-Z]*)_(\d*[A-Z]*)$',
                      r'\1 \2 \3-\4-\5-\6', sw_model)


class SuiteUdks:
    def __init__(self):
        self.auto_actions = AutoActions()
        self.utils = Utils()
        self.xiq = XiqLibrary()
        self.defaultLibrary = DefaultLibrary()
        self.devCmd = self.defaultLibrary.deviceNetworkElement.networkElementCliSend

    def get_virtual_router(self, dut):
        """
        This function is used to get the virtual router from an EXOS device
        :param dut: the instance of the EXOS device
        :return: 1 - if the virtual router was found successfully ; -1 - if not
        """
        result = self.devCmd.send_cmd(dut.name, 'show vlan', max_wait=10, interval=2)
        output = result[0].cmd_obj.return_text

        pattern = r'(\w+)(\s+)(\d+)(\s+)(' + f'{dut.ip}' r')(\s+)(\/.*)(\s+)(\w+)(\s+/)(.*)(VR-\w+)'
        match = re.search(pattern, output)

        if match:
            self.utils.print_info(f"Mgmt Vlan Name  : {match.group(1)}")
            self.utils.print_info(f"Vlan ID         : {match.group(3)}")
            self.utils.print_info(f"Mgmt IP address : {match.group(5)}")
            self.utils.print_info(f"Active ports    : {match.group(9)}")
            self.utils.print_info(f"Total ports     : {match.group(11)}")
            self.utils.print_info(f"Virtual router  : {match.group(12)}")

            if int(match.group(9)) > 0:
                return match.group(12)
            else:
                self.utils.print_info(f"There is no active port in the mgmt vlan {match.group(1)}")
                return -1
        else:
            self.utils.print_info("Pattern not found, unable to get virtual router info!")
            return -1

    def disable_iqagent(self, dut):
        """
        This function is used to disable IQAgent on an EXOS device
        :param dut: the instance of the EXOS device
        :return: 1 - if the IQAgent was disabled successfully ; -1 - if not
        """
        try:
            self.devCmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to continue? (y/N)', confirmation_args='y')
        except Exception as exc:
            self.utils.print_info(exc)
            return -1
        return 1

    def configure_iqagent(self, dut, xiq_ip_addr):
        """
        This function is used to configure IQAgent on an EXOS device
        :param dut: the instance of the EXOS device
        :param xiq_ip_addr: the ip address of the XIQ
        :return: 1 - if the configuration was successful ; -1 - if not
        """
        try:
            self.devCmd.send_cmd(dut.name, f'configure iqagent server ipaddress {xiq_ip_addr}', max_wait=10, interval=2)

            vr_name = self.get_virtual_router(dut)
            if vr_name == -1:
                return -1
            self.devCmd.send_cmd(dut.name, f'configure iqagent server vr {vr_name}', max_wait=10, interval=2)

            self.devCmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)
            self.devCmd.send_cmd(dut.name, 'save configuration', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to save configuration to primary.cfg and overwrite '
                                                      'it? (y/N)', confirmation_args='y')
            self.devCmd.send_cmd_verify_output(dut.name, 'show process iqagent', 'Ready', max_wait=30, interval=10)
        except Exception as exc:
            self.utils.print_info(exc)
            return -1
        return 1

    def verify_upload_config_auto_button(self, option="OFF"):
        """
        This function is used to verify the `Upload configuration automatically` button from Advanced Settings tab
        based on an option given as parameter
        :param option: name of policy
        :return: 1 - if the button is equal with option was successful ; -1 - if not
        """
        try:
            switch_template = self.xiq.xflowsconfigureSwitchTemplate
            verify_upload_cfg_auto = switch_template.sw_template_web_elements.get_sw_template_auto_cfg().is_selected()
            if not verify_upload_cfg_auto and option == "OFF":
                self.utils.print_info("Auto configuration button is on OFF!")
                return 1
            elif verify_upload_cfg_auto and option == "ON":
                self.utils.print_info("Auto configuration button is on ON!")
                return 1
        except Exception as exc:
            self.utils.print_info(exc)
            return -1
        return -1

    def set_upload_config_auto_button(self):
        """
        This function is used to set the `Upload configuration automatically` button from Advanced Settings tab
        :return: 1 - if the button is set successfully ; -1 - if not
        """
        try:
            switch_template = self.xiq.xflowsconfigureSwitchTemplate
            verify_upload_cfg_auto = switch_template.sw_template_web_elements.get_sw_template_auto_cfg().is_selected()
            if not verify_upload_cfg_auto:
                self.utils.print_info("Auto configuration button is by default on OFF!")
            else:
                self.utils.print_info("Auto configuration button is already on ON!")
                return -1

            self.utils.print_info("Click on Upload configuration automatically button")
            self.auto_actions.click(switch_template.sw_template_web_elements.get_sw_template_auto_cfg())
        except Exception as exc:
            self.utils.print_info(exc)
            return -1
        time.sleep(3)
        return 1

    def verify_enable_auto_revert_option(self):
        """
        This function is used to verify if the `Reboot and revert Extreme Networks switch configuration if IQAgent is
        unresponsive after configuration update.` button from Advanced Settings tab is present or not
        :return: 1 - if the button is present ; -1 - if not
        """
        try:
            switch_template = self.xiq.xflowsconfigureSwitchTemplate

            enable_auto_revert = switch_template.sw_template_web_elements.get_sw_template_auto_revert_enabled()
            if not enable_auto_revert:
                self.utils.print_info("Enable Auto Revert button is not present!")
                return -1
            elif not enable_auto_revert.is_displayed():
                self.utils.print_info("Enable Auto Revert button is not present!")
                return -1
            else:
                self.utils.print_info("Enable Auto Revert button is present!")
                return 1
        except Exception as exc:
            self.utils.print_info(exc)
            return -1

    def check_text_enable_auto_revert_option(self):
        """
        This function is used to verify the `Reboot and revert Extreme Networks switch configuration if IQAgent is
        unresponsive after configuration update.` button text from Advanced Settings tab based on an option given as
        parameter
        :return: 1 - if the button text is the one expected ; -1 - if not
        """
        try:
            switch_template = self.xiq.xflowsconfigureSwitchTemplate

            enable_auto_revert_message = switch_template.sw_template_web_elements.get_sw_template_auto_revert_msg().text
            if enable_auto_revert_message != "Reboot and revert Extreme Networks switch configuration if IQAgent is " \
                                             "unresponsive after configuration update.":
                self.utils.print_info(
                    f"The Enable Auto Revert button name is not the correct one: {enable_auto_revert_message}!")
                return -1
        except Exception as exc:
            self.utils.print_info(exc)
            return -1
        return 1

    def set_enable_auto_revert_option(self):
        """
        This function is used to set/check the `Reboot and revert Extreme Networks switch configuration if IQAgent is
        unresponsive after configuration update.` button under the `Upload configuration automatically` button
        from Advanced Settings tab
        :return: 1 - if the button is set successfully ; -1 - if not
        """
        try:
            switch_template = self.xiq.xflowsconfigureSwitchTemplate

            enable_auto_revert_message = switch_template.sw_template_web_elements.get_sw_template_auto_revert_msg().text
            if enable_auto_revert_message != "Reboot and revert Extreme Networks switch configuration if IQAgent is " \
                                             "unresponsive after configuration update.":
                self.utils.print_info(f"The Enable Auto Revert button name is not the correct one:"
                                      f" {enable_auto_revert_message}!")
                return -1

            enable_auto_revert = switch_template.sw_template_web_elements.get_sw_template_auto_revert_enabled()
            if not enable_auto_revert:
                self.utils.print_info("Enable Auto Revert button is not present!")
                return -1
            if not enable_auto_revert.is_selected():
                self.utils.print_info("Enable Auto Revert button is by default unchecked!")
            else:
                self.utils.print_info("Enable Auto Revert button is already checked!")
                return -1

            self.utils.print_info("Click on Enable Auto Revert button")
            self.auto_actions.click(enable_auto_revert)
        except Exception as exc:
            self.utils.print_info(exc)
            return -1
        return 1

    def save_template_with_popup(self):
        """
        This function is used to save the current device template with a pop-up displayed
        :return: 1 - if the save was successful ; -1 - if not
        """
        try:
            switch_template = self.xiq.xflowsconfigureSwitchTemplate
            save_template_button = switch_template.sw_template_web_elements.get_switch_temp_save_button()
            if not save_template_button.is_displayed():
                self.utils.print_info("SAVE button is not displayed")
                return -1

            self.utils.print_info("Click on SAVE button")
            self.auto_actions.click(save_template_button)

            sw_yes_button = switch_template.sw_template_web_elements.get_sw_template_notification_yes_btn()
            if not sw_yes_button.is_displayed():
                self.utils.print_info("YES button is not displayed")
                return -1

            self.utils.print_info("Click on SAVE button")
            self.auto_actions.click(sw_yes_button)
        except Exception as exc:
            self.utils.print_info(exc)
            return -1
        return 1

    def check_update_column_by_failure_message(self, device_serial, failure_message):
        """
        This function is used to check the UPDATED column from device grid from a device with device_serial given as
        parameter. Check if the update process failed with the same message as failure_message given as parameter
        :param device_serial: device serial number to check the config push status
        :param failure_message: failure message that is expected to appear after Device Update Failed
        :return: 1 - if the update process failed with the same message as failure_message ; -1 - if not
        """
        current_status = self.xiq.xflowscommonDevices.get_device_updated_status(device_serial=device_serial)
        count = 0
        max_wait = 900
        current_date = datetime.datetime.now()
        update_text = str(current_date).split()[0]

        while "Device Update Failed" != current_status:
            time.sleep(10)
            count += 10
            current_status = self.xiq.xflowscommonDevices.get_device_updated_status(device_serial=device_serial)
            self.utils.print_info(f"\nINFO \t Time elapsed in the Update process is '{count} seconds'\n")

            if update_text in current_status:
                self.utils.print_info("Update process ended up successfully!")
                return -1
            if count > max_wait:
                self.utils.print_info(f"Max time {max_wait} seconds exceeded")
                return -1

        current_message = \
            self.xiq.xflowscommonDevices.get_device_updated_fail_message_after_reboot(device_serial=device_serial,
                                                                                      ignore_failure=True)

        if failure_message != current_message:
            self.utils.print_info(f"Update process ended up with another failure message: {current_message}")
            return -1
        return 1

    def get_ip(self, dut):
        """
        This function is used to return an unresponsive ip address from the mgmt class to be used in testing
        iqagent unresponsive.
        :param : dut
        :return: ip
        """
        octet = 254
        try:
            while octet > 240:
                octet_str = str(octet)
                ip = '.'.join(dut.ip.split('.')[:-1] + [octet_str])
                if dut.platform == '5320':
                    output = self.devCmd.send_cmd(dut.name, f"ping vr VR-Default {ip}", max_wait=10)
                else:
                    output = self.devCmd.send_cmd(dut.name, f"ping vr VR-Mgmt {ip}", max_wait=10)
                if "Request timed out" in output[0].return_text:
                    self.utils.print_info("Ping failed. IP is usable.")
                    return ip
                else:
                    self.utils.print_info("Ping successfully. Making another try.")
                    octet = octet - 1
        except Exception as exc:
            self.utils.print_info(exc)
            return -1

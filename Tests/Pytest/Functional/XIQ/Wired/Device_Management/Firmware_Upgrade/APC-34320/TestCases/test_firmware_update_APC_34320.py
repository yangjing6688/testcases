# Author        :   Natarajan Periannan
# Description   :   APC-34320 - Extreme Firmware upgrade with and without network policy assigned to the devices
# Pre-Requests  :   Latest and four last supported firmware images should be copied to XIQ env prior to start this test.
#                   EXOS is having known bug EXOS-27245 which will often failed to download the image to device,
#                   if the device and the tftp server are in different locations. So it is recommended to run these
#                   tests when both XIQ environment and Testbeds are in the same geological location.
# Test Cases    :   TCXM_20120, TCXM_20121, TCXM_20122, TCXM_20123, TCXM_20124, TCXM_20125, TCXM_20677,
#                   TCXM-20112, TCXM-20113, TCXM-20114, TCXM-20115, TCXM-20116, TCXM-20117, TCXM-20676
# Comments      :   This test is applicable for EXOS, VOSS and EXOS_STACK
#                   Need to run two runlists to cover both policy and non policy cases.

import pytest
import re
import time


class Apc34320:

    def pre_check(self, node, enter_switch_cli, logger, test_case):
        """
        This method used to validate the EXOS Stack status and to clear the logs prior to start the test on EXOS
        """
        logger.info(f"Pre-check validation for the {test_case} is started...")
        time.sleep(60)
        with enter_switch_cli(node) as dev_cmd:
            if node.make.upper() == "EXOS":
                dev_cmd.send_cmd(node.name, 'show version', max_wait=10, interval=2)
                dev_cmd.send_cmd(node.name, 'show switch', max_wait=10, interval=2)
                dev_cmd.send_cmd(node.name, 'clear log static', max_wait=10, interval=2)
                if node.platform.upper() == 'STACK':
                    slot_count = len(node.serial.split(','))
                    result = dev_cmd.send_cmd(node.name, f'show switch | grep (Image Booted:)', max_wait=10, interval=2)
                    output = result[0].cmd_obj.return_text
                    pattern = f'(\s+Image Booted:\s+)(\w+)(\s+)(\w+)(\s+)'
                    match = re.search(pattern, output)
                    partition = match.group(2)
                    if slot_count > 1:
                        dev_cmd.send_cmd_verify_output(
                            node.name,
                            f'show slot | grep "Operational" | count',
                            f'Total lines: {slot_count}',
                            max_wait=10,
                            interval=2)
                        dev_cmd.send_cmd_verify_output(
                            node.name,
                            f'show slot detail | grep (Image Booted:\s+)({partition}) | count',
                            f'Total lines: {slot_count}',
                            max_wait=10,
                            interval=2)
                    else:
                        dev_cmd.send_cmd(node.name, 'show version images', max_wait=10, interval=2)
                        logger.fail(f"Pre-check validation for the {test_case} is failed!!!")
                        pytest.skip("Either all the slots are not in 'Operational' state or Images are booted from different partitions!!!")
            else:
                dev_cmd.send_cmd(node.name, 'show sys software | include Version', max_wait=10, interval=2)
                dev_cmd.send_cmd(node.name, 'clear logging', max_wait=10, interval=2)
            time.sleep(5)
            logger.info(f"Pre-check validation for the {test_case} is completed successfully!!!")

    def collect_logs(self, node, enter_switch_cli, logger, test_case):
        """
        This method used to collect the device logs in case of test case failed on EXOS and VOSS devices
        """
        logger.info(f"Log collection for the {test_case} is started...")
        with enter_switch_cli(node) as dev_cmd:
            if node.make.upper() == "EXOS":
                dev_cmd.send_cmd(node.name, 'show version', max_wait=10, interval=2)
                dev_cmd.send_cmd(node.name, 'show log', ignore_cli_feedback=True, max_wait=10, interval=2)
                dev_cmd.send_cmd(node.name, 'clear log static', max_wait=10, interval=2)
            else:
                dev_cmd.send_cmd(node.name, 'show sys software | include Version', max_wait=10, interval=2)
                dev_cmd.send_cmd(node.name, 'show logging file detail', ignore_cli_feedback=True, max_wait=10, interval=2)
                dev_cmd.send_cmd(node.name, 'clear logging', max_wait=10, interval=2)
            time.sleep(30)
            logger.info(f"Log collection for the {test_case} is completed successfully!")


@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.testbed_1_node
@pytest.mark.testbed_stack
class Apc34320Tests(Apc34320):

    @pytest.mark.tcxm_20120
    @pytest.mark.tcxm_20121
    @pytest.mark.tcxm_20123
    @pytest.mark.tcxm_20124
    @pytest.mark.tcxm_20122
    @pytest.mark.tcxm_20125
    @pytest.mark.tcxm_20112
    @pytest.mark.tcxm_20113
    @pytest.mark.tcxm_20115
    @pytest.mark.tcxm_20116
    @pytest.mark.tcxm_20114
    @pytest.mark.tcxm_20117
    @pytest.mark.p1
    def test_firmware_update (self, test_data, node, xiq_library_at_class_level, logger, enter_switch_cli):
        """
        TCXM-20120/20112  Verify the firmware upgrade function to the latest version even if versions are the same
        TCXM-20121/20113  Verify the firmware upgrade to the latest version without selecting the option perform upgrade
                          even if versions are same.
        TCXM-20123/20115  Verify the firmware upgrade for a specific version and perform upgrade with upgrade
                          even if versions are the same option selected.
        TCXM-20124/20116  Verify firmware upgrade to a specific firmware version and perform upgrade without upgrade
                          even if versions are same option.
        TCXM-20122/20114  Verify the firmware upgrade for the specific firmware version and perform upgrade but the versions
                          are not same
        TCXM-20125/20117  Verify the firmware upgrade button is present and can be launching the firmware upgrade window
                          from D360 page.
        """
        try:
            self.pre_check(node, enter_switch_cli, logger, test_data['tc'])
            xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(
                device_mac=node.mac,
                version=test_data['version'],
                forceDownloadImage=test_data['forceDownloadImage'],
                performUpgrade=test_data['performUpgrade'],
                updateTo=test_data['updateTo'],
                updatefromD360Page=test_data['updatefromD360Page'])
        finally:
            self.collect_logs(node, enter_switch_cli, logger, test_data['tc'])

    @pytest.mark.tcxm_20677
    @pytest.mark.tcxm_20676
    @pytest.mark.p2
    def test_validating_the_close_button_function(self, test_data, node, xiq_library_at_class_level):
        """
        TCXM-20677/20676  Verify the close button operation on the firmware update window
        """
        xiq_library_at_class_level.xflowscommonDevices.update_network_device_firmware(
            device_mac=node.mac,
            performUpgrade="false")
        

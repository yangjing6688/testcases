# Author        : Alexandru Prihotin
# Description   : XIQ-908 --> Provide customer option to reboot during configuration update
# Testcases     : TCXM_19668, TCXM_19669, TCXM_19671, TCXM_19672, TCXM_19677, TCXM_19678
# Comments      : These are the names of the EXOS test cases; all of the test cases apply for VOSS too.
# Modified by   : Ioana Cosmineanu

from pytest import mark
import pytest
import time


@pytest.fixture()
def xiq_teardown_device(request, test_bed, auto_actions, cli, suite_data, test_data, utils, logger, xiq_library_at_class_level, node, node_policy_name, node_template_name):
    def teardown():

        hang_cli_exos = "ping continuous 0.0.0.5"
        hang_cli_voss = "ping 0.0.0.5 -s mgmt"
        supplemental_cli_name_exos = "hang_cli_exos"
        supplemental_cli_name_voss = "hang_cli_voss"

        xiq_library_at_class_level.xflowscommonDevices.delete_device(device_mac=node.mac)
        device_1 = xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node)

        if device_1 != 1:
            logger.fail("There is a problem while onboarding device.. Initiating Cleanup...")

        time.sleep(20)
        cli.bounce_IQAgent(node)
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        time.sleep(20)

        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        online_device_1 = xiq_library_at_class_level.xflowscommonDevices. \
            wait_until_device_online(device_mac=node.mac)

        if online_device_1 != 1:
            logger.fail("Device didn't come online")

        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

        check_assigned_policy = xiq_library_at_class_level.xflowsmanageDevices.assign_network_policy_to_switch_mac(
            policy_name=node_policy_name, mac=node.mac)
        if check_assigned_policy == -1:
            pytest.fail("Can't assign network policy to device.")

        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        xiq_library_at_class_level.xflowscommonDevices.select_device(device_mac=node.mac)
        xiq_library_at_class_level.xflowscommonDevices._update_switch(update_method="PolicyAndConfig")

        online_device_1 = xiq_library_at_class_level.xflowscommonDevices. \
            wait_until_device_online(device_mac=node.mac)

        if online_device_1 != 1:
            logger.fail("Device didn't come online")

        if node.cli_type.lower() == "exos":
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node.mac))
            xiq_library_at_class_level.xflowsmanageDevice360.get_supplemental_cli(supplemental_cli_name_exos,
                                                                                  hang_cli_exos)
        else:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node.mac))
            xiq_library_at_class_level.xflowsmanageDevice360.get_supplemental_cli(supplemental_cli_name_voss,
                                                                                  hang_cli_voss)
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        time.sleep(5)

    request.addfinalizer(teardown)


@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.testbed_1_node
@pytest.mark.testbed_stack
@pytest.mark.p1
@pytest.mark.development
class Xiq908Tests:

    def _change_to_specific_version(self, logger, xiq, dut1, suite_data):

        try:
            if dut1.cli_type.lower() == 'voss':
                device_1 = xiq.xflowscommonDevices.update_network_device_firmware(
                    device_mac=dut1.mac,
                    version=suite_data["os_version_voss"],
                    updateTo=suite_data["os_version_voss"])
                logger.info(f"Device has {device_1} version")
            elif dut1.cli_type.lower() == 'exos':
                device_1 = xiq.xflowscommonDevices.update_network_device_firmware(
                    device_mac=dut1.mac,
                    version=suite_data["os_version_exos"],
                    updateTo=suite_data["os_version_exos"])
                logger.info(f"Device has {device_1} version")
            xiq.xflowsmanageDevices.wait_until_device_update_done(dut1.mac)
        except:
            try:
                xiq.xflowsmanageDevices.wait_until_device_update_done(dut1.mac)
            except:
                updated_status = xiq.xflowsmanageDevices.get_device_updated_status(
                    device_mac=dut1.mac)
                max_wait = 10
                count = 0
                while updated_status != "Device Update Failed" and count < max_wait:
                    time.sleep(2)
                    count += 1
                    updated_status = xiq.xflowsmanageDevices.get_device_updated_status(
                        device_mac=dut1.mac)
                    xiq.xflowsmanageDevice360.device360_refresh_page()
                if updated_status == "Device Update Failed":
                    logger.info(f"Device has finished updating with:  {updated_status}")
                    os_version = xiq.xflowsmanageDevices.get_device_row_values(dut1.mac, 'OS VERSION')
                    if os_version['OS VERSION'] == suite_data["os_version_voss"] or os_version['OS VERSION'] == suite_data["os_version_exos"]:
                        pass
                else:
                    logger.fail(f"Device has finished updating but with a failed condition: {updated_status}")

    @pytest.fixture(scope="class", autouse=True)
    def setup(self, xiq_library_at_class_level, network_manager, enter_switch_cli, cli, utils, logger, node):
        # these supplemental cli commands are needed in order to stretch the timeframe for other actions during config push
        hang_cli_exos = "ping continuous 0.0.0.5"
        hang_cli_voss = "ping 0.0.0.5 -s mgmt"
        supplemental_cli_name_exos = "hang_cli_exos"
        supplemental_cli_name_voss = "hang_cli_voss"
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

        xiq_library_at_class_level.xflowsglobalsettingsGlobalSetting.get_supplemental_cli_option("enable")
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

        if node.cli_type.lower() == "exos":
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node.mac))
            xiq_library_at_class_level.xflowsmanageDevice360.get_supplemental_cli(supplemental_cli_name_exos,
                                                                                  hang_cli_exos)
        else:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node.mac))
            xiq_library_at_class_level.xflowsmanageDevice360.get_supplemental_cli(supplemental_cli_name_voss,
                                                                                  hang_cli_voss)
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        time.sleep(5)

        try:
            network_manager.connect_to_network_element_name(node.name)
            network_manager.connect_to_network_element_name(node.name)
            with enter_switch_cli(node) as dev_cmd:
                dev_cmd.send_cmd(node.name, 'save config',
                                 max_wait=10,
                                 interval=2)
                online_device_1 = xiq_library_at_class_level.xflowscommonDevices. \
                    wait_until_device_online(device_mac=node.mac)

                if online_device_1 != 1:
                    logger.fail("Device didn't come online")
        finally:
            cli.close_connection_with_error_handling(node)

    @pytest.mark.tcxm_19668
    def test_TCXM_19668(self, xiq_teardown_device, logger, xiq_library_at_class_level, utils, node, node_policy_name,
                        auto_actions):
        """
        TCXM_19668 - Check that device license action is disabled while the device update is in progress
        TCXM_19671 - Check that reboot option is available during device update with configuration upgrade
        TCXM_19672 - Check that a config push fail event is created if device update is cancelled by rebooting
        """

        xiq_library_at_class_level.xflowsmanageDevices.get_update_devices_reboot_rollback(
            policy_name=node_policy_name,
            option='disable', device_mac=node.mac)
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

        xiq_library_at_class_level.xflowsmanageDevices.check_device_license_action(node.mac)

        xiq_library_at_class_level.xflowsmanageDevices.reboot_device_while_update(node.mac)
        time.sleep(10)
        try:
            assert xiq_library_at_class_level.xflowsmanageDevice360.get_event_from_device360(dut=node,
                                                                                             event="Configuration update process is canceled by the us",
                                                                                             close_360_window=True,
                                                                                             configuration_event=True) == 1, \
                "FAIL! Did not find the configuration event"

        except:
            time.sleep(10)
            auto_actions.click(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_refresh_page_button())
            time.sleep(5)
            assert xiq_library_at_class_level.xflowsmanageDevice360.get_event_from_device360(dut=node,
                                                                                             event="Configuration update process is canceled by the us",
                                                                                             close_360_window=True,
                                                                                             configuration_event=True) == 1, \
                "Did not find the configuration event"

        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        xiq_library_at_class_level.xflowsmanageDevices.wait_until_device_update_done(node.mac)

    @pytest.mark.tcxm_19669
    def test_TCXM_19669(self, xiq_teardown_device, xiq_library_at_class_level, suite_data, test_data, logger, utils,
                        node):
        """
        TCXM_19669 - Check if reboot option is disabled during device update with image upgrade
        """

        logger.info("For an efficient and correct running of the automation tests, it is necessary to have the image "
                    "versions 8.8.2.0 for voss and 32.2.1.8 for exos. These in addition to the latest versions.")
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

        os_version = xiq_library_at_class_level.xflowsmanageDevices.get_device_row_values(node.mac, 'OS VERSION')

        if os_version['OS VERSION'] == suite_data["os_version_voss"] or os_version['OS VERSION'] == suite_data[
            "os_version_exos"]:
            xiq_library_at_class_level.xflowsmanageDevices.update_device_policy_image(node.mac)
        else:
            self._change_to_specific_version(logger, xiq_library_at_class_level, node, suite_data)
            xiq_library_at_class_level.xflowsmanageDevices.update_device_policy_image(node.mac)

        time.sleep(5)
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        assert xiq_library_at_class_level.xflowsmanageDevices.check_device_reboot_action(node.mac) == 1, \
            "Failed! Reboot action is present"

        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        try:
            xiq_library_at_class_level.xflowsmanageDevices.wait_until_device_update_done(node.mac)
        except:
            updated_status = xiq_library_at_class_level.xflowsmanageDevices.get_device_updated_status(
                device_mac=node.mac)
            max_wait = 10
            count = 0
            while updated_status != "Device Update Failed" and count < max_wait:
                time.sleep(2)
                count += 1
                updated_status = xiq_library_at_class_level.xflowsmanageDevices.get_device_updated_status(
                    device_mac=node.mac)
                utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
            if updated_status == "Device Update Failed":
                logger.info(f"Device has finished updating with:  {updated_status}")
            else:
                logger.info(f"Device has finished updating but with a failed condition: {updated_status}")

    @mark.tcxm_19671
    @pytest.mark.dependson("tcxm_19668")
    def test_TCXM_19671(self, logger):

        logger.info("TestCase TCXM_19671 is covered in TCXM_19668")

    @mark.tcxm_19672
    @pytest.mark.dependson("tcxm_19668")
    def test_TCXM_19672(self, logger):

        logger.info("TestCase TCXM_19672 is covered in TCXM_19668")

    @mark.tcxm_19677
    def test_TCXM_19677(self, xiq_teardown_device, xiq_library_at_class_level, utils, node, node_policy_name):
        """
        TCXM_19677 - Check that reboot option is available while device update with reboot option enabled
        """

        xiq_library_at_class_level.xflowscommonDevices.get_update_devices_reboot_rollback(
            policy_name=node_policy_name, option='enable',
            device_mac=node.mac,
            device_serial=node.mac)

        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        time.sleep(5)
        xiq_library_at_class_level.xflowsmanageDevices.reboot_device_while_update(node.mac)

        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        xiq_library_at_class_level.xflowsmanageDevices.wait_until_device_update_done(node.mac)

    @mark.tcxm_19678
    def test_TCXM_19678(self, xiq_teardown_device, xiq_library_at_class_level, utils, node, logger, suite_data,
                        test_data):
        """
        TCXM_19678 - Check that reboot option is disabled while device update with configuration upgrade and image
        upgrade
        """

        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        self._change_to_specific_version(logger, xiq_library_at_class_level, node, suite_data)
        xiq_library_at_class_level.xflowsmanageDevices.update_device_policy_config_image(device_serial=node.mac)
        time.sleep(5)
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        time.sleep(5)
        assert xiq_library_at_class_level.xflowsmanageDevices.check_device_reboot_action(
            device_serial=node.mac) == 1, \
            "Fail! Reboot action is present"

        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        try:
            xiq_library_at_class_level.xflowsmanageDevices.wait_until_device_update_done(node.mac)
        except:
            updated_status = xiq_library_at_class_level.xflowsmanageDevices.get_device_updated_status(
                device_mac=node.mac)
            max_wait = 10
            count = 0
            while updated_status != "Device Update Failed" and count < max_wait:
                time.sleep(2)
                count += 1
                updated_status = xiq_library_at_class_level.xflowsmanageDevices.get_device_updated_status(
                    device_mac=node.mac)
                utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page, delay=2)
            if updated_status == "Device Update Failed":
                logger.info(f"Device has finished updating with:  {updated_status}")
            else:
                logger.info(f"Device has finished updating but with a failed condition: {updated_status}")

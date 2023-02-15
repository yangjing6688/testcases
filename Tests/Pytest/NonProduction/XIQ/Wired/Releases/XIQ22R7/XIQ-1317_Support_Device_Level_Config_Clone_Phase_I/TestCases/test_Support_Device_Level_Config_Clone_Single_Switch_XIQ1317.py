# Author        : Dragos Sofiea
# Title         : Support Device Level Config Clone Single Switch Engine (EXOS)/Fabric Engine (VOSS) Phase I
# Description   : This script run the below tests for clone switch configuration feature according with XIQ-1317 story
# Testcases     : TCXM-22475, TCXM-22472, TCXM-22474, TCXM-22483, TCXM-22480, TCXM-22482, TXCM-22481,
#                 TCXM-22479, TCXM-22476, TCXM-22478, TCXM-22477
# Comments      : This test is applicable for 2_node (VOSS, EXOS)
import pytest
import random
import string


def random_word(x=5):
    randword = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(x))
    return randword


def rand_numbers():
    numbers = random.sample(range(3, 20), 5)
    numbers.sort()
    string_numbers = ','.join(str(x) for x in numbers)
    return string_numbers


port_type_exos_access = 'Port_type_exos_access_' + random_word()
port_type_exos_trunk = 'Port_type_exos_trunk_' + random_word()
port_type_voss_access = 'Port_type_voss_access_' + random_word()
port_type_voss_trunk = 'Port_type_voss_trunk_' + random_word()
port_type_exos_teardown = 'Port_type_exos_teardown'
port_numbers = rand_numbers()

template_exos_access = {'name': [port_type_exos_access, port_type_exos_access],
                        'description': [None, None],
                        'status': [None, 'on'],
                        'port usage': ['access port', 'access'],
                        'page2 accessVlanPage': ['next_page', None],
                        'vlan': ['2', '2'],
                        'page3 transmissionSettings': ["next_page", None],
                        'transmission type': ['Full-Duplex', 'Full-Duplex'],
                        'transmission speed': ['100 Mbps', '100'],
                        'page4 stp': ["next_page", None],
                        'page5 stormControlSettings': ["next_page", None],
                        'page6 MACLOCKINGSettingsPage': ["next_page", None],
                        'mac locking': ["click", "On"],
                        'max first arrival': ["20", "20"],
                        'page7 ELRPSettingsPage': ["next_page", None],
                        'elrp status': ["click", "enabled"],
                        'page8 pseSettings': ["next_page", None],
                        'page9 summary': ["next_page", None]
                        }

template_voss_access = {'name': [port_type_voss_access, port_type_voss_access],
                        'description': [None, None],
                        'status': [None, 'on'],
                        'auto-sense': ['click', None],
                        'port usage': ['access port', 'access'],
                        'page2 accessVlanPage': ['next_page', None],
                        'vlan': ['2', '2'],
                        'page3 transmissionSettings': ["next_page", None],
                        'transmission type': ['Full-Duplex', 'Full-Duplex'],
                        'transmission speed': ['100 Mbps', '100'],
                        'page4 stp': ["next_page", None],
                        'page5 stormControlSettings': ["next_page", None],
                        'page6 pseSettings': ["next_page", None],
                        'page7 summary': ["next_page", None]
                        }

template_exos_trunk = {'name': [port_type_exos_trunk, port_type_exos_trunk],
                       'description': [None, None],
                       'status': [None, 'on'],
                       'port usage': ['trunk port', 'TRUNK'],
                       'page2 trunkVlanPage': ['next_page', None],
                       'native vlan': ['3', '3'],
                       'page3 transmissionSettings': ["next_page", None],
                       'transmission type': ['Full-Duplex', 'Full-Duplex'],
                       'transmission speed': ['100 Mbps', '100'],
                       'page4 stp': ["next_page", None],
                       'page5 stormControlSettings': ["next_page", None],
                       'page6 MACLOCKINGSettingsPage': ["next_page", None],
                       'page7 ELRPSettingsPage': ["next_page", None],
                       'page8 pseSettings': ["next_page", None],
                       'page9 summary': ["next_page", None]
                       }

template_voss_trunk = {'name': [port_type_voss_trunk, port_type_voss_trunk],
                       'description': [None, None],
                       'status': [None, 'on'],
                       'port usage': ['trunk port', 'TRUNK'],
                       'page2 trunkVlanPage': ['next_page', None],
                       'native vlan': ['3', '3'],
                       'page3 transmissionSettings': ["next_page", None],
                       'transmission type': ['Full-Duplex', 'Full-Duplex'],
                       'transmission speed': ['100 Mbps', '100'],
                       'page4 stp': ["next_page", None],
                       'page5 stormControlSettings': ["next_page", None],
                       'page6 pseSettings': ["next_page", None],
                       'page7 summary': ["next_page", None]
                       }
template_exos_teardown = 'Access Port'
template_voss_teardown = 'Auto-sense Port'


@pytest.fixture()
def xiq_teardown_template(request, utils, logger, xiq_library_at_class_level, node_1, node_2, node_1_policy_name, node_1_template_name, node_2_policy_name, node_2_template_name):
    network_policy_name = node_1_policy_name
    sw_template_name = node_1_template_name

    def teardown():
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                    sw_template_name)
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        if node_1.cli_type == 'exos':
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate. \
                template_assign_ports_to_an_existing_port_type(port_numbers,
                                                               template_exos_teardown)
        elif node_1.cli_type == 'voss':
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate. \
                template_assign_ports_to_an_existing_port_type(port_numbers,
                                                               template_voss_teardown)
        # Update default config for cloning device
        xiq_library_at_class_level.xflowscommonDevices. \
            get_update_devices_reboot_rollback(policy_name=network_policy_name,
                                               option="disable",
                                               device_mac=node_1.mac)

        xiq_library_at_class_level.xflowsmanageDevices. \
            check_device_update_status_by_using_mac(node_1.mac)

        # Clone the replacement device
        xiq_library_at_class_level.xflowsmanageDevices.select_clone_device(device_serial=node_1.serial,
                                                                     replacement_device_type="Onboarded",
                                                                     replacement_serial=node_2.serial)
        xiq_library_at_class_level.xflowsmanageDevices. \
            check_device_update_status_by_using_mac(node_2.mac)

        xiq_library_at_class_level.xflowscommonDevices.delete_device(device_mac=node_1.mac)
        xiq_library_at_class_level.xflowscommonDevices.delete_device(device_mac=node_2.mac)

        solo_serial_1 = node_1.serial.split(',')
        for eachdevice in solo_serial_1:
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=eachdevice)
        solo_serial_2 = node_2.serial.split(',')
        for eachdevice in solo_serial_2:
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=eachdevice)

        device_1 = xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_1)

        device_2 = xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_2)

        if device_1 != 1 and device_2 != 1:
            logger.fail("There is a problem while onboarding devices.. Initiating Cleanup...")

        online_device_1 = xiq_library_at_class_level.xflowscommonDevices.\
            wait_until_device_online(device_mac=node_1.mac)
        online_device_2 = xiq_library_at_class_level.xflowscommonDevices.\
            wait_until_device_online(device_mac=node_2.mac)

        if online_device_1 != 1 and online_device_2 != 1:
            logger.fail("Device didn't come online")

        xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(policy_name=network_policy_name,
                                                                         mac=node_1.mac)
    request.addfinalizer(teardown)


@pytest.mark.p1
@pytest.mark.testbed_2_node
@pytest.mark.development
@pytest.mark.dependson("tcxm_xiq_onboarding")
class Xiq1317Tests:

    def _change_to_same(self, logger, xiq, dut1, dut2):

        try:
            device_1 = xiq.xflowscommonDevices.update_network_device_firmware(
                device_mac=dut1.mac)
            device_2 = xiq.xflowscommonDevices.update_network_device_firmware(
                device_mac=dut2.mac)
            if device_1 == device_2:
                logger.info("Devices have the same OS versions")
            else:
                logger.fail("Devices still don't have the same versions")
        except:
            logger.fail("Problem in updating the firmware")

    def _change_to_different(self, logger, xiq, dut1, suite_data):

        try:
            if dut1.cli_type.lower() == 'voss':
                device_1 = xiq.xflowscommonDevices.update_network_device_firmware(
                    device_mac=dut1.mac,
                    version=suite_data["os_version_voss"],
                    updateTo=suite_data["os_version_voss"])
                logger.info(f"Clone device has {device_1} version")
            elif dut1.cli_type.lower() == 'exos':
                device_1 = xiq.xflowscommonDevices.update_network_device_firmware(
                    device_mac=dut1.mac,
                    version=suite_data["os_version_exos"],
                    updateTo=suite_data["os_version_exos"])
                logger.info(f"Clone device has {device_1} version")
        except:
            logger.fail("Problem in updating the firmware")

    @pytest.fixture(scope="class", autouse=True)
    def setup(self, logger, network_manager, utils, xiq_library_at_class_level, cli, node_1, node_2, node_1_policy_name, node_1_template_name, node_2_policy_name, node_2_template_name):
        network_policy_name = node_1_policy_name
        sw_template_name = node_1_template_name
        try:
            network_manager.connect_to_network_element_name(node_1.name)
            network_manager.connect_to_network_element_name(node_2.name)

            device1_model_1 = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.generate_template_name(
                platform=node_1.cli_type, serial=node_1.serial, model=node_1.model)
            device1_model = device1_model_1[0]
            logger.info(f"device1_model: {device1_model}")

            device2_model_2 = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.generate_template_name(
                platform=node_2.cli_type, serial=node_2.serial, model=node_2.model)
            device2_model = device2_model_2[0]
            logger.info(f"device2_model: {device2_model}")

            if device1_model == device2_model:
                logger.info("Devices are the same")
            else:
                pytest.skip("Devices are not the same")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                        sw_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()

            # Create port type profiles trunk and access
            if node_1.cli_type == 'exos':
                create_new_port_type_access = xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(template_exos_access,
                                                                                                 port_numbers.split(',')
                                                                                                 [0])
                create_new_port_type_trunk = xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(template_exos_trunk,
                                                                                                port_numbers.split(',')
                                                                                                [0])
                if create_new_port_type_access != 1 or create_new_port_type_trunk != 1:
                    logger.fail("Problem in creating the port type profiles")
            elif node_1.cli_type == 'voss':
                create_new_port_type_access = xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(template_voss_access,
                                                                                                 port_numbers.split(',')
                                                                                                 [0])
                create_new_port_type_trunk = xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(template_voss_trunk,
                                                                                                port_numbers.split(',')
                                                                                                [0])
                if create_new_port_type_access != 1 or create_new_port_type_trunk != 1:
                    logger.fail("Problem in creating the port type profiles")
            yield
        finally:
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name, sw_template_name)

            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.revert_port_configuration_template_level("Access Port")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.switch_template_save()
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            res = xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_exos(serial=node_1.serial)
            assert res == 1, f"Failed to update network policy to the device"

            # Delete the port type created
            if node_1.cli_type == 'exos':
                xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_port_type_profile(template_exos_access)
                xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_port_type_profile(template_exos_trunk)
            elif node_1.cli_type == 'voss':
                xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_port_type_profile(template_voss_access)
                xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_port_type_profile(template_voss_trunk)
            cli.close_connection_with_error_handling(node_1)
            cli.close_connection_with_error_handling(node_2)
            xiq_library_at_class_level.login.logout_user()
            xiq_library_at_class_level.login.quit_browser()

    @pytest.mark.tcxm_22472
    @pytest.mark.p1
    def test_replacement_cloning_same_os_txcm22472(self, logger, cli, xiq_teardown_template, xiq_library_at_class_level, node_1, node_2, node_1_policy_name, node_1_template_name):
        """TCXM-22475-Check Clone Device function lists the replacement device if it is onboarded and connected to XIQ.
        Select a replacement device and initiate the Cloning Operation."""
        """TCXM-22472 - Check Clone Device page has Replacement Device drop down menu if "Onboarded" is selected then
        "Replacement Serials" should list the matching serials that are already onboarded and connected"""

        logger.info("For an efficient and correct running of the automation tests, it is necessary to have the image versions 8.8.0.0 for voss and 31.7.1.4 for exos. These in addition to the latest versions.")
        network_policy_name = node_1_policy_name
        sw_template_name = node_1_template_name
        os_versions = cli.check_os_versions(dut1=node_1, dut2=node_2)

        # Check if devices have same or different os versions
        if os_versions == 'different':
            self._change_to_same(logger, xiq_library_at_class_level, node_1, node_2)
        elif os_versions == 'same':
            logger.info("Devices have the same OS versions")
            pass

        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                    sw_template_name)
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()

        # Create port type
        if node_1.cli_type == 'exos':
            # Assign port type to ports
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                  port_type_exos_access)
        elif node_1.cli_type == 'voss':
            # Assign port type to ports
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                  port_type_voss_access)
        # Configure CLI logs from XIQ
        cli.configure_cli_table(dut1=node_1, dut2=node_2)

        # Update config for cloning device
        xiq_library_at_class_level.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=network_policy_name, option="disable", device_mac=node_1.mac)
        xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_1.mac)

        # Clone the replacement device
        xiq_library_at_class_level.xflowsmanageDevices.select_clone_device(device_serial=node_1.serial,
                                                         replacement_device_type="Onboarded",
                                                         replacement_serial=node_2.serial)
        xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_2.mac)
        
        # Check cli commands are the same
        cli.check_clone_configuration(dut1=node_1, dut2=node_2)

    @pytest.mark.p1
    @pytest.mark.tcxm_22475
    @pytest.mark.dependson("tcxm_22472")
    def test_replacement_cloning_same_os_txcm22475(self, logger):

        logger.info("For an efficient and correct running of the automation tests, it is necessary to have the image versions 8.8.0.0 for voss and 31.7.1.4 for exos. These in addition to the latest versions.")
        logger.info("TestCase TCXM-22475 is covered in TCXM-22472")

    @pytest.mark.p1
    @pytest.mark.tcxm_22474
    def test_replacement_cloning_same_os_unmanaged_txcm_22474(self, logger, cli, xiq_teardown_template, xiq_library_at_class_level, node_1, node_2, node_1_policy_name, node_1_template_name, node_2_policy_name, node_2_template_name):
        """TCXM-22474-Check Clone Device function is available even the original device is onboarded but unmanaged in XIQ
        Select a replacement device and initiate the Cloning Operation."""
        network_policy_name = node_1_policy_name
        sw_template_name = node_1_template_name

        logger.info("For an efficient and correct running of the automation tests, it is necessary to have the image versions 8.8.0.0 for voss and 31.7.1.4 for exos. These in addition to the latest versions.")

        os_versions = cli.check_os_versions(dut1=node_1, dut2=node_2)

        # Check if devices have same or different os versions
        if os_versions == 'different':
            self._change_to_same(logger, xiq_library_at_class_level, node_1, node_2)
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                    sw_template_name)
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()

        # Create port type
        if node_1.cli_type == 'exos':
            # Assign port type to ports
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                  port_type_exos_trunk)
        elif node_1.cli_type == 'voss':
            # Assign port type to ports
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                  port_type_voss_trunk)
        # Configure CLI logs from XIQ
        cli.configure_cli_table(dut1=node_1, dut2=node_2)

        # Update config for cloning device
        xiq_library_at_class_level.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=network_policy_name,option="disable",device_mac=node_1.mac)
        xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_1.mac)

        # Put the cloning device in unmanaged state
        xiq_library_at_class_level.xflowsmanageDevices.change_manage_device_status(manage_type='UNMANAGE', device_mac=node_1.mac)

        # Clone the replacement device
        xiq_library_at_class_level.xflowsmanageDevices.select_clone_device(device_serial=node_1.serial,
                                                         replacement_device_type="Onboarded",
                                                         replacement_serial=node_2.serial)
        xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_2.mac)

        # Check cli commands are the same
        try:
            cli.check_clone_configuration(dut1=node_1, dut2=node_2)
        finally:
        # Change back the cloning device to managed state
            xiq_library_at_class_level.xflowsmanageDevices.change_manage_device_status(device_mac=node_1.mac)

    @pytest.mark.p1
    @pytest.mark.tcxm_22473
    def test_replacement_cloning_same_os_disconnected_txcm_22473(self, logger, cli, xiq_teardown_template, xiq_library_at_class_level, node_1, node_2, node_1_policy_name, node_1_template_name, node_2_policy_name, node_2_template_name, loaded_config):
        """TCXM-22473 - Check Clone Device function is available even if the original device is not connected to the XIQ
        Select a replacement device and initiate the Cloning Operation."""
        network_policy_name = node_1_policy_name
        sw_template_name = node_1_template_name

        logger.info("For an efficient and correct running of the automation tests, it is necessary to have the image versions 8.8.0.0 for voss and 31.7.1.4 for exos. These in addition to the latest versions.")

        os_versions = cli.check_os_versions(dut1=node_1, dut2=node_2)

        # Check if devices have same or different os versions
        if os_versions == 'different':
            self._change_to_same(logger, xiq_library_at_class_level, node_1, node_2)
        # Select switch template
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                    sw_template_name)
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()

        # Create port type
        if node_1.cli_type == 'exos':
            # Assign port type to ports
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                  port_type_exos_trunk)
        elif node_1.cli_type == 'voss':
            # Assign port type to ports
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                  port_type_voss_trunk)
        # Configure CLI logs from XIQ
        cli.configure_cli_table(dut1=node_1, dut2=node_2)

        # Update config for cloning device
        xiq_library_at_class_level.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=network_policy_name, option="disable", device_mac=node_1.mac)
        xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_1.mac)

        # Disconnect the cloning device from XIQ
        cli.disable_enable_iqagent_clone_device(device=node_1, iqagent_option='disable')

        # Clone the replacement device
        xiq_library_at_class_level.xflowsmanageDevices.select_clone_device(device_serial=node_1.serial,
                                                         replacement_device_type="Onboarded",
                                                         replacement_serial=node_2.serial)
        xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_2.mac)
        # Check cli commands are the same
        try:
            cli.check_clone_configuration(dut1=node_1, dut2=node_2)
        # Connect back the cloning device to XIQ
        finally:
            cli.disable_enable_iqagent_clone_device(device=node_1, iqagent_option='enable')
            connection = cli.open_spawn(node_1.ip, node_1.port, node_1.username, node_1.password, node_1.cli_type)
            cli.wait_for_configure_device_to_connect_to_cloud(cli_type=node_1.cli_type, server_name=loaded_config['sw_connection_host'], connection= connection, retry_count=30)

    @pytest.mark.p1
    @pytest.mark.tcxm_22480
    def test_replacement_cloning_policy_txcm22480(self, utils, cli, suite_data, test_data, logger, xiq_teardown_template, xiq_library_at_class_level, node_1, node_2, node_1_policy_name, node_1_template_name, node_2_policy_name, node_2_template_name):
        """TCXM-22480 - Check Clone Device page has Replacement Device drop down menu if "Onboarded" is selected then
        "Replacement Serials" should list the matching serials that are already onboarded and connected"""
        """TCXM-22483 - Check Clone Device function lists the replacement device if it is onboarded and connected to XIQ.
        Select a replacement device and initiate the Cloning Operation."""

        policy_default = node_2_policy_name
        network_policy_name = node_1_policy_name
        sw_template_name = node_1_template_name

        logger.info("For an efficient and correct running of the automation tests, it is necessary to have the image versions 8.8.0.0 for voss and 31.7.1.4 for exos. These in addition to the latest versions.")

        def _checks():
            # Assign a default policy for replacement
            xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(policy_name=policy_default,
                                                                             mac=node_2.mac)
            # Select switch template
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                        sw_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            # Create port type
            if node_1.cli_type == 'exos':
                # Assign port type to ports
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                      port_type_exos_access)
            elif node_1.cli_type == 'voss':
                # Assign port type to ports
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                      port_type_voss_access)

            # Configure CLI logs from XIQ
            cli.configure_cli_table(dut1=node_1, dut2=node_2)
            # Update config for cloning device
            xiq_library_at_class_level.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=network_policy_name, option="disable", device_mac=node_1.mac)
            xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_1.mac)

            # Clone the replacement device
            xiq_library_at_class_level.xflowsmanageDevices.select_clone_device(device_serial=node_1.serial,
                                                             replacement_device_type="Onboarded",
                                                             replacement_serial=node_2.serial)
            xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_2.mac)
            # Check cli commands are the same
            cli.check_clone_configuration(dut1=node_1, dut2=node_2)

        os_versions = cli.check_os_versions(dut1=node_1, dut2=node_2)

        # Check if devices have same or different os versions
        if os_versions == 'different':
            _checks()
            self._change_to_same(logger, xiq_library_at_class_level, node_1, node_2)
            _checks()

        elif os_versions == 'same':
            _checks()
            self._change_to_different(logger, xiq_library_at_class_level, node_1, suite_data)
            _checks()

    @pytest.mark.p1
    @pytest.mark.tcxm_22483
    @pytest.mark.dependson("tcxm_22480")
    def test_replacement_cloning_policy_txcm22483(self, logger, xiq_teardown_template):

        logger.info("For an efficient and correct running of the automation tests, it is necessary to have the image versions 8.8.0.0 for voss and 31.7.1.4 for exos. These in addition to the latest versions.")
        logger.info("TestCase TCXM-22483 is covered in TCXM-22480")

    @pytest.mark.p1
    @pytest.mark.tcxm_22482
    def test_replacement_cloning_policy_unmanaged_txcm_22482(self, logger, cli, suite_data, test_data, xiq_teardown_template, xiq_library_at_class_level, node_1, node_2, node_1_policy_name, node_1_template_name, node_2_policy_name, node_2_template_name):
        """TCXM-22482 - Check Clone Device function is available even the original device is onboarded but unmanaged in XIQ
        Select a replacement device and initiate the Cloning Operation."""
        policy_default = node_2_policy_name
        network_policy_name = node_1_policy_name
        sw_template_name = node_1_template_name

        logger.info("For an efficient and correct running of the automation tests, it is necessary to have the image versions 8.8.0.0 for voss and 31.7.1.4 for exos. These in addition to the latest versions.")

        def _checks():
            # Assign a default policy for replacement
            xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(policy_name=policy_default,
                                                                             mac=node_2.mac)
            # Select switch template
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                        sw_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            # Create port type
            if node_1.cli_type == 'exos':
                # Assign port type to ports
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                      port_type_exos_trunk)
            elif node_1.cli_type == 'voss':
                # Assign port type to ports
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                      port_type_voss_trunk)
            # Configure CLI logs from XIQ
            cli.configure_cli_table(dut1=node_1, dut2=node_2)

            # Update config for cloning device
            xiq_library_at_class_level.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=network_policy_name, option="disable", device_mac=node_1.mac)
            xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_1.mac)

            # Put the cloning device in unmanaged state
            xiq_library_at_class_level.xflowsmanageDevices.change_manage_device_status(manage_type='UNMANAGE',
                                                                     device_mac=node_1.mac)
            # Clone the replacement device
            xiq_library_at_class_level.xflowsmanageDevices.select_clone_device(device_serial=node_1.serial,
                                                             replacement_device_type="Onboarded",
                                                             replacement_serial=node_2.serial)
            xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_2.mac)

            # Check cli commands are the same
            try:
                cli.check_clone_configuration(dut1=node_1, dut2=node_2)
            # Change back the cloning device to managed state
            finally:
                xiq_library_at_class_level.xflowsmanageDevices.change_manage_device_status(device_mac=node_1.mac)

        os_versions = cli.check_os_versions(dut1=node_1, dut2=node_2)

        # Check if devices have same or different os versions
        if os_versions == 'different':
            self._change_to_same(logger, xiq_library_at_class_level, node_1, node_2)
            _checks()
            self._change_to_different(logger, xiq_library_at_class_level, node_1, suite_data)
            _checks()

        elif os_versions == 'same':
            _checks()
            self._change_to_different(logger, xiq_library_at_class_level, node_1, suite_data)
            _checks()

    @pytest.mark.p1
    @pytest.mark.tcxm_22481
    def test_replacement_cloning_policy_disconnected_txcm_22481(self, logger, cli, suite_data, test_data, xiq_teardown_template, xiq_library_at_class_level, node_1, node_2, node_1_policy_name, node_1_template_name, node_2_policy_name, node_2_template_name, loaded_config):
        """TXCM-22481 - Check Clone Device function is available even if the original device is not connected to the XIQ
        Select a replacement device and initiate the Cloning Operation."""
        policy_default = node_2_policy_name
        network_policy_name = node_1_policy_name
        sw_template_name = node_1_template_name

        logger.info("For an efficient and correct running of the automation tests, it is necessary to have the image versions 8.8.0.0 for voss and 31.7.1.4 for exos. These in addition to the latest versions.")

        def _checks():
            # Assign a default policy for replacement
            xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(policy_name=policy_default,
                                                                             mac=node_2.mac)

            # Select switch template
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                        sw_template_name)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()

            # Create port type
            if node_1.cli_type == 'exos':
                # Assign port type to ports
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                      port_type_exos_trunk)
            elif node_1.cli_type == 'voss':
                # Assign port type to ports
                xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                      port_type_voss_trunk)
            else:
                logger.fail("Didn't find any os type")

            # Configure CLI logs from XIQ
            cli.configure_cli_table(dut1=node_1, dut2=node_2)

            # Update config for cloning device
            xiq_library_at_class_level.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=network_policy_name, option="disable", device_mac=node_1.mac)
            xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_1.mac)

            # Disconnect the cloning device from XIQ
            cli.disable_enable_iqagent_clone_device(device=node_1, iqagent_option='disable')

            # Clone the replacement device
            xiq_library_at_class_level.xflowsmanageDevices.select_clone_device(device_serial=node_1.serial,
                                                             replacement_device_type="Onboarded",
                                                             replacement_serial=node_2.serial)
            xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_2.mac)

            # Check cli commands are the same
            try:
                cli.check_clone_configuration(dut1=node_1, dut2=node_2)
            # Connect back the cloning device to XIQ
            finally:
                cli.disable_enable_iqagent_clone_device(device=node_1, iqagent_option='enable')
                connection = cli.open_spawn(node_1.ip, node_1.port, node_1.username,
                                                    node_1.password, node_1.cli_type)
                cli.wait_for_configure_device_to_connect_to_cloud(cli_type=node_1.cli_type,
                                                                        server_name=loaded_config['sw_connection_host'],
                                                                        connection=connection, retry_count=30)

        os_versions = cli.check_os_versions(dut1=node_1, dut2=node_2)

        # Check if devices have same or different os versions
        if os_versions == 'different':
            self._change_to_same(logger, xiq_library_at_class_level, node_1, node_2)
            _checks()
            self._change_to_different(logger, xiq_library_at_class_level, node_1, suite_data)
            _checks()

        elif os_versions == 'same':
            _checks()
            self._change_to_different(logger, xiq_library_at_class_level, node_1, suite_data)
            _checks()

    @pytest.mark.p1
    @pytest.mark.tcxm_22476
    def test_replacement_cloning_different_os_txcm22476(self, logger, cli, suite_data, test_data, xiq_teardown_template, xiq_library_at_class_level, node_1, node_2, node_1_policy_name, node_1_template_name, node_2_policy_name, node_2_template_name):
        """TCXM-22479 - Check Clone Device function lists the replacement device if it is onboarded and connected to XIQ.
        Select a replacement device and initiate the Cloning Operation."""
        """TCXM-22476 - Check Clone Device page has Replacement Device drop down menu if "Onboarded" is selected then
        "Replacement Serials" should list the matching serials that are already onboarded and connected"""
        network_policy_name = node_1_policy_name
        sw_template_name = node_1_template_name
        os_versions = cli.check_os_versions(dut1=node_1, dut2=node_2)

        logger.info("For an efficient and correct running of the automation tests, it is necessary to have the image versions 8.8.0.0 for voss and 31.7.1.4 for exos. These in addition to the latest versions.")

        # Check if devices have same or different os versions
        if os_versions == 'same':
            self._change_to_different(logger, xiq_library_at_class_level, node_1, suite_data)
        elif os_versions == 'different':
            logger.info("Devices have different OS versions")
            pass

        # Select switch template
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                    sw_template_name)
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()

        # Create port type
        if node_1.cli_type == 'exos':
            # Assign port type to ports
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                  port_type_exos_access)
        elif node_1.cli_type == 'voss':
            # Assign port type to ports
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                  port_type_voss_access)
        # Configure CLI logs from XIQ
        cli.configure_cli_table(dut1=node_1, dut2=node_2)

        # Update config for cloning device
        xiq_library_at_class_level.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=network_policy_name, option="disable", device_mac=node_1.mac)
        xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_1.mac)

        # Clone the replacement device
        xiq_library_at_class_level.xflowsmanageDevices.select_clone_device(device_serial=node_1.serial,
                                                         replacement_device_type="Onboarded",
                                                         replacement_serial=node_2.serial)
        xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_2.mac)

        # Check cli commands are the same
        cli.check_clone_configuration(dut1=node_1, dut2=node_2)

    @pytest.mark.p1
    @pytest.mark.tcxm_22479
    @pytest.mark.dependson("tcxm_22476")
    def test_replacement_cloning_different_os_txcm22479(self, logger, xiq_teardown_template):

        logger.info("For an efficient and correct running of the automation tests, it is necessary to have the image "
                    "versions 8.8.0.0 for voss and 31.7.1.4 for exos. These in addition to the latest versions.")
        logger.info("TestCase TCXM-22479 is covered in TCXM-22476")

    @pytest.mark.p1
    @pytest.mark.tcxm_22478
    def test_replacement_cloning_different_os_unmanaged_txcm_22478(self, logger, cli, xiq_teardown_template, xiq_library_at_class_level, node_1, node_2, node_1_policy_name, node_1_template_name, node_2_policy_name, node_2_template_name):
        """TCXM-22478 - Check Clone Device function is available even the original device is onboarded but unmanaged in XIQ
        Select a replacement device and initiate the Cloning Operation."""
        network_policy_name = node_1_policy_name
        sw_template_name = node_1_template_name

        logger.info("For an efficient and correct running of the automation tests, it is necessary to have the image "
                    "versions 8.8.0.0 for voss and 31.7.1.4 for exos. These in addition to the latest versions.")

        # Select switch template
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                    sw_template_name)
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()

        # Create port type
        if node_1.cli_type == 'exos':
            # Assign port type to ports
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                  port_type_exos_trunk)
        elif node_1.cli_type == 'voss':
            # Assign port type to ports
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                  port_type_voss_trunk)
        # Configure CLI logs from XIQ
        cli.configure_cli_table(dut1=node_1, dut2=node_2)

        # Update config for cloning device
        xiq_library_at_class_level.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=network_policy_name, option="disable", device_mac=node_1.mac)
        xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_1.mac)

        # Put the cloning device in unmanaged state
        xiq_library_at_class_level.xflowsmanageDevices.change_manage_device_status(manage_type='UNMANAGE', device_mac=node_1.mac)

        # Clone the replacement device
        xiq_library_at_class_level.xflowsmanageDevices.select_clone_device(device_serial=node_1.serial,
                                                         replacement_device_type="Onboarded",
                                                         replacement_serial=node_2.serial)
        xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_2.mac)

        # Check cli commands are the same
        try:
            cli.check_clone_configuration(dut1=node_1, dut2=node_2)
        # Change back the cloning device to managed state
        finally:
            xiq_library_at_class_level.xflowsmanageDevices.change_manage_device_status(device_mac=node_1.mac)

    @pytest.mark.p1
    @pytest.mark.tcxm_22477
    def test_replacement_cloning_different_disconnected_txcm_22477(self, logger, cli, xiq_teardown_template, xiq_library_at_class_level, node_1, node_2, node_1_policy_name, node_1_template_name, node_2_policy_name, node_2_template_name, loaded_config):
        """TCXM-22477 - Check Clone Device function is available even if the original device is not connected to the XIQ
        Select a replacement device and initiate the Cloning Operation."""
        network_policy_name = node_1_policy_name
        sw_template_name = node_1_template_name

        logger.info("For an efficient and correct running of the automation tests, it is necessary to have the image versions 8.8.0.0 for voss and 31.7.1.4 for exos. These in addition to the latest versions.")

        # Select switch template
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                    sw_template_name)
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()

        # Create port type
        if node_1.cli_type == 'exos':
            # Assign port type to ports
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                  port_type_exos_trunk)
        elif node_1.cli_type == 'voss':
            # Assign port type to ports
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                  port_type_voss_trunk)
        # Configure CLI logs from XIQ
        cli.configure_cli_table(dut1=node_1, dut2=node_2)

        # Update config for cloning device
        xiq_library_at_class_level.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=network_policy_name, option="disable", device_mac=node_1.mac)
        xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_1.mac)

        # Disconnect the cloning device from XIQ
        cli.disable_enable_iqagent_clone_device(device=node_1, iqagent_option='disable')

        # Clone the replacement device
        xiq_library_at_class_level.xflowsmanageDevices.select_clone_device(device_serial=node_1.serial,
                                                         replacement_device_type="Onboarded",
                                                         replacement_serial=node_2.serial)
        xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_2.mac)

        # Check cli commands are the same
        try:
            cli.check_clone_configuration(dut1=node_1, dut2=node_2)
        # Connect back the cloning device to XIQ
        finally:
            cli.disable_enable_iqagent_clone_device(device=node_1, iqagent_option='enable')
            connection = cli.open_spawn(node_1.ip, node_1.port, node_1.username,
                                                    node_1.password, node_1.cli_type)
            cli.wait_for_configure_device_to_connect_to_cloud(cli_type=node_1.cli_type, server_name=loaded_config['sw_connection_host'], connection= connection, retry_count=30)

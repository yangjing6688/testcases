import pytest
import string
import random
from pytest_testconfig import config

event = "IQagent lost connectivity during configuration update, switch rebooted, and previous configuration has been " \
        "loaded"
failure_message = "*IQAgent unresponsive after configuration update. The device was rebooted and reverted to previous " \
                  "configuration.<br><br>Review configuration delta that resulted in IQAgent connectivity loss and make" \
                  " necessary changes."


class XIQ8955Tests:

    @pytest.mark.development
    @pytest.mark.tcxm_22592
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_tcxm_22592(self, node_1, logger, test_bed, xiq_library_at_class_level, loaded_config, enter_switch_cli,
                        cli, navigator):
        """
        Author          :   Dennis-Mircea Ciupitu (id: dciupitu)
        Description     :
        TCXM-22591      -   Verify that "Reboot and revert Extreme Networks switch configuration if IQAgent is
                            unresponsive after configuration update" checkbox from Advanced settings TAB within template
                            under Upload configuration automatically (when enabled) is present and disabled by default.
        TCXM-22592      -   Verify that if the upload config toggle is turned off, the "Reboot and revert Extreme
                            Networks switch configuration if IQAgent is unresponsive after configuration update"
                            checkbox is not present.
        Prerequisites:      None
        Steps Description:
        1.                  Create a Network Policy with specific EXOS device template.
        2.                  Go to Device Template TAB.
        3.                  Select an EXOS switch template.
        4.                  Verify that Advanced Settings TAB is present in Configuration Menu.
        5.                  Click on Advanced Settings TAB.
        6.                  Verify that  "Upload configuration automatically" is present in Advanced Settings TAB.
        7.                  Verify that the Toggle for "Upload configuration automatically" is OFF by default.
        -----------------------------------------------------------------------------------------------------
        8.                  Verify that the Toggle for "Upload configuration automatically" is not present.
        9.                  Onboard the EXOS device and assign the previously created Network Policy during onboarding.
        """
        # Variables definitions
        loaded_config['${TEST_NAME}'] = 'test_tcxm_22592_run'
        dut = node_1
        xiq_ip_address = config['sw_connection_host']
        sw_model_template = test_bed.generate_template_for_given_model(node_1)[0]
        # Create random network policy & switch template names
        pool = list(string.ascii_letters) + list(string.digits)
        network_policy_name = f"XIQ_8955_np_{''.join(random.sample(pool, k=6))}"
        device_template_name = f"XIQ_8955_template_{''.join(random.sample(pool, k=6))}"

        try:
            with enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to continue? (y/N)', confirmation_args='y')

            assert xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                network_policy_name) == 1, \
                "Failed to create Switching and Routing network policy"

            logger.info("Disable DNS server so we do not have out of sync config.")
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.navigate_to_np_edit_tab(network_policy_name)
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.go_to_dns_server_tab()
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.set_dns_server_status("disable")
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.save_dns_server_tab()
            navigator.wait_until_loading_is_done()

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.add_sw_template(network_policy_name,
                                                                                            sw_model_template,
                                                                                            device_template_name, node_1.cli_type) == 1, \
                f"Failed to add switch template with model: {sw_model_template}"
            logger.info("Set override so we can delete policy!")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                        device_template_name,
                                                                                        node_1.cli_type)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.set_override_policy_common_settings(state=True)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.save_template()
            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_adv_settings_tab(network_policy_name,
                                                                                                    device_template_name, node_1.cli_type) == 1, \
                "Failed to open Advanced Settings tab"

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.verify_upload_config_auto_button() == 1, \
                "Failed to verify Upload configuration automatically button"

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.verify_enable_auto_revert_option(), \
                "Failed to verify Enable auto revert button"

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.save_template() == 1, "Failed to save the template"

            assert xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_1,
                                                                                       policy_name=network_policy_name) == 1, \
                f"Failed to onboard this dut to XIQ: {dut}"

            spawn = None

            try:
                spawn = cli.open_spawn(dut.ip, dut.port, dut.username, dut.password, dut.cli_type,
                                       connection_method=dut.connection_method)
                cli.configure_device_to_connect_to_cloud(dut.cli_type, xiq_ip_address, spawn,
                                                         vr='VR-Default' if '5320' in dut.model else "VR-Mgmt")
            finally:
                cli.close_spawn(spawn)

            with enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)

            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(dut.serial) == 1, \
                f"Device {dut} didn't get online"

            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(dut.serial) == 1, \
                f"Device {dut} didn't get in MANAGED state"

            # assert xiq_library_at_class_level.xflowscommonDevices.device_update_progress(
            #     device_serial=dut.serial) != -1, \
            #     "Failed to push the configuration to the device"

            update_status = xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(
                node_1.mac, IRV=False)
            if update_status == -1:
                logger.step("Update failed due to mismatch, trying to do a Delta Update")
                xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(node_1.serial)
                xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_1.mac)
            else:
                logger.info("Successfully update the device.")

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_22592_teardown'

            try:
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=dut.serial)
                xiq_library_at_class_level.xflowsconfigureNetworkPolicy.delete_network_polices(network_policy_name)
                xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_switch_template(device_template_name)


            except Exception as exc:
                logger.info(exc)

    @pytest.mark.development
    @pytest.mark.tcxm_22591
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    @pytest.mark.dependson("tcxm_22592")
    def test_tcxm_22591(self, logger):
        """
        Author          :   Dennis-Mircea Ciupitu (id: dciupitu)
        Description     :
        TCXM-22591      -   Verify that "Reboot and revert Extreme Networks switch configuration if IQAgent is
                            unresponsive after configuration update" checkbox from Advanced settings TAB within template
                            under Upload configuration automatically (when enabled) is present and disabled by default.
        """
        logger.info("This test is covered by tcxm_22592")

    @pytest.mark.development
    @pytest.mark.tcxm_22593
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_tcxm_22593(self, node_1, logger, test_bed, xiq_library_at_class_level, loaded_config, enter_switch_cli,
                        cli, navigator):
        """
        Author          :   Dennis-Mircea Ciupitu (id: dciupitu)
        Description     :   Verify that if the upload config toggle is turned off, the "Reboot and revert Extreme
                            Networks switch configuration if IQAgent is unresponsive after configuration update"
                            checkbox is not present.
        Prerequisites   :   None
        Steps Description:
        1.                  Create a Network Policy with specific EXOS device template.
        2.                  Go to Device Template TAB.
        3.                  Select an EXOS switch template.
        4.                  Verify that Advanced Settings TAB is present in Configuration Menu.
        5.                  Click on Advanced Settings TAB.
        6.                  There is a Toggle  for "Upload configuration automatically" and can be switched on
                            (is off by default).
        7.                  Under upload configuration automatically toggle there is a checkbox called "Reboot and
                            revert Extreme Networks switch configuration if IQAgent is unresponsive after configuration
                            update" which is disabled by default.
        8.                  Verify if the text displayed for the checkbox is correct according to the initial
                            specifications.
        9.                  Onboard the EXOS device and assign the previously created Network Policy during onboarding.
        """
        # Variables definitions
        loaded_config['${TEST_NAME}'] = 'test_tcxm_22593_run'
        dut = node_1
        xiq_ip_address = config['sw_connection_host']
        sw_model_template = test_bed.generate_template_for_given_model(node_1)[0]

        # Create random network policy & switch template names
        pool = list(string.ascii_letters) + list(string.digits)
        network_policy_name = f"XIQ_8955_np_{''.join(random.sample(pool, k=6))}"
        device_template_name = f"XIQ_8955_template_{''.join(random.sample(pool, k=6))}"

        try:
            with enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to continue? (y/N)', confirmation_args='y')

            assert xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                network_policy_name) == 1, \
                "Failed to create Switching and Routing network policy"

            logger.info("Disable DNS server so we do not have out of sync config.")
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.navigate_to_np_edit_tab(network_policy_name)
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.go_to_dns_server_tab()
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.set_dns_server_status("disable")
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.save_dns_server_tab()
            navigator.wait_until_loading_is_done()

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.add_sw_template(network_policy_name,
                                                                                            sw_model_template,
                                                                                            device_template_name, node_1.cli_type) == 1, \
                f"Failed to add switch template with model: {sw_model_template}"
            logger.info("Set override so we can delete policy!")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                        device_template_name,
                                                                                        node_1.cli_type)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.set_override_policy_common_settings(state=True)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.save_template()
            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_adv_settings_tab(network_policy_name,
                                                                                                    device_template_name, node_1.cli_type) == 1, \
                "Failed to open Advanced Settings tab"

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.set_upload_config_auto_button() == 1, \
                "Failed to check Upload configuration automatically button"

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.check_text_enable_auto_revert_option() == 1, \
                "Failed to check the text of Enable auto revert button"

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.save_template() == 1, "Failed to save the template"

            assert xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_1,
                                                                                       policy_name=network_policy_name) == 1, \
                f"Failed to onboard this dut to XIQ: {dut}"

            try:
                spawn = cli.open_spawn(dut.ip, dut.port, dut.username, dut.password, dut.cli_type,
                                       connection_method=dut.connection_method)
                cli.configure_device_to_connect_to_cloud(dut.cli_type, xiq_ip_address, spawn,
                                                         vr='VR-Default' if '5320' in dut.model else "VR-Mgmt")
            finally:
                cli.close_spawn(spawn)

            with enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)

            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(dut.serial) == 1, \
                f"Device {dut} didn't get online"

            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(dut.serial) == 1, \
                f"Device {dut} didn't get in MANAGED state"

            # assert xiq_library_at_class_level.xflowscommonDevices.device_update_progress(
            #     device_serial=dut.serial) != -1, \
            #     "Failed to push the configuration to the device"

            update_status = xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(
                node_1.mac, IRV=False)
            if update_status == -1:
                logger.step("Update failed due to mismatch, trying to do a Delta Update")
                xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(node_1.serial)
                xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_1.mac)
            else:
                logger.info("Successfully update the device.")

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_22593_teardown'

            try:
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=dut.serial)
                xiq_library_at_class_level.xflowsconfigureNetworkPolicy.delete_network_polices(network_policy_name)
                xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_switch_template(device_template_name)

            except Exception as exc:
                logger.info(exc)

    @pytest.mark.development
    @pytest.mark.tcxm_22595
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_tcxm_22595(self, node_1, logger, test_bed, xiq_library_at_class_level, loaded_config, enter_switch_cli,
                        cli, navigator):
        """
        Author          :   Dennis-Mircea Ciupitu (id: dciupitu)
        Description     :
        TCXM-22594      -   Verify that additional message that's used for validating option to user should be displayed
                            when customer saves template. The user can select to ignore the message.
        TCXM-22595      -   Verify that "Reboot and revert Extreme Networks switch configuration if IQAgent is
                            unresponsive after configuration update" checkbox from Advanced settings TAB within template
                            under Upload configuration automatically (when enabled) can be selected.
        Prerequisites   :   None
        Steps Description:
        1.                  Create a Network Policy with specific EXOS device template.
        2.                  Go to Device Template TAB.
        3.                  Select an EXOS switch template.
        4.                  Verify that Advanced Settings TAB is present in Configuration Menu.
        5.                  Click on Advanced Settings TAB.
        6.                  Verify that  "Upload configuration automatically" is present in Advanced Settings TAB.
        7.                  Verify that the Toggle for "Upload configuration automatically" is OFF by default.
        8.                  Verify that the Toggle for "Upload configuration automatically" can be switched to ON.
        9.                  Verify that "Reboot and revert Extreme Networks switch configuration if IQAgent is
                            unresponsive after configuration update" checkbox is visible.
        10.                 Verify that "Reboot and revert Extreme Networks switch configuration if IQAgent is
                            unresponsive after configuration update" checkbox is disabled by default.
        11.                 Select the specified checkbox.
        12.                 Click Save button for the template.
        13.                 Click yes on the new opened box.
        14.                 Onboard the EXOS device and assign the previously created Network Policy during onboarding.
        """

        # Variables definitions
        loaded_config['${TEST_NAME}'] = 'test_tcxm_22595_run'
        dut = node_1
        xiq_ip_address = config['sw_connection_host']
        sw_model_template = test_bed.generate_template_for_given_model(node_1)[0]

        # Create random network policy & switch template names
        pool = list(string.ascii_letters) + list(string.digits)
        network_policy_name = f"XIQ_8955_np_{''.join(random.sample(pool, k=6))}"
        device_template_name = f"XIQ_8955_template_{''.join(random.sample(pool, k=6))}"

        try:
            with enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to continue? (y/N)', confirmation_args='y')

            assert xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                network_policy_name) == 1, \
                "Failed to create Switching and Routing network policy"

            logger.info("Disable DNS server so we do not have out of sync config.")
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.navigate_to_np_edit_tab(network_policy_name)
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.go_to_dns_server_tab()
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.set_dns_server_status("disable")
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.save_dns_server_tab()
            navigator.wait_until_loading_is_done()

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.add_sw_template(network_policy_name,
                                                                                            sw_model_template,
                                                                                            device_template_name, node_1.cli_type) == 1, \
                f"Failed to add switch template with model: {sw_model_template}"
            logger.info("Set override so we can delete policy!")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                        device_template_name,
                                                                                        node_1.cli_type)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.set_override_policy_common_settings(state=True)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.save_template()
            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_adv_settings_tab(network_policy_name,
                                                                                                    device_template_name, node_1.cli_type) == 1, \
                "Failed to open Advanced Settings tab"

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.set_upload_config_auto_button() == 1, \
                "Failed to set Upload configuration automatically button"

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.set_enable_auto_revert_option() == 1, \
                "Failed to set Enable auto revert button"

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.save_template_with_popup() == 1, "Failed to save the template"

            assert xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_1,
                                                                                       policy_name=network_policy_name) == 1, \
                f"Failed to onboard this dut to XIQ: {dut}"

            try:
                spawn = cli.open_spawn(dut.ip, dut.port, dut.username, dut.password, dut.cli_type,
                                       connection_method=dut.connection_method)
                cli.configure_device_to_connect_to_cloud(dut.cli_type, xiq_ip_address, spawn,
                                                         vr='VR-Default' if '5320' in dut.model else "VR-Mgmt")
            finally:
                cli.close_spawn(spawn)

            with enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)

            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(dut.serial) == 1, \
                f"Device {dut} didn't get online"

            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(dut.serial) == 1, \
                f"Device {dut} didn't get in MANAGED state"

            # assert xiq_library_at_class_level.xflowscommonDevices.device_update_progress(
            #     device_serial=dut.serial) != -1, \
            #     "Failed to push the configuration to the device"

            update_status = xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(
                node_1.mac, IRV=False)
            if update_status == -1:
                logger.step("Update failed due to mismatch, trying to do a Delta Update")
                xiq_library_at_class_level.xflowsmanageDevices.update_device_delta_configuration(node_1.serial)
                xiq_library_at_class_level.xflowsmanageDevices.check_device_update_status_by_using_mac(node_1.mac)
            else:
                logger.info("Successfully update the device.")
        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_22595_teardown'

            try:
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=dut.serial)
                xiq_library_at_class_level.xflowsconfigureNetworkPolicy.delete_network_polices(network_policy_name)
                xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_switch_template(device_template_name)
            except Exception as exc:
                logger.info(exc)

    @pytest.mark.dependson("tcxm_22595")
    @pytest.mark.development
    @pytest.mark.tcxm_22594
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_tcxm_22594(self, logger):
        """
        Author          :   Dennis-Mircea Ciupitu (id: dciupitu)
        Description     :
        TCXM-22594      -   Verify that additional message that's used for validating option to user should be displayed
                            when customer saves template. The user can select to ignore the message.
        """
        logger.info("This test is covered by tcxm_22592")

    @pytest.mark.development
    @pytest.mark.tcxm_22599
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_tcxm_22599(self, node_1, logger, test_bed, xiq_library_at_class_level, loaded_config, enter_switch_cli,
                        cli, navigator):
        """
        Author          :   Dennis-Mircea Ciupitu (id: dciupitu)
        Description     :   Verify that the rebooting process is triggered if the IQAgent is unresponsive during the
                            upload configuration process.
        Prerequisites   :   None
        Steps Description:
        1.                  Go to Global Settings Section.
        2.                  Go to the VIQ Management tab.
        3.                  Turn ON the supplemental cli button.
        4.                  Create a Network Policy with specific EXOS device template.
        5.                  Go to Device Template TAB.
        6.                  Select an EXOS switch template.
        7.                  Verify that Advanced Settings TAB is present in Configuration Menu.
        8.                  Click on Advanced Settings TAB.
        9.                  Verify that  "Upload configuration automatically" is present in Advanced Settings TAB.
        10.                 Verify that the Toggle for "Upload configuration automatically" is OFF by default.
        11.                 Verify that the Toggle for "Upload configuration automatically" can be switched to ON.
        12.                 Verify that "Reboot and revert Extreme Networks switch configuration if IQAgent is
                            unresponsive after configuration update" checkbox is visible.
        13.                 Verify that "Reboot and revert Extreme Networks switch configuration if IQAgent is
                            unresponsive after configuration update" checkbox is disabled by default.
        14.                 Select the specified checkbox
        15.                 Turn ON the supplemental cli button from advanced settings tab.
        16.                 Enter "unconfigure Mgmt ipaddress" command.
        17.                 Click Save button for the template.
        18.                 Click yes on the new opened box.
        19.                 Onboard the EXOS device and assign the previously created Network Policy during onboarding.
        20.                 Wait for approx. 15 minutes until updated columns displays the update device failed message
                            and the device is still connected.
        21.                 Check that by hovering the error message link the "IQAgent unresponsive after configuration
                            update. The device was rebooted and reverted to the previous configuration" message is
                            displayed.
        22.                 Verify that all appropriate alarms/events should be triggered
        23.                 Check that the audit icon remains orange and no configuration update was made
        """

        # Variables definitions
        loaded_config['${TEST_NAME}'] = 'test_tcxm_22599_run'
        dut = node_1
        xiq_ip_address = config['sw_connection_host']

        octet = 254
        try:
            while octet > 240:

                octet_str = str(octet)
                dut_ip = '.'.join(dut.ip.split('.')[:-1] + [octet_str])
                with enter_switch_cli(node_1) as dev_cmd:
                    if dut.platform == '5320':
                        output = dev_cmd.send_cmd(dut.name, f"ping vr VR-Default {dut_ip}", max_wait=10)
                    else:
                        output = dev_cmd.send_cmd(dut.name, f"ping vr VR-Mgmt {dut_ip}", max_wait=10)

                if "Request timed out" in output[0].return_text:
                    logger.info("Ping failed. IP is usable.")
                    break
                else:
                    logger.info("Ping successfully. Making another try.")
                    octet = octet - 1
            else:
                assert False

        except Exception as exc:
            pytest.fail(f"Failed to get an unresponsive ip address from the mgmt vr")

        sw_model_template = test_bed.generate_template_for_given_model(node_1)[0]

        # Create random network policy & switch template names
        pool = list(string.ascii_letters) + list(string.digits)
        network_policy_name = f"XIQ_8955_np_{''.join(random.sample(pool, k=6))}"
        device_template_name = f"XIQ_8955_template_{''.join(random.sample(pool, k=6))}"
        supplemental_cli_name = f"scli_8955_{''.join(random.sample(pool, k=6))}"
        try:
            with enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to continue? (y/N)', confirmation_args='y')

            assert xiq_library_at_class_level.xflowsglobalsettingsGlobalSetting.get_supplemental_cli_option(
                "enable") == 1, \
                "Failed to enable Supplemental CLI in Global Settings"

            assert xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                network_policy_name) == 1, \
                "Failed to create Switching and Routing network policy"

            logger.info("Disable DNS server so we do not have out of sync config.")
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.navigate_to_np_edit_tab(network_policy_name)
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.go_to_dns_server_tab()
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.set_dns_server_status("disable")
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.save_dns_server_tab()
            navigator.wait_until_loading_is_done()
            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.add_sw_template(network_policy_name,
                                                                                            sw_model_template,
                                                                                            device_template_name, node_1.cli_type) == 1, \
                f"Failed to add switch template with model: {sw_model_template}"
            logger.info("Set override so we can delete policy!")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name, device_template_name, node_1.cli_type)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.set_override_policy_common_settings(state=True)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.save_template()

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_adv_settings_tab(network_policy_name,
                                                                                                    device_template_name, node_1.cli_type) == 1, \
                "Failed to open Advanced Settings tab"

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.set_upload_config_auto_button() == 1, \
                "Failed to set Upload configuration automatically button"

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.set_enable_auto_revert_option() == 1, \
                "Failed to set Enable auto revert button"

            if dut.platform == '5320':
                commands = f"configure iproute add default {dut_ip} vr vr-default"
            else:
                commands = f"configure iproute add default {dut_ip} vr vr-mgmt"

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.add_supplemental_cli_into_template(
                network_policy_name, device_template_name,
                supplemental_cli_name, commands,
                navigate_to_scli=False,
                save_template=False) == 1, \
                "Failed to configure Supplemental CLI profile"

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.save_template_with_popup() == 1, "Failed to save the template"

            assert xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_1,
                                                                                       policy_name=network_policy_name) == 1, \
                f"Failed to onboard this dut to XIQ: {dut}"

            try:
                spawn = cli.open_spawn(dut.ip, dut.port, dut.username, dut.password, dut.cli_type,
                                       connection_method=dut.connection_method)
                cli.configure_device_to_connect_to_cloud(dut.cli_type, xiq_ip_address, spawn,
                                                         vr='VR-Default' if '5320' in dut.model else "VR-Mgmt")
            finally:
                cli.close_spawn(spawn)

            with enter_switch_cli(node_1) as dev_cmd:
                #dev_cmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)
                dev_cmd.send_cmd(dut.name, 'save configuration', confirmation_phrases='(y/N)',
                                 confirmation_args="y", max_wait=10, interval=2)
            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(dut.serial) == 1, \
                f"Device {dut} didn't get online"

            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(dut.serial) == 1, \
                f"Device {dut} didn't get in MANAGED state"

            assert xiq_library_at_class_level.xflowscommonDevices.check_update_column_by_failure_message(dut.serial,
                                                                                                         failure_message) == 1, \
                "Failed to obtain the expected Device Updated Failed message"

            assert xiq_library_at_class_level.xflowsmanageDevice360.get_event_from_device360(dut, event,
                                                                                             event_type="config") == 1, \
                "The IQAgent unresponsive event was not triggered!"

            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(device_serial=dut.serial)
            assert res == 'config audit mismatch', \
                f"The EXOS device did not come up successfully in the XIQ; Device: {dut}"

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_22599_teardown'

            try:
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=dut.serial)
                xiq_library_at_class_level.xflowsconfigureNetworkPolicy.delete_network_polices(network_policy_name)
                xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_switch_template(device_template_name)
                xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_supplemental_cli_profile(
                    supplemental_cli_name)
            except Exception as exc:
                logger.info(exc)

    @pytest.mark.development
    @pytest.mark.tcxm_22603
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_tcxm_22603(self, node_1, logger, test_bed, xiq_library_at_class_level, loaded_config, enter_switch_cli,
                        cli, navigator):
        """
        Author          :   Dennis-Mircea Ciupitu (id: dciupitu)
        Description     :   Verify that  the rebooting process is triggered if the IQAgent is unresponsive during the
                            upload configuration process (the policy isn't assigned at onboarding). The DUT transitions
                            from unmanaged to managed.
        Prerequisites   :   None
        Steps Description:
        1.                  Go to Global Settings Section.
        2.                  Go to the VIQ Management tab.
        3.                  Turn ON the supplemental cli button.
        4.                  Create a Network Policy with specific EXOS device template.
        5.                  Go to Device Template TAB.
        6.                  Select an EXOS switch template.
        7.                  Verify that Advanced Settings TAB is present in Configuration Menu.
        8.                  Click on Advanced Settings TAB.
        9.                  Verify that  "Upload configuration automatically" is present in Advanced Settings TAB.
        10.                 Verify that the Toggle for "Upload configuration automatically" is OFF by default.
        11.                 Verify that the Toggle for "Upload configuration automatically" can be switched to ON.
        12.                 Verify that "Reboot and revert Extreme Networks switch configuration if IQAgent is
                            unresponsive after configuration update" checkbox is visible.
        13.                 Verify that "Reboot and revert Extreme Networks switch configuration if IQAgent is
                            unresponsive after configuration update" checkbox is disabled by default.
        14.                 Select the specified checkbox.
        15.                 Turn ON the supplemental cli button from advanced settings tab.
        16.                 Enter "unconfigure Mgmt ipaddress" command.
        17                  Click Save button for the template.
        18.                 Click yes on the new opened box.
        19.                 Onboard the EXOS device and assign the previously created Network Policy during onboarding.
        20.                 Once the device is onboarded and managed make the device as unmanaged and assign the policy
                            template.
        21.                 Now move the device to managed and ensure  the  config upload is triggered for the device.
        22.                 Wait for approx. 15 minutes until updated columns displays the update device failed message
                            and the device is still connected.
        23.                 Check that by hovering the error message link the "IQAgent unresponsive after configuration
                            update. The device was rebooted and reverted to the previous configuration" message is
                            displayed.
        24.                 Verify that all appropriate alarms/events should be triggered
        25.                 Check that the audit icon remains orange and no configuration update was made
        """

        # Variables definitions
        loaded_config['${TEST_NAME}'] = 'test_tcxm_22603_run'
        dut = node_1
        xiq_ip_address = config['sw_connection_host']

        octet = 254
        try:
            while octet > 240:

                octet_str = str(octet)
                dut_ip = '.'.join(dut.ip.split('.')[:-1] + [octet_str])
                with enter_switch_cli(node_1) as dev_cmd:
                    if dut.platform == '5320':
                        output = dev_cmd.send_cmd(dut.name, f"ping vr VR-Default {dut_ip}", max_wait=10)
                    else:
                        output = dev_cmd.send_cmd(dut.name, f"ping vr VR-Mgmt {dut_ip}", max_wait=10)

                if "Request timed out" in output[0].return_text:
                    logger.info("Ping failed. IP is usable.")
                    break
                else:
                    logger.info("Ping successfully. Making another try.")
                    octet = octet - 1
            else:
                assert False

        except Exception as exc:
            pytest.fail(f"Failed to get an unresponsive ip address from the mgmt vr")

        sw_model_template = test_bed.generate_template_for_given_model(node_1)[0]

        # Create random network policy & switch template names
        pool = list(string.ascii_letters) + list(string.digits)
        network_policy_name = f"XIQ_8955_np_{''.join(random.sample(pool, k=6))}"
        device_template_name = f"XIQ_8955_template_{''.join(random.sample(pool, k=6))}"
        supplemental_cli_name = f"scli_8955_{''.join(random.sample(pool, k=6))}"
        try:
            with enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to continue? (y/N)', confirmation_args='y')

            assert xiq_library_at_class_level.xflowsglobalsettingsGlobalSetting.get_supplemental_cli_option(
                "enable") == 1, \
                "Failed to enable Supplemental CLI in Global Settings"

            network_policy = xiq_library_at_class_level.xflowsconfigureNetworkPolicy
            assert network_policy.create_switching_routing_network_policy(network_policy_name) == 1, \
                "Failed to create Switching and Routing network policy"

            logger.info("Disable DNS server so we do not have out of sync config.")
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.navigate_to_np_edit_tab(network_policy_name)
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.go_to_dns_server_tab()
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.set_dns_server_status("disable")
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.save_dns_server_tab()
            navigator.wait_until_loading_is_done()
            switch_template = xiq_library_at_class_level.xflowsconfigureSwitchTemplate
            assert switch_template.add_sw_template(network_policy_name,
                                                   sw_model_template,
                                                   device_template_name, node_1.cli_type) == 1, \
                f"Failed to add switch template with model: {sw_model_template}"
            logger.info("Set override so we can delete policy!")
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name, device_template_name, node_1.cli_type)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.set_override_policy_common_settings(state=True)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.save_template()

            assert switch_template.select_adv_settings_tab(network_policy_name, device_template_name, node_1.cli_type) == 1, \
                "Failed to open Advanced Settings tab"

            assert switch_template.set_upload_config_auto_button() == 1, \
                "Failed to set Upload configuration automatically button"

            assert switch_template.set_enable_auto_revert_option() == 1, \
                "Failed to set Enable auto revert button"

            if dut.platform == '5320':
                commands = f"configure iproute add default {dut_ip} vr vr-default"
            else:
                commands = f"configure iproute add default {dut_ip} vr vr-mgmt"

            assert switch_template.add_supplemental_cli_into_template(network_policy_name, device_template_name,
                                                                      supplemental_cli_name, commands,
                                                                      navigate_to_scli=False,
                                                                      save_template=False) == 1, \
                "Failed to configure Supplemental CLI profile"

            assert switch_template.save_template_with_popup() == 1, "Failed to save the template"

            assert xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_1) == 1, \
                f"Failed to onboard this dut to XIQ: {dut}"

            try:
                spawn = cli.open_spawn(dut.ip, dut.port, dut.username, dut.password, dut.cli_type,
                                       connection_method=dut.connection_method)
                cli.configure_device_to_connect_to_cloud(dut.cli_type, xiq_ip_address, spawn,
                                                         vr='VR-Default' if '5320' in dut.model else "VR-Mgmt")
            finally:
                cli.close_spawn(spawn)
            with enter_switch_cli(node_1) as dev_cmd:
                #dev_cmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)
                dev_cmd.send_cmd(dut.name, 'save configuration', confirmation_phrases='(y/N)',
                                 confirmation_args="y", max_wait=10, interval=2)

            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(dut.serial) == 1, \
                f"Device {dut} didn't get online"

            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(dut.serial) == 1, \
                f"Device {dut} didn't get in MANAGED state"

            assert xiq_library_at_class_level.xflowscommonDevices.change_manage_device_status(manage_type="UNMANAGE",
                                                                                              device_serial=dut.serial) == 1, \
                f"Failed to change Management status of {dut} in UNMANAGE"

            assert xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch(network_policy_name,
                                                                                                  dut.serial,
                                                                                                  update_device=False) == 1, \
                f"Failed to assign network policy to {dut}"

            assert xiq_library_at_class_level.xflowscommonDevices.change_manage_device_status(manage_type="MANAGE",
                                                                                              device_serial=dut.serial) == 1, \
                f"Failed to change Management status of {dut} in MANAGE"

            assert xiq_library_at_class_level.xflowscommonDevices.check_update_column_by_failure_message(dut.serial,
                                                                                                         failure_message) == 1, \
                "Failed to obtain the expected Device Updated Failed message"

            assert xiq_library_at_class_level.xflowsmanageDevice360.get_event_from_device360(dut, event,
                                                                                             event_type="config") == 1, \
                "The IQAgent unresponsive event was not triggered!"

            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

            res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(device_serial=dut.serial)
            assert res == 'config audit mismatch', \
                f"The EXOS device did not come up successfully in the XIQ; Device: {dut}"

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_22603_teardown'

            try:
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=dut.serial)
                xiq_library_at_class_level.xflowsconfigureNetworkPolicy.delete_network_polices(network_policy_name)
                xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_switch_template(device_template_name)
                xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_supplemental_cli_profile(
                    supplemental_cli_name)
            except Exception as exc:
                logger.info(exc)

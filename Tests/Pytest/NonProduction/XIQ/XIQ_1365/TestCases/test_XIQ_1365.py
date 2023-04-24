import pytest
import re


@pytest.mark.p1
@pytest.mark.development
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class Xiq1365Tests:

    @pytest.fixture(scope="class", autouse=True)
    def make_sure_node_1_is_onboarded(self, revert_node, node_1, xiq_library_at_class_level):
        try:
            yield
        finally:
            revert_node(node_1, xiq_library_at_class_level, assign_network_policy=False, push_network_policy=False, downgrade_iqagent=True)

    @pytest.mark.tcxm_20574
    def test_tcxm_20574(self, xiq_library_at_class_level, node_1, test_bed, utils):
        """
        tcxm_20574 - Verify that Advanced settings TAB is present in Configuration Menu in Switch Template Configuration   
        """
        network_policy_name = f"policy_XIQ1365_{test_bed.get_random_word()}"
        device_template_name = f"template_XIQ1365_{test_bed.get_random_word()}"

        try:

            with test_bed.enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(node_1.name, 'disable iqagent', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to continue? (y/N)', confirmation_args='y')

            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                network_policy_name)

            utils.wait_till(timeout=3)

            sw_name_final, _ = test_bed.generate_template_for_given_model(node_1)

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.add_sw_template(network_policy_name,
                                                                                            sw_name_final,
                                                                                            device_template_name,
                                                                                            node_1.cli_type) == 1, \
                f"Failed to add switch template with model: {device_template_name}"
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.device_templ_advanced_settings(network_policy_name,
                                                                                                    device_template_name,
                                                                                                    node_1.cli_type,
                                                                                                    sw_model=node_1.model,
                                                                                                    upgrade_device_upon_auth=True
                                                                                                    )

        finally:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            test_bed.add_switch_template_to_teardown(device_template_name)
            test_bed.add_network_policy_to_teardown(network_policy_name)
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)

    @pytest.mark.tcxm_20576
    def test_tcxm_20576(self, xiq_library_at_class_level, node_1, enter_switch_cli, test_bed, utils):
        """
        tcxm_20576 - Verify that Toggle for "Upgrade device firmware upon device authentication" is present.
        """
        network_policy_name = f"policy_XIQ1365_{test_bed.get_random_word()}"
        device_template_name = f"template_XIQ1365_{test_bed.get_random_word()}"

        try:
            with enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(node_1.name, 'disable iqagent', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to continue? (y/N)', confirmation_args='y')
                
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                network_policy_name)

            utils.wait_till(timeout=3)

            sw_name_final, _ = test_bed.generate_template_for_given_model(node_1)
            
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.add_sw_template(
                network_policy_name,
                sw_name_final,
                device_template_name,
                cli_type=node_1.cli_type)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.device_templ_advanced_settings(network_policy_name,
                                                                                                    device_template_name,
                                                                                                    node_1.cli_type,
                                                                                                    upgrade_device_upon_auth=True,
                                                                                                    sw_model=node_1.model)
        finally:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            test_bed.add_switch_template_to_teardown(device_template_name)
            test_bed.add_network_policy_to_teardown(network_policy_name)
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)

    @pytest.mark.tcxm_20577
    def test_tcxm_20577(self, xiq_library_at_class_level, node_1, enter_switch_cli, cli, test_bed,
                        logger, utils):
        """
        tcxm_20577 - Verify that Option  for "Upgrade firmware to the latest version" is present.           
        """
        network_policy_name = f"policy_XIQ1365_{test_bed.get_random_word()}"
        device_template_name = f"template_XIQ1365_{test_bed.get_random_word()}"

        try:

            with enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(node_1.name, 'disable iqagent', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to continue? (y/N)', confirmation_args='y')

            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                network_policy_name)

            utils.wait_till(timeout=3)

            sw_name_final, _ = test_bed.generate_template_for_given_model(node_1)

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.add_sw_template(network_policy_name,
                                                                                            sw_name_final,
                                                                                            device_template_name,
                                                                                            node_1.cli_type) == 1, \
                f"Failed to add switch template with model: {device_template_name}"
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.device_templ_advanced_settings(network_policy_name,
                                                                                                    device_template_name,
                                                                                                    node_1.cli_type,
                                                                                                    upgrade_device_upon_auth=True,
                                                                                                    sw_model=node_1.model)

            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

            utils.wait_till(timeout=5)

            if xiq_library_at_class_level.xflowscommonDevices.search_device(device_mac=node_1.mac, ignore_failure=True) == 1:
                xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)
            
            xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick({**node_1, "location": test_bed.node_1_onboarding_location}, policy_name=network_policy_name)

            with test_bed.open_spawn(node_1) as spawn:
                cli.configure_device_to_connect_to_cloud(node_1.cli_type, test_bed.sw_connection_host, spawn, vr=node_1.mgmt_vr)
                
            utils.wait_till(timeout=600)
            logger.step("Wait for the update to finish")
            if xiq_library_at_class_level.xflowscommonDevices._check_update_network_policy_status(network_policy_name, node_1.mac, IRV=False) != 1:
                if xiq_library_at_class_level.xflowscommonDevices.update_device_delta_configuration(node_1.mac) != 1:
                    logger.fail(f"Failed to do a delta confguration update for this switch: '{node_1.mac}'.")
                
                if xiq_library_at_class_level.xflowscommonDevices._check_update_network_policy_status(network_policy_name, node_1.mac, IRV=False) != 1:
                    logger.fail(f"It looks like both type of device update failed for this switch: '{node_1.mac}'.")

            xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()
            utils.wait_till(timeout=15)

            with test_bed.open_spawn(node_1) as spawn:
                cli.downgrade_iqagent(node_1.cli_type, spawn)

            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_1.serial) == 1, \
                f"Device {node_1} didn't get online"
            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_1.serial) == 1, \
                f"Device {node_1} didn't get in MANAGED state"

            xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()
            utils.wait_till(timeout=15)

            logger.info("Get os version from device")
            os_version = xiq_library_at_class_level.xflowscommonDevices.get_device_row_values(node_1.mac, 'OS VERSION')
            nos_version = str(os_version['OS VERSION'])
            logger.info(f"device os_version: {nos_version}")

            latest_os_version = xiq_library_at_class_level.xflowscommonDevices.get_latest_version_from_device_update(
                node_1)
            assert nos_version == latest_os_version, f"The current device os version: {nos_version} is differet to the latest version {latest_os_version} after the update"

            logger.info(f"device latest_os_version = {latest_os_version}")

            res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(node_1.serial)
            assert res == 'config audit mismatch', \
                f"The EXOS device did not come up successfully in the XIQ; Device: {node_1}"

        finally:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            test_bed.add_switch_template_to_teardown(device_template_name)
            test_bed.add_network_policy_to_teardown(network_policy_name)
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)

    @pytest.mark.tcxm_20578
    def test_tcxm_20578(self, xiq_library_at_class_level, node_1, enter_switch_cli, cli, test_bed, logger, utils):
        """
        tcxm_20578 - Verify that Option for "Upgrade to the specific device firmware version" is present.
        """
        network_policy_name = f"policy_XIQ1365_{test_bed.get_random_word()}"
        device_template_name = f"template_XIQ1365_{test_bed.get_random_word()}"

        try:
            with enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(node_1.name, 'disable iqagent', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to continue? (y/N)', confirmation_args='y')

                output_cmd = dev_cmd.send_cmd(node_1.name, 'show version', max_wait=10, interval=2)[0].return_text

            image_version = re.findall(r"IMG:\s+(\d+\.\d+\.\d+\.\d+)", output_cmd)[0]
            logger.info(f"Initial image version on device is {image_version}")

            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                network_policy_name)

            utils.wait_till(timeout=3)

            sw_name_final, _ = test_bed.generate_template_for_given_model(node_1)

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.add_sw_template(network_policy_name,
                                                                                            sw_name_final,
                                                                                            device_template_name,
                                                                                            node_1.cli_type) == 1, \
                f"Failed to add switch template with model: {device_template_name}"
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.device_templ_advanced_settings(network_policy_name,
                                                                                                    device_template_name,
                                                                                                    node_1.cli_type,
                                                                                                    upgrade_device_upon_auth=True,
                                                                                                    current_image_version=image_version,
                                                                                                    sw_model=sw_name_final)

            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            
            if xiq_library_at_class_level.xflowscommonDevices.search_device(device_mac=node_1.mac, ignore_failure=True) == 1:
                xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)
                
            xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(
                {**node_1, "location": test_bed.node_1_onboarding_location}, policy_name=network_policy_name)
            status_before = xiq_library_at_class_level.xflowscommonDevices.get_device_updated_status(
                device_mac=node_1.serial)
            logger.info(f"Device updated status after onboarding is {status_before}")

            with test_bed.open_spawn(node_1) as spawn:
                cli.configure_device_to_connect_to_cloud(node_1.cli_type, test_bed.sw_connection_host, spawn, vr=node_1.mgmt_vr)

            xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()

            utils.wait_till(timeout=600)
            logger.step("Wait for the update to finish")
            if xiq_library_at_class_level.xflowscommonDevices._check_update_network_policy_status(network_policy_name, node_1.mac, IRV=False) != 1:
                if xiq_library_at_class_level.xflowscommonDevices.update_device_delta_configuration(node_1.mac) != 1:
                    logger.fail(f"Failed to do a delta confguration update for this switch: '{node_1.mac}'.")
                
                if xiq_library_at_class_level.xflowscommonDevices._check_update_network_policy_status(network_policy_name, node_1.mac, IRV=False) != 1:
                    logger.fail(f"It looks like both type of device update failed for this switch: '{node_1.mac}'.")

            xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()
            utils.wait_till(timeout=15)
            
            logger.step("Checking for the update column to reflect the firmware update status")
            xiq_library_at_class_level.xflowscommonDevices.check_update_column_change(node_1.serial, status_before)

            with test_bed.open_spawn(node_1) as spawn:
                cli.downgrade_iqagent(node_1.cli_type, spawn)
                
            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_1.serial) == 1, \
                f"Device {node_1} didn't get online"
            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_1.serial) == 1, \
                f"Device {node_1} didn't get in MANAGED state"

            res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(node_1.serial)
            assert res == 'config audit mismatch', \
                f"The EXOS device did not come up successfully in the XIQ; Device: {node_1}"

        finally:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            test_bed.add_switch_template_to_teardown(device_template_name)
            test_bed.add_network_policy_to_teardown(network_policy_name)
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)

    @pytest.mark.tcxm_20579
    def test_tcxm_20579(self, xiq_library_at_class_level, node_1, enter_switch_cli, cli, test_bed, logger, utils, poll):
        """
        tcxm_20579 - Verify that Toggle for "Upload configuration automatically" is present and off by default.
        """
        network_policy_name = f"policy_XIQ1365_{test_bed.get_random_word()}"
        device_template_name = f"template_XIQ1365_{test_bed.get_random_word()}"

        try:
            with enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(node_1.name, 'disable iqagent', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to continue? (y/N)', confirmation_args='y')

            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                network_policy_name)

            utils.wait_till(timeout=3)

            sw_name_final, _ = test_bed.generate_template_for_given_model(node_1)

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.add_sw_template(network_policy_name,
                                                                                            sw_name_final,
                                                                                            device_template_name,
                                                                                            node_1.cli_type) == 1, \
                f"Failed to add switch template with model: {device_template_name}"
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.device_templ_advanced_settings(network_policy_name,
                                                                                                    device_template_name,
                                                                                                    node_1.cli_type,
                                                                                                    upload_auto=True,
                                                                                                    sw_model=sw_name_final)

            logger.step("Change STP forward delay value; this change will be used to check if config push has been successfuly done")
            xiq_fw_delay = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template_device_config_forw_delay(
                network_policy_name,
                device_template_name)
            logger.info(f"STP forward delay has been configured in device template: {xiq_fw_delay}")

            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

            utils.wait_till(timeout=5)
            if xiq_library_at_class_level.xflowscommonDevices.search_device(device_mac=node_1.mac, ignore_failure=True) == 1:
                xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)
            
            xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(
                {**node_1, "location": test_bed.node_1_onboarding_location}, policy_name=network_policy_name)
            xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()

            status_before = xiq_library_at_class_level.xflowscommonDevices.get_device_updated_status(
                device_mac=node_1.serial)

            with test_bed.open_spawn(node_1) as spawn:
                cli.configure_device_to_connect_to_cloud(node_1.cli_type, test_bed.sw_connection_host, spawn, vr=node_1.mgmt_vr)

            xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()

            utils.wait_till(timeout=600)
            logger.step("Wait for the update to finish")
            if xiq_library_at_class_level.xflowscommonDevices._check_update_network_policy_status(network_policy_name, node_1.mac, IRV=False) != 1:
                if xiq_library_at_class_level.xflowscommonDevices.update_device_delta_configuration(node_1.mac) != 1:
                    logger.fail(f"Failed to do a delta confguration update for this switch: '{node_1.mac}'.")
                
                if xiq_library_at_class_level.xflowscommonDevices._check_update_network_policy_status(network_policy_name, node_1.mac, IRV=False) != 1:
                    logger.fail(f"It looks like both type of device update failed for this switch: '{node_1.mac}'.")

            xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()
            utils.wait_till(timeout=15)
            
            logger.step("Checking for the update column to reflect the firmware update status")
            xiq_library_at_class_level.xflowscommonDevices.check_update_column_change(node_1.serial, status_before)

            with test_bed.open_spawn(node_1) as spawn:
                cli.downgrade_iqagent(node_1.cli_type, spawn)

            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_1.serial) == 1, \
                f"Device {node_1} didn't get online"
            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_1.serial) == 1, \
                f"Device {node_1} didn't get in MANAGED state"

            try:
                for status in poll(lambda: xiq_library_at_class_level.xflowscommonDevices.get_device_status(node_1.serial), max_poll_time=300):
                    if status == "green":
                        break
            except:
                logger.fail(f"The EXOS device did not come up successfully in the XIQ; Device: {node_1}")

            logger.step("Get the STP forward delay value configured on device after config push")
            dev_fw_delay = cli.get_nw_templ_device_config_forward_delay(node_1)
            logger.info(f"STP forward delay value configured on device after config push is: {dev_fw_delay}")

            assert dev_fw_delay == xiq_fw_delay, f"Upload configuration automatically failed, STP forward delay value " \
                                                 f"configured on XIQ is different: {xiq_fw_delay}"

        finally:
            delay_xiq = cli.set_nw_templ_device_config_forward_delay(node_1)
            logger.info(f"STP forward delay default value has been restored: {delay_xiq}")

            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            test_bed.add_switch_template_to_teardown(device_template_name)
            test_bed.add_network_policy_to_teardown(network_policy_name)
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)

    @pytest.mark.tcxm_20580
    def test_tcxm_20580(self, xiq_library_at_class_level, node_1, cli, test_bed, logger, utils):
        """
        tcxm_20580 - Check that if the node_1 is already onboarded and has a network policy, changing "Upload
                     configuration automatically" or "Upgrade device firmware upon device firmware authentication"
                     from off to on will not have any effect.
        """
        network_policy_name = f"policy_XIQ1365_{test_bed.get_random_word()}"
        device_template_name = f"template_XIQ1365_{test_bed.get_random_word()}"

        try:
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                network_policy_name)

            utils.wait_till(timeout=3)

            sw_name_final, _ = test_bed.generate_template_for_given_model(node_1)

            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.add_sw_template(
                network_policy_name,
                sw_name_final,
                device_template_name,
                cli_type=node_1.cli_type)

            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

            utils.wait_till(timeout=5)
            
            if xiq_library_at_class_level.xflowscommonDevices.search_device(device_mac=node_1.mac, ignore_failure=True) == 1:
                xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)
                
            xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(
                {**node_1, "location": test_bed.node_1_onboarding_location}, policy_name=network_policy_name)
            utils.wait_till(timeout=5)
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

            with test_bed.open_spawn(node_1) as spawn:
                cli.configure_device_to_connect_to_cloud(node_1.cli_type, test_bed.sw_connection_host, spawn, vr=node_1.mgmt_vr)

            xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()

            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.device_templ_advanced_settings(network_policy_name,
                                                                                                    device_template_name,
                                                                                                    node_1.cli_type,
                                                                                                    upgrade_device_upon_auth=True,
                                                                                                    upload_auto=True,
                                                                                                    sw_model=sw_name_final)
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

            logger.info("Get managed value from device")
            managed_field = xiq_library_at_class_level.xflowscommonDevices.get_device_row_values(node_1.serial, 'MANAGED')
            managed_final = str(managed_field['MANAGED'])
            logger.info(f"device managed field is {managed_final}")

            max_wait = 180
            count = 0
            while "Managed" not in managed_final and count < max_wait:
                utils.wait_till(timeout=10)
                count += 10
                xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()
                managed_field = xiq_library_at_class_level.xflowscommonDevices.get_device_row_values(node_1.serial, 'MANAGED')
                managed_final = str(managed_field['MANAGED'])

            logger.step("Change STP forward delay value; this change will be used to check if "
                        "config push has been successfully done")
            xiq_fw_delay = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template_device_config_forw_delay(
                network_policy_name,
                device_template_name)
            logger.info(f"STP forward delay has been configured in device template: {xiq_fw_delay}")

            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.press_upload_config_and_upgr_firm_button(
                network_policy_name, device_template_name)

            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_1.serial) == 1, \
                f"Device {node_1} didn't get online"
            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_1.serial) == 1, \
                f"Device {node_1} didn't get in MANAGED state"

            res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(device_serial=node_1.serial)

            logger.step("Get the STP forward delay value configured on device after config push")
            dev_fw_delay = cli.get_nw_templ_device_config_forward_delay(node_1)
            logger.info(f"STP forward delay value configured on device after config push is: {dev_fw_delay}")

            assert dev_fw_delay != xiq_fw_delay, f"Upload configuration automatically was triggered, STP forward delay value " \
                                                 f"configured on XIQ is equal: {xiq_fw_delay}"

            assert xiq_library_at_class_level.xflowsmanageDevice360.get_event_from_device360(node_1, "Download Config",
                                                                                             event_type="config",
                                                                                             ignore_failure=True) == -1, "Download config event was found in event table"
            assert xiq_library_at_class_level.xflowsmanageDevice360.get_event_from_device360(node_1,
                                                                                             "firmware successful",
                                                                                             ignore_failure=True) == -1, "Download firmware successfull event was found in event table"

        finally:

            delay_xiq = cli.set_nw_templ_device_config_forward_delay(node_1)
            logger.info(f"STP forward delay default value has been restored: {delay_xiq}")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

            test_bed.add_switch_template_to_teardown(device_template_name)
            test_bed.add_network_policy_to_teardown(network_policy_name)
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)

    @pytest.mark.tcxm_20582
    def test_tcxm_20582(self, xiq_library_at_class_level, node_1, enter_switch_cli, cli, test_bed, logger, utils):
        """
        tcxm_20582 - Check that all appropriate alarms/events should be triggered for upgrade firmware and auto upload config.
        """
        network_policy_name = f"policy_XIQ1365_{test_bed.get_random_word()}"
        device_template_name = f"template_XIQ1365_{test_bed.get_random_word()}"
        sw_name_final, _ = test_bed.generate_template_for_given_model(node_1)

        try:
            logger.step("Check test preconditions")
            with enter_switch_cli(node_1) as dev_cmd:
                output_1 = dev_cmd.send_cmd(node_1.name, 'show version | grep IMG')
                check_image_version = output_1[0].return_text
                image_version_regex = 'IMG:([ ]{1,}.{0,})'
                image_version = utils.get_regexp_matches(check_image_version, image_version_regex, 1)[0]
                device_image_version = image_version.replace(utils.get_regexp_matches(image_version, '([ ])')[0], '')
                device_image_version = device_image_version.strip()

            latest_image_version, image_versions = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.get_latest_firmware_version_from_switch_template(
                sw_name_final)
            
            if device_image_version in latest_image_version:

                if xiq_library_at_class_level.xflowscommonDevices.search_device(device_mac=node_1.mac,
                                                                                ignore_failure=True) == 1:
                    xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)
                xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick({**node_1, "location": test_bed.node_1_onboarding_location})

                test_upgrade_version = None
                for version in image_versions:
                    if version and (device_image_version not in version):
                        test_upgrade_version = version.split('-')[1].replace('.xos', '').replace('(GLOBAL)', '').strip()
                        break
                else:
                    logger.fail("Failed to find a system version for this test case")

                xiq_library_at_class_level.xflowsmanageDevices.upgrade_device(node_1, version=test_upgrade_version)
                utils.wait_till(timeout=600)
                image_version = test_upgrade_version
                assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_1.serial) == 1, \
                    f"Device {node_1} didn't get online"
                assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_1.serial) == 1, \
                    f"Device {node_1} didn't get in MANAGED state"

                xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)
            
                with test_bed.open_spawn(node_1) as spawn:
                    cli.downgrade_iqagent(node_1.cli_type, spawn)
                
            logger.step("Device onfiguration before test")
            with enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(node_1.name, 'disable iqagent', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to continue? (y/N)', confirmation_args='y')
                output_cmd = dev_cmd.send_cmd(node_1.name, 'show version', max_wait=10, interval=2)[0].return_text
                
            image_version = re.findall(r"IMG:\s+(\d+\.\d+\.\d+\.\d+)", output_cmd)[0]
            logger.info(f"Initial image version on device is {image_version}")

            logger.step("Create a network policy")
            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                network_policy_name)
            utils.wait_till(timeout=3)

            logger.step("Create switch template")

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.add_sw_template(network_policy_name,
                                                                                            sw_name_final,
                                                                                            device_template_name,
                                                                                            node_1.cli_type) == 1, \
                f"Failed to add switch template with model: {device_template_name}"
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.device_templ_advanced_settings(network_policy_name,
                                                                                                    device_template_name,
                                                                                                    node_1.cli_type,
                                                                                                    upgrade_device_upon_auth=True,
                                                                                                    upload_auto=True,
                                                                                                    sw_model=sw_name_final)

            logger.info(
                "Change STP forward delay value; this change will be used to check if config push has been successfully")
            xiq_fw_delay = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template_device_config_forw_delay(
                network_policy_name,
                device_template_name)
            logger.info(f"STP forward delay has been configured in device template: {xiq_fw_delay}")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            utils.wait_till(timeout=5)

            if xiq_library_at_class_level.xflowscommonDevices.search_device(device_mac=node_1.mac, ignore_failure=True) == 1:
                xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)

            logger.step("Onboard device")
            xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(
                {**node_1, "location": test_bed.node_1_onboarding_location}, policy_name=network_policy_name)

            with test_bed.open_spawn(node_1) as spawn:
                cli.configure_device_to_connect_to_cloud(node_1.cli_type, test_bed.sw_connection_host, spawn, vr=node_1.mgmt_vr)

            utils.wait_till(timeout=600)
            logger.step("Wait for the update to finish")
            if xiq_library_at_class_level.xflowscommonDevices._check_update_network_policy_status(network_policy_name, node_1.mac, IRV=False) != 1:
                if xiq_library_at_class_level.xflowscommonDevices.update_device_delta_configuration(node_1.mac) != 1:
                    logger.fail(f"Failed to do a delta confguration update for this switch: '{node_1.mac}'.")
                
                if xiq_library_at_class_level.xflowscommonDevices._check_update_network_policy_status(network_policy_name, node_1.mac, IRV=False) != 1:
                    logger.fail(f"It looks like both type of device update failed for this switch: '{node_1.mac}'.")

            xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()
            utils.wait_till(timeout=15)

            with test_bed.open_spawn(node_1) as spawn:
                cli.downgrade_iqagent(node_1.cli_type, spawn)

            logger.step(
                "Check that all alarms and events are triggered and that config push and software update are triggered")
            logger.info("Get os version from device")
            os_version = xiq_library_at_class_level.xflowscommonDevices.get_device_row_values(node_1.mac, 'OS VERSION')
            nos_version = str(os_version['OS VERSION'])
            logger.info(f"device latest_os_version = {latest_image_version}")
            logger.info(f"device os_version = {nos_version}")
            assert nos_version in latest_image_version, f"The current device os version: {nos_version} is differet to the latest version {latest_image_version} after the update"
            
            dev_fw_delay = cli.get_nw_templ_device_config_forward_delay(node_1)
            logger.info(f"STP forward delay value configured on device after config push is: {dev_fw_delay}")
            assert dev_fw_delay == xiq_fw_delay, \
                f"Upload configuration automatically failed, STP forward delay value " \
                f"configured on XIQ is different: {xiq_fw_delay}"
            assert xiq_library_at_class_level.xflowsmanageDevice360.get_event_from_device360(
                node_1, "Download Config", event_type="config") != 1, "Download config event was not found in event table"
            assert xiq_library_at_class_level.xflowsmanageDevice360.get_event_from_device360(
                node_1, "firmware successful") != -1, "Download firmware successfull event was not found in event table"

        finally:
            delay_xiq = cli.set_nw_templ_device_config_forward_delay(node_1)
            logger.info(f"STP forward delay default value has been restored: {delay_xiq}")

            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            test_bed.add_switch_template_to_teardown(device_template_name)
            test_bed.add_network_policy_to_teardown(network_policy_name)
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)

    @pytest.mark.tcxm_20583
    def test_tcxm_20583(self, xiq_library_at_class_level, node_1, enter_switch_cli, cli, test_bed, logger, utils, poll):
        """
        tcxm_20583 - Verify that Option for "Upgrade to the specific device firmware version" is present.
        """
        network_policy_name = f"policy_XIQ1365_{test_bed.get_random_word()}"
        device_template_name = f"template_XIQ1365_{test_bed.get_random_word()}"

        try:
            with enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(node_1.name, 'disable iqagent', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to continue? (y/N)', confirmation_args='y')
                output_cmd = dev_cmd.send_cmd(node_1.name, 'show version', max_wait=10, interval=2)[0].return_text

            image_version = re.findall(r"IMG:\s+(\d+\.\d+\.\d+\.\d+)", output_cmd)[0]
            logger.info(f"Initial image version on device is {image_version}")

            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                network_policy_name)

            utils.wait_till(timeout=3)

            sw_name_final, _ = test_bed.generate_template_for_given_model(node_1)

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.add_sw_template(network_policy_name,
                                                                                            sw_name_final,
                                                                                            device_template_name,
                                                                                            node_1.cli_type) == 1, \
                f"Failed to add switch template with model: {device_template_name}"
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.device_templ_advanced_settings(network_policy_name,
                                                                                                    device_template_name,
                                                                                                    node_1.cli_type,
                                                                                                    upgrade_device_upon_auth=True,
                                                                                                    upload_auto=True,
                                                                                                    current_image_version=image_version,
                                                                                                    sw_model=sw_name_final)

            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

            utils.wait_till(timeout=5)
            if xiq_library_at_class_level.xflowscommonDevices.search_device(device_mac=node_1.mac, ignore_failure=True) == 1:
                xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)
                
            xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(
                {**node_1, "location": test_bed.node_1_onboarding_location}, policy_name=network_policy_name)
            xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()

            status_before = xiq_library_at_class_level.xflowscommonDevices.get_device_updated_status(
                device_mac=node_1.serial)

            with test_bed.open_spawn(node_1) as spawn:
                cli.configure_device_to_connect_to_cloud(node_1.cli_type, test_bed.sw_connection_host, spawn, vr=node_1.mgmt_vr)

            utils.wait_till(timeout=600)
            logger.step("Wait for the update to finish")
            if xiq_library_at_class_level.xflowscommonDevices._check_update_network_policy_status(network_policy_name, node_1.mac, IRV=False) != 1:
                if xiq_library_at_class_level.xflowscommonDevices.update_device_delta_configuration(node_1.mac) != 1:
                    logger.fail(f"Failed to do a delta confguration update for this switch: '{node_1.mac}'.")
                
                if xiq_library_at_class_level.xflowscommonDevices._check_update_network_policy_status(network_policy_name, node_1.mac, IRV=False) != 1:
                    logger.fail(f"It looks like both type of device update failed for this switch: '{node_1.mac}'.")

            with test_bed.open_spawn(node_1) as spawn:
                cli.downgrade_iqagent(node_1.cli_type, spawn)
                
            xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()

            xiq_library_at_class_level.xflowscommonDevices.check_update_column_change(node_1.serial, status_before)

            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_1.serial) == 1, \
                f"Device {node_1} didn't get online"
            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_1.serial) == 1, \
                f"Device {node_1} didn't get in MANAGED state"

            xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()
            utils.wait_till(timeout=5)

            try:
                for status in poll(lambda: xiq_library_at_class_level.xflowscommonDevices.get_device_status(node_1.serial), max_poll_time=300):
                    if status == "green":
                        break
            except:
                logger.fail(f"The EXOS device did not come up successfully in the XIQ; Device: {node_1}")

            assert xiq_library_at_class_level.xflowsmanageDevice360.get_event_from_device360(node_1, "Download Config",
                                                                                             event_type="config") != -1, "Download config event was not found in event table"
            assert xiq_library_at_class_level.xflowsmanageDevice360.get_event_from_device360(node_1,
                                                                                             "firmware successful") != -1, "Download firmware successfull event was not found in event table"
        finally:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

            test_bed.add_switch_template_to_teardown(device_template_name)
            test_bed.add_network_policy_to_teardown(network_policy_name)
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)

    @pytest.mark.tcxm_20589
    def test_tcxm_20589(self, xiq_library_at_class_level, node_1, enter_switch_cli, cli, test_bed, logger, utils):
        """
        tcxm_20589 - Check that the Upgrade firmware and Upload Configuration automatically functions are triggered after node_1 transitions from unmanaged to managed.
        """
        network_policy_name = f"policy_XIQ1365_{test_bed.get_random_word()}"
        device_template_name = f"template_XIQ1365_{test_bed.get_random_word()}"
        sw_name_final, _ = test_bed.generate_template_for_given_model(node_1)

        try:
            logger.step("Check test preconditions")
            with enter_switch_cli(node_1) as dev_cmd:
                output_1 = dev_cmd.send_cmd(node_1.name, 'show version | grep IMG')
                check_image_version = output_1[0].return_text
                image_version_regex = 'IMG:([ ]{1,}.{0,})'
                image_version = utils.get_regexp_matches(check_image_version, image_version_regex, 1)[0]
                device_image_version = image_version.replace(utils.get_regexp_matches(image_version, '([ ])')[0], '')
                device_image_version = device_image_version.strip()

            latest_image_version, image_versions = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.get_latest_firmware_version_from_switch_template(
                sw_name_final)
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            image_version = device_image_version
            
            if device_image_version in latest_image_version:

                with test_bed.open_spawn(node_1) as spawn:
                    cli.downgrade_iqagent(node_1.cli_type, spawn)
                    cli.configure_device_to_connect_to_cloud(node_1.cli_type, test_bed.sw_connection_host, spawn, vr=node_1.mgmt_vr)
                
                if xiq_library_at_class_level.xflowscommonDevices.search_device(device_mac=node_1.mac, ignore_failure=True) == 1:
                    xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)
                    
                xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick({**node_1, "location": test_bed.node_1_onboarding_location})

                test_upgrade_version = None
                for version in image_versions:
                    if version and (device_image_version not in version):
                        test_upgrade_version = version.split('-')[1].replace('.xos', '').replace('(GLOBAL)', '').strip()
                        break
                else:
                    logger.fail("Failed to find a system version for this test case")

                xiq_library_at_class_level.xflowsmanageDevices.upgrade_device(node_1, version=test_upgrade_version)
                image_version = test_upgrade_version
                utils.wait_till(timeout=600)
                
                assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_1.serial) == 1, \
                    f"Device {node_1} didn't get online"
                assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_1.serial) == 1, \
                    f"Device {node_1} didn't get in MANAGED state"

                xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)
                
                with test_bed.open_spawn(node_1) as spawn:
                    cli.downgrade_iqagent(node_1.cli_type, spawn)
                    
            logger.info(f"Initial image version on device is {image_version}")

            assert xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                network_policy_name) == 1, "Failed to create Switching and Routing network policy"

            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.add_sw_template(network_policy_name,
                                                                                            sw_name_final,
                                                                                            device_template_name,
                                                                                            node_1.cli_type) == 1, \
                f"Failed to add switch template with model: {sw_name_final}"
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.device_templ_advanced_settings(network_policy_name,
                                                                                                    device_template_name,
                                                                                                    node_1.cli_type,
                                                                                                    upgrade_device_upon_auth=True,
                                                                                                    upload_auto=True)
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

            logger.step("Onboard the node_1 without assigning the network policy configured.")
            if xiq_library_at_class_level.xflowscommonDevices.search_device(device_mac=node_1.mac, ignore_failure=True) == 1:
                xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)
                
            xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(
                {**node_1, "location": test_bed.node_1_onboarding_location})

            with test_bed.open_spawn(node_1) as spawn:
                cli.configure_device_to_connect_to_cloud(node_1.cli_type, test_bed.sw_connection_host, spawn, vr=node_1.mgmt_vr)
                
            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_1.serial) == 1, \
                f"Device {node_1} didn't get online"

            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_1.serial) == 1, \
                f"Device {node_1} didn't get in MANAGED state"

            assert xiq_library_at_class_level.xflowscommonDevices.change_manage_device_status(
                manage_type="UNMANAGE", device_serial=node_1.serial) == 1, f"Failed to change Management status of {node_1} in UNMANAGE"

            assert xiq_library_at_class_level.xflowsmanageDevices.assign_network_policy_to_switch_mac(
                policy_name=network_policy_name, mac=node_1.mac) == 1, f"Failed to assign network policy to {node_1}"

            assert xiq_library_at_class_level.xflowscommonDevices.change_manage_device_status(
                manage_type="MANAGE", device_serial=node_1.serial) == 1, f"Failed to change Management status of {node_1} in MANAGE"

            utils.wait_till(timeout=600)
            logger.step("Wait for the update to finish")
            if xiq_library_at_class_level.xflowscommonDevices._check_update_network_policy_status(network_policy_name, node_1.mac, IRV=False) != 1:
                if xiq_library_at_class_level.xflowscommonDevices.update_device_delta_configuration(node_1.mac) != 1:
                    logger.fail(f"Failed to do a delta confguration update for this switch: '{node_1.mac}'.")
                
                if xiq_library_at_class_level.xflowscommonDevices._check_update_network_policy_status(network_policy_name, node_1.mac, IRV=False) != 1:
                    logger.fail(f"It looks like both type of device update failed for this switch: '{node_1.mac}'.")

            with test_bed.open_spawn(node_1) as spawn:
                cli.downgrade_iqagent(node_1.cli_type, spawn)
                
            xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()
            utils.wait_till(timeout=15)
            
            logger.info("Get OS version from device")
            os_version = xiq_library_at_class_level.xflowscommonDevices.get_device_row_values(node_1.mac, 'OS VERSION')
            nos_version = str(os_version['OS VERSION'])
            logger.info(f"Device os_version = {nos_version}")

            latest_os_version = xiq_library_at_class_level.xflowscommonDevices.get_latest_version_from_device_update(
                node_1)
            logger.info(f"Device latest_os_version = {latest_os_version}")

            assert xiq_library_at_class_level.xflowsmanageDevice360.get_event_from_device360(
                node_1, "firmware successful", ignore_failure=True) != -1, \
                "The IQAgent unresponsive event was not triggered!"

        finally:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            test_bed.add_switch_template_to_teardown(device_template_name)
            test_bed.add_network_policy_to_teardown(network_policy_name)
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)

    @pytest.mark.tcxm_20590
    def test_tcxm_20590(self, xiq_library_at_class_level, node_1, utils, enter_switch_cli, cli, logger, test_bed):
        """
        tcxm_20590 - Check for the Upgrade firmware and Upload Configuration automatically functions are not
                    triggered if the procedure is already made and device is switched from managed to unmanaged
                    and from unmanaged to managed back.
        """
        network_policy_name = f"policy_XIQ1365_{test_bed.get_random_word()}"
        device_template_name = f"template_XIQ1365_{test_bed.get_random_word()}"
        sw_name_final, _ = test_bed.generate_template_for_given_model(node_1)

        try:
            logger.step("Check test preconditions")
            with enter_switch_cli(node_1) as dev_cmd:
                output_1 = dev_cmd.send_cmd(node_1.name, 'show version | grep IMG')
                check_image_version = output_1[0].return_text
                image_version_regex = 'IMG:([ ]{1,}.{0,})'
                image_version = utils.get_regexp_matches(check_image_version, image_version_regex, 1)[0]
                device_image_version = image_version.replace(utils.get_regexp_matches(image_version, '([ ])')[0], '')
                device_image_version = device_image_version.strip()

            latest_image_version, image_versions = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.get_latest_firmware_version_from_switch_template(
                sw_name_final)
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            
            if device_image_version in latest_image_version:

                with test_bed.open_spawn(node_1) as spawn:
                    cli.downgrade_iqagent(node_1.cli_type, spawn)
                    cli.configure_device_to_connect_to_cloud(node_1.cli_type, test_bed.sw_connection_host, spawn, vr=node_1.mgmt_vr)
                
                if xiq_library_at_class_level.xflowscommonDevices.search_device(device_mac=node_1.mac, ignore_failure=True) == 1:
                    xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)
                
                xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick({**node_1, "location": test_bed.node_1_onboarding_location})

                test_upgrade_version = None
                for version in image_versions:
                    if version and (device_image_version not in version):
                        test_upgrade_version = version.split('-')[1].replace('.xos', '').replace('(GLOBAL)', '').strip()
                        break
                else:
                    logger.fail("Failed to find a system version for this test case")

                xiq_library_at_class_level.xflowsmanageDevices.upgrade_device(node_1, version=test_upgrade_version)
                utils.wait_till(timeout=600)
                
                assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_1.serial) == 1, \
                    f"Device {node_1} didn't get online"
                assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_1.serial) == 1, \
                    f"Device {node_1} didn't get in MANAGED state"

                xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)

                with test_bed.open_spawn(node_1) as spawn:
                    cli.downgrade_iqagent(node_1.cli_type, spawn)

            with enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(node_1.name, 'disable iqagent', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to continue? (y/N)', confirmation_args='y')
                output_cmd = dev_cmd.send_cmd(node_1.name, 'show version', max_wait=10, interval=2)[0].return_text
            
            image_version = re.findall(r"IMG:\s+(\d+\.\d+\.\d+\.\d+)", output_cmd)[0]
            logger.info(f"Initial image version on device is {image_version}")

            assert xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                network_policy_name) == 1, \
                "Failed to create Switching and Routing network policy"
            assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.add_sw_template(network_policy_name,
                                                                                            sw_name_final,
                                                                                            device_template_name,
                                                                                            node_1.cli_type) == 1, \
                f"Failed to add switch template with model: {sw_name_final}"
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.device_templ_advanced_settings(network_policy_name,
                                                                                                    device_template_name,
                                                                                                    node_1.cli_type,
                                                                                                    upgrade_device_upon_auth=True,
                                                                                                    upload_auto=True)

            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            if xiq_library_at_class_level.xflowscommonDevices.search_device(device_mac=node_1.mac, ignore_failure=True) == 1:
                xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)
                
            xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(
                {**node_1, "location": test_bed.node_1_onboarding_location}, policy_name=network_policy_name)

            with test_bed.open_spawn(node_1) as spawn:
                cli.configure_device_to_connect_to_cloud(node_1.cli_type, test_bed.sw_connection_host, spawn, vr=node_1.mgmt_vr)
                
            xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()

            utils.wait_till(timeout=600)
            logger.step("Wait for the update to finish")
            if xiq_library_at_class_level.xflowscommonDevices._check_update_network_policy_status(network_policy_name, node_1.mac, IRV=False) != 1:
                if xiq_library_at_class_level.xflowscommonDevices.update_device_delta_configuration(node_1.mac) != 1:
                    logger.fail(f"Failed to do a delta confguration update for this switch: '{node_1.mac}'.")
                
                if xiq_library_at_class_level.xflowscommonDevices._check_update_network_policy_status(network_policy_name, node_1.mac, IRV=False) != 1:
                    logger.fail(f"It looks like both type of device update failed for this switch: '{node_1.mac}'.")

            xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()
            utils.wait_till(timeout=15)

            with test_bed.open_spawn(node_1) as spawn:
                cli.downgrade_iqagent(node_1.cli_type, spawn)

            logger.info("Get os version from device")
            os_version = xiq_library_at_class_level.xflowscommonDevices.get_device_row_values(node_1.mac, 'OS VERSION')
            nos_version = str(os_version['OS VERSION'])
            logger.info(f"Device OS version after upgrade is {nos_version}")

            latest_os_version = xiq_library_at_class_level.xflowscommonDevices.get_latest_version_from_device_update(
                node_1)
            logger.info(f"Latest OS image version from XIQ is {latest_os_version}")

            assert xiq_library_at_class_level.xflowsmanageDevice360.get_event_from_device360(
                node_1, "firmware successful", ignore_failure=True, ) != -1, "Message 'Firmware successful' was not triggered in Monitor->Events!"
            assert xiq_library_at_class_level.xflowsmanageDevice360.get_event_from_device360(
                node_1, "Download Config", ignore_failure=True, event_type="config") != -1, "Message 'Download config' was not triggered in Monitor->Events!"
            
            with test_bed.open_spawn(node_1) as spawn:
                cli.downgrade_iqagent(node_1.cli_type, spawn)
                
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            assert xiq_library_at_class_level.xflowscommonDevices.change_manage_device_status(manage_type="UNMANAGE",
                                                                                              device_serial=node_1.serial) == 1, \
                f"Failed to change Management status of {node_1} in UNMANAGE"
            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_offline(node_1.serial) == 1, \
                f"Device {node_1} didn't get in 'Disconnect' state"
            assert xiq_library_at_class_level.xflowscommonDevices.change_manage_device_status(manage_type="MANAGE",
                                                                                              device_serial=node_1.serial) == 1, \
                f"Failed to change Management status of {node_1} in MANAGE"
            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_1.serial) != -1, \
                f"Device {node_1} didn't get 'Online'"
            assert xiq_library_at_class_level.xflowscommonDevices.wait_until_device_managed(node_1.serial) != -1, \
                f"Device {node_1} didn't get in 'MANAGED' state"

            status_after_manange_unamanage = xiq_library_at_class_level.xflowscommonDevices.get_device_updated_status(
            device_mac=node_1.mac)
            assert "Firmware Updating" not in status_after_manange_unamanage, "The device is doing Firmware Update after manage/unamange and it should not do this."
            
        finally:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            test_bed.add_switch_template_to_teardown(device_template_name)
            test_bed.add_network_policy_to_teardown(network_policy_name)
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)

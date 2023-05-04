import pytest
import random
import string


@pytest.fixture
def make_sure_windows_are_closed(xiq_library_at_class_level, auto_actions):
    """ This fixture makes sure that the honeycomb/device360 windows are closed at the TEARDOWN of the test case.
    This way the next test case won't be affected if the current test failed and did not close all the windows during its call.
    """
    try:
        yield
    finally:
        try:
            if btn := xiq_library_at_class_level.xflowsmanageDevice360.get_cancel_port_type_box():
                auto_actions.click(btn)
        except:
            # close button not found
            pass

        try:
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
        except:
            # device360 window is not opened
            pass


@pytest.mark.p1
@pytest.mark.development
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class Xiq1053OneNodeTests:

    @pytest.fixture
    def setup_lldp(self, node_1, logger, dut_ports, bounce_iqagent, set_lldp):
        try:
            try:
                ports = sorted(dut_ports[node_1.name],
                               key=int if node_1.cli_type.upper() == "EXOS" else (
                                   lambda x: int(x.split("/")[1])))
                set_lldp(node_1, ports, action="disable")
                bounce_iqagent(node_1)
            except Exception as exc:
                logger.warning(repr(exc))

            yield

        finally:

            try:
                ports = sorted(dut_ports[node_1.name],
                               key=int if node_1.cli_type.upper() == "EXOS" else (
                                   lambda x: int(x.split("/")[1])))
                set_lldp(node_1, ports, action="enable")
                bounce_iqagent(node_1)
            except Exception as exc:
                logger.warning(repr(exc))

    @pytest.mark.tcxm_17588
    def test_tcxm_17588(self, xiq_library_at_class_level, logger, node_1, node_1_policy_name, dut_ports,
                        bounce_iqagent, setup_lldp, make_sure_windows_are_closed):
        """
        TCXM-17588
        Test Description: Configure "none" option in "Native" for trunk ports in device level configuration
        Author: vstefan
        """

        xiq = xiq_library_at_class_level
        xiq_d360 = xiq.xflowsmanageDevice360

        allowed_vlan = str(random.choice(range(1024, 4096)))
        configured_port = str(random.choice(dut_ports['dut1']))

        if node_1.cli_type.upper() == 'EXOS':
            expected_cli_commands = [f"configure vlan {allowed_vlan} add port {configured_port} tagged"]
        else:
            expected_cli_commands = ["enable",
                                     "configure terminal",
                                     f"vlan members add {allowed_vlan} {configured_port} portmember"]

        try:
            try:
                logger.info("Go to device360 port configuration")
                xiq_d360.go_to_device_360_port_config(dut=node_1)

                logger.info(f"For port {configured_port} set port_type='Trunk', native_vlan='none', "
                            f"allowed_vlans='{allowed_vlan}'")
                xiq_d360.enter_port_type_and_vlan_id(port=configured_port,
                                                     port_type="Trunk Port",
                                                     native_vlan="none",
                                                     allowed_vlans=allowed_vlan,
                                                     device_os=node_1.cli_type.upper())

                logger.info(f"Successfully configured port {configured_port}")

            finally:

                assert xiq_d360.save_device_360_port_config() == 1, f"Failed to Save the Port Configuration"
                xiq.Utils.wait_till(timeout=5)
                assert xiq_d360.close_device360_window() == 1, f"Failed to Close D360 window"
                logger.info("Saved the device360 port configuration and closed the window.")

            logger.info(f"Verify that these commands are found in the delta cli: {expected_cli_commands}")
            assert xiq.xflowsmanageDeviceConfig.verify_delta_cli_commands(dut=node_1,
                                                                          commands=expected_cli_commands) == 1, \
                f"Command not found in delta cli"

            logger.info("Push configuration to the switch and wait")
            xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_1_policy_name, dut=node_1)

            logger.info("Check if the port was removed from vlan from CLI")
            assert xiq.Cli.verify_port_removed_from_vlan(dut=node_1, port=configured_port,
                                                         port_type="trunk", allowed_vlans=allowed_vlan) == 1, \
                f"Port {configured_port} not removed from vlan {allowed_vlan}"

            for _ in range(7):

                try:

                    logger.info(f"Get VLAN data from device360 tabular view for port {configured_port} of {node_1}")
                    bounce_iqagent(node_1)
                    port_data = xiq_d360.get_vlan_data_from_device_360_tabular_view(dut=node_1,
                                                                                    port=configured_port)
                    logger.info(f"Data found: {port_data}")

                    logger.info("Verify that the port configuration appears correctly in the device360 port table")
                    assert port_data["port_mode"].upper() == "TRUNK", \
                        f"Expected port_mode to be trunk but found {port_data['port_mode']}"
                    assert port_data["port_access_vlan"].upper() == "NONE", \
                        f"Expected port_access_vlan to be none but found {port_data['port_access_vlan']}"

                    tagged_vlans = []
                    [tagged_vlans.extend(list(range(int(vlan.split("-")[0]),
                                                    int(vlan.split("-")[1]) + 1))) if "-" in vlan
                     else tagged_vlans.append(int(vlan)) for vlan in port_data["port_tagged_vlan"].split(",")]

                    logger.info("Check if the expected vlan is found in the device360 port table")
                    assert int(allowed_vlan) in tagged_vlans, \
                        f"Expected port_tagged_vlan to be {allowed_vlan} but found {port_data['port_tagged_vlan']}"

                except Exception as exc:
                    logger.warning(repr(exc))
                    xiq.Utils.wait_till(timeout=30)

                else:
                    break
            else:
                assert False, "Failed to verify the port configuration in monitor overview of device 360"

        finally:
            logger.info(f"Performing test cleanup")
            xiq.xflowscommonNavigator.navigate_to_devices()
            xiq.xflowsmanageDevices.revert_device_to_template(node_1.mac)

    @pytest.mark.tcxm_17589
    def test_tcxm_17589(self, xiq_library_at_class_level, logger, node_1, node_1_policy_name, dut_ports,
                        node_1_template_name, setup_lldp, make_sure_windows_are_closed):
        """
        TCXM-17589
        Test Description: Configure "none" option in "VLAN ID" for user-defined trunk port
        in template level configuration
        Author: vstefan
        """

        xiq = xiq_library_at_class_level
        xiq_d360 = xiq.xflowsmanageDevice360
        xiq_st = xiq.xflowsconfigureSwitchTemplate

        configured_port = str(random.choice(dut_ports['dut1']))
        allowed_vlan = str(random.choice(range(1024, 4096)))
        port_type_name_with_none = \
            f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"
        default_port_type = "Auto-sense" if node_1.cli_type.upper() == "VOSS" else "Access"

        try:
            logger.info(f"Go to the port configuration of {node_1_template_name} template")
            xiq_st.select_sw_template(nw_policy=node_1_policy_name, sw_template=node_1_template_name, cli_type=node_1.cli_type.upper())
            xiq_st.go_to_port_configuration()

            if node_1.cli_type.upper() == "VOSS":
                vlan_id = str(random.choice(range(1024, 4096)))
                port_type_name_with_vlan_id = \
                    f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"

                expected_cli_commands = ["enable",
                                         "configure terminal",
                                         f'vlan members add {allowed_vlan} {configured_port} portmember']

                logger.info(
                    f"Create a new port type for port {configured_port}: port_type='trunk', "
                    f"native_vlan_id={vlan_id}, port_type_name={port_type_name_with_vlan_id}")

                assert xiq_d360.create_port_type_with_custom_vlan_values(port=configured_port,
                                                                         port_type_name=port_type_name_with_vlan_id,
                                                                         port_type="trunk",
                                                                         native_vlan_id=vlan_id) == 1, \
                    f"Failed to create the port type"
                xiq.Utils.wait_till(timeout=5)
                xiq_st.switch_template_save()
                xiq.Utils.wait_till(timeout=10)
                logger.info("Successfully saved the port config at template level")

                logger.info("Push the changes to the dut and wait")
                xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_1_policy_name, dut=node_1)

                logger.info(f"Go to the port configuration of {node_1_template_name} template")
                xiq_st.select_sw_template(nw_policy=node_1_policy_name, sw_template=node_1_template_name, cli_type=node_1.cli_type.upper())
                xiq_st.go_to_port_configuration()

            else:
                expected_cli_commands = [rf"configure vlan\s\d*\sdelete port {configured_port}",
                                         f"configure vlan {allowed_vlan} add port {configured_port} tagged"]

            try:
                logger.info(f"Create a new trunk port type named {port_type_name_with_none}")
                xiq_d360.open_new_port_type_editor(port=configured_port)
                xiq_d360.configure_port_name_usage_tab(port_type_name=port_type_name_with_none,
                                                       port_type="trunk")
                xiq_d360.go_to_next_editor_tab()

                logger.info("Set native vlan id to none")
                xiq_d360.set_native_vlan_id(native_vlan_id="none")

                logger.info(f"Set allowed vlans to {allowed_vlan}")
                xiq_d360.set_allowed_vlans(allowed_vlans_value=allowed_vlan)

                logger.info("Navigate to 'Summary' page")
                xiq_d360.go_to_last_page()

                expected_summary = {"Port Usage": "Trunk",
                                    "Native VLAN": "none",
                                    "Allowed VLANs": allowed_vlan,
                                    "VLAN": ""}
                logger.info(f"Expected summary: {expected_summary}")

                summary = xiq_d360.get_vlan_settings_summary()

                logger.info("Verify that the configured fields appear correctly in the summary tab")
                assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones. " \
                    f"Expected summary: {expected_summary}\nFound summary: {summary}"
                logger.info("Successfully verified the summary")

            finally:
                xiq_d360.save_port_type_config()
                xiq.Utils.wait_till(timeout=5)
                xiq_st.switch_template_save()
                xiq.Utils.wait_till(timeout=10)
                logger.info("Saved the port configuration at template level")

            logger.info(f"Verify that these commands are found in the delta cli: {expected_cli_commands}")
            xiq.xflowsmanageDeviceConfig.verify_delta_cli_commands(dut=node_1,
                                                                   commands=expected_cli_commands)

            logger.info("Push the changes to the device and wait")
            xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_1_policy_name,
                                                           dut=node_1)

            logger.info("Check if the expected vlan is found in the device360 port table")
            xiq.Cli.verify_port_removed_from_vlan(dut=node_1,
                                                  port=configured_port,
                                                  allowed_vlans=allowed_vlan,
                                                  port_type="trunk")

        finally:
            logger.info("Performing test cleanup")
            logger.info(f"Go to the port configuration of {node_1_template_name} template")
            xiq_st.select_sw_template(node_1_policy_name, node_1_template_name, cli_type=node_1.cli_type.upper())
            xiq_st.go_to_port_configuration()

            logger.info(f"Set {configured_port} port type to '{default_port_type} Port'")
            xiq_st.revert_port_configuration_template_level(f"{default_port_type} Port")
            xiq.Utils.wait_till(timeout=5)

            xiq_st.switch_template_save()
            xiq.Utils.wait_till(timeout=10)

            logger.info("Saved the port type configuration, now push the changes to the device")
            xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_1_policy_name, dut=node_1)

            try:
                if node_1.cli_type.upper() == "VOSS":
                    logger.info(f"Delete port type profile: {port_type_name_with_vlan_id}")
                    xiq.xflowsconfigureCommonObjects.delete_port_type_profile(
                        port_type_name=port_type_name_with_vlan_id)

                logger.info(f"Delete port type profile: {port_type_name_with_none}")
                xiq.xflowsconfigureCommonObjects.delete_port_type_profile(port_type_name_with_none)
            except Exception as e:
                logger.warning(repr(e))

    @pytest.mark.dependson("tcxm_17588")
    @pytest.mark.tcxm_17590
    def test_tcxm_17590(self, logger):
        """
        TCXM-17588
        Test Description: Configure "none" option in "Native" for trunk ports in device level configuration
        Author: dpetrescu
        """

        logger.info("This testcase is covered by test 17588")

    @pytest.mark.dependson("tcxm_17589")
    @pytest.mark.tcxm_17591
    def test_tcxm_17591(self, logger):
        """
        TCXM-17591
        Test Description: Configure "none" option in "VLAN ID" for user-defined trunk port
                          in template level configuration
        Author: vstefan
        """

        logger.info("This testcase is covered by test 17589")

    @pytest.mark.tcxm_17596
    @pytest.mark.tcxm_17597
    def test_tcxm_17596(self, xiq_library_at_class_level, logger, node_1, node_1_policy_name, dut_ports,
                        setup_lldp, test_data, make_sure_windows_are_closed):
        """
        TCXM-17596
        Test Description: Configure "none" option in "VLAN" for access port in device level configuration
        Author: kbr

        TCXM-17597
        Test Description: Configure "none" option in "VLAN" for access port in device level configuration
        Author: kbr
        """

        if node_1.cli_type.upper() != "VOSS":
            pytest.skip(f"Expected a VOSS switch for {test_data['tc']} test case.")

        xiq = xiq_library_at_class_level
        xiq_d360 = xiq.xflowsmanageDevice360

        configured_port = str(random.choice(dut_ports['dut1']))
        port_type_xiq = 'Onboarding Port' if test_data['port_type'] == 'onboarding' else 'Disabled Port'
        port_type_cli = test_data['port_type']

        try:
            try:
                logger.info("Go to device360 port configuration")
                xiq_d360.go_to_device_360_port_config(node_1)
                logger.info(f"For port {configured_port} set port_type='{port_type_xiq} Port'")
                xiq_d360.enter_port_type_and_vlan_id(port=configured_port,
                                                     port_type=port_type_xiq,
                                                     device_os=node_1.cli_type.upper())
                logger.info(f"Successfully configured port {configured_port}")
            finally:
                assert xiq_d360.save_device_360_port_config() == 1, f"Failed to Save the Port Configuration"
                xiq.Utils.wait_till(timeout=5)
                assert xiq_d360.close_device360_window() == 1, f"Failed to Close D360 window"
                logger.info("Saved the device360 port configuration and closed the window.")

            logger.info("Push configuration to the switch and wait")
            xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_1_policy_name,
                                                           dut=node_1)

            try:
                logger.info("Go to device360 port configuration")
                xiq_d360.go_to_device_360_port_config(dut=node_1)

                logger.info(f"For port {configured_port} set port_type='{port_type_xiq}', native_vlan='none', "
                            f"allowed_vlans='none'")
                xiq_d360.enter_port_type_and_vlan_id(port=configured_port,
                                                     port_type=port_type_xiq,
                                                     access_vlan_id="none",
                                                     device_os=node_1.cli_type.upper())
                logger.info(f"Successfully configured port {configured_port}")
            finally:
                assert xiq_d360.save_device_360_port_config() == 1, f"Failed to Save the Port Configuration"
                xiq.Utils.wait_till(timeout=5)
                assert xiq_d360.close_device360_window() == 1, f"Failed to Close D360 window"
                logger.info("Saved the device360 port configuration and closed the window.")

            expected_cli_commands = [rf"vlan members remove \d+ {configured_port} portmember"]

            logger.info(f"Verify that these commands are found in the delta cli: {expected_cli_commands}")
            assert xiq.xflowsmanageDeviceConfig.verify_delta_cli_commands(dut=node_1,
                                                                          commands=expected_cli_commands) == 1, \
                f"Command not found in delta cli"

            logger.info("Push configuration to the switch and wait")
            xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_1_policy_name, dut=node_1)

            logger.info("Check if the port was removed from vlan from CLI")
            xiq.Cli.verify_port_removed_from_vlan(dut=node_1,
                                                  port=configured_port,
                                                  port_type=port_type_cli)

        finally:
            logger.info(f"Performing test cleanup")
            xiq.xflowscommonNavigator.navigate_to_devices()
            xiq.xflowsmanageDevices.revert_device_to_template(node_1.mac)

    @pytest.mark.tcxm_17598
    def test_tcxm_17598(self, xiq_library_at_class_level, logger, node_1, node_1_policy_name, dut_ports,
                        setup_lldp, make_sure_windows_are_closed):

        """

        TCXM-17598
        Test Description: Configure "none" option in "Native" for user-defined trunk port in device level configuration
        Author: kbr

        """

        xiq = xiq_library_at_class_level
        xiq_d360 = xiq.xflowsmanageDevice360

        allowed_vlan = str(random.choice(range(1024, 4096)))
        configured_port = str(random.choice(dut_ports['dut1']))
        port_type_name = f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"

        if node_1.cli_type.upper() == 'EXOS':
            expected_cli_commands = [rf"configure vlan\s\d*\sdelete port {configured_port}",
                                     f"configure vlan {allowed_vlan} add port {configured_port} tagged"]
        else:
            expected_cli_commands = ["enable",
                                     "configure terminal",
                                     f'vlan members add {allowed_vlan} {configured_port} portmember']

        try:
            try:
                logger.info("Go to device360 port configuration")
                xiq_d360.go_to_device_360_port_config(dut=node_1)

                logger.info(f"Create a new trunk port type named {port_type_name}")

                xiq_d360.open_new_port_type_editor(port=configured_port,
                                                   device_360=True)
                xiq_d360.configure_port_name_usage_tab(port_type_name=port_type_name,
                                                       port_type="trunk")
                xiq_d360.go_to_next_editor_tab()

                logger.info("Set native vlan id to none")
                xiq_d360.set_native_vlan_id(native_vlan_id="none")

                logger.info(f"Set allowed vlans to {allowed_vlan}")
                xiq_d360.set_allowed_vlans(allowed_vlans_value=allowed_vlan)

                logger.info("Navigate to 'Summary' page")
                xiq_d360.go_to_last_page()

                expected_summary = {'Port Usage': 'Trunk',
                                    'Native VLAN': 'none',
                                    'Allowed VLANs': allowed_vlan,
                                    'VLAN': ''}
                logger.info(f"Expected summary: {expected_summary}")

                summary = xiq_d360.get_vlan_settings_summary()

                logger.info("Verify that the configured fields appear correctly in the summary tab")
                assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones. " \
                    f"Expected summary: {expected_summary}\nFound summary: {summary}"
                logger.info("Successfully verified the summary")

            finally:
                xiq_d360.save_port_type_config()
                xiq.Utils.wait_till(timeout=5)
                assert xiq_d360.save_device_360_port_config() == 1, f"Failed to Save the Port Configuration"
                xiq.Utils.wait_till(timeout=5)
                assert xiq_d360.close_device360_window() == 1, f"Failed to Close D360 window"
                logger.info("Saved the device360 port configuration and closed the window.")

            logger.info(f"Verify that these commands are found in the delta cli: {expected_cli_commands}")
            xiq.xflowsmanageDeviceConfig.verify_delta_cli_commands(dut=node_1, commands=expected_cli_commands)

            logger.info("Push the changes to the device and wait")
            xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_1_policy_name, dut=node_1)

            logger.info("Check if the port was removed from vlan from CLI")
            xiq.Cli.verify_port_removed_from_vlan(dut=node_1,
                                                  port=configured_port,
                                                  allowed_vlans=allowed_vlan,
                                                  port_type="trunk")

        finally:

            logger.info("Performing test cleanup")
            xiq.xflowscommonNavigator.navigate_to_devices()
            xiq.xflowsmanageDevices.revert_device_to_template(node_1.mac)

            try:
                logger.info(f"Remove port type profile {port_type_name}")
                xiq.xflowsconfigureCommonObjects.delete_port_type_profile(port_type_name)

            except Exception as e:
                logger.warning(repr(e))

    @pytest.mark.dependson("tcxm_17598")
    @pytest.mark.tcxm_17600
    def test_tcxm_17600(self, logger):
        """
        TCXM-17600
        Test Description: Configure "none" option in "Native" for user-defined trunk port in device level configuration
        Author: kbr
        """

        logger.info("This testcase is covered by test 17598")

    @pytest.mark.tcxm_17606
    def test_tcxm_17606(self, xiq_library_at_class_level, logger, node_1, node_1_policy_name, dut_ports,
                        setup_lldp, bounce_iqagent, make_sure_windows_are_closed):

        """
        TCXM-17606
        Test Description: Verify the port is added as tagged to all other existing vlans in XIQ
        Author: vstefan
        """

        xiq = xiq_library_at_class_level
        xiq_d360 = xiq.xflowsmanageDevice360

        configured_port = str(random.choice(dut_ports['dut1']))
        port_type_name = f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"

        try:
            try:
                logger.info("Go to device360 port configuration")
                xiq_d360.go_to_device_360_port_config(dut=node_1)

                logger.info(f"For port {configured_port} create a new port type: port_type_name={port_type_name}, "
                            f"port_type=trunk, native_vlan_id=none, allowed_vlans=all")
                xiq_d360.create_port_type_with_custom_vlan_values(port=configured_port,
                                                                  port_type_name=port_type_name,
                                                                  port_type="trunk",
                                                                  native_vlan_id="none",
                                                                  allowed_vlans="all",
                                                                  device_360=True)

            finally:
                assert xiq_d360.save_device_360_port_config() == 1, f"Failed to Save the Port Configuration"
                xiq.Utils.wait_till(timeout=5)
                assert xiq_d360.close_device360_window() == 1, f"Failed to Close D360 window"
                logger.info("Closed the device360 window")

            logger.info("Push configuration to the switch and wait")
            xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_1_policy_name, dut=node_1)

            for _ in range(7):
                try:
                    logger.info(f"Get vlan data from device360 tabular view for port {configured_port} of {node_1}")
                    bounce_iqagent(node_1)
                    port_data = xiq_d360.get_vlan_data_from_device_360_tabular_view(dut=node_1,
                                                                                    port=configured_port)

                    logger.info(f"Verify that the port configuration of port {configured_port} appears correctly")
                    assert port_data["port_mode"].lower() == "trunk", \
                        f"Expected port_mode to be trunk but found {port_data['port_mode']}"
                    assert port_data["port_access_vlan"].lower() == "none", \
                        f"Expected port_access_vlan to be none but found {port_data['port_access_vlan']}"
                    logger.info(
                        "Successfully verified that the port configuration appear correctly "
                        "in the device360 port table")

                    tagged_vlans = []
                    [tagged_vlans.extend(list(range(*[int(x) for x in vlan.split("-")]))) if "-" in vlan
                     else tagged_vlans.append(int(vlan)) for vlan in port_data["port_tagged_vlan"].split(",")]

                    all_ports_data = {k: v for k, v in
                                      xiq_d360.get_vlan_data_from_device_360_tabular_for_all_ports(
                                          node_1).items() if k != "mgmt"}  # NOQA

                    configured_vlan_ids = list(
                        set([int(port_data["port_access_vlan"]) for port_data in all_ports_data.values()
                             if port_data["port_access_vlan"].isdigit()]))

                    if node_1.cli_type.upper() == "VOSS" and not configured_vlan_ids:
                        configured_vlan_ids = [1]
                    assert sorted(tagged_vlans) == sorted(configured_vlan_ids), \
                        f"Not all the configured vlan ids were found as tagged vlans for {configured_port} port"

                except Exception as e:
                    logger.warning(repr(e))
                else:
                    break
            else:
                assert False, "Failed to verify the port configuration in monitor overview of device 360"

        finally:

            logger.info("Performing test cleanup")
            xiq.xflowscommonNavigator.navigate_to_devices()
            xiq.xflowsmanageDevices.revert_device_to_template(node_1.mac)

            try:
                logger.info(f"Delete port type profile: {port_type_name}")
                xiq.xflowsconfigureCommonObjects.delete_port_type_profile(port_type_name)

            except Exception as e:
                logger.warning(repr(e))

    @pytest.mark.tcxm_19995
    def test_tcxm_19995(self, xiq_library_at_class_level, logger, node_1, node_1_policy_name, dut_ports,
                        set_lldp, bounce_iqagent, make_sure_windows_are_closed):

        """
        TCXM-19995
        Test Description: Configure "none" option in "VLAN" for access port in device level configuration
        Author: vstefan
        """

        if node_1.cli_type.upper() != "EXOS":
            pytest.skip("Expected an EXOS switch for the TCXM-19995 test case.")

        xiq = xiq_library_at_class_level
        xiq_d360 = xiq.xflowsmanageDevice360

        configured_port = str(random.choice(dut_ports['dut1']))

        try:
            try:
                logger.info("Go to device360 port configuration")
                xiq_d360.go_to_device_360_port_config(dut=node_1)

                logger.info(f"For port {configured_port} set port_type='Access Port', access_vlan_id='none'")
                xiq_d360.enter_port_type_and_vlan_id(port=configured_port,
                                                     port_type="Access Port",
                                                     access_vlan_id="none")
                logger.info(f"Successfully configured port {configured_port}")

            finally:
                assert xiq_d360.save_device_360_port_config() == 1, f"Failed to Save the Port Configuration"
                xiq.Utils.wait_till(timeout=5)
                assert xiq_d360.close_device360_window() == 1, f"Failed to Close D360 window"
                logger.info("Closed the device360 window")

            expected_cli_commands = [
                rf"configure\svlan\s\d*\sdelete\sport\s{configured_port}"
            ]
            logger.info(f"Verify that these commands are found in the delta cli: {expected_cli_commands}")
            xiq.xflowsmanageDeviceConfig.verify_delta_cli_commands(dut=node_1, commands=expected_cli_commands)
            logger.info("Successfully found the expected cli commands in delta cli")

            logger.info("Push configuration to the switch and wait")
            xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_1_policy_name, dut=node_1)

            logger.info("Check if the port was removed from vlan from CLI")
            xiq.Cli.verify_port_removed_from_vlan(dut=node_1, port=configured_port, port_type="access")

            for _ in range(7):
                try:
                    logger.info(f"Get vlan data from device360 tabular view for port {configured_port} of {node_1}")
                    bounce_iqagent(node_1)
                    port_data = xiq_d360.get_vlan_data_from_device_360_tabular_view(dut=node_1, port=configured_port)
                    logger.info(f"Found: {port_data}")

                    assert port_data["port_mode"].upper() == "ACCESS", \
                        f"Expected port_mode to be access but found {port_data['port_mode']}"
                    assert port_data["port_access_vlan"].upper() == "NONE", \
                        f"Expected port_access_vlan to be none but found {port_data['port_access_vlan']}"
                    logger.info(
                        "Successfully verified that the port configuration appear correctly "
                        "in the device360 port table")
                except Exception as exc:
                    logger.warning(repr(exc))
                    xiq.Utils.wait_till(timeout=30)
                else:
                    break
            else:
                assert False, "Failed to verify the port configuration in monitor overview of device 360"

        finally:
            logger.info("Performing test cleanup")
            xiq.xflowscommonNavigator.navigate_to_devices()
            xiq.xflowsmanageDevices.revert_device_to_template(node_1.mac)

    @pytest.mark.tcxm_19996
    def test_tcxm_19996(self, xiq_library_at_class_level, logger, node_1, node_1_policy_name, dut_ports,
                        setup_lldp, node_1_template_name, make_sure_windows_are_closed):

        """
        TCXM-19996
        Test Description: Configure "none" option in "VLAN ID" for user-defined access port
                          in template level configuration
        Author: vstefan
        """

        xiq = xiq_library_at_class_level
        xiq_d360 = xiq.xflowsmanageDevice360
        xiq_st = xiq.xflowsconfigureSwitchTemplate

        configured_port = str(random.choice(dut_ports['dut1']))
        port_type_name_with_none = \
            f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"
        default_port_type = "Auto-sense" if node_1.cli_type.upper() == "VOSS" else "Access"

        try:

            logger.info(f"Go to the port configuration of {node_1_template_name} template")
            xiq_st.select_sw_template(nw_policy=node_1_policy_name, sw_template=node_1_template_name, cli_type=node_1.cli_type.upper())
            xiq_st.go_to_port_configuration()

            if node_1.cli_type.upper() == "VOSS":
                vlan_id = str(random.choice(range(1024, 4096)))
                port_type_name_with_vlan_id = \
                    f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"

                expected_cli_commands = ["enable",
                                         "configure terminal",
                                         f'no vlan {vlan_id}']

                logger.info(
                    f"Create a new port type for port {configured_port}: port_type='access', "
                    f"vlan_id={vlan_id}, port_type_name={port_type_name_with_vlan_id}")
                xiq_d360.create_port_type_with_custom_vlan_values(port=configured_port,
                                                                  port_type_name=port_type_name_with_vlan_id,
                                                                  port_type="access",
                                                                  vlan_id=vlan_id)
                xiq.Utils.wait_till(timeout=5)
                xiq_st.switch_template_save()
                xiq.Utils.wait_till(timeout=10)
                logger.info("Successfully saved the port config at template level")

                logger.info("Push the changes to the dut and wait")
                xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_1_policy_name, dut=node_1)

                logger.info(f"Go to the port configuration of {node_1_template_name} template")
                xiq_st.select_sw_template(nw_policy=node_1_policy_name, sw_template=node_1_template_name, cli_type=node_1.cli_type.upper())
                xiq_st.go_to_port_configuration()

            else:
                expected_cli_commands = [rf"configure\svlan\s\d*\sdelete\sport\s{configured_port}"]

            try:
                logger.info(f"Create a new access port type named {port_type_name_with_none}")
                xiq_d360.open_new_port_type_editor(port=configured_port)
                xiq_d360.configure_port_name_usage_tab(port_type_name=port_type_name_with_none, port_type="access")
                xiq_d360.go_to_next_editor_tab()

                logger.info("Set native vlan id to none")
                xiq_d360.set_vlan_id(vlan_id="none")

                logger.info("Navigate to 'Summary' page")
                xiq_d360.go_to_last_page()

                expected_summary = {
                    "Port Usage": "Access",
                    "Native VLAN": "",
                    "Allowed VLANs": "",
                    "VLAN": "none"
                }
                logger.info(f"Expected summary: {expected_summary}")

                summary = xiq_d360.get_vlan_settings_summary()
                logger.info(f"Found summary: {summary}")

                logger.info("Verify that the configured fields appear correctly in the summary tab")
                assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones. " \
                    f"Expected summary: {expected_summary}\nFound summary: {summary}"
                logger.info("Found the configured fields correctly in th summary tab")

            finally:
                xiq_d360.save_port_type_config()
                xiq.Utils.wait_till(timeout=5)
                xiq_st.switch_template_save()
                xiq.Utils.wait_till(timeout=10)
                logger.info("Saved the port configuration at template level")

            logger.info(f"Verify that these commands are found in the delta cli: {expected_cli_commands}")
            xiq.xflowsmanageDeviceConfig.verify_delta_cli_commands(dut=node_1, commands=expected_cli_commands)
            logger.info("Successfully found the expected cli commands in delta cli")

            logger.info("Push the changes to the dut and wait")
            xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_1_policy_name, dut=node_1)

            logger.info("Check if the port was removed from vlan from CLI")
            vlan = vlan_id if node_1.cli_type.upper() == "VOSS" else None
            xiq.Cli.verify_port_removed_from_vlan(node_1, configured_port, port_type="access", vlan=vlan)

        finally:
            try:

                logger.info(f"Go to the port configuration of {node_1_template_name} template")
                xiq_st.select_sw_template(node_1_policy_name, node_1_template_name, cli_type=node_1.cli_type.upper())
                xiq_st.go_to_port_configuration()

                logger.info(f"Set {configured_port} port type to '{default_port_type} Port'")
                xiq_st.revert_port_configuration_template_level(port_type=f"{default_port_type} Port")
            finally:
                xiq.Utils.wait_till(timeout=5)
                xiq_st.switch_template_save()
                xiq.Utils.wait_till(timeout=10)
                logger.info("Saved the port type configuration")

            logger.info("Push the changes to the dut and wait")
            xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_1_policy_name, dut=node_1)

            try:
                if node_1.cli_type.upper() == "VOSS":
                    logger.info(f"Delete port type profile: {port_type_name_with_vlan_id}")
                    xiq.xflowsconfigureCommonObjects.delete_port_type_profile(
                        port_type_name=port_type_name_with_vlan_id)

                logger.info(f"Delete port type profile: {port_type_name_with_none}")
                xiq.xflowsconfigureCommonObjects.delete_port_type_profile(port_type_name_with_none)

            except Exception as exc:
                logger.warning(repr(exc))

    @pytest.mark.tcxm_19997
    def test_tcxm_19997(self, xiq_library_at_class_level, logger, node_1, node_1_policy_name, dut_ports,
                        setup_lldp, make_sure_windows_are_closed):
        """
        TCXM-19997
        Test Description: Configure "none" option in "VLAN" for access port in device level configuration
        Author: dpetrescu
        """
        if node_1.cli_type.upper() != "VOSS":
            pytest.skip("Expected a VOSS switch for the TCXM-19997 test case.")

        xiq = xiq_library_at_class_level
        xiq_d360 = xiq.xflowsmanageDevice360

        configured_port = str(random.choice(dut_ports['dut1']))
        port_name_with_vlan_id = \
            f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"
        port_name_with_none = \
            f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"
        vlan_id = str(random.choice(range(1024, 4096)))

        try:
            try:
                logger.info("Go to device360 port configuration")
                xiq_d360.go_to_device_360_port_config(node_1)

                logger.info(f"For port {configured_port} create a new port type: "
                            f"port_type_name={port_name_with_vlan_id}, port_type=access, vlan_id={vlan_id}")
                xiq_d360.create_port_type_with_custom_vlan_values(port=configured_port,
                                                                  port_type_name=port_name_with_vlan_id,
                                                                  port_type="access",
                                                                  vlan_id=vlan_id,
                                                                  device_360=True)
            finally:
                assert xiq_d360.save_device_360_port_config() == 1, f"Failed to Save the Port Configuration"
                xiq.Utils.wait_till(timeout=5)
                assert xiq_d360.close_device360_window() == 1, f"Failed to Close D360 window"
                logger.info("Closed the device360 window")

            logger.info("Push configuration to the switch and wait")
            xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_1_policy_name, dut=node_1)

            try:
                logger.info("Go to device360 port configuration")
                xiq_d360.go_to_device_360_port_config(node_1)

                logger.info(f"Create a new access port type named {port_name_with_none}")
                xiq_d360.open_new_port_type_editor(port=configured_port, device_360=True)
                xiq_d360.configure_port_name_usage_tab(port_type_name=port_name_with_none, port_type="access")
                xiq_d360.go_to_next_editor_tab()

                logger.info("Set native vlan id to none")
                xiq_d360.set_vlan_id(vlan_id="none")

                logger.info("Navigate to 'Summary' page")
                xiq_d360.go_to_last_page()

                expected_summary = {
                    "Port Usage": "Access",
                    "Native VLAN": "",
                    "Allowed VLANs": "",
                    "VLAN": "none"
                }
                logger.info(f"Expected summary: {expected_summary}")

                summary = xiq_d360.get_vlan_settings_summary()
                logger.info(f"Found summary: {summary}")

                logger.info("Verify that the configured fields appear correctly in the summary tab")
                assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones. " \
                    f"Expected summary: {expected_summary}\nFound summary: {summary}"
                logger.info("Found the configured fields correctly in th summary tab")

            finally:
                xiq_d360.save_port_type_config()
                xiq.Utils.wait_till(timeout=5)
                assert xiq_d360.save_device_360_port_config() == 1, f"Failed to Save the Port Configuration"
                xiq.Utils.wait_till(timeout=5)
                assert xiq_d360.close_device360_window() == 1, f"Failed to Close D360 window"
                logger.info("Saved the port configuration at device level")

            expected_cli_commands = [
                "enable",
                "configure terminal",
                f"no vlan {vlan_id}"
            ]
            logger.info(f"Verify that these commands are found in the delta cli: {expected_cli_commands}")
            xiq.xflowsmanageDeviceConfig.verify_delta_cli_commands(dut=node_1, commands=expected_cli_commands)
            logger.info("Successfully found the expected cli commands in delta cli")

            logger.info("Push the changes to the dut and wait")
            xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_1_policy_name, dut=node_1)
            xiq_d360.verify_none_vlan_id_appears_in_device_view(dut=node_1, port=configured_port)

            logger.info("Check if the port was removed from vlan from CLI")
            xiq.Cli.verify_port_removed_from_vlan(dut=node_1, port=configured_port, port_type="access")

        finally:

            logger.info("Performing test cleanup")
            xiq.xflowscommonNavigator.navigate_to_devices()
            xiq.xflowsmanageDevices.revert_device_to_template(node_1.mac)

            try:
                logger.info(f"Delete port type profile: {port_name_with_none}")
                xiq.xflowsconfigureCommonObjects.delete_port_type_profile(port_name_with_none)

                logger.info(f"Delete port type profile: {port_name_with_vlan_id}")
                xiq.xflowsconfigureCommonObjects.delete_port_type_profile(port_name_with_vlan_id)

            except Exception as e:
                print(repr(e))

    @pytest.mark.dependson("tcxm_19996")
    @pytest.mark.tcxm_19998
    def test_tcxm_19998(self, logger):
        """
        TCXM-19998
        Test Description: Configure "none" option in "VLAN ID" for user-defined access port
                          in template level configuration
        Author: vstefan
        """

        logger.info("This testcase is covered by test 19996")

    @pytest.mark.tcxm_19999
    def test_tcxm_19999(self, xiq_library_at_class_level, logger, node_1, node_1_policy_name, dut_ports,
                        setup_lldp, make_sure_windows_are_closed):

        """
        TCXM-19999
        Test Description: Configure "none" option in "VLAN" for user-defined access port in device level configuration
        Author: vstefan
        """

        xiq = xiq_library_at_class_level
        xiq_d360 = xiq.xflowsmanageDevice360

        configured_port = str(random.choice(dut_ports['dut1']))
        port_name_with_none = \
            f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"

        try:

            logger.info("Go to device360 port configuration")
            xiq_d360.go_to_device_360_port_config(node_1)

            if node_1.cli_type.upper() == "VOSS":
                port_name_with_vlan_id = \
                    f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"
                vlan_id = str(random.choice(range(1024, 4096)))
                expected_cli_commands = ["enable",
                                         "configure terminal",
                                         f"no vlan {vlan_id}"]

                logger.info(f"For port {configured_port} set port_type='access', vlan_id='{vlan_id}'")
                xiq_d360.create_port_type_with_custom_vlan_values(port=configured_port,
                                                                  port_type_name=port_name_with_vlan_id,
                                                                  port_type="access",
                                                                  vlan_id=vlan_id,
                                                                  device_360=True)

                xiq.Utils.wait_till(timeout=5)
                assert xiq_d360.save_device_360_port_config() == 1, f"Failed to Save the Port Configuration"
                xiq.Utils.wait_till(timeout=5)
                assert xiq_d360.close_device360_window() == 1, f"Failed to Close D360 window"
                logger.info("Closed the device360 window")
                logger.info(f"Successfully configured port {configured_port}")

                logger.info("Push configuration to the switch and wait")
                xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_1_policy_name, dut=node_1)

                logger.info("Go to device360 port configuration")
                xiq_d360.go_to_device_360_port_config(node_1)
            else:
                expected_cli_commands = [rf"configure\svlan\s\d*\sdelete\sport\s{configured_port}"]

            try:
                logger.info(f"Configure port {configured_port} as access port with vlan_id=none")
                xiq_d360.open_new_port_type_editor(port=configured_port, device_360=True)
                xiq_d360.configure_port_name_usage_tab(port_type_name=port_name_with_none, port_type="access")
                xiq_d360.go_to_next_editor_tab()

                logger.info("Set vlan id to none")
                xiq_d360.set_vlan_id(vlan_id="none")

                logger.info("Navigate to 'Summary' page")
                xiq_d360.go_to_last_page()

                expected_summary = {
                    "Port Usage": "Access",
                    "Native VLAN": "",
                    "Allowed VLANs": "",
                    "VLAN": "none"
                }
                logger.info(f"Expected summary: {expected_summary}")

                summary = xiq_d360.get_vlan_settings_summary()
                logger.info(f"Found summary: {summary}")

                logger.info("Verify that the configured fields appear correctly in the summary tab")
                assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones. " \
                    f"Expected summary: {expected_summary}\nFound summary: {summary}"
                logger.info("Found the configured fields correctly in the summary tab")

            finally:
                xiq_d360.save_port_type_config()
                assert xiq_d360.save_device_360_port_config() == 1, f"Failed to Save the Port Configuration"
                xiq.Utils.wait_till(timeout=5)
                assert xiq_d360.close_device360_window() == 1, f"Failed to Close D360 window"
                logger.info("Closed the device360 window")

            logger.info(f"Verify that these commands are found in the delta cli: {expected_cli_commands}")
            xiq.xflowsmanageDeviceConfig.verify_delta_cli_commands(dut=node_1, commands=expected_cli_commands)
            logger.info("Successfully found the expected cli commands in the delta cli")

            logger.info("Push configuration to the switch and wait")
            xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_1_policy_name, dut=node_1)

            for _ in range(7):
                try:
                    logger.info(f"Check if 'None' appear as access vlan in the device 360 window ")
                    xiq_d360.verify_none_vlan_id_appears_in_device_view(node_1, configured_port)
                except Exception as exc:
                    logger.warning(repr(exc))
                    xiq.Utils.wait_till(timeout=30)
                else:
                    break
            else:
                assert False, "Failed to verify the port configuration in monitor overview of device 360"

            logger.info("Check if the port was removed from vlan from CLI")
            xiq.Cli.verify_port_removed_from_vlan(dut=node_1, port=configured_port, port_type="access")

        finally:
            logger.info("Performing test cleanup")
            xiq.xflowscommonNavigator.navigate_to_devices()
            xiq.xflowsmanageDevices.revert_device_to_template(node_1.mac)

            try:
                if node_1.cli_type.upper() == "VOSS":
                    logger.info(f"Delete port type profile: {port_name_with_vlan_id}")
                    xiq.xflowsconfigureCommonObjects.delete_port_type_profile(port_type_name=port_name_with_vlan_id)

                logger.info(f"Delete port type profile: {port_name_with_none}")
                xiq.xflowsconfigureCommonObjects.delete_port_type_profile(port_name_with_none)

            except Exception as exc:
                logger.warning(repr(exc))

    @pytest.mark.dependson("tcxm_19999")
    @pytest.mark.tcxm_20000
    def test_tcxm_20000(self, logger):
        """
        TCXM-20000
        Test Description: Configure "none" option in "VLAN ID" for user-defined access port
                          in template level configuration
        Author: vstefan
        """

        logger.info("This testcase is covered by test 19999")

    @pytest.mark.tcxm_20001
    @pytest.mark.tcxm_20002
    def test_tcxm_20001(self, xiq_library_at_class_level, logger, node_1, node_1_policy_name, dut_ports,
                        bounce_iqagent, test_data, setup_lldp, make_sure_windows_are_closed):
        """
        TCXM-20001
        Test Description: Configure "none" option for trunk port and change
                          the port type of the specific port to access port
        Author: vstefan

        TCXM-20002
        Test Description: Configure "none" option for an access port and change
                          the port type of the specific type to trunk port.
        Author: vstefan

        """
        xiq = xiq_library_at_class_level
        xiq_d360 = xiq.xflowsmanageDevice360

        vlan_id = str(random.choice(range(1024, 4096)))
        configured_port = str(random.choice(dut_ports['dut1']))

        try:
            xiq_d360.go_to_device_360_port_config(node_1)
            xiq_d360.enter_port_type_and_vlan_id(
                port=random.choice([p for p in dut_ports["dut1"] if p != configured_port]),
                port_type="Access Port", device_os=node_1.cli_type.upper(),
                access_vlan_id="1000")
        finally:
            xiq_d360.save_device_360_port_config()
            xiq_d360.close_device360_window()

        logger.info("Push configuration to the switch and wait")
        xiq.xflowscommonDevices.update_and_wait_device(
            policy_name=node_1_policy_name, dut=node_1)

        port_name_access = f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"
        port_name_trunk = f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"

        port_type_list = ["trunk", "access"] if test_data['from'] == 'trunk' else ["access", "trunk"]

        try:
            for port_type in port_type_list:
                try:
                    xiq_d360.go_to_device_360_port_config(node_1)

                    kwargs = {
                        "port": configured_port,
                        "port_type_name": locals()[f"port_name_{port_type}"],
                        "port_type": port_type,
                        "device_360": True,
                        "native_vlan_id": "none" if port_type == "trunk" else None,
                        "vlan_id": "none" if port_type == "access" else None,
                        "allowed_vlans": vlan_id if port_type == "trunk" else None
                    }
                    xiq_d360.create_port_type_with_custom_vlan_values(**kwargs)
                    logger.info(f"Create a new port type for port {configured_port} with these kwargs: {kwargs}")

                finally:
                    assert xiq_d360.save_device_360_port_config() == 1, f"Failed to Save the Port Configuration"
                    xiq.Utils.wait_till(timeout=5)
                    assert xiq_d360.close_device360_window() == 1, f"Failed to Close D360 window"
                    logger.info("Closed the device360 window")

                logger.info("Push configuration to the switch and wait")
                xiq.xflowscommonDevices.update_and_wait_device(
                    policy_name=node_1_policy_name, dut=node_1)

                for _ in range(7):
                    try:
                        logger.info(f"Get vlan data from device360 tabular view for port {configured_port} of {node_1}")
                        bounce_iqagent(node_1)
                        port_data = xiq_d360.get_vlan_data_from_device_360_tabular_view(
                            node_1, configured_port)
                        logger.info(f"Found data: {port_data} for port {configured_port}")

                        logger.info("Verify that the port configuration appears correctly in the device360 port table")
                        assert port_data["port_mode"].upper() == port_type.upper(), \
                            f"Expected port_mode to be {port_type} but found {port_data['port_mode']}"
                        assert port_data["port_access_vlan"].upper() == "NONE", \
                            f"Expected port_access_vlan to be none but found {port_data['port_access_vlan']}"

                        if port_type == "trunk":
                            tagged_vlans = []

                            [tagged_vlans.extend(list(range(
                                int(vlan.split("-")[0]),
                                int(vlan.split("-")[1]) + 1
                            ))) if "-" in vlan
                             else tagged_vlans.append(int(vlan))
                             for vlan in port_data["port_tagged_vlan"].split(",")]

                            assert int(vlan_id) in tagged_vlans, \
                                f"Expected port_tagged_vlan to be {vlan_id}" \
                                f" but found {port_data['port_tagged_vlan']}"

                        logger.info(
                            "Successfully verified that the port configuration appear correctly "
                            "in the device360 port table")

                    except Exception as exc:
                        logger.warning(repr(exc))
                        xiq.Utils.wait_till(timeout=30)
                    else:
                        break
                else:
                    assert False, "Failed to verify the port configuration in monitor overview of device 360"
        finally:

            logger.info("Performing test cleanup")
            xiq.xflowscommonNavigator.navigate_to_devices()
            xiq.xflowsmanageDevices.revert_device_to_template(node_1.mac)

            try:
                logger.info(f"Delete port type profile: {port_name_trunk}")
                xiq.xflowsconfigureCommonObjects.delete_port_type_profile(port_name_trunk)

                logger.info(f"Delete port type profile: {port_name_access}")
                xiq.xflowsconfigureCommonObjects.delete_port_type_profile(port_name_access)

            except Exception as exc:
                logger.warning(repr(exc))


@pytest.mark.p1
@pytest.mark.development
@pytest.mark.testbed_stack
@pytest.mark.dependson("tcxm_xiq_onboarding")
class Xiq1053StackTests:

    @pytest.fixture
    def setup_lldp(self, node_stack, logger, dut_ports, bounce_iqagent, set_lldp):
        try:
            try:
                set_lldp(node_stack, dut_ports[node_stack.name], action="disable")
                bounce_iqagent(node_stack)
            except Exception as exc:
                logger.warning(repr(exc))

            yield

        finally:

            try:
                set_lldp(node_stack, dut_ports[node_stack.name], action="enable")
                bounce_iqagent(node_stack)
            except Exception as exc:
                logger.warning(repr(exc))

    @pytest.mark.tcxm_21055
    def test_tcxm_21055(self, xiq_library_at_class_level, logger, node_stack, node_stack_policy_name, dut_ports,
                        setup_lldp, node_stack_template_name, make_sure_windows_are_closed):
        """
        TCXM-21055
        Test Description: Configure "none" option in "VLAN ID" for user-defined trunk port
                          in template level configuration
        Author: vstefan

        """

        xiq = xiq_library_at_class_level
        xiq_d360 = xiq.xflowsmanageDevice360

        allowed_vlan = str(random.choice(range(1024, 4096)))
        configured_port = dut_ports['dut1'][1]
        port_name = f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"

        xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_stack_policy_name, dut=node_stack)

        try:
            logger.info(
                f"Go to the port configuration of {node_stack_template_name} template")
            xiq.xflowsconfigureSwitchTemplate.select_sw_template(
                node_stack_policy_name, node_stack_template_name, cli_type=node_stack.cli_type.upper())
            xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()

            try:
                logger.info(f"Create a new trunk port type named {port_name}")
                xiq_d360.open_new_port_type_editor(port=configured_port)
                xiq_d360.configure_port_name_usage_tab(
                    port_type_name=port_name, port_type="trunk")
                xiq_d360.go_to_next_editor_tab()

                logger.info("Set native vlan id to none")
                xiq_d360.set_native_vlan_id(native_vlan_id="none")

                logger.info(f"Set allowed vlans to {allowed_vlan}")
                xiq_d360.set_allowed_vlans(allowed_vlans_value=allowed_vlan)

                xiq_d360.go_to_last_page()

                expected_summary = {
                    "Port Usage": "Trunk",
                    "Native VLAN": "none",
                    "Allowed VLANs": allowed_vlan,
                    "VLAN": ""
                }
                logger.info(f"Expected summary: {expected_summary}")

                summary = xiq_d360.get_vlan_settings_summary()
                logger.info(f"Found summary: {summary}")

                logger.info("Verify that the configured fields appear correctly in the summary tab")
                assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones. " \
                    f"Expected summary: {expected_summary}\nFound summary: {summary}"
                logger.info("Found the configured fields correctly in th summary tab")

            finally:

                xiq_d360.save_port_type_config()
                xiq.Utils.wait_till(timeout=5)
                xiq.xflowsconfigureSwitchTemplate.switch_template_save()
                xiq.Utils.wait_till(timeout=10)
                logger.info("Saved the port configuration at template level")

            expected_cli_commands = [
                rf"configure vlan\s\d*\sdelete port {configured_port}",
                f"configure vlan {allowed_vlan} add port {configured_port} tagged"
            ]

            logger.info(f"Verify that these commands are found in the delta cli: {expected_cli_commands}")
            xiq.xflowsmanageDeviceConfig.verify_delta_cli_commands(
                node_stack, commands=expected_cli_commands)
            logger.info("Successfully found the expected cli commands in the delta cli")

            logger.info("Push the changes to the dut and wait")
            xiq.xflowscommonDevices.update_and_wait_device(
                policy_name=node_stack_policy_name, dut=node_stack)

            xiq.Cli.verify_port_removed_from_vlan(
                node_stack, configured_port, allowed_vlans=allowed_vlan,
                port_type="trunk")

        finally:
            try:
                logger.info(f"Go to the port configuration of {node_stack_template_name} template")
                xiq.xflowsconfigureSwitchTemplate.select_sw_template(node_stack_policy_name,
                                                                     node_stack_template_name,
                                                                     cli_type=node_stack.cli_type.upper())
                xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()

                logger.info(f"Set {configured_port} port type to 'Access Port'")
                xiq.xflowsconfigureSwitchTemplate.revert_port_configuration_template_level("Access Port")

            finally:

                xiq.Utils.wait_till(timeout=5)
                xiq.xflowsconfigureSwitchTemplate.switch_template_save()
                xiq.Utils.wait_till(timeout=10)
                logger.info("Saved the port type configuration, now push the changes to the dut")

                xiq.xflowscommonDevices.update_and_wait_device(
                    policy_name=node_stack_policy_name, dut=node_stack)

            try:
                logger.info(f"Delete port type profile: {port_name}")
                xiq.xflowsconfigureCommonObjects.delete_port_type_profile(
                    port_name)

            except Exception as exc:
                logger.warning(repr(exc))

    @pytest.mark.tcxm_21056
    def test_tcxm_21056(self, xiq_library_at_class_level, logger, node_stack, node_stack_policy_name, dut_ports,
                        setup_lldp, make_sure_windows_are_closed):

        """
        TCXM-21056
        Test Description: Configure "none" option in "Native" for trunk ports in device level configuration
        Author: dpetrescu
        """

        xiq = xiq_library_at_class_level
        xiq_d360 = xiq.xflowsmanageDevice360

        configured_port = dut_ports['dut1'][2]
        configured_slot = str(configured_port).split(":")[0]
        port_type_name = f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"
        allowed_vlan = str(random.choice(range(1024, 4096)))

        xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_stack_policy_name, dut=node_stack)

        try:
            try:
                logger.info("Go to device360 port configuration")
                xiq_d360.go_to_device_360_port_config(node_stack, slot=configured_slot)

                logger.info(f"Create a new trunk port type named {port_type_name}")

                xiq_d360.open_new_port_type_editor(port=configured_port,
                                                   device_360=True)
                xiq_d360.configure_port_name_usage_tab(port_type_name=port_type_name,
                                                       port_type="trunk")
                xiq_d360.go_to_next_editor_tab()

                logger.info("Set native vlan id to none")
                xiq_d360.set_native_vlan_id(native_vlan_id="none")

                logger.info(f"Set allowed vlans to {allowed_vlan}")
                xiq_d360.set_allowed_vlans(allowed_vlans_value=allowed_vlan)

                logger.info("Navigate to 'Summary' page")
                xiq_d360.go_to_last_page()

                expected_summary = {
                    "Port Usage": "Trunk",
                    "Native VLAN": "none",
                    "Allowed VLANs": allowed_vlan,
                    "VLAN": ""
                }

                logger.info(f"Expected summary: {expected_summary}")

                summary = xiq_d360.get_vlan_settings_summary()

                logger.info("Verify that the configured fields appear correctly in the summary tab")
                assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones. " \
                    f"Expected summary: {expected_summary}\nFound summary: {summary}"
                logger.info("Successfully verified the summary")

            finally:
                xiq_d360.save_port_type_config()
                xiq_d360.save_device_360_port_config()
                xiq_d360.close_device360_window()
            expected_cli_commands = [rf"configure vlan\s\d*\sdelete port {configured_port}",
                                     f"configure vlan {allowed_vlan} add port {configured_port} tagged"]
            xiq.xflowsmanageDeviceConfig.verify_delta_cli_commands(
                node_stack, commands=expected_cli_commands)

            xiq.xflowscommonDevices.update_and_wait_device(
                policy_name=node_stack_policy_name, dut=node_stack)

        finally:

            xiq.xflowscommonNavigator.navigate_to_devices()
            xiq.xflowsmanageDevices.revert_device_to_template(node_stack.mac)

            try:
                xiq.xflowsconfigureCommonObjects.delete_port_type_profile(port_type_name=port_type_name)
            except Exception as exc:
                logger.error(repr(exc))

    @pytest.mark.tcxm_21057
    def test_tcxm_21057(self, xiq_library_at_class_level, logger, node_stack, node_stack_policy_name, dut_ports,
                        setup_lldp, make_sure_windows_are_closed):
        """
        TCXM-21057
        Test Description: Configure "none" option in "Native" for user-defined trunk port in device level configuration
        Author: kbr
        """
        xiq = xiq_library_at_class_level
        xiq_d360 = xiq.xflowsmanageDevice360

        allowed_vlan = str(random.choice(range(1024, 4096)))
        configured_port = dut_ports['dut1'][3]
        configured_slot = str(configured_port).split(":")[0]
        port_name = f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"

        xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_stack_policy_name, dut=node_stack)

        try:
            try:
                xiq_d360.go_to_device_360_port_config(node_stack,
                                                      slot=configured_slot)

                xiq_d360.open_new_port_type_editor(port=configured_port, device_360=True)
                xiq_d360.configure_port_name_usage_tab(
                    port_type_name=port_name, port_type="trunk")
                xiq_d360.go_to_next_editor_tab()

                xiq_d360.set_native_vlan_id(native_vlan_id="none")
                xiq_d360.set_allowed_vlans(
                    allowed_vlans_value=allowed_vlan)

                xiq_d360.go_to_last_page()

                expected_summary = {
                    "Port Usage": "Trunk",
                    "Native VLAN": "none",
                    "Allowed VLANs": allowed_vlan,
                    "VLAN": ""
                }
                summary = xiq_d360.get_vlan_settings_summary()

                assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones. " \
                    f"Expected summary: {expected_summary}\nFound summary: {summary}"

            finally:
                xiq_d360.save_port_type_config()
                xiq_d360.save_device_360_port_config()
                xiq_d360.close_device360_window()

            expected_cli_commands = [
                rf"configure vlan\s\d*\sdelete port {configured_port}",
                f"configure vlan {allowed_vlan} add port {configured_port} tagged"
            ]
            xiq.xflowsmanageDeviceConfig.verify_delta_cli_commands(
                node_stack, commands=expected_cli_commands)

            xiq.xflowscommonDevices.update_and_wait_device(
                policy_name=node_stack_policy_name, dut=node_stack)

            xiq.Cli.verify_port_removed_from_vlan(
                node_stack, configured_port, allowed_vlans=allowed_vlan,
                port_type="trunk")

        finally:

            xiq.xflowscommonNavigator.navigate_to_devices()
            xiq.xflowsmanageDevices.revert_device_to_template(node_stack.mac)

            try:
                xiq.xflowsconfigureCommonObjects.delete_port_type_profile(port_name)
            except Exception as exc:
                logger.error(repr(exc))

    @pytest.mark.tcxm_21058
    def test_tcxm_21058(self, xiq_library_at_class_level, logger, node_stack, node_stack_policy_name, dut_ports,
                        setup_lldp, make_sure_windows_are_closed):
        """
        TCXM-21058
        Test Description: Configure "none" option in "VLAN" for access port in device level configuration
        Author: dpetrescu
        """

        xiq = xiq_library_at_class_level
        xiq_d360 = xiq.xflowsmanageDevice360

        configured_port = dut_ports['dut1'][3]
        configured_slot = str(configured_port).split(":")[0]
        port_name = f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"

        xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_stack_policy_name, dut=node_stack)

        try:
            try:
                xiq_d360.go_to_device_360_port_config(node_stack, slot=configured_slot)
                xiq_d360.open_new_port_type_editor(port=configured_port, device_360=True)
                xiq_d360.configure_port_name_usage_tab(
                    port_type_name=port_name, port_type="access")
                xiq_d360.go_to_next_editor_tab()
                xiq_d360.set_vlan_id(vlan_id="none")
                xiq_d360.go_to_last_page()
                expected_summary = {
                    "Port Usage": "Access",
                    "Native VLAN": "",
                    "Allowed VLANs": "",
                    "VLAN": "none"
                }
                summary = xiq_d360.get_vlan_settings_summary()
                assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones. " \
                    f"Expected summary: {expected_summary}\nFound summary: {summary}"
            finally:
                xiq_d360.save_port_type_config()
                xiq_d360.save_device_360_port_config()
                xiq_d360.close_device360_window()
            expected_cli_commands = [
                rf"configure\svlan\s\d*\sdelete\sport\s{configured_port}"
            ]
            xiq.xflowsmanageDeviceConfig.verify_delta_cli_commands(
                node_stack, commands=expected_cli_commands)

            xiq.xflowscommonDevices.update_and_wait_device(
                policy_name=node_stack_policy_name, dut=node_stack)

            for _ in range(7):
                try:
                    xiq_d360.verify_none_vlan_id_appears_in_device_view(
                        node_stack, configured_port)
                except Exception as exc:
                    logger.error(repr(exc))
                    xiq.Utils.wait_till(timeout=10)
                else:
                    break
            else:
                assert False, "The port type configuration was not found correctly in the device360 monitor page"

            xiq.Cli.verify_port_removed_from_vlan(
                node_stack, configured_port, port_type="access")

        finally:
            try:
                xiq_d360.close_port_type_config(IRV=False)
            except Exception as exc:
                logger.warning(repr(exc))

            xiq.xflowscommonNavigator.navigate_to_devices()
            xiq.xflowsmanageDevices.revert_device_to_template(node_stack.mac)

            try:
                xiq.xflowsconfigureCommonObjects.delete_port_type_profile(port_name)
            except Exception as exc:
                logger.error(repr(exc))

    @pytest.mark.tcxm_21059
    def test_tcxm_21059(self, xiq_library_at_class_level, logger, node_stack, node_stack_policy_name, dut_ports,
                        setup_lldp, node_stack_template_name, make_sure_windows_are_closed):
        """
        TCXM-21059
        Test Description: Configure "none" option in "VLAN ID" for user-defined access port
                          in template level configuration
        Author: vstefan
        """

        xiq = xiq_library_at_class_level
        xiq_d360 = xiq.xflowsmanageDevice360

        configured_port = dut_ports['dut1'][4]
        port_name = f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"

        xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_stack_policy_name, dut=node_stack)

        try:

            logger.info(f"Go to the port configuration of {node_stack_template_name} template")
            xiq.xflowsconfigureSwitchTemplate.select_sw_template(
                node_stack_policy_name, node_stack_template_name, cli_type=node_stack.cli_type.upper())
            xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()

            try:
                logger.info(f"Create a new trunk port type named {port_name}")
                xiq_d360.open_new_port_type_editor(port=configured_port)
                xiq_d360.configure_port_name_usage_tab(
                    port_type_name=port_name, port_type="access")
                xiq_d360.go_to_next_editor_tab()

                logger.info("Set native vlan id to none")
                xiq_d360.set_vlan_id(vlan_id="none")

                xiq_d360.go_to_last_page()

                expected_summary = {
                    "Port Usage": "Access",
                    "Native VLAN": "",
                    "Allowed VLANs": "",
                    "VLAN": "none"
                }
                logger.info(f"Expected summary: {expected_summary}")

                summary = xiq_d360.get_vlan_settings_summary()
                logger.info(f"Found summary: {summary}")

                logger.info("Verify that the configured fields appear correctly in the summary tab")
                assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones. " \
                    f"Expected summary: {expected_summary}\nFound summary: {summary}"
                logger.info("Found the configured fields correctly in th summary tab")

            finally:
                xiq_d360.save_port_type_config()
                xiq.Utils.wait_till(timeout=5)
                xiq.xflowsconfigureSwitchTemplate.switch_template_save()
                xiq.Utils.wait_till(timeout=10)
                logger.info("Saved the port configuration at template level")

            expected_cli_commands = [
                rf"configure\svlan\s\d*\sdelete\sport\s{configured_port}"
            ]
            logger.info(f"Verify that these commands are found in the delta cli: {expected_cli_commands}")
            xiq.xflowsmanageDeviceConfig.verify_delta_cli_commands(
                node_stack, commands=expected_cli_commands)
            logger.info("Successfully found the expected cli commands in the delta cli")

            logger.info("Push the changes to the dut and wait")
            xiq.xflowscommonDevices.update_and_wait_device(
                policy_name=node_stack_policy_name, dut=node_stack)

            xiq.Cli.verify_port_removed_from_vlan(
                node_stack, configured_port, port_type="access")

        finally:

            try:
                xiq_d360.close_port_type_config(IRV=False)
            except Exception as exc:
                logger.warning(repr(exc))

            try:
                logger.info(f"Go to the port configuration of {node_stack_template_name} template")
                xiq.xflowsconfigureSwitchTemplate.select_sw_template(node_stack_policy_name, node_stack_template_name, cli_type=node_stack.cli_type.upper())
                xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()

                logger.info(f"Set {configured_port} port type to 'Access Port'")
                xiq.xflowsconfigureSwitchTemplate.revert_port_configuration_template_level("Access Port")

            finally:
                xiq.Utils.wait_till(timeout=5)
                xiq.xflowsconfigureSwitchTemplate.switch_template_save()
                xiq.Utils.wait_till(timeout=10)
                logger.info("Saved the port type configuration, now push the changes to the dut")
                xiq.xflowscommonDevices.update_and_wait_device(
                    policy_name=node_stack_policy_name, dut=node_stack)

            try:
                logger.info(f"Delete port type profile: {port_name}")
                xiq.xflowsconfigureCommonObjects.delete_port_type_profile(
                    port_name)

            except Exception as exc:
                logger.warning(repr(exc))

    @pytest.mark.tcxm_21060
    def test_tcxm_21060(self, xiq_library_at_class_level, logger, node_stack, node_stack_policy_name, dut_ports,
                        setup_lldp, make_sure_windows_are_closed):

        """
        TCXM-21060
        Test Description: Configure "none" option in "VLAN" for user-defined access port in device level configuration
        Author: vstefan
        """

        xiq = xiq_library_at_class_level
        xiq_d360 = xiq.xflowsmanageDevice360

        configured_port = dut_ports['dut1'][5]
        port_name = f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"

        xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_stack_policy_name, dut=node_stack)

        try:
            try:
                logger.info("Go to device360 port configuration")
                xiq_d360.go_to_device_360_port_config(node_stack,
                                                      slot=str(configured_port).split(":")[0])

                logger.info(f"For port {configured_port} create a new port type: port_type_name={port_name},"
                            f" port_type=access, vlan_id=none")
                xiq_d360.open_new_port_type_editor(port=configured_port, device_360=True)
                xiq_d360.configure_port_name_usage_tab(
                    port_type_name=port_name, port_type="access")
                xiq_d360.go_to_next_editor_tab()

                logger.info("Set vlan id to none")
                xiq_d360.set_vlan_id(vlan_id="none")

                xiq_d360.go_to_last_page()

                expected_summary = {
                    "Port Usage": "Access",
                    "Native VLAN": "",
                    "Allowed VLANs": "",
                    "VLAN": "none"
                }
                logger.info(f"Expected summary: {expected_summary}")

                summary = xiq_d360.get_vlan_settings_summary()
                logger.info(f"Found summary: {summary}")

                logger.info("Verify that the configured fields appear correctly in the summary tab")
                assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones. " \
                    f"Expected summary: {expected_summary}\nFound summary: {summary}"
                logger.info("Found the configured fields correctly in th summary tab")

            finally:
                xiq_d360.save_port_type_config()
                xiq_d360.save_device_360_port_config()
                xiq_d360.close_device360_window()
                logger.info("Closed the device360 window")

            expected_cli_commands = [rf"configure\svlan\s\d*\sdelete\sport\s{configured_port}"]
            logger.info(f"Verify that these commands are found in the delta cli: {expected_cli_commands}")

            xiq.xflowsmanageDeviceConfig.verify_delta_cli_commands(node_stack, commands=expected_cli_commands)
            logger.info("Successfully found the expected cli commands in the delta cli")

            logger.info("Push configuration to the switch and wait")
            xiq.xflowscommonDevices.update_and_wait_device(policy_name=node_stack_policy_name, dut=node_stack)

            for _ in range(7):
                try:
                    xiq_d360.verify_none_vlan_id_appears_in_device_view(
                        node_stack, configured_port)
                except Exception as exc:
                    logger.warning(repr(exc))
                    xiq.Utils.wait_till(timeout=30)
                else:
                    break
            else:
                assert False, "Failed to verify the port configuration in monitor overview of device 360"

            xiq.Cli.verify_port_removed_from_vlan(
                node_stack, configured_port, port_type="access")

        finally:

            xiq.xflowscommonNavigator.navigate_to_devices()
            xiq.xflowsmanageDevices.revert_device_to_template(
                node_stack.mac)

            try:

                logger.info(f"Delete port type profile: {port_name}")
                xiq.xflowsconfigureCommonObjects.delete_port_type_profile(
                    port_name)

            except Exception as exc:
                logger.warning(repr(exc))

    @pytest.mark.tcxm_21061
    def test_tcxm_21061(self, xiq_library_at_class_level, logger, node_stack, node_stack_policy_name, dut_ports,
                        bounce_iqagent, setup_lldp, make_sure_windows_are_closed):

        """
        TCXM-21061
        Test Description: Verify the port is added as tagged to all other existing vlans in XIQ
        Author: dpetrescu
        """

        xiq = xiq_library_at_class_level
        xiq_d360 = xiq.xflowsmanageDevice360

        configured_port = dut_ports['dut1'][6]
        port_name = f"port_type_{''.join(random.sample(list(string.ascii_letters) + list(string.digits), k=6))}"
        slot = configured_port.split(":")[0]

        try:
            try:
                xiq_d360.go_to_device_360_port_config(node_stack, slot=slot)
                xiq_d360.create_port_type_with_custom_vlan_values(
                    port=configured_port, port_type_name=port_name,
                    port_type="trunk", native_vlan_id="none",
                    allowed_vlans="all", device_360=True)
            finally:
                xiq_d360.save_device_360_port_config()
                xiq_d360.close_device360_window()

            xiq.xflowscommonDevices.update_and_wait_device(
                policy_name=node_stack_policy_name, dut=node_stack)

            try:
                xiq_d360.go_to_device_360_port_config(node_stack, slot=slot)
                xiq_d360.enter_port_type_and_vlan_id(port=dut_ports['dut1'][7],
                                                     port_type="Access Port",
                                                     access_vlan_id="1000")
            finally:
                xiq_d360.save_device_360_port_config()
                xiq_d360.close_device360_window()

            xiq.xflowscommonDevices.update_and_wait_device(
                policy_name=node_stack_policy_name, dut=node_stack)

            for _ in range(15):
                try:
                    bounce_iqagent(node_stack)
                    xiq.Utils.wait_till(timeout=20)
                    port_data = xiq_d360.get_vlan_data_from_device_360_tabular_view(
                        node_stack, configured_port)

                    assert port_data["port_mode"].lower() == "trunk"
                    assert port_data["port_access_vlan"].lower() == "none"

                except Exception as exc:
                    print(repr(exc))
                    logger.error(repr(exc))
                    xiq.Utils.wait_till(timeout=120)
                else:
                    break
            else:
                assert False, "The port type configuration was not found correctly in the device360 monitor page"

        finally:

            xiq.xflowscommonNavigator.navigate_to_devices()
            xiq.xflowsmanageDevices.revert_device_to_template(node_stack.mac)

            try:
                xiq.xflowsconfigureCommonObjects.delete_port_type_profile(port_name)
            except Exception as exc:
                logger.error(repr(exc))

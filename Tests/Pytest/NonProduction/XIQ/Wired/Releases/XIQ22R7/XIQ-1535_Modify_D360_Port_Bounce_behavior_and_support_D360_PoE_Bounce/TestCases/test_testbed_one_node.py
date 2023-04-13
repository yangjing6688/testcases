# Author        : Ionut Daniel Zoican
# Description   : These tests were created for XIQ-1535 - Modify D360 Port Bounce behavior and support D360 PoE Bounce
#                 for EXOS(Single/Stack)/VOSS.
# Testcases     : TCXM-23835, TCXM-23836, TCXM-23837, TCXM-23838, TCXM-23843, TCXM-23844, TCXM-23845, TCXM-23846,
#                 TCXM-23849, TCXM-23850, TCXM-26870
# Comments      : These tests are applicable for FabricEngine, SwitchEngine and Stack.
# Runlist implementation and keywords moved to framework: Ninel Burlacu

import pytest
import random


@pytest.fixture
def test_teardown(xiq_library_at_class_level):
    """
    This fixture makes sure that the honeycomb/device360 windows are closed at the TEARDOWN of the test case.
    This way the next test case won't be affected if the current test failed and did not close all the windows during its call.
    """
    try:
        xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
    except:
        # device360 window is not opened
        pass


@pytest.mark.p1
@pytest.mark.development
@pytest.mark.enter_switch_cli
@pytest.mark.testbed_1_node
@pytest.mark.testbed_stack
class XIQ1535OneNodeTests:

    #@pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.tcxm_23835
    def test_23835(self, logger, xiq_library_at_class_level, test_bed, test_data, test_teardown):
        logger.info(f"This test is {test_data['tc']}")
        logger.info(f"This test is writen by {test_data['author']}")
        """
        TCXM-23835: Verify that 'Bounce Port' button is present in 'Port Info' dialog box
        TCXM_23837: Verify that after 'Bounce Port' button has been clicked, the agent will only reset the port
        TCXM_23843: Verify that 'Bounce Port' button is present in 'Port Info' dialog box in all slots for stack devices
        TCXM_23845: Verify that after 'Bounce Port' button has been clicked, the agent will only reset the port in a
                    specific slot in a stack
        """
        # Using a random active port
        with test_bed.enter_switch_cli(test_bed.node) as spawn_connection:
            poe_ports = xiq_library_at_class_level.Cli.get_switch_poe_ports(test_bed.node)
            connected_ports = xiq_library_at_class_level.Cli.get_switch_connected_ports(test_bed.node)
            available_ports = [port for port in poe_ports if port in connected_ports]
            if not available_ports:
                pytest.skip(f"Test skipped because {test_bed.node.cli_type.upper()} {test_bed.node.platform} has no connected ports")
            else:
                port_used = random.choice(available_ports)
            if test_bed.node.cli_type.lower() == 'voss':
                expected_commands = ['en', 'config t', f'interface gig {port_used}', 'shutdown', 'no shutdown',
                                     'exit', 'exit']
                switch_time = None
            elif test_bed.node.cli_type.lower() == 'exos':
                expected_commands = [f'restart port {port_used}']
                output_time = spawn_connection.send_cmd(test_bed.node.name, 'show time', max_wait=10, interval=2)
                output_time_text = output_time[0].cmd_obj.return_text
                switch_time = xiq_library_at_class_level.Utils.get_regexp_matches(output_time_text, '(\d+:\d+:\d+)', 1)[0]
                logger.info(f"The time on the switch is: {switch_time}")

            # Bouncing port and checking that the correct commands have been sent to the switch

            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(test_bed.node.mac)
            if test_bed.node.cli_type.lower() == "voss":
                spawn_connection.send_cmd(test_bed.node.name, 'clear logging', max_wait=10, interval=2)

            xiq_library_at_class_level.xflowsmanageDevice360.port_info_bounce_port(port_used)
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

            xiq_library_at_class_level.Utils.wait_till(timeout=30, delay=10, silent_failure=True, msg="Waiting for commands to "
                                                        "be sent to the switch...")
            xiq_library_at_class_level.Cli.expected_commands_in_cli_history(expected_commands, test_bed.node, switch_time)

    @pytest.mark.tcxm_23837
    @pytest.mark.dependson("tcxm_23835")
    def test_23837(self, logger):
        logger.info("This testcase is covered by tcxm_23835")

    @pytest.mark.tcxm_23843
    @pytest.mark.dependson("tcxm_23835")
    def test_23843(self, logger):
        logger.info("This testcase is covered by tcxm_23835")

    @pytest.mark.tcxm_23845
    @pytest.mark.dependson("tcxm_23835")
    def test_23845(self, logger):
        logger.info("This testcase is covered by tcxm_23835")

    @pytest.mark.tcxm_23836
    @pytest.mark.skip_if_node_1_does_not_support_poe
    #@pytest.mark.dependson("tcxm_xiq_onboarding")
    def test_23836(self, logger, xiq_library_at_class_level, test_bed, test_data, test_teardown):
        logger.info(f"This test is {test_data['tc']}")
        logger.info(f"This test is writen by {test_data['author']}")
        """
        TCXM_23836: Verify that 'Bounce PoE' button is present in 'Port Info' dialog box
        TCXM_23838: Verify that after 'Bounce PoE' button has been clicked, the agent will only reset PoE
        TCXM_23844: Verify that 'Bounce PoE' button is present in 'Port Info' dialog box only for slots which support
                    PoE in a stack
        TCXM_23846: Verify that after 'Bounce PoE' button has been clicked, the agent will only reset PoE port on a
                    specific slot in a stack
        """
        # Using a random active port
        with test_bed.enter_switch_cli(test_bed.node) as spawn_connection:
            poe_ports = xiq_library_at_class_level.Cli.get_switch_poe_ports(test_bed.node)
            connected_ports = xiq_library_at_class_level.Cli.get_switch_connected_ports(test_bed.node)
            available_ports = [port for port in poe_ports if port in connected_ports]
            if not available_ports:
                pytest.skip(f"Test skipped because {test_bed.node.cli_type.upper()} {test_bed.node.platform} has no connected ports")
            else:
                port_used = random.choice(available_ports)
            if test_bed.node.cli_type.lower() == 'voss':
                expected_commands = ['en', 'config t', f'interface gig {port_used}', 'poe poe-shutdown',
                                     'no poe-shutdown', 'exit', 'exit']
                switch_time = None
            elif test_bed.node.cli_type.lower() == 'exos':
                expected_commands = [f'reset inline-power ports {port_used}']
                output_time = spawn_connection.send_cmd(test_bed.node.name, 'show time', max_wait=10, interval=2)
                output_time_text = output_time[0].cmd_obj.return_text
                switch_time = xiq_library_at_class_level.Utils.get_regexp_matches(output_time_text, '(\d+:\d+:\d+)', 1)[0]
                logger.info(f"The time on the switch is: {switch_time}")

            # Bouncing port and checking that the correct commands have been sent to the switch

            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(test_bed.node.mac)
            if test_bed.node.cli_type.lower() == "voss":
                spawn_connection.send_cmd(test_bed.node.name, 'clear logging', max_wait=10, interval=2)

            xiq_library_at_class_level.xflowsmanageDevice360.port_info_bounce_poe(port_used)
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

            xiq_library_at_class_level.Utils.wait_till(timeout=30, delay=10, silent_failure=True, msg="Waiting for commands to "
                                                                                    "be sent to the switch...")
            xiq_library_at_class_level.Cli.expected_commands_in_cli_history(expected_commands, test_bed.node, switch_time)

    @pytest.mark.tcxm_23838
    @pytest.mark.dependson("tcxm_23836")
    def test_23838(self, logger):
        logger.info("This testcase is covered by tcxm_23836")

    @pytest.mark.tcxm_23844
    @pytest.mark.dependson("tcxm_23836")
    def test_23844(self, logger):
        logger.info("This testcase is covered by tcxm_23836")

    @pytest.mark.tcxm_23846
    @pytest.mark.dependson("tcxm_23836")
    def test_23846(self, logger):
        logger.info("This testcase is covered by tcxm_23836")

    @pytest.mark.tcxm_23849
    #@pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.run_if_node_cli_type("VOSS")
    def test_23849(self, logger, xiq_library_at_class_level, test_bed, network_manager, test_data, test_teardown):
        logger.info(f"This test is {test_data['tc']}")
        logger.info(f"This test is writen by {test_data['author']}")
        """
        TCXM_23849: Check that "Bounce Port" is visible for the management port if the device is voss
        TCXM_23850: Verify that after 'Bounce Port' button has been clicked, the agent will only reset the management
                    port
        """
        expected_commands = ['en', 'config t', f'interface mgmt mgmt', 'shutdown', 'no shutdown',
                             'exit', 'exit']

        # Bouncing port and checking that the correct commands have been sent to the switch

        with test_bed.enter_switch_cli(test_bed.node) as spawn_connection:
            logger.info("Checking the management port status on voss switch")
            output = spawn_connection.send_cmd(test_bed.node.name, 'show mgmt interface', max_wait=10, interval=2)
            mgmt_interface_output = output[0].cmd_obj.return_text
            try:
                mgmt_port_status = xiq_library_at_class_level.Utils.get_regexp_matches(mgmt_interface_output,
                                                                     '(\d+[ ]+Mgmt-oob\d+.+)', 1)
                if 'enable' in mgmt_port_status[0]:
                    logger.info("VOSS Management port is enabled.")
                    return True
                else:
                    logger.info("VOSS Management port isn't enabled.")
                    pytest.skip(f"Test skipped because {test_bed.node.platform} is not using the mgmt interface. Mgmt interface is disabled")
            except IndexError:
                pytest.skip(f"Test skipped because {test_bed.node.platform} does not have a mgmt interface")

            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(test_bed.node.mac)
            if test_bed.node.cli_type.lower() == "voss":
                spawn_connection.send_cmd(test_bed.node.name, 'clear logging', max_wait=10, interval=2)

            network_manager.close_connection_to_all_network_elements()
            xiq_library_at_class_level.xflowsmanageDevice360.port_info_bounce_port("mgmt")
            xiq_library_at_class_level.Utils.wait_till(timeout=50, delay=10, silent_failure=True, msg="Waiting for dut mgmt connection"
                                                                                    " to come back up to")
            network_manager.connect_to_all_network_elements()
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

            xiq_library_at_class_level.Utils.wait_till(timeout=30, delay=10, silent_failure=True, msg="Waiting for commands to "
                                                                                    "be sent to the switch...")
            xiq_library_at_class_level.Cli.expected_commands_in_cli_history(expected_commands, test_bed.node)

    @pytest.mark.tcxm_23850
    @pytest.mark.dependson("tcxm_23849")
    def test_23850(self, logger):
        logger.info("This testcase is covered by tcxm_23849")

    @pytest.mark.tcxm_26870
    #@pytest.mark.dependson("tcxm_xiq_onboarding")
    @pytest.mark.skip_if_node_1_does_not_support_poe
    def test_26870(self, xiq_library_at_class_level, test_bed, logger, test_data, test_teardown):
        logger.info(f"This test is {test_data['tc']}")
        logger.info(f"This test is writen by {test_data['author']}")
        """
        TCXM-26870: Check that "Bounce PoE" is visible for ports which were shut down and the right commands were sent
                    to the switch after clicking it
        """
        with test_bed.enter_switch_cli(test_bed.node) as spawn_connection:
            poe_ports = xiq_library_at_class_level.Cli.get_switch_poe_ports(test_bed.node)
            connected_ports = xiq_library_at_class_level.Cli.get_switch_connected_ports(test_bed.node)
            used_ports = xiq_library_at_class_level.Cli.get_switch_disconnected_ports(test_bed.node,
                                                                                      connected_ports)
            available_ports = [port for port in poe_ports if port in used_ports]

            # Use a random disconnected port
            if not available_ports:
                pytest.skip(f"Test skipped because {test_bed.node.cli_type.upper()} {test_bed.node.platform} has no disconnected ports")
            else:
                port_used = random.choice(available_ports)

            # Checking bounce port
            if test_bed.node.cli_type.lower() == 'voss':
                expected_commands = ['en', 'config t', f'interface gig {port_used}', 'poe poe-shutdown',
                                     'no poe-shutdown', 'exit', 'exit']
                switch_time = None
            elif test_bed.node.cli_type.lower() == 'exos':
                expected_commands = [f'reset inline-power ports {port_used}']
                output_time = spawn_connection.send_cmd(test_bed.node.name, 'show time', max_wait=10, interval=2)
                output_time_text = output_time[0].cmd_obj.return_text
                switch_time = xiq_library_at_class_level.Utils.get_regexp_matches(output_time_text, '(\d+:\d+:\d+)', 1)[0]
                logger.info(f"The time on the switch is: {switch_time}")

            # Bouncing port and checking that the correct commands have been sent to the switch
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(test_bed.node.mac)
            if test_bed.node.cli_type.lower() == "voss":
                spawn_connection.send_cmd(test_bed.node.name, 'clear logging', max_wait=10, interval=2)

            xiq_library_at_class_level.xflowsmanageDevice360.port_info_bounce_poe(port_used)
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

            xiq_library_at_class_level.Utils.wait_till(timeout=30, delay=10, silent_failure=True, msg="Waiting for commands to "
                                                                                    "be sent to the switch...")
            xiq_library_at_class_level.Cli.expected_commands_in_cli_history(expected_commands, test_bed.node, switch_time)


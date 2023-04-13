import pytest
import time

from extauto.xiq.elements.MLInsightsMonitorWebElements import MLInsighstMonitorWebElements


@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM25169Tests:

    @pytest.mark.development
    @pytest.mark.testbed_stack
    @pytest.mark.tcxm_25169
    @pytest.mark.p1
    def test_tcxm_25169(self, node_stack, logger, auto_actions, xiq_library_at_class_level, cli, loaded_config, request):

        MLInsWebElements = MLInsighstMonitorWebElements()
        ml_insights_monitor_option = "All Switches"

        try:
            logger.info("Navigate to ML Insights -> Network 360 Monitor.")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network360monitor()

            logger.info("Clicking on dropdown arrow.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_drop_down()

            logger.info("Navigate to 'All Switches' option.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(ml_insights_monitor_option)

            logger.info("Clicking the devices card.")
            auto_actions.click(xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card())

            time.sleep(60)
            
            logger.info("Getting hostname and mac address from legend section.")
            hostname_mac_before_reboot_legend = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_hostname_and_macaddress_hyperlinks_legend_check(node_stack)
            logger.info(f"The hostname and mac address for each speed before reboot are : {hostname_mac_before_reboot_legend}")

            time.sleep(10)
            
            logger.info("Getting hostname and mac address from halfpie section.")
            hostname_mac_before_reboot_halfpie = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_hostname_and_macaddress_hyperlinks_halfpie_check(node_stack)
            logger.info(f"The hostname and mac address for each speed before reboot are: {hostname_mac_before_reboot_halfpie}")

            time.sleep(10)
            
            logger.info("Getting number of ports from legend section.")
            no_ports_before_reboot_legend = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_legend_ports_number(node_stack)
            logger.info(f"The number of ports for each speed before reboot is : {no_ports_before_reboot_legend }")

            time.sleep(10)
            
            logger.info("Getting number of ports from halfpie section.")
            no_ports_before_reboot_halfpie = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_halfpie_ports_number(node_stack)
            logger.info(f"The number of ports for each speed before reboot is : {no_ports_before_reboot_halfpie}")

            logger.info("Rebooting stack slot 1.")
            cli.boot_stack_slot(node_stack, slot='1')

            time.sleep(300)

            logger.info("Clicking the refresh button...")
            res = auto_actions.click(MLInsWebElements.get_n360_monitor_port_connection_speed_section_refresh_page())
            assert res != -1, "Unable to click the refresh button."

            time.sleep(10)
            
            logger.info("Getting hostname and mac address from legend section.")
            hostname_mac_after_reboot_legend = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_hostname_and_macaddress_hyperlinks_legend_check(node_stack)
            logger.info(f"The hostname and mac address for each speed after reboot are : {hostname_mac_after_reboot_legend}")

            time.sleep(10)
            
            logger.info("Clicking the refresh button...")
            res = auto_actions.click(MLInsWebElements.get_n360_monitor_port_connection_speed_section_refresh_page())
            assert res != -1, "Unable to click the refresh button."
            
            time.sleep(10)
            
            logger.info("Getting hostname and mac address from halfpie section.")
            hostname_mac_after_reboot_halfpie = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_hostname_and_macaddress_hyperlinks_halfpie_check(node_stack)
            logger.info(f"The hostname and mac address for each speed after reboot are: {hostname_mac_after_reboot_halfpie}")

            time.sleep(10)
            
            logger.info("Clicking the refresh button...")
            res = auto_actions.click(MLInsWebElements.get_n360_monitor_port_connection_speed_section_refresh_page())
            assert res != -1, "Unable to click the refresh button."
            
            time.sleep(10)
            
            logger.info("Getting number of ports from legend section.")
            no_ports_after_reboot_legend = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_legend_ports_number(node_stack)
            logger.info(f"The number of ports for each speed after reboot is : {no_ports_after_reboot_legend}")

            time.sleep(10)
            
            logger.info("Clicking the refresh button...")
            res = auto_actions.click(MLInsWebElements.get_n360_monitor_port_connection_speed_section_refresh_page())
            assert res != -1, "Unable to click the refresh button."
            
            time.sleep(10)
            
            logger.info("Getting number of ports from halfpie section.")
            no_ports_after_reboot_halfpie = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_halfpie_ports_number(node_stack)
            logger.info(f"The number of ports for each speed after reboot is : {no_ports_after_reboot_halfpie}")

            assert sorted(list(set(hostname_mac_before_reboot_legend))) == sorted(list(set(hostname_mac_after_reboot_legend))), "The Hostname and Mac Address are the same after reboot in the legend section."
            assert sorted(list(set(hostname_mac_before_reboot_halfpie))) == sorted(list(set(hostname_mac_after_reboot_halfpie))), "The Hostname and Mac Address are the same after reboot in the halfpie section."

            assert no_ports_before_reboot_legend == no_ports_after_reboot_legend, "The number of ports are the same after reboot in the legend section"
            assert no_ports_before_reboot_halfpie == no_ports_after_reboot_halfpie, "The number of ports are the same after reboot in the halfpie section"
        finally:
            logger.step("Closing Device Health window.")
            if close_dialog := MLInsWebElements.get_n360_monitor_device_health_window_close_dialog():
                auto_actions.click(close_dialog)

import pytest
import time

from extauto.xiq.elements.MLInsightsMonitorWebElements import MLInsighstMonitorWebElements


@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM25126Tests:

    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_25126
    @pytest.mark.p1
    def test_tcxm_25126(self, logger, auto_actions, xiq_library_at_class_level, test_data):

        MLInsWebElements = MLInsighstMonitorWebElements()
        ml_insights_monitor_option = "All Switches"

        try:
            logger.step("Navigate to ML Insights -> Network 360 Monitor.")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network360monitor()

            logger.step("Clicking on dropdown arrow.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_drop_down()

            logger.step("Navigate to 'All Switches' option.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(ml_insights_monitor_option)

            logger.step("Clicking the devices card.")
            auto_actions.click(xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card())

            time.sleep(60)
            
            logger.step("Checking hyperlinks, back button, table's header columns and table's title under the legend section.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_legend_check()

            time.sleep(10)
            
            logger.step("Checking hyperlinks, back button, table's header columns and table's title under the halfpie section.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_halfpie_check()

        finally:
            logger.step("Closing Device Health window.")
            if close_dialog := MLInsWebElements.get_n360_monitor_device_health_window_close_dialog():
                auto_actions.click(close_dialog)


@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM25152Tests:

    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_25152
    @pytest.mark.p1
    def test_tcxm_25152(self, node_1, logger, auto_actions, xiq_library_at_class_level, cli, network_manager):

        MLInsWebElements = MLInsighstMonitorWebElements()
        ml_insights_monitor_option = "All Switches"

        try:
            logger.step("Navigate to ML Insights -> Network 360 Monitor.")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network360monitor()

            logger.step("Clicking on dropdown arrow.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_drop_down()

            logger.step("Navigate to 'All Switches' option.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(ml_insights_monitor_option)

            logger.step("Clicking the devices card.")
            auto_actions.click(xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card())

            time.sleep(60)
            
            logger.step("Verifying hostname and mac address in XIQ for legend section..")
            output_xiq_legend = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_hostname_and_macaddress_hyperlinks_legend_check(node_1)
            logger.info(f"The list form xiq is {output_xiq_legend}")

            time.sleep(10)
            
            logger.step("Verifying hostname and mac address in XIQ for halfpie section..")
            output_xiq_halfpie = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_hostname_and_macaddress_hyperlinks_halfpie_check(node_1)
            logger.info(f"The list form xiq is {output_xiq_halfpie}")

            logger.step("Verifying hostname and mac address in CLI..")
            output_cli = cli.hostname_and_mac_address_from_dut(node_1)
            logger.info(f"The list from cli is {output_cli}")

            for i in range(0, len(output_xiq_legend)-1, 2):
                a = output_xiq_legend[i]
                b = output_xiq_halfpie[i]

                c = output_xiq_legend[i + 1]
                d = output_xiq_halfpie[i + 1]

                assert a == output_cli[0] and c == output_cli[1], f"The hostname and mac adress from legend section match the ones from CLI for every speed."
                assert b == output_cli[0] and d == output_cli[1], f"The hostname and mac adress from halfpie section match the ones from CLI for every speed."
        finally:
            
            logger.step("Closing Device Health window.")
            if close_dialog := MLInsWebElements.get_n360_monitor_device_health_window_close_dialog():
                auto_actions.click(close_dialog)
            
            cli.close_connection_with_error_handling(node_1)


@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM25153Tests:

    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_25153
    @pytest.mark.p1
    def test_tcxm_25153(self, node_1, logger, auto_actions, xiq_library_at_class_level, cli, node_1_onboarding_location):

        MLInsWebElements = MLInsighstMonitorWebElements()
        ml_insights_monitor_option = "All Switches"

        xiq_library_at_class_level.xflowscommonDevices.column_picker_select("MAC Address", "Host Name", "Location")

        try:
            manage_device_dict = xiq_library_at_class_level.xflowscommonDevices.get_device_row_values(node_1.mac, "LOCATION,HOST NAME,MAC")
            logger.info(f"manage_device_dict is {manage_device_dict}")
            location = manage_device_dict["LOCATION"].split(" >> ")
            floor = location[-1]
            
            if not floor:
                floor = node_1_onboarding_location.split(",")[-1].strip()
            
            logger.info(f"The floor for the device in Manage -> Devices is: {floor}")
            hostname = manage_device_dict["HOST NAME"]
            logger.info(f"The hostname is: {hostname}")
            mac_address = manage_device_dict["MAC"]
            logger.info(f"The mac address is: {mac_address}")

            logger.step("Navigate to ML Insights -> Network 360 Monitor.")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network360monitor()

            logger.step("Clicking on dropdown arrow.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_drop_down()

            logger.step("Navigate to 'All Switches' option.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(ml_insights_monitor_option)

            logger.step("Search the floor in Network360Monitor.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor._search_and_click_floor(floor)

            logger.step("Clicking the devices card.")
            auto_actions.click(xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card())

            time.sleep(60)
            
            logger.step("Verifying hostname and mac address in XIQ for legend section..")
            output_xiq_legend = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_hostname_and_macaddress_hyperlinks_legend_check(node_1)
            logger.info(f"The list form xiq is {output_xiq_legend}")

            time.sleep(10)
            
            logger.step("Verifying hostname and mac address in XIQ for halfpie section..")
            output_xiq_halfpie = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_hostname_and_macaddress_hyperlinks_halfpie_check(node_1)
            logger.info(f"The list form xiq is {output_xiq_halfpie}")

            for i in range(0, len(output_xiq_legend) - 1, 2):
                a = output_xiq_legend[i]
                b = output_xiq_halfpie[i]

                c = output_xiq_legend[i + 1]
                d = output_xiq_halfpie[i + 1]

                assert a == hostname and c == mac_address, f"The hostname and mac adress from legend section match the ones from CLI for every speed."
                assert b == hostname and d == mac_address, f"The hostname and mac adress from halfpie section match the ones from CLI for every speed."

        finally:
            
            logger.step("Closing Device Health window.")
            if close_dialog := MLInsWebElements.get_n360_monitor_device_health_window_close_dialog():
                auto_actions.click(close_dialog)
            
            cli.close_connection_with_error_handling(node_1)


@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM25154Tests:

    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_25154
    @pytest.mark.p1
    def test_tcxm_25154(self, node_1, logger, auto_actions, xiq_library_at_class_level, cli):

        MLInsWebElements = MLInsighstMonitorWebElements()
        ml_insights_monitor_option = "All Switches"

        try:
            logger.step("Navigate to ML Insights -> Network 360 Monitor.")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network360monitor()

            logger.step("Clicking on dropdown arrow.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_drop_down()

            logger.step("Navigate to 'All Switches' option.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(ml_insights_monitor_option)

            logger.step("Clicking the devices card.")
            auto_actions.click(xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card())

            time.sleep(60)
            
            logger.step("Verifying hostname and mac address are hyperlinks for legend section..")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_hostname_and_macaddress_hyperlinks_legend_check(node_1)

            time.sleep(10)
            
            logger.step("Verifying hostname and mac address are hyperlinks for halfpie section..")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_hostname_and_macaddress_hyperlinks_halfpie_check(node_1)

        finally:
            
            logger.step("Closing Device Health window.")
            if close_dialog := MLInsWebElements.get_n360_monitor_device_health_window_close_dialog():
                auto_actions.click(close_dialog)
            
            cli.close_connection_with_error_handling(node_1)


@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM25155Tests:

    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_25155
    @pytest.mark.p1
    def test_tcxm_25155(self, node_1, logger, auto_actions, xiq_library_at_class_level, cli):

        MLInsWebElements = MLInsighstMonitorWebElements()
        ml_insights_monitor_option = "All Switches"

        try:
            logger.info("Navigate to ML Insights -> Network 360 Monitor.")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network360monitor()

            logger.step("Clicking on dropdown arrow.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_drop_down()

            logger.step("Navigate to 'All Switches' option.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(ml_insights_monitor_option)

            logger.step("Clicking the devices card.")
            auto_actions.click(xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card())

            time.sleep(60)
            
            logger.step("Verifying the number of ports and if hostname and mac address hyperlinks can be clicked and Device360 opens in legend section.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_clicking_hostname_mac_hyperlinks_legend_check(node_1)

            time.sleep(10)
            
            logger.info("Verifying the number of ports and if hostname and mac address hyperlinks can be clicked and Device360 opens in halfpie section.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_clicking_hostname_mac_hyperlinks_halfpie_check(node_1)

        finally:
            
            logger.step("Closing Device Health window.")
            if close_dialog := MLInsWebElements.get_n360_monitor_device_health_window_close_dialog():
                auto_actions.click(close_dialog)
            
            cli.close_connection_with_error_handling(node_1)


@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM25164Tests:

    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_25164
    @pytest.mark.p1
    def test_tcxm_25164(self, node_1, logger, auto_actions, xiq_library_at_class_level, cli):

        MLInsWebElements = MLInsighstMonitorWebElements()
        ml_insights_monitor_option = "All Switches"

        speeds_list = ["10000 Mbps", "5000 Mbps", "2500 Mbps", "1000 Mbps", "100 Mbps", "10 Mbps"]
        port_speed_dict = {"10000 Mbps": [],
                           "5000 Mbps": [],
                           "2500 Mbps": [],
                           "1000 Mbps": [],
                           "100 Mbps": [],
                           "10 Mbps": []}
        port_list = []
        port_list_string = ''

        try:
            logger.step("Navigate to ML Insights -> Network 360 Monitor.")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network360monitor()

            logger.step("Clicking on dropdown arrow.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_drop_down()

            logger.step("Navigate to 'All Switches' option.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(ml_insights_monitor_option)

            logger.step("Clicking the devices card.")
            auto_actions.click(xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card())

            time.sleep(60)
            
            connected_ports = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_clicking_hostname_mac_hyperlinks_legend_check(node_1)
            logger.info(f"The connected ports are: {connected_ports}")
            for i in speeds_list:
                for j in range(len(connected_ports)):
                    if connected_ports[j][0] != "mgmt" and connected_ports[j][1] == i:
                        logger.info(f"The connected port {connected_ports[j][0]} has the speed {i}")
                        port_speed_dict[i].append(connected_ports[j][0])
           
            for key in port_speed_dict:
                if port_speed_dict[key] != []:
                    port_list.append(port_speed_dict[key][0])

            if (port_list is None) or (len(port_list) < 2):
                pytest.skip("Skip this test case because the only connected port of the dut is the mgmt one")

            for port in port_list:
                port_list_string += port + ","
            port_list_string = port_list_string.strip(",")

            logger.step("Disable the first port of each speed.")
            cli.disable_enable_ports(node_1, port_list_string, action="disable")
            time.sleep(15)

            logger.step("Clicking the refresh button...")
            res = auto_actions.click(MLInsWebElements.get_n360_monitor_port_connection_speed_section_refresh_page())
            assert res != -1, "Unable to click the refresh button."

            time.sleep(60)
            
            logger.step("Getting the connected ports after disable from legend section.")
            connected_ports_disable_legend = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_clicking_hostname_mac_hyperlinks_legend_check(node_1)
            logger.info(f"The connected ports from legend section are: {connected_ports_disable_legend}")

            logger.step("Getting the connected ports after disable from halfpie section.")
            connected_ports_disable_halfpie = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_clicking_hostname_mac_hyperlinks_halfpie_check(node_1)
            logger.info(f"The connected ports from legend section are: {connected_ports_disable_halfpie}")

            assert connected_ports_disable_legend == connected_ports_disable_halfpie, "The ports from legend and halfpie section are not the same."

            logger.step("Enable the first port of each speed.")
            cli.disable_enable_ports(node_1, port_list_string, action="enable")
            time.sleep(15)

            logger.step("Clicking the refresh button...")
            res = auto_actions.click(MLInsWebElements.get_n360_monitor_port_connection_speed_section_refresh_page())
            assert res != -1, "Unable to click the refresh button."

            time.sleep(60)
            
            connected_ports_enable_legend = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_clicking_hostname_mac_hyperlinks_legend_check(node_1)
            logger.info(f"The connected ports from legend section are: {connected_ports_enable_legend}")

            connected_ports_enable_halfpie = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_clicking_hostname_mac_hyperlinks_halfpie_check(node_1)
            logger.info(f"The connected ports from legend section are: {connected_ports_enable_halfpie}")

            assert connected_ports_enable_legend == connected_ports, "The ports after enable are the same for the legend section."
            assert connected_ports_enable_halfpie == connected_ports, "The ports after enable are the same for the halfpie section."

        finally:
            
            logger.step("Closing Device Health window.")
            if close_dialog := MLInsWebElements.get_n360_monitor_device_health_window_close_dialog():
                auto_actions.click(close_dialog)
            
            cli.close_connection_with_error_handling(node_1)


@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM25165Tests:

    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_25165
    @pytest.mark.p1
    def test_tcxm_25165(self, node_1, logger, auto_actions, xiq_library_at_class_level, cli, enter_switch_cli):

        MLInsWebElements = MLInsighstMonitorWebElements()
        ml_insights_monitor_option = "All Switches"
        port_list = []

        try:
            logger.step("Navigate to ML Insights -> Network 360 Monitor.")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network360monitor()

            logger.step("Clicking on dropdown arrow.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_drop_down()

            logger.step("Navigate to 'All Switches' option.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(ml_insights_monitor_option)

            logger.step("Clicking the devices card.")
            auto_actions.click(xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card())

            time.sleep(60)
            
            connected_ports = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_clicking_hostname_mac_hyperlinks_legend_check(node_1)
            logger.info(f"The connected ports are: {connected_ports}")

            for i in range(len(connected_ports)):
                if connected_ports[i][0] != "mgmt" and connected_ports[i][1] == "1000 Mbps":
                    logger.info(f"The connected port {connected_ports[i][0]} has the speed 1000 Mbps")
                    port_list.append(connected_ports[i][0])
            
            if (port_list is None) or (len(port_list) < 2):
                pytest.skip("The only connected port is the mgmt one.")
                
            logger.step("Change port's speed to 100 Mbps.")
            with enter_switch_cli(node_1):
                for port in port_list:
                    try:
                        cli.change_port_speed(node_1, port, speed="100 Mbps", connect_to_dut=False, disconnect_from_dut=False)
                    except Exception as exc:
                        logger.warning(exc)
                    else:
                        logger.info(f"Successfully set 100Mbps as port speed for port {port}.")
                        break
                else:
                    pytest.skip(f"Did not find a connected port (with default 1000 Mbps port speed) to set 100 Mbps in the available ports: {port_list}.\n Check the logged warning messages to see the CLI errors")

            time.sleep(25)

            logger.step("Clicking the refresh button...")
            res = auto_actions.click(MLInsWebElements.get_n360_monitor_port_connection_speed_section_refresh_page())
            assert res != -1, "Unable to click the refresh button."

            time.sleep(60)

            logger.step("Verify in Port Connection Speed section that the port's speed has changed to 100 Mbps")
            connected_ports = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_clicking_hostname_mac_hyperlinks_legend_check(node_1)
            logger.info(f"The connected ports from legend section are: {connected_ports}")

            for i in range(len(connected_ports)):
                if connected_ports[i][0] == f"{port}" and connected_ports[i][1] == "100 Mbps":
                    assert connected_ports[i] == (port, '100 Mbps'), f"The port {port} doesn't have the speed 100 Mbps."
                    logger.info(f"The port {port} has the speed 100 Mbps in Port Connection Speed section")

            logger.step("Change port's speed to 10 Mbps.")
            cli.change_port_speed(node_1, port, speed="10 Mbps")
            time.sleep(25)

            logger.step("Clicking the refresh button...")
            res = auto_actions.click(MLInsWebElements.get_n360_monitor_port_connection_speed_section_refresh_page())
            assert res != -1, "Unable to click the refresh button."

            time.sleep(60)
            
            logger.step("Verify in Port Connection Speed section that the port's speed has changed to 10 Mbps")
            connected_ports = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_clicking_hostname_mac_hyperlinks_legend_check(node_1)
            logger.info(f"The connected ports from legend section are: {connected_ports}")

            for i in range(len(connected_ports)):
                if connected_ports[i][0] == f"{port}" and connected_ports[i][1] == "10 Mbps":
                    assert connected_ports[i] == (port, '10 Mbps'), f"The port {port} doesn't have the speed 10 Mbps."
                    logger.info(f"The port {port} has the speed 10 Mbps in Port Connection Speed section")

            logger.step("Change port's speed back to 1000 Mbps.")
            cli.change_port_speed(node_1, port, speed="1000 Mbps")
            time.sleep(25)

            logger.step("Clicking the refresh button...")
            res = auto_actions.click(MLInsWebElements.get_n360_monitor_port_connection_speed_section_refresh_page())
            assert res != -1, "Unable to click the refresh button."

            time.sleep(60)
            
            logger.step("Verify in Port Connection Speed section that the port's speed has changed to 1000 Mbps")
            connected_ports = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_clicking_hostname_mac_hyperlinks_legend_check(node_1)
            logger.info(f"The connected ports from legend section are: {connected_ports}")

            for i in range(len(connected_ports)):
                if connected_ports[i][0] == f"{port}" and connected_ports[i][1] == "1000 Mbps":
                    assert connected_ports[i] == (port, '1000 Mbps'), f"The port {port} doesn't have the speed 1000 Mbps."
                    logger.info(f"The port {port} has the speed 100 Mbps in Port Connection Speed section")

        finally:
            logger.step("Closing Device Health window.")
            if close_dialog := MLInsWebElements.get_n360_monitor_device_health_window_close_dialog():
                auto_actions.click(close_dialog)
            
            cli.close_connection_with_error_handling(node_1)


@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM25166Tests:

    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_25166
    @pytest.mark.p1
    def test_tcxm_25166(self, node_1, logger, auto_actions, reset_utils, xiq_library_at_class_level, cli, loaded_config, network_manager, dev_cmd, default_library):

        MLInsWebElements = MLInsighstMonitorWebElements()
        ml_insights_monitor_option = "All Switches"

        try:
            logger.step("Navigate to ML Insights -> Network 360 Monitor.")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network360monitor()

            logger.step("Clicking on dropdown arrow.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_drop_down()

            logger.step("Navigate to 'All Switches' option.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(ml_insights_monitor_option)

            logger.step("Clicking the devices card.")
            auto_actions.click(xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card())
            time.sleep(60)

            logger.step("Clicking the refresh button...")
            res = auto_actions.click(MLInsWebElements.get_n360_monitor_port_connection_speed_section_refresh_page())
            assert res != -1, "Unable to click the refresh button."
            
            time.sleep(60)
            
            logger.step("Getting the number of ports for each speed in legend section.")
            before_reboot_legend = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_legend_ports_number(node_1)
            logger.info(f"The number of ports (legend) for each speed before reboot is : {before_reboot_legend}")
            time.sleep(10)

            logger.step("Getting the number of ports for each speed in halfpie section.")
            before_reboot_halfpie = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_halfpie_ports_number(node_1)
            logger.info(f"The number of ports (halfpie) for each speed before reboot is : {before_reboot_halfpie}")

            logger.step("Closing the device health window.")
            res = auto_actions.click(MLInsWebElements.get_n360_monitor_device_health_window_close_dialog())
            assert res != -1, "Unable to close the device health window."

            try:
                network_manager.connect_to_network_element_name(node_1.name)
                if node_1.cli_type.upper() == "VOSS":
                    dev_cmd.send_cmd(node_1.name, 'save config', max_wait=10, interval=2)
                elif node_1.cli_type.upper() == "EXOS":
                    dev_cmd.send_cmd(node_1.name, 'save configuration', max_wait=10, interval=2,
                                    confirmation_phrases='Do you want to save configuration to primary.cfg and overwrite it?',
                                    confirmation_args='y')
                reset_utils.reboot_network_element_now_and_wait(node_1.name, max_wait=300)
                
            finally:
                network_manager.close_connection_to_network_element(node_1.name)

            time.sleep(300)

            logger.step("Clicking the devices card.")
            auto_actions.click(xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card())
            time.sleep(20)

            logger.step("Clicking the refresh button...")
            res = auto_actions.click(MLInsWebElements.get_n360_monitor_port_connection_speed_section_refresh_page())
            assert res != -1, "Unable to click the refresh button."
            time.sleep(30)
            
            logger.step("Getting the number of ports for each speed in legend section after reboot.")
            after_reboot_legend = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_legend_ports_number(node_1)
            logger.info(f"The number of ports for each speed after reboot is : {after_reboot_legend}")

            logger.step("Clicking the refresh button...")
            res = auto_actions.click(MLInsWebElements.get_n360_monitor_port_connection_speed_section_refresh_page())
            assert res != -1, "Unable to click the refresh button."
            time.sleep(20)

            logger.step("Getting the number of ports for each speed in halfpie section after reboot.")
            after_reboot_halfpie = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_halfpie_ports_number(node_1)
            logger.info(f"The number of ports for each speed after reboot is : {after_reboot_halfpie}")

            assert before_reboot_legend == after_reboot_legend, "Port speed tables differ."
            assert before_reboot_halfpie == after_reboot_halfpie, "Port speed tables differ."

        finally:
            logger.step("Closing Device Health window.")
            if close_dialog := MLInsWebElements.get_n360_monitor_device_health_window_close_dialog():
                auto_actions.click(close_dialog)
            
            cli.close_connection_with_error_handling(node_1)


@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM25167Tests:

    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_25167
    @pytest.mark.p1
    def test_tcxm_25167(self, node_1, logger, auto_actions, xiq_library_at_class_level, cli, node_1_onboarding_location):

        MLInsWebElements = MLInsighstMonitorWebElements()
        ml_insights_monitor_option = "All Switches"

        try:
            logger.step("Navigate to ML Insights -> Network 360 Monitor.")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network360monitor()

            logger.step("Clicking on dropdown arrow.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_drop_down()

            logger.step("Navigate to 'All Switches' option.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(ml_insights_monitor_option)

            logger.step("Clicking the devices card.")
            auto_actions.click(xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card())
            time.sleep(60)

            logger.step("Getting the number of ports for each speed in legend section before offboarding.")
            before_offboarding_legend = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_legend_ports_number(node_1)
            logger.info(f"The number of ports for each speed before offboarding is : {before_offboarding_legend}")
            time.sleep(10)

            logger.step("Getting the number of ports for each speed in halfpie section before offboarding.")
            before_offboarding_halfpie = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_halfpie_ports_number(node_1)
            logger.info(f"The number of ports for each speed before offboarding is : {before_offboarding_halfpie}")

            logger.step("Closing the device health window.")
            res = auto_actions.click(MLInsWebElements.get_n360_monitor_device_health_window_close_dialog())
            assert res != -1, "Unable to close the device health window."

            logger.step("Offboarding the device..")
            xiq_library_at_class_level.xflowscommonDevices._goto_devices()
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial)

            logger.step("Navigate to ML Insights -> Network 360 Monitor.")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network360monitor()

            logger.step("Clicking on dropdown arrow.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_drop_down()

            logger.step("Navigate to 'All Switches' option.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(ml_insights_monitor_option)

            logger.step("Clicking the devices card.")
            auto_actions.click(xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card())
            time.sleep(20)

            logger.step("Verifying there are not speed hyperlinks under the Port Connection Speed section...")
            no_data = MLInsWebElements.get_n360_monitor_port_connection_speed_section_no_data()
            assert no_data, "The Port Connection Speed section is not empty"
            time.sleep(10)

            logger.step("Closing the device health window.")
            res = auto_actions.click(MLInsWebElements.get_n360_monitor_device_health_window_close_dialog())
            assert res != -1, "Unable to close the device health window."

            xiq_library_at_class_level.xflowscommonDevices._goto_devices()
            
            logger.step("Onboarding the device...")
            xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick({**node_1, "location": node_1_onboarding_location})

            time.sleep(60)
            xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(device_mac=node_1.mac)
                
            logger.step("Navigate to ML Insights -> Network 360 Monitor.")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network360monitor()

            logger.step("Clicking on dropdown arrow.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_drop_down()

            logger.step("Navigate to 'All Switches' option.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(ml_insights_monitor_option)

            time.sleep(25)
            logger.step("Clicking the devices card.")
            auto_actions.click(xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card())

            time.sleep(60)
            
            logger.step("Getting the number of ports for each speed in legend section after onboarding.")
            after_onboarding_legend = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_legend_ports_number(node_1)
            logger.info(f"The number of ports for each speed after onboarding is : {after_onboarding_legend }")

            assert before_offboarding_legend == after_onboarding_legend, "Port speed tables differ."
            time.sleep(20)
            logger.step("Getting the number of ports for each speed in halfpie section after onboarding.")
            after_onboarding_halfpie = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_halfpie_ports_number(node_1)
            logger.info(f"The number of ports for each speed after onboarding is : {after_onboarding_halfpie}")

            assert before_offboarding_halfpie == after_onboarding_halfpie, "Port speed tables differ."

        finally:
            logger.step("Closing Device Health window.")
            if close_dialog := MLInsWebElements.get_n360_monitor_device_health_window_close_dialog():
                auto_actions.click(close_dialog)
            
            xiq_library_at_class_level.xflowscommonDevices._goto_devices()
            
            if xiq_library_at_class_level.xflowscommonDevices.search_device(device_mac=node_1.mac) == -1:
                xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick({**node_1, "location": node_1_onboarding_location})
                time.sleep(60)
                xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(device_mac=node_1.mac)
            
            cli.close_connection_with_error_handling(node_1)


@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM25168Tests:

    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_25168
    @pytest.mark.p1
    def test_tcxm_25168(self, node_1, logger, auto_actions, xiq_library_at_class_level, loaded_config, cli):

        MLInsWebElements = MLInsighstMonitorWebElements()
        ml_insights_monitor_option = "All Switches"

        try:
            logger.step("Navigate to ML Insights -> Network 360 Monitor.")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network360monitor()

            logger.step("Clicking on dropdown arrow.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_drop_down()

            logger.step("Navigate to 'All Switches' option.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(ml_insights_monitor_option)

            logger.step("Clicking the devices card.")
            auto_actions.click(xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card())

            time.sleep(60)
            
            logger.step("Getting the number of ports from legend section before bounce.")
            before_bounce_legend = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_legend_ports_number(node_1)
            logger.info(f"The number of ports for each speed before bounce is : {before_bounce_legend}")
            time.sleep(10)
            logger.step("Getting the number of ports from halfpie section before bounce.")
            before_bounce_halfpie = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_halfpie_ports_number(node_1)
            logger.info(f"The number of ports for each speed before bounce is : {before_bounce_halfpie}")

            logger.step("Closing the device health window.")
            res = auto_actions.click(MLInsWebElements.get_n360_monitor_device_health_window_close_dialog())
            assert res != -1, "Unable to close the device health window."

            logger.step("Bouncing the IqAgent.")
            cli.bounce_IQAgent(node_1)

            logger.step("Navigate to ML Insights -> Network 360 Monitor.")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network360monitor()

            logger.step("Clicking on dropdown arrow.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_drop_down()

            logger.step("Navigate to 'All Switches' option.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(ml_insights_monitor_option)

            logger.step("Clicking the devices card.")
            auto_actions.click(xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card())

            time.sleep(60)
            
            logger.step("Getting the number of ports from legend section after bounce.")
            after_bounce_legend = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_legend_ports_number(node_1)
            logger.info(f"The number of ports for each speed after bounce is : {after_bounce_legend}")
            assert before_bounce_legend == after_bounce_legend, "Port speed tables differ."
            time.sleep(20)
            logger.step("Getting the number of ports from halfpie section after bounce.")
            after_bounce_halfpie = xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_halfpie_ports_number(node_1)
            logger.info(f"The number of ports for each speed after bounce is : {after_bounce_halfpie}")
            assert before_bounce_halfpie == after_bounce_halfpie, "Port speed tables differ."

        finally:
            
            logger.step("Closing Device Health window.")
            if close_dialog := MLInsWebElements.get_n360_monitor_device_health_window_close_dialog():
                auto_actions.click(close_dialog)
            
            cli.close_connection_with_error_handling(node_1)

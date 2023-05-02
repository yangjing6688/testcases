import pytest
import re
import time


@pytest.mark.p1
#@pytest.mark.dependson("tcxm_xiq_onboarding")
class XIQ9129Tests:
    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_25174
    def test_tcxm_25174(self, loaded_config, auto_actions, logger, utils, xiq_library_at_class_level,
                        network_360_monitor_elements):

        try:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_25174_run'
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(
                option="All Switches")
            logger.info("Clicking the devices card...")
            res = auto_actions.click(
                xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card())
            assert res != -1, "Unable to click the devices card"

            elem1 = network_360_monitor_elements.get_graph_line_color
            elem2 = network_360_monitor_elements.get_graph_point
            elem3 = network_360_monitor_elements.get_graph_point_hover
            x = elem1(0)
            retries = 0
            while x is None or x.size['width'] < 1000:
                logger.info('Waiting for graph to get populated with data.')
                utils.wait_till(timeout=5)
                auto_actions.click(network_360_monitor_elements.get_n360_device_health_refresh_btn())
                x = elem1(0)
                logger.info('Waiting another 5 sec for the device to send data.')
                retries += 1
                if retries >= 20:
                    logger.info(f'To many retries: {retries}')
                    break
            for i in range(0, 3):
                utils.wait_till(timeout=3)
                if i == 0:
                    auto_actions.click(network_360_monitor_elements.get_graph_legend_names(i + 1))
                    auto_actions.click(network_360_monitor_elements.get_graph_legend_names(i + 2))
                    logger.info(f'Hovering on BLUE line:')
                elif i == 1:
                    auto_actions.click(network_360_monitor_elements.get_graph_legend_names(i - 1))
                    auto_actions.click(network_360_monitor_elements.get_graph_legend_names(i + 1))
                    logger.info(f'Hovering on YELLOW line:')
                elif i == 2:
                    auto_actions.click(network_360_monitor_elements.get_graph_legend_names(i - 2))
                    auto_actions.click(network_360_monitor_elements.get_graph_legend_names(i - 1))
                    logger.info(f'Hovering on RED line:')
                auto_actions.move_to_element(elem1(i))
                auto_actions.move_mouse_with_offset((elem1(0).size["width"]-11)//2, 0)
                auto_actions.move_to_element(elem2(i))
                auto_actions.move_to_element(elem3(i))
                assert network_360_monitor_elements.get_n360_graph_tooltip().get_attribute(
                    "opacity") == '1', "Tooltip is not visible!"
                tooltip_info_elm = network_360_monitor_elements.get_n360_graph_tooltip_info()
                matched_info = re.compile(
                    r'\d*-\d*-\d* \d*:\d*:\d*|USAGE|CLIENT|HEALTH|Click on graph line for more information')
                for info in tooltip_info_elm:
                    logger.info(f'Found {info.text}')
                    assert re.findall(matched_info, info.text), f"The {info.text} from tooltip should not be there!"
                if i == 0:
                    auto_actions.click(network_360_monitor_elements.get_graph_legend_names(i + 1))
                    auto_actions.click(network_360_monitor_elements.get_graph_legend_names(i + 2))
                elif i == 1:
                    auto_actions.click(network_360_monitor_elements.get_graph_legend_names(i - 1))
                    auto_actions.click(network_360_monitor_elements.get_graph_legend_names(i + 1))
                elif i == 2:
                    auto_actions.click(network_360_monitor_elements.get_graph_legend_names(i - 2))
                    auto_actions.click(network_360_monitor_elements.get_graph_legend_names(i - 1))
        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_25174_finally'
            logger.info("Closing dialog box.")
            auto_actions.click_reference(network_360_monitor_elements.get_close_n360_dialog_box)

    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_25176
    def test_tcxm_25176(self, loaded_config, auto_actions, logger, xiq_library_at_class_level,
                        network_360_monitor_elements, navigator):
        try:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_25176_run'
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(
                option="All Switches")
            logger.info("Clicking the devices card...")
            res = auto_actions.click_reference(network_360_monitor_elements.get_n360_monitor_devices_card)
            assert res != -1, "Unable to click the devices card"
            navigator.wait_until_loading_is_done()
            settings_btn = network_360_monitor_elements.get_n360_device_health_settings()
            auto_actions.click(settings_btn)
            event_flags_existing = ['Power Supply Mode Change Events', 'DFS Events', 'Channel Change Events',
                                    'Device Connect/Disconnect', 'Stack Events', 'Port Up/Down',
                                    'CPU Crossed Threshold', 'Memory Crossed Threshold',
                                    'Temperature Crossed Threshold',
                                    'MAC Address Table Crossed Threshold', 'PoE Consumption Crossed Threshold']

            event_flags_list_elem = network_360_monitor_elements.get_n360_device_health_events_list()
            event_flags_list = []
            for _ in event_flags_list_elem:
                event_flags_list.append(_.text)
            for event in event_flags_list:
                if event:
                    assert any(event in existing_event for existing_event in
                               event_flags_existing), f"Event {event} is missing!"
            logger.info("Checking that clicking on an element unchecks the checkbox")
            for elem in event_flags_list_elem:
                if elem.is_displayed():
                    auto_actions.click(elem)
                    assert not elem.is_selected(), f"Element {elem.text} did not unchecked after clicking."
        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_25176_finally'
            auto_actions.click_reference(network_360_monitor_elements.get_close_n360_dialog_box)

    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_25193
    def test_tcxm_25193(self, loaded_config, auto_actions, logger, utils, xiq_library_at_class_level,
                        network_360_monitor_elements, navigator):

        try:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_25193_run'
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(
                option="All Switches")
            logger.info("Clicking the devices card...")
            res = auto_actions.click_reference(
                xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card)
            assert res != -1, "Unable to click the devices card"
            navigator.wait_until_loading_is_done()
            elem1 = network_360_monitor_elements.get_graph_line_color
            elem2 = network_360_monitor_elements.get_graph_point
            elem3 = network_360_monitor_elements.get_graph_point_hover
            x = elem1(0)
            retries = 0
            while x is None or x.size['width'] < 1000:
                logger.info('Waiting for graph to get populated with data.')
                utils.wait_till(timeout=5)
                auto_actions.click(network_360_monitor_elements.get_n360_device_health_refresh_btn())
                x = elem1(0)
                logger.info('Waiting another 5 sec for the device to send data.')
                retries += 1
                if retries >= 20:
                    logger.info(f'To many retries: {retries}')
                    break
            logger.info("Entering table view.")

            auto_actions.click(network_360_monitor_elements.get_graph_legend_names(1))
            auto_actions.click(network_360_monitor_elements.get_graph_legend_names(2))
            auto_actions.move_to_element(elem1(0))
            auto_actions.move_mouse_with_offset((elem1(0).size["width"]-11)//2, 0)
            auto_actions.move_to_element(elem2(0))
            auto_actions.move_to_element(elem3(0))
            logger.info('Clicking on line.')
            auto_actions.mouse_left_click()
            utils.wait_till(timeout=5)
            logger.info('Verify if the searchbox is present: ')
            search_box = network_360_monitor_elements.get_n360_device_health_search_box()
            assert search_box != -1, "Unable to verify if the searchbox is present"

            logger.info('Verify if the Total Client Usage section is present above the table ')
            total_usage = network_360_monitor_elements.get_n360_device_health_total_usage()
            assert "Total Client" in total_usage.text, "The Total Client Usage section in not displayed correctly"

            logger.info('Verify if the "Download Button" is present')
            download_button = network_360_monitor_elements.get_n360_device_health_download_button()
            if download_button.is_displayed():
                logger.info("Download Button is present")
            else:
                pytest.fail("Download button not visible")

            logger.info('Verify the table header')
            headers = network_360_monitor_elements.get_n360_device_health_column_header()
            given_headers = ["HOST NAME", "MAC ADDRESS", "DATA USAGE", "HEALTH SCORE"]
            assert any(i in headers.text for i in given_headers), "Failed"

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_25193_finally'
            auto_actions.click_reference(network_360_monitor_elements.get_close_n360_dialog_box)

    @pytest.mark.testbed_1_node
    @pytest.mark.tcxm_25194
    def test_tcxm_25194(self, loaded_config, auto_actions, logger, utils, xiq_library_at_class_level,
                        network_360_monitor_elements, node_1_hostname, node_1, navigator):

        try:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_25194_run'
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(
                option="All Switches")
            logger.info("Clicking the devices card...")
            res = auto_actions.click_reference(
                xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card)
            assert res != -1, "Unable to click the devices card"
            navigator.wait_until_loading_is_done()
            elem1 = network_360_monitor_elements.get_graph_line_color
            elem2 = network_360_monitor_elements.get_graph_point
            elem3 = network_360_monitor_elements.get_graph_point_hover
            x = elem1(0)
            retries = 0
            while x is None or x.size['width'] < 1000:
                logger.info('Waiting for graph to get populated with data.')
                utils.wait_till(timeout=5)
                auto_actions.click(network_360_monitor_elements.get_n360_device_health_refresh_btn())
                x = elem1(0)
                logger.info('Waiting another 5 sec for the device to send data.')
                retries += 1
                if retries >= 20:
                    logger.info(f'To many retries: {retries}')
                    break
            logger.info("Entering table view.")
            auto_actions.click(network_360_monitor_elements.get_graph_legend_names(1))
            auto_actions.click(network_360_monitor_elements.get_graph_legend_names(2))
            auto_actions.move_to_element(elem1(0))
            auto_actions.move_mouse_with_offset((elem1(0).size["width"]-11)//2, 0)
            auto_actions.move_to_element(elem2(0))
            auto_actions.move_to_element(elem3(0))
            logger.info('Clicking on line.')
            auto_actions.mouse_left_click()
            utils.wait_till(timeout=5)
            logger.info('Get HOSTNAME and MAC ADDRESS from dut')

            table_elem = network_360_monitor_elements.get_n360_monitor_port_device_health_usage_table_rows()
            if not table_elem:
                pytest.fail("No elements were found on the table.")
            else:
                found = False
                for row in table_elem:
                    logger.info(f"Table elements are: {row.text}")
                    if row.text.split()[0] == node_1_hostname and row.text.split()[1] == node_1.mac:
                        logger.info("Test is successfully. Values from the table matches those on CLI.")
                        found = True
                        break
                    else:
                        logger.info("Trying next row.")
                if not found:
                    pytest.fail("No matches found!")

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_25194_finally'
            auto_actions.click_reference(network_360_monitor_elements.get_close_n360_dialog_box)

    @pytest.mark.testbed_2_node
    @pytest.mark.tcxm_25195
    def test_tcxm_25195(self, loaded_config, auto_actions, logger, utils, xiq_library_at_class_level,
                        network_360_monitor_elements, node_1_hostname, node_2_hostname, navigator, node_1, node_2):

        try:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_25195_run'
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(
                option="All Switches")
            logger.info("Clicking the devices card...")
            res = auto_actions.click_reference(
                xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card)
            assert res != -1, "Unable to click the devices card"
            utils.wait_till(timeout=2)
            navigator.wait_until_loading_is_done()
            elem1 = network_360_monitor_elements.get_graph_line_color
            elem2 = network_360_monitor_elements.get_graph_point
            elem3 = network_360_monitor_elements.get_graph_point_hover
            x = elem1(0)
            retries = 0
            while x is None or x.size['width'] < 1000:
                logger.info('Waiting for graph to get populated with data.')
                time.sleep(5)
                auto_actions.click(network_360_monitor_elements.get_n360_device_health_refresh_btn())
                x = elem1(0)
                logger.info('Waiting another 5 sec for the device to send data.')
                retries += 1
                if retries >= 20:
                    logger.info(f'To many retries: {retries}')
                    break
            logger.info("Entering table view.")
            auto_actions.click(network_360_monitor_elements.get_graph_legend_names(1))
            auto_actions.click(network_360_monitor_elements.get_graph_legend_names(2))
            auto_actions.move_to_element(elem1(0))
            auto_actions.move_mouse_with_offset((elem1(0).size["width"]-11)//2, 0)
            auto_actions.move_to_element(elem2(0))
            auto_actions.move_to_element(elem3(0))
            logger.info('Clicking on line.')
            auto_actions.mouse_left_click()
            utils.wait_till(timeout=5)

            logger.info('Verify if the searchbox is present: ')
            search_box = network_360_monitor_elements.get_n360_device_health_search_box()
            assert search_box != -1, "Unable to verify if the searchbox is present"

            logger.info('Verify if the Total Client Usage section is present above the table ')
            total_usage = network_360_monitor_elements.get_n360_device_health_total_usage()
            assert total_usage.is_displayed(), "Total Client Usage section is not visible on page."
            assert "Total Client Usage" in total_usage.text, "The Total Client Usage section in not displayed correctly"

            logger.info('Verify it the Download Button is present')
            download_button = network_360_monitor_elements.get_n360_device_health_download_button()
            assert download_button.is_displayed(), "Download Button is not present"

            logger.info('Verify the table header')
            headers = network_360_monitor_elements.get_n360_device_health_column_header()
            given_headers = ["HOST NAME", "MAC ADDRESS", "DATA USAGE", "HEALTH SCORE"]
            assert any(i in headers.text for i in given_headers), "Failed to find all the column header."

            logger.info("Getting the initial table elements.")
            table_elem = network_360_monitor_elements.get_n360_monitor_port_device_health_usage_table_rows()
            if not table_elem:
                pytest.fail("No elements were found on the table.")
            table_dict = {}
            for i in range(len(table_elem)):
                table_dict[i] = table_elem[i].text
            if len(table_dict) < 2:
                pytest.fail("Need at least 2 devices in N360 for this test.")

            else:
                for value in table_dict.values():
                    logger.info(f"Table elements are: {value}")
                    if value.split()[0] == node_1_hostname and value.split()[1] == node_1.mac or value.split()[0] == node_2_hostname and value.split()[1] == node_2.mac:
                        logger.info("Test is successfully. Values from the table matches those on CLI.")
                    else:
                        pytest.fail("No match found!")
        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_25195_finally'
            auto_actions.click_reference(network_360_monitor_elements.get_close_n360_dialog_box)

    @pytest.mark.testbed_2_node
    @pytest.mark.tcxm_25196
    def test_tcxm_25196(self, loaded_config, auto_actions, logger, utils, xiq_library_at_class_level,
                        network_360_monitor_elements, navigator):
        try:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_25196_run'
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(
                option="All Switches")
            logger.info("Clicking the devices card...")
            res = auto_actions.click_reference(
                xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card)
            assert res != -1, "Unable to click the devices card"
            utils.wait_till(timeout=2)
            navigator.wait_until_loading_is_done()
            elem1 = network_360_monitor_elements.get_graph_line_color
            elem2 = network_360_monitor_elements.get_graph_point
            elem3 = network_360_monitor_elements.get_graph_point_hover
            x = elem1(0)
            retries = 0
            while x is None or x.size['width'] < 1000:
                logger.info('Waiting for graph to get populated with data.')
                auto_actions.click(network_360_monitor_elements.get_n360_device_health_refresh_btn())
                time.sleep(10)
                x = elem1(0)
                logger.info('Waiting another 10 sec for the device to send data.')
                retries += 1
                if retries >= 60:
                    logger.info(f'To many retries: {retries}')
                    break
            logger.info("Entering table view.")
            auto_actions.click_reference(lambda: network_360_monitor_elements.get_graph_legend_names(1))
            auto_actions.click_reference(lambda: network_360_monitor_elements.get_graph_legend_names(2))
            auto_actions.move_to_element(elem1(0))
            auto_actions.move_mouse_with_offset((elem1(0).size["width"]-11)//2, 0)
            auto_actions.move_to_element(elem2(0))
            auto_actions.move_to_element(elem3(0))
            logger.info('Clicking on line.')
            auto_actions.mouse_left_click()
            utils.wait_till(timeout=5)

            logger.info('Verify if the devices are sorted in the table')
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_device_health_sorting_table()

        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_25196_finally'
            auto_actions.click_reference(network_360_monitor_elements.get_close_n360_dialog_box)

    @pytest.mark.testbed_2_node
    @pytest.mark.tcxm_25179
    def test_tcxm_25179(self, loaded_config, auto_actions, logger, utils, xiq_library_at_class_level,
                        network_360_monitor_elements, navigator, node_1_hostname, node_2_hostname, node_1, node_2):
        try:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_25179_run'
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(
                option="All Switches")
            logger.info("Clicking the devices card...")
            res = auto_actions.click_reference(
                xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card)
            assert res != -1, "Unable to click the devices card"
            navigator.wait_until_loading_is_done()
            elem1 = network_360_monitor_elements.get_graph_line_color
            elem2 = network_360_monitor_elements.get_graph_point
            elem3 = network_360_monitor_elements.get_graph_point_hover
            x = elem1(0)
            retries = 0
            while x is None or x.size['width'] < 1000:
                logger.info('Waiting for graph to get populated with data.')
                time.sleep(5)
                auto_actions.click(network_360_monitor_elements.get_n360_device_health_refresh_btn())
                x = elem1(0)
                logger.info('Waiting another 5 sec for the device to send data.')
                retries += 1
                if retries >= 20:
                    logger.info(f'To many retries: {retries}')
                    break
            logger.info("Entering table view.")
            auto_actions.click_reference(lambda: network_360_monitor_elements.get_graph_legend_names(1))
            auto_actions.click_reference(lambda: network_360_monitor_elements.get_graph_legend_names(2))
            auto_actions.move_to_element(elem1(0))
            auto_actions.move_mouse_with_offset((elem1(0).size["width"]-11)//2, 0)
            auto_actions.move_to_element(elem2(0))
            auto_actions.move_to_element(elem3(0))
            logger.info('Clicking on line.')
            auto_actions.mouse_left_click()
            utils.wait_till(timeout=5)

            logger.info('Entering Hostname in search box')
            auto_actions.send_keys(network_360_monitor_elements.get_n360_device_health_search_box(), node_1_hostname)
            auto_actions.send_enter(network_360_monitor_elements.get_n360_device_health_search_box())
            utils.wait_till(timeout=5)
            table_elem = network_360_monitor_elements.get_n360_monitor_port_device_health_usage_table_rows()
            if not table_elem:
                pytest.fail("No elements were found on the table. Search is not working")
            elif len(table_elem) != 1:
                pytest.fail("Search result is zero or more than 1 row which is not correct!")
            else:
                for row in table_elem:
                    logger.info(f"Table elements are: {row.text}")
                    if row.text.split()[0] == node_1_hostname:
                        logger.info("Test is successfully. Searched hostname is returned.")
                    else:
                        pytest.fail("Search result did not returned the expected result.")
            show_all_btn = network_360_monitor_elements.get_n360_show_all_btn()
            if "fn-hidden" in show_all_btn.get_attribute("class"):
                pytest.fail("The 'Show All' button is missing")
            else:
                auto_actions.click(show_all_btn)
        finally:
            loaded_config['${TEST_NAME}'] = 'test_tcxm_25179_finally'
            auto_actions.click_reference(network_360_monitor_elements.get_close_n360_dialog_box)

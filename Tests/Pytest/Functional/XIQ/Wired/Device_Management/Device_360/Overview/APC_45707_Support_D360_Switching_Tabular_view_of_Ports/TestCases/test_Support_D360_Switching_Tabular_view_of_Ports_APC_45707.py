import pytest
import time
from typing import List
import re


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9311Tests:

    @pytest.mark.tcxm_9310
    def test_9310_verify_default_columns_in_ports_table(self, utils, xiq_library_at_class_level, node_1):

        utils.wait_till(lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))
        table_rows = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_port_table_rows()
        assert table_rows, "Did not find the rows of the ports table"
        xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

    @pytest.mark.tcxm_9311
    def test_9311_verify_default_columns_in_ports_table(self, navigator, utils, auto_actions, xiq_library_at_class_level, logger,
                                                        node_1):
        navigator.wait_until_loading_is_done()
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
        utils.wait_till(lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))

        expected_default_columns = [
            'Port Name', 'LLDP Neighbor', 'Port Status', 'Transmission Mode', 'Port Mode',
            'Access VLAN', 'Tagged VLAN(s)', 'Traffic Received (Rx)', 'Traffic Transmitted (Tx)',
            'Power Used', 'Port Speed'
        ]

        if node_1.cli_type.upper() == "EXOS":
            expected_default_columns.extend(
                [
                    'ELRP Enabled VLAN(s)',
                    'MAC Locking',
                    'Link Aggregation'
                ]
            )

        for _ in range(2):

            checkbox_button = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button()
            checkbox_button.location_once_scrolled_into_view
            auto_actions.click(checkbox_button)
            time.sleep(3)

            all_checkboxes = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
            columns_found_enabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is True]
            logger.info(f"These columns are currently found enabled: {columns_found_enabled}")

            assert sorted(expected_default_columns) == sorted(columns_found_enabled), \
                "Did not find all the expected columns enabled"
            logger.info(f"Successfully found all the expected columns enabled: {expected_default_columns}")

            found_headers = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_description_table_header()
            logger.info(f"The table has these columns viewable: {found_headers}")

            assert len(found_headers) == len(expected_default_columns), \
                "Failed! More columns visible than checkbox enabled"

            for column_name in expected_default_columns:
                assert any(column_name.upper() == header.upper() for header in found_headers), \
                    f"Did not find this column in the table header: {column_name.upper()}"
                logger.info(f"Successfully verified this column is visible in table: {column_name}")

            auto_actions.click(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_refresh_page_button())
            time.sleep(5)

        xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()


@pytest.mark.p2
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9312Tests:

    @pytest.mark.tcxm_9312
    def test_9312_verify_column_picker_usage(self, utils, xiq_library_at_class_level, auto_actions, request, logger,
                                             node_1):

        utils.wait_till(lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))

        checkbox_button, _ = utils.wait_till(
            xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button, delay=2)
        checkbox_button.location_once_scrolled_into_view
        auto_actions.click(checkbox_button)
        time.sleep(3)

        all_checkboxes = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
        default_enabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is True]
        logger.info(f"These columns are enabled by default: {default_enabled}")

        default_disabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is False]
        logger.info(f"These columns are disabled by default: {default_disabled}")

        found_headers = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_description_table_header()
        logger.info(f"The table has these columns viewable: {found_headers}")

        for checkbox_name, stats in all_checkboxes.items():
            is_selected = stats["is_selected"]

            if is_selected:
                assert any(checkbox_name.upper() == header.upper() for header in found_headers), \
                    f"Did not find this column in the table header: {checkbox_name}"
            else:
                assert not any(checkbox_name.upper() == header.upper() for header in found_headers), \
                    f"Found this column in the table header which is not expected: {checkbox_name}"

        def func():

            all_checkboxes = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()

            for checkbox_name, stats in all_checkboxes.items():
                if any([
                    (checkbox_name in default_enabled) and (stats["is_selected"] is False),
                    (checkbox_name in default_disabled) and (stats["is_selected"] is True)
                ]):
                    auto_actions.click(stats["element"])

            auto_actions.click(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button())
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            time.sleep(3)

        request.addfinalizer(func)

        logger.info("Press each checkbox")
        for stats in all_checkboxes.values():
            auto_actions.click(stats["element"])
        time.sleep(3)

        all_checkboxes = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
        found_headers = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_description_table_header()
        logger.info(f"The table has these columns viewable: {found_headers}")

        for checkbox_name, stats in all_checkboxes.items():
            is_selected = stats["is_selected"]

            if checkbox_name in default_enabled:
                assert is_selected is False, f"{checkbox_name} checkbox should be disabled"
                assert not any(checkbox_name.upper() == header.upper() for header in found_headers), \
                    f"Found this column in the table header which is not expected: {checkbox_name}"
            elif checkbox_name in default_disabled:
                assert is_selected is True, f"{checkbox_name} checkbox should be enabled"
                assert any(checkbox_name.upper() == header.upper() for header in found_headers), \
                    f"Did not find this column in the table header: {checkbox_name}"


@pytest.mark.p2
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9313Tests:

    @pytest.fixture(scope="class", autouse=True)
    def setup(self, logger, network_manager, cli, node_1):
        try:
            network_manager.connect_to_network_element_name(node_1.name)
            onboarded_switch = node_1
            ports = sorted(
                cli.get_ports_from_dut(onboarded_switch),
                key=int if onboarded_switch.cli_type.upper() == "EXOS" else (lambda x: int(x.split("/")[1]))
            )
            try:
                cli.set_lldp(onboarded_switch, ports, action="disable")
                cli.bounce_IQAgent(onboarded_switch)
                yield
            finally:
                cli.set_lldp(onboarded_switch, ports, action="enable")
                cli.bounce_IQAgent(onboarded_switch)
        finally:
            cli.close_connection_with_error_handling(node_1)

    @pytest.mark.tcxm_9313
    def test_9313_verify_columns_can_be_sorted_by_name(self, xiq_library_at_class_level, auto_actions, loaded_config,
                                                       utils, cli, logger, node_1, request):

        xiq_ip_address = loaded_config['sw_connection_host']

        ports = sorted(
            cli.get_ports_from_dut(node_1),
            key=int if node_1.cli_type.upper() == "EXOS" else (lambda x: int(x.split("/")[1]))
        )
        logger.info(f"Found these ports available on switch: {ports}")

        utils.wait_till(
            lambda: xiq_library_at_class_level.xflowsglobalsettingsGlobalSetting.change_device_management_settings(
                option="disable"))

        policy_name = "APC_45707_policy_" + node_1.mac[:-3]
        assert xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
            policy_name=policy_name) == 1, f"Failed to create this network policy: {policy_name}"

        xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(policy_name, node_1.mac)

        port_vlan_mapping = {p: str(int(p) * 25) if node_1.cli_type.upper() == "EXOS" else str(
            int(p.split("/")[1]) * 25) for p in ports[:4]}
        logger.info(f"port-vlanid mapping {port_vlan_mapping}")

        def func():
            port_type = "Access Port" if node_1.cli_type.upper() == "EXOS" else "Auto-sense Port"
            access_vlan_id = "1" if node_1.cli_type.upper() == "EXOS" else None

            try:
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                utils.wait_till(
                    lambda: xiq_library_at_class_level.xflowsmanageDevice360.go_to_device_360_port_config(
                        node_1))

                for port in port_vlan_mapping:
                    xiq_library_at_class_level.xflowsmanageDevice360.enter_port_type_and_vlan_id(port=port,
                                                                                                 port_type=port_type,
                                                                                                 access_vlan_id=access_vlan_id,
                                                                                                 device_os=node_1.cli_type.upper())

            finally:
                utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.save_device_360_port_config, delay=2)

                logger.info("Saved the device360 port configuration.")

                utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window, delay=2)
                logger.info("Closed the device360 window")

            xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(policy_name=policy_name,
                                                                                           serial=node_1.serial)

            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial))
            xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_1)
            cli.bounce_IQAgent(node_1, xiq_ip_address)

            try:
                xiq_library_at_class_level.xflowsconfigureNetworkPolicy.delete_network_policy(policy=policy_name)
            except Exception as exc:
                logger.warning(repr(exc))

        request.addfinalizer(func)

        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowsmanageDevice360.go_to_device_360_port_config(
                    node_1))

            for port, vlan in port_vlan_mapping.items():
                logger.info(f"Set {vlan} vlan for {port} port")
                xiq_library_at_class_level.xflowsmanageDevice360.enter_port_type_and_vlan_id(port=port,
                                                                                             port_type="Access Port",
                                                                                             access_vlan_id=vlan,
                                                                                             device_os=node_1.cli_type.upper())

        finally:
            utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.save_device_360_port_config, delay=2)
            logger.info("Saved the device360 port configuration.")

            utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window, delay=2)
            logger.info("Closed the device360 window")

        xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(policy_name=policy_name,
                                                                                       serial=node_1.serial)

        cli.verify_vlan_config_on_switch(node_1, port_vlan_mapping, logger)

        try:

            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))

            xiq_library_at_class_level.xflowsmanageDevice360.select_max_pagination_size()

            time.sleep(5)

            logger.info("The port names rows should be now in ascending order")
            first_order_rows = [r.text for r in
                                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_port_table_rows()]
            first_port_names = [r.split(" ")[0] for r in first_order_rows]
            logger.info(f"Found these port names in the table: {first_port_names}")

            # pop the mgmt port got from xiq d360 because it does not appear in
            # the output of the exos/voss command that shows the available ports
            first_port_names.pop(first_port_names.index("mgmt"))
            # first_port_names.pop(first_port_names.index("PORT"))
            assert first_port_names == sorted(first_port_names,
                                              key=lambda x: int(x)
                                              if node_1.cli_type.upper() == "EXOS" else int(x.split("/")[1])), \
                f"port names are not in ascending order: {first_port_names}"
            logger.info(f"Successfully found the port names in ascending order")

            # the first verification is done for the 'PORT NAME' column of the table
            logger.info(f"Click on the th element with text='PORT NAME' in order to see the ports in descending order")
            auto_actions.click(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()[
                    'PORT NAME'])

            time.sleep(5)

            logger.info("The port names rows should be now in descending order")
            second_order_rows = [r.text for r in
                                 xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_port_table_rows()]
            second_port_names = [r.split(" ")[0] for r in second_order_rows]
            logger.info(f"Found these port names in the table: {second_port_names}")

            second_port_names.pop(second_port_names.index("mgmt"))
            assert second_port_names == sorted(second_port_names,
                                               key=lambda x: int(x)
                                               if node_1.cli_type.upper() == "EXOS" else int(x.split("/")[1]),
                                               reverse=True), \
                f"port names are not in descending order: {second_port_names}"

            logger.info("Check that the port name entries are completely reversed")
            assert [r.split(" ")[0] for r in second_order_rows] == [r.split(" ")[0] for r in first_order_rows][::-1], \
                "port names are not in ascending order"

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
            utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window, delay=2)

        try:

            # the second verification is done for the 'ACCESS VLAN' column of the table
            # voss: auto-sense is enabled by default (ACCESS VLAN on all the ports is set to 'None')

            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))

            xiq_library_at_class_level.xflowsmanageDevice360.select_max_pagination_size()

            table = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table()
            initial_order = [int(row["ACCESS VLAN"]) for row in table] if node_1.cli_type.upper() == "EXOS" else \
                [int(row["ACCESS VLAN"]) for row in table if row["ACCESS VLAN"] != "None"]
            logger.info(f"vlan ids order before clicking on the 'ACCESS VLAN' column: {initial_order}")

            logger.info(f"Verify the vlan is set correctly for each port: {port_vlan_mapping}")
            for port, vlan in port_vlan_mapping.items():
                assert any((row["PORT NAME"] == port) and (row["ACCESS VLAN"] == vlan) for row in table), \
                    f"Did not find an entry in the ports table for vlanid={vlan} and port name={port}"

            auto_actions.click(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()[
                    'ACCESS VLAN'])
            logger.info("The entries in the tabular view should be in ascending order now")

            table = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table()
            ascending_order = [int(row["ACCESS VLAN"]) for row in table] if node_1.cli_type.upper() == "EXOS" else \
                [int(row["ACCESS VLAN"]) for row in table if row["ACCESS VLAN"] != "None"]
            assert sorted(initial_order) == ascending_order, \
                f"The entries should be in ascending order but found: {ascending_order}"
            logger.info("Successfully verified the ascending order after pressing once on the 'ACCESS VLAN' column")

            auto_actions.click(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()[
                    'ACCESS VLAN'])
            logger.info("The entries in the tabular view should be in descending order now")

            table = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table()
            descending_order = [int(row["ACCESS VLAN"]) for row in table] if node_1.cli_type.upper() == "EXOS" else \
                [int(row["ACCESS VLAN"]) for row in table if row["ACCESS VLAN"] != "None"]
            assert sorted(initial_order, reverse=True) == descending_order, \
                f"The entries should be in descending order but found: {descending_order}"
            logger.info(
                "Successfully verified the descending order after presedonce again on the 'ACCESS VLAN' column")

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
            utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window, delay=2)


@pytest.mark.p2
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9314Tests:

    @pytest.mark.tcxm_9314
    def test_9314_verify_column_can_be_resized(self, xiq_library_at_class_level, auto_actions, action_chains,
                                               cloud_driver, utils, logger, node_1):

        for _ in range(3):
            try:
                utils.wait_till(
                    lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))

                ths = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()
                first_column = ths[list(ths)[0]]
                column_name = first_column.text
                initial_width = first_column.size["width"]
                logger.info(f"The width of {column_name} column before resize is {initial_width}px")

                logger.info(f"Increase width of {column_name} column with 10px")
                action = action_chains(cloud_driver.cloud_driver)
                action.move_to_element(first_column).move_by_offset(initial_width / 2 - 1,
                                                                    0).click_and_hold().move_by_offset(
                    10, 0).release().perform()
                time.sleep(5)

                ths = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()
                first_column = ths[list(ths)[0]]
                final_width = first_column.size["width"]
                logger.info(f"The width of {column_name} column after resize is {final_width}px")

                assert initial_width + 10 == final_width
                logger.info("Successfully verified the size of the column increased with 10px")

                auto_actions.click(
                    xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_refresh_page_button())
                time.sleep(5)

                ths = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()
                first_column = ths[list(ths)[0]]
                width_after_refresh = first_column.size["width"]

                assert width_after_refresh == initial_width, f"Failed! The width after refreshing Device 360 is " \
                                                             f"{width_after_refresh}px but expected {initial_width}px"
            except Exception as exc:
                logger.info(exc)
            else:
                logger.info(f"Successfully verified the size of the column after refreshing the Device 360 window")
                break
            finally:
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
        else:
            assert False, "Failed to resize the column"


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9315Tests:

    @pytest.mark.tcxm_9315
    def test_9315_verify_10_rows_are_displayed_by_default(self, xiq_library_at_class_level, auto_actions, utils, logger,
                                                          node_1):

        try:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))

            table_rows = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_port_table_rows()
            assert table_rows, "Did not find the rows of the ports table"
            table_rows[0].location_once_scrolled_into_view

            for row in table_rows:
                logger.info(f"Found this row: {row.text}")

            assert len(table_rows) == 10, f"Error! Expected 10 entries in the ports table but found {len(table_rows)}"
            logger.info("Successfully checked that the ports table has 10 entries")

            paginations = [
                p.text for p in
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes()]
            assert paginations, "Failed to find the paginations for Device 360 tabular ports view"
            logger.info(f"Found paginations: {paginations}")

            for pg in paginations:
                pg_elem = [p for p in
                           xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes()
                           if p.text == pg][0]
                auto_actions.click(pg_elem)
                time.sleep(5)

                current_pagination_size = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_current_pagination_size()  # NOQA
                assert current_pagination_size.text == pg, \
                    f"pagination size is not set to 10; found pagination size: {current_pagination_size}"

            pg_size_default = \
                [p for p in
                 xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes()
                 if p.text == "10"][0]
            auto_actions.click(pg_size_default)
            time.sleep(5)

            table_rows = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_port_table_rows()
            assert table_rows, "Did not find the rows of the ports table"

            for row in table_rows:
                logger.info(f"Found this row: {row.text}")

            assert len(table_rows) == 10, f"Error! Expected 10 entries in the ports table but found {len(table_rows)}"
            logger.info("Successfully checked that the ports table has 10 entries")

            current_pagination_size = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_current_pagination_size()  # NOQA
            assert current_pagination_size.text == '10', \
                f"pagination size is not set to 10;found pagination size: {current_pagination_size}"

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()


@pytest.mark.p2
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9316Tests:

    @pytest.mark.tcxm_9316
    def test_9316_verify_columns_can_be_moved(self, xiq_library_at_class_level, auto_actions, logger, utils, node_1):

        try:

            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))

            for _ in range(3):
                try:

                    ths = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()

                    first_column, second_column = ths[list(ths)[0]], ths[list(ths)[1]]
                    first_column_width = first_column.size.get("width")
                    first_column_name_before_moving = first_column.text
                    logger.info(f"The first column before moving: {first_column_name_before_moving}")

                    second_column_name_before_moving = second_column.text
                    logger.info(f"The second column before moving: {second_column_name_before_moving}")

                    second_column_width = second_column.size.get('width')
                    offset_x = first_column_width + second_column_width - 20
                    logger.info(f"Move first column {first_column_name_before_moving} with {offset_x}px")
                    auto_actions.click_and_hold_element(first_column, offset_value=offset_x)

                    time.sleep(5)

                    ths = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()

                    first_column, second_column = ths[list(ths)[0]], ths[list(ths)[1]]
                    first_column_name_after_moving = first_column.text
                    logger.info(f"The first column after moving: {first_column_name_after_moving}")

                    second_column_name_after_moving = second_column.text
                    logger.info(f"The second column after moving: {second_column_name_after_moving}")

                    assert first_column_name_before_moving == second_column_name_after_moving, \
                        "First column before moving is not equal with the second column after moving"
                    assert second_column_name_before_moving == first_column_name_after_moving, \
                        "Second column before moving is not equal with the first column after moving"
                    logger.info("Succesfully verified that the columns changed their positions")
                except AssertionError as exc:
                    logger.info(exc)
                else:
                    break
            else:
                assert False, f"Failed to move the {first_column_name_before_moving} column"

            auto_actions.click(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_refresh_page_button())
            time.sleep(5)

            ths = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_th_columns()

            first_column, second_column = ths[list(ths)[0]], ths[list(ths)[1]]
            first_column_name_after_refresh = first_column.text
            logger.info(f"The first column after refresh: {first_column_name_after_refresh}")

            second_column_name_after_refresh = second_column.text
            logger.info(f"The second column after refresh: {second_column_name_after_refresh}")

            assert first_column_name_after_refresh == first_column_name_before_moving, \
                "The first column after refresh is not equal with the first one before moving"
            assert second_column_name_after_refresh == second_column_name_before_moving, \
                "The seconds column after refresh is not equal with the second one before moving"

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9317Tests:

    @pytest.mark.tcxm_9317
    def test_9317_verify_row_length_can_be_increased_to_20_50_100(self, xiq_library_at_class_level, cli, auto_actions,
                                                                  logger, utils, node_1):

        dut = node_1

        cli_no_ports = cli.get_the_number_of_ports_from_cli(dut)
        logger.info(f"The number of CLI ports is: {cli_no_ports}")

        utils.wait_till(
            lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))

        try:
            pagination_number = [20, 50, 100, 10]
            for pag in pagination_number:
                paginations = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes()
                assert paginations, "Failed to find the paginations for Device 360 tabular ports view"
                [pagination] = [pg for pg in paginations if pg.text == str(pag)]
                logger.info(f"Pagination is:{str(pag)}")
                time.sleep(5)

                auto_actions.click(pagination)
                logger.info(f"Selected the pagination size: {pagination.text}")
                time.sleep(3)

                table_rows = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_port_table_rows()
                current_pagination_size = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_current_pagination_size()
                if current_pagination_size.text != str(pag):
                    logger.info(f"Pagination size is not set to {str(pag)}")
                else:
                    logger.info(f"pagination size is already set to {str(pag)}")

                for row in table_rows:
                    logger.info(f"Found this row: {row.text}")

                """The following verifications take into account 5420F platform, VOSS and EXOS.
                On VOSS, if 4 channelized ports are seen in CLI, in XIQ will be seen only 2.
                On EXOS, 4 stacking ports are seen in CLI and only 2 in XIQ.
                The verifications cover the fact that on XIQ can be seen fewer ports than on CLI.
                The number of ports in XIQ include also the management port (no_ports + 1) or less for 5420F (no_ports - 1)
                """

                if cli_no_ports + 1 < pag and len(table_rows) <= cli_no_ports + 1:
                    assert len(
                        table_rows) <= cli_no_ports + 1, f"Error! Expected at least {str(cli_no_ports - 1)} entries in the ports table but found {len(table_rows)}"
                    logger.info(f'The table has:{len(table_rows)} entries')
                    logger.info(
                        f'Successfully checked that the ports table has at least:{str(cli_no_ports - 1)} entries')
                elif cli_no_ports + 1 >= pag and len(table_rows) <= cli_no_ports + 1:
                    assert len(
                        table_rows) == pag, f"Error! Expected {str(pag)} entries in the ports table but found {len(table_rows)}"
                    logger.info(f'Successfully checked that the ports table has:{str(pag)} entries')

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()


@pytest.mark.p2
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9318Tests:

    @pytest.mark.tcxm_9318
    def test_9318_verify_other_rows_display_using_pagination_hyperlink(self, xiq_library_at_class_level, utils, node_1):

        current_page_number = 1
        try:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))

            ports_list_current_page = []
            more_pages = 1

            while more_pages == 1:
                xiq_library_at_class_level.xflowsmanageDevice360.device360_confirm_current_page_number(
                    current_page_number)
                ports_list_reference = ports_list_current_page
                ports_list_current_page = xiq_library_at_class_level.xflowsmanageDevice360.device360_switch_get_current_page_port_name_list()
                assert len(list(set(ports_list_reference).intersection(ports_list_current_page))) == 0, \
                    f"Table on new page share ports with the previous page"
                more_pages = xiq_library_at_class_level.xflowsmanageDevice360.device360_monitor_overview_pagination_next_page_by_number()
                current_page_number = current_page_number + 1

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9319Tests:

    @pytest.mark.tcxm_9319
    def test_9319_verify_lldp_neighbor_column(self, xiq_library_at_class_level, utils, node_1):
        utils.wait_till(
            lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))

        if xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_d360_monitor_lldp_neighbor_header() is None:
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            pytest.fail("Missing LLDP Neighbor column")

        xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9322Tests:

    @pytest.mark.tcxm_9322
    def test_tcxm_9322(self, xiq_library_at_class_level, network_manager, auto_actions, cli, logger, utils, node_1):

        try:
            network_manager.connect_to_network_element_name(node_1.name)
            no_of_ports = len(cli.get_port_list_from_dut_without_not_present_ports(node_1))
        finally:
            network_manager.close_connection_to_network_element(node_1.name)

        logger.info(f'Number of ports for this switch is {no_of_ports}')

        utils.wait_till(
            lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))

        try:
            for i in range(1, no_of_ports):
                auto_actions.click(
                    xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_refresh_page_button())
                for _ in range(4):
                    try:
                        port_icon_present = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ah_icon(
                            i)
                        if port_icon_present:

                            if port_icon_present.get_attribute("data-automation-tag") == "automation-port-console":
                                break
                            utils.wait_till(
                                lambda: xiq_library_at_class_level.xflowsmanageDevice360.device360_left_click_on_port_icon(
                                    i))
                            xiq_library_at_class_level.xflowsmanageDevice360.list_port_element(
                                xiq_library_at_class_level, i, node_1)
                        else:
                            logger.info(f'Port {i} is not displayed on the graphical representation of the DUT!')
                    except:
                        time.sleep(5)
                    else:
                        break
                else:
                    assert False, "Failed: Port details missing"
        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9324Tests:

    @pytest.fixture(scope="class", autouse=True)
    def setup(self, logger, network_manager, cli, node_1):
        try:
            network_manager.connect_to_network_element_name(node_1.name)
            onboarded_switch = node_1
            ports = sorted(
                cli.get_ports_from_dut(onboarded_switch),
                key=int if onboarded_switch.cli_type.upper() == "EXOS" else (lambda x: int(x.split("/")[1]))
            )
            try:
                cli.set_lldp(onboarded_switch, ports, action="disable")
                cli.bounce_IQAgent(onboarded_switch)
                yield
            finally:
                cli.set_lldp(onboarded_switch, ports, action="enable")
                cli.bounce_IQAgent(onboarded_switch)
        finally:
            cli.close_connection_with_error_handling(node_1)

    @pytest.mark.tcxm_9324
    def test_9324_verify_transmission_mode_column(self, logger, node_1, request, loaded_config,
                                                  xiq_library_at_class_level, auto_actions, utils, cli):

        xiq_ip_address = loaded_config['sw_connection_host']

        column_name = "Transmission Mode"
        connected_ports: List[str] = []

        try:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))
            xiq_library_at_class_level.xflowsmanageDevice360.select_max_pagination_size()

            checkbox_button, _ = utils.wait_till(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button, delay=2)
            checkbox_button.location_once_scrolled_into_view
            auto_actions.click(checkbox_button)
            time.sleep(3)

            all_checkboxes = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
            columns_found_enabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is True]
            logger.info(f"These columns are currently found enabled: {columns_found_enabled}")

            assert column_name in columns_found_enabled, f"Failed! {column_name} column is not visible by default"
            logger.info(f"{column_name} column is visible by default")

            ports_table = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table()

            for entry in ports_table:

                assert column_name.upper() in entry, f"Failed to find {column_name} column in table row: {entry}"

                transmission_mode = entry[column_name.upper()]
                port_name = entry['PORT NAME']
                logger.info(f"Row with 'Port Name'='{port_name}' has '{column_name}'='{transmission_mode}'")

                if entry["PORT STATUS"] == "Connected":
                    assert transmission_mode == "Full-Duplex", \
                        f"{port_name} port is connected but transmission mode={transmission_mode} (expected 'Full-Duplex')"
                    logger.info(f"Successfully found transmission_mode='Full-Duplex' for port_name={port_name}")
                    if port_name != "mgmt":
                        connected_ports.append(port_name)

                elif entry["PORT STATUS"] == "Disconnected" and node_1.cli_type.upper() == "VOSS":
                    assert entry[column_name.upper()] == "N/A", \
                        f"{port_name} port is disconnected but transmission mode={transmission_mode} (expected 'N/A')"
                    logger.info(f"Successfully found transmission_mode='N/A' for port_name={port_name}")

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

        unsupported_models = ["FabricEngine5520_48SE", "SwitchEngine5520_48SE"]
        switch_model = node_1.get("model", "")

        if not connected_ports:
            pytest.skip("There are no ports in connected state on the onboarded switch; will skip this test case")
        elif switch_model in unsupported_models:
            pytest.skip(f'Can\'t set half duplex speed on {switch_model} model')
        else:
            connected_ports = connected_ports[:4]
            logger.info(f"Will verify these connected ports: {connected_ports}")

            policy_name = "APC_45707_policy_" + node_1.mac[:-3]

            assert xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
                policy_name=policy_name) == 1, f"Failed to create this network policy: {policy_name}"

            xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(policy_name, node_1.mac)

            def func():
                if node_1.cli_type.upper() == "VOSS":
                    try:
                        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                        utils.wait_till(
                            lambda: xiq_library_at_class_level.xflowsmanageDevice360.go_to_device_360_port_config(
                                node_1))
                        for port in connected_ports:
                            xiq_library_at_class_level.xflowsmanageDevice360.enter_port_type_and_vlan_id(port=port,
                                                                                                         port_type="Auto-sense Port",
                                                                                                         device_os=node_1.cli_type.upper())

                    finally:
                        utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.save_device_360_port_config,
                                        delay=2)
                        logger.info("Saved the device360 port configuration.")

                        xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
                        logger.info("Closed the device360 window")

                try:
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                    utils.wait_till(
                        lambda: xiq_library_at_class_level.xflowsmanageDevice360.go_to_device_360_port_config(
                            node_1))

                    for port in connected_ports:
                        xiq_library_at_class_level.xflowsmanageDevice360.enter_port_transmission_mode(port,
                                                                                                      transmission_mode="Auto")
                finally:
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.save_device_360_port_config,
                                    delay=2)
                    logger.info("Saved the device360 port configuration.")

                    xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
                    logger.info("Closed the device360 window")
                    xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(
                        policy_name=policy_name,
                        serial=node_1.serial)

                    utils.wait_till(
                        lambda: xiq_library_at_class_level.xflowscommonDevices.delete_device(
                            device_serial=node_1.serial))
                    xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_1)
                    cli.bounce_IQAgent(node_1, xiq_ip_address)
                    try:
                        xiq_library_at_class_level.xflowsconfigureNetworkPolicy.delete_network_policy(
                            policy=policy_name)
                    except Exception as exc:
                        logger.warning(repr(exc))

            request.addfinalizer(func)

            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowsglobalsettingsGlobalSetting.change_device_management_settings(
                    option="disable"))
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

            if node_1.cli_type.upper() == "VOSS":

                logger.info(f"Change {connected_ports} ports from auto-sense to access port")
                try:
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                    utils.wait_till(
                        lambda: xiq_library_at_class_level.xflowsmanageDevice360.go_to_device_360_port_config(
                            node_1))

                    for port in connected_ports:
                        logger.info(f"Set vlan 1 for {port} port")
                        xiq_library_at_class_level.xflowsmanageDevice360.enter_port_type_and_vlan_id(port=port,
                                                                                                     port_type="Access Port",
                                                                                                     access_vlan_id="1",
                                                                                                     device_os=node_1.cli_type.upper())

                finally:
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.save_device_360_port_config,
                                    delay=2)
                    logger.info("Saved the device360 port configuration.")

                    xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
                    logger.info("Closed the device360 window")

            try:
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                utils.wait_till(
                    lambda: xiq_library_at_class_level.xflowsmanageDevice360.go_to_device_360_port_config(
                        node_1))

                for port in connected_ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.enter_port_transmission_mode(port,
                                                                                                  transmission_mode="Half-Duplex")

            finally:

                utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.save_device_360_port_config, delay=2)
                logger.info("Saved the device360 port configuration.")

                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
                logger.info("Closed the device360 window")

            xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(policy_name=policy_name,
                                                                                           serial=node_1.serial)

            try:
                utils.wait_till(
                    lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))
                xiq_library_at_class_level.xflowsmanageDevice360.select_max_pagination_size()

                ports_table = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table()
                for row in ports_table:

                    port_name = row["PORT NAME"]
                    transmission_mode = row["TRANSMISSION MODE"]
                    logger.info(f"Row with 'Port Name'='{port_name}' has '{column_name}'='{transmission_mode}'")

                    if port_name in connected_ports:
                        assert transmission_mode == "Half-Duplex", \
                            f"Expected the transmission mode to be Half-Duplex for '{port_name}' port but found '{transmission_mode}'"
                        logger.info(f"Successfully found transmission_mode='Half-Duplex' for port_name='{port_name}'")
            finally:
                xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9325Tests:

    @pytest.fixture(scope="class", autouse=True)
    def setup(self, logger, network_manager, cli, node_1):
        try:
            network_manager.connect_to_network_element_name(node_1.name)
            onboarded_switch = node_1
            ports = sorted(
                cli.get_ports_from_dut(onboarded_switch),
                key=int if onboarded_switch.cli_type.upper() == "EXOS" else (lambda x: int(x.split("/")[1]))
            )
            try:
                cli.set_lldp(onboarded_switch, ports, action="disable")
                cli.bounce_IQAgent(onboarded_switch)
                yield
            finally:
                cli.set_lldp(onboarded_switch, ports, action="enable")
                cli.bounce_IQAgent(onboarded_switch)
        finally:
            cli.close_connection_with_error_handling(node_1)

    @pytest.mark.tcxm_9325
    def test_9325_verify_port_mode_column(self, cli, logger, node_1, request, loaded_config, xiq_library_at_class_level,
                                          utils, auto_actions):

        xiq_ip_address = loaded_config['sw_connection_host']
        column_name = "Port Mode"

        try:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))
            xiq_library_at_class_level.xflowsmanageDevice360.select_max_pagination_size()

            checkbox_button, _ = utils.wait_till(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button, delay=2)
            checkbox_button.location_once_scrolled_into_view
            auto_actions.click(checkbox_button)
            time.sleep(3)

            all_checkboxes = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
            columns_found_enabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is True]
            logger.info(f"These columns are currently found enabled: {columns_found_enabled}")

            assert column_name in columns_found_enabled, f"Failed! {column_name} column is not already visible"
            logger.info(f"{column_name} column is already visible")

            ports_table = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table()

            for entry in ports_table:
                assert column_name.upper() in entry, f"Failed to find {column_name} column in table row: {entry}"

                port_mode = entry[column_name.upper()]
                port_name = entry['PORT NAME']
                logger.info(
                    f"Row with 'Port Name'='{port_name}' has '{column_name}'='{entry[column_name.upper()]}'")

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

        ports = sorted(
            cli.get_ports_from_dut(node_1),
            key=int if node_1.cli_type.upper() == "EXOS" else (lambda x: int(x.split("/")[1]))
        )
        logger.info(f"Found these ports available on switch: {ports}")

        utils.wait_till(
            lambda: xiq_library_at_class_level.xflowsglobalsettingsGlobalSetting.change_device_management_settings(
                option="disable"))
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

        policy_name = "APC_45707_policy_" + node_1.mac[:-3]
        assert xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
            policy_name=policy_name) == 1, f"Failed to create this network policy: {policy_name}"

        xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(policy_name, node_1.mac)

        trunk_ports = ports[:2]
        logger.info(f"Trunk ports: {trunk_ports}")

        port_vlan_mapping = {p: str(int(p) * 25) if node_1.cli_type.upper() == "EXOS" else str(
            int(p.split("/")[1]) * 25) for p in ports[2:6]}
        logger.info(f"port-vlanid mapping: {port_vlan_mapping}")

        def func():

            port_type = "Access Port" if node_1.cli_type.upper() == "EXOS" else "Auto-sense Port"
            access_vlan_id = "1" if node_1.cli_type.upper() == "EXOS" else None

            if node_1.cli_type.upper() == "VOSS":

                try:
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                    utils.wait_till(
                        lambda: xiq_library_at_class_level.xflowsmanageDevice360.go_to_device_360_port_config(
                            node_1))
                    for port in trunk_ports:
                        xiq_library_at_class_level.xflowsmanageDevice360.enter_port_type_and_vlan_id(port=port,
                                                                                                     port_type="Access Port",
                                                                                                     device_os=node_1.cli_type.upper())

                finally:

                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.save_device_360_port_config,
                                    delay=2)
                    logger.info("Saved the device360 port configuration.")

                    xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
                    logger.info("Closed the device360 window")
                xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(policy_name=policy_name,
                                                                                               serial=node_1.serial)

            try:
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                utils.wait_till(
                    lambda: xiq_library_at_class_level.xflowsmanageDevice360.go_to_device_360_port_config(
                        node_1))

                for port in list(port_vlan_mapping) + trunk_ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.enter_port_type_and_vlan_id(port=port,
                                                                                                 port_type=port_type,
                                                                                                 access_vlan_id=access_vlan_id,
                                                                                                 device_os=node_1.cli_type.upper())
            finally:

                utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.save_device_360_port_config, delay=2)
                logger.info("Saved the device360 port configuration.")

                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
                logger.info("Closed the device360 window")

            xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(policy_name=policy_name,
                                                                                           serial=node_1.serial)
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial))
            xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_1)
            cli.bounce_IQAgent(node_1, xiq_ip_address)

            xiq_library_at_class_level.xflowsconfigureNetworkPolicy.delete_network_policy(policy=policy_name)

        request.addfinalizer(func)

        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowsmanageDevice360.go_to_device_360_port_config(
                    node_1))

            for port, vlan in port_vlan_mapping.items():
                logger.info(f"Set {vlan} vlan for {port} port")
                xiq_library_at_class_level.xflowsmanageDevice360.enter_port_type_and_vlan_id(port=port,
                                                                                             port_type="Access Port",
                                                                                             access_vlan_id=vlan,
                                                                                             device_os=node_1.cli_type.upper())

            for port in trunk_ports:
                logger.info(f"Set {port} port as Trunk Port")
                xiq_library_at_class_level.xflowsmanageDevice360.enter_port_type_and_vlan_id(port=port,
                                                                                             port_type="Trunk Port",
                                                                                             device_os=node_1.cli_type.upper())

        finally:
            utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.save_device_360_port_config, delay=2)
            logger.info("Saved the device360 port configuration.")

            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            logger.info("Closed the device360 window")

        xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(policy_name=policy_name,
                                                                                       serial=node_1.serial)

        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))
            xiq_library_at_class_level.xflowsmanageDevice360.select_max_pagination_size()

            ports_table = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table()

            for row in ports_table:

                port_name = row["PORT NAME"]
                port_mode = row[column_name.upper()]

                if port_name in port_vlan_mapping:

                    assert port_mode == "Access", f"Expected port_mode='Access' but found '{port_mode}' for port_name='{port_name}'"
                    logger.info(f"Successfully verified {port_name} port is in Access port mode")

                    assert row["ACCESS VLAN"] == port_vlan_mapping[port_name], \
                        f"Expected vlanid={port_vlan_mapping[port_name]} but found {row['ACCESS VLAN']} for {port_name} port"
                    logger.info(f"Successfully found vlanid='{port_vlan_mapping[port_name]}' for {port_name} port")

                elif port_name in trunk_ports:
                    assert port_mode == "Trunk", f"Expected port_mode='Trunk' but found '{port_mode}' for port_name='{port_name}'"
                    logger.info(f"Successfully verified {port_name} port is in Trunk port mode")

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9326Tests:

    @pytest.fixture(scope="class", autouse=True)
    def setup(self, logger, network_manager, cli, node_1):
        try:
            network_manager.connect_to_network_element_name(node_1.name)
            onboarded_switch = node_1
            ports = sorted(
                cli.get_ports_from_dut(onboarded_switch),
                key=int if onboarded_switch.cli_type.upper() == "EXOS" else (lambda x: int(x.split("/")[1]))
            )
            try:
                cli.set_lldp(onboarded_switch, ports, action="disable")
                cli.bounce_IQAgent(onboarded_switch)
                yield
            finally:
                cli.set_lldp(onboarded_switch, ports, action="enable")
                cli.bounce_IQAgent(onboarded_switch)
        finally:
            cli.close_connection_with_error_handling(node_1)

    @pytest.mark.tcxm_9326
    def test_tcxm_9326(self, cli, logger, node_1, loaded_config, xiq_library_at_class_level, utils, auto_actions,
                       request):

        xiq_ip_address = loaded_config['sw_connection_host']
        column_name = "Port Mode"

        try:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))
            xiq_library_at_class_level.xflowsmanageDevice360.select_max_pagination_size()

            checkbox_button, _ = utils.wait_till(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button, delay=2)
            checkbox_button.location_once_scrolled_into_view
            auto_actions.click(checkbox_button)
            time.sleep(3)

            all_checkboxes = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
            columns_found_enabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is True]
            logger.info(f"These columns are currently found enabled: {columns_found_enabled}")

            assert column_name in columns_found_enabled, f"Failed! {column_name} column is not already visible"
            logger.info(f"{column_name} column is already visible")

            ports_table = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table()

            for entry in ports_table:
                assert column_name.upper() in entry, f"Failed to find {column_name} column in table row: {entry}"

                port_mode = entry[column_name.upper()]
                port_name = entry['PORT NAME']
                logger.info(
                    f"Row with 'Port Name'='{port_name}' has '{column_name}'='{entry[column_name.upper()]}'")

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

        ports = sorted(
            cli.get_ports_from_dut(node_1),
            key=int if node_1.cli_type.upper() == "EXOS" else (lambda x: int(x.split("/")[1]))
        )
        logger.info(f"Found these ports available on switch: {ports}")

        utils.wait_till(
            lambda: xiq_library_at_class_level.xflowsglobalsettingsGlobalSetting.change_device_management_settings(
                option="disable"))
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

        policy_name = "APC_45707_policy_" + node_1.mac[:-3]
        assert xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
            policy_name=policy_name) == 1, f"Failed to create this network policy: {policy_name}"

        xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(policy_name, node_1.mac)

        trunk_ports = ports[:10]
        logger.info(f"Trunk ports: {trunk_ports}")

        access_ports = ports[10:12]
        logger.info(f"Access ports: {access_ports}")

        def func():

            port_type = "Access Port" if node_1.cli_type.upper() == "EXOS" else "Auto-sense Port"
            access_vlan_id = "1" if node_1.cli_type.upper() == "EXOS" else None

            if node_1.cli_type.upper() == "VOSS":

                try:
                    xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                    utils.wait_till(
                        lambda: xiq_library_at_class_level.xflowsmanageDevice360.go_to_device_360_port_config(
                            node_1))
                    for port in trunk_ports:
                        xiq_library_at_class_level.xflowsmanageDevice360.enter_port_type_and_vlan_id(port=port,
                                                                                                     port_type="Access Port",
                                                                                                     device_os=node_1.cli_type.upper())

                finally:
                    utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.save_device_360_port_config,
                                    delay=2)
                    logger.info("Saved the device360 port configuration.")

                    xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
                    logger.info("Closed the device360 window")
                xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(policy_name=policy_name,
                                                                                               serial=node_1.serial)

            try:
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                utils.wait_till(
                    lambda: xiq_library_at_class_level.xflowsmanageDevice360.go_to_device_360_port_config(
                        node_1))

                for port in trunk_ports + access_ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.enter_port_type_and_vlan_id(port=port,
                                                                                                 port_type=port_type,
                                                                                                 access_vlan_id=access_vlan_id,
                                                                                                 device_os=node_1.cli_type.upper())
            finally:

                utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.save_device_360_port_config, delay=2)
                logger.info("Saved the device360 port configuration.")

                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
                logger.info("Closed the device360 window")
            xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(policy_name=policy_name,
                                                                                           serial=node_1.serial)
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial))
            xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_1)
            cli.bounce_IQAgent(node_1, xiq_ip_address)

            try:
                xiq_library_at_class_level.xflowsconfigureNetworkPolicy.delete_network_policy(policy=policy_name)
            except Exception as exc:
                logger(repr(exc))

        request.addfinalizer(func)

        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowsmanageDevice360.go_to_device_360_port_config(
                    node_1))

            for port in trunk_ports:
                logger.info(f"Set {port} port as Trunk Port")
                xiq_library_at_class_level.xflowsmanageDevice360.enter_port_type_and_vlan_id(port=port,
                                                                                             port_type="Trunk Port",
                                                                                             device_os=node_1.cli_type.upper())

        finally:
            utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.save_device_360_port_config, delay=2)
            logger.info("Saved the device360 port configuration.")

            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            logger.info("Closed the device360 window")

        xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(policy_name=policy_name,
                                                                                       serial=node_1.serial)

        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowsmanageDevice360.go_to_device_360_port_config(
                    node_1))

            for port in access_ports:
                temp_vlan = xiq_library_at_class_level.xflowsmanageDevice360.generate_vlan_id()
                logger.info(f"Set {temp_vlan} vlan for {port} port")
                xiq_library_at_class_level.xflowsmanageDevice360.enter_port_type_and_vlan_id(port=port,
                                                                                             port_type="Access Port",
                                                                                             access_vlan_id=temp_vlan,
                                                                                             device_os=node_1.cli_type.upper())

        finally:
            utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.save_device_360_port_config, delay=2)
            logger.info("Saved the device360 port configuration.")

            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            logger.info("Closed the device360 window")

        xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(policy_name=policy_name,
                                                                                       serial=node_1.serial)

        for _ in range(7):
            try:
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                utils.wait_till(
                    lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))
                xiq_library_at_class_level.xflowsmanageDevice360.select_max_pagination_size()

                ports_table = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table()

                for row in ports_table:

                    port_name = row["PORT NAME"]
                    port_mode = row[column_name.upper()]

                    if port_name in trunk_ports:
                        assert port_mode == "Trunk", f"Expected port_mode='Trunk' but found '{port_mode}' for port_name='{port_name}'"
                        logger.info(f"Successfully verified {port_name} port is in Trunk port mode")

            except Exception as exc:
                logger.warning(repr(exc))
                time.sleep(60)
            else:
                break
            finally:
                xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
        else:
            assert False, "Failed to very the port configuration"


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9327Tests:

    @pytest.mark.tcxm_9327
    def test_9327_verify_mgmt_port_details(self, xiq_library_at_class_level, utils, auto_actions, logger, node_1):

        unsupported_platforms = ["X435", "5320 UHW"]
        dut_platform = node_1.get("platform", "")

        if any(re.search(dut_platform, platform) for platform in unsupported_platforms):
            pytest.skip(
                f"The switch platform is {node_1['platform']} and it is not supported; skipping the test case;\nunsupported platforms: {unsupported_platforms}")

        try:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))
            paginations_size = [
                pg.text for pg in
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes()]

            for pg_size_number in paginations_size:

                logger.info(f"Current pagination size is {pg_size_number}")

                xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size(pg_size_number)

                for i in range(1, 99):

                    try:
                        rows = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_port_table_rows()
                        if any(
                                re.search("mgmt.*Management", row.text) for row in rows):
                            logger.info(f"Successfully found the management port in current page {i}")
                            time.sleep(3)
                            break
                        else:
                            logger.info(f"Did not find the management port in the current page: {i}")

                        next_page_button = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_pagination_next_button()
                        assert next_page_button, f"Did not find the next page button (current page is {i})"
                        auto_actions.click(next_page_button)
                        time.sleep(3)

                    except AssertionError as exc:
                        assert False, f"No page left to check: {repr(exc)}"
        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9331Tests:

    @pytest.mark.tcxm_9331
    def test_9331_verify_channelized_ports(self, logger, loaded_config, xiq_library_at_class_level, network_manager,
                                           enter_switch_cli, cli, utils, node_1):
        xiq_ip_address = loaded_config['sw_connection_host']
        if node_1.cli_type.upper() == "EXOS":
            pytest.skip("EXOS platform not supported")

        elif not node_1.get("console_ip") or not node_1.get("console_port"):
            pytest.skip("This test case needs a testbed yaml with console ip and port")

        try:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))

            network_manager.connect_to_network_element_name(node_1.name)
            with enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(node_1.name, 'enable',
                                 max_wait=10,
                                 interval=2)
                dev_cmd.send_cmd(node_1.name, 'configure terminal',
                                 max_wait=10,
                                 interval=2)
                output = dev_cmd.send_cmd(node_1.name, 'show interfaces GigabitEthernet channelize',
                                          max_wait=10,
                                          interval=2)[0].return_text
                match_port = re.findall(r"(\d+)\/(\d+)\s+(false|true)\s+[a-zA-Z0-9]+", output)

                if len(match_port) == 0:
                    output = dev_cmd.send_cmd(node_1.name, 'show boot config flags',
                                              max_wait=10,
                                              interval=2)[0].return_text
                    advanced_flag = re.findall(r"flags\sadvanced-feature-bandwidth-reservation\s([a-zA-Z]+)", output)
                    spbm_flag = re.findall(r"flags\sspbm-config-mode\s([a-zA-Z]+)", output)

                    if advanced_flag != "disable":
                        if spbm_flag == "false":
                            dev_cmd.send_cmd(node_1.name, 'boot config flags spbm-config-mode',
                                             max_wait=10,
                                             interval=2)
                            dev_cmd.send_cmd(node_1.name, 'save config',
                                             max_wait=10,
                                             interval=2)
                            dev_cmd.send_cmd(node_1.name, 'reset -y',
                                             max_wait=10,
                                             interval=2)

                            network_manager.close_connection_to_network_element(node_1.name)
                            time.sleep(240)
                            network_manager.connect_to_network_element_name(node_1.name)

                            logger.info("spbm-config-mode flag has been disabled")

                            dev_cmd.send_cmd(node_1.name, f'enable',
                                             max_wait=10,
                                             interval=2)
                            dev_cmd.send_cmd(node_1.name, f'configure terminal',
                                             max_wait=10,
                                             interval=2)

                        output = dev_cmd.send_cmd(node_1.name, 'no spbm',
                                                  max_wait=10,
                                                  interval=2,
                                                  ignore_cli_feedback=True)[0].return_text
                        error_msg = re.findall("Error: Delete i-sid from Vlan before setting SPBM global flag", output)
                        if error_msg:
                            output = dev_cmd.send_cmd(node_1.name, f'show interfaces GigabitEthernet state',
                                                      max_wait=10,
                                                      interval=2)[0].return_text
                            ports = re.findall(
                                r"(\d+)\/(\d+)\s+(up|down)\s+(up|down)\s+--\s+(\d+)\/(\d+)\/(\d+)\s(\d+):(\d+):(\d+)",
                                output)

                            slots = []
                            num_ports = {}
                            for port in ports:
                                if port[0] not in slots:
                                    slots.append(port[0])
                                if port[0] not in num_ports.keys():
                                    num_ports[port[0]] = 1
                                else:
                                    num_ports[port[0]] += 1

                            for slot in slots:
                                command = "interface GigabitEthernet " + str(slot) + "/1-" + str(slot) + "/" + str(
                                    num_ports[slot])
                                dev_cmd.send_cmd(node_1.name, command,
                                                 max_wait=10,
                                                 interval=2)
                                dev_cmd.send_cmd(node_1.name, 'no auto-sense enable',
                                                 max_wait=10,
                                                 interval=2)
                                dev_cmd.send_cmd(node_1.name, 'exit',
                                                 max_wait=10,
                                                 interval=2)
                                logger.info("auto-sense has been disabled on all ports")

                            dev_cmd.send_cmd(node_1.name, 'no auto-sense onboarding i-sid',
                                             max_wait=10,
                                             interval=2)
                            logger.info("auto-sense onboarding i-sid has been deleted")
                            dev_cmd.send_cmd(node_1.name, 'no vlan i-sid 4048',
                                             max_wait=10,
                                             interval=2)
                            logger.info("vlan onboarding i-sid has been deleted")
                            dev_cmd.send_cmd(node_1.name, 'no router isis enable',
                                             confirmation_phrases='Do you want to continue (y/n) ?',
                                             confirmation_args='y')
                            logger.info("router isis has been disabled")

                        dev_cmd.send_cmd(node_1.name, 'no spbm',
                                         max_wait=10,
                                         interval=2,
                                         ignore_cli_feedback=True)
                        logger.info("spbm has been disabled")
                        dev_cmd.send_cmd(node_1.name, 'no boot config flags advanced-feature-bandwidth-reservation',
                                         max_wait=10,
                                         interval=2)
                        dev_cmd.send_cmd(node_1.name, 'save config',
                                         max_wait=10,
                                         interval=2)
                        dev_cmd.send_cmd(node_1.name, 'reset -y',
                                         max_wait=10,
                                         interval=2)

                        network_manager.close_connection_to_network_element(node_1.name)
                        time.sleep(240)
                        network_manager.connect_to_network_element_name(node_1.name)

                        logger.info("advanced-feature-bandwidth-reservation flag has been disabled")

                        dev_cmd.send_cmd(node_1.name, f'enable',
                                         max_wait=10,
                                         interval=2)
                        dev_cmd.send_cmd(node_1.name, f'configure terminal',
                                         max_wait=10,
                                         interval=2)

                        output = dev_cmd.send_cmd(node_1.name, 'show interfaces GigabitEthernet channelize',
                                                  max_wait=10,
                                                  interval=2)[0].return_text
                        match_port = re.findall(r"(\d+)\/(\d+)\s+(false|true)\s+[a-zA-Z0-9]+", output)

            if len(match_port) > 0:

                already_channelized = []
                for port in match_port:
                    if port[2] == "false":
                        command = "interface GigabitEthernet " + port[0] + "/" + port[1]
                        with enter_switch_cli(node_1) as dev_cmd:
                            dev_cmd.send_cmd(node_1.name, 'enable',
                                             max_wait=10,
                                             interval=2)
                            dev_cmd.send_cmd(node_1.name, 'configure terminal',
                                             max_wait=10,
                                             interval=2)
                            dev_cmd.send_cmd(node_1.name, command)
                            dev_cmd.send_cmd(node_1.name, 'channelize enable',
                                             confirmation_phrases='Do you wish to continue (y/n) ?',
                                             confirmation_args='y')
                    else:
                        already_channelized.append(port[0] + "/" + port[1])
                logger.info("Channelization enabled on all ports")

                time.sleep(200)
                for port in match_port:
                    ok = 0
                    start_time = time.time()
                    while time.time() - start_time < 500:
                        xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page()
                        device_info = xiq_library_at_class_level.xflowsmanageDevice360.device360_get_automation_port_info(
                            port[0] + "/" + port[1])

                        device_port_mode = device_info["port_mode"].split()[2]
                        if device_port_mode != "Channelized":
                            time.sleep(20)
                        else:
                            ok = 1
                            break

                    if ok == 0:
                        cli.no_channel_enable_on_all_ports(node_1)
                        assert ok, f"Failed to change Port Mode {port[1]} to Channelized"

                for port in match_port:
                    command = "interface GigabitEthernet " + port[0] + "/" + port[1] + "/1"
                    with enter_switch_cli(node_1) as dev_cmd:
                        dev_cmd.send_cmd(node_1.name, 'enable',
                                         max_wait=10,
                                         interval=2)
                        dev_cmd.send_cmd(node_1.name, 'configure terminal',
                                         max_wait=10,
                                         interval=2)
                        dev_cmd.send_cmd(node_1.name, command)
                        output = dev_cmd.send_cmd(node_1.name, 'no channelize enable',
                                                  confirmation_phrases='Do you wish to continue (y/n) ?',
                                                  confirmation_args='y',
                                                  ignore_cli_feedback=True)[0].return_text

                logger.info("Channelization disabled on all ports")

                time.sleep(200)
                for port in match_port:
                    str_port = port[0] + "/" + port[1]
                    if str_port in already_channelized:
                        continue

                    ok = 0
                    start_time = time.time()
                    while time.time() - start_time < 500:
                        xiq_library_at_class_level.xflowsmanageDevice360.device360_refresh_page()
                        device_info = xiq_library_at_class_level.xflowsmanageDevice360.device360_get_automation_port_info(
                            port[0] + "/" + port[1])
                        device_port_mode = device_info["port_mode"].split()[2]
                        if device_port_mode == "Channelized":
                            time.sleep(20)
                        else:
                            ok = 1
                            break
                    if ok == 0:
                        cli.no_channel_enable_on_all_ports(node_1)
                        assert ok, f"Failed to change Port Mode {port[1]} back"

        finally:

            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

            try:
                network_manager.connect_to_network_element_name(node_1.name)
            except Exception as exc:
                logger.info(repr(exc))

            # output = dev_cmd.send_cmd(node_1.name, 'show boot config choice',
            #                               max_wait=10,
            #                               interval=2)[0].return_text
            # config_file = re.findall(r"choice primary config-file \"(.*)\"", output)[0]
            # dev_cmd.send_cmd(node_1.name, 'remove ' + config_file,
            #                      confirmation_phrases='Are you sure (y/n) ?',
            #                      confirmation_args='y')
            with enter_switch_cli(node_1) as dev_cmd:
                dev_cmd.send_cmd(node_1.name, 'save config',
                                 max_wait=10,
                                 interval=2)
                dev_cmd.send_cmd(node_1.name, 'reset -y',
                                 max_wait=10,
                                 interval=2)
                network_manager.close_connection_to_network_element(node_1.name)
                time.sleep(240)
                logger.info("Primary choice config file has been deleted")

                network_manager.connect_to_network_element_name(node_1.name)

                dev_cmd.send_cmd(node_1.name, 'enable', max_wait=10, interval=2)
                dev_cmd.send_cmd(node_1.name, 'configure terminal', max_wait=10, interval=2)
                dev_cmd.send_cmd(node_1.name, 'boot config flags sshd', max_wait=10, interval=2)
                dev_cmd.send_cmd(node_1.name, 'boot config flags telnet', max_wait=10, interval=2)
                dev_cmd.send_cmd(node_1.name, 'application', max_wait=10, interval=2)
                dev_cmd.send_cmd(node_1.name, 'no iqagent enable', max_wait=10, interval=2)
                dev_cmd.send_cmd(node_1.name, f'iqagent server {xiq_ip_address}', max_wait=10,
                                 interval=2)
                dev_cmd.send_cmd(node_1.name, 'iqagent enable', max_wait=10, interval=2)

                xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(node_1.serial)
                res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(device_serial=node_1.serial)
                assert res == 'green', f"The device did not come up successfully in the XIQ; Device: {node_1}"

                logger.info("Device come up successfully in the XIQ")


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9562Tests:

    @pytest.mark.tcxm_9562
    def test_tcxm_9562(self, xiq_library_at_class_level, cli, utils, network_manager, node_1):

        dut = node_1

        try:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))
            xiq_library_at_class_level.xflowsmanageDevice360.select_max_pagination_size()

            try:

                network_manager.connect_to_network_element_name(dut.name)
                dut_list_of_ports = cli.get_port_list_from_dut_without_not_present_ports(dut)
                assert dut_list_of_ports != -1, f"Unable to get ports from dut!"
                table_list_of_ports = xiq_library_at_class_level.xflowsmanageDevice360.device360_switch_get_current_page_port_name_list()
                for port in table_list_of_ports:
                    if port in dut_list_of_ports:
                        dut_list_of_ports.remove(port)
                assert len(dut_list_of_ports) == 0, "Some ports were not displayed in the table"
            finally:
                network_manager.close_connection_to_network_element(dut.name)

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            time.sleep(3)


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9563Tests:

    @pytest.mark.tcxm_9563
    def test_tcxm_9563(self, xiq_library_at_class_level, utils, logger, network_manager, node_1, auto_actions):

        dut = node_1
        is_selected = False

        try:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))
            xiq_library_at_class_level.xflowsmanageDevice360.select_max_pagination_size()

            table_rows = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_port_table_rows()
            assert table_rows, "Did not find the rows of the ports table"

            expected_port_type_column = ['Type']

            time.sleep(3)
            found_headers = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_description_table_header()
            logger.info(f"The table has these columns viewable: {found_headers}")

            for column_name in found_headers:
                assert column_name != expected_port_type_column[0].upper(), "Found port type column in the table header"

            checkbox_button = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button()
            auto_actions.click(checkbox_button)
            time.sleep(3)

            all_checkboxes = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
            columns_found_enabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is True]
            logger.info(f"These columns are currently found enabled: {columns_found_enabled}")

            for selected_column_name in columns_found_enabled:
                assert selected_column_name != expected_port_type_column, f"Port type checkbox is selected"

            port_type_checkbox = all_checkboxes['Type']['element']
            auto_actions.click(port_type_checkbox)

            found_headers = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_description_table_header()
            logger.info(f"The table has these columns viewable: {found_headers}")

            if expected_port_type_column[0].upper() in found_headers:
                logger.info("Successfully found port type column in the table header")
                is_selected = True

            try:
                network_manager.connect_to_network_element_name(dut.name)
                xiq_library_at_class_level.xflowsmanageDevice360.check_port_type(dut)
            finally:
                network_manager.close_connection_to_network_element(dut.name)

            time.sleep(3)

        finally:

            expected_port_type_column = ['Type']

            if is_selected:

                checkbox_button = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button()
                if not checkbox_button.is_selected():
                    auto_actions.click(checkbox_button)
                    time.sleep(3)

                all_checkboxes = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
                columns_found_enabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is True]
                logger.info(f"These columns are currently found enabled: {columns_found_enabled}")

                port_type_checkbox = all_checkboxes['Type']['element']
                auto_actions.click(port_type_checkbox)

                for selected_column_name in columns_found_enabled:
                    assert selected_column_name != expected_port_type_column, f"Port type checkbox is selected"

                found_headers = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_description_table_header()
                logger.info(f"The table has these columns viewable: {found_headers}")
                time.sleep(5)
                if expected_port_type_column[0].upper() not in found_headers:
                    logger.info("Port type column is not in the table header")

            else:
                checkbox_button = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button()
                if not checkbox_button.is_selected():
                    auto_actions.click(checkbox_button)
                    time.sleep(3)

                all_checkboxes = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
                columns_found_enabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is True]
                logger.info(f"These columns are currently found enabled: {columns_found_enabled}")

                for selected_column_name in columns_found_enabled:
                    assert selected_column_name != expected_port_type_column, f"Port type checkbox is selected"

                found_headers = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_description_table_header()
                logger(f"The table has these columns viewable: {found_headers}")
                time.sleep(5)
                if expected_port_type_column[0].upper() not in found_headers:
                    logger.info("Port type column is not in the table header")

            xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9565Tests:

    @pytest.mark.tcxm_9565
    def test_9565_check_ports_status(self, cli, utils, dev_cmd, xiq_library_at_class_level, logger, network_manager,
                                     node_1):

        cli.bounce_IQAgent(node_1)

        try:
            network_manager.connect_to_network_element_name(node_1.name)
            cli_ports_status = cli.get_device_port_status(networkElementCliSend=dev_cmd,
                                                          dut=node_1)
        finally:
            network_manager.close_connection_to_network_element(node_1.name)

        if cli_ports_status is None:
            pytest.fail('cli_ports_status=None')

        # get the list of the ports of the device
        match_port = cli_ports_status.keys()

        # retrieve the port status values from XIQ
        logger.info("****************** Getting XIQ ports status: ******************")
        try:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))
            xiq_library_at_class_level.xflowsmanageDevice360.select_max_pagination_size()
            time.sleep(5)
            xiq_port_table_info = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table()

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

        logger.info(xiq_port_table_info)

        # CLI - XIQ speed values comparison
        logger.info("****************** Ports status info ******************")
        for port in match_port:
            # compare the values only if the port is shown in XIQ D360
            table_entry = [e for e in xiq_port_table_info if e['PORT NAME'] == port]
            if table_entry:
                table_entry = table_entry[0]

                xiq_port_status = table_entry["PORT STATUS"]
                if xiq_port_status == "Connected":
                    xiq_port_status_mapped = "up"
                else:
                    xiq_port_status_mapped = "down"
                    # if the admin status is "down", the operate status cannot be
                    # "up", so "Port Disabled by Admin" will be mapped as "down"

                cli_port_status = cli_ports_status[port]
                logger.info(f'port: {port}, xid_port_status: {xiq_port_status}, device_port_status: {cli_port_status},'
                            f' xiq_port_status_mapped: {xiq_port_status_mapped}')

                logger.info("comparing cli - xiq port status")
                assert xiq_port_status_mapped == cli_port_status, \
                    f"for port: {port} found xiq_port_status: {xiq_port_status} " \
                    f"different than cli_port_status: {cli_port_status}"


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9566Tests:

    @pytest.fixture(scope="class", autouse=True)
    def setup(self, logger, network_manager, cli, node_1):
        try:
            network_manager.connect_to_network_element_name(node_1.name)
            onboarded_switch = node_1
            ports = sorted(
                cli.get_ports_from_dut(onboarded_switch),
                key=int if onboarded_switch.cli_type.upper() == "EXOS" else (lambda x: int(x.split("/")[1]))
            )
            try:
                cli.set_lldp(onboarded_switch, ports, action="disable")
                cli.bounce_IQAgent(onboarded_switch)
                yield
            finally:
                cli.set_lldp(onboarded_switch, ports, action="enable")
                cli.bounce_IQAgent(onboarded_switch)
        finally:
            cli.close_connection_with_error_handling(node_1)

    @pytest.mark.tcxm_9566
    def test_tcxm_9566(self, logger, node_1, utils, loaded_config, xiq_library_at_class_level, cli, request):
        xiq_ip_address = loaded_config['sw_connection_host']

        vlan_id = xiq_library_at_class_level.xflowsmanageDevice360.generate_vlan_id()
        policy_name = "APC_45707_policy_" + node_1.mac[:-3]

        utils.wait_till(
            lambda: xiq_library_at_class_level.xflowsglobalsettingsGlobalSetting.change_device_management_settings(
                option="disable"))
        xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()

        ports = sorted(
            cli.get_ports_from_dut(node_1),
            key=int if node_1.cli_type.upper() == "EXOS" else (lambda x: int(x.split("/")[1]))
        )[:4]

        assert xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
            policy_name=policy_name) == 1, f"Failed to create this network policy: {policy_name}"
        xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(policy_name, node_1.mac)


        def finalizer():
            try:
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                utils.wait_till(
                    lambda: xiq_library_at_class_level.xflowsmanageDevice360.go_to_device_360_port_config(
                        node_1))

                access_vlan_id = "1" if node_1.cli_type.upper() == "EXOS" else None
                port_type = "Access Port" if node_1.cli_type.upper() == "EXOS" else "Auto-sense Port"

                for port in ports:
                    xiq_library_at_class_level.xflowsmanageDevice360.enter_port_type_and_vlan_id(port=port,
                                                                                                 port_type=port_type,
                                                                                                 access_vlan_id=access_vlan_id,
                                                                                                 device_os=node_1.cli_type.upper())

            finally:
                utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.save_device_360_port_config, delay=2)
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

            xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(policy_name=policy_name,
                                                                                           serial=node_1.serial)

            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=node_1.serial))
            xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(node_1)
            cli.bounce_IQAgent(node_1, xiq_ip_address)

            try:
                xiq_library_at_class_level.xflowsconfigureNetworkPolicy.delete_network_policy(policy_name)
            except Exception as exc:
                logger.info(repr(exc))

        request.addfinalizer(finalizer)

        try:
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowsmanageDevice360.go_to_device_360_port_config(
                    node_1))

            for port in ports:
                xiq_library_at_class_level.xflowsmanageDevice360.enter_port_type_and_vlan_id(port=port,
                                                                                             port_type="Access Port",
                                                                                             access_vlan_id=vlan_id,
                                                                                             device_os=node_1.cli_type.upper())

        finally:
            utils.wait_till(xiq_library_at_class_level.xflowsmanageDevice360.save_device_360_port_config, delay=2)
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

        xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(policy_name, node_1.mac)
        xiq_library_at_class_level.xflowscommonDevices.update_network_policy_to_switch(policy_name=policy_name,
                                                                                       serial=node_1.serial)

        try:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))
            xiq_library_at_class_level.xflowsmanageDevice360.select_max_pagination_size()

            table_rows = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table()
            for row in table_rows:
                access_vlan = row["ACCESS VLAN"]
                if row["PORT NAME"] in ports:
                    if access_vlan == vlan_id:
                        logger.info(f'Port {row["PORT NAME"]} has assign VLAN ID {vlan_id}')
                    else:
                        pytest.fail(
                            f'Port {row["PORT NAME"]} does not have assigned the VLAN ID {vlan_id}.None was found!')

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9567Tests:

    @pytest.mark.tcxm_9567
    def test_tcxm_9567(self, udks, node_1, logger, xiq_library_at_class_level, config_helper, utils, auto_actions, cli):

        dut = node_1

        port_list = [dut.tgen.port_a.ifname, dut.tgen.port_b.ifname]
        first_port, second_port = port_list

        udks.setupTeardownUdks.Base_Test_Suite_Setup()

        cli.clear_counters(
            dut, first_port=first_port, second_port=second_port)
        cli.bounce_IQAgent(
            dut, connect_to_dut=False, disconnect_from_dut=False, wait=False)

        packet_a = 'packetA'
        packet_b = 'packetB'

        tgen_port_a = config_helper.createTgenPort(config_helper.tgen1_name, config_helper.tgen_dut1_port_a.ifname)
        tgen_port_b = config_helper.createTgenPort(config_helper.tgen1_name, config_helper.tgen_dut1_port_b.ifname)
        udks.trafficGenerationUdks.Create_Ethernet2_Packet(
            packet_a, '00:22:22:22:22:22', '00:11:11:11:11:11')
        udks.trafficGenerationUdks.Create_Ethernet2_Packet(
            packet_b, '00:11:11:11:11:11', '00:22:22:22:22:22')

        udks.trafficGenerationUdks.Transmit_Traffic_Bidirectionally(
            tgen_port_a, tgen_port_b, packet_a, packet_b, packet_b, packet_a, tx_count=5)
        try:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))

            checkboxes_button, _ = utils.wait_till(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button, delay=2)
            checkboxes_button.location_once_scrolled_into_view
            auto_actions.click(checkboxes_button)
            time.sleep(2)

            checkboxes = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_all_marked_checkboxes()
            time.sleep(3)

            logger.info("Checking if the Received Traffic checkbox is marked in the columns section")
            for i in checkboxes:
                if "Received" in i:
                    logger.info(f"The {i} checkbox is checked")
                    break
            else:
                assert False, "The received traffic checkbox is not checked"

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            time.sleep(3)

        cli.bounce_IQAgent(
            dut, connect_to_dut=False, disconnect_from_dut=False, wait=False)

        start_time = time.time()
        while time.time() - start_time < 1200:

            time.sleep(4)
            xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()
            time.sleep(4)

            try:
                traffic_list_from_dut = cli.get_received_traffic_list_from_dut(
                    dut, first_port, second_port)
                cli.bounce_IQAgent(
                    dut, connect_to_dut=False, disconnect_from_dut=False, wait=False)

                time.sleep(30)
                utils.wait_till(
                    lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))
                traffic_list_from_xiq = xiq_library_at_class_level.xflowsmanageDevice360.device360_display_traffic_received_from_xiq_and_return_traffic_list(
                    dut, first_port, second_port)

                for i in range(2):

                    match = re.search(r'(\d+(\.\d+)?)', traffic_list_from_xiq[i]).group(1)
                    if "KB" in traffic_list_from_xiq[i]:
                        traffic_list_from_xiq[i] = float(match) * 1024
                    elif "MB" in traffic_list_from_xiq[i]:
                        traffic_list_from_xiq[i] = float(match) * 1024 * 1024
                    else:
                        traffic_list_from_xiq[i] = float(match)

                logger.info("Traffic list from xiq is: ", traffic_list_from_xiq)
                logger.info("Traffic list from dut is: ", traffic_list_from_dut)

                for i in range(2):
                    a = float(traffic_list_from_dut[i])
                    b = float(traffic_list_from_xiq[i])

                    logger.info("Finding the difference in percentage between the traffic values")

                    try:
                        percentage_diff = ((b - a) / a) * 100
                    except ZeroDivisionError:
                        percentage_diff = 0

                    logger.info(f"the percentage for index {i} is {percentage_diff}")
                    assert abs(percentage_diff) <= 10, "The difference is more than 10%"
            except Exception as exc:
                logger.info(exc)
            else:
                break
            finally:
                xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
                time.sleep(10)
        else:
            assert False, f"Failed to verify values after {int(time.time() - start_time)} seconds"


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9568Tests:

    @pytest.mark.tcxm_9568
    def test_tcxm_9568(self, logger, udks, node_1, config_helper, utils, xiq_library_at_class_level, auto_actions, cli):

        dut = node_1

        port_list = [dut.tgen.port_a.ifname, dut.tgen.port_b.ifname]
        first_port, second_port = port_list

        udks.setupTeardownUdks.Base_Test_Suite_Setup()

        cli.clear_counters(
            dut, first_port=first_port, second_port=second_port)
        cli.bounce_IQAgent(
            dut, connect_to_dut=False, disconnect_from_dut=False, wait=False)

        packet_a = 'packetA'
        packet_b = 'packetB'

        tgen_port_a = config_helper.createTgenPort(config_helper.tgen1_name, config_helper.tgen_dut1_port_a.ifname)
        tgen_port_b = config_helper.createTgenPort(config_helper.tgen1_name, config_helper.tgen_dut1_port_b.ifname)
        udks.trafficGenerationUdks.Create_Ethernet2_Packet(
            packet_a, '00:22:22:22:22:22', '00:11:11:11:11:11')
        udks.trafficGenerationUdks.Create_Ethernet2_Packet(
            packet_b, '00:11:11:11:11:11', '00:22:22:22:22:22')

        udks.trafficGenerationUdks.Transmit_Traffic_Bidirectionally(
            tgen_port_a, tgen_port_b, packet_a, packet_b, packet_b, packet_a, tx_count=5)
        try:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))

            checkboxes_button, _ = utils.wait_till(
                xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button, delay=2)
            checkboxes_button.location_once_scrolled_into_view
            auto_actions.click(checkboxes_button)
            time.sleep(2)

            checkboxes = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_all_marked_checkboxes()
            time.sleep(3)

            logger.info("Checking if the Transmitted Traffic checkbox is marked in the columns section")
            for i in checkboxes:
                if "Transmitted" in i:
                    logger.info(f"The {i} checkbox is checked")
                    break
            else:
                assert False, "The transmitted traffic checkbox is not checked"

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

        cli.bounce_IQAgent(
            dut, connect_to_dut=False, disconnect_from_dut=False, wait=False)

        start_time = time.time()
        while time.time() - start_time < 1200:

            try:

                time.sleep(4)
                xiq_library_at_class_level.xflowscommonDevices.refresh_devices_page()
                time.sleep(4)

                traffic_list_from_dut = cli.get_transmitted_traffic_list_from_dut(
                    dut, first_port, second_port)
                cli.bounce_IQAgent(
                    dut, connect_to_dut=False, disconnect_from_dut=False, wait=False)

                time.sleep(30)
                utils.wait_till(
                    lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))
                traffic_list_from_xiq = xiq_library_at_class_level.xflowsmanageDevice360.device360_display_traffic_transmitted_from_xiq_and_return_traffic_list(
                    dut, first_port, second_port)

                for i in range(2):

                    match = re.search(
                        r'(\d+(\.\d+)?)', traffic_list_from_xiq[i]).group(1)
                    if "KB" in traffic_list_from_xiq[i]:
                        traffic_list_from_xiq[i] = float(match) * 1024
                    elif "MB" in traffic_list_from_xiq[i]:
                        traffic_list_from_xiq[i] = float(match) * 1024 * 1024
                    else:
                        traffic_list_from_xiq[i] = float(match)

                logger.info("Traffic list from xiq is: ", traffic_list_from_xiq)
                logger.info("Traffic list from dut is: ", traffic_list_from_dut)

                for i in range(2):
                    a = float(traffic_list_from_dut[i])
                    b = float(traffic_list_from_xiq[i])

                    logger.info("Finding the difference in percentage between the traffic values")

                    try:
                        percentage_diff = ((b - a) / a) * 100
                    except ZeroDivisionError:
                        percentage_diff = 0

                    logger.info(f"the percentage for index {i} is {percentage_diff}")
                    assert abs(percentage_diff) <= 10, "The difference is more than 10%"

            except Exception as exc:
                logger.info(exc)
            else:
                break
            finally:
                xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
                time.sleep(10)
        else:
            assert False, f"Failed to verify values after {int(time.time() - start_time)} seconds"


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9569Tests:

    @pytest.mark.tcxm_9569
    def test_9569_verify_power_usage_column(self, logger, enter_switch_cli, node_1, auto_actions, network_manager,
                                            utils, loaded_config, xiq_library_at_class_level, cli, request):

        column_name = "Power Used"

        try:
            logger.info("Collect the Power Usages values for all ports from CLI!")
            try:
                network_manager.connect_to_network_element_name(node_1.name)
                ports_power_cli = []

                if node_1.cli_type.upper() == "EXOS":

                    try:
                        with enter_switch_cli(node_1) as dev_cmd:
                            output = dev_cmd.send_cmd(node_1.name, "show inline-power info ports | begin 1",
                                                      max_wait=5, interval=2)[0].return_text
                            time.sleep(1)
                    except Exception as error:
                        logger.info(error)
                        pytest.skip("The device '{}' does not supported the PoE feature!".format(node_1.name))

                    output_lines = output.splitlines()
                    for line in output_lines:
                        if not (not line
                                or line.startswith("\x1bE")
                                or line.startswith("*")):
                            line = line.split()
                            port_power_value = [line[0], line[-2]]
                            ports_power_cli.append(port_power_value)
                            logger.info("Line CLI: ", port_power_value)

                elif node_1.cli_type.upper() == "VOSS":
                    with enter_switch_cli(node_1) as dev_cmd:
                        dev_cmd.send_cmd(node_1.name, "enable", max_wait=5, interval=2)
                        dev_cmd.send_cmd(node_1.name, "configure terminal", max_wait=5, interval=2)
                        output = dev_cmd.send_cmd(node_1.name, "show poe-power-measurement | begin 1",
                                                  max_wait=5, interval=2, ignore_cli_feedback=True)[0].return_text
                        time.sleep(1)
                        if "Device is not a POE device" in output:
                            logger.info(output)
                            pytest.skip("The device '{}' does not supported the PoE feature!".format(node_1.name))

                        output_lines = output.splitlines()
                        for line in output_lines:
                            if not (not line
                                    or line.startswith("\t")
                                    or line.startswith("-")
                                    or line.startswith("*")
                                    or line.endswith("#")):
                                if "does not support" in line:
                                    line = line.split()
                                    port_power_value = [line[1], "N/A"]
                                    logger.info("Line CLI: ", port_power_value)
                                else:
                                    line = line.split()
                                    port_power_value = [line[0], line[-1]]
                                    logger.info("Line CLI: ", port_power_value)
                                ports_power_cli.append(port_power_value)

            finally:
                cli.close_connection_with_error_handling(node_1)

            logger.info("Collect the Power Usages values for all ports from XIQ!")
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))
            xiq_library_at_class_level.xflowsmanageDevice360.select_max_pagination_size()

            checkbox_button = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button()

            auto_actions.click(checkbox_button)
            time.sleep(3)

            all_checkboxes = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
            columns_found_enabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is True]
            logger.info(f"These columns are currently found enabled: {columns_found_enabled}")

            if column_name in columns_found_enabled:
                logger.info(f"{column_name} column is already visible")
            else:
                logger.info(f"{column_name} column is not already visible; click on its checkbox")
                auto_actions.click(all_checkboxes[column_name]['element'])
                time.sleep(5)

            ports_power_xiq = []
            ports_table = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table()

            for entry in ports_table:
                assert column_name.upper() in entry, f"Failed to find {column_name} column in table row: {entry}"
                if not (entry['PORT NAME'] == "mgmt"):
                    power_value_port_xiq = entry[column_name.upper()].split()
                    line_xiq = [entry['PORT NAME'], power_value_port_xiq[0]]
                    ports_power_xiq.append(line_xiq)
                    logger.info("Line XIQ: ", line_xiq)

            logger.info("Compare the Power Usages values - XIQ vs CLI!")
            for result in xiq_library_at_class_level.xflowsmanageDevice360.check_power_values(ports_power_xiq,
                                                                                              ports_power_cli):
                if result[1] != "PASSED":
                    pytest.fail(
                        "For {}, the 'Power Usages' values from XIQ and CLI do NOT match "
                        "- Jira ticket XIQ-5903".format(result[0]))

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()


@pytest.mark.p1
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9570Tests:

    @pytest.mark.tcxm_9570
    def test_9570_check_speed_all_ports(self, logger, utils, network_manager, dev_cmd, xiq_library_at_class_level,
                                        auto_actions, cli, node_1):

        try:
            network_manager.connect_to_network_element_name(node_1.name)
            # retrieve the port speed values from the device
            device_ports_speed = cli.get_device_ports_speed(networkElementCliSend=dev_cmd,
                                                            dut=node_1)
        finally:
            cli.close_connection_with_error_handling(node_1)

        if device_ports_speed is None:
            pytest.fail('device_ports_speed is None')

        # get the list of the ports of the device
        match_port = device_ports_speed.keys()

        # retrieve the port speed values from XIQ
        logger.info("****************** Getting XIQ ports speed: ******************")
        try:

            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_1.mac))
            xiq_library_at_class_level.xflowsmanageDevice360.select_max_pagination_size()
            time.sleep(5)

            xiq_port_table_info = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table()

        finally:

            paginations = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes()
            if paginations:
                [pg_10] = [pg for pg in paginations if pg.text == "10"]
                auto_actions.click(pg_10)
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

        logger.info("****************** XIQ ports speed dictionary: ******************")
        logger.info(xiq_port_table_info)

        # device - XIQ speed values comparison
        logger.info("****************** Ports speed info ******************")
        for port in match_port:

            table_entry = [e for e in xiq_port_table_info if e['PORT NAME'] == port]
            if table_entry:
                table_entry = table_entry[0]
                # compare the values only if the port is shown in XIQ D360
                xiq_port_speed = table_entry["PORT SPEED"]
                device_port_speed = device_ports_speed[port]

                # remove the Mbps string from the XIQ D360 speed value
                if xiq_port_speed != "Auto":
                    xiq_port_speed = re.search(r'\d+', xiq_port_speed).group(0)

                logger.info(f'port: {port}, xid_port_speed: {xiq_port_speed}, device_port_speed: {device_port_speed}')

                if device_port_speed != xiq_port_speed:
                    if not (device_port_speed == "0" and xiq_port_speed == "Auto"):
                        pytest.fail('Device port speed "{}" and XIQ port speed "{}" differ'.format(
                            device_port_speed, xiq_port_speed))


@pytest.mark.p1
@pytest.mark.testbed_2_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9320Tests:

    @pytest.mark.tcxm_9320
    def test_9320_verify_LLDP_column_in_ports_table(self, xiq_library_at_class_level, logger, cli, utils, node_2,
                                                    node_1, netelem_listutils):

        dut1 = node_1
        dut2 = node_2

        isl_ports = netelem_listutils.create_list_of_netelem_isl_ports("netelem1")
        logger.info(f"isl_ports: {isl_ports}")

        if len(isl_ports) < 1:
            pytest.skip(
                "****This testcase doesn't run on single node testbed, it needs at least two nodes for execution. "
                "Hence skipping test****")

        logger.info("Wait for LLDP NEIGHBORS column to be updated before to start the test (bounce IQAgent)")
        cli.bounce_IQAgent(dut1)
        cli.bounce_IQAgent(dut2)
        time.sleep(5)

        try:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(dut1.mac))

            xiq_library_at_class_level.xflowsmanageDevice360.select_max_pagination_size()
            time.sleep(5)

            logger.info("Verify if LLDP NEIGHBOR column displays the sysname with hyperlink on all ports connected to "
                        "the onboarded neighbor device as configured in yaml file")
            xiq_library_at_class_level.xflowsmanageDevice360.check_device360_LLDP_neighbors_with_hyperlink(isl_ports)

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            time.sleep(5)

        try:
            logger.info("Delete the onboarded neighbor device from XIQ")
            xiq_library_at_class_level.xflowscommonDevices.delete_device(device_serial=dut2.serial)
            time.sleep(5)

            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(dut1.mac))
            xiq_library_at_class_level.xflowsmanageDevice360.select_max_pagination_size()

            logger.info(
                "Verify if LLDP NEIGHBOR column displays the sysname without hyperlink on all ports connected to "
                "the neighbor device as configured in yaml file")
            xiq_library_at_class_level.xflowsmanageDevice360.check_device360_LLDP_neighbors_without_hyperlink(isl_ports)

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()

            time.sleep(5)
            assert xiq_library_at_class_level.xflowscommonDevices.onboard_device_quick(dut2) == 1

            xiq_library_at_class_level.xflowscommonDevices.wait_until_device_online(dut2.serial)
            res = xiq_library_at_class_level.xflowscommonDevices.get_device_status(device_serial=dut2.serial)
            assert res == 'green', f"The device did not come up successfully in the XIQ; Device: {dut2}"


@pytest.mark.p1
@pytest.mark.testbed_2_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9321Tests:

    @pytest.mark.tcxm_9321
    def test_9321_verify_hyperlink_in_LLDP_column_takes_to_LLDP_neighbor(self, logger, utils, auto_actions, cli,
                                                                         xiq_library_at_class_level, netelem_listutils,
                                                                         node_1, node_2):

        dut1 = node_1
        dut2 = node_2

        isl_ports_dut1 = netelem_listutils.create_list_of_netelem_isl_ports("netelem1")
        isl_ports_dut2 = netelem_listutils.create_list_of_netelem_isl_ports("netelem2")

        if len(isl_ports_dut1) < 1:
            pytest.skip(
                "****This testcase doesn't run on single node testbed, it needs at least two nodes for execution. "
                "Hence skipping test****")

        if len(isl_ports_dut2) < 1:
            pytest.skip(
                "****This testcase doesn't run on single node testbed, it needs at least two nodes for execution. "
                "Hence skipping test****")

        logger.info("Wait for LLDP NEIGHBORS column to be updated before to start the test (bounce IQAgent)")
        cli.bounce_IQAgent(dut1)
        cli.bounce_IQAgent(dut2)

        utils.wait_till(lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(dut1.mac))

        try:
            xiq_library_at_class_level.xflowsmanageDevice360.select_max_pagination_size()

            logger.info("Verify if LLDP NEIGHBOR column displays the sysname with hyperlink on all ports connected to "
                        "the onboarded neighbor device as configured in yaml file and click it")
            time.sleep(5)
            hyperlinks_list_dut1 = xiq_library_at_class_level.xflowsmanageDevice360.check_device360_LLDP_neighbors_with_hyperlink(
                isl_ports_dut1, hyperlinks=True)
            print(f"hyperlinks_list_dut1:{hyperlinks_list_dut1}")
            for i in range(len(hyperlinks_list_dut1)):
                time.sleep(15)
                hyperlinks_list_dut1 = xiq_library_at_class_level.xflowsmanageDevice360.check_device360_LLDP_neighbors_with_hyperlink(
                    isl_ports_dut1, hyperlinks=True)
                print(f"hyperlinks_list_dut1:{hyperlinks_list_dut1}")
                hyper_dut1 = hyperlinks_list_dut1[i]

                auto_actions.click(hyper_dut1)
                time.sleep(15)

                mac_device360 = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device_info_mac_address()
                assert "MAC Address:\n" + dut2.mac.upper() == mac_device360.text, "The mac in device360 is not the same as in the yaml file!"
                logger.info(f"The displayed LLDP neighbor is correct and has the mac: {dut2.mac.upper()}")

                hyperlinks_list_dut2 = xiq_library_at_class_level.xflowsmanageDevice360.check_device360_LLDP_neighbors_with_hyperlink(
                    isl_ports_dut2, hyperlinks=True)
                print(f"hyperlinks_list_dut2:{hyperlinks_list_dut2}")
                time.sleep(15)

                auto_actions.click(hyperlinks_list_dut2[i])
                time.sleep(15)

                mac_device360 = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_device_info_mac_address()
                assert "MAC Address:\n" + dut1.mac.upper() == mac_device360.text, "The mac in device360 is not the same as in the yaml file!"

                logger.info(f"The displayed LLDP neighbor is correct and has the mac: {dut1.mac.upper()}")

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.select_pagination_size("10")
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()


@pytest.mark.p2
@pytest.mark.testbed_2_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9323Tests:

    @pytest.mark.tcxm_9323
    def test_9323_check_lldp_neighbour_hyperlink_and_value(self, netelem_listutils, client_web_elements, xiq_library_at_class_level,
                                                           auto_actions, cli, utils, logger, node_1, node_2):

        dut1 = node_1
        dut2 = node_2

        ports_isl = []
        ports = netelem_listutils.create_list_of_netelem_isl_ports("netelem1")
        logger.info('Ports = {} for dut = {}'.format(ports, dut1.name))
        contains = True
        for old_port in ports:
            if old_port is not None:
                if old_port.find('/') != -1:
                    parts = old_port.split("/")
                    ports_isl.append(parts[1])
                    contains = True
                else:
                    contains = False
        if not contains:
            ports_isl = ports
        ports_isl = list(map(int, ports_isl))
        logger.info('ISL ports = {} for dut = {}'.format(ports_isl, dut1.name))

        start_time = time.time()
        cli.bounce_IQAgent(dut1)
        cli.bounce_IQAgent(dut2)

        while time.time() - start_time < 600:
            try:
                logger.info('Refresh page')
                auto_actions.click(client_web_elements.get_client_page_refresh_button())
                time.sleep(5)

                logger.info('Go to 360 page of dut = {}'.format(dut1.name))
                utils.wait_till(
                    lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(dut1.mac))

                real_ports = xiq_library_at_class_level.xflowsmanageDevice360.dev360.get_ports_from_device360_up()
                logger.info("REAL PORTS =  {}".format(real_ports))
                time.sleep(10)

                success = xiq_library_at_class_level.xflowsmanageDevice360.check_lld_neighbour_field_with_value_and_with_hyperlink(
                    ports_isl, real_ports, logger)

                assert success == 1

            except Exception as exc:

                logger.error("Test is a failure and LLDP neighbours does not exist with Hyperlinks")
                logger.error(repr(exc))
                time.sleep(30)

            else:

                logger.info("Test is a success and LLDP neighbours exist with Hyperlinks")
                break

            finally:

                xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
        else:
            pytest.fail("Test is a failure and LLDP neighbours does not exist with Hyperlinks")


@pytest.mark.p2
@pytest.mark.testbed_2_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9564Tests:

    @pytest.mark.tcxm_9564
    def test_9564_lacp_status(self, xiq_library_at_class_level, cli, utils, logger, node_1, node_2):

        dut1 = node_1
        dut2 = node_2
        port_device_1 = dut1.isl.port_a.ifname
        port_device_2 = dut2.isl.port_a.ifname
        mlt = 70
        key = 7

        cli.bounce_IQAgent(dut1)
        cli.bounce_IQAgent(dut2)

        utils.wait_till(lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(dut1.mac))
        xiq_library_at_class_level.xflowsmanageDevice360.verify_lacp_status_for_port_device_in_360_table(logger, dut1,
                                                                                                         port_device_1,
                                                                                                         'false')

        try:

            logger.info(f"Modify lacp for device 1 port {port_device_1}")
            cli.set_lacp(dut1, mlt, key, port_device_1)
            time.sleep(2)

            logger.info(f"Modify lacp for device 2 port {port_device_2}")
            cli.set_lacp(dut2, mlt, key, port_device_2)
            time.sleep(20)

            logger.info("Bounce device 2")
            cli.bounce_IQAgent(dut2)

            logger.info("Bounce device 1")
            cli.bounce_IQAgent(dut1)
            time.sleep(5)

            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(dut1.mac))
            if node_1.cli_type.upper() == "EXOS":
                xiq_library_at_class_level.xflowsmanageDevice360.verify_lacp_status_for_port_device_in_360_table(logger,
                                                                                                             dut1,
                                                                                                             port_device_1,
                                                                                                             'LACP')
            if node_1.cli_type.upper() == "VOSS":
                xiq_library_at_class_level.xflowsmanageDevice360.verify_lacp_status_for_port_device_in_360_table(logger,
                                                                                                             dut1,
                                                                                                             port_device_1,
                                                                                                             'true')
        finally:

            logger.info("Cleanup")
            cli.cleanup_lacp(dut1, mlt, port_device_1)
            time.sleep(3)
            cli.cleanup_lacp(dut2, mlt, port_device_2)


@pytest.mark.p1
@pytest.mark.testbed_stack
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9329Tests:

    @pytest.mark.tcxm_9329
    def test_9329_verify_default_port_details(self, utils, enter_switch_cli, network_manager, cli,
                                              xiq_library_at_class_level, node_stack):

        try:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_stack.mac))
            xiq_library_at_class_level.Cli.close_connection_with_error_handling(node_stack)
            xiq_library_at_class_level.xflowsmanageDevice360.verify_port_names()

            try:
                network_manager.connect_to_network_element_name(node_stack.name)
                master_slot = cli.get_master_slot(node_stack)
                with enter_switch_cli(node_stack) as dev_cmd:
                    dev_cmd.send_cmd(node_stack.name, 'reboot slot ' + str(master_slot), max_wait=10, interval=2,
                                     confirmation_phrases='(y - save and reboot, n - reboot without save, <cr> - cancel command)',
                                     confirmation_args='y')
            finally:
                xiq_library_at_class_level.Cli.close_connection_with_error_handling(node_stack)

            time.sleep(10)
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
            time.sleep(5)

            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_stack.mac))
            xiq_library_at_class_level.xflowsmanageDevice360.verify_port_names()

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()


@pytest.mark.p1
@pytest.mark.testbed_stack
@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM9330Tests:

    @pytest.mark.tcxm_9330
    def test_9330_verify_other_slot_ports_displayed(self, xiq_library_at_class_level, cli, utils, network_manager,
                                                    node_stack):

        current_page_number = 1

        try:
            utils.wait_till(
                lambda: xiq_library_at_class_level.xflowscommonDeviceCommon.go_to_device360_window(node_stack.mac))

            try:
                network_manager.connect_to_network_element_name(node_stack.name)
                dut_list_of_ports = cli.get_port_list_from_dut_without_not_present_ports(node_stack)
            finally:
                xiq_library_at_class_level.Cli.close_connection_with_error_handling(node_stack)

            more_pages = 1

            while more_pages == 1:
                xiq_library_at_class_level.xflowsmanageDevice360.device360_confirm_current_page_number(
                    current_page_number)

                table_list_of_ports = xiq_library_at_class_level.xflowsmanageDevice360.device360_switch_get_current_page_port_name_list()
                for port in table_list_of_ports:
                    if port in dut_list_of_ports:
                        dut_list_of_ports.remove(port)
                more_pages = xiq_library_at_class_level.xflowsmanageDevice360.device360_monitor_overview_pagination_next_page_by_number()
                current_page_number = current_page_number + 1
            assert len(dut_list_of_ports) == 0, f"Some ports wre not displayed in the table"

        finally:
            xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
import time

from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from extauto.common.AutoActions import AutoActions
from extauto.xiq.elements.Device360WebElements import Device360WebElements
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementLacpGenKeywords import \
    NetworkElementLacpGenKeywords
from ExtremeAutomation.Keywords.NetworkElementKeywords.GeneratedKeywords.NetworkElementMltGenKeywords import \
    NetworkElementMltGenKeywords


class SuiteUdk:
    
    def __init__(self, setup_cls_obj):
        self.defaultLibrary = DefaultLibrary()
        self.setup_cls_obj = setup_cls_obj
        self.auto_actions = AutoActions()
        self.xiq = setup_cls_obj.xiq
        self.networkElementLacpGenKeywords = NetworkElementLacpGenKeywords()
        self.networkElementMltGenKeywords = NetworkElementMltGenKeywords()

    def list_port_element(self, xiq, port_no, netelem_name):
        # rows = xiq.xflowscommonDevices.devices_web_elements.get_port_info(netelem_name, slot_number)
        rows = xiq.DeviceDiscoveryKeywords.get_port_info(netelem_name, slot_number=port_no)
        matchers = ['LLDP Neighbor']
        if rows:
            xiq.xflowscommonDevices.utils.print_debug(f"Searching {len(rows)} rows")
            for row in rows:
                xiq.xflowscommonDevices.utils.print_info(f"Port {port_no} details: ",
                                                         xiq.xflowscommonDevices.format_row(row.text))
                for i in matchers:
                    test = any(i in string for string in xiq.xflowscommonDevices.format_row(row.text))
                    if test == False:
                        return -1
            return 1
        else:
            return -1

    def get_isl_ports(self, port_dict):
        ports = []
        for port_key in port_dict.keys():
            port = port_dict[port_key]
            if port and 'ifname' in port and port is not None:
                ports.append(port['ifname'])
        return ports

    def create_ports_list(self, port_dict):
        ports_isl = []
        ports = self.get_isl_ports(port_dict)
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
        return ports_isl

    def check_lld_neighbour_field_with_value_and_with_hyperlink(self, ports_isl, real_ports, logger):
        lldp_neighbour = {}
        success = 1
        for port in ports_isl:
            logger.info("PORT =  {}".format(port))
            try:
                self.auto_actions.click(real_ports[port - 1])
                elem = Device360WebElements().get_ports_from_device360_up_lldp_neighbour()
                if not elem:
                    elem = Device360WebElements().weh.get_element(
                        {"XPATH": '//div[contains(@class, "port-info port-lldp-neighbor")]'})
                lldp_neighbour[port] = elem
                logger.info("lldp_neighbour =  {}".format(lldp_neighbour[port].text))
                lldp_hyper_link = Device360WebElements().get_cell_href(lldp_neighbour[port])
                logger.info("lldp_neighbour href =  {}".format(lldp_hyper_link is not None))
                str1 = lldp_neighbour[port].text
                splits = str1.split()
                for split in splits:
                    logger.info("SPLIT = {}".format(split))
                if (lldp_neighbour[port].text is not None and lldp_neighbour[port].text != "" and len(
                        splits) > 2) and lldp_hyper_link is not None:
                    success = 1
                else:
                    success = 0
                    break
                time.sleep(5)
            except IndexError:
                logger.error("PORT =  {} does not exists".format(port))
        return success

    def check_lld_neighbour_field_with_value_and_without_hyperlink(self, ports_isl, real_ports, logger):
        lldp_neighbour = {}
        success = 1
        for port in ports_isl:
            logger.info("PORT =  {}".format(port))
            try:
                self.auto_actions.click(real_ports[port - 1])
                elem = Device360WebElements().get_ports_from_device360_up_lldp_neighbour()
                if not elem:
                    elem = Device360WebElements().weh.get_element(
                        {"XPATH": '//div[contains(@class, "port-info port-lldp-neighbor")]'})
                lldp_neighbour[port] = elem
                logger.info("lldp_neighbour =  {}".format(lldp_neighbour[port].text))
                lldp_hyper_link = Device360WebElements().get_cell_href(lldp_neighbour[port])
                logger.info("lldp_neighbour href =  {}".format(lldp_hyper_link is not None))
                str1 = lldp_neighbour[port].text
                splits = str1.split()
                for split in splits:
                    logger.info("SPLIT = {}".format(split))
                if (lldp_neighbour[port].text is not None and lldp_neighbour[port].text != "" and len(splits) > 2) and (
                        lldp_hyper_link is None or lldp_hyper_link is False):
                    success = 1
                else:
                    success = 0
                    break
                time.sleep(5)
            except IndexError:
                logger.error("PORT =  {} does not exists".format(port))
        return success

    def check_lld_neighbour_field_without_value_and_without_hyperlink(self, ports_isl, real_ports, logger):
        lldp_neighbour = {}
        success = 1
        for port in ports_isl:
            logger.info("PORT =  {}".format(port))
            try:
                self.auto_actions.click(real_ports[port - 1])
                elem = Device360WebElements().get_ports_from_device360_up_lldp_neighbour()
                if not elem:
                    elem = Device360WebElements().weh.get_element(
                        {"XPATH": '//div[contains(@class, "port-info port-lldp-neighbor")]'})
                lldp_neighbour[port] = elem
                logger.info("lldp_neighbour =  {}".format(lldp_neighbour[port].text))
                lldp_hyper_link = Device360WebElements().get_cell_href(lldp_neighbour[port])
                logger.info("lldp_neighbour href =  {}".format(lldp_hyper_link is None))
                str1 = lldp_neighbour[port].text
                splits = str1.split()
                for split in splits:
                    logger.info("SPLIT = {}".format(split))
                if (lldp_neighbour[port].text is None or lldp_neighbour[port].text == "") or len(splits) <= 2:
                    success = 1
                else:
                    success = 0
                    break
                time.sleep(5)
            except IndexError:
                logger.error("PORT =  {} does not exists".format(port))
        return success

    def go_to_device360(self, dut):
        time.sleep(5)
        self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
        time.sleep(5)

    def bounce_device(self, xiq, dut):
        try:
            self.close_connection_with_error_handling(dut)
            self.setup_cls_obj.network_manager.connect_to_network_element_name(dut.name)

            if dut.cli_type.upper() == "EXOS":
                self.setup_cls_obj.devCmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2,
                                                confirmation_phrases='Do you want to continue?', confirmation_args='Yes')
                self.setup_cls_obj.devCmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)
            elif dut.cli_type.upper() == "VOSS":
                self.setup_cls_obj.devCmd.send_cmd(dut.name, 'enable', max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, 'configure terminal', max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, 'application', max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, 'no iqagent enable', max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, 'iqagent enable', max_wait=10, interval=2)

            xiq.xflowscommonDevices.wait_until_device_online(device_mac=dut.mac)
        finally:
            self.close_connection_with_error_handling(dut)

    def set_lacp(self, dut, mlt, key, port):
        try:
            self.close_connection_with_error_handling(dut)
            self.setup_cls_obj.network_manager.connect_to_network_element_name(dut.name)

            if dut.cli_type.upper() == "EXOS":
                self.networkElementLacpGenKeywords.lacp_create_lag(dut.name, f"{port}", f"{port}-{port}", '')
            elif dut.cli_type.upper() == "VOSS":
                self.networkElementMltGenKeywords.mlt_create_id(dut.name, mlt)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, 'enable', max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, 'configure terminal', max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, f"interface gigabitEthernet {port}", max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, "no auto-sense enable", max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, "exit", max_wait=10, interval=2)
                self.networkElementLacpGenKeywords.lacp_create_lag(dut.name, f"gigabitEthernet {port}", port,
                                                                                key)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, 'configure terminal', max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, f"interface mlt {mlt}", max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, f"lacp key {key}", max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, "lacp enable", max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, "exit", max_wait=10, interval=2)
                self.networkElementLacpGenKeywords.lacp_enable_global(dut.name)
        finally:
            self.close_connection_with_error_handling(dut)

    def cleanup_lacp(self, dut, mlt, port):
        self.close_connection_with_error_handling(dut)
        self.setup_cls_obj.network_manager.connect_to_network_element_name(dut.name)

        if dut.cli_type.upper() == "EXOS":
            self.networkElementLacpGenKeywords.lacp_delete_lag(dut.name, port, '', '')
        elif dut.cli_type.upper() == "VOSS":
            self.networkElementLacpGenKeywords.lacp_delete_lag(dut.name, f"gigabitEthernet {port}", '',
                                                                             port)
            self.setup_cls_obj.devCmd.send_cmd(dut.name, 'enable', max_wait=10, interval=2)
            self.setup_cls_obj.devCmd.send_cmd(dut.name, 'configure terminal', max_wait=10, interval=2)
            self.setup_cls_obj.devCmd.send_cmd(dut.name, f"interface gigabitEthernet {port}", max_wait=10, interval=2)
            self.setup_cls_obj.devCmd.send_cmd(dut.name, "no lacp enable", max_wait=10, interval=2)
            self.setup_cls_obj.devCmd.send_cmd(dut.name, "default lacp key", max_wait=10, interval=2)
            self.setup_cls_obj.devCmd.send_cmd(dut.name, "auto-sense enable", max_wait=10, interval=2)
            self.setup_cls_obj.devCmd.send_cmd(dut.name, "exit", max_wait=10, interval=2)
            self.networkElementMltGenKeywords.mlt_delete_id(dut.name, mlt)

        self.close_connection_with_error_handling(dut)

    def verify_lacp_status_for_port_device_in_360_table(self, xiq, dut1, logger, port, check_value):
        
        try:
            
            self.go_to_device360(dut1)
            
            self.select_max_pagination_size()
            
            logger.info("Select LACP Status column if is not selected in column picker")
            checkbox_button = xiq.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button()
            checkbox_button.location_once_scrolled_into_view
            
            try:
                self.auto_actions.click(checkbox_button)

                time.sleep(2)
                all_checkboxes = xiq.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
                default_disabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is False]

                for checkbox_name, stats in all_checkboxes.items():
                    if checkbox_name.upper() == "LACP STATUS" and checkbox_name in default_disabled \
                            and stats["is_selected"] is False:
                        self.auto_actions.click(stats["element"])
                        break
            finally:                    
                # Close column picker
                self.auto_actions.click(checkbox_button)
                time.sleep(2)

            ports_table = xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()
            [port_row] = [row for row in ports_table if row["PORT NAME"] == port]
            lacp_status = port_row["LACP STATUS"]
            logger.info(f"LACP status = {lacp_status}")

            assert lacp_status == check_value, f"Default LACP Status for port: {port} is not {check_value}"

        finally:
            
            logger.info("Select LACP Status column if is not selected in column picker")
            checkbox_button = xiq.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button()
            if checkbox_button:
                checkbox_button.location_once_scrolled_into_view
                
                try:
                    self.auto_actions.click(checkbox_button)
                    time.sleep(2)
                    
                    all_checkboxes = xiq.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()

                    for checkbox_name, stats in all_checkboxes.items():
                        if checkbox_name.upper() == "LACP STATUS" and stats["is_selected"] is True:
                            self.auto_actions.click(stats["element"])
                            break
                finally:                    
                    # Close column picker
                    self.auto_actions.click(checkbox_button)
                    time.sleep(2)
            
            self.select_pagination_size("10")
            xiq.xflowsmanageDevice360.close_device360_window()

    def check_device360_LLDP_neighbors_with_hyperlink(self, isl_ports):

        header_row = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_description_table_row()
        ths = self.xiq.xflowsmanageDevice360.dev360.weh.get_elements(
            self.xiq.xflowsmanageDevice360.dev360.device360_ports_table_th_columns, parent=header_row)

        table_rows = self.get_device360_port_table_rows()

        is_hyperlink = 0
        for row in table_rows:
            tds = self.xiq.xflowsmanageDevice360.dev360.weh.get_elements(
                self.xiq.xflowsmanageDevice360.dev360.device360_ports_table_td_gridcell, parent=row)
            for th, td in zip(ths, tds):
                if th.text.strip() == "PORT NAME":
                    port_found = 0
                    for port in isl_ports:
                        if td.text.strip() == port:
                            port_found = 1
                            print(f"Port found: {td.text.strip()}")
                            break
                elif th.text.strip() == "LLDP NEIGHBOR":
                    if port_found == 1:
                        print(self.xiq.xflowsmanageDevice360.dev360.get_cell_href(td))
                        if self.xiq.xflowsmanageDevice360.dev360.get_cell_href(td) != None:
                            is_hyperlink = is_hyperlink + 1
                            print(f"LLDP column displays the sysname, {td.text.strip()} with hyperlink for port {port}")
                        else:
                            print(
                                f"LLDP column displays the sysname, {td.text.strip()} without hyperlink for port {port}")
                    break

        assert is_hyperlink == len(
            isl_ports), "LLDP column displays the sysname without hyperlink for at least one port"

    def check_device360_LLDP_neighbors_without_hyperlink(self, isl_ports):

        header_row = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_description_table_row()
        ths = self.xiq.xflowsmanageDevice360.dev360.weh.get_elements(
            self.xiq.xflowsmanageDevice360.dev360.device360_ports_table_th_columns, parent=header_row)

        table_rows = self.get_device360_port_table_rows()

        no_hyperlink = 0
        for row in table_rows:
            tds = self.xiq.xflowsmanageDevice360.dev360.weh.get_elements(
                self.xiq.xflowsmanageDevice360.dev360.device360_ports_table_td_gridcell, parent=row)
            for th, td in zip(ths, tds):
                if th.text.strip() == "PORT NAME":
                    port_found = 0
                    for port in isl_ports:
                        if td.text.strip() == port:
                            port_found = 1
                            print(f"Port found: {td.text.strip()}")
                            break
                elif th.text.strip() == "LLDP NEIGHBOR":
                    if port_found == 1:
                        if self.xiq.xflowsmanageDevice360.dev360.get_cell_href(td) != None:
                            print(
                                f"LLDP column displays the sysname, {td.text.strip()} with hyperlink for port {port}")
                        else:
                            if td.text.strip() != "":
                                no_hyperlink = no_hyperlink + 1
                            print(
                                f"LLDP column displays the sysname, {td.text.strip()} without hyperlink for port {port}")
                    break

        assert no_hyperlink == len(
            isl_ports), "LLDP column displays the sysname with hyperlink/sysname missing for at least one port"

    def check_device360_LLDP_neighbors_with_hyperlink_dut1(self, isl_ports_dut1):
    
        header_row = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_description_table_row()
        ths = self.xiq.xflowsmanageDevice360.dev360.weh.get_elements(
            self.xiq.xflowsmanageDevice360.dev360.device360_ports_table_th_columns, parent=header_row)

        table_rows = self.get_device360_port_table_rows()

        is_hyperlink = 0
        hyperlinks_dut1 = []
        for row in table_rows:
            tds = self.xiq.xflowsmanageDevice360.dev360.weh.get_elements(
                self.xiq.xflowsmanageDevice360.dev360.device360_ports_table_td_gridcell, parent=row)
            for th, td in zip(ths, tds):
                if th.text.strip() == "PORT NAME":
                    port_found = 0
                    for port in isl_ports_dut1:
                        if td.text.strip() == port:
                            port_found = 1
                            print(f"Port found: {td.text.strip()}")
                            break
                elif th.text.strip() == "LLDP NEIGHBOR":
                    if port_found == 1:
                        if self.xiq.xflowsmanageDevice360.dev360.get_cell_href(td) != None:
                            hyperlink_dut1 = self.xiq.xflowsmanageDevice360.dev360.get_cell_href(td)
                            hyperlinks_dut1.append(hyperlink_dut1)
                            is_hyperlink = is_hyperlink + 1
                            print(f"LLDP column displays the sysname, {td.text.strip()} with hyperlink for port {port}")
                        else:
                            print(
                                f"LLDP column displays the sysname, {td.text.strip()} without hyperlink for port {port}")
                    break

        assert is_hyperlink == len(
            isl_ports_dut1), "LLDP column displays the sysname without hyperlink for at least one port"

        return hyperlinks_dut1

    def check_device360_LLDP_neighbors_with_hyperlink_dut2(self, isl_ports_dut2):
    
        header_row = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_description_table_row()
        ths = self.xiq.xflowsmanageDevice360.dev360.weh.get_elements(
            self.xiq.xflowsmanageDevice360.dev360.device360_ports_table_th_columns, parent=header_row)

        table_rows = self.get_device360_port_table_rows()

        is_hyperlink = 0
        hyperlinks_dut2 = []
        for row in table_rows:
            tds = self.xiq.xflowsmanageDevice360.dev360.weh.get_elements(
                self.xiq.xflowsmanageDevice360.dev360.device360_ports_table_td_gridcell, parent=row)
            for th, td in zip(ths, tds):
                if th.text.strip() == "PORT NAME":
                    port_found = 0
                    for port in isl_ports_dut2:
                        if td.text.strip() == port:
                            port_found = 1
                            print(f"Port found: {td.text.strip()}")
                            break
                elif th.text.strip() == "LLDP NEIGHBOR":
                    if port_found == 1:
                        if self.xiq.xflowsmanageDevice360.dev360.get_cell_href(td) != None:
                            hyperlink_dut2 = self.xiq.xflowsmanageDevice360.dev360.get_cell_href(td)
                            hyperlinks_dut2.append(hyperlink_dut2)
                            is_hyperlink = is_hyperlink + 1
                            print(f"LLDP column displays the sysname, {td.text.strip()} with hyperlink for port {port}")
                        else:
                            print(
                                f"LLDP column displays the sysname, {td.text.strip()} without hyperlink for port {port}")
                    break

        assert is_hyperlink == len(
            isl_ports_dut2), "LLDP column displays the sysname without hyperlink for at least one port"

        # self.auto_actions.click(hyperlinks_dut2[0])
        return hyperlinks_dut2

    def close_connection_with_error_handling(self, dut):
        try:
            
            try:
                if dut.cli_type.upper() == "VOSS":
                    for session_id in range(7):
                        self.setup_cls_obj.devCmd.send_cmd(dut.name, f"clear ssh {session_id}")
                elif dut.cli_type.upper() == "EXOS":
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, "clear session all")
            except Exception as err:
                print(err)
                
            self.setup_cls_obj.network_manager.device_collection.remove_device(dut.name)
            self.setup_cls_obj.network_manager.close_connection_to_network_element(dut.name)
            
        except Exception as exc:
            print(exc)
        else:
            time.sleep(30)

    def do_onboarding(self, dut, location='Salem,Northeastern,Groundfloor',
                      delete_if_already_onboarded=True, configure_iqagent=False, wait_for_green_status=False):

        try:
            xiq_ip_address = self.setup_cls_obj.cfg['sw_connection_host']
            self.close_connection_with_error_handling(dut)
            
            self.setup_cls_obj.network_manager.connect_to_network_element_name(dut.name)

            if delete_if_already_onboarded:
                self.xiq.xflowscommonDevices._goto_devices()
                self.xiq.xflowscommonDevices.delete_device(device_serial=dut.serial)

            assert self.xiq.xflowsmanageSwitch.onboard_switch(
                dut.serial, device_os=dut.cli_type, location=location) == 1, f"Failed to onboard this dut to XiQ: {dut}"

            if configure_iqagent:

                if dut.cli_type.upper() == "EXOS":

                    self.setup_cls_obj.devCmd.send_cmd_verify_output(dut.name, 'show process iqagent', 'Ready', max_wait=30, interval=10)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2,
                                        confirmation_phrases='Do you want to continue?', confirmation_args='y')
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'configure iqagent server ipaddress none', max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'configure iqagent server ipaddress ' + xiq_ip_address,
                                        max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)

                elif dut.cli_type.upper() == "VOSS":

                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'configure terminal', max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'application', max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'no iqagent enable', max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'iqagent server ' + xiq_ip_address,
                                        max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'iqagent enable', max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd_verify_output(dut.name, 'show application iqagent', 'true', max_wait=30,
                                            interval=10)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'exit', max_wait=10, interval=2)

                time.sleep(10)

            if wait_for_green_status:
                self.xiq.xflowscommonDevices.wait_until_device_online(dut.serial)
                res = self.xiq.xflowscommonDevices.get_device_status(device_serial=dut.serial)
                assert res == 'green', f"The EXOS device did not come up successfully in the XIQ; Device: {dut}"

        finally:
            self.close_connection_with_error_handling(dut)

    def get_device360_port_table_rows(self):
        table_rows = self.xiq.xflowsmanageDevice360.dev360.get_device360_port_table_rows()
        assert table_rows, "Did not find the rows of the ports table"
        table_rows[0].location_once_scrolled_into_view
        return [
            row for row in table_rows if not 
            any(field in row.text for field in ["PORT NAME", "LLDP NEIGHBOR", "PORT STATUS"])
        ]

    def select_max_pagination_size(self):
        try:
            time.sleep(2)
            pagination_size = max(self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes(),
                                key=lambda x: int(x.text))
            pagination_size.location_once_scrolled_into_view
            self.auto_actions.click(pagination_size)
            print(f"Selected the max pagination size: {pagination_size.text}")
            time.sleep(5)
            return 1
        except Exception as exc:
            print(repr(exc))
            return -1

    def select_pagination_size(self, int_size):
        try:
            time.sleep(2)
            paginations = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes()
            [pg_size] = [pg for pg in paginations if pg.text == int_size]
            self.auto_actions.click(pg_size)
            time.sleep(5)
            return 1
        except Exception as exc:
            print(repr(exc))
            return -1

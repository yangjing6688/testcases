import time
import re
import pytest

from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary


class SuiteUdk:
    
    def __init__(self, pytestConfigHelper, xiqLib, devCmd):

        self.defaultLibrary = DefaultLibrary()
        self.tb = pytestConfigHelper
        self.xiq = xiqLib
        self.devCmd = devCmd

    def device360_switch_get_current_page_port_name_list(self):
        """
         - This keyword will get a list with all the port names from the current page (Monitoring->Overview)
         - Flow: Click next page number
         It Assumes That Already Navigated to Device360 Page (Monitoring->Overview)
         - Keyword Usage:
         - ``Device360 Monitor Overview Pagination Next Page By Number``
        :return: port_name_list if successfully extracted the port names
        :return: -1 if error
        """
        try:
            port_name_list = []
            rows = self.xiq.xflowsmanageDevice360.get_d360_switch_ports_table_grid_rows()
            for row in rows:
                port_name_list.append(self.xiq.xflowsmanageDevice360.get_d360_switch_ports_table_interface_port_name_cell(row).text)
            if 'PORT NAME' in port_name_list:
                port_name_list.remove('PORT NAME')
            pattern_voss_three_nums = re.compile(r'\d+\/\d+\/\d+', re.M)
            filtered = [i for i in port_name_list if not pattern_voss_three_nums.match(i)]
            pattern_mgmt = re.compile(r'.*mgmt.*', re.M)
            filtered = [i for i in filtered if not pattern_mgmt.match(i)]
            return filtered
        except Exception as e:
            return -1

    def device360_monitor_overview_pagination_next_page_by_number(self):
        """
         - This keyword will navigate to the next page of the Monitoring Overview Ports Table, using the
         page number button
         - Flow: Click next page number
         It Assumes That Already Navigated to Device360 Page
         - Keyword Usage:
         - ``Device360 Monitor Overview Pagination Next Page By Number``
        :return: 1 if successfully changed to next page
        :return: 2 if already on the last page
        :return: -1 if error
        """
        try:
            current_page = int(self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_current_pagin_number().text)
            other_pages = self.xiq.xflowsmanageDevice360.dev360.get_device360_pagination_page_buttons()
            for page in other_pages:
                if int(page.text) == current_page + 1:
                    self.xiq.xflowsmanageDevice360.utils.print_info(f"Going to page " + str(current_page + 1))
                    self.xiq.xflowsmanageDevice360.auto_actions.click(page)
                    time.sleep(5)
                    return 1
            return 2
        except Exception as e:
            return -1

    def device360_confirm_current_page_number(self, page_num_ref):
        """
         - This keyword will check if the page with page_num_ref number is currently displayed
         It Assumes That Already Navigated to Device360 Page (Monitoring->Overview)
         - Keyword Usage:
         - ``Device360 Monitor Overview Pagination Next Page By Number``
        :return: True if page number matches
        :return: False if page number doesn't match or on error
        """
        try:
            current_page = int(self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_current_pagin_number().text)
            if current_page == page_num_ref:
                return True
            return False
        except Exception as e:
            return False

    def get_port_list_from_dut(self, dut):

        if dut.cli_type.upper() == "VOSS":
            
            time.sleep(10)
            self.devCmd.send_cmd(dut.name, 'enable',
                                max_wait=10, interval=2)
            output = self.devCmd.send_cmd(dut.name, 'show int gig int | no-more',
                                max_wait=10, interval=2)
            p = re.compile(r'^\d+\/\d+\/?\d*', re.M)
            match_port = re.findall(p, output[0].return_text)
            print(f"{match_port}")

            #remove elements with two /
            p2 = re.compile(r'\d+\/\d+\/\d+', re.M)
            filtered = [port for port in match_port if not p2.match(port)]
            return filtered
    
        elif dut.cli_type.upper() == "EXOS":
            
            time.sleep(10)
            self.devCmd.send_cmd(dut.name, 'disable cli paging',
                                max_wait=10, interval=2)
            output = self.devCmd.send_cmd(dut.name, 'show ports info',
                                max_wait=10, interval=2)
            p = re.compile(r'^\d+:\d+', re.M)
            match_port = re.findall(p, output[0].return_text)
            is_stack = True
            
            if len(match_port) == 0:
                is_stack = False
                p = re.compile(r'^\d+', re.M)
                match_port = re.findall(p, output[0].return_text)

            # Remove "not present" ports
            if is_stack:
                p_notPresent = re.compile(r'^\d+:\d+.*NotPresent.*$', re.M)
            else:
                p_notPresent = re.compile(r'^\d+.*NotPresent.*$', re.M)
            parsed_info = re.findall(p_notPresent, output[0].return_text)

            for port in parsed_info:
                port_num = re.findall(p, port)
                match_port.remove(port_num[0])

            print(f"{match_port}")
            return match_port

    def go_to_device360(self, dut):
        time.sleep(5)
        self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
        time.sleep(5)

    def get_master_slot(self, onboarded_stack):
        output = self.devCmd.send_cmd(onboarded_stack.name, "show stacking")[0].return_text
        rows = output.split("\r\n")
        for row in rows:
            slot = re.search(r"\s+.*\s+(\d+)\s+", row)
            
            if not slot:
                continue
            
            slot = slot.group(1)
            
            if 'Master' in row:
                return slot
        return -1

    def get_device360_port_table_rows(self):
        table_rows = self.xiq.xflowsmanageDevice360.dev360.get_device360_port_table_rows()
        assert table_rows, "Did not find the rows of the ports table"
        table_rows[0].location_once_scrolled_into_view
        return [
            row for row in table_rows if not 
            any(field in row.text for field in ["PORT NAME", "LLDP NEIGHBOR", "PORT STATUS"])
        ]

    def verify_port_names(self, logger):
        first_order_rows = [r.text for r in self.get_device360_port_table_rows()]
        first_port_names = [r.split(" ")[0] for r in first_order_rows]
        logger.info(f"Found these port names in the table: {first_port_names}")

        for port_name in first_port_names:
            logger.info(f"Port name: {port_name}")
            if not re.match(r"1:(\d+|mgmt)", port_name):
                pytest.fail('At least one port displayed is not from Slot 1')
        logger.info(f"All ports displayed by default are from Slot 1")

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

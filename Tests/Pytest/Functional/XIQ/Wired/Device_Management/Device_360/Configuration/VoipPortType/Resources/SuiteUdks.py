import time
import string
import random
import re


class SuiteUdk:

    def __init__(self, setup_cls):
        self.setup_cls = setup_cls
        self.dev360 = setup_cls.xiq.xflowsmanageDevice360
        self.utils = setup_cls.utils
        self.auto_actions = setup_cls.auto_actions
        self.vr_name ="VR-Mgmt"
    def get_dut(self, os):
        for dut_index in [f"dut{i}" for i in range(4)]:
            if getattr(self.setup_cls.tb, dut_index, {}).get("cli_type") == os:
                return getattr(self.setup_cls.tb, dut_index)
        return None

    def close_connection_with_error_handling(self, dut):
        try:
            self.setup_cls.network_manager.device_collection.remove_device(dut.name)
            self.setup_cls.network_manager.close_connection_to_network_element(dut.name)
        except Exception as exc:
            print(exc)
        else:
            time.sleep(30)

    def get_virtual_router (self, dut_name, mgmtip):
        global vr_name
        # Send a command "show vlan" to switch and get the output
        result = self.setup_cls.devCmd.send_cmd(dut_name, 'show vlan', max_wait=10, interval=2)
        # getting the command output from the result object as a string as given below
        output = result[0].cmd_obj.return_text
        # create a regex pattern to match the vlan that contains a testbed mgmt ip to find it's virtual router info
        pattern = f'(\w+)(\s+)(\d+)(\s+)({mgmtip})(\s+)(\/.*)(\s+)(\w+)(\s+/)(.*)(VR-\w+)'
        # match variable contains a Match object.
        match = re.search(pattern, output)
        if match:
            print(f"Mgmt Vlan Name : {match.group(1)}")
            print(f"Vlan ID        : {match.group(3)}")
            print(f"Mgmt Ipaddress : {match.group(5)}")
            print(f"Active Ports   : {match.group(9)}")
            print(f"Total Ports    : {match.group(11)}")
            print(f"Virtual Router : {match.group(12)}")
            # return the vr info only if there is an active port in the mgmt vlan
            if int(match.group(9)) > 0 :
                self.vr_name = match.group(12)
                return match.group(12)
            else:
                print (f"There is no active port in the mgmt vlan {match.group(1)}")
                return -1
        else:
            print("Pattern not found, unable to get the virtual router info!")
            return -1

    def delete_create_location_organization(self, location):
        try:
            self.setup_cls.xiq.xflowsmanageLocation.create_first_organization("Extreme", "broadway", "newyork",
                                                                              "Romania")
        except:
            pass
        self.setup_cls.xiq.xflowsmanageLocation.delete_location_building_floor(*location.split(","))
        self.setup_cls.xiq.xflowsmanageLocation.create_location_building_floor(*location.split(","))

    def configure_iqagent(self, dut):
        if dut.cli_type.upper() == "EXOS":
            self.setup_cls.devCmd.send_cmd_verify_output(
                dut.name, 'show process iqagent', 'Ready', max_wait=30, interval=10)
            self.setup_cls.devCmd.send_cmd(
                dut.name, 'disable iqagent', max_wait=10,
                interval=2, confirmation_phrases='Do you want to continue?', confirmation_args='y')
            self.setup_cls.devCmd.send_cmd(
                dut.name, 'configure iqagent server ipaddress ' + self.setup_cls.cfg['sw_connection_host'],
                max_wait=10, interval=2)
            self.setup_cls.devCmd.send_cmd(dut.name, f'configure iqagent server vr {self.vr_name}', max_wait=10, interval=2)
            self.setup_cls.devCmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)
            time.sleep(10)

        elif dut.cli_type.upper() == "VOSS":

            self.setup_cls.devCmd.send_cmd(dut.name, 'configure terminal', max_wait=10, interval=2)
            self.setup_cls.devCmd.send_cmd(dut.name, 'application', max_wait=10, interval=2)
            self.setup_cls.devCmd.send_cmd(dut.name, 'no iqagent enable', max_wait=10, interval=2)
            self.setup_cls.devCmd.send_cmd(dut.name, 'iqagent server ' + self.setup_cls.cfg['sw_connection_host'],
                                           max_wait=10, interval=2)
            self.setup_cls.devCmd.send_cmd(dut.name, 'iqagent enable', max_wait=10, interval=2)
            self.setup_cls.devCmd.send_cmd_verify_output(dut.name, 'show application iqagent', 'true', max_wait=30,
                                                         interval=10)
            self.setup_cls.devCmd.send_cmd(dut.name, 'exit', max_wait=10, interval=2)
            time.sleep(10)

    def generate_random_onboarding_location(self):
        pool = list(string.ascii_letters) + list(string.digits)
        return f"Salem_{''.join(random.sample(pool, k=4))},Northeastern_{''.join(random.sample(pool, k=4))},Floor_{''.join(random.sample(pool, k=4))}"

    def verify_port_type_is_created_in_device360(self, port, port_type_name, timeout=120):

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                port_conf_content = self.dev360.get_device360_port_configuration_content()
                if port_conf_content and port_conf_content.is_displayed():
                    port_row = self.dev360.device360_get_port_row(port)

                    if re.search(fr"{port}\n{port_type_name}\n", port_row.text):
                        self.utils.print_info(
                            f"Successfully found the port type '{port_type_name}' set for the port '{port}'"
                            f" of the dut after {round(time.time() - start_time)} seconds")
                        break
                    else:
                        self.utils.print_info(
                            f"Did not find yet the port type '{port_type_name}' set for the port '{port}'")

            except Exception as exc:
                self.utils.print_warning(repr(exc))

            finally:
                time.sleep(10)
                self.auto_actions.click(self.dev360.get_device360_refresh_page_button())
        else:
            assert False, f"Did not find the port type '{port_type_name}' set for the port '{port}' of the dut"

    def go_to_device_360_port_config(self, dut):
        time.sleep(15)
        self.setup_cls.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
        time.sleep(5)
        self.setup_cls.xiq.xflowscommonNavigator.navigate_to_port_configuration_d360()

    def save_device_360_port_config(self):
        save_btn = self.dev360.get_device360_configure_port_save_button()
        self.auto_actions.click(save_btn)
        time.sleep(20)

    def open_new_port_type_editor(self, port, device_360=False):

        ret = 1
        if not device_360:
            rows = self.dev360.get_policy_configure_port_rows()
            if not rows:
                self.utils.print_info("Could not obtain list of port rows")
                ret = -1
            else:
                for row in rows:
                    if re.search(f'{port}\n', row.text):
                        d360_create_port_type = self.dev360.get_d360_create_port_type(row)
                        if d360_create_port_type:
                            self.utils.print_info(" The button d360_create_port_type from policy  was found")
                            self.auto_actions.click(d360_create_port_type)
                            time.sleep(10)
                            ret = 1
                            break
                        else:
                            self.utils.print_info(" The button d360_create_port_type from policy  was not found")
        else:
            port_conf_content = self.dev360.get_device360_port_configuration_content()

            if port_conf_content:
                port_row = self.dev360.device360_get_port_row(port)
                if not re.search(f"{port}\n", port_row.text):
                    port_row = self.dev360.device360_get_port_row(f"{port}\n")
                    if not re.search(f"{port}\n", port_row.text):
                        self.utils.print_info("Port was not found ")
                        port_row = None

                if port_row:
                    self.utils.print_debug("Found row for port: ", port_row.text)

                    d360_create_port_type = self.dev360.get_d360_create_port_type(port_row)
                    if d360_create_port_type:
                        self.utils.print_info(" The button d360_create_port_type  was found")
                        self.auto_actions.click(d360_create_port_type)
                        time.sleep(10)
                        ret = 1
                    else:
                        self.utils.print_info(" The button d360_create_port_type  was not found")

        assert ret == 1, "Failed to find port {port}"

    def go_to_next_editor_tab(self):
        get_next_button = self.dev360.get_select_element_port_type("next_button")
        if get_next_button:
            self.utils.print_info("go to the vlan configuration page")
            self.auto_actions.click(get_next_button)
            time.sleep(2)
        else:
            self.utils.print_info("get_next_button not found ")
            return -1

    def configure_port_name_usage_tab(self, port_type_name, description="test", status=True):

        name_element = self.dev360.get_select_element_port_type("name")
        if not name_element:
            self.utils.print_info("Port name was not found ")
            return -1
        self.auto_actions.send_keys(name_element, port_type_name)
        time.sleep(2)

        description_element = self.dev360.get_select_element_port_type("description")
        if not description_element:
            self.utils.print_info("Port description was not found ")
            return -1
        self.auto_actions.send_keys(description_element, description)
        time.sleep(2)

        status_element = self.dev360.get_select_element_port_type("status")
        if not status_element:
            self.utils.print_info("Port status was not found ")
            return -1

        if (not status_element.is_selected() and status) or (
                status_element.is_selected() and not status):
            self.auto_actions.click(status_element)
            time.sleep(2)

        phone_port_element = self.dev360.get_select_element_port_type("port usage", "phone port")
        if not phone_port_element:
            self.utils.print_info("phone port type was not found ")
            return -1
        self.auto_actions.click(phone_port_element)
        time.sleep(2)

    def set_voice_vlan(self, voice_vlan):

        get_select_button = self.dev360.get_select_element_port_type("voice_vlan_select_button")
        if get_select_button:
            self.auto_actions.click(get_select_button)
            time.sleep(2)
            get_dropdown_items = self.dev360.get_select_element_port_type("voice_vlan_dropdown_items")

            if self.auto_actions.select_drop_down_options(get_dropdown_items, voice_vlan):
                self.utils.print_info(" Selected into dropdown voice_vlan : ", voice_vlan)
            else:
                get_add_vlan = self.dev360.get_select_element_port_type("voice_vlan_add_vlan")
                if get_add_vlan:
                    self.auto_actions.click(get_add_vlan)
                    time.sleep(2)
                    get_name_vlan = self.dev360.get_select_element_port_type("voice_vlan_name_vlan")
                    if get_name_vlan:
                        self.auto_actions.send_keys(get_name_vlan, voice_vlan)
                        time.sleep(2)
                    else:
                        self.utils.print_info("voice vlan get_id_vlan not found ")
                        return -1
                    get_id_vlan = self.dev360.get_select_element_port_type("voice_vlan_id_vlan")
                    if get_id_vlan:
                        self.auto_actions.send_keys(get_id_vlan, voice_vlan)
                        time.sleep(2)
                    else:
                        self.utils.print_info("voice vlan get_id_vlan not found ")
                        return -1
                    get_save_vlan = self.dev360.get_select_element_port_type("save_vlan")
                    if get_save_vlan:
                        self.auto_actions.click(get_save_vlan)
                    else:
                        self.utils.print_info("get_save_vlan not found ")
                        return -1
                else:
                    self.utils.print_info("voice vlan get_add_vlan not found ")
                    return -1
        else:
            self.utils.print_info("voice vlan get_select_button not found ")
            return -1

    def set_data_vlan(self, data_vlan):
        get_select_button = self.dev360.get_select_element_port_type("data_vlan_select_button")
        if get_select_button:
            self.auto_actions.click(get_select_button)
            time.sleep(2)
            get_dropdown_items = self.dev360.get_select_element_port_type("data_vlan_dropdown_items")
            if self.auto_actions.select_drop_down_options(get_dropdown_items, data_vlan):
                self.utils.print_info(" Selected into dropdown value : ", data_vlan)
            else:
                get_add_vlan = self.dev360.get_select_element_port_type("data_vlan_add_vlan")
                if get_add_vlan:
                    self.auto_actions.click(get_add_vlan)
                    time.sleep(2)
                    get_name_vlan = self.dev360.get_select_element_port_type("data_vlan_name_vlan")
                    if get_name_vlan:
                        self.auto_actions.send_keys(get_name_vlan, data_vlan)
                        time.sleep(2)
                    else:
                        self.utils.print_info("data vlan get_id_vlan not found ")
                        return -1
                    get_id_vlan = self.dev360.get_select_element_port_type("data_vlan_id_vlan")
                    if get_id_vlan:
                        self.auto_actions.send_keys(get_id_vlan, data_vlan)
                        time.sleep(2)
                    else:
                        self.utils.print_info("data vlan get_id_vlan not found ")
                        return -1
                    get_save_vlan = self.dev360.get_select_element_port_type("save_vlan")
                    if get_save_vlan:
                        self.auto_actions.click(get_save_vlan)
                    else:
                        self.utils.print_info("get_save_vlan not found ")
                        return -1
                else:
                    self.utils.print_info("data vlan get_add_vlan not found ")
                    return -1
        else:
            self.utils.print_info("data vlan get_select_button not found ")
            return -1

    def enable_lldp_voice_vlan_options(self, lldp_voice_options_flag):
        lldp_voice_options = self.dev360.get_select_element_port_type("lldp_voice_vlan_options")
        if not lldp_voice_options:
            self.utils.print_info("checkbox not found")
            return -1

        if (not lldp_voice_options.is_selected() and lldp_voice_options_flag) or (
                lldp_voice_options.is_selected() and not lldp_voice_options_flag):
            self.auto_actions.click(lldp_voice_options)
            time.sleep(2)

    def enable_cdp_voice_vlan_options(self, cdp_voice_options_flag):
        cdp_voice_options = self.dev360.get_select_element_port_type("cdp_voice_vlan_options")
        if not cdp_voice_options:
            self.utils.print_info("checkbox not found")
            return -1

        if (not cdp_voice_options.is_selected() and cdp_voice_options_flag) or (
                cdp_voice_options.is_selected() and not cdp_voice_options_flag):
            self.auto_actions.click(cdp_voice_options)
            time.sleep(2)

    def configure_lldp_adv_of_med_voice_vlan(self, lldp_advertisment_of_med_voice_vlan_flag, lldp_voice_vlan_dscp):
        lldp_advertisment_of_med_voice_vlan = self.dev360.get_select_element_port_type(
            "enable_lldp_advertisment_of_med_voice_vlan")

        if not lldp_advertisment_of_med_voice_vlan:
            self.utils.print_info("'checkbox option not found")
            return -1

        if (not lldp_advertisment_of_med_voice_vlan.is_selected() and lldp_advertisment_of_med_voice_vlan_flag) or \
                (lldp_advertisment_of_med_voice_vlan.is_selected() and not lldp_advertisment_of_med_voice_vlan_flag):
            self.auto_actions.click(lldp_advertisment_of_med_voice_vlan)
            time.sleep(2)

        if lldp_advertisment_of_med_voice_vlan.is_selected():

            lldp_advertisment_of_med_voice_vlan_dscp_value_element = self.dev360.get_select_element_port_type(
                "lldp_advertisment_of_med_voice_vlan_dscp_value")
            if not lldp_advertisment_of_med_voice_vlan_dscp_value_element:
                self.utils.print_info(
                    f"input dscp value not found")
                return -1
            else:
                self.auto_actions.send_keys(lldp_advertisment_of_med_voice_vlan_dscp_value_element,
                                            lldp_voice_vlan_dscp)
                time.sleep(2)

    def configure_lldp_adv_of_med_voice_signaling_vlan(
            self, lldp_advertisment_of_med_signaling_vlan_flag, lldp_voice_signaling_dscp):

        lldp_advertisment_of_med_signaling_vlan = self.dev360.get_select_element_port_type(
            "enable_lldp_advertisment_of_med_voice_signaling_vlan")

        if not lldp_advertisment_of_med_signaling_vlan:
            self.utils.print_info(f"'checkbox not found")
            return -1

        if (not lldp_advertisment_of_med_signaling_vlan.is_selected() and lldp_advertisment_of_med_signaling_vlan_flag) \
                or (lldp_advertisment_of_med_signaling_vlan.is_selected()
                    and not lldp_advertisment_of_med_signaling_vlan_flag):
            self.auto_actions.click(lldp_advertisment_of_med_signaling_vlan)
            time.sleep(2)

        if lldp_advertisment_of_med_signaling_vlan.is_selected():
            lldp_advertisment_of_med_voice_signaling_vlan_dscp_value_element = self.dev360.get_select_element_port_type(
                "lldp_advertisment_of_med_voice_signaling_vlan_dscp_value")
            if not lldp_advertisment_of_med_voice_signaling_vlan_dscp_value_element:
                self.utils.print_info(
                    "input dscp value not found")
                return -1
            else:
                self.auto_actions.send_keys(lldp_advertisment_of_med_voice_signaling_vlan_dscp_value_element,
                                            lldp_voice_signaling_dscp)
                time.sleep(2)

    def verify_dscp_values_validation(
            self, dscp_field, min_dscp, max_dscp, expected_error_message, values_to_test=["", -2, 67]):

        assert dscp_field in [
            "lldp_advertisment_of_med_voice_vlan_dscp_value",
            "lldp_advertisment_of_med_voice_signaling_vlan_dscp_value"
        ]

        if dscp_field == 'lldp_advertisment_of_med_voice_vlan_dscp_value':

            lldp_advertisment_of_med_voice_vlan = self.dev360.get_select_element_port_type(
                "lldp_advertisment_of_med_voice_vlan_dscp_value")

            assert lldp_advertisment_of_med_voice_vlan, "checkbox option not found"

            assert lldp_advertisment_of_med_voice_vlan.get_attribute("type") == "number"
            assert int(lldp_advertisment_of_med_voice_vlan.get_attribute("min")) == min_dscp
            assert int(lldp_advertisment_of_med_voice_vlan.get_attribute("max")) == max_dscp
            assert lldp_advertisment_of_med_voice_vlan.get_attribute(
                "data-validation-error-msg") == expected_error_message

            for wrong_value in values_to_test:

                self.configure_lldp_adv_of_med_voice_vlan(
                    lldp_advertisment_of_med_voice_vlan_flag=True, lldp_voice_vlan_dscp=1)
                time.sleep(2)

                errors = self.dev360.get_phone_dscp_values_validation_errors(validation_message=expected_error_message)
                assert not errors

                self.configure_lldp_adv_of_med_voice_vlan(
                    lldp_advertisment_of_med_voice_vlan_flag=True, lldp_voice_vlan_dscp=wrong_value)
                time.sleep(2)

                [error] = self.dev360.get_phone_dscp_values_validation_errors(validation_message=expected_error_message)

                assert re.search(expected_error_message, error.get_attribute("data-tooltip"))

                self.configure_lldp_adv_of_med_voice_vlan(
                    lldp_advertisment_of_med_voice_vlan_flag=True, lldp_voice_vlan_dscp=1)
                time.sleep(5)
                error = self.dev360.get_phone_dscp_values_validation_errors(validation_message=expected_error_message)
                if error:
                    self.auto_actions.click(error[0])

                self.configure_lldp_adv_of_med_voice_vlan(
                    lldp_advertisment_of_med_voice_vlan_flag=False, lldp_voice_vlan_dscp=0)
                time.sleep(2)

        elif dscp_field == "lldp_advertisment_of_med_voice_signaling_vlan_dscp_value":

            lldp_advertisment_of_med_signaling_vlan = self.dev360.get_select_element_port_type(
                "lldp_advertisment_of_med_voice_signaling_vlan_dscp_value")

            assert lldp_advertisment_of_med_signaling_vlan, "checkbox not found"

            assert lldp_advertisment_of_med_signaling_vlan.get_attribute("type") == "number"
            assert int(lldp_advertisment_of_med_signaling_vlan.get_attribute("min")) == 0
            assert int(lldp_advertisment_of_med_signaling_vlan.get_attribute("max")) == 63
            assert lldp_advertisment_of_med_signaling_vlan.get_attribute(
                "data-validation-error-msg") == expected_error_message

            for wrong_value in values_to_test:

                self.configure_lldp_adv_of_med_voice_signaling_vlan(
                    lldp_advertisment_of_med_signaling_vlan_flag=True, lldp_voice_signaling_dscp=1)
                time.sleep(2)

                errors = self.dev360.get_phone_dscp_values_validation_errors(validation_message=expected_error_message)
                assert not errors

                self.configure_lldp_adv_of_med_voice_signaling_vlan(
                    lldp_advertisment_of_med_signaling_vlan_flag=True, lldp_voice_signaling_dscp=wrong_value)
                time.sleep(2)

                [error] = self.dev360.get_phone_dscp_values_validation_errors(validation_message=expected_error_message)

                assert re.search(expected_error_message, error.get_attribute("data-tooltip"))

                self.configure_lldp_adv_of_med_voice_signaling_vlan(
                    lldp_advertisment_of_med_signaling_vlan_flag=True, lldp_voice_signaling_dscp=1)
                time.sleep(5)
                error = self.dev360.get_phone_dscp_values_validation_errors(validation_message=expected_error_message)
                if error:
                    self.auto_actions.click(error[0])

                self.configure_lldp_adv_of_med_voice_signaling_vlan(
                    lldp_advertisment_of_med_signaling_vlan_flag=False, lldp_voice_signaling_dscp=0)
                time.sleep(2)

    def revert_port_configuration(self, port, port_type_name, retries=5):

        for _ in range(retries):
            try:
                rows = self.dev360.get_device360_configure_port_rows()
                for row in rows:
                    if re.search(rf"{port}\n{port_type_name}", row.text):
                        port_row = row
                        break
                else:
                    raise AssertionError("Failed to get the port row")

                self.utils.print_info("Found row for port: ", port_row.text)
                port_override_revert = self.dev360.get_d360_configure_port_details_settings_aggregation_stp_storm_control_row_override_revert(
                    "port usage", port_row)

                if port_override_revert:
                    time.sleep(3)
                    self.utils.print_info("move on 'override' button ")
                    self.auto_actions.move_to_element(port_override_revert)
                    time.sleep(5)

                    port_revert = self.dev360.get_d360_configure_port_row_revert_button(port_row)
                    if port_revert:
                        self.utils.print_info("Clicking 'Revert' button")
                        self.auto_actions.click(port_revert)
                        time.sleep(5)
                        break
                    else:
                        raise AssertionError("Could not click Revert button")
                else:
                    raise AssertionError("The override revert button was not found")
            except Exception as exc:
                self.utils.print_info(repr(exc))
                time.sleep(30)
        else:
            raise AssertionError("Failed to revert to default port config")

    def get_voice_vlan(self):
        return self.dev360.get_select_element_port_type("voice_vlan_input")

    def get_data_vlan(self):
        return self.dev360.get_select_element_port_type("data_vlan_input")

    def get_lldp_voice_vlan_options(self):
        return self.dev360.get_select_element_port_type("lldp_voice_vlan_options").is_selected()

    def get_cdp_voice_vlan_options(self):
        return self.dev360.get_select_element_port_type("cdp_voice_vlan_options").is_selected()

    def go_to_last_page(self):

        self.utils.print_info("Go to the last page and save the port type")
        for _ in range(10):
            get_next_button = self.dev360.get_select_element_port_type("next_button")
            if get_next_button:
                if get_next_button.is_enabled():
                    self.auto_actions.click(get_next_button)
                    time.sleep(2)
                else:
                    break
            else:
                self.utils.print_info("get_next_button not found")

    def get_summary(self):
        ret = {}
        for row_name, row_value in zip(
                [
                    "LLDP Advertisements",
                    "802.1 VLAN and port protocol",
                    "Med Voice VLAN DSCP Value",
                    "Med Voice Signaling DSCP Value",
                    "CDP Advertisement",
                    "CDP Voice VLAN",
                    "CDP Power Available",
                    "Voice VLAN",
                    "Data VLAN"
                ],
                [
                    "port_type_voice_lldp_advertisment_summary",
                    "802_1_vlan_and_port_protocol_summary",
                    "med_voice_vlan_dscp_value_summary",
                    "med_voice_signaling_dscp_value_summary",
                    "cdp_advertisment_summary",
                    "cdp_voice_vlan_summary",
                    "cdp_power_available_summary",
                    "voice_vlan_summary",
                    "data_vlan_summary"
                ]
        ):
            print("row name and value ",row_name,row_value)
            print(self.dev360.get_select_element_port_type_summary(row_value))
            ret[row_name] = self.dev360.get_select_element_port_type_summary(row_value).text
        return ret

    def generate_port_type_name(self):
        return f"port_type_{str(time.time())[::-1][:5]}"

    def generate_policy_name(self):
        return f"test_policy_{str(time.time())[::-1][:5]}"

    def generate_template_name(self):
        return f"template_{str(time.time())[::-1][:5]}"

    def generate_cli_locally(self,configs_list,ports=2,vlan_voice=77,vlan_data=78,voicevlan_alpha="VLAN_0077"):

        configs = ["configure vlan %s add port %s untagged",
                   "configure vlan %s add port %s tagged",
                   "configure lldp ports %s advertise vendor-specific med capabilities",
                   "configure lldp ports %s advertise system-capabilities",
                   "configure lldp ports %s advertise vendor-specific dot1 vlan-name vlan %s",
                   "configure lldp ports %s advertise vendor-specific dot1 port-protocol-vlan-id vlan %s",
                   "configure lldp ports %s advertise vendor-specific med policy application voice vlan %s dscp 10",
                   "configure lldp ports %s advertise vendor-specific med policy application voice-signaling vlan %s dscp 10",
                   "configure cdp voip-vlan %s ports %s",
                   "configure cdp power-available advertise ports %s",]

        configurationList = []
        for each in configs_list:
            if each == 0:
                configurationList.append((configs[each] % (vlan_data, ports)))
            if each == 1:
                configurationList.append((configs[each] % (vlan_voice, ports)))
            if each in [2,3]:
                configurationList.append((configs[each] % (ports)))
            if each in [4, 5, 6, 7]:
                configurationList.append((configs[each] % (ports, voicevlan_alpha)))
            if each == 8:
                configurationList.append((configs[each] % (voicevlan_alpha,ports)))
            if each == 9:
                configurationList.append((configs[each] % (ports)))

        return configurationList

import pytest
import re
import string
import random

from collections import defaultdict
from extauto.common.Utils import Utils
from extauto.common.AutoActions import AutoActions


class SuiteUdk:

    def __init__(self, setup_cls):
        self.setup_cls = setup_cls
        self.xiq = self.setup_cls.xiq
        self.dev360 = setup_cls.xiq.xflowsmanageDevice360
        self.devices = setup_cls.xiq.xflowscommonDevices
        self.utils = Utils()
        self.auto_actions = AutoActions()
        self.wait_till = self.utils.wait_till
        self.wait_till_web_element_delay = 5
        self.wait_till_click_delay = 4
        self.wait_till_send_keys_delay = 4

    def close_connection_with_error_handling(self, dut):
        try:

            try:
                if dut.cli_type.upper() == "VOSS":
                    for session_id in range(7):
                        self.setup_cls.devCmd.send_cmd(dut.name, f"clear ssh {session_id}")
                elif dut.cli_type.upper() == "EXOS":
                    self.setup_cls.devCmd.send_cmd(dut.name, "clear session all")
            except Exception as err:
                self.utils.print_info(err)

            self.setup_cls.network_manager.device_collection.remove_device(dut.name)
            self.setup_cls.network_manager.close_connection_to_network_element(dut.name)

        except Exception as exc:
            self.utils.print_info(exc)
        else:
            self.wait_till(timeout=20)

    def generate_port_type_name(self):
        pool = list(string.ascii_letters) + list(string.digits)
        return f"port_type_{''.join(random.sample(pool, k=6))}"

    def go_to_last_page(self):
        self.utils.print_info("Go to the last page and save the port type")
        for _ in range(10):

            get_next_button, _ = self.wait_till(
                func=lambda: self.dev360.get_select_element_port_type("next_button"),
                exp_func_resp=True,
                delay=self.wait_till_web_element_delay
            )

            if get_next_button.is_enabled():
                self.wait_till(
                    func=lambda: self.auto_actions.click(get_next_button),
                    exp_func_resp=True,
                    delay=self.wait_till_click_delay
                )
            else:
                break

    def go_to_next_editor_tab(self):
        get_next_button, _ = self.wait_till(lambda: self.dev360.get_select_element_port_type("next_button"),
                                            exp_func_resp=True, delay=self.wait_till_web_element_delay)
        if get_next_button:
            self.wait_till(
                func=lambda: self.auto_actions.click(get_next_button),
                exp_func_resp=True, delay=self.wait_till_click_delay)
        else:
            self.utils.print_info("get_next_button not found ")
            return -1

    def configure_port_name_usage_tab(self, port_type_name, description="test", status=True, port_type="access"):
        name_element, _ = self.wait_till(
            func=lambda: self.dev360.get_select_element_port_type("name"),
            exp_func_resp=True,
            delay=self.wait_till_web_element_delay)

        if not name_element:
            self.utils.print_info("Port name was not found ")
            return -1

        self.wait_till(
            func=lambda: self.auto_actions.send_keys(name_element, port_type_name),
            exp_func_resp=True,
            delay=self.wait_till_send_keys_delay
        )

        description_element, _ = self.wait_till(
            func=lambda: self.dev360.get_select_element_port_type("description"),
            exp_func_resp=True,
            silent_failure=True,
            delay=self.wait_till_web_element_delay)

        if not description_element:
            self.utils.print_info("Port description was not found ")
            return -1

        self.wait_till(
            func=lambda: self.auto_actions.send_keys(description_element, description),
            exp_func_resp=True,
            delay=self.wait_till_send_keys_delay
        )

        status_element, _ = self.wait_till(
            func=lambda: self.dev360.get_select_element_port_type("status"),
            exp_func_resp=True,
            silent_failure=True,
            delay=self.wait_till_web_element_delay
        )

        if not status_element:
            self.utils.print_info("Port status was not found ")
            return -1

        if (not status_element.is_selected() and status) or (
                status_element.is_selected() and not status):
            self.wait_till(
                func=lambda: self.auto_actions.click(status_element),
                exp_func_resp=True,
                delay=self.wait_till_click_delay
            )

        auto_sense, _ = self.wait_till(
            func=lambda: self.dev360.get_select_element_port_type("auto-sense"),
            exp_func_resp=True,
            silent_failure=True,
            delay=self.wait_till_web_element_delay
        )

        if auto_sense:
            if auto_sense.is_selected():
                self.wait_till(
                    func=lambda: self.auto_actions.click(auto_sense),
                    exp_func_resp=True,
                    delay=self.wait_till_click_delay
                )

        port_element, _ = self.wait_till(
            func=lambda: self.dev360.get_select_element_port_type("port usage", f"{port_type} port"),
            exp_func_resp=True,
            silent_failure=True,
            delay=self.wait_till_web_element_delay
        )

        if not port_element:
            self.utils.print_info(f"{port_type} port type was not found ")
            return -1

        self.wait_till(
            func=lambda: self.auto_actions.click(port_element),
            exp_func_resp=True,
            delay=self.wait_till_click_delay
        )
        self.wait_till(timeout=2)

    def open_new_port_type_editor(self, port, device_360=False):
        self.wait_till(timeout=10)
        ret = 1
        if not device_360:
            rows, _ = self.wait_till(
                func=self.dev360.get_policy_configure_port_rows,
                exp_func_resp=True,
                silent_failure=True,
                delay=self.wait_till_web_element_delay
            )
            if not rows:
                self.utils.print_info("Could not obtain list of port rows")
                ret = -1
            else:
                for row in rows:
                    if re.search(f'{port}\n', row.text):
                        d360_create_port_type, _ = self.wait_till(
                            func=lambda: self.dev360.get_d360_create_port_type(row),
                            exp_func_resp=True,
                            silent_failure=True,
                            delay=self.wait_till_web_element_delay
                        )
                        if d360_create_port_type:
                            self.utils.print_info(" The button d360_create_port_type from policy  was found")
                            self.wait_till(
                                func=lambda: self.auto_actions.click(d360_create_port_type),
                                exp_func_resp=True,
                                delay=self.wait_till_click_delay
                            )
                            self.wait_till(timeout=10)
                            ret = 1
                            break
                        else:
                            self.utils.print_info(" The button d360_create_port_type from policy  was not found")
        else:
            port_conf_content, _ = self.wait_till(
                func=self.dev360.get_device360_port_configuration_content,
                exp_func_resp=True,
                silent_failure=True,
                delay=self.wait_till_web_element_delay
            )

            if port_conf_content:
                port_row, _ = self.wait_till(
                    func=lambda: self.dev360.device360_get_port_row(port),
                    exp_func_resp=True,
                    silent_failure=True,
                    delay=self.wait_till_web_element_delay
                )
                if not re.search(f"{port}\n", port_row.text):
                    port_row, _ = self.wait_till(
                        func=lambda: self.dev360.device360_get_port_row(f"{port}\n"),
                        exp_func_resp=True,
                        silent_failure=True
                    )
                    if not re.search(f"{port}\n", port_row.text):
                        self.utils.print_info("Port was not found ")
                        port_row = None

                if port_row:
                    self.utils.print_debug("Found row for port: ", port_row.text)

                    d360_create_port_type, _ = self.wait_till(
                        func=lambda: self.dev360.get_d360_create_port_type(port_row),
                        silent_failure=True,
                        exp_func_resp=True,
                        delay=self.wait_till_web_element_delay
                    )

                    if d360_create_port_type:
                        self.utils.print_info(" The button d360_create_port_type  was found")
                        self.wait_till(
                            func=lambda: self.auto_actions.click(d360_create_port_type),
                            exp_func_resp=True,
                            delay=self.wait_till_click_delay
                        )
                        self.wait_till(timeout=10)
                        ret = 1
                    else:
                        self.utils.print_info(" The button d360_create_port_type  was not found")

        assert ret == 1, "Failed to find port {port}"

    def save_port_type_config(self):
        save_button, _ = self.wait_till(
            func=self.dev360.get_close_port_type_box,
            exp_func_resp=True,
            delay=self.wait_till_web_element_delay
        )

        self.wait_till(
            func=lambda: self.auto_actions.click(save_button),
            exp_func_resp=True,
            delay=self.wait_till_click_delay
        )
        self.wait_till(timeout=10)

    def close_port_type_config(self):
        close_button, _ = self.wait_till(
            func=self.dev360.get_cancel_port_type_box,
            exp_func_resp=True,
            delay=self.wait_till_web_element_delay
        )
        self.wait_till(
            func=lambda: self.auto_actions.click(close_button),
            exp_func_resp=True,
            delay=self.wait_till_click_delay
        )
        self.wait_till(timeout=10)

    def save_template_config(self):
        self.wait_till(timeout=5)
        self.setup_cls.xiq.xflowsconfigureSwitchTemplate.switch_template_save()
        self.wait_till(timeout=10)

    def verify_delta_cli_commands(self, dut, commands, retries=5):
        self.wait_till(timeout=10)
        self.xiq.xflowscommonDevices._goto_devices()
        self.wait_till(timeout=10)

        self.xiq.xflowsmanageDevices.refresh_devices_page()
        self.wait_till(timeout=5)

        for _ in range(retries):
            try:
                self.setup_cls.xiq.xflowscommonDevices.select_device(device_mac=dut.mac)

                btn, _ = self.wait_till(
                    func=self.setup_cls.xiq.xflowsmanageDeviceConfig.get_device_config_audit_view,
                    delay=self.wait_till_web_element_delay,
                    exp_func_resp=True
                )

                self.wait_till(
                    func=lambda: self.auto_actions.click(btn),
                    delay=self.wait_till_click_delay,
                    exp_func_resp=True
                )

                delta_view, _ = self.wait_till(
                    func=self.setup_cls.xiq.xflowsmanageDeviceConfig.get_device_config_audit_delta_view,
                    delay=self.wait_till_web_element_delay,
                    exp_func_resp=True
                )

                self.wait_till(
                    func=lambda: self.auto_actions.click(delta_view),
                    timeout=60,
                    delay=20,
                    exp_func_resp=True
                )

                delta_configs, _ = self.wait_till(
                    func=self.setup_cls.xiq.xflowsmanageDeviceConfig.get_device_config_audit_delta_view_content,
                    timeout=60,
                    exp_func_resp=True,
                    delay=self.wait_till_web_element_delay
                )

                delta_configs = delta_configs.text

                for command in commands:
                    assert re.search(command, delta_configs), f"Did not find this command in delta CLI: {command}"

            except Exception as exc:
                self.utils.print_info(repr(exc))
                self.wait_till(timeout=15)
            else:
                break
            finally:

                try:
                    close_btn, _ = self.wait_till(
                        func=self.setup_cls.xiq.xflowsmanageDeviceConfig.get_device_config_audit_view_close_button,
                        exp_func_resp=True,
                        silent_failure=True,
                        delay=self.wait_till_web_element_delay
                    )

                    self.wait_till(
                        func=lambda: self.auto_actions.click(close_btn) == 1,
                        exp_func_resp=True,
                        delay=self.wait_till_click_delay,
                        silent_failure=True
                    )
                except:
                    pass

                self.setup_cls.xiq.xflowscommonDevices.select_device(device_mac=dut.mac)
        else:
            assert False, f"Failed to verify these commands in the delta cli after {retries} retries: {commands}"

    def click_on_stp_tab(self, level="template"):
        if level == "template":
            stp_tab_button, _ = self.wait_till(
                func=self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_stp_tab,
                silent_failure=True,
                exp_func_resp=True,
                delay=self.wait_till_web_element_delay
            )
        elif level == "device":
            stp_tab_button, _ = self.wait_till(
                func=self.xiq.xflowsmanageDevice360.get_d360_configure_port_stp_tab_button,
                silent_failure=True,
                exp_func_resp=True,
                delay=self.wait_till_web_element_delay
            )

        assert stp_tab_button, "Failed to get the STP tab button"

        self.wait_till(
            func=lambda: self.auto_actions.click(stp_tab_button),
            exp_func_resp=True,
            delay=self.wait_till_click_delay
        )

        self.utils.print_info("Successfully clicked the STP tab button")

    def click_on_port_details_tab(self, level="template"):
        if level == "template":
            stp_tab_button, _ = self.wait_till(
                func=self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_port_details_tab,
                silent_failure=True,
                exp_func_resp=True,
                delay=self.wait_till_web_element_delay
            )

            assert stp_tab_button, "Failed to get the Port Details tab button"

            self.wait_till(
                func=lambda: self.auto_actions.click(stp_tab_button),
                exp_func_resp=True,
                delay=self.wait_till_click_delay
            )

            self.utils.print_info("Successfully clicked the Port Details tab button")

        elif level == "device":
            pass

    def get_stp_port_configuration_rows(self, level="template"):
        if level == "template":
            rows, _ = self.wait_till(
                func=self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_stp_port_rows,
                silent_failure=True,
                exp_func_resp=True,
                delay=self.wait_till_web_element_delay
            )

        elif level == "device":
            rows, _ = self.wait_till(
                func=self.xiq.xflowsmanageDevice360.get_device360_configure_stp_rows,
                silent_failure=True,
                exp_func_resp=True,
                delay=self.wait_till_web_element_delay

            )

        assert rows, "Failed to get the STP port configuration rows"
        return rows

    def get_stp_port_configuration_row(self, port, level="template"):
        rows = self.get_stp_port_configuration_rows(level=level)
        for row in rows:
            if re.search(f"^{port}\n", row.text):
                self.utils.print_info(f"Successfully found the row port for port={port}")
                return row
        else:
            pytest.fail(f"Failed to find the row port for port={port}")

    def get_path_cost_value_from_stp_port_configuration_row(self, port, level="template"):
        row = self.get_stp_port_configuration_row(port=port, level=level)

        if level == "template":

            cost_element, _ = self.wait_till(
                func=lambda:
                self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_path_cost_row(row),
                silent_failure=True,
                exp_func_resp=True,
                delay=self.wait_till_web_element_delay
            )

        elif level == "device":

            cost_element, _ = self.wait_till(
                func=lambda: self.xiq.xflowsmanageDevice360.get_device360_port_configuration_path_cost_stp(row),
                silent_failure=True,
                exp_func_resp=True,
                delay=self.wait_till_web_element_delay
            )

        return cost_element.get_attribute("value")

    def get_stp_settings_summary(self):
        self.wait_till(timeout=5)
        summary = {}

        for row_name, row_value in zip(
                ["STP", "Edge Port", "BPDU Protection", "Priority", "Path Cost"],
                ["stp", "edge port", "bpdu protection", "priority", "path cost"]
        ):
            try:
                summary[row_name] = self.dev360.dev360.get_select_element_port_type_summary(row_value).text
            except:
                summary[row_name] = ""
        return summary

    def go_to_stp_settings_tab_in_honeycomb(self):
        self.utils.print_info("Go to the STP settings page")

        for _ in range(5):

            if "active" in self.dev360.get_select_element_port_type("stpPage").get_attribute("class"):
                return

            get_next_button, _ = self.wait_till(
                func=lambda: self.dev360.get_select_element_port_type("next_button"),
                exp_func_resp=True,
                delay=self.wait_till_web_element_delay
            )

            if get_next_button:
                if get_next_button.is_enabled():

                    self.wait_till(
                        func=lambda: self.auto_actions.click(get_next_button),
                        exp_func_resp=True,
                        delay=self.wait_till_click_delay
                    )

                    self.wait_till(timeout=2)
                else:
                    break
            else:
                self.utils.print_info("get_next_button not found")

    def configure_stp_settings_tab_in_honeycomb(self, stp_enabled=None, edge_port=None, bpdu_protection=None,
                                                path_cost=None, priority=None):
        if stp_enabled is not None:
            stp_enabled_element, _ = self.wait_till(
                func=lambda: self.dev360.get_select_element_port_type("stp enable"),
                exp_func_resp=True,
                silent_failure=True,
                delay=self.wait_till_web_element_delay
            )

            assert stp_enabled_element, "STP Enabled element was not found"

            if (not stp_enabled_element.is_selected() and stp_enabled) or (
                    stp_enabled_element.is_selected() and not stp_enabled):
                self.wait_till(
                    func=lambda: self.auto_actions.click(stp_enabled_element),
                    exp_func_resp=True,
                    delay=self.wait_till_click_delay
                )
                self.utils.print_info("Successfully clicked on the STP enabled element")

        if edge_port is not None:
            edge_port_element, _ = self.wait_till(
                func=lambda: self.dev360.get_select_element_port_type("edge port"),
                exp_func_resp=True,
                silent_failure=True,
                delay=self.wait_till_web_element_delay
            )

            assert edge_port_element, "Edge Port element was not found"

            if (not edge_port_element.is_selected() and edge_port) or (
                    edge_port_element.is_selected() and not edge_port):
                self.wait_till(
                    func=lambda: self.auto_actions.click(edge_port_element),
                    exp_func_resp=True,
                    delay=self.wait_till_click_delay
                )
                self.utils.print_info("Successfully clicked on the Edge Port element")

        if bpdu_protection is not None:
            bpdu_protection_element, _ = self.wait_till(
                func=lambda: self.dev360.get_select_element_port_type("bpdu protection"),
                exp_func_resp=True,
                silent_failure=True,
                delay=self.wait_till_web_element_delay
            )

            assert bpdu_protection_element, "BPDU Protection element was not found"

            self.wait_till(
                func=lambda: self.auto_actions.click(bpdu_protection_element),
                exp_func_resp=True,
                delay=self.wait_till_click_delay
            )
            self.utils.print_info("Successfully clicked on the BPDU Protection element")

            get_bpdu_protection_items, _ = self.wait_till(
                func=lambda: self.dev360.get_select_element_port_type("bpdu_protection_items"),
                exp_func_resp=True,
                silent_failure=True,
                delay=self.wait_till_web_element_delay
            )

            assert get_bpdu_protection_items, "BPDU Protection list elements not found"

            self.wait_till(
                func=lambda: self.auto_actions.select_drop_down_options(
                    get_bpdu_protection_items, bpdu_protection),
                exp_func_resp=True
            )
            self.utils.print_info("Selected into dropdown value : ", bpdu_protection)

        if path_cost is not None:
            path_cost_element, _ = self.wait_till(
                func=lambda: self.dev360.get_select_element_port_type("path cost"),
                exp_func_resp=True, silent_failure=True,
                delay=self.wait_till_web_element_delay
            )

            assert path_cost_element, "Path Cost element was not found"

            self.wait_till(
                func=lambda: self.auto_actions.send_keys(path_cost_element, str(path_cost)),
                exp_func_resp=True,
                delay=self.wait_till_send_keys_delay
            )
            self.utils.print_info("Successfully configured the path cost field")

        if priority:
            priority_element, _ = self.wait_till(
                func=lambda: self.dev360.get_select_element_port_type("priority"),
                exp_func_resp=True,
                silent_failure=True,
                delay=self.wait_till_web_element_delay
            )

            assert priority_element, "Priority element was not found"

            self.wait_till(
                func=lambda: self.auto_actions.click(priority_element),
                exp_func_resp=True,
                delay=self.wait_till_click_delay
            )
            self.utils.print_info("Successfully clicked on the priority element")

            get_priority_items, _ = self.wait_till(
                func=lambda: self.dev360.get_select_element_port_type("priority_items"),
                exp_func_resp=True,
                silent_failure=True,
                delay=self.wait_till_web_element_delay
            )
            assert get_priority_items, "Priority dropdown elements not found"

            self.wait_till(
                func=lambda: self.auto_actions.select_drop_down_options(get_priority_items, str(priority)),
                exp_func_resp=True
            )
            self.utils.print_info("Selected into dropdown value : ", priority)

    def verify_path_cost_field_is_editable(self):
        path_cost_element, _ = self.wait_till(
            func=lambda: self.dev360.get_select_element_port_type("path cost"),
            exp_func_resp=True,
            silent_failure=True,
            delay=self.wait_till_web_element_delay
        )
        assert path_cost_element, "Path Cost element was not found"

        assert path_cost_element.is_enabled() is True, "The path cost element is not editable"
        self.utils.print_info("Successfully verified that the path cost field is editable")

    def verify_stp_settings_in_honeycomb_summary(self, stp_settings_summary, stp_enabled=None, edge_port=None,
                                                 bpdu_protection=None, priority=None, path_cost=None):
        if stp_enabled is not None:
            stp_enabled = "Enabled" if stp_enabled is True else "Disabled"
            assert stp_enabled == stp_settings_summary["STP"], \
                f'Expected STP Enabled to be "{stp_enabled}" but found "{stp_settings_summary["STP"]}"'

        if edge_port is not None:
            edge_port = "Enabled" if edge_port is True else "Disabled"
            assert edge_port == stp_settings_summary["Edge Port"], \
                f'Expected Edge Port to be "{edge_port}" but found "{stp_settings_summary["Edge Port"]}"'

        if bpdu_protection is not None:
            assert bpdu_protection == stp_settings_summary["BPDU Protection"], \
                f'Expected BPDU Protection to be "{bpdu_protection}" ' \
                f'but found "{stp_settings_summary["BPDU Protection"]}"'

        if priority is not None:
            assert int(priority) == int(stp_settings_summary["Priority"]), \
                f'Expected Priority to be "{priority}" but found "{stp_settings_summary["Priority"]}"'

        if path_cost is not None:
            assert int(path_cost) == int(stp_settings_summary["Path Cost"]), \
                f'Expected Path Cost enabled to be "{path_cost}" but found "{stp_settings_summary["Path Cost"]}"'

    def update_and_wait_switch(self, policy_name, dut):
        self.wait_till(timeout=10)
        self.xiq.xflowscommonDevices._goto_devices()
        self.wait_till(timeout=10)

        self.utils.print_info(f"Select switch row with serial {dut.mac}")
        if not self.devices.select_device(device_mac=dut.mac):
            self.utils.print_info(f"Switch {dut.mac} is not present in the grid")
            return -1
        self.wait_till(timeout=10)
        self.devices._update_switch(update_method="PolicyAndConfig")
        self.wait_till(timeout=10)
        return self.devices._check_update_network_policy_status(policy_name, dut.mac)

    def verify_path_cost_on_dut(self, dut, port, expected_path_cost, mode="mstp", retries=4, step=60):
        for _ in range(retries):
            try:
                self.close_connection_with_error_handling(dut)
                self.connect_to_network_element(dut)

                if dut.cli_type.upper() == "AH-FASTPATH":
                    output = self.setup_cls.devCmd.send_cmd(
                        dut.name, f'show spanning-tree mst port detailed 0 {port}', max_wait=10, interval=2)[
                        0].return_text
                    path_cost_match = re.search(rf"\r\nPort Path Cost\.+\s+(\d+)", output)
                    external_path_cost_match = re.search(rf"\r\nExternal Port Path Cost\.+\s+(\d+)", output)
                    assert path_cost_match or external_path_cost_match

                    for path_cost_match in [path_cost_match, external_path_cost_match]:
                        try:
                            found_path_cost = int(path_cost_match.group(1))
                            self.utils.print_info(f"Found path_cost='{found_path_cost}' for port={port}")
                            assert int(expected_path_cost) == found_path_cost, \
                                f"Found path cost for port={port} is {found_path_cost}" \
                                f" but expected {expected_path_cost}"
                        except:
                            continue
                        else:
                            return
                    else:
                        pytest.fail(f"Failed to find the path cost correctly configure for port={port}")

                else:
                    if dut.cli_type.upper() == "VOSS":
                        output = self.setup_cls.devCmd.send_cmd(
                            dut.name, f'show spanning-tree {mode} port config {port}', max_wait=10, interval=2)[
                            0].return_text
                        path_cost_match = re.search(fr"\r\nCist Port cost\s+:\s*(\d+)\s*\r\n", output)

                    elif dut.cli_type.upper() == "EXOS":
                        output = self.setup_cls.devCmd.send_cmd(
                            dut.name, f'show stpd s0 ports {port} detail', max_wait=10, interval=2)[
                            0].return_text
                        path_cost_match = re.search(fr"\tPath Cost:\s(\d+)\r\n", output)

                    assert path_cost_match, "Failed to match get the path cost of port={port} from dut {dut}"
                    found_path_cost = int(path_cost_match.group(1))
                    self.utils.print_info(f"Found path_cost='{found_path_cost}' for port={port}")
                    assert int(expected_path_cost) == found_path_cost, \
                        f"Found path cost for port={port} is {found_path_cost}" \
                        f" but expected {expected_path_cost}"
                    return

            except Exception as exc:
                self.utils.print_info(repr(exc))
                self.wait_till(timeout=step)
            finally:
                self.close_connection_with_error_handling(dut)
        else:
            pytest.fail("Failed to verify the path cost of port={port} on this dut\n{dut}")

    def revert_port_configuration_template_level(self, port_type):
        try:

            select_all_ports, _ = self.wait_till(
                func=self.setup_cls.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.all_ports_selected,
                silent_failure=True,
                exp_func_resp=True
            )

            assert select_all_ports, "Select all ports button was not found"
            self.utils.print_info("Select all ports button was found")

            self.wait_till(
                func=lambda: self.auto_actions.click(select_all_ports),
                exp_func_resp=True,
                delay=self.wait_till_click_delay
            )

            assign_to_all_ports_selected, _ = self.wait_till(
                func=
                self.setup_cls.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.assign_all_ports_selected,
                silent_failure=True,
                exp_func_resp=True,
                delay=self.wait_till_web_element_delay
            )

            assert assign_to_all_ports_selected, "Assign button was not found"
            self.utils.print_info("Assign Button was found")

            self.wait_till(
                func=lambda: self.auto_actions.click(assign_to_all_ports_selected),
                exp_func_resp=True,
                delay=self.wait_till_click_delay
            )

            assign_button, _ = self.wait_till(
                func=self.setup_cls.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_assign_choose_existing,
                silent_failure=True,
                exp_func_resp=True,
                delay=self.wait_till_web_element_delay
            )

            assert assign_button

            self.wait_till(
                func=lambda: self.auto_actions.click(assign_button),
                exp_func_resp=True,
                delay=self.wait_till_click_delay
            )

            radio_buttons, _ = self.wait_till(
                func=self.setup_cls.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_all_port_type_list_radio,
                silent_failure=True,
                exp_func_resp=True,
                timeout=40,
                delay=self.wait_till_web_element_delay
            )

            assert radio_buttons, "Radio buttons not found"

            radio_buttons_labels, _ = self.wait_till(
                func=self.setup_cls.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_all_port_type_list_label,
                silent_failure=True,
                exp_func_resp=True,
                delay=self.wait_till_web_element_delay

            )
            assert radio_buttons_labels, "Radio buttons labels not found"

            for btn, label in zip(radio_buttons, radio_buttons_labels):
                if label.text == port_type:
                    self.wait_till(
                        func=lambda: self.auto_actions.click(btn),
                        exp_func_resp=True,
                        delay=self.wait_till_click_delay
                    )
                    break
            else:
                assert False, "Failed to found the correct button for port type"

        finally:

            save_button, _ = self.wait_till(
                func=self.setup_cls.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_port_type_list_save_button,
                silent_failure=True,
                exp_func_resp=True,
                delay=self.wait_till_web_element_delay
            )

            assert save_button, "Save button was not found"
            self.wait_till(
                func=lambda: self.auto_actions.click(save_button),
                exp_func_resp=True
            )

            self.wait_till(timeout=5)

    def verify_path_cost_in_port_configuration_stp_tab(self, template_switch, network_policy, port, path_cost, slot=None):
        self.utils.print_info(f"Go to the port configuration of {template_switch} template")
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(
            network_policy, template_switch)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        required_slot = template_switch + "-" + slot
        self.navigate_to_slot_template(required_slot)
        self.click_on_stp_tab(level="template")

        found_path_cost_value = self.get_path_cost_value_from_stp_port_configuration_row(
            port, level="template")
        assert str(found_path_cost_value) == str(path_cost), \
            f"In XIQ port configuration: Expected path cost for port='{port}' is {path_cost} " \
            f"but found {found_path_cost_value}"

    def verify_path_cost_at_template_level(
            self, onboarded_switch, path_cost, template_switch,
            network_policy, default_path_cost="", revert_mode="revert_template",
            port_type="access", verify_delta_cli=False, revert_configuration=True,
            port_order_in_asic=None, ports=None, stp_mode="mstp", slot=None):

        dut = onboarded_switch

        if not default_path_cost:
            default_path_cost = "200000000" if onboarded_switch.cli_type.upper() == "VOSS" else "20000"

        if not ports:
            ports = self.get_one_port_from_each_asic_stack(
                dut=onboarded_switch, order=port_order_in_asic, slot=slot)
            print(f"THE PORTS ARE:{ports}")

        port_config = defaultdict(lambda: {})
        for port in ports:
            port_config[port]["port_type_name"] = self.generate_port_type_name()
            port_config[port]["path_cost"] = self.generate_random_path_cost() \
                if path_cost == "random" else path_cost
        self.utils.print_info(f"Port Type Configuration: {port_config}")

        self.utils.print_info(
            f"Go to the port configuration of '{template_switch}' template")
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(
            network_policy, template_switch, dut.cli_type)
        self.set_stp(enable=True)
        self.choose_stp_mode(mode=stp_mode)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        required_slot = template_switch + "-" + slot
        self.navigate_to_slot_template(required_slot)
        self.click_on_port_details_tab(level="template")

        try:
            try:
                for port, port_type_config in port_config.items():
                    self.utils.print_info(
                        f"Configuring port '{port}' with {port_type_config}")

                    try:
                        self.open_new_port_type_editor(port=port)
                        self.configure_port_name_usage_tab(
                            port_type_name=port_type_config["port_type_name"],
                            port_type=port_type
                        )
                        self.go_to_stp_settings_tab_in_honeycomb()
                        self.verify_path_cost_field_is_editable()
                        self.configure_stp_settings_tab_in_honeycomb(
                            stp_enabled=True,
                            edge_port=True,
                            bpdu_protection="Disabled",
                            path_cost=port_type_config["path_cost"],
                            priority=64
                        )
                        self.go_to_last_page()

                        expected_summary = {
                            'STP': 'Enabled',
                            'Edge Port': 'Enabled',
                            'BPDU Protection': 'Disabled',
                            'Priority': '64',
                            'Path Cost': str(port_type_config["path_cost"])
                        }
                        self.utils.print_info(
                            f"Expected summary: {expected_summary}")

                        summary = self.get_stp_settings_summary()
                        self.utils.print_info(f"Found summary: {summary}")

                        self.utils.print_info(
                            "Verify that the configured fields"
                            " appear correctly in the summary tab"
                        )
                        assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                            f"Not all the values of the summary are the expected ones. " \
                            f"Expected summary: {expected_summary}\nFound summary: {summary}"
                        self.utils.print_info(
                            "Successfully verified the summary")

                    finally:
                        self.save_port_type_config()
            finally:
                self.save_template_config()

            self.utils.print_info(f"Go to the port configuration of {template_switch} template")
            self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(
                network_policy, template_switch, dut.cli_type)
            self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            required_slot = template_switch + "-" + slot
            self.navigate_to_slot_template(required_slot)
            self.click_on_stp_tab(level="template")
            for port, port_type_config in port_config.items():
                self.utils.print_info(
                    f"Verifying STP tab for port {port}: {port_type_config}")
                self.verify_path_cost_in_port_configuration_stp_tab(template_switch, network_policy, port,
                    port_type_config["path_cost"], slot=slot
                )

            if verify_delta_cli:
                commands = []
                if onboarded_switch.cli_type.upper() == "EXOS":

                    for port, port_type_config in port_config.items():
                        commands.append(
                            f"configure stpd s0 ports cost {port_type_config['path_cost']} {port}")

                elif onboarded_switch.cli_type.upper() == "VOSS":
                    commands.extend(
                        [
                            "enable",
                            "configure terminal"
                        ]
                    )

                    for port, port_type_config in port_config.items():
                        commands.extend(
                            [
                                f"interface gigabitEthernet {port}",
                                f"spanning-tree {stp_mode} cost {port_type_config['path_cost']}"
                            ]
                        )

                elif onboarded_switch.cli_type.upper() == "AH-FASTPATH":
                    commands.extend(
                        [
                            "enable",
                            "configure"
                        ]
                    )
                    for port, port_type_config in port_config.items():
                        commands.extend(
                            [
                                f"interface {port}",
                                f"spanning-tree cost {port_type_config['path_cost']}"
                            ]
                        )

                self.verify_delta_cli_commands(
                    onboarded_switch, commands=commands)

            self.update_and_wait_switch(
                policy_name=network_policy, dut=onboarded_switch)

            for port, port_type_config in port_config.items():
                self.utils.print_info(
                    f"Verifying path cost for port {port} on dut:"
                    f" {port_type_config}"
                )
                self.verify_path_cost_on_dut(
                    onboarded_switch,
                    expected_path_cost=port_type_config["path_cost"],
                    port=port,
                    mode=stp_mode
                )

        finally:

            if revert_configuration:
                try:
                    self.utils.print_info(
                        f"Go to the port configuration of"
                        f" '{template_switch} 'template"
                    )
                    self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(
                        network_policy, template_switch, dut.cli_type)
                    self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                    self.navigate_to_slot_template(required_slot)
                    self.click_on_port_details_tab(level="template")

                    if revert_mode == "revert_template":
                        self.revert_port_configuration_template_level(
                            "Auto-sense Port" if onboarded_switch.cli_type.upper() == "VOSS" else "Access Port")
                    elif revert_mode == "edit_honeycomb_with_empty_path_cost":

                        for port, port_type_config in port_config.items():
                            _, summary = self.xiq.xflowsmanageDevice360.edit_stp_settings_in_honeycomb_port_editor(
                                port,
                                port_type_name=port_type_config["port_type_name"],
                                path_cost=""
                            )
                            assert summary["Path Cost"] == "", \
                                "Failed to edit the Path Cost"
                            self.utils.print_info(
                                "Successfully edited the Path Cost")

                finally:

                    self.save_template_config()
                    self.utils.print_info(
                        "Saved the port type configuration, "
                        "now push the changes to the dut")

                    self.update_and_wait_switch(
                        policy_name=network_policy,
                        dut=onboarded_switch
                    )

                    for port in port_config:
                        self.verify_path_cost_on_dut(
                            onboarded_switch,
                            expected_path_cost=default_path_cost,
                            port=port,
                            mode=stp_mode
                        )

                    for port_info in port_config.values():
                        port_type_name = port_info['port_type_name']
                        try:
                            self.utils.print_info(f"Delete port type profile: {port_type_name}")
                            self.xiq.xflowsconfigureCommonObjects.delete_port_type_profile(
                                port_type_name)
                        except Exception as exc:
                            self.utils.print_info(repr(exc))

    def set_path_cost_in_honeycomb(self, path_cost):
        path_cost_element, _ = self.wait_till(
            func=lambda: self.dev360.get_select_element_port_type("path cost"),
            exp_func_resp=True,
            silent_failure=True,
            delay=self.wait_till_web_element_delay
        )

        assert path_cost_element, "Path Cost element was not found"

        self.wait_till(
            func=lambda: self.auto_actions.send_keys(path_cost_element, str(path_cost)),
            exp_func_resp=True,
            delay=self.wait_till_send_keys_delay
        )
        self.utils.print_info("Successfully configured the path cost field")
        self.wait_till(timeout=5)

    def verify_port_type_editor_still_in_stp_tab(self):
        stp_tab, _ = self.wait_till(
            func=lambda: self.dev360.get_select_element_port_type("stpPage"),
            exp_func_resp=True,
            delay=self.wait_till_web_element_delay
        )
        assert "active" in stp_tab.get_attribute("class")

    def set_stp(self, enable=True):
        button, _ = self.wait_till(
            func=self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_enable_spanningtree,
            exp_func_resp=True,
            silent_failure=True,
            delay=self.wait_till_web_element_delay
        )

        if (not button.is_selected() and enable) or (
                button.is_selected() and not enable):
            self.wait_till(
                func=lambda: self.auto_actions.click(button),
                exp_func_resp=True,
                delay=self.wait_till_click_delay
            )

    def choose_stp_mode(self, mode):
        if mode == "stp":
            button, _ = self.wait_till(
                func=self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_enable_stp,
                exp_func_resp=True,
                silent_failure=True,
                delay=self.wait_till_web_element_delay
            )

        elif mode == "rstp":
            button, _ = self.wait_till(
                func=self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_enable_rstp,
                exp_func_resp=True,
                silent_failure=True,
                delay=self.wait_till_web_element_delay
            )

        elif mode == "mstp":
            button, _ = self.wait_till(
                func=self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_enable_mstp,
                exp_func_resp=True,
                silent_failure=True,
                delay=self.wait_till_web_element_delay
            )

        assert button, f"Failed to get the {mode} stp mode button"
        self.wait_till(
            func=lambda: self.auto_actions.click(button),
            exp_func_resp=True,
            delay=self.wait_till_click_delay
        )

    def connect_to_network_element(self, dut):
        try:
            self.setup_cls.network_manager.connect_to_network_element_name(dut.name)
        except Exception as exc:
            if pytest.default_device_password:
                self.setup_cls.network_manager.connect_to_network_element(
                    net_elem_name=dut.name, ip=dut.ip, username=dut.username, connection_method=dut.connection_method,
                    device_cli_type=dut.cli_type, password=pytest.default_device_password
                )
            else:
                raise exc

    def generate_random_path_cost(self, rng=range(1, 200000000)):
        return str(random.choice(rng))

    def reboot_dut(self, dut):

        try:
            self.close_connection_with_error_handling(dut)
            self.connect_to_network_element(dut)
            if dut.cli_type.upper() == "EXOS":
                self.setup_cls.devCmd.send_cmd(dut.name, 'reboot all', max_wait=10, interval=2,
                                     confirmation_phrases='Are you sure you want to reboot the switch?',
                                     confirmation_args='y'
                                     )
            elif dut.cli_type.upper() == "VOSS":
                self.setup_cls.devCmd.send_cmd(dut.name, 'reset -y', max_wait=10, interval=2)
            elif dut.cli_type.upper() == "AH-FASTPATH":
                try:
                    self.setup_cls.devCmd.send_cmd(dut.name, "enable")
                except:
                    self.setup_cls.devCmd.send_cmd(dut.name, "exit")

                self.setup_cls.devCmd.send_cmd(
                    dut.name, 'reload', max_wait=10, interval=2,
                    confirmation_phrases='Would you like to save them now? (y/n)', confirmation_args='y'
                )
        except:
            pass
        else:
            self.utils.wait_till(timeout=120)
        finally:
            self.close_connection_with_error_handling(dut)

    def get_one_port_from_each_asic_stack(self, dut, order, slot):

        self.wait_till(timeout=10)
        self.xiq.xflowscommonDevices._goto_devices()
        self.wait_till(timeout=10)

        try:
            self.wait_till(timeout=5)
            self.setup_cls.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
            self.wait_till(timeout=5)

            return self.dev360.get_one_port_from_each_asic_stack(order=order, slot=slot)

        finally:
            self.wait_till(timeout=5)
            self.xiq.xflowsmanageDevice360.close_device360_window()
            self.wait_till(timeout=5)

    def navigate_to_slot_template(self, slot):
        """
        This keyword is navigate to template stack ${slot}.
        """
        try:
            template_slot = self.setup_cls.switch_template_web_elements.get_template_slot(slot=slot)
            AutoActions().click(template_slot)
            self.wait_till(timeout=5)
        except Exception as e:
            print(f"Error Exception: {e}")
            return -1
        return 1

    def verify_path_cost_edit_summary(self, template_switch, network_policy, dut, order, slot=None):
        """
        This Keyword verifies that path cost is correct in Edit Type Port Summary
        """
        ports = self.get_one_port_from_each_asic_stack(dut=dut, order=order, slot=slot)
        port_config = defaultdict(lambda: {})
        for port in ports:
            port_config[port]["port_type_name"] = self.generate_port_type_name()
            port_config[port]["path_cost"] = self.generate_random_path_cost()
        self.utils.print_info(f"Port Type Configuration: {port_config}")

        self.utils.print_info(f"Go to the port configuration of '{template_switch}' template")
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(network_policy, template_switch, dut.cli_type)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        required_slot = template_switch + "-" + slot
        self.navigate_to_slot_template(required_slot)
        self.click_on_port_details_tab()

        for port, port_info in port_config.items():
            port_type_name = port_info["port_type_name"]
            path_cost = port_info["path_cost"]
            self.utils.print_info(
                f"Create a new port type '{port_type_name}' with path cost '{path_cost}' for port '{port}'")

            expected_summary = {
                'STP': 'Enabled',
                'Edge Port': 'Enabled',
                'BPDU Protection': 'Disabled',
                'Priority': '64',
                'Path Cost': path_cost
            }
            self.utils.print_info(f"Expected summary: {expected_summary}")

            _, create_port_type_summary = self.xiq.xflowsmanageDevice360.create_port_type_with_stp_settings(
                port, port_type_name=port_type_name, path_cost=path_cost, description="description", status=True,
                port_usage="access", priority=64, bpdu_protection="Disabled", stp_enabled=True, edge_port=True)
            self.utils.print_info(
                f"Summary from create port type in honeycom (port {port}): {create_port_type_summary}")

            self.utils.print_info(
                f"Verify that the configured fields appear correctly in the summary tab (port {port})")
            assert all(expected_summary[k] == create_port_type_summary[k] for k in expected_summary), \
                f"Not all the values of the summary are the expected ones (port {port}). " \
                f"Expected summary: {expected_summary}\nFound summary: {create_port_type_summary}"
            self.utils.print_info(
                f"Successfully verified the summary at port type creation in honeycomb (port {port})")

            self.utils.wait_till(timeout=10)
            _, edit_port_type_summary = self.xiq.xflowsmanageDevice360.edit_stp_settings_in_honeycomb_port_editor(
                    port, port_type_name)
            self.utils.print_info(
                f"Summary from edit port type in honeycomb (port {port}): {create_port_type_summary}")

            self.utils.print_info(
                f"Verify that the configured fields appear correctly in the summary tab (port {port})")
            assert all(expected_summary[k] == edit_port_type_summary[k] for k in expected_summary), \
                f"Not all the values of the summary are the expected ones (port {port}). " \
                f"Expected summary: {expected_summary}\nFound summary: {edit_port_type_summary}"
            self.utils.print_info(
                f"Successfully verified the summary at port type edit in honeycomb (port {port})")

    def verify_path_cost_wrong_value(self, template_switch, network_policy, dut, order, slot):
        """
         This Keyword verifies a wrong value for path cost is not admitted
         """
        wrong_values = [-1, 200000001, "#", "b"]
        ports = self.get_one_port_from_each_asic_stack(dut=dut, order=order, slot=slot)
        port_type_name = self.generate_port_type_name()

        self.utils.print_info(
            f"Go to the port configuration of '{template_switch}' template")
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(
            network_policy, template_switch, dut.cli_type)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        required_slot = template_switch + "-" + slot
        self.navigate_to_slot_template(required_slot)
        self.click_on_port_details_tab()

        for port in ports:
            self.utils.print_info(
                f"Verifying that the wrong values ('{wrong_values}') cannot be"
                f"set as path cost in honeycomb port editor for port '{port}'"
            )

            try:
                self.open_new_port_type_editor(port=port)
                self.configure_port_name_usage_tab(
                    port_type_name=port_type_name,
                    port_type="access"
                )
                self.go_to_stp_settings_tab_in_honeycomb()

                for value in wrong_values:

                    self.utils.print_info(
                        f"Try to set '{value}' as path_cost for port '{port}'")
                    self.set_path_cost_in_honeycomb(value)
                    self.go_to_next_editor_tab()

                    try:
                        self.verify_port_type_editor_still_in_stp_tab()

                    except AssertionError as err:
                        msg = f"Failed! Expected the honeycomb editor to " \
                              f"still be in the STP tab after " \
                              f"clicking NEXT TAB when path_cost='{value}'"
                        self.utils.print_info(msg)
                        self.utils.print_info(repr(err))
                        pytest.fail(msg)

                self.utils.print_info(
                    f"Successfully verified that these values cannot be set"
                    f" (port '{port}'): '{wrong_values}'"
                )
            finally:
                self.close_port_type_config()

    def check_stp_path_cost_column(self):
        """
        This keyword checks if STP path cost column exists for each port in Device Template.
        Go to Device Template -> Port Configuration is needed before this function.
        """
        self.wait_till(timeout=2)
        self.click_on_stp_tab(level="template")
        rows = self.get_stp_port_configuration_rows(level="template")

        for index, row in enumerate(rows):
            path_cost_element, _ = self.utils.wait_till(
                func=lambda:
                self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_path_cost_row(row),
                silent_failure=True,
                exp_func_resp=True,
                delay=1
            )

            assert path_cost_element, \
                f"Did not find the path cost element for this row:" \
                f" '{row.text}' (row index: {index})"
            self.utils.print_info(
                f"Successfully found the path cost element (it has "
                f"value='{path_cost_element.get_attribute('value')}') "
                f"for the row with index: {index}")

        self.utils.print_info(
            "Successfully verified that the path cost element is contained"
            "in every row of the STP port configuration table"
        )

    def check_default_stp_path_cost(self):
        """
        This keyword checks if default STP path cost (empty value) exists for each port in Device Template.
        Go to Device Template -> Port Configuration is needed before this function.
        """
        self.wait_till(timeout=2)
        self.click_on_stp_tab(level="template")
        rows = self.get_stp_port_configuration_rows(level="template")

        results = defaultdict(lambda: {"msg": "", "status": False})

        for row in rows:
            port_match = re.search(r"^(.*)\n", row.text)
            assert port_match, f"Failed to get the port from '{row.text}'"
            port = port_match.group(1)

            path_cost_element, _ = self.utils.wait_till(
                func=lambda:
                self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_path_cost_row(row),
                exp_func_resp=True,
                delay=1
            )

            path_cost_value = path_cost_element.get_attribute("value")
            results[port]["status"] = path_cost_value == ""
            results[port]["msg"] = f"Expected the path cost value to be '' but found '{path_cost_value}'" \
                                   f" for row with port='{port}'" if path_cost_value != "" else \
                f"Successfully verified the default value of path cost for row with port={port}"

        for port, data in {port: data for port, data in results.items() if data["status"] is True}.items():
            self.utils.print_info(data["msg"])

        failed_verifications = {port: data for port, data in results.items() if data["status"] is False}

        if failed_verifications:
            for port, data in failed_verifications.items():
                self.utils.print_error(data["msg"])
            pytest.fail("\n".join(list(data["msg"] for data in failed_verifications.values())))

        self.utils.print_info("Successfully verified that the default path cost values are '' at template level")

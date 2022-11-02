
import pytest
from time import sleep
import random

from ..Resources.testcase_base import xiqBase


class TCXM20608Tests(xiqBase):
    @pytest.mark.development
    @pytest.mark.testbed_standalone
    @pytest.mark.xim_tcxm_20608
    @pytest.mark.p1
    def test_vim_negative_sw_template_assign_button(self, onboarded_dut, network_policy, template_switch):
        """
        Author        : scostache
        TCXM-20608    : https://aerohive.qtestnet.com/p/101323/portal/project#tab=testdesign&object=1&id=55067625
        Description   : Verify that LACP cannot be formed between VIM and fixed panel ports using Assign button from
        Switch Template.
         0	Use devices with 4 ports VIM module (10 or 25 G ports) and aggregate them according to tests requirements.
        Supported devices: 5520-24T, 5520-24W, 5520-48T, 5520-48W, 5520-12MW-36W, 5520-24X, 5520-48SE, 5520-VIM-4X,
        5520-VIM-4XE
        , 5520-VIM-4YE.
        Tested EXOS devices: 5520-48SE with 5520-VIM-4XE, 5520-24W with 5520-VIM-4X, 5520-24T with 5520-VIM-4YE.
         1	Onboard the EXOS 5520 standalone.
        Device is onboarded successfully.
         2	Create a Network Policy with specific 5520 template.
        Network Policy is created successfully.
         3	Using the Assign button from Switch Template -> Port configuration aggregate 1 VIM port and
                                        1 fixed panel port

        * If the fixed panel port is Ethernet type the following error is received:
            You cannot aggregate Ethernet ports with SFP ports.
        * If the fixed panel port is SFP type the following error is received:
            Only VIM ports within the same VIM can be part of the same LAG.
        """
        self.xiq.Utils.print_info("---------TEST_TCXM_20608---------")

        self.executionHelper.testSkipCheck()
        dut = onboarded_dut
        device_mac = dut.mac

        try:
            self.xiq.xflowscommonNavigator.navigate_to_device360_page_with_mac(device_mac)
            sleep(5)

            if not self.xiq.xflowsmanageDevice360.d360_check_if_vim_is_installed():
                self.xiq.Utils.print_info("Warning: no actual VIM module installed")
                wireframe_port_list = self.xiq.xflowsmanageDevice360.get_device360_wireframe_port()
                # VIM ports are the last 4 ports
                tmp_len = len(wireframe_port_list)
                vim_port = wireframe_port_list[random.randint(tmp_len-4, tmp_len-1)].text
                if vim_port == -1:
                    pytest.fail("Can't retrieve VIM port")
            else:
                vim_port = self.xiq.xflowsmanageDevice360.d360_return_vim_port_number()
                vim_port = str(random.randint(int(vim_port), int(vim_port) + 3))
                if vim_port == -1:
                    pytest.fail("Can't retrieve VIM port")

            self.xiq.Utils.print_info("------Test Ports------")
            self.xiq.Utils.print_info("Use VIM SFP Port:  " + vim_port)

            wireframe_port_list = self.xiq.xflowsmanageDevice360.get_device360_wireframe_ether_port()
            tmp_len = len(wireframe_port_list)
            wireframe_port = wireframe_port_list[random.randint(0, tmp_len-1)].text

            self.xiq.Utils.print_info("Use Ethernet Port: " + wireframe_port)

            sfp28_port_list = self.xiq.xflowsmanageDevice360.get_device360_wireframe_sfp28_port()
            sfp28_port_list_len = len(sfp28_port_list)
            if sfp28_port_list_len == 0:
                sfp_port = None
            else:
                # SFP port text is U#number, so consider SFP port number is last-ether-port + random int between 1
                # and length of sfp port_list
                sfp_port = str(int(wireframe_port_list[tmp_len-1].text) + random.randint(1, sfp28_port_list_len))

            self.xiq.Utils.print_info("Use Fiber Port:    " + sfp_port)
            self.xiq.Utils.print_info("------Test Ports------")
            self.xiq.xflowsmanageDevice360.close_device360_window()
            sleep(1)

            self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(network_policy, template_switch)
            sleep(1)
            self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            sleep(2)

            self.xiq.Utils.print_info("-------------------------------------------------------------")
            self.xiq.Utils.print_info("First add a VIM port in LAG, then try to add an Ethernet port")
            self.xiq.Utils.print_info("then try to add an universal SFP port")
            self.xiq.Utils.print_info("------------------------------")
            # First add a VIM port and then try to add the Ethernet Port and then try adding the Fiber Port
            self.auto_actions.click(
                self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_assign_button())
            sleep(1)
            element = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.\
                get_sw_template_assign_advanced_actions()
            self.auto_actions.move_to_element(element)
            element = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.\
                get_sw_template_assign_advanced_actions_aggr()
            self.auto_actions.move_to_element(element)
            self.auto_actions.click(element)
            sleep(1)

            # Add VIM port
            element = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_available_port(vim_port)
            if element is None:
                self.xiq.Utils.print_info("Couldn't get vim port, exit")
                pytest.fail("port get error")
            self.auto_actions.click(element)
            self.auto_actions.click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                                    get_lag_add_port_button())
            sleep(1)

            # check port in agg list
            element = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_selected_port(vim_port)
            if element is None:
                self.xiq.Utils.print_info("selected vim port not found, exit")
                pytest.fail("port error")

            # Try to add a wireframe copper port
            element = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_available_port(wireframe_port)
            if element is None:
                self.xiq.Utils.print_info("Couldn't get copper port, exit")
                pytest.fail("port get error")
            self.auto_actions.click(element)
            self.auto_actions.click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                                    get_lag_add_port_button())
            sleep(1)

            # check port in agg list
            element = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_selected_port(wireframe_port)
            if element is not None:
                self.xiq.Utils.print_info("selected copper port is found, exit")
                pytest.fail("port error")

            tool_tip_text = ""
            tip_box_error = self.xiq.xflowsconfigureCommonObjects.cobj_web_elements.get_ui_tipbox_error()
            if tip_box_error:
                tool_tip_text = tip_box_error.text
            retry = 0
            while retry < 15:
                if "You cannot aggregate Ethernet ports with SFP ports." in tool_tip_text:
                    self.xiq.Utils.print_info("Negative Scenario Validated, Error Received. \n "
                                              "Tool tip Text Displayed on Page: ", tool_tip_text)
                    break
                self.xiq.Utils.print_info(
                        f"Tool tip for port aggr error not found in {tool_tip_text}, retry: {retry} ")
                sleep(1)
                tip_box_error = self.xiq.xflowsconfigureCommonObjects.cobj_web_elements.get_ui_tipbox_error()
                if tip_box_error:
                    tool_tip_text = tip_box_error.text
                retry += 1

            if retry >= 15:
                self.xiq.Utils.print_info("Tool tip for port aggr error not found in: ", tool_tip_text)
                pytest.fail("Tool tip for port aggr error not found")

            self.auto_actions.click(self.xiq.xflowscommonGlobalSearch.global_web_elements.
                                    get_tool_tip_error_close_button())

            # Try to add an SFP port
            if sfp_port is not None:
                element = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_available_port(sfp_port)
                if element is None:
                    self.xiq.Utils.print_info("Couldn't get fiber port, exit")
                    pytest.fail("port get error")
                self.auto_actions.click(element)
                self.auto_actions.click(
                    self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_lag_add_port_button())
                sleep(1)

                # check port in agg list
                element = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_selected_port(sfp_port)
                if element is not None:
                    self.xiq.Utils.print_info("selected fiber port is found, exit")
                    pytest.fail("port error")

                tool_tip_text = ""
                tip_box_error = self.xiq.xflowsconfigureCommonObjects.cobj_web_elements.get_ui_tipbox_error()
                if tip_box_error:
                    tool_tip_text = tip_box_error.text
                retry = 0
                while retry < 15:
                    sleep(1)
                    if "Only VIM ports within the same VIM can be part of the same LAG" in tool_tip_text:
                        self.xiq.Utils.print_info("Negative Scenario Validated, Error Received. \n "
                                                  "Tool tip Text Displayed on Page: ", tool_tip_text)
                        break
                    self.xiq.Utils.print_info(
                            f"Tool tip for port aggr error not found in {tool_tip_text}, retry: {retry} ")
                    sleep(1)
                    tip_box_error = self.xiq.xflowsconfigureCommonObjects.cobj_web_elements.get_ui_tipbox_error()
                    if tip_box_error:
                        tool_tip_text = tip_box_error.text
                    retry += 1

                if retry >= 15:
                    self.xiq.Utils.print_info("Tool tip for port aggr error not found in: ",
                                              tool_tip_text)
                    pytest.fail("Tool tip for port aggr error not found")

                self.auto_actions.click(self.xiq.xflowscommonGlobalSearch.global_web_elements.
                                        get_tool_tip_error_close_button())

            self.xiq.Utils.print_info("Close Assign Aggregate Ports Window")
            self.auto_actions.click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                                    get_cancel_button())
            sleep(1)

            self.xiq.Utils.print_info("-------------------------------------------------------------")
            self.xiq.Utils.print_info("Try again, different order: First Wired Copper Port, then VIM")
            self.xiq.Utils.print_info("------------------------------")
            self.auto_actions.click(
                self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_assign_button())
            sleep(1)
            element = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.\
                get_sw_template_assign_advanced_actions()
            self.auto_actions.move_to_element(element)
            element = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.\
                get_sw_template_assign_advanced_actions_aggr()
            self.auto_actions.move_to_element(element)
            self.auto_actions.click(element)
            sleep(1)
            # Try to add a wireframe copper port
            element = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_available_port(wireframe_port)
            if element is None:
                self.xiq.Utils.print_info("Couldn't get copper port, exit")
                pytest.fail("port get error")
            self.auto_actions.click(element)
            self.auto_actions.click(
                self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_lag_add_port_button())
            sleep(1)

            # check port in agg list
            element = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_selected_port(wireframe_port)
            if element is None:
                self.xiq.Utils.print_info("selected copper port is not found, exit")
                pytest.fail("port error")

            # Add VIM port
            element = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_available_port(vim_port)
            if element is None:
                self.xiq.Utils.print_info("Couldn't get vim port, exit")
                pytest.fail("port get error")
            self.auto_actions.click(element)
            self.auto_actions.click(
                self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_lag_add_port_button())
            sleep(1)

            # check port in agg list
            element = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_selected_port(vim_port)
            if element is not None:
                self.xiq.Utils.print_info("selected vim port is found, exit")
                pytest.fail("port error")

            tool_tip_text = ""
            tip_box_error = self.xiq.xflowsconfigureCommonObjects.cobj_web_elements.get_ui_tipbox_error()
            if tip_box_error:
                tool_tip_text = tip_box_error.text
            retry = 0
            while retry < 15:
                if "You cannot aggregate Ethernet ports with SFP ports." in tool_tip_text:
                    self.xiq.Utils.print_info("Negative Scenario Validated, Error Received. \n "
                                              "Tool tip Text Displayed on Page: ", tool_tip_text)
                    break
                self.xiq.Utils.print_info(
                        f"Tool tip for port aggr error not found in {tool_tip_text}, retry: {retry} ")
                sleep(1)
                tip_box_error = self.xiq.xflowsconfigureCommonObjects.cobj_web_elements.get_ui_tipbox_error()
                if tip_box_error:
                    tool_tip_text = tip_box_error.text
                retry += 1

            if retry >= 15:
                self.xiq.Utils.print_info("Tool tip for port aggr error not found in: ",
                                          tool_tip_text)
                pytest.fail("Tool tip for port aggr error not found")

            self.auto_actions.click(
                self.xiq.xflowscommonGlobalSearch.global_web_elements.get_tool_tip_error_close_button())
            self.xiq.Utils.print_info("Close Assign Aggregate Ports Window")
            self.auto_actions.click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                                    get_cancel_button())
            sleep(1)
        finally:
            self.xiq.xflowscommonNavigator.navigate_to_devices()
            self.xiq.Utils.print_info("-------END TEST_TCXM_20608-------")

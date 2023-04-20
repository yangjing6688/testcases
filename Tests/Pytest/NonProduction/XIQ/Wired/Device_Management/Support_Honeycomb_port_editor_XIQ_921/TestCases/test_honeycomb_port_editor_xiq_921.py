import pytest
import random
import string
import time
def random_word(x=12):
    randword = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(x))
    return randword

@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.testbed_stack
@pytest.mark.EXOS
@pytest.mark.VOSS
@pytest.mark.testbed_1_node
class Xiq921Tests:

    def verify_poe_supported(self,node):
        flag_poe = False
        poe_index = ['P', 'U', 'W']
        for el in poe_index:
            if el in node.model:
                flag_poe = True
        if not flag_poe:
            pytest.skip("No poe support")

    def get_random_name(self, base_string):
        random_value = base_string + "_" + random_word(x=6)
        return random_value

    def get_delete_port_type(self, xiq_library_at_class_level, port_type_name):
        xiq_library_at_class_level.xflowsconfigureCommonObjects.delete_port_type_profile(port_type_name)

    def check_ports_existence(self, check_port_voss, check_port_exos, os, xiq_library_at_class_level, node, dev_cmd, network_manager):
        network_manager.connect_to_network_element_name(node.name)
        if os == "voss":
            system_type_regex = "(\\d+/\\d+)\\s+\\w+"
            output = dev_cmd.send_cmd(node.name, 'show ports vlan')[0].cmd_obj._return_text
            network_manager.close_connection_to_network_element(node.name)
            all_ports = xiq_library_at_class_level.Utils.get_regexp_matches(output, system_type_regex, 1)
            print("Found the ports: ", all_ports)
            for elem in all_ports:
                if check_port_voss == elem:
                    return elem
            if len(all_ports) > 3:
                return all_ports[1]
            else:
                return '1/2'
        if os == "exos":
            system_type_regex = "(\\d+)\\s+\\w+"
            output = dev_cmd.send_cmd(node.name, 'show ports vlan')[0].cmd_obj._return_text
            network_manager.close_connection_to_network_element(node.name)
            all_ports = xiq_library_at_class_level.Utils.get_regexp_matches(output, system_type_regex, 1)
            print("Found the ports: ", all_ports)
            for elem in all_ports:
                if check_port_exos == elem:
                    flag_port_found = True
                    if node.platform.lower() == 'stack':
                        return '1:' + elem
                    return elem
            if len(all_ports) > 3:
                return all_ports[1]
            else:
                if node.platform.lower() == 'stack':
                    return '1:2'
                return '2'

    def delete_port_type_local(self, node, xiq_library_at_class_level,  delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name):
        if node.cli_type.lower() == 'voss' and delete_port_type:
            self.get_delete_port_type(xiq_library_at_class_level, port_type_voss_auto_sense_off_name)
        elif node.cli_type.lower() == 'exos' and delete_port_type:
            self.get_delete_port_type(xiq_library_at_class_level, port_type_exos_name)

    def configure_port_type_local(self, xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos, voss_port, exos_port,
                                  policy_name=None, device_template_name=None, d360=True):
        delete_port_type = False
        create_new_port_type_and_check_summary = -1
        time.sleep(10)
        if d360:
            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices() == 1:
                pytest.fail("Fail on navigating to devices")

            xiq_library_at_class_level.xflowsmanageDevices.refresh_devices_page()
            # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
            time.sleep(10)

            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_device360_page_with_mac(node.mac) == 1:
                pytest.fail("Fail on navigating to D360 view with MAC")
            # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
            time.sleep(10)
            if not xiq_library_at_class_level.xflowscommonNavigator.navigate_to_port_configuration_d360() == 1:
                pytest.fail("Fail on navigating to Port Config")
            time.sleep(10)
            if node.cli_type.lower() == 'voss':
                create_new_port_type_and_check_summary = xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(
                    template_voss_auto_sense_off, voss_port, d360=d360)

            elif node.cli_type.lower() == 'exos':
                if node.platform.lower() == 'stack':
                    xiq_library_at_class_level.xflowsmanageDevice360.select_stack_unit(1)
                time.sleep(10)
                create_new_port_type_and_check_summary = xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(
                    template_exos, exos_port, d360=d360)

            if not create_new_port_type_and_check_summary == 1:
                print("Result is: ", create_new_port_type_and_check_summary)
                pytest.fail("Fail on Creating Port Type template")
            else:
                print("Result is: ", create_new_port_type_and_check_summary)
                print("Port Type template was created on device.")
                delete_port_type = True

        else:
            print("***Selecting SW template ", device_template_name)
            time.sleep(10)
            select_template = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(policy_name, device_template_name, node.cli_type)
            if select_template != 1:
                pytest.fail("Could not select switch template ", device_template_name)

            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            time.sleep(10)
            if node.cli_type.lower() == 'voss':
                create_new_port_type_and_check_summary = xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(
                    template_voss_auto_sense_off, voss_port.split('/')[1], d360=d360)
            elif node.cli_type.lower() == 'exos':
                create_new_port_type_and_check_summary = xiq_library_at_class_level.xflowsmanageDevice360.create_new_port_type(
                    template_exos, exos_port, d360=d360)

            if not create_new_port_type_and_check_summary == 1:
                print("Result is: ", create_new_port_type_and_check_summary)
                pytest.fail("Fail on Creating Port Type template")
            else:
                print("Result is: ", create_new_port_type_and_check_summary)
                print("Port Type template was created on device.")
                delete_port_type = True

        return delete_port_type

    def edit_port_type_local(self, node, xiq_library_at_class_level, template_voss, template_exos, voss_port, exos_port):
        delete_port_type = False
        create_new_port_type_and_check_summary = -1
        # Edit Port Type and check summary
        time.sleep(10)
        if node.cli_type.lower() == 'voss':
            create_new_port_type_and_check_summary = xiq_library_at_class_level.xflowsmanageDevice360.edit_port_type(template_voss,
                                                                                                   voss_port)
        elif node.cli_type.lower() == 'exos':
            create_new_port_type_and_check_summary = xiq_library_at_class_level.xflowsmanageDevice360.edit_port_type(template_exos,
                                                                                                   exos_port)
        time.sleep(10)
        if not create_new_port_type_and_check_summary == 1:
            print("Result is: ", create_new_port_type_and_check_summary)
            pytest.fail("Fail on Editing Port Type template")
        else:
            print("Result is: ", create_new_port_type_and_check_summary)
            print("Port Type template was created on device.")
            delete_port_type = True
        return delete_port_type

    @pytest.mark.p2
    @pytest.mark.tcxm_18417
    def test_tcxm_18417(self, node, xiq_library_at_class_level, dev_cmd, network_manager):
        '''
        TCXM-18417 - D360 View - Add Port Name&Usage Configuration in Create Port Type tab for U100 device and check
         config Summary tab.
        '''
        voss_port_check = ''
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        elif node.platform.lower == 'voss':
            voss_port_check = "1/2"
        else:
            exos_port_check = "6"
        #
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )
        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': ["port_type_description", "port_type_description"],
            'status': ['click', 'off'],
            'auto-sense': ['click', None],
            'port usage': ['trunk port', 'trunk'],

            'page2 trunkVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 pseSettings': ["next_page", None],

            'page7 summary': ["next_page", None]
        }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': ["port_type_description", "port_type_description"],
                         'status': [None, 'on'],
                         'port usage': ['trunk port', 'trunk'],

                         'page2 trunkVlanPage': ["next_page", None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, d360=True)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @pytest.mark.p2
    @pytest.mark.tcxm_18420
    def test_tcxm_18420(self, node, xiq_library_at_class_level, dev_cmd, network_manager):
        """	 TCXM-18420 - D360 View - Add Vlan in VLAN tab for U100 device and check config Summary tab.
            TCXM-18422 - D360 View - Add Vlan in VLAN tab for U100 stack and check config Summary tab."""

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],
            'vlan': ['50', '50'],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 pseSettings': ["next_page", None],

            'page7 summary': ["next_page", None]
            }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 accessVlanPage': ["next_page", None],
                         'vlan': ['30', '30'],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, d360=True)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @pytest.mark.p1
    @pytest.mark.tcxm_18423
    def test_tcxm_18423(self, node, xiq_library_at_class_level, dev_cmd, network_manager):
        """	 TCXM-18423 - D360 View - Add Transmission Settings in Create Port Type tab for U100 device and check
        config Summary tab.
        TCXM-18425 - D360 View - Add Transmission Settings in Create Port Type tab for U100 stack and check
        config Summary tab."""

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],
            'transmission type': ['Full-Duplex', 'Full-Duplex'],
            'transmission speed': ['100 Mbps', '100'],
            'cdp receive': [None, 'off'],
            'lldp transmit': ['click', 'off'],
            'lldp receive': [None, 'off'],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 pseSettings': ["next_page", None],

            'page7 summary': ["next_page", None]
            }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'Access'],

                         'page2 accessVlanPage': ['next_page', None],

                         'page3 transmissionSettings': ["next_page", None],
                         'transmission type': ['Full-Duplex', 'Full-Duplex'],
                         'transmission speed': ['100 Mbps', '100'],
                         'cdp receive': ['click', 'on'],
                         'lldp transmit': ['click', 'off'],
                         'lldp receive': ['click', 'off'],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, d360=True)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @pytest.mark.tcxm_18426
    @pytest.mark.p1
    def test_tcxm_18426(self, node, xiq_library_at_class_level, dev_cmd, network_manager):
        """	 TCXM-18426 - D360 View - Add STP Settings in Create Port Type tab for U100 device and check config Summary tab.
            TCXM-18428 - D360 View - Add STP Settings in Create Port Type tab for U100 stack and check config Summary tab.
        """
        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],
            'stp enable': [None, None],
            'edge port': ['click', 'enabled'],
            'bpdu protection': [None, None],
            'priority': ['32', '32'],
            'path cost': ['50', '50'],

            'page5 stormControlSettings': ["next_page", None],

            'page6 pseSettings': ["next_page", None],

            'page7 summary': ["next_page", None]
            }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'Access'],

                         'page2 accessVlanPage': ['next_page', None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],
                         'stp enable': [None, None],
                         'edge port': ['click', 'enabled'],
                         'bpdu protection': [None, None],
                         'priority': ['48', '48'],
                         'path cost': ['90000', '90000'],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, d360=True)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @pytest.mark.tcxm_18429
    @pytest.mark.p1
    def test_tcxm_18429(self, node, xiq_library_at_class_level, dev_cmd, network_manager):
        """	 TCXM-18429 - D360 View - Add Storm Control Settings in Create Port Type tab for U100 device and
        check config Summary tab.
            TCXM-18431 - D360 View - Add Storm Control Settings in Create Port Type tab for U100 stack and
        check config Summary tab."""

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],
            'broadcast': ['click', 'enabled'],
            'unknown unicast': [None, 'disabled'],
            'multicast': ['click', 'enabled'],
            'rate limit type': [None, 'pps'],
            'rate limit value': ['65521', '65521'],

            'page6 MACLocking': ["next_page", None],

            'page7 ELRP': ["next_page", None],

            'page8 pseSettings': ["next_page", None],

            'page9 summary': ["next_page", None]
            }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 accessVlanPage': ['next_page', None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],
                         'broadcast': ['click', 'enabled'],
                         'unknown unicast': ['click', 'enabled'],
                         'multicast': ['click', 'enabled'],
                         'rate limit type': [None, 'pps'],
                         'rate limit value': ['262100', '262100'],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, d360=True)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @pytest.mark.tcxm_18432
    @pytest.mark.p1
    def test_tcxm_18432(self, node, xiq_library_at_class_level, dev_cmd, network_manager):
        """	 TCXM-18432 - D360 View - Add PSE Settings in Create Port Type tab for U100 device and check config Summary tab.
             TCXM-18434 - D360 View - Add PSE Settings in Create Port Type tab for U100 stack and check config Summary tab.
        """

        # This test should skip if device does not support POE.
        self.verify_poe_supported(node)

        # refresh page
        xiq_library_at_class_level.CloudDriver.refresh_page()

        def _check_page_after_refresh():
            try:
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                return True
            except Exception as e:
                print("Exception: ", e)
                return False

        xiq_library_at_class_level.Utils.wait_till(_check_page_after_refresh, timeout=30, is_logging_enabled=True)

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")
        pse_profile_name = "PSE_" + random_word(x=6)

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 pseSettings': ["next_page", None],
            'pse profile': [{'pse_profile_name': pse_profile_name,
                             'pse_profile_power_mode': '802.3at',
                             'pse_profile_power_limit': '20000',
                             'pse_profile_priority': 'high',
                             'pse_profile_description': 'Testing PSE'
                             }, pse_profile_name],

            'POE status': ['off', 'off'],

            'page7 summary': ["next_page", None]
        }
        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 accessVlanPage': ['next_page', None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],
                         'pse profile': [{'pse_profile_name': pse_profile_name,
                                          'pse_profile_power_mode': '802.3at',
                                          'pse_profile_power_limit': '20000',
                                          'pse_profile_priority': 'high',
                                          'pse_profile_description': 'Testing PSE'
                                          }, pse_profile_name],
                         'poe status': ['off', 'off'],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, d360=True)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @pytest.mark.tcxm_18440
    @pytest.mark.p2
    def test_tcxm_18440(self, node, xiq_library_at_class_level, dev_cmd, network_manager):
        """	 TCXM-18440 - D360 View - Created a Port Type Template on U100 VOSS device and toggle Auto-Sense button."""

        # This test should skip if device is not VOSS
        if node.cli_type.lower() != "voss":
            pytest.skip("This test can run only on VOSS.")

        # refresh page
        # xiq_library_at_class_level.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_on_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_on = {
            'name': [port_type_voss_auto_sense_on_name, port_type_voss_auto_sense_on_name],
            'description': ["port_type_description", "port_type_description"],
            'status': ['click', 'off'],
            'auto-sense': [None, None],
            'port usage': [None, 'auto_sense'],

            'page3 transmissionSettings': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 pseSettings': ["next_page", None],

            'page7 summary': ["next_page", None]
        }
        template_exos = None

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_on, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, d360=True)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        xiq_library_at_class_level.xflowsmanageDevice360.close_device360_window()
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_on_name, port_type_exos_name)

    @pytest.mark.tcxm_18473
    @pytest.mark.p1
    def test_tcxm_18473(self, node, xiq_library_at_class_level, dev_cmd, network_manager, node_policy_name, node_template_name):
        """	 TCXM-18473 - Policy Template - Add Port Name&Usage Configuration in Create Port Type tab for U100 device
        and check config Summary tab.
            TCXM-18473 - Policy Template - Add Port Name&Usage Configuration in Create Port Type tab for U100 stack
        and check config Summary tab."""

        # refresh page
        # xiq_library_at_class_level.CloudDriver.refresh_page()

        # BGD
        #node_policy_name = "XIQ_921_np_HxVpL9H5"
        #node_template_name = "XIQ_921_template_BRFRyxpv"

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': ["port_type_description", "port_type_description"],
            'status': ['click', 'off'],
            'auto-sense': ['click', None],
            'port usage': ['trunk port', 'trunk'],

            'page2 trunkVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': ["port_type_description", "port_type_description"],
                         'status': [None, 'on'],
                         'port usage': ['trunk port', 'trunk'],

                         'page2 trunkVlanPage': ["next_page", None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port,
                                                          node_policy_name, node_template_name, d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @pytest.mark.tcxm_18476
    @pytest.mark.p1
    def test_tcxm_18476(self, node, xiq_library_at_class_level, dev_cmd, network_manager, node_policy_name, node_template_name):
        """	 TCXM-18476 - Policy Template - Add Vlan in VLAN tab for U100 device and check config Summary tab.
             TCXM-18478 - Policy Template - Add Vlan in VLAN tab for U100 stack and check config Summary tab."""

        # refresh page
        # xiq_library_at_class_level.CloudDriver.refresh_page()

        # BGD
        #node_policy_name = "XIQ_921_np_HxVpL9H5"
        #node_template_name = "XIQ_921_template_BRFRyxpv"

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],
            'vlan': ['50', '50'],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        template_exos = {
            'name': [port_type_exos_name, port_type_exos_name],
            'description': [None, None],
            'status': [None, 'on'],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],
            'vlan': ['30', '30'],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 ELRP': ["next_page", None],

            'page8 pseSettings': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port,
                                                          node_policy_name, node_template_name, d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @pytest.mark.tcxm_18479
    @pytest.mark.p1
    def test_tcxm_18479(self, node, xiq_library_at_class_level, dev_cmd, network_manager, node_policy_name, node_template_name):
        """	 TCXM-18479 - Policy Template - Add Transmission Settings in Create Port Type tab for U100 device
        and check config Summary tab.
             TCXM-18481 - Policy Template - Add Transmission Settings in Create Port Type tab for U100 stack
        and check config Summary tab."""


        # refresh page
        # xiq_library_at_class_level.CloudDriver.refresh_page()

        # BGD
        #node_policy_name = "XIQ_921_np_HxVpL9H5"
        #node_template_name = "XIQ_921_template_BRFRyxpv"

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],
            'transmission type': ['Full-Duplex', 'Full-Duplex'],
            'transmission speed': ['100 Mbps', '100'],
            'cdp receive': [None, 'off'],
            'lldp transmit': ['click', 'off'],
            'lldp receive': [None, 'off'],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        template_exos = {
            'name': [port_type_exos_name, port_type_exos_name],
            'description': [None, None],
            'status': [None, 'on'],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ['next_page', None],

            'page3 transmissionSettings': ["next_page", None],
            'transmission type': ['Full-Duplex', 'Full-Duplex'],
            'transmission speed': ['100 Mbps', '100'],
            'cdp receive': ['click', 'on'],
            'lldp transmit': ['click', 'off'],
            'lldp receive': ['click', 'off'],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 ELRP': ["next_page", None],

            'page8 pseSettings': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, node_policy_name,
                                                          node_template_name, d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @pytest.mark.tcxm_18482
    @pytest.mark.p1
    def test_tcxm_18482(self, node, xiq_library_at_class_level, dev_cmd, network_manager, node_policy_name, node_template_name):
        """	 TCXM-18482 - Policy Template - Add STP Settings in Create Port Type tab for U100 device and check config
            in Summary tab.
            TCXM-18484 - Policy Template - Add STP Settings in Create Port Type tab for U100 stack and check config
            in Summary tab.
        """


        # refresh page
        # xiq_library_at_class_level.CloudDriver.refresh_page()

        # BGD
        #node_policy_name = "XIQ_921_np_HxVpL9H5"
        #node_template_name = "XIQ_921_template_BRFRyxpv"

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],
            'stp enable': [None, None],
            'edge port': ['click', 'enabled'],
            'bpdu protection': [None, None],
            'priority': ['32', '32'],
            'path cost': ['50', '50'],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        template_exos = {
            'name': [port_type_exos_name, port_type_exos_name],
            'description': [None, None],
            'status': [None, 'on'],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ['next_page', None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],
            'stp enable': [None, None],
            'edge port': ['click', 'enabled'],
            'bpdu protection': [None, None],
            'priority': ['48', '48'],
            'path cost': ['90000', '90000'],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 ELRP': ["next_page", None],

            'page8 pseSettings': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        # Configure port type
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, node_policy_name,
                                                          node_template_name, d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @pytest.mark.tcxm_18485
    @pytest.mark.p1
    def test_tcxm_18485(self, node, xiq_library_at_class_level, dev_cmd, network_manager, node_policy_name, node_template_name):
        """	 TCXM-18485 - Policy Template - Add Storm Control Settings in Create Port Type tab for U100 device
        and check config Summary tab.
            TCXM-18487 - Policy Template - Add Storm Control Settings in Create Port Type tab for U100 stack
        and check config Summary tab."""

        # refresh page
        # xiq_library_at_class_level.CloudDriver.refresh_page()

        # BGD
        #node_policy_name = "XIQ_921_np_HxVpL9H5"
        #node_template_name = "XIQ_921_template_BRFRyxpv"

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],
            'broadcast': ['click', 'enabled'],
            'unknown unicast': [None, 'disabled'],
            'multicast': ['click', 'enabled'],
            'rate limit type': [None, 'pps'],
            'rate limit value': ['65521', '65521'],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        template_exos = {
            'name': [port_type_exos_name, port_type_exos_name],
            'description': [None, None],
            'status': [None, 'on'],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ['next_page', None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],
            'broadcast': ['click', 'enabled'],
            'unknown unicast': ['click', 'enabled'],
            'multicast': ['click', 'enabled'],
            'rate limit type': [None, 'pps'],
            'rate limit value': ['262100', '262100'],

            'page6 MACLocking': ["next_page", None],

            'page7 ELRP': ["next_page", None],

            'page8 pseSettings': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, node_policy_name,
                                                          node_template_name, d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @pytest.mark.tcxm_18488
    @pytest.mark.p1
    def test_tcxm_18488(self, node, xiq_library_at_class_level, dev_cmd, network_manager, node_policy_name, node_template_name):
        """	 TCXM-18488 - Policy Template - Add PSE Settings in Create Port Type tab for U100 device and check
            config in Summary tab.
            TCXM-18490 - Policy Template - Add PSE Settings in Create Port Type tab for U100 stack and check
            config in Summary tab.
        """

        # BGD
        #node_policy_name = "XIQ_921_np_HxVpL9H5"
        #node_template_name = "XIQ_921_template_BRFRyxpv"

        # This test should skip if device does not support POE.
        self.verify_poe_supported(node)

        # refresh page
        xiq_library_at_class_level.CloudDriver.refresh_page()

        def _check_page_after_refresh():
            try:
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                return True
            except Exception as e:
                print("Exception: ", e)
                return False

        xiq_library_at_class_level.Utils.wait_till(_check_page_after_refresh, timeout=30, is_logging_enabled=True)

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")
        pse_profile_name = "PSE_" + random_word(x=6)

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page7 pseSettings': ["next_page", None],
            'pse profile': [{'pse_profile_name': pse_profile_name,
                             'pse_profile_power_mode': '802.3at',
                             'pse_profile_power_limit': '20000',
                             'pse_profile_priority': 'high',
                             'pse_profile_description': 'Testing PSE'
                             }, pse_profile_name],
            'POE status': ['off', 'off'],

            'page9 summary': ["next_page", None]
            }
        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 accessVlanPage': ['next_page', None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],
                         'pse profile': [{'pse_profile_name': pse_profile_name,
                                          'pse_profile_power_mode': '802.3at',
                                          'pse_profile_power_limit': '20000',
                                          'pse_profile_priority': 'high',
                                          'pse_profile_description': 'Testing PSE'
                                          }, pse_profile_name],
                         # 'pse profile': [(pse_profile_name, '802.3at', '20000', 'high', 'Testing PSE', False),
                         #                 pse_profile_name],
                         'poe status': ['off', 'off'],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, node_policy_name,
                                                          node_template_name, d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @pytest.mark.tcxm_18561
    @pytest.mark.p2
    def test_tcxm_18561(self, node, xiq_library_at_class_level, dev_cmd, network_manager, node_policy_name, node_template_name):
        """	 TCXM-18561 - Policy Template - Created a Port Type Template on U100 VOSS device and toggle Auto-Sense button.
        """

        # BGD
        #node_policy_name = "XIQ_921_np_HxVpL9H5"
        #node_template_name = "XIQ_921_template_BRFRyxpv"

        # This test should skip if device is not VOSS
        if node.cli_type.lower() != "voss":
            pytest.skip("This test cand run only on VOSS.")

        # refresh page
        # xiq_library_at_class_level.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_on_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_on = {
            'name': [port_type_voss_auto_sense_on_name, port_type_voss_auto_sense_on_name],
            'description': ["port_type_description", "port_type_description"],
            'status': ['click', 'off'],
            'auto-sense': [None, None],
            'port usage': [None, 'auto_sense'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        template_exos = None

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_on, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, node_policy_name,
                                                          node_template_name, d360=False)

        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')

        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_on_name, port_type_exos_name)

    @pytest.mark.tcxm_18493
    @pytest.mark.p1
    def test_tcxm_18493(self, node, xiq_library_at_class_level, dev_cmd, network_manager, node_policy_name, node_template_name):
        """	 TCXM-18493 - Policy Template - Edit Port Name&Usage in Create Port Type tab for U100 stack and check
            config in Summary tab."""


        # refresh page
        # xiq_library_at_class_level.CloudDriver.refresh_page()

        # BGD
        #node_policy_name = "XIQ_921_np_HxVpL9H5"
        #node_template_name = "XIQ_921_template_BRFRyxpv"

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': ["port_type_description", "port_type_description"],
            'status': ['click', 'off'],
            'auto-sense': ['click', None],
            'port usage': ['trunk port', 'trunk'],

            'page2 trunkVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        template_exos = {
            'name': [port_type_exos_name, port_type_exos_name],
            'description': ["port_type_description", "port_type_description"],
            'status': ['click', 'off'],
            'port usage': ['trunk port', 'trunk'],

            'page2 trunkVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 ELRP': ["next_page", None],

            'page8 pseSettings': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        # Configure port type
        print(f"Configuring Port Type in network policy {node_policy_name} and sw "
              f"template {node_template_name}")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, node_policy_name,
                                                          node_template_name, d360=False)
        if delete_port_type != 1:
            pytest.fail("Failed to create new port type.")
        template_voss_auto_sense_off_edit = {'page1 usagePage': ["usagePage", None],
                                             'name': [port_type_voss_auto_sense_off_name,
                                                      port_type_voss_auto_sense_off_name],
                                             'description': ["port_type_description1", "port_type_description1"],
                                             'status': ['click', 'on'],
                                             'auto-sense': [None, None],
                                             'port usage': ['trunk port', 'trunk'],
                                             'page7 summaryPage': ["summaryPage", None]
                                             }

        template_exos_edit = {
            'page1 usagePage': ["usagePage", None],
            'name': [port_type_exos_name, port_type_exos_name],
            'description': ["port_type_description1", "port_type_description1"],
            'status': ['click', 'on'],
            'port usage': ['trunk port', 'trunk'],
            'page7 summaryPage': ["summaryPage", None]
        }

        # Create port type
        print("EDITING Port Type")
        if node.platform.lower() == "stack":
            delete_port_type = self.edit_port_type_local(node, xiq_library_at_class_level,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        else:
            delete_port_type = self.edit_port_type_local(node, xiq_library_at_class_level,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        if delete_port_type != 1:
            pytest.fail("Failed to edit the port type.")
        # Delete port type
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @pytest.mark.tcxm_18494
    @pytest.mark.p1
    def test_tcxm_18494(self, node, xiq_library_at_class_level, dev_cmd, network_manager, node_policy_name, node_template_name):
        """	 TCXM-18494 - Policy Template - Edit Vlan in VLAN tab for U100 device and check config Summary tab.
             TCXM-18496 - Policy Template - Edit Vlan in VLAN tab for U100 stack and check config Summary tab."""

        # refresh page
        # xiq_library_at_class_level.CloudDriver.refresh_page()

        # BGD
        #node_policy_name = "XIQ_921_np_HxVpL9H5"
        #node_template_name = "XIQ_921_template_BRFRyxpv"

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],
            'vlan': ['50', '50'],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
            }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 accessVlanPage': ["next_page", None],
                         'vlan': ['30', '30'],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print(
            f"Configuring Port Type in network policy {node_policy_name} and sw template {node_template_name}")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port,
                                                          voss_or_exos_port, node_policy_name,
                                                          node_template_name,
                                                          d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to create a new port type.')
        # Create new templates for editing port type - the name of the template should remain the same
        template_voss_auto_sense_off_edit = {'page2 accessVlanPage': ["tab_vlan", None],
                                             'vlan': ['30', '30'],
                                             'page7 summaryPage': ["summaryPage", None]
                                             }

        template_exos_edit = {'page2 accessVlanPage': ["tab_vlan", None],
                              'vlan': ['30', '30'],
                              'page7 summaryPage': ["summaryPage", None]
                              }

        # Create port type
        print("EDITING Port Type")
        if node.platform.lower() == "stack":
            delete_port_type = self.edit_port_type_local(node, xiq_library_at_class_level,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        else:
            delete_port_type = self.edit_port_type_local(node, xiq_library_at_class_level,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        if delete_port_type != 1:
            pytest.fail('Failed to edit port type.')
        # Delete port type
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @pytest.mark.tcxm_18497
    @pytest.mark.p1
    def test_tcxm_18497(self, node, xiq_library_at_class_level, dev_cmd, network_manager, node_policy_name, node_template_name):
        """	 TCXM-18497 - Policy Template - Edit Transmission Settings in Create Port Type tab for U100 device and
            check config in Summary tab.
            TCXM-18499 - Policy Template - Edit Transmission Settings in Create Port Type tab for U100 stack and
            check config in Summary tab."""

        # refresh page
        # xiq_library_at_class_level.CloudDriver.refresh_page()

        # BGD
        #node_policy_name = "XIQ_921_np_HxVpL9H5"
        #node_template_name = "XIQ_921_template_BRFRyxpv"

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],
            'transmission type': ['Full-Duplex', 'Full-Duplex'],
            'transmission speed': ['100 Mbps', '100'],
            'cdp receive': [None, 'off'],
            'lldp transmit': ['click', 'off'],
            'lldp receive': [None, 'off'],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
            }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 accessVlanPage': ['next_page', None],

                         'page3 transmissionSettings': ["next_page", None],
                         'transmission type': ['Full-Duplex', 'Full-Duplex'],
                         'transmission speed': ['100 Mbps', '100'],
                         'cdp receive': ['click', 'on'],
                         'lldp transmit': ['click', 'off'],
                         'lldp receive': ['click', 'off'],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print(
            f"Configuring Port Type in network policy {node_policy_name} and sw template {node_template_name}")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port,
                                                          voss_or_exos_port, node_policy_name,
                                                          node_template_name,
                                                          d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to create port type.')
        # Create new templates for editing port type - the name of the template should remain the same
        template_voss_auto_sense_off_edit = {'page3 transmissionSettingsPage': ["transmissionSettingsPage", None],
                                             'transmission type': ['auto', 'auto'],
                                             'transmission speed': ['auto', 'auto'],
                                             'cdp receive': [None, 'off'],
                                             'lldp transmit': ['click', 'on'],
                                             'lldp receive': [None, 'on'],
                                             'page7 summaryPage': ["summaryPage", None]
                                             }

        template_exos_edit = {'page3 transmissionSettingsPage': ["transmissionSettingsPage", None],
                              'transmission type': ['auto', 'auto'],
                              'transmission speed': ['auto', 'auto'],
                              'cdp receive': ['click', 'off'],
                              'lldp transmit': ['click', 'on'],
                              'lldp receive': ['click', 'on'],
                              'page7 summaryPage': ["summaryPage", None]
                              }

        # Create port type
        print("EDITING Port Type")
        if node.platform.lower() == "stack":
            delete_port_type = self.edit_port_type_local(node, xiq_library_at_class_level,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        else:
            delete_port_type = self.edit_port_type_local(node, xiq_library_at_class_level,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        if delete_port_type != 1:
            pytest.fail('Failed to edit port type.')
        # Delete port type
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @pytest.mark.tcxm_18500
    @pytest.mark.p1
    def test_tcxm_18500(self, node, xiq_library_at_class_level, dev_cmd, network_manager, node_policy_name, node_template_name):
        """	 TCXM-18500 - Policy Template - Edit STP Settings in Create Port Type tab for U100 device and check
            config in Summary tab.
            TCXM-18502 - Policy Template - Edit STP Settings in Create Port Type tab for U100 stack and check
            config in Summary tab.
        """

        # refresh page
        # xiq_library_at_class_level.CloudDriver.refresh_page()

        # BGD
        #node_policy_name = "XIQ_921_np_HxVpL9H5"
        #node_template_name = "XIQ_921_template_BRFRyxpv"

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 trunkVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],
            'stp enable': [None, None],
            'edge port': [None, None],
            'bpdu protection': [None, None],
            'priority': ['32', '32'],
            'path cost': ['50', '50'],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
            }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 trunkVlanPage': ["next_page", None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],
                         'stp enable': [None, None],
                         'edge port': [None, None],
                         'bpdu protection': [None, None],
                         'priority': ['48', '48'],
                         'path cost': ['90000', '90000'],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print(
            f"Configuring Port Type in network policy {node_policy_name} and sw template {node_template_name}")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port,
                                                          voss_or_exos_port, node_policy_name,
                                                          node_template_name,
                                                          d360=False)
        if delete_port_type != 1:
            pytest.fail("Failed to create new port type")
        # Create new templates for editing port type - the name of the template should remain the same
        template_voss_auto_sense_off_edit = {'page4 stpPage': ["stpPage", None],
                                             'stp enable': [None, None],
                                             'edge port': [None, None],
                                             'bpdu protection': [None, None],
                                             'priority': ['16', '16'],
                                             'path cost': ['2435', '2435'],
                                             'page7 summaryPage': ["summaryPage", None]
                                             }

        template_exos_edit = {'page4 stpPage': ["stpPage", None],
                              'stp enable': [None, None],
                              'edge port': [None, None],
                              'bpdu protection': [None, None],
                              'priority': ['16', '16'],
                              'path cost': ['2435', '2435'],
                              'page7 summaryPage': ["summaryPage", None]
                              }

        # Create port type
        print("EDITING Port Type")
        if node.platform.lower() == "stack":
            delete_port_type = self.edit_port_type_local(node, xiq_library_at_class_level,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        else:
            delete_port_type = self.edit_port_type_local(node, xiq_library_at_class_level,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        if delete_port_type != 1:
            pytest.fail("Failed to edit port type.")
        # Delete port type
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @pytest.mark.tcxm_18503
    @pytest.mark.p1
    def test_tcxm_18503(self, node, xiq_library_at_class_level, dev_cmd, network_manager, node_policy_name, node_template_name):
        """	 TCXM-18503 - Policy Template - Edit Storm Control Settings in Create Port Type tab for U100 device and
            check config in Summary tab.
            TCXM-18505 - Policy Template - Edit Storm Control Settings in Create Port Type tab for U100 stack and
            check config in Summary tab."""


        # refresh page
        # xiq_library_at_class_level.CloudDriver.refresh_page()

        # BGD
        #node_policy_name = "XIQ_921_np_HxVpL9H5"
        #node_template_name = "XIQ_921_template_BRFRyxpv"

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],
            'broadcast': ['click', 'enabled'],
            'unknown unicast': [None, 'disabled'],
            'multicast': ['click', 'enabled'],
            'rate limit type': [None, 'pps'],
            'rate limit value': ['65521', '65521'],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 trunkVlanPage': ["next_page", None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],
                         'page5 stormControlSettings': ["next_page", None],
                         'broadcast': ['click', 'enabled'],
                         'unknown unicast': ['click', 'enabled'],
                         'multicast': ['click', 'enabled'],
                         'rate limit type': [None, 'pps'],
                         'rate limit value': ['262100', '262100'],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print(
            f"Configuring Port Type in network policy {node_policy_name} and sw template {node_template_name}")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port,
                                                          voss_or_exos_port, node_policy_name,
                                                          node_template_name,
                                                          d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to create new port type.')
        # Create new templates for editing port type - the name of the template should remain the same
        template_voss_auto_sense_off_edit = {'page5 stormControlSettingsPage': ["stormControlSettingsPage", None],
                                             'broadcast': ['click', 'disabled'],
                                             'unknown unicast': [None, 'disabled'],
                                             'multicast': ['click', 'disabled'],
                                             'rate limit type': [None, 'pps'],
                                             'rate limit value': ['65522', '65522'],
                                             'page7 summaryPage': ["summaryPage", None]
                                             }

        template_exos_edit = {'page5 stormControlSettingsPage': ["stormControlSettingsPage", None],
                              'broadcast': ['click', 'disabled'],
                              'unknown unicast': ['click', 'disabled'],
                              'multicast': ['click', 'disabled'],
                              'rate limit type': [None, 'pps'],
                              'rate limit value': ['265', '265'],
                              'page7 summaryPage': ["summaryPage", None]
                              }

        # Create port type
        print("EDITING Port Type")
        if node.platform.lower() == "stack":
            delete_port_type = self.edit_port_type_local(node, xiq_library_at_class_level,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        else:
            delete_port_type = self.edit_port_type_local(node, xiq_library_at_class_level,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        if delete_port_type != 1:
            pytest.fail("Failed to edit port type.")
        # Delete port type
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @pytest.mark.tcxm_18506
    @pytest.mark.p1
    def test_tcxm_18506(self, node, xiq_library_at_class_level, dev_cmd, network_manager, node_policy_name, node_template_name):
        """	 TCXM-18506 - Policy Template - Edit PSE Settings in Create Port Type tab for U100 device and check
            config in Summary tab.
            TCXM-18508 - Policy Template - Edit PSE Settings in Create Port Type tab for U100 device and check
            config in Summary tab.
        """

        # BGD
        #node_policy_name = "XIQ_921_np_HxVpL9H5"
        #node_template_name = "XIQ_921_template_BRFRyxpv"

        #Skip if the device is 5320 running voss OS
        if node.platform == "5320" and node.cli_type == "voss":
            pytest.skip("SKIP the test . The 5320 voss device doesn't support PSE 802.3bt mode")

        # This test should skip if device does not support PSE
        self.verify_poe_supported(node)

        xiq_library_at_class_level.CloudDriver.refresh_page()

        def _check_page_after_refresh():
            try:
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                return True
            except Exception as e:
                print("Exception: ", e)
                return False

        xiq_library_at_class_level.Utils.wait_till(_check_page_after_refresh, timeout=30, is_logging_enabled=True)

        voss_port_check = "1/2"
        if node.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:7'
        else:
            exos_port_check = "7"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, node.cli_type, xiq_library_at_class_level, node, dev_cmd, network_manager )

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")
        pse_profile_name = "PSE_" + random_word(x=6)

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page7 pseSettings': ["next_page", None],
            'pse profile': [{'pse_profile_name': pse_profile_name,
                             'pse_profile_power_mode': '802.3at',
                             'pse_profile_power_limit': '20000',
                             'pse_profile_priority': 'high',
                             'pse_profile_description': 'Testing PSE'
                             }, pse_profile_name],
            'poe status': ['off', 'off'],

            'page9 summary': ["next_page", None]
        }
        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 accessVlanPage': ['next_page', None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],
                         'pse profile': [{'pse_profile_name': pse_profile_name,
                                          'pse_profile_power_mode': '802.3at',
                                          'pse_profile_power_limit': '20000',
                                          'pse_profile_priority': 'high',
                                          'pse_profile_description': 'Testing PSE'
                                          }, pse_profile_name],
                         'poe status': ['off', 'off'],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print(
            f"Configuring Port Type in network policy {node_policy_name} and sw template {node_template_name}")
        delete_port_type = self.configure_port_type_local(xiq_library_at_class_level, node, template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port,
                                                          voss_or_exos_port, node_policy_name,
                                                          node_template_name,
                                                          d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to create new port type')

        print("Saving template")

        def _check_template_save():
            if xiq_library_at_class_level.xflowsconfigureSwitchTemplate.save_template() == 1:
                return True
            else:
                return False

        xiq_library_at_class_level.Utils.wait_till(_check_template_save, delay=5, timeout=30)

        # refresh page
        xiq_library_at_class_level.CloudDriver.refresh_page()

        def _check_page_after_refresh():
            try:
                xiq_library_at_class_level.xflowscommonNavigator.navigate_to_devices()
                return True
            except Exception as e:
                print("Exception: ", e)
                return False

        xiq_library_at_class_level.Utils.wait_till(_check_page_after_refresh, timeout=30, is_logging_enabled=True)
        time.sleep(10)
        select_template = xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_policy_name,
                                                                                    node_template_name, node.cli_type)
        if select_template != 1:
            pytest.fail("Could not select switch template ", node_template_name)

        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.go_to_port_configuration()

        # Create new templates for editing port type - the name of the template should remain the same
        template_voss_auto_sense_off_edit = {'page6 pseSettingsPage': ["pseSettingsPage", None],
                                             'pse profile': [{'pse_profile_name': pse_profile_name,
                                                              'pse_profile_power_mode': '802.3bt',
                                                              'pse_profile_power_limit': '30000',
                                                              'pse_profile_priority': 'critical',
                                                              'pse_profile_description': 'Testing PSE EDIT',
                                                              'pse_profile_edit_flag': True
                                                              }, pse_profile_name],
                                             'poe status': ['on', 'on'],

                                             'page7 summaryPage': ["summaryPage", None]
                                             }

        template_exos_edit = {'page6 pseSettingsPage': ["pseSettingsPage", None],
                              'pse profile': [{'pse_profile_name': pse_profile_name,
                                               'pse_profile_power_mode': '802.3bt',
                                               'pse_profile_power_limit': '30000',
                                               'pse_profile_priority': 'critical',
                                               'pse_profile_description': 'Testing PSE EDIT',
                                               'pse_profile_edit_flag': True
                                               }, pse_profile_name],
                              'poe status': ['on', 'on'],

                              'page7 summaryPage': ["summaryPage", None]
                              }

        # Create port type
        print("EDITING Port Type")
        if node.platform.lower() == "stack":
            delete_port_type = self.edit_port_type_local(node, xiq_library_at_class_level,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        else:
            delete_port_type = self.edit_port_type_local(node, xiq_library_at_class_level,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        if delete_port_type != 1:
            pytest.fail('Failed to edit port type')
        if node.make == 'voss':
            voss_or_exos_port = voss_or_exos_port.split('/')[1]
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(voss_or_exos_port,
                                                                                                  'Auto-sense Port')
        else:
            if node.platform.lower() == 'stack':
                voss_or_exos_port = voss_or_exos_port.split(':')[1]
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(voss_or_exos_port,
                                                                                                  'Access Port')
        # Delete port type
        self.delete_port_type_local(node, xiq_library_at_class_level, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

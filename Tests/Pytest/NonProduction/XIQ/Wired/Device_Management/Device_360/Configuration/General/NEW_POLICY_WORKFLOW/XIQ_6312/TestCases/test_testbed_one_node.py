import pytest
import random
import string
import re

global port_type_name

@pytest.mark.development
@pytest.mark.testbed_1_node

class XIQ6312OneNodeTests():

    @pytest.mark.p1
    @pytest.mark.tcxm_23826
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    def test_23826(self, logger, xiq_library_at_class_level,
            node_1, node_1_policy_name, node_1_template_name, utils):

        xiq_library_at_class_level.xflowsconfigureNetworkPolicy.navigate_to_switching_tab(policy_name=node_1_policy_name)
        assert xiq_library_at_class_level.xflowsconfigureNetworkPolicy.get_port_types_section() == 1, "Port types section not found"


    @pytest.mark.p1
    @pytest.mark.tcxm_23827
    @pytest.mark.dependson("tcxm_23826")
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    def test_23827(self, test_data, logger,
                xiq_library_at_class_level, node_1, node_1_policy_name, node_1_template_name, utils):

        # Verify user can create port-type

        port_type_name = xiq_library_at_class_level.xflowsconfigureNetworkPolicy.get_random_name("test_port_type")
        expected_summary = {
            # currently below there are the default values from GUI
            'STP': 'Enabled',
            'VLAN': '1',
            'Status': 'On',
            'Port Usage': 'Access'
        }
        logger.info(f"Expected summary: {expected_summary}")

        assert xiq_library_at_class_level.xflowsconfigureNetworkPolicy.create_new_port_type(node_1.cli_type.upper()) == 1, "Port type Configuration did not open"

        _, create_port_type_summary = xiq_library_at_class_level.xflowsconfigureNetworkPolicy.configure_port_type(port_type_name)
        logger.info(f"Summary from create port type in Port Types Section: {create_port_type_summary}")
        logger.info(f"Verify that the configured fields appear correctly in the summary tab ")
        assert all(expected_summary[k] == create_port_type_summary[k] for k in expected_summary), \
            f"Not all the values of the summary are the expected ones . " \
            f"Expected summary: {expected_summary}\nFound summary: {create_port_type_summary}"
        logger.info(f"Successfully verified the summary of {port_type_name} at port type creation "
              f"using Port types Section")

        # Verify user can edit port-type

        xiq_library_at_class_level.xflowsconfigureNetworkPolicy.navigate_to_switching_tab(policy_name=node_1_policy_name)
        assert xiq_library_at_class_level.xflowsconfigureNetworkPolicy.get_port_types_section() == 1, "Port types section not found"
        
        xiq_library_at_class_level.xflowsconfigureNetworkPolicy.edit_port_type(port_type_name)
        xiq_library_at_class_level.xflowsconfigureNetworkPolicy.go_to_specific_tab_in_port_type_configuration(tab_name="NAME")
        xiq_library_at_class_level.xflowsmanageDevice360.configure_port_name_usage_tab(port_type_name=port_type_name, status=False)
        xiq_library_at_class_level.xflowsmanageDevice360.port_type_nav_to_summary_page_and_save()

        expected_edit_result = {
            'PORT STATUS': 'Disabled'
        }
        logger.info(f"Expected result after edit: {expected_edit_result}")

        edit_port_type_summary = xiq_library_at_class_level.xflowsconfigureNetworkPolicy.get_port_type_row_details(port_type_name,
                                    col_list="PORT STATUS")

        logger.info(f"Verify that the modified fields have the new values correctly saved in Port Types table ")
        assert all(expected_edit_result[k] == edit_port_type_summary[k] for k in expected_edit_result), \
                f"Status expected for port-type named {port_type_name} was Disabled. Instead found status Enabled."

        # Verify user can delete port-type

        assert xiq_library_at_class_level.xflowsconfigureNetworkPolicy.delete_port_type(port_type_name) == 1 ,\
                f"Port-type {port_type_name} was not deleted"

    @pytest.mark.p1
    @pytest.mark.tcxm_23833
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.dependson("tcxm_xiq_onboarding")
    def test_23833(self, test_data,
                logger, xiq_library_at_class_level, node_1, node_1_policy_name, node_1_template_name, utils):

        assert xiq_library_at_class_level.xflowscommonDevices.assign_network_policy_to_switch_mac(policy_name=node_1_policy_name, mac=node_1.mac), \
            f"Couldn't assign policy {node_1_policy_name} to device {node_1}"

        commands_listed = xiq_library_at_class_level.xflowsmanageDeviceConfig.get_device_config_audit_delta(node_1.mac)

        assert commands_listed, f"No configuration found in Delta Audit"

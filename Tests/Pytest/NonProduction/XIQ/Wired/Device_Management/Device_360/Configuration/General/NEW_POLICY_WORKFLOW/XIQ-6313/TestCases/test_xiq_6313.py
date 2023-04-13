import pytest


@pytest.mark.development
@pytest.mark.p1
@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.testbed_1_node
class XIQ6313OneNodeTests:

    @pytest.mark.tcxm_23749
    def test_tcxm_23749(self, logger, xiq_library_at_class_level, node_1_policy_name, node_1_template_name, node_1,
                        auto_actions):
        """
        Verify that switch templates can override common settings parameters.
        """
        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_1_policy_name,
                                                                                    node_1_template_name)
        auto_actions.click_reference(xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                                     get_device_template_override_policy)
        assert xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_web_elements. \
            get_device_template_override_policy().is_selected(), "'Override Policy Common Settings' is not selected."

        if node_1.cli_type.lower() == "exos":
            logger.info("Configure IGMP for exos devices.")
            cmd_to_check = "disable igmp snooping"
            wireless_network_conf = {
                'igmp_setting': {
                    'igmp_snooping': 'off'
                }
            }
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.configure_switch_igmp_setting(
                wireless_network_conf)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.save_template()
            delta_cli = xiq_library_at_class_level.xflowsmanageDeviceConfig.check_config_audit_delta_match(
                serial=node_1.serial)
            logger.info("Check the command is generated in Delta CLI")
            assert cmd_to_check in delta_cli, f"Fail to check command {cmd_to_check} in Delta CLI"

        elif node_1.cli_type.lower() == "voss":
            logger.info("Configure MTU for voss devices.")
            cmd_to_check = "sys mtu 1522"
            wireless_network_conf = {'mtu': '1522'}
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.configure_switch_template_mtu_setting(
                wireless_network_conf)
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.save_template()
            delta_cli = xiq_library_at_class_level.xflowsmanageDeviceConfig.check_config_audit_delta_match(
                serial=node_1.serial)
            logger.info("Check the command is generated in Delta CLI")
            assert cmd_to_check in delta_cli, f"Fail to check command {cmd_to_check} in Delta CLI"

        else:
            logger.info("UNKNOWN CLI TYPE")

    @pytest.mark.tcxm_23747
    @pytest.mark.dependson("tcxm_23749")
    def test_tcxm_23747(self, logger):
        logger.info("this test case is covered by tcxm_23815")

    @pytest.mark.tcxm_23745
    @pytest.mark.dependson("tcxm_23749")
    def test_tcxm_23745(self, logger):
        logger.info("this test case is covered by tcxm_23815")

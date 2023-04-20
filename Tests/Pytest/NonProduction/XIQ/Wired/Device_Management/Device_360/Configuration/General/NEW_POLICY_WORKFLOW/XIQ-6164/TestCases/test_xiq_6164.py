import pytest


@pytest.mark.development
@pytest.mark.p1
@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.testbed_1_node
class XIQ6164OneNodeTests:
    @pytest.mark.testbed_stack
    @pytest.mark.tcxm_23823
    def test_tcxm_23823(self, logger, xiq_library_at_class_level, node_policy_name, node_template_name, node,
                        auto_actions, navigator, ):
        """
            Verify that the changes made in common settings are reflected in the default switch template for each policy
        """

        logger.step("Initialize variables")
        xiq = xiq_library_at_class_level
        xiq_np = xiq.xflowsconfigureNetworkPolicy
        dev_temp = xiq.xflowsconfigureSwitchTemplate
        xiq_np.navigate_to_np_edit_tab(node_policy_name)
        navigator.wait_until_loading_is_done()
        logger.info("Click on Device Template tab button")
        auto_actions.click_reference(dev_temp.device_template_web_elements.get_add_device_template_menu)
        navigator.wait_until_loading_is_done()
        if node.cli_type == "voss":
            auto_actions.click_reference(xiq_np.np_web_elements.get_common_settings_voss)
        elif node.cli_type == "exos":
            auto_actions.click_reference(xiq_np.np_web_elements.get_common_settings_exos)
        else:
            pytest.fail("CLI type unknown.")
        navigator.wait_until_loading_is_done()
        stp_common_settings_btn = None
        if node.cli_type == "voss":
            stp_common_settings_btn = xiq_np.np_web_elements.get_common_settings_voss_stp_toogle()
        elif node.cli_type == "exos":
            stp_common_settings_btn = xiq_np.np_web_elements.get_common_settings_exos_stp_toogle()
        else:
            pytest.fail("CLI type unknown.")

        current_status_from_comm_sett = stp_common_settings_btn.is_selected()
        if current_status_from_comm_sett:
            logger.info("Disabling STP from common settings")
            auto_actions.click_reference(lambda: stp_common_settings_btn)
        else:
            logger.info("Enabling STP from common settings")
            auto_actions.click_reference(lambda: stp_common_settings_btn)
        current_status_from_comm_sett = stp_common_settings_btn.is_selected()
        assert auto_actions.click_reference(xiq_np.np_web_elements.get_common_settings_save_button) == 1, \
            "Fail to save common settings"

        xiq_library_at_class_level.xflowsconfigureSwitchTemplate.select_sw_template(node_policy_name,
                                                                                    node_template_name)
        navigator.wait_until_loading_is_done()
        logger.info("Checking if configuration from common settings is overriding template config")
        assert dev_temp.sw_template_web_elements.get_sw_template_enable_spanningtree().is_selected() == \
               current_status_from_comm_sett, "Device status in template is not matching the one configured in " \
                                              "commong settings "
        if node.platform.lower() == "stack":
            xiq_library_at_class_level.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(2)
            navigator.wait_until_loading_is_done()
            assert dev_temp.sw_template_web_elements.get_sw_template_enable_spanningtree().is_selected() == \
                   current_status_from_comm_sett, "Device status in template is not matching the one configured in " \
                                                  "commong settings "

        logger.info("Common settings overrides template")

    @pytest.mark.tcxm_23808
    def test_tcxm_23808(self, logger, xiq_library_at_class_level, node_1_policy_name, node_1_template_name, node_1,
                        auto_actions, navigator):
        """
            Verify that the EXOS/Switch Engine subsection contains the STP parameter

        """

        exos_common_settings_parameters = ["Management Servers", "STP Configurations", "MTU Settings", "IGMP Settings",
                                           "PSE Settings", "MAC Locking Settings",
                                           "Extreme Loop Recovery Protocol Settings",
                                           "Management Interface Settings"]
        voss_common_settings_parameters = ["STP Configurations", "MTU Settings", "IGMP Settings", "PSE Settings"]
        logger.step("Initialize variables")
        xiq = xiq_library_at_class_level
        xiq_np = xiq.xflowsconfigureNetworkPolicy
        dev_temp = xiq.xflowsconfigureSwitchTemplate
        xiq_np.navigate_to_np_edit_tab(node_1_policy_name)
        navigator.wait_until_loading_is_done()
        logger.info("Click on Device Template tab button")
        auto_actions.click_reference(dev_temp.device_template_web_elements.get_add_device_template_menu)
        navigator.wait_until_loading_is_done()
        if node_1.cli_type == "voss":
            auto_actions.click_reference(xiq_np.np_web_elements.get_common_settings_voss)
        elif node_1.cli_type == "exos":
            auto_actions.click_reference(xiq_np.np_web_elements.get_common_settings_exos)
        else:
            pytest.fail("CLI type unknown.")
        navigator.wait_until_loading_is_done()
        get_all_possible_common_configs = xiq_np.np_web_elements.get_all_common_settings_configs()
        get_all_possible_common_configs_txt = []
        for el in get_all_possible_common_configs:
            get_all_possible_common_configs_txt.append(el.text)

        if node_1.cli_type.lower() == "exos":
            assert set(exos_common_settings_parameters) == set(get_all_possible_common_configs_txt), \
                "Not all the configuration parameters are present"
        elif node_1.cli_type.lower() == "voss":
            assert set(voss_common_settings_parameters) == set(get_all_possible_common_configs_txt), \
                "Not all the configuration parameters are present"
        else:
            assert "No CLI type found"

    @pytest.mark.tcxm_23809
    @pytest.mark.dependson("tcxm_23808")
    def test_tcxm_23809(self, logger):
        logger.info("this test case is covered by tcxm_23808")

    @pytest.mark.tcxm_23810
    @pytest.mark.dependson("tcxm_23808")
    def test_tcxm_23810(self, logger):
        logger.info("this test case is covered by tcxm_23808")

    @pytest.mark.tcxm_23811
    @pytest.mark.dependson("tcxm_23808")
    def test_tcxm_23811(self, logger):
        logger.info("this test case is covered by tcxm_23808")

    @pytest.mark.tcxm_23812
    @pytest.mark.dependson("tcxm_23808")
    def test_tcxm_23812(self, logger):
        logger.info("this test case is covered by tcxm_23808")

    @pytest.mark.tcxm_23813
    @pytest.mark.dependson("tcxm_23808")
    def test_tcxm_23813(self, logger):
        logger.info("this test case is covered by tcxm_23808")

    @pytest.mark.tcxm_23814
    @pytest.mark.dependson("tcxm_23808")
    def test_tcxm_23814(self, logger):
        logger.info("this test case is covered by tcxm_23808")

    @pytest.mark.tcxm_23815
    @pytest.mark.dependson("tcxm_23808")
    def test_tcxm_23815(self, logger):
        logger.info("this test case is covered by tcxm_23808")

    @pytest.mark.tcxm_23816
    @pytest.mark.dependson("tcxm_23808")
    def test_tcxm_23816(self, logger):
        logger.info("this test case is covered by tcxm_23808")

    @pytest.mark.tcxm_23817
    @pytest.mark.dependson("tcxm_23808")
    def test_tcxm_23817(self, logger):
        logger.info("this test case is covered by tcxm_23808")

    @pytest.mark.tcxm_23818
    @pytest.mark.dependson("tcxm_23808")
    def test_tcxm_23818(self, logger):
        logger.info("this test case is covered by tcxm_23808")

    @pytest.mark.tcxm_23806
    @pytest.mark.dependson("tcxm_23808")
    def test_tcxm_23806(self, logger):
        logger.info("this test case is covered by tcxm_23808")

    @pytest.mark.tcxm_23807
    @pytest.mark.dependson("tcxm_23808")
    def test_tcxm_23807(self, logger):
        logger.info("this test case is covered by tcxm_23808")


import pytest
import time

from extauto.xiq.elements.MLInsightsMonitorWebElements import MLInsighstMonitorWebElements


@pytest.mark.dependson("tcxm_xiq_onboarding")
class TCXM25159Tests:

    @pytest.mark.development
    @pytest.mark.testbed_2_node
    @pytest.mark.tcxm_25159
    @pytest.mark.p1
    def test_tcxm_25159(self, node_1, node_2, logger, auto_actions, xiq_library_at_class_level, loaded_config):

        MLInsWebElements = MLInsighstMonitorWebElements()
        ml_insights_monitor_option = "All Switches"

        try:
            logger.info("Navigate to ML Insights -> Network 360 Monitor.")
            xiq_library_at_class_level.xflowscommonNavigator.navigate_to_network360monitor()

            logger.info("Clicking on dropdown arrow.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_drop_down()

            logger.info("Navigate to 'All Switches' option.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.ml_insights_monitor_navigate_to_options_drop_down(ml_insights_monitor_option)

            logger.info("Clicking the devices card.")
            auto_actions.click(xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_elements.get_n360_monitor_devices_card())

            time.sleep(60)

            logger.info("Verifying sorting in legend section.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_sorting_legend_check()

            time.sleep(10)
            
            logger.info("Verifying sorting in halfpie section.")
            xiq_library_at_class_level.xflowsmlinsightsNetwork360Monitor.n360_monitor_port_connection_speed_sorting_halfpie_check()

        finally:
            logger.step("Closing Device Health window.")
            if close_dialog := MLInsWebElements.get_n360_monitor_device_health_window_close_dialog():
                auto_actions.click(close_dialog)

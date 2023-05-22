import pytest


@pytest.mark.p1
@pytest.mark.development
@pytest.mark.testbed_1_node
@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.skip_if_node_does_not_support_poe
class XIQ3012OneNodeTests:
    @pytest.mark.tcxm_20549
    def test_tcxm_20549(self, node_1, xiq_library_at_class_level):
        """ TCXM-20549 - Restart PSE" option from "Utilities" , the Pop-up window should be closed and the command
        “reset inline-power ports <port-list>” should be executed in DUT - EXOS standalone

        Step Description
        1.  Onboard the EXOS device
        2.  Select the EXOS device -> Actions
        3.  Click on Restart PSE
        4.  Verify the status in XIQ if the PSE reset has been completed
        -----------
        5.  Verify in CLI with "show cli journal" command if "reset inline-power ports <port-list>" command has been executed
        """

        xiq_library_at_class_level.xflowscommonDevices.restart_pse_function(dut=node_1)
        xiq_library_at_class_level.Cli.check_pse_restart_in_cli(dut=node_1)


@pytest.mark.p1
@pytest.mark.development
@pytest.mark.dependson("tcxm_xiq_onboarding")
@pytest.mark.testbed_stack
@pytest.mark.skip_if_node_does_not_support_poe
class XIQ3012StackTests:
    @pytest.mark.tcxm_20561
    def test_tcxm_20561(self, node_stack, xiq_library_at_class_level):
        """ TCXM-20561 - Restart PSE" option from "Utilities" , the Pop-up window should be closed and the command
        “reset inline-power ports <port-list>” should be executed in DUT - EXOS stack

        Step Description
        1.  Onboard the EXOS device
        2.  Select the EXOS device -> Actions
        3.  Click on Restart PSE
        4.  Verify the status in XIQ if the PSE reset has been completed
        -----------
        5.  Verify in CLI with "show cli journal" command if "reset inline-power ports <port-list>" command has been executed
        """

        xiq_library_at_class_level.xflowscommonDevices.restart_pse_function(dut=node_stack)
        xiq_library_at_class_level.Cli.check_pse_restart_in_cli(dut=node_stack)

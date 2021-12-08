"""
Feature ID: EXOS-291
Feature Name: EXOS Stacking LLDP Sync on Failover
Feature Owner: Vasanth Suresh

This test suite automates all Unit Test Cases of the feature EXOS-291.
This test suite works only on 'rdu_x460g2_stk_pod1_4node.yaml' testbed (4 node including Stack DUT)

To run all Testcases, use below command:
    pytest --tc-file=../../../../TestEnvironments/Rdu/Physical/Exos/rdu_x460g2_stk_pod1_4node.yaml TestCases
To run a specific Testcase using marker (say t1, t2, etc), use below command:
    pytest -m t1 --tc-file=../../../../TestEnvironments/Rdu/Physical/Exos/rdu_x460g2_stk_pod1_4node.yaml TestCases
Command execution path:
    Tests/Staging/Functional/LLDP_Sync_on_Failover_Feature_Unit_Tests
"""

from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from pytest import mark

from Tests.Pytest.Functional.nonprod.LLDP_Sync_on_Failover_Feature_Unit_Tests.Resources.SuiteUdks import SuiteUdk
from Tests.Pytest.Functional.nonprod.LLDP_Sync_on_Failover_Feature_Unit_Tests.Resources.SuiteVariables import SuiteVariable


@mark.required_platform('stack')
class LLDPSyncOnFailoverTests:

    # [Setup]  Test class Setup
    @classmethod
    def setup_class(cls):
        try:
            # Create the pytest execution helper
            cls.executionHelper = PytestExecutionHelper()
            # Create an instance of the helper class that will read in the test bed yaml file and provide basic
            # methods and variable access. The user can also get to the test bed yaml by using the config dictionary
            cls.tb = PytestConfigHelper(config)
            # Create an instance to use suite variables.
            cls.var = SuiteVariable()
            # Create an instance to use suite UDK functions/methods.
            cls.suiteUdks = SuiteUdk()
            # Create new objects to use in test. Here we will import everything from the default library
            cls.defaultLibrary = DefaultLibrary()
            cls.netElement = cls.defaultLibrary.deviceNetworkElement
            cls.lowApis = cls.defaultLibrary.apiLowLevelApis
            cls.udks = cls.defaultLibrary.apiUdks

            # Call base setup to connect to network elements
            cls.udks.setupTeardownUdks.Base_Test_Suite_Setup()
            # Generic setup for all our test cases
            cls.suiteUdks.test_suite_setup()

        except Exception:
            cls.executionHelper.setSetupFailure(True)

    # [Teardown]  Test class Cleanup
    @classmethod
    def teardown_class(cls):
        # Generic cleanup for all our test cases
        cls.suiteUdks.test_suite_cleanup()
        # Call base cleanup to disconnect from network elements
        cls.udks.setupTeardownUdks.Base_Test_Suite_Cleanup()

    """
    Test ID: 1
    
    Connect an FA server and client to DUT (FA proxy). Configure VLAN-NSI map in FA client.
    
    Verify if all below show commands are in sync between master and backup:
    1) show lldp neighbors
    2) show fabric attach elements
    3) show fabric attach assignments
    """

    @mark.t1  # Marked as a t1 test case
    def test_01_verify_sync_after_failover(self):
        self.executionHelper.testSkipCheck()
        print("Unit Test ID 1:")

        self.suiteUdks.verify_neighbors_and_assignments(60)

        self.udks.hostServicesUdks.networkElementResetDeviceKeywords.start_network_element_failover_and_wait(
            self.tb.dut1_name, max_wait=60, wait_before=10, wait_after_success=10)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name, 'show switch',
                                                                           'Current.*State.*BACKUP', exists=False)
        self.suiteUdks.verify_neighbors_and_assignments(0)
        self.suiteUdks.wait_for_backup_sync()
        self.suiteUdks.verify_neighbors_and_assignments(0)

    """
    Test ID 2:
    
    Repeat steps in Test ID 1 and do failover from master to backup. Once backup comes up do failover once again.
    
    Verify if all below show commands retains entries for all ports in current master node:
    1) show lldp neighbors
    2) show fabric attach elements
    3) show fabric attach assignments
    """

    @mark.t2
    def test_02_verify_sync_after_failover(self):
        self.executionHelper.testSkipCheck()
        print("Unit Test ID 2:")

        self.suiteUdks.verify_neighbors_and_assignments(60)

        self.udks.hostServicesUdks.networkElementResetDeviceKeywords.start_network_element_failover_and_wait(
            self.tb.dut1_name, max_wait=60, wait_before=10, wait_after_success=10)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name, 'show switch',
                                                                           'Current.*State.*BACKUP', exists=False)
        self.suiteUdks.verify_neighbors_and_assignments(0)
        self.suiteUdks.wait_for_backup_sync()
        self.suiteUdks.verify_neighbors_and_assignments(0)

        self.udks.hostServicesUdks.networkElementResetDeviceKeywords.start_network_element_failover_and_wait(
            self.tb.dut1_name, max_wait=60, wait_before=10, wait_after_success=10)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name, 'show switch',
                                                                           'Current.*State.*BACKUP', exists=False)
        self.suiteUdks.verify_neighbors_and_assignments(0)
        self.suiteUdks.wait_for_backup_sync()
        self.suiteUdks.verify_neighbors_and_assignments(0)

    """
    Test ID 3:
    
    Repeat steps in Test ID 1 and unconfigure VLAN-NSI map in FA client.
    
    Verify if fabric attach assignments of that client are removed in both primary and backup after timeout.
    """

    @mark.t3
    def test_03_verify_sync_after_failover(self):
        self.executionHelper.testSkipCheck()
        print("Unit Test ID 3:")

        self.suiteUdks.verify_neighbors_and_assignments(60)
        self.udks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.dut2_name, self.var.fa_client_vlan_id)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach assignments',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*' + self.var.fa_client_vlan_id +
                                                                           '.*' + self.var.fa_client_vlan_nsi,
                                                                           exists=False, max_wait=260, interval=20)

        self.udks.hostServicesUdks.networkElementResetDeviceKeywords.start_network_element_failover_and_wait(
            self.tb.dut1_name, max_wait=60, wait_before=10, wait_after_success=10)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name, 'show switch',
                                                                           'Current.*State.*BACKUP', exists=False)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach assignments',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*' + self.var.fa_client_vlan_id +
                                                                           '.*' + self.var.fa_client_vlan_nsi,
                                                                           exists=False)
        self.suiteUdks.wait_for_backup_sync()
        self.suiteUdks.create_fa_client_vlan_and_nsi(self.tb.dut2_name)

    """
    Test ID 4:
    
    Repeat steps in Test ID 1 and then disable port that connected to FA client.
    
    Verify if fabric attach element and assignments of that client are removed in both primary and backup immediately.
    """

    @mark.t4
    def test_04_verify_sync_after_failover(self):
        self.executionHelper.testSkipCheck()
        print("Unit Test ID 4:")

        self.suiteUdks.verify_neighbors_and_assignments(60)
        self.udks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.dut1_name,
                                                                      self.tb.dut1_isl_dut2_port_c.ifname)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach elements',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*Switch', exists=False)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach assignments',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*' + self.var.fa_client_vlan_id +
                                                                           '.*' + self.var.fa_client_vlan_nsi,
                                                                           exists=False)

        self.udks.hostServicesUdks.networkElementResetDeviceKeywords.start_network_element_failover_and_wait(
            self.tb.dut1_name, max_wait=60, wait_before=10, wait_after_success=10)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name, 'show switch',
                                                                           'Current.*State.*BACKUP', exists=False)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach elements',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*Switch', exists=False)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach assignments',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*' + self.var.fa_client_vlan_id +
                                                                           '.*' + self.var.fa_client_vlan_nsi,
                                                                           exists=False)
        self.suiteUdks.wait_for_backup_sync()
        self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut1_name,
                                                                    self.tb.dut1_isl_dut2_port_c.ifname)

    """
    Test ID 5:
    
    Repeat steps in Test ID 1 and then delete the dynamic vlan learnt from FA client.
    
    Verify if fabric attach assignments of that vlan are removed in both primary and backup immediately.
    """

    @mark.t5
    def test_05_verify_sync_after_failover(self):
        self.executionHelper.testSkipCheck()
        print("Unit Test ID 5:")

        self.suiteUdks.verify_neighbors_and_assignments(60)
        self.udks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.dut1_name, self.var.fa_client_vlan_id)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach assignments',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*' + self.var.fa_client_vlan_id +
                                                                           '.*' + self.var.fa_client_vlan_nsi,
                                                                           exists=False)

        self.udks.hostServicesUdks.networkElementResetDeviceKeywords.start_network_element_failover_and_wait(
            self.tb.dut1_name, max_wait=10)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach assignments',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*' + self.var.fa_client_vlan_id +
                                                                           '.*' + self.var.fa_client_vlan_nsi,
                                                                           exists=False)
        self.suiteUdks.wait_for_backup_sync()

    """
    Test ID 6:
    
    Connect an FA server and client to both MLAG Peers DUT (FA proxy). Configure VLAN-NSI map in FA client.
    
    Verify if all below show commands are in sync between master and backup:
    1) show lldp neighbors
    2) show fabric attach elements
    3) show fabric attach assignments
    """

    @mark.t6
    def test_06_verify_sync_after_failover(self):
        self.executionHelper.testSkipCheck()
        print("Unit Test ID 6:")

        # Remove FA Server and Client vlan configurations before doing LAG configurations
        self.suiteUdks.unconfigure_fa_server(self.tb.dut3_name)
        self.suiteUdks.delete_fa_client_vlan(self.tb.dut2_name)

        self.suiteUdks.enable_required_mlag_setup_ports()
        # Do LAG configurations
        self.suiteUdks.configure_lag_on_required_ports_in_all_duts()
        # Do MLAG configurations on Peer A and B
        self.suiteUdks.configure_mlag_on_peer_a()
        self.suiteUdks.configure_mlag_on_peer_b()

        self.suiteUdks.configure_fa_server(self.tb.dut3_name)
        self.suiteUdks.create_fa_client_vlan_and_nsi(self.tb.dut2_name)
        self.suiteUdks.verify_neighbors_and_assignments(60)
        self.udks.hostServicesUdks.networkElementResetDeviceKeywords.start_network_element_failover_and_wait(
            self.tb.dut1_name, max_wait=60, wait_before=10, wait_after_success=10)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name, 'show switch',
                                                                           'Current.*State.*BACKUP', exists=False)
        self.suiteUdks.verify_neighbors_and_assignments(0)
        self.suiteUdks.wait_for_backup_sync()
        self.suiteUdks.verify_neighbors_and_assignments(0)

        # Remove MLAG configurations on Peer A and B
        self.suiteUdks.unconfigure_mlag_on_peer_a()
        self.suiteUdks.unconfigure_mlag_on_peer_b()

        # Remove LAG configurations
        self.suiteUdks.unconfigure_lag_on_required_ports_in_all_duts()

    """
    Test ID 7:
    
    Repeat steps in Test ID 6 and then disable the port in FA client which is connected to one of the MLAG peers.
    
    Verify if fabric attach assignments of disabled MLAG port is retained in primary and backup.
    Also corresponding lldp and fabric attach neighbor should be removed for that port.
    """

    @mark.t7
    def test_07_verify_sync_after_failover(self):
        self.executionHelper.testSkipCheck()
        print("Unit Test ID 7:")

        # Remove FA Server and Client vlan configurations before doing LAG configurations
        self.suiteUdks.unconfigure_fa_server(self.tb.dut3_name)
        self.suiteUdks.delete_fa_client_vlan(self.tb.dut2_name)

        self.suiteUdks.enable_required_mlag_setup_ports()
        # Do LAG configurations
        self.suiteUdks.configure_lag_on_required_ports_in_all_duts()
        # Do MLAG configurations on Peer A and B
        self.suiteUdks.configure_mlag_on_peer_a()
        self.suiteUdks.configure_mlag_on_peer_b()

        self.suiteUdks.configure_fa_server(self.tb.dut3_name)
        self.suiteUdks.create_fa_client_vlan_and_nsi(self.tb.dut2_name)
        self.suiteUdks.verify_neighbors_and_assignments(60)
        self.udks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(self.tb.dut2_name,
                                                                      self.tb.dut2_isl_dut1_port_c.ifname)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show lldp port ' +
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           ' neighbors',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*' + self.tb.dut2_isl_dut1_port_c.ifname,
                                                                           exists=False, max_wait=160, interval=20)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach elements',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*Switch', exists=False)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach assignments',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*' + self.var.fa_client_vlan_id +
                                                                           '.*' + self.var.fa_client_vlan_nsi +
                                                                           '.*Active')
        self.udks.hostServicesUdks.networkElementResetDeviceKeywords.start_network_element_failover_and_wait(
            self.tb.dut1_name, max_wait=60, wait_before=10, wait_after_success=10)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name, 'show switch',
                                                                           'Current.*State.*BACKUP', exists=False)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach elements',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*Switch', exists=False)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show lldp port ' +
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           ' neighbors',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*' + self.tb.dut2_isl_dut1_port_c.ifname,
                                                                           exists=False)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach assignments',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*' + self.var.fa_client_vlan_id +
                                                                           '.*' + self.var.fa_client_vlan_nsi +
                                                                           '.*Active')
        self.suiteUdks.wait_for_backup_sync()
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach elements',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*Switch', exists=False)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show lldp port ' +
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           ' neighbors',
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '.*' + self.tb.dut2_isl_dut1_port_c.ifname,
                                                                           exists=False)
        self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(self.tb.dut2_name,
                                                                    self.tb.dut2_isl_dut1_port_c.ifname)

        # Remove MLAG configurations on Peer A and B
        self.suiteUdks.unconfigure_mlag_on_peer_a()
        self.suiteUdks.unconfigure_mlag_on_peer_b()

        # Remove LAG configurations
        self.suiteUdks.unconfigure_lag_on_required_ports_in_all_duts()

    """
    Test ID 8:
    
    Repeat steps in Test ID 3 and do failover from master to backup. Once backup comes up do failover once again.
    
    Verify if all below show commands retains entries for all ports in current master node:
    1) show lldp neighbors
    2) show fabric attach elements
    3) show fabric attach assignments
    """

    @mark.t8
    def test_08_verify_sync_after_failover(self):
        self.executionHelper.testSkipCheck()
        print("Unit Test ID 8:")

        # Remove FA Server and Client vlan configurations before doing LAG configurations
        self.suiteUdks.unconfigure_fa_server(self.tb.dut3_name)
        self.suiteUdks.delete_fa_client_vlan(self.tb.dut2_name)

        self.suiteUdks.enable_required_mlag_setup_ports()
        # Do LAG configurations
        self.suiteUdks.configure_lag_on_required_ports_in_all_duts()
        # Do MLAG configurations on Peer A and B
        self.suiteUdks.configure_mlag_on_peer_a()
        self.suiteUdks.configure_mlag_on_peer_b()

        self.suiteUdks.configure_fa_server(self.tb.dut3_name)
        self.suiteUdks.create_fa_client_vlan_and_nsi(self.tb.dut2_name)
        self.suiteUdks.verify_neighbors_and_assignments(60)
        self.udks.hostServicesUdks.networkElementResetDeviceKeywords.start_network_element_failover_and_wait(
            self.tb.dut1_name, max_wait=60, wait_before=10, wait_after_success=10)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name, 'show switch',
                                                                           'Current.*State.*BACKUP', exists=False)
        self.suiteUdks.verify_neighbors_and_assignments(0)
        self.suiteUdks.wait_for_backup_sync()
        self.suiteUdks.verify_neighbors_and_assignments(0)
        self.udks.hostServicesUdks.networkElementResetDeviceKeywords.start_network_element_failover_and_wait(
            self.tb.dut1_name, max_wait=60, wait_before=10, wait_after_success=10)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name, 'show switch',
                                                                           'Current.*State.*BACKUP', exists=False)
        self.suiteUdks.verify_neighbors_and_assignments(0)
        self.suiteUdks.wait_for_backup_sync()
        self.suiteUdks.verify_neighbors_and_assignments(0)

        # Remove MLAG configurations on Peer A and B
        self.suiteUdks.unconfigure_mlag_on_peer_a()
        self.suiteUdks.unconfigure_mlag_on_peer_b()

        # Remove LAG configurations
        self.suiteUdks.unconfigure_lag_on_required_ports_in_all_duts()

    """
    Test ID 9:
    
    Check below statistics commands in backup node before and after failover.
    1) show lldp statistics
    2) show fabric attach statistics
    
    Verify if below error message is displayed in backup before failover:
        "Error: This command can only be executed on Master."
    Verify if above error message is not displayed after failover (backup becomes primary) and statistics are cleared.
    """

    @mark.t9
    def test_09_verify_sync_after_failover(self):
        self.executionHelper.testSkipCheck()
        print("Unit Test ID 9:")

        self.suiteUdks.verify_neighbors_and_assignments(60)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name, 'show lldp port ' +
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           ' statistics',
                                                                           '\\n' + self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '\\s+0', exists=False,
                                                                           ignore_error="Error")
        # Disable advertise so that we can verify if Tx statistics cleared after failover.
        self.lowApis.lldp.lldp_disable_tlv_all(self.tb.dut1_name, self.tb.dut1_isl_dut2_port_c.ifname)
        self.udks.hostServicesUdks.networkElementResetDeviceKeywords.start_network_element_failover_and_wait(
            self.tb.dut1_name, max_wait=10)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name, 'show lldp port ' +
                                                                           self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           ' statistics',
                                                                           '\\n' + self.tb.dut1_isl_dut2_port_c.ifname +
                                                                           '\\s+0', ignore_error="Error")
        self.lowApis.lldp.lldp_enable_tlv_all(self.tb.dut1_name, self.tb.dut1_isl_dut2_port_c.ifname)
        self.suiteUdks.wait_for_backup_sync()

    """
    Test ID 10:
    
    Connect an FA server and client to both MLAG Peers DUT (FA proxy).
    Configure VLAN-NSI map through policy profile configuration on one of the MLAG peer.
    Once MLAG checkpointing is done, unconfigure VLAN-NSI map.
    
    Verify if VLAN-NSI map is checkpointed to MLAG peer's backup node using 
    "show fabric attach assignments" command.
    Once VLAN-NSI map is unconfigured, verify if the map is removed from MLAG peer's backup node.
    """

    @mark.t10
    def test_10_verify_sync_after_failover(self):
        self.executionHelper.testSkipCheck()
        print("Unit Test ID 10:")

        # Remove FA Server and Client vlan configurations before doing LAG configurations
        self.suiteUdks.unconfigure_fa_server(self.tb.dut3_name)
        self.suiteUdks.delete_fa_client_vlan(self.tb.dut2_name)

        self.suiteUdks.enable_required_mlag_setup_ports()
        # Do LAG configurations
        self.suiteUdks.configure_lag_on_required_ports_in_all_duts()
        # Do MLAG configurations on Peer A and B
        self.suiteUdks.configure_mlag_on_peer_a()
        self.suiteUdks.configure_mlag_on_peer_b()

        self.suiteUdks.configure_fa_server(self.tb.dut3_name)
        self.suiteUdks.create_fa_client_vlan_and_nsi(self.tb.dut2_name)
        self.suiteUdks.verify_neighbors_and_assignments(60)

        self.netElement.networkElementCliSend.send_cmd(self.tb.dut4_name, 'configure policy profile ' +
                                                       self.var.policy_profile_id + ' name ' +
                                                       self.var.policy_profile_name + ' pvid-status enable pvid '
                                                       + self.var.policy_vlan_id + ' nsi ' + self.var.policy_vlan_nsi)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut4_name, 'show policy profile ' +
                                                                           self.var.policy_profile_id, 'Profile Index.*'
                                                                           + self.var.policy_profile_id)
        # Associate policy profile to dummy port which is disabled
        self.udks.policyUdks.Create_Port_Admin_Profile_and_Verify_it_Exists(self.tb.dut4_name,
                                                                            self.tb.dut4_isl_dut2_port_b.ifname,
                                                                            self.var.policy_profile_id)
        self.udks.policyUdks.Enable_Policy_and_Verify_it_is_Enabled(self.tb.dut4_name)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut4_name,
                                                                           'show fabric attach assignments',
                                                                           self.var.policy_vlan_id + '.*' +
                                                                           self.var.policy_vlan_nsi + '.*Active',
                                                                           max_wait=120)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach assignments',
                                                                           self.tb.dut1_isl_dut4_port_d.ifname +
                                                                           '.*' + self.var.policy_vlan_id + '.*' +
                                                                           self.var.policy_vlan_nsi + '.*Active',
                                                                           max_wait=30)

        self.udks.hostServicesUdks.networkElementResetDeviceKeywords.start_network_element_failover_and_wait(
            self.tb.dut1_name, max_wait=60, wait_before=10, wait_after_success=10)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name, 'show switch',
                                                                           'Current.*State.*BACKUP', exists=False)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach assignments',
                                                                           self.tb.dut1_isl_dut4_port_d.ifname +
                                                                           '.*' + self.var.policy_vlan_id + '.*' +
                                                                           self.var.policy_vlan_nsi + '.*Active')
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name, 'show switch',
                                                                           'Current.*State.*BACKUP.*(In.*Sync)',
                                                                           max_wait=360, interval=20)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach assignments',
                                                                           self.tb.dut1_isl_dut4_port_d.ifname +
                                                                           '.*' + self.var.policy_vlan_id + '.*' +
                                                                           self.var.policy_vlan_nsi + '.*Active')
        self.lowApis.policy.policy_disable(self.tb.dut4_name)
        self.lowApis.policy.policy_verify_state_disabled(self.tb.dut4_name)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut4_name,
                                                                           'show fabric attach assignments',
                                                                           self.var.policy_vlan_id + '.*' +
                                                                           self.var.policy_vlan_nsi, exists=False)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach assignments',
                                                                           self.tb.dut1_isl_dut4_port_d.ifname +
                                                                           '.*' + self.var.policy_vlan_id + '.*' +
                                                                           self.var.policy_vlan_nsi, exists=False,
                                                                           max_wait=30)

        self.udks.hostServicesUdks.networkElementResetDeviceKeywords.start_network_element_failover_and_wait(
            self.tb.dut1_name, max_wait=60, wait_before=10, wait_after_success=10)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name, 'show switch',
                                                                           'Current.*State.*BACKUP', exists=False)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach assignments',
                                                                           self.tb.dut1_isl_dut4_port_d.ifname +
                                                                           '.*' + self.var.policy_vlan_id + '.*' +
                                                                           self.var.policy_vlan_nsi, exists=False)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name, 'show switch',
                                                                           'Current.*State.*BACKUP.*(In.*Sync)',
                                                                           max_wait=360, interval=20)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut1_name,
                                                                           'show fabric attach assignments',
                                                                           self.tb.dut1_isl_dut4_port_d.ifname +
                                                                           '.*' + self.var.policy_vlan_id + '.*' +
                                                                           self.var.policy_vlan_nsi, exists=False)

        self.udks.policyUdks.Remove_Port_Admin_Profile_and_Verify_it_was_Removed(self.tb.dut4_name,
                                                                                 self.tb.dut4_isl_dut2_port_b.ifname,
                                                                                 self.var.policy_profile_id)
        self.netElement.networkElementCliSend.send_cmd(self.tb.dut4_name, 'unconfigure policy profile ' +
                                                       self.var.policy_profile_id)
        self.netElement.networkElementCliSend.send_cmd_verify_output_regex(self.tb.dut4_name, 'show policy profile ' +
                                                                           self.var.policy_profile_id, 'Profile Index.*'
                                                                           + self.var.policy_profile_id, exists=False)
        # Ideally this dynamic vlan should be removed when policy was disabled on peer (Fix this bug in separate CR).
        self.udks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.dut1_name, self.var.policy_vlan_id,
                                                                ignore_error="Error")

        # Remove MLAG configurations on Peer A and B
        self.suiteUdks.unconfigure_mlag_on_peer_a()
        self.suiteUdks.unconfigure_mlag_on_peer_b()

        # Remove LAG configurations
        self.suiteUdks.unconfigure_lag_on_required_ports_in_all_duts()

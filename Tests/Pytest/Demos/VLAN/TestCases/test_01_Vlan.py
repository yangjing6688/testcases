from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from pytest import mark
from time import sleep

# VLAN Variables
vlan_a = "10"
vlan_b = '11'
vlan_b_name = "test"


@mark.testbed_1_node
class Vlan01Tests:
    
    # [Setup]  Test Case Setup
    @classmethod
    def setup_class(cls):
        try:
            # Create the pytest execution helper
            cls.executionHelper = PytestExecutionHelper()
            
            # Create an instance of the helper class that will read in the test bed yaml file and provide basic methods and variable access.
            # The user can also get to the test bed yaml by using the config dictionary
            cls.tb = PytestConfigHelper(config)
            
            # Create new objects to use in test. Here we will import everything from the default library
            cls.defaultLibrary = DefaultLibrary()
            
            # Create a shorter version for the UDKs
            cls.udks = cls.defaultLibrary.apiUdks
            
            # Call the setup
            cls.udks.setupTeardownUdks.Base_Test_Suite_Setup()
            cls.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(cls.tb.dut1_name, cls.tb.dut1_tgen_port_a.ifname)
            cls.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(cls.tb.dut1_name, cls.tb.dut1_tgen_port_b.ifname)
        except Exception:
            # Setup has failed, so set the flag
            cls.executionHelper.setSetupFailure(True)

    # [Teardown]  Test Case Cleanup
    @classmethod
    def teardown_class(cls):
        cls.udks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(cls.tb.dut1_name, cls.tb.dut1_tgen_port_a.ifname)
        cls.udks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(cls.tb.dut1_name, cls.tb.dut1_tgen_port_b.ifname)
        cls.udks.vlanUdks.Clear_PVID_and_Verify_it_is_Cleared(cls.tb.dut1_name, cls.tb.dut1_tgen_port_a.ifname, vlan_a)
        cls.udks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(cls.tb.dut1_name, vlan_a)
        cls.udks.setupTeardownUdks.Base_Test_Suite_Cleanup()
       
    # """ Test Cases """
    @mark.p1
    def test_01_vlan(self):
        # Helper to see if the setup failed and skip the test
        self.executionHelper.testSkipCheck()
        """  Test Objective:  Create a VLAN and verify was properly configured using keyword and traffic. """
        port_list = [self.tb.dut1_tgen_port_a.ifname, self.tb.dut1_tgen_port_b.ifname]
        self.udks.vlanUdks.Create_VLAN_and_Add_Ports_Untagged_then_Verify(self.tb.dut1_name, vlan_a, port_list)
    
        # Create the packet information
        packet_a = 'packetA'
        packet_b = 'packetB'
        tgen_port_a = self.tb.createTgenPort(self.tb.tgen1_name, self.tb.tgen_dut1_port_a.ifname)
        tgen_port_b = self.tb.createTgenPort(self.tb.tgen1_name, self.tb.tgen_dut1_port_b.ifname)
        self.udks.trafficGenerationUdks.Create_Ethernet2_Packet(packet_a, '00:22:22:22:22:22', '00:11:11:11:11:11')
        self.udks.trafficGenerationUdks.Create_Ethernet2_Packet(packet_b, '00:11:11:11:11:11', '00:22:22:22:22:22')
        self.udks.trafficGenerationUdks.Transmit_Traffic_Bidirectionally_and_Verify_it_was_Received(tgen_port_a, 
                                                                                                    tgen_port_b, 
                                                                                                    packet_a, 
                                                                                                    packet_b, 
                                                                                                    packet_b, 
                                                                                                    packet_a,
                                                                                                    tx_count=10)

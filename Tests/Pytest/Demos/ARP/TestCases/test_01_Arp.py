from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from time import sleep
from pytest import mark

# VLAN Variables
vlan_default = "1"
vlan_a = "10"
vlan_mgmt = "4000"

# Interface Variables
vlan_a_ip_address = "10.10.10.66"
vlan_a_ip_mask = "255.255.255.0"
vlan_a_ip_address_2 = "10.10.10.67"
vlan_a_ip_mask_2 = "255.255.255.0"

@mark.testbed_2_node
class ArpTests:
    
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
            cls.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(cls.tb.dut1_name, cls.tb.dut1_isl_dut2_port_a.ifname)
            cls.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(cls.tb.dut2_name, cls.tb.dut2_isl_dut1_port_a.ifname)
            cls.udks.portUdks.Verify_Xstp_Forwarding_State(cls.tb.dut1_name,cls.tb.dut1_isl_dut2_port_a.ifname)
            cls.udks.portUdks.Verify_Xstp_Forwarding_State(cls.tb.dut2_name,cls.tb.dut2_isl_dut1_port_a.ifname)
            cls.udks.vlanUdks.Create_VLAN_and_Add_Ports_Untagged_then_Verify(cls.tb.dut1_name, vlan_a, cls.tb.dut1_isl_dut2_port_a.ifname)
            cls.udks.vlanUdks.Create_VLAN_and_Add_Ports_Untagged_then_Verify(cls.tb.dut2_name, vlan_a, cls.tb.dut2_isl_dut1_port_a.ifname)
            cls.defaultLibrary.apiLowLevelApis.interface.interface_set_ipv4_primary_addr_netmask(cls.tb.dut1_name, vlan_a, vlan_a_ip_address, vlan_a_ip_mask)
            cls.defaultLibrary.apiLowLevelApis.interface.interface_set_ipv4_primary_addr_netmask(cls.tb.dut2_name, vlan_a, vlan_a_ip_address_2, vlan_a_ip_mask_2)
            cls.defaultLibrary.apiLowLevelApis.interface.interface_enable_interface(cls.tb.dut1_name, vlan_a)
            cls.defaultLibrary.apiLowLevelApis.interface.interface_enable_interface(cls.tb.dut2_name, vlan_a)
            sleep(25)
            cls.defaultLibrary.apiLowLevelApis.hostUtils.host_address_should_be_reachable(cls.tb.dut1_name, vlan_a_ip_address_2)
        except Exception:
            cls.executionHelper.setSetupFailure(True)

    # [Teardown]  Test Case Cleanup
    @classmethod
    def teardown_class(cls):
        cls.udks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(cls.tb.dut1_name, cls.tb.dut1_isl_dut2_port_a.ifname)
        cls.udks.portUdks.Disable_Port_and_Validate_Port_is_Disabled(cls.tb.dut2_name, cls.tb.dut2_isl_dut1_port_a.ifname)
        cls.udks.vlanUdks.Clear_PVID_and_Verify_it_is_Cleared(cls.tb.dut1_name, cls.tb.dut1_isl_dut2_port_a.ifname, vlan_a)
        cls.udks.vlanUdks.Clear_PVID_and_Verify_it_is_Cleared(cls.tb.dut2_name, cls.tb.dut2_isl_dut1_port_a.ifname, vlan_a)
        cls.defaultLibrary.apiLowLevelApis.interface.interface_disable_interface(cls.tb.dut1_name, vlan_a)
        cls.defaultLibrary.apiLowLevelApis.interface.interface_disable_interface(cls.tb.dut2_name, vlan_a)
        cls.udks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(cls.tb.dut1_name, vlan_a)
        cls.udks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(cls.tb.dut2_name, vlan_a)
        cls.udks.setupTeardownUdks.Base_Test_Suite_Cleanup()

    # """ Test Cases """
    def test_01_arp(self):
        self.executionHelper.testSkipCheck()
        
        """ Get the mac address on the dut_a_vlan to be used in the verify/check methods """
        return_value = self.defaultLibrary.apiLowLevelApis.arp.arp_verify_entry_exists(self.tb.dut2_name, vlan_a_ip_address, get_only=True)
        return_dict = return_value[1]
        dut_a_vlan_mac_address = return_dict.get('ret_mac')
        
        ''' Log  (Step 1) Clear Network Element 2's ARP table. '''
        self.defaultLibrary.apiLowLevelApis.arp.arp_clear_all_entries(self.tb.dut2_name)
        
        ''' Log  (Verification 1) Verify that Network Element 1's ARP entry does not exist in Network Element 2's ARP table. '''
        self.defaultLibrary.apiLowLevelApis.arp.arp_verify_entry_does_not_exist(self.tb.dut2_name, vlan_a_ip_address, dut_a_vlan_mac_address, vlan_a)
        
        ''' Log  (Step 2) Populate the ARP entry in Network Element 2's ARP table by pinging it's interface from Network Element 1. '''
        self.defaultLibrary.apiLowLevelApis.hostUtils.host_address_should_be_reachable(self.tb.dut1_name, vlan_a_ip_address_2)
        
        ''' Log  (Verify Network Element 1's ARP entry exists in Network Element 2's ARP table. '''
        self.defaultLibrary.apiLowLevelApis.arp.arp_verify_entry_exists(self.tb.dut2_name, vlan_a_ip_address, dut_a_vlan_mac_address, vlan_a)
        
        ''' Log  (Step 3) Clear Network Element 1's ARP entry from Network Element 2's ARP table. '''
        self.defaultLibrary.apiLowLevelApis.arp.arp_delete_entry(self.tb.dut2_name, vlan_a_ip_address)
        
        ''' Log  (Verification 3) Verify that Network Element 1's ARP entry is no longer in Network Element 2's ARP table . '''
        self.defaultLibrary.apiLowLevelApis.arp.arp_verify_entry_does_not_exist(self.tb.dut2_name, vlan_a_ip_address, dut_a_vlan_mac_address, vlan_a)

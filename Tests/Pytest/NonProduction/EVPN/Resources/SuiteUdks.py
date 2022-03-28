from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
#----------------------------------------------------------------------------------------------------------
#   Setup/Teardown Keywords
#----------------------------------------------------------------------------------------------------------

class SuiteUdk():
    
    def __init__(self):
        self.defaultLibrary = DefaultLibrary()
        # Create a shorter version for the UDKs
        self.udks = self.defaultLibrary.apiUdks
        # Create a shorter version for cli send
        self.cliSend = self.defaultLibrary.deviceNetworkElement.networkElementCliSend

    ###########################################################################
    # These are predefined configurations which can be setup and torn down as
    # needed
    ###########################################################################

    ###########################################################################
    # Confiruration 1:
    # This is a single virtual network configured on two VTEPS mapped to the
    # same vlan.
    # Auto-peering is used for the underlay.
    ###########################################################################
    def setup_AP_and_one_vnet_cfg(self,dut_name,rtrid,asnum,vlan_name,vlan_tag,nsi,vlan_port_list,test_port_list):
        # auto-peering
        self.defaultLibrary.apiLowLevelApis.bgp.bgp_set_auto_peering(dut_name,asnum,rtrid)
        # tenant vlan
        self.udks.vlanUdks.Create_VLAN_with_Name_and_Add_Ports_Tagged_then_Verify(dut_name,vlan_name,vlan_tag,vlan_port_list)
        # map the nsi onto the vlan
        cmd = "configure vlan " + vlan_name + " add nsi " + nsi
        self.cliSend.send_cmd(dut_name,cmd)
        # Start by disabling all ports
        self.cliSend.send_cmd(dut_name,"disable port all")
        # Enable the ports used for the test.
        for port in test_port_list:
            self.udks.portUdks.Enable_Port_and_Validate_Port_is_Enabled(dut_name,port)
        print("setup_AP_and_one_vnet_cfg")

    # UnConfigure the DUTs to run the test
    def teardown_AP_and_one_vlan_cfg(self,dut_name,vlan_tag):
        # auto-peering
        self.defaultLibrary.apiLowLevelApis.bgp.bgp_clear_auto_peering(dut_name)
        # tenant vlan, note nsi config is also destroyed
        self.udks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(dut_name,vlan_tag)
        # disable all ports
        self.cliSend.send_cmd(dut_name,"disable port all")
        print("teardown_AP_and_one_vlan")
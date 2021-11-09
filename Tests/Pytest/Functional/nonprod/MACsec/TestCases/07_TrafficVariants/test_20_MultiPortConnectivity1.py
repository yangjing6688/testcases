from Tests.Pytest.Functional.nonprod.MACsec.Resources.MACsecBase import MACsecBase
from pytest import mark
from pytest import fixture

@fixture()
def test_setup_teardown(request):
    request.instance.Disable_All_Macsec_Ports()
    def teardown():
        request.instance.Reenable_Base_Macsec_Ports()
       
    request.addfinalizer(teardown)

class MultiPortConnectivityTests(MACsecBase):

    # *** Test_Cases ***
    def test_07_20_Multiport_Connectivity_with_MACsec_Disabled(self, test_setup_teardown):
        """ Verify_connectivity_between_multiple_DUT1_to_DUT2_ports_with
        ...              MACsec_disabled.  This_test_validates_the_inter-switch_links
        ...              are_installed_correctly_and_that_the_traffic_generators
        ...              are_operational. """
        length = len(self.tb.dut1.ports)
        for index in range(length):
            self.Enable_Ports_and_Add_to_Traffic_Vlan(index)
            self.Verify_Ports_Operational(index)
    
            self.suiteUdks.Verify_Connectivity()
    
            self.Disable_Ports_and_Remove_from_Traffic_Vlan(index)
    
    @mark.BUILD
    @mark.NIGHTLY
    def test_07_21_Multiport_Connectivity_with_MACsec_Enabled(self, test_setup_teardown):
        """ Verify_connectivity_between_multiple_DUT1_to_DUT2_ports
        ...              with_MACsec_enabled. """
        length = len(self.tb.dut1.ports)
        for index in range(length):
            self.Enable_Ports_and_Add_to_Traffic_Vlan(index)
            self.Macsec_Enable_and_Verify_Secure(index)
    
            # Bidirectional_garbage_to_populate_FDB (required_for_5420)
            #  run_keyword_and_ignore_error_
            self.suiteUdks.Transmit_Test(tx_count=181, prime_packet_pump=True, ignore_error=True)
    
            # The_real_test
            self.suiteUdks.Verify_Connectivity()
            self.Verify_No_Macsec_Errors_on_Ports(index)
    
            self.Macsec_Disable(index)
            self.Disable_Ports_and_Remove_from_Traffic_Vlan(index)
    
    
    # *** keywords ***
    def Disable_All_Macsec_Ports(self):
        self.defaultLibrary.apiLowLevelApis.port.port_disable_state(self.tb.dut1.name, self.tb.dut1.ports)
        self.defaultLibrary.apiLowLevelApis.port.port_disable_state(self.tb.dut2.name, self.tb.dut2.ports)
    
    def Reenable_Base_Macsec_Ports(self):
        self.defaultLibrary.apiLowLevelApis.port.port_enable_state(self.tb.dut1.name, self.tb.dut1.port)
        self.defaultLibrary.apiLowLevelApis.port.port_enable_state(self.tb.dut2.name, self.tb.dut2.port)
    
    def Enable_Ports_and_Add_to_Traffic_Vlan(self, index):
        dut1_port = self.tb.dut1.ports[index]
        dut2_port = self.tb.dut2.ports[index]
        self.defaultLibrary.apiLowLevelApis.port.port_enable_state(self.tb.dut1.name, dut1_port)
        self.defaultLibrary.apiLowLevelApis.port.port_enable_state(self.tb.dut2.name, dut2_port)
        self.suiteUdks.Add_Port_to_Traffic_VLAN_Tagged(self.tb.dut1.name, dut1_port)
        self.suiteUdks.Add_Port_to_Traffic_VLAN_Tagged(self.tb.dut2.name, dut2_port)
    
    def Disable_Ports_and_Remove_from_Traffic_Vlan(self, index):
        dut1_port = self.tb.dut1.ports[index]
        dut2_port = self.tb.dut2.ports[index]
        self.suiteUdks.Remove_Port_from_Traffic_VLAN_Tagged(self.tb.dut1.name, dut1_port)
        self.suiteUdks.Remove_Port_from_Traffic_VLAN_Tagged(self.tb.dut2.name, dut2_port)
        self.defaultLibrary.apiLowLevelApis.port.port_disable_state(self.tb.dut1.name, dut1_port)
        self.defaultLibrary.apiLowLevelApis.port.port_disable_state(self.tb.dut2.name, dut2_port)
    
    def  Macsec_Enable_and_Verify_Secure(self, index):
        dut1_port = self.tb.dut1.ports[index]
        dut2_port = self.tb.dut2.ports[index]
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(self.tb.dut1.name, self.tb.dut1.ca, dut1_port)
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(self.tb.dut2.name, self.tb.dut1.ca, dut2_port)
        self.suiteUdks.Macsec_Verify_Port_Connect_Secure(self.tb.dut1.name, dut1_port)
        self.suiteUdks.Macsec_Verify_Port_Connect_Secure(self.tb.dut2.name, dut2_port)
    
    def  Macsec_Disable(self, index):
        dut1_port = self.tb.dut1.ports[index]
        dut2_port = self.tb.dut2.ports[index]
        self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut1.name, self.tb.dut1.ca, dut1_port)
        self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut2.name, self.tb.dut1.ca, dut2_port)
    
    def Verify_Ports_Operational(self, index):
        dut1_port = self.tb.dut1.ports[index]
        dut2_port = self.tb.dut2.ports[index]
        self.defaultLibrary.apiLowLevelApis.port.port_verify_operational(self.tb.dut1.name, dut1_port, wait_for=True, wait_max=10)
        self.defaultLibrary.apiLowLevelApis.port.port_verify_operational(self.tb.dut2.name, dut2_port, wait_for=True, wait_max=10)
    
    def  Verify_No_Macsec_Errors_on_Ports(self, index):
        dut1_port = self.tb.dut1.ports[index]
        dut2_port = self.tb.dut2.ports[index]
        self.suiteUdks.Verify_No_Macsec_Errors_on_Port(self.tb.dut1.name, dut1_port)
        self.suiteUdks.Verify_No_Macsec_Errors_on_Port(self.tb.dut2.name, dut2_port)

from Tests.Pytest.Functional.nonprod.MACsec.Resources.MACsecBase import MACsecBase
from pytest import mark
from pytest import fixture
import time

@fixture()
def test_setup_teardown(request):
    request.instance.suiteUdks.Add_Port_to_Traffic_VLAN(request.instance.tb.dut1.name, request.instance.tb.dut1.port)
    request.instance.suiteUdks.Add_Port_to_Traffic_VLAN(request.instance.tb.dut2.name, request.instance.tb.dut2.port)
    
    def teardown():
        request.instance.suiteUdks.Remove_Port_from_Traffic_VLAN(request.instance.tb.dut1.name, request.instance.tb.dut1.port)
        request.instance.suiteUdks.Remove_Port_from_Traffic_VLAN(request.instance.tb.dut2.name, request.instance.tb.dut2.port)
    request.addfinalizer(teardown)
    
class BasicConnectivityTests(MACsecBase):

    def test_01_40_Disable_MACsec_on_Both_DUTs_and_Verify_Connectivity(self, test_setup_teardown):
        """ Verify_DUTs_are_properly_connected_to_eachother_and_to_the
            traffic_generator_by_running_a_ping_test_with_MACsec_disabled.
            ISL_traffic_will_be_in-the-clear. """
    
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_disabled_on_port(self.tb.dut1.name, self.tb.dut1.port)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_disabled_on_port(self.tb.dut2.name, self.tb.dut2.port)
        self.defaultLibrary.apiLowLevelApis.port.port_verify_operational(self.tb.dut1.name, self.tb.dut1.port, wait_for=True, wait_max=10)
        self.defaultLibrary.apiLowLevelApis.port.port_verify_operational(self.tb.dut2.name, self.tb.dut2.port, wait_for=True, wait_max=10)
        self.suiteUdks.Verify_Connectivity()
    
    @mark.NIGHTLY
    def test_01_41_Enable_MACsec_on_Both_DUTs_and_Verify_Connectivity(self, test_setup_teardown):
        """ Enable_MACsec_on_both_DUT_ports_and_verify_connectivity_with
            a_ping_test. ISL_traffic_will_be_encrypted. """
    
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(self.tb.dut1.name, self.tb.dut1.ca, self.tb.dut1.port)
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(self.tb.dut2.name, self.tb.dut2.ca, self.tb.dut2.port)
        self.suiteUdks.Macsec_Verify_Port_Connect_Secure(self.tb.dut1.name, self.tb.dut1.port)
        self.suiteUdks.Macsec_Verify_Port_Connect_Secure(self.tb.dut2.name, self.tb.dut2.port)
        self.suiteUdks.Verify_Connectivity()
        # HACK: Xflow_can't_handle_ICMP
        # Ping_Test
    
        self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut1.name, self.tb.dut1.ca, self.tb.dut1.port)
        self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut2.name, self.tb.dut2.ca, self.tb.dut2.port)
    
    @mark.NIGHTLY
    def test_01_42_Enable_MACsec_on_One_DUT_and_Verify_No_Connectivity(self, test_setup_teardown):
        """ Enable_MACsec_on_self.tb.dut1_and_disable_on_self.tb.dut2. Verify
            self.tb.dut1_link_held_down_by_MACsec, but_self.tb.dut2_links_is_up.
            Verify_ping_test_fails.  ISL_traffic_will_be_blocked. """
    
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(self.tb.dut1.name, self.tb.dut1.ca, self.tb.dut1.port)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_disabled_on_port(self.tb.dut2.name, self.tb.dut2.port)
        self.suiteUdks.Macsec_Verify_Port_Connect_Pending(self.tb.dut1.name, self.tb.dut1.port)
        time.sleep(2)
        self.suiteUdks.Verify_No_Connectivity()
        self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut1.name, self.tb.dut1.ca, self.tb.dut1.port)



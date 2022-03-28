from Tests.Pytest.NonProduction.MACsec.Resources.MACsecBase import MACsecBase
from pytest import mark
from pytest import fixture
import time

@fixture()
def test_setup_teardown(request):
    request.instance.suiteUdks.Add_Port_to_Traffic_VLAN(request.instance.tb.dut1.name, request.instance.tb.dut1.port)
    request.instance.suiteUdks.Add_Port_to_Traffic_VLAN(request.instance.tb.dut2.name, request.instance.tb.dut2.port)
    
    def teardown():
        request.instance.suiteUdks.Disable_and_Verify_Macsec_on_Port(request.instance.tb.dut1.name,
                                                                     request.instance.tb.config.ca128,
                                                                     request.instance.tb.dut1.port)
        request.instance.suiteUdks.Disable_and_Verify_Macsec_on_Port(request.instance.tb.dut2.name,
                                                                     request.instance.tb.config.ca128_bad_ckn,
                                                                     request.instance.tb.dut2.port)
        request.instance.suiteUdks.Remove_Port_from_Traffic_VLAN(request.instance.tb.dut1.name, request.instance.tb.dut1.port)
        request.instance.suiteUdks.Remove_Port_from_Traffic_VLAN(request.instance.tb.dut2.name, request.instance.tb.dut2.port)
    request.addfinalizer(teardown)

    
class MismatchedPSKsTests(MACsecBase):
    
    @mark.NIGHTLY
    def test_01_50_Mismatch_CKNs_and_Verify_No_Connectivity(self, test_setup_teardown):
        """ Configure_different_CAK_Names (CKN) but_same_CAK_keys. Verify
        ...              ping_test_fails.  ISL_traffic_will_be_blocked. """
       
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(self.tb.dut1.name,
                                                        self.tb.config.ca128,
                                                        self.tb.dut1.port)
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(self.tb.dut2.name,
                                                        self.tb.config.ca128_bad_ckn,
                                                        self.tb.dut2.port)
    
        self.suiteUdks.Macsec_Verify_Port_Connect_Pending(self.tb.dut1.name, 
                                                          self.tb.dut1.port)
        self.suiteUdks.Macsec_Verify_Port_Connect_Pending(self.tb.dut2.name,
                                                          self.tb.dut2.port)
    
        self.suiteUdks.Verify_No_Connectivity()

    
    @mark.NIGHTLY
    @mark.BUILD
    def test_01_51_Mismatch_CAKs_and_Verify_No_Connectivity(self, test_setup_teardown):
        """ Configure_same_CAK_Names (CKN) but_different_CAK_keys. Verify
        ...              ping_test_fails.  ISL_traffic_will_be_blocked. """
    
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(self.tb.dut1.name, 
                                                        self.tb.config.ca128,
                                                        self.tb.dut1.port)
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(self.tb.dut2.name,
                                                        self.tb.config.ca128_bad_cak,
                                                        self.tb.dut2.port)
    
        self.suiteUdks.Macsec_Verify_Port_Connect_Pending(self.tb.dut1.name, 
                                                          self.tb.dut1.port)
        self.suiteUdks.Macsec_Verify_Port_Connect_Pending(self.tb.dut2.name, 
                                                          self.tb.dut2.port)
    
        self.suiteUdks.Verify_No_Connectivity()


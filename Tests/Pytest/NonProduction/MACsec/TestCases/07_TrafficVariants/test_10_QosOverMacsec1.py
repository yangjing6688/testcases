from Tests.Pytest.NonProduction.MACsec.Resources.MACsecBase import MACsecBase
from pytest import mark
from pytest import fixture

@fixture()
def test_setup_teardown(request):
    request.instance.Configure_DUTs_for_Traffic()
    def teardown():
        request.instance.Unconfigure_DUTs_for_Traffic()
       
    request.addfinalizer(teardown)

class QosOverMacsecTests(MACsecBase):

    def test_07_10_VLAN_Priority_MACsec_Disabled(self, test_setup_teardown):
        """ Verify_802.1Q_Priority_Traffic_without_MACsec """
    
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_disabled_on_port(self.tb.dut1.name, self.tb.dut1.port)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_disabled_on_port(self.tb.dut2.name, self.tb.dut2.port)
        prio_list = [0,1,5,7]
        for prio in prio_list:
            self.suiteUdks.Transmit_Test_with_Priority(exp_priority=prio)
      
    @mark.NIGHTLY
    @mark.BUILD
    def test_07_11_VLAN_Priority_MACsec_Enabled(self, test_setup_teardown):
        """ Verify_802.1Q_Priority_Traffic_with_MACsec """
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(self.tb.dut1.name, self.tb.dut1.ca, self.tb.dut1.port)
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(self.tb.dut2.name, self.tb.dut1.ca, self.tb.dut2.port)
        prio_list = [7,6,5,4,1,0]
        for prio in prio_list:
            self.suiteUdks.Transmit_Test_with_Priority(exp_priority=prio)
            self.suiteUdks.Verify_No_Macsec_Errors_on_Port(self.tb.dut1.name, self.tb.dut1.port)
            self.suiteUdks.Verify_No_Macsec_Errors_on_Port(self.tb.dut2.name, self.tb.dut2.port)
        self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut1.name, self.tb.dut1.ca, self.tb.dut1.port)
        self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut2.name, self.tb.dut1.ca, self.tb.dut2.port)
    
    
    # *** keywords ***
    def Configure_DUTs_for_Traffic(self):
        # add_ISL_to_tagged_vlan
        self.suiteUdks.Add_Port_to_Traffic_VLAN_Tagged(self.tb.dut1.name, self.tb.dut1.port)
        self.suiteUdks.Add_Port_to_Traffic_VLAN_Tagged(self.tb.dut2.name, self.tb.dut2.port)
        # move_tgen_to_tagged_vlan
        self.defaultLibrary.apiUdks.vlanUdks.Remove_Ports_from_Untagged_Egress_for_VLAN_and_Verify_it_is_Removed(self.tb.dut1.name, self.tb.config.vlan_traffic, self.tb.dut1.tg_port)
        self.defaultLibrary.apiUdks.vlanUdks.Remove_Ports_from_Untagged_Egress_for_VLAN_and_Verify_it_is_Removed(self.tb.dut2.name, self.tb.config.vlan_traffic, self.tb.dut2.tg_port)
        self.suiteUdks.Add_Port_to_Traffic_VLAN_Tagged(self.tb.dut1.name, self.tb.dut1.tg_port)
        self.suiteUdks.Add_Port_to_Traffic_VLAN_Tagged(self.tb.dut2.name, self.tb.dut2.tg_port)
    
    def Unconfigure_DUTs_for_Traffic(self):
        # remove_ISL_to_tagged_vlan
        self.suiteUdks.Add_Port_to_Traffic_VLAN_Tagged(self.tb.dut1.name, self.tb.dut1.port)
        self.suiteUdks.Remove_Port_from_Traffic_VLAN_Tagged(self.tb.dut1.name, self.tb.dut1.port)
        self.suiteUdks.Remove_Port_from_Traffic_VLAN_Tagged(self.tb.dut2.name, self.tb.dut2.port)
        # move_tgen_to_untagged_vlan
        self.defaultLibrary.apiUdks.vlanUdks.Remove_Ports_from_Tagged_Egress_for_VLAN_and_Verify_it_is_Removed(self.tb.dut1.name, self.tb.config.vlan_traffic, self.tb.dut1.tg_port)
        self.defaultLibrary.apiUdks.vlanUdks.Remove_Ports_from_Tagged_Egress_for_VLAN_and_Verify_it_is_Removed(self.tb.dut2.name, self.tb.config.vlan_traffic, self.tb.dut2.tg_port)
        self.suiteUdks.Add_Port_to_Traffic_VLAN(self.tb.dut1.name, self.tb.dut1.tg_port)
        self.suiteUdks.Add_Port_to_Traffic_VLAN(self.tb.dut2.name, self.tb.dut2.tg_port)

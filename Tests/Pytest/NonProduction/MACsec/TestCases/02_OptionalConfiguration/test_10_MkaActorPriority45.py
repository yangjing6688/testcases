from Tests.Pytest.NonProduction.MACsec.Resources.MACsecBase import MACsecBase
from pytest import mark
from pytest import fixture


@fixture()
def test_setup_teardown(request):
    def teardown():
        request.instance.suiteUdks.Disable_and_Verify_Macsec_Connection(request.instance.tb.dut1.name, 
                                                                        request.instance.tb.dut1.port, 
                                                                        request.instance.tb.dut2.name, 
                                                                        request.instance.tb.dut2.port, 
                                                                        request.instance.tb.config.ca128)
    request.addfinalizer(teardown)

# Test Template  MKA Actor Priority Test
#
# *** Test Cases ***
#                            Confidentiality Offsets
#                             DUT1  DUT2
# Test Name                   Prio  Prio
#---------------------------  ----  ----
# 02.10 Default Priority          16    16
    # [Tags]  NIGHTLY
# 02.11 DUT1 Higher                2    16
    # [Tags]  NIGHTLY
# 02.12 DUT2 Higher               16     5
    # [Tags]  NIGHTLY  BUILD
# 02.13 Same Priority            100   100
    # [Tags]  NIGHTLY

# *** keywords ***
class MkaActorProirityTests(MACsecBase):

    @mark.NIGHTLY
    @mark.parametrize('dut1_prio,dut2_prio', [
                                                ('16', '16'),
                                                ('2', '16'),
                                                ('16', '5'),
                                                ('100', '100'),
                                            ])
    def test_MKA_Actor_Priority(self, dut1_prio, dut2_prio, test_setup_teardown):
        """ Configure DUT1 and DUT2 with different (or the same) MKA Actor Priority
        ...              and verify the correct DUT is elected as Key Server. """
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_set_mka_actor_priority(self.tb.dut1.name, 
                                                                               dut1_prio, 
                                                                               self.tb.dut1.port)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_set_mka_actor_priority(self.tb.dut2.name, 
                                                                               dut2_prio, 
                                                                               self.tb.dut2.port)
        self.suiteUdks.Create_and_Verify_Macsec_Connection(self.tb.dut1.name, 
                                                           self.tb.dut1.port, 
                                                           self.tb.dut2.name, 
                                                           self.tb.dut2.port, 
                                                           self.tb.config.ca128)
    
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_port_actor_priority(self.tb.dut1.name, 
                                                                                   self.tb.dut1.port, 
                                                                                   dut1_prio)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_port_actor_priority(self.tb.dut2.name, 
                                                                                   self.tb.dut2.port, 
                                                                                   dut2_prio)
        self.Macsec_Verify_Key_Server(dut1_prio, dut2_prio)
    
    def Determine_Key_Server(self, dut1_prio, dut2_prio):
        """ Given two MKA ports determine which one should be elected
        ...              as Key Server.  Per IEEE802.1X-2010, the actor with the
        ...              higher priority (lower number) should be elected.  If the
        ...              priorities are equal, the port with the lower MAC address
        ...              will be elected as key server. """
        
        d1p = int(dut1_prio)
        d2p = int(dut2_prio)
        if (d1p < d2p):
            return  self.tb.dut1, self.tb.dut2
            
        if (d1p > d2p):
            return self.tb.dut2, self.tb.dut1
        if (self.tb.dut1.host_mac < self.tb.dut2.host_mac):
            return self.tb.dut1, self.tb.dut2
        if (self.tb.dut1.host_mac > self.tb.dut2.host_mac):   
            return self.tb.dut2, self.tb.dut1
        else:
            pytest.fail("Cannot determine Key Server because actor priorities and Host MACs are identical")
            
    def Macsec_Verify_Key_Server(self, dut1_prio, dut2_prio):
        key_server, not_key_server = self.Determine_Key_Server(dut1_prio, dut2_prio)
        print("DUT " + key_server.name + " is expected to be the Key Server")
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_self_elected_key_server(key_server.name, key_server.port)
        print("DUT " + not_key_server.name + " is expected to NOT be the Key Server")
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_peer_elected_key_server(not_key_server.name, not_key_server.port)

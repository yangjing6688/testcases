from Tests.Pytest.NonProduction.MACsec.Resources.MACsecBase import MACsecBase
from pytest import mark
from pytest import fixture

@fixture()
def test_setup_teardown(request):
    request.instance.suiteUdks.Add_Port_to_Traffic_VLAN(request.instance.tb.dut1.name, request.instance.tb.dut1.port)
    request.instance.suiteUdks.Add_Port_to_Traffic_VLAN(request.instance.tb.dut2.name, request.instance.tb.dut2.port)
    
    def teardown():
        request.instance.suiteUdks.Disable_and_Verify_Macsec_on_Port(request.instance.tb.dut1.name, request.instance.tb.config.ca256, request.instance.tb.dut1.port)
        request.instance.suiteUdks.Disable_and_Verify_Macsec_on_Port(request.instance.tb.dut2.name, request.instance.tb.config.ca256, request.instance.tb.dut2.port)
        request.instance.suiteUdks.Remove_Port_from_Traffic_VLAN(request.instance.tb.dut1.name, request.instance.tb.dut1.port)
        request.instance.suiteUdks.Remove_Port_from_Traffic_VLAN(request.instance.tb.dut2.name, request.instance.tb.dut2.port)
        request.instance.suiteUdks.Macsec_Set_Pending_PN_Exhaustion_to_Default(request.instance.tb.dut1.name)
    request.addfinalizer(teardown)
    
class SAKRolloverTests(MACsecBase):

    @mark.NIGHTLY
    def test_01_60_SAK_Rollover(self, test_setup_teardown):
        """  Verify_SAK_rolls_over_once_as_a_result_of_bidirectional_traffic
        ...              exceeding_a_Pending_PN_Exhaustion_value_of_2000 (lowered_from
        ...              0xC0000000_by_a_debug_command). """
        self.suiteUdks.Macsec_Set_Pending_PN_Exhaustion(self.tb.dut1.name, 2000)
        self.suiteUdks.Create_and_Verify_Macsec_Connection_DUT1_Key_Server(self.tb.dut1.name, 
                                                                           self.tb.dut1.port, 
                                                                           self.tb.dut2.name, 
                                                                           self.tb.dut2.port, 
                                                                           self.tb.config.ca256)
        self.Verify_Port_Key_Numbers(1)
        self.Verify_Port_Association_Numbers(0)
        self.suiteUdks.Transmit_Test(tx_count=2100)
        self.Verify_Port_Key_Numbers(2)
        self.Verify_Port_Association_Numbers(1)
        
        # self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut1.name, self.tb.config.ca256, self.tb.dut1.port)
        # self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut2.name, self.tb.config.ca256, self.tb.dut2.port)
        
        
    def test_01_61_SAK_Rollover_by_Tx_PN_Exhaustion(self, test_setup_teardown):
        """  Verify_that_DUT1_key_server_will_roll_the_SAK_when_the
        ...              transmitted_MKPDU_Packet_Number (PN) exceeds_the_debug_threshold.
        ...              NOTE: requires_manual_FDB_entries_on_DUT1 """
        
        # to_learn_traffic_before_MACsec_is_enabled
        self.suiteUdks.Transmit_Test(tx_count=2100)
        
        self.suiteUdks.Macsec_Set_Pending_PN_Exhaustion(self.tb.dut1.name, 2000)
        self.suiteUdks.Create_and_Verify_Macsec_Connection_DUT1_Key_Server(self.tb.dut1.name, 
                                                                           self.tb.dut1.port, 
                                                                           self.tb.dut2.name, 
                                                                           self.tb.dut2.port, 
                                                                           self.tb.config.ca256)
                                                                           
        self.Verify_Port_Key_Numbers(1)
        self.Verify_Port_Association_Numbers(0)
        # Send_packets_from_DUT1_to_DUT2
        self.suiteUdks.Transmit_Test(tx_count=2100, tx_count_b=0) 
        self.Verify_Port_Key_Numbers(2)
        self.Verify_Port_Association_Numbers(1)
        
        # self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut1.name, self.tb.config.ca256, self.tb.dut1.port)
        # self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut2.name, self.tb.config.ca256, self.tb.dut2.port)
        
        
    def test_01_62_SAK_Rollover_by_Rx_PN_Exhaustion(self, test_setup_teardown):
        """  Verify_that_DUT1_key_server_will_roll_the_SAK_when_the
        ...              received_MKPDU_Packet_Number (PN) exceeds_the_debug_threshold. """
        
        # to_learn_traffic_before_MACsec_is_enabled
        self.suiteUdks.Transmit_Test(tx_count=2100)
        
        self.suiteUdks.Macsec_Set_Pending_PN_Exhaustion(self.tb.dut1.name, 2000)
        self.suiteUdks.Create_and_Verify_Macsec_Connection_DUT1_Key_Server(self.tb.dut1.name, 
                                                                           self.tb.dut1.port, 
                                                                           self.tb.dut2.name, 
                                                                           self.tb.dut2.port, 
                                                                           self.tb.config.ca256)
                                                                           
        self.Verify_Port_Key_Numbers(1)
        self.Verify_Port_Association_Numbers(0)
        
        # Send_packets_from_DUT2_to_DUT1
        self.suiteUdks.Transmit_Test(tx_count=1, tx_count_b=0, prime_packet_pump=False)   # Hack_to_prime_FDB
        self.suiteUdks.Transmit_Test(tx_count=0, tx_count_b=2100, prime_packet_pump=False)
        self.Verify_Port_Key_Numbers(2)
        self.Verify_Port_Association_Numbers(1)
        
        # self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut1.name, self.tb.config.ca256, self.tb.dut1.port)
        # self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut2.name, self.tb.config.ca256, self.tb.dut2.port)
        
    @mark.NIGHTLY
    def test_01_63_SAK_Rollover_Tx_and_Rx_SA_Counts(self, test_setup_teardown):
        """  Perform_5_SAK_rollovers_to_ensure_AN_rolls_over (i.e., 0, 1, 2, 3, 0).
        ...              Also_self.Verify_SA_Counters()_are_accurate_for_each_of_these_ANs."""
        
        self.suiteUdks.Macsec_Set_Pending_PN_Exhaustion(self.tb.dut1.name, 2000)
        self.suiteUdks.Create_and_Verify_Macsec_Connection_DUT1_Key_Server(self.tb.dut1.name,
                                                            self.tb.dut1.port,
                                                            self.tb.dut2.name,
                                                            self.tb.dut2.port,
                                                            self.tb.config.ca256)
                                                            
        # First_SAK_should_be_on_AN-0
        self.Verify_Port_Key_Numbers(1)
        self.Verify_Port_Association_Numbers(0)
        self.Verify_SA_Counters()
        
        # Send_packets_to_roll_SAK_to_AN-1
        self.suiteUdks.Transmit_Test(tx_count=2100)
        self.Verify_Port_Key_Numbers(2)
        self.Verify_Port_Association_Numbers(1)
        self.Verify_SA_Counters()
        
        # Send_packets_to_roll_SAK_to_AN-2
        self.suiteUdks.Transmit_Test(tx_count=2100)
        self.Verify_Port_Key_Numbers(3)
        self.Verify_Port_Association_Numbers(2)
        self.Verify_SA_Counters()
        
        # Send_packets_to_roll_SAK_to_AN-3
        self.suiteUdks.Transmit_Test(tx_count=2100)
        self.Verify_Port_Key_Numbers(4)
        self.Verify_Port_Association_Numbers(3)
        self.Verify_SA_Counters()
        
        # Send_packets_to_roll_SAK_to_AN-0
        self.suiteUdks.Transmit_Test(tx_count=2100)
        self.Verify_Port_Key_Numbers(5)
        self.Verify_Port_Association_Numbers(0)
        self.Verify_SA_Counters()
        
        # self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut1.name, self.tb.config.ca256, self.tb.dut1.port)
        # self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut2.name, self.tb.config.ca256, self.tb.dut2.port)
        
        
    """ keywords """  
    def Verify_Port_Key_Numbers(self, expected_kn):
        expected_kn = str(expected_kn)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_port_key_number(self.tb.dut1.name, self.tb.dut1.port, expected_kn, wait_for=True, max_wait=3)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_port_key_number(self.tb.dut1.name, self.tb.dut1.port, expected_kn)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_port_key_number(self.tb.dut2.name, self.tb.dut2.port, expected_kn)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_port_key_number(self.tb.dut2.name, self.tb.dut2.port, expected_kn)
        
    def Verify_Port_Association_Numbers(self, expected_an):
        expected_an = str(expected_an)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_port_association_number(self.tb.dut1.name, self.tb.dut1.port, expected_an, wait_for=True, max_wait=3)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_port_association_number(self.tb.dut1.name, self.tb.dut1.port, expected_an)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_port_association_number(self.tb.dut2.name, self.tb.dut2.port, expected_an)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_port_association_number(self.tb.dut2.name, self.tb.dut2.port, expected_an)
        
    def Verify_SA_Counters(self):
        """  Send_packets_between_DUTs_and_Verify_SA_Counters_match
        ...              the_number_of_packets_sent.  The_caller_should_roll_the
        ...              SAK (and_therefore_the_AN) between_calls_to_this_keyword.  """
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_clear_counters_on_port(self.tb.dut1.name, self.tb.dut1.port)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_clear_counters_on_port(self.tb.dut2.name, self.tb.dut2.port)
        
        self.suiteUdks.Transmit_Test(tx_count=19, tx_count_b=0, prime_packet_pump=False)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_sa_encrypted_packets(self.tb.dut1.name, self.tb.dut1.port, count='19')
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_sa_ok_packets(self.tb.dut2.name, self.tb.dut2.port, count='19')
        
        self.suiteUdks.Transmit_Test(tx_count=0, tx_count_b=23, prime_packet_pump=False)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_sa_encrypted_packets(self.tb.dut2.name, self.tb.dut2.port, count='23')
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_sa_ok_packets(self.tb.dut1.name, self.tb.dut1.port, count='23')

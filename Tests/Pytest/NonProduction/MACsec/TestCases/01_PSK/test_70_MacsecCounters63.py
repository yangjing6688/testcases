from Tests.Pytest.NonProduction.MACsec.Resources.MACsecBase import MACsecBase
from pytest import mark
from pytest import fixture
import time

@fixture()
def test_setup_teardown(request):
    request.instance.Configure_DUTs_for_Traffic(request.instance.tb.dut1, request.instance.tb.dut2)

    def teardown():
        request.instance.Unconfigure_DUTs_for_Traffic(request.instance.tb.dut1, request.instance.tb.dut2)
    request.addfinalizer(teardown)

class MacsecCountersTests(MACsecBase):

    @mark.NIGHTLY
    def test_01_70_Macsec_Counters_no_Errors(self, test_setup_teardown):
        """  Send_traffic_over_MACsec_connection_and_verify_all
        ...              error_counters_are_zero. """
        
        self.Clear_Macsec_Counters(self.tb.dut1, self.tb.dut2)
        self.suiteUdks.Transmit_Test(tx_count=1700, prime_packet_pump=True)
        
        self.suiteUdks.Verify_No_Macsec_Errors_on_Port(self.tb.dut1.name, self.tb.dut1.port)
        self.suiteUdks.Verify_No_Macsec_Errors_on_Port(self.tb.dut2.name, self.tb.dut2.port)
        
    @mark.NIGHTLY
    def test_01_71_Macsec_Counters_Clear(self, test_setup_teardown):
        """  Send_traffic_over_MACsec_connection_and_verify
        ...              clear_command_zeros_all_packet_and_octet_counters. """
        
        self.suiteUdks.Transmit_Test(tx_count=171, prime_packet_pump=True)
        self.Clear_Macsec_Counters(self.tb.dut1, self.tb.dut2)
        
        self.Verify_Macsec_All_Counts_Are_Zero(self.tb.dut1)
        self.Verify_Macsec_All_Counts_Are_Zero(self.tb.dut2)
        
        
    @mark.BUILD
    @mark.NIGHTLY
    def test_01_72_Macsec_Counters_All(self, test_setup_teardown):
        """  Send_traffic_over_MACsec_connection_and_verify_packet
        ...              counts (TxSC, TxSA, RxSC_and_RxSA) and_octet_counts
        ...              (TxSC_and_RxSC) are_exact.  This_single_test_is
        ...              equivalent_to_running_tests_01.73_thru_01.78. """
        num_packets = 4500
        packet_len = 350
        encrypted_len = packet_len - 12      # 12-octets_of_MAC_SA_DA_are_not_encrypted
        num_octets =  num_packets * encrypted_len
        
        self.suiteUdks.Transmit_Test(tx_count=172, prime_packet_pump=True, packet_len=packet_len)
        self.Clear_Macsec_Counters(self.tb.dut1, self.tb.dut2)
        self.Verify_Macsec_All_Counts_Are_Zero(self.tb.dut1)
        self.Verify_Macsec_All_Counts_Are_Zero(self.tb.dut2)
        
        print( str(num_packets) + ' packets_of ' + str(packet_len) + ' octets_each, yielding '+ str(num_octets) + ' encrypted_octets')
        self.suiteUdks.Transmit_Test(tx_count=num_packets, prime_packet_pump=False, packet_len=packet_len)
        self.Verify_Macsec_Tx_and_Rx_Packet_Counts(self.tb.dut1, count=num_packets)
        self.Verify_Macsec_Tx_and_Rx_Octet_Counts(self.tb.dut1, count=num_octets)
        self.Verify_Macsec_Tx_and_Rx_Packet_Counts(self.tb.dut2, count=num_packets)
        self.Verify_Macsec_Tx_and_Rx_Octet_Counts(self.tb.dut2, count=num_octets)
        
    @mark.NIGHTLY
    def test_01_73_Macsec_Counters_Rx_SC_Packets(self, test_setup_teardown):
        """  Send_traffic_over_MACsec_connection_and_verify
        ...              receive_secure_channel (RxSC) packet_counters. """
        num_packets=2000
        packet_len=600
        
        self.suiteUdks.Transmit_Test(tx_count=173, prime_packet_pump=True, packet_len=packet_len)
        self.Clear_Macsec_Counters(self.tb.dut1, self.tb.dut2)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_sc_ok_packets(self.tb.dut1.name, self.tb.dut1.port, count='0')
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_sc_ok_packets(self.tb.dut2.name, self.tb.dut2.port, count='0')
        
        print(str(num_packets) + " packets of " + str(packet_len) + " octets each")
        self.suiteUdks.Transmit_Test(tx_count=num_packets, prime_packet_pump=False, packet_len=packet_len)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_sc_ok_packets(self.tb.dut1.name, self.tb.dut1.port, count=num_packets)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_sc_ok_packets(self.tb.dut2.name, self.tb.dut2.port, count=num_packets)
        
    @mark.NIGHTLY
    def test_01_74_Macsec_Counters_Rx_SA_Packets(self, test_setup_teardown):
        """  Send_traffic_over_MACsec_connection_and_verify
        ...              receive_secure_association (RxSA) packet_counters. """
        num_packets = 2500
        packet_len = 550
        
        self.suiteUdks.Transmit_Test(tx_count=174, prime_packet_pump=True, packet_len=packet_len)
        self.Clear_Macsec_Counters(self.tb.dut1, self.tb.dut2)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_sa_ok_packets(self.tb.dut1.name, self.tb.dut1.port, count='0')
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_sa_ok_packets(self.tb.dut2.name, self.tb.dut2.port, count='0')
        
        print(str(num_packets) + " packets of " + str(packet_len) + " octets each")
        self.suiteUdks.Transmit_Test(tx_count=num_packets, prime_packet_pump=False, packet_len=packet_len)
        # Debug_Show_Counters 
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_sa_ok_packets(self.tb.dut1.name, self.tb.dut1.port, count=num_packets)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_sa_ok_packets(self.tb.dut2.name, self.tb.dut2.port, count=num_packets)
        # Debug_Show_Counters 
        
    @mark.NIGHTLY     
    def test_01_75_Macsec_Counters_Rx_SC_Octets(self, test_setup_teardown):
        """  Send_traffic_over_MACsec_connection_and_verify
        ...              receive_secure_channel (RxSC) octet_counters. """
        num_packets =  3000
        packet_len =  500
        encrypted_len = packet_len - 12      # 12-octets_of_MAC_SA_DA_are_not_encrypted
        num_octets = num_packets * encrypted_len
        
        self.suiteUdks.Transmit_Test(tx_count=175, prime_packet_pump=True, packet_len=packet_len)
        self.Clear_Macsec_Counters(self.tb.dut1, self.tb.dut2)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_sc_octets_decrypted(self.tb.dut1.name, self.tb.dut1.port, count='0')
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_sc_octets_decrypted(self.tb.dut2.name, self.tb.dut2.port, count='0')
        
        print(str(num_packets) + " packets of " + str(packet_len) + " octets each, yielding " + str(num_octets) + " decrypted_octets")
        self.suiteUdks.Transmit_Test(tx_count=num_packets, prime_packet_pump=False, packet_len=packet_len)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_sc_octets_decrypted(self.tb.dut1.name, self.tb.dut1.port, count=num_octets)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_sc_octets_decrypted(self.tb.dut2.name, self.tb.dut2.port, count=num_octets)
        
    @mark.NIGHTLY    
    def test_01_76_Macsec_Counters_Tx_SC_Packets(self, test_setup_teardown):
        """  Send_traffic_over_MACsec_connection_and_verify
        ...              transmit_secure_channel (TxSC) packet_counters. """
        num_packets =  3500
        packet_len =  450
        
        self.suiteUdks.Transmit_Test(tx_count=176, prime_packet_pump=True, packet_len=packet_len)
        self.Clear_Macsec_Counters(self.tb.dut1, self.tb.dut2)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_sc_encrypted_packets(self.tb.dut1.name, self.tb.dut1.port, count='0')
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_sc_encrypted_packets(self.tb.dut2.name, self.tb.dut2.port, count='0')
        
        print(str(num_packets) + " packets of " + str(packet_len) + " octets_each")
        self.suiteUdks.Transmit_Test(tx_count=num_packets, prime_packet_pump=False, packet_len=packet_len)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_sc_encrypted_packets(self.tb.dut1.name, self.tb.dut1.port, count=num_packets)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_sc_encrypted_packets(self.tb.dut2.name, self.tb.dut2.port, count=num_packets)
        
    @mark.NIGHTLY     
    def test_01_77_Macsec_Counters_Tx_SA_Packets(self, test_setup_teardown):
        """  Send_traffic_over_MACsec_connection_and_verify
        ...              transmit_secure_association (TxSA) packet_counters. """
        num_packets =  4000
        packet_len =  400
        
        self.suiteUdks.Transmit_Test(tx_count=177, prime_packet_pump=True, packet_len=packet_len)
        self.Clear_Macsec_Counters(self.tb.dut1, self.tb.dut2)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_sa_encrypted_packets(self.tb.dut1.name, self.tb.dut1.port, count='0')
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_sa_encrypted_packets(self.tb.dut2.name, self.tb.dut2.port, count='0')
        
        print( str(num_packets) + " packets of " + str(packet_len) + " octets_each")
        self.suiteUdks.Transmit_Test(tx_count=num_packets, prime_packet_pump=False, packet_len=packet_len)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_sa_encrypted_packets(self.tb.dut1.name, self.tb.dut1.port, count=num_packets)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_sa_encrypted_packets(self.tb.dut2.name, self.tb.dut2.port, count=num_packets)
        
    @mark.NIGHTLY     
    def test_01_78_Macsec_Tx_Counters_SC_Octets(self, test_setup_teardown):
        """  Send_traffic_over_MACsec_connection_and_verify
        ...              transmit_secure_channel (TxSC) octet_counters. """
        num_packets=  3500
        # JETS_Rx_count_failures_seen_when_packet_len_is_set_to_1000
        packet_len=  400
        encrypted_len= packet_len - 12      # 12-octets_of_MAC_SA_DA_are_not_encrypted
        num_octets= num_packets * encrypted_len
        
        print("Prime the packet pump and clear octet counters")
        self.suiteUdks.Transmit_Test(tx_count=178, prime_packet_pump=True, packet_len=packet_len)
        self.Clear_Macsec_Counters(self.tb.dut1, self.tb.dut2)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_sc_octets_encrypted(self.tb.dut1.name, self.tb.dut1.port, count='0')
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_sc_octets_encrypted(self.tb.dut2.name, self.tb.dut2.port, count='0')
        
        print(self.tb.dut1.name + " sends  " + str(num_packets) + " packets of " + str(packet_len) + " octets each, yielding " + str(num_octets) + " encrypted octets")
        self.suiteUdks.Transmit_Test(tx_count=num_packets, tx_count_b=0, prime_packet_pump=False, packet_len=packet_len)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_sc_octets_encrypted(self.tb.dut1.name, self.tb.dut1.port, count=num_octets)
        
        print(self.tb.dut2.name + " sends " + str(num_packets) + " packets of " +  str(packet_len) + " octets_each, yielding " +  str(num_octets) + " encrypted_octets")
        self.suiteUdks.Transmit_Test(tx_count=0, tx_count_b=num_packets, prime_packet_pump=False, packet_len=packet_len)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_sc_octets_encrypted(self.tb.dut2.name, self.tb.dut2.port, count=num_octets)
        
        
    """ keywords """
    def Configure_DUTs_for_Traffic(self, dut1, dut2):
        self.suiteUdks.Add_Port_to_Traffic_VLAN(dut1.name, dut1.port)
        self.suiteUdks.Add_Port_to_Traffic_VLAN(dut2.name, dut2.port)
        self.Enable_and_Verify_Macsec(dut1, dut2)
        
    def Unconfigure_DUTs_for_Traffic(self, dut1, dut2):
        self.Disable_Macsec(dut1, dut2)
        self.suiteUdks.Remove_Port_from_Traffic_VLAN(dut1.name, dut1.port)
        self.suiteUdks.Remove_Port_from_Traffic_VLAN(dut2.name, dut2.port)
        
    def Enable_and_Verify_Macsec(self, dut1, dut2):
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(dut1.name, dut1.ca, dut1.port)
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(dut2.name, dut2.ca, dut2.port) # was dut1.ca
        self.suiteUdks.Macsec_Verify_Port_Connect_Secure(dut1.name, dut1.port)
        self.suiteUdks.Macsec_Verify_Port_Connect_Secure(dut2.name, dut2.port)
        
    def Disable_Macsec(self, dut1, dut2):
        self.suiteUdks.Disable_and_Verify_Macsec_on_Port(dut1.name, dut1.ca, dut1.port)
        self.suiteUdks.Disable_and_Verify_Macsec_on_Port(dut2.name, dut2.ca, dut2.port) # was dut1.ca
        
    def Clear_Macsec_Counters(self, dut1, dut2):
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_clear_counters_on_port(dut1.name, dut1.port)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_clear_counters_on_port(dut2.name, dut2.port)
        time.sleep(1)
        
    def Verify_Macsec_All_Counts_Are_Zero(self, dut):
        """  Verify_Packet_and_Octet_counts_for_both_Tx_and_Rx_are_all_zero """
        self.Verify_Macsec_Tx_and_Rx_Packet_Counts(dut, count='0')
        self.Verify_Macsec_Tx_and_Rx_Octet_Counts(dut, count='0')
        
    def Verify_Macsec_Tx_and_Rx_Packet_Counts(self, dut, count):
        """  Verify_exact_packet_count_on_TxSC, TxSA, RxSC_and_RxSA """
        # count_leeway = str(count + 2)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_sc_encrypted_packets(dut.name, dut.port, count=count)  # count_max=${count_leeway}
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_sa_encrypted_packets(dut.name, dut.port, count=count)  # count_max=${count_leeway}
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_sc_ok_packets(dut.name, dut.port, count=count)  # count_max=${count_leeway}
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_sa_ok_packets(dut.name, dut.port, count=count)  # count_max=${count_leeway}
        
    def Verify_Macsec_Tx_and_Rx_Octet_Counts(self, dut, count):
        """  Verify_exact_octet_count_on_TxSC_and_RxSC """
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_tx_sc_octets_encrypted(dut.name, dut.port, count=count)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_rx_sc_octets_decrypted(dut.name, dut.port, count=count)
        
    def Debug_Show_Counters(self, dut1, dut2):
        """  Send_a_debug_commands_which_dumps_every_available_MACsec
        ...              counter_for_DUT1_and_DUT2.  This_is_not_a_test; it_is_only
        ...              for_informational_and_debug_purposes. """
        self.networkElementCliSend.send_cmd(dut1.name, "debug_hal_show_macsec " + str(dut1.port) + " counters")
        self.networkElementCliSend.send_cmd(dut2.name, "debug_hal_show_macsec " + str(dut2.port) + " counters")
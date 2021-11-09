from Tests.Pytest.Functional.nonprod.MACsec.Resources.MACsecBase import MACsecBase
from pytest import mark
from pytest import fixture

class GcmAes256BasicConnectivityTests(MACsecBase):

    @mark.BUILD
    @mark.NIGHTLY
    def test_03_10_Cipher_Suite_GCM_AES_256_Basic_Connectivity(self):
        
        """ Configure_cipher_suite_gcm-aes-256_on_both_DUTs_and_verify_connectivity """
      
        self.suiteUdks.Skip_Test_if_gcm_aes_256_Not_Supported()
    
        self.suiteUdks.Set_Macsec_Cipher_Suite(self.tb.dut1.name, self.tb.dut1.port256, 'gcm-aes-256')
        self.suiteUdks.Set_Macsec_Cipher_Suite(self.tb.dut2.name, self.tb.dut2.port256, 'gcm-aes-256')
        self.suiteUdks.Create_and_Verify_Macsec_Connection(self.tb.dut1.name, self.tb.dut1.port256, self.tb.dut2.name, self.tb.dut2.port256, self.tb.config.ca256)
    
        print("Burst_1, 30_pkts_DUT1-to-DUT2_then_30_pkts_DUT2-to-DUT1")
        self.Clear_Macsec_Counters(self.tb.dut1, self.tb.dut2)
        self.suiteUdks.Add_Port_to_Traffic_VLAN(self.tb.dut1.name, self.tb.dut1.port256)
        self.suiteUdks.Add_Port_to_Traffic_VLAN(self.tb.dut2.name, self.tb.dut2.port256)
        self.suiteUdks.Transmit_Test(tx_count=30, tx_count_b=0, prime_packet_pump=False)
        self.suiteUdks.Transmit_Test(tx_count=0, tx_count_b=30, prime_packet_pump=False)
        self.Verify_No_Macsec_Errors(self.tb.dut1, self.tb.dut2)
    
        print("Burst_2, 300_pkts_DUT1-to-DUT2_then_300_pkts_DUT2-to-DUT1")
        self.suiteUdks.Transmit_Test(tx_count=300, tx_count_b=0, prime_packet_pump=False)
        self.suiteUdks.Transmit_Test(tx_count=0, tx_count_b=300, prime_packet_pump=False)
        self.Verify_No_Macsec_Errors(self.tb.dut1, self.tb.dut2)
    
        print("Burst_3, Simultaneous_5000_pkts_DUT1-to-DUT2_and_6000_pts_DUT2-to-DUT1")
        self.suiteUdks.Transmit_Test(tx_count=5000, tx_count_b=6000, prime_packet_pump=False)
        self.Verify_No_Macsec_Errors(self.tb.dut1, self.tb.dut2)
    
        self.suiteUdks.Remove_Port_from_Traffic_VLAN(self.tb.dut1.name, self.tb.dut1.port256)
        self.suiteUdks.Remove_Port_from_Traffic_VLAN(self.tb.dut2.name, self.tb.dut2.port256)
        self.suiteUdks.Disable_and_Verify_Macsec_Connection(self.tb.dut1.name, self.tb.dut1.port256, self.tb.dut2.name, self.tb.dut2.port256, self.tb.config.ca256)
    
    def Clear_Macsec_Counters(self, dut1, dut2):
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_clear_counters_on_port(dut1.name, dut1.port256)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_clear_counters_on_port(dut2.name, dut2.port256)
    
    def Verify_No_Macsec_Errors(self, dut1, dut2):
        print("Skip_error_test")
        self.suiteUdks.Verify_No_Macsec_Errors_on_Port(dut1.name, dut1.port256)
        self.suiteUdks.Verify_No_Macsec_Errors_on_Port(dut2.name, dut2.port256)
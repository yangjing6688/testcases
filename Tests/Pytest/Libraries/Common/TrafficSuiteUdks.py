    
    
from ExtremeAutomation.Keywords.TrafficKeywords.TrafficCaptureKeywords import TrafficCaptureKeywords
from ExtremeAutomation.Keywords.TrafficKeywords.TrafficGeneratorConnectionManager import TrafficGeneratorConnectionManager
from ExtremeAutomation.Keywords.TrafficKeywords.TrafficPacketCreationKeywords import TrafficPacketCreationKeywords
from ExtremeAutomation.Keywords.TrafficKeywords.TrafficPacketInspectionKeywords import TrafficPacketInspectionKeywords
from ExtremeAutomation.Keywords.TrafficKeywords.TrafficStatisticsKeywords import TrafficStatisticsKeywords
from ExtremeAutomation.Keywords.TrafficKeywords.TrafficTransmitKeywords import TrafficTransmitKeywords
from ExtremeAutomation.Keywords.TrafficKeywords.TrafficStreamConfigurationKeywords import TrafficStreamConfigurationKeywords
from ExtremeAutomation.Keywords.TrafficKeywords.EzTrafficValidation.TrafficValidationKeywords import TrafficValidationKeywords
from ExtremeAutomation.Keywords.TrafficKeywords.Utils.Constants.PacketTypeConstants import PacketTypeConstants
from ExtremeAutomation.Keywords.UserDefinedKeywords.TrafficGeneration.TrafficGenerationUdks import TrafficGenerationUdks
import time


class TrafficGenerationSuiteUdks():
    def __init__(self):
        self.trafficCaptureKeywords = TrafficCaptureKeywords()
        self.trafficGeneratorConnectionManager = TrafficGeneratorConnectionManager()
        self.trafficPacketCreationKeywords = TrafficPacketCreationKeywords()
        self.trafficPacketInspectionKeywords = TrafficPacketInspectionKeywords()
        self.trafficStatisticsKeywords = TrafficStatisticsKeywords()
        self.trafficStreamConfigurationKeywords = TrafficStreamConfigurationKeywords()
        self.trafficValidationKeywords = TrafficValidationKeywords()
        self.trafficTransmitKeywords = TrafficTransmitKeywords()
        self.packetTypeConstants = PacketTypeConstants()
        self.trafficUdks = TrafficGenerationUdks()
    
    # EXOS UDKS  
    def Setup_Packet_Streams(self, port_a, port_b, tx_packet_a, tx_packet_b, tx_count=100, tx_count_b=-1,  tx_rate=100):
        if tx_count_b < 0:
            tx_count_b =  tx_count
        self.trafficUdks.Configure_Packet_on_Port_Single_Burst(port_a, tx_packet_a, count=tx_count, rate=tx_rate)
        self.trafficUdks.Configure_Packet_on_Port_Single_Burst(port_b, tx_packet_b, count=tx_count_b, rate=tx_rate)

    def Send_Packets_Verify_Not_Received(self, port_a, port_b, rx_packet_b, rx_packet_a,
                                     packet_a_src_mac, packet_b_src_mac, tx_count=100, tx_rate=100):
         # Kick off authentication, run UPM Script.
        self.trafficTransmitKeywords.start_transmit_on_port(port_a)
        self.trafficTransmitKeywords.start_transmit_on_port(port_b)
        time.sleep(1)
    
        # Send again to re-program the FDB entry if necessary.
        #    Not 100% necessary to validate UPM scripting
        self.trafficTransmitKeywords.start_transmit_on_port(port_a)
        self.trafficTransmitKeywords.start_transmit_on_port(port_b)
        time.sleep(1)
    
        # Make sure the session is set up.
        #    Not 100% necessary to validate UPM scripting
        self.trafficUdks.Start_Capture_with_DMAC_and_SMAC_Filter(port_a, packet_a_src_mac, packet_b_src_mac)
        self.trafficUdks.Start_Capture_with_DMAC_and_SMAC_Filter(port_b, packet_b_src_mac, packet_a_src_mac)
        self.trafficCaptureKeywords.clear_port_statistics(port_a)
        self.trafficCaptureKeywords.clear_port_statistics(port_b)
    
        self.trafficTransmitKeywords.start_transmit_on_port(port_a)
        self.trafficTransmitKeywords.start_transmit_on_port(port_b)
    
        time.sleep(2)
    
        self.trafficTransmitKeywords.stop_transmit_on_port(port_a)
        self.trafficTransmitKeywords.stop_transmit_on_port(port_b)
    
        self.trafficStatisticsKeywords.get_captured_count(port_a)
        self.trafficStatisticsKeywords.stat_value_should_be_equal(port_a, 0)
        self.trafficStatisticsKeywords.get_captured_count(port_b)
        self.trafficStatisticsKeywords.stat_value_should_be_equal(port_b, 0)
        self.trafficStatisticsKeywords.get_tx_count(port_a)                           
        self.trafficStatisticsKeywords.stat_value_should_be_equal(port_a, tx_count)
        self.trafficStatisticsKeywords.get_tx_count(port_b)
        self.trafficStatisticsKeywords.stat_value_should_be_equal(port_b, tx_count)


    def Prime_Packet_Pump(self, port_a, port_b):
        # Kick off authentication, run UPM Script.
        self.trafficTransmitKeywords.start_transmit_on_port(port_a)
        self.trafficTransmitKeywords.start_transmit_on_port(port_b)
        time.sleep(1)
    
        # Send again to re-program the FDB entry if necessary.
        #    Not 100% necessary to validate UPM scripting
        self.trafficTransmitKeywords.start_transmit_on_port(port_a)
        self.trafficTransmitKeywords.start_transmit_on_port(port_b)
        time.sleep(1)
        
    
    
    def Send_Packets_Verify_Received(self, port_a, port_b, tx_packet_a, tx_packet_b, rx_packet_a, rx_packet_b,
                                     packet_a_src_mac, packet_b_src_mac, tx_count=100, tx_count_b=-1, tx_rate=100,
                                     prime_packet_pump=True,
                                     ignore_error = False):
        # Xmit Three "bursts"
        #   1st Xmit - creates netlogin session - Causes UPM Auth script to run keyword run
        #         Script command may clear FDB
        #   2nd Xmit - 1st packet will be dropped when the FDB entry is reprogrammed.
        #   3rd Xmit - Should be 100% working.
        #
        
        if tx_count_b < 0:
            tx_count_b = tx_count
            
        if prime_packet_pump:
            self.Prime_Packet_Pump(port_a, port_b)

        self.trafficTransmitKeywords.stop_transmit_on_port(port_a)
        self.trafficTransmitKeywords.stop_transmit_on_port(port_b)
        self.trafficUdks.Start_Capture_with_DMAC_and_SMAC_Filter(port_a, packet_a_src_mac, packet_b_src_mac)
        self.trafficUdks.Start_Capture_with_DMAC_and_SMAC_Filter(port_b, packet_b_src_mac, packet_a_src_mac)
        self.trafficCaptureKeywords.clear_port_statistics(port_a)
        self.trafficCaptureKeywords.clear_port_statistics(port_b)
        
        self.trafficTransmitKeywords.start_transmit_on_port(port_a)
        self.trafficTransmitKeywords.start_transmit_on_port(port_b)
        
        transmit_time = max(tx_count, tx_count_b) / tx_rate + 2
        time.sleep(transmit_time)
        
        self.trafficCaptureKeywords.stop_capture_on_port(port_a)
        self.trafficCaptureKeywords.stop_capture_on_port(port_b)
        
        if not ignore_error:
            self.trafficStatisticsKeywords.get_captured_count(port_a)
            self.trafficStatisticsKeywords.stat_value_should_be_equal(port_a, tx_count_b)
            self.trafficStatisticsKeywords.get_captured_count(port_b)
            self.trafficStatisticsKeywords.stat_value_should_be_equal(port_b, tx_count)
            self.trafficStatisticsKeywords.get_tx_count(port_a)    
            self.trafficStatisticsKeywords.stat_value_should_be_equal(port_a, tx_count)
            self.trafficStatisticsKeywords.get_tx_count(port_b)    
            self.trafficStatisticsKeywords.stat_value_should_be_equal(port_b, tx_count_b)
            
            num_pkts_to_inspect_a = min(tx_count_b, 5)
            if num_pkts_to_inspect_a > 0:
                self.trafficPacketInspectionKeywords.capture_inspection_random_list(port_a, rx_packet_a, num_pkts_to_inspect_a)
            num_pkts_to_inspect_b = min(tx_count, 5)
            if num_pkts_to_inspect_b > 0:
                self.trafficPacketInspectionKeywords.capture_inspection_random_list(port_b, rx_packet_b, num_pkts_to_inspect_b)
        
        
    '''def Setup_Packet_Streams(self, port_a, port_b,
                             tx_packet_a, tx_packet_b,
                             tx_count=100, tx_count_b=-1,
                             tx_rate=100 ):

        if tx_count_b < 0:
             tx_count_b = tx_count
             
        self.trafficUdks.Configure_Packet_on_Port_Single_Burst(port_a, tx_packet_a, count=tx_count, rate=tx_rate)
        self.trafficUdks.Configure_Packet_on_Port_Single_Burst(port_b, tx_packet_b, count=tx_count_b, rate=tx_rate)'''

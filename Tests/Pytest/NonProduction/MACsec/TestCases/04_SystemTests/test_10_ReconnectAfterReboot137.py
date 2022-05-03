from Tests.Pytest.NonProduction.MACsec.Resources.MACsecBase import MACsecBase
from ExtremeAutomation.Library.Utils.StringUtils import StringUtils
from pytest import mark
import time

class ReconnectAfterReboot(MACsecBase):
    
    @mark.NIGHTLY
    def test_04_10_Reboot_DUT1_and_Verify_Connectivity_Reestablished(self):
        """ Verify MACsec connectivity returns after rebooting DUT1.
        ...              Side effect is that DUT1 config is saved to a file. """
        
        self.Configure_DUTs_for_MACsec()
        self.defaultLibrary.apiLowLevelApis.fileManagementUtils.save_current_config(self.tb.dut1.name)
    
        self.defaultLibrary.apiLowLevelApis.resetDeviceUtils.reboot_network_element_now_and_wait(self.tb.dut1.name, max_wait=180, wait_before=1, wait_after_success=90)
        self.Macsec_Verify_All_Connections()
    
        self.Unconfigure_DUTs_for_MACsec()
    
    @mark.NIGHTLY
    @mark.STACK
    def test_04_11_Reboot_DUT2_slot_and_Verify_Connectivity_Reestablished(self):
        """ Verify MACsec connectivity returns after rebooting DUT2's MACsec slot.
        ...              This test should only be run on testbeds where DUT2 is a stacked system. """
    
        self.suiteUdks.Skip_Test_if_Not_Stacked_System(self.tb.dut2)
    
        self.Configure_DUTs_for_MACsec()
        self.defaultLibrary.apiLowLevelApis.fileManagementUtils.save_current_config(self.tb.dut1.name)
    
        dut2_slot = StringUtils.get_slot_from_port_string(self.tb.dut2.port)
        self.suiteUdks.Reboot_Slot_in_EXOS_Stack(self.tb.dut2.name, self.tb.dut2_slot)
        print("Waiting_3_minutes_for " +  str(self.tb.dut2.name) + " slot " + str(self.tb.dut2_slot) + " to_reboot_and_for LRM/MACsec Adapater to initialize")
        time.sleep(180)
        self.Macsec_Verify_All_Connections()
    
        self.Unconfigure_DUTs_for_MACsec()
    
    
    def Configure_DUTs_for_MACsec(self):
        self.suiteUdks.Add_Port_to_Traffic_VLAN(self.tb.dut1.name, self.tb.dut1.port)
        self.suiteUdks.Add_Port_to_Traffic_VLAN(self.tb.dut2.name, self.tb.dut2.port)
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(self.tb.dut1.name, self.tb.dut1.ca,self.tb.dut1.port)
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(self.tb.dut2.name, self.tb.dut1.ca, self.tb.dut2.port)
        self.suiteUdks.Macsec_Verify_Port_Connect_Secure(self.tb.dut1.name, self.tb.dut1.port)
        self.suiteUdks.Macsec_Verify_Port_Connect_Secure(self.tb.dut2.name, self.tb.dut2.port)
    
    def Unconfigure_DUTs_for_MACsec(self):
        self.suiteUdks.Remove_Port_from_Traffic_VLAN(self.tb.dut1.name, self.tb.dut1.port)
        self.suiteUdks.Remove_Port_from_Traffic_VLAN(self.tb.dut2.name, self.tb.dut2.port)
        self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut1.name, self.tb.dut1.ca, self.tb.dut1.port)
        self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut2.name, self.tb.dut1.ca, self.tb.dut2.port)
    
    def Macsec_Verify_All_Connections(self):
        self.defaultLibrary.apiLowLevelApis.port.port_verify_operational(self.tb.dut1.name, self.tb.dut1.port, wait_for=True, wait_max=10)
        self.defaultLibrary.apiLowLevelApis.port.port_verify_operational(self.tb.dut2.name, self.tb.dut2.port, wait_for=True, wait_max=10)
        self.suiteUdks.Macsec_Verify_Port_Connect_Secure(self.tb.dut1.name, self.tb.dut1.port)
        self.suiteUdks.Macsec_Verify_Port_Connect_Secure(self.tb.dut2.name, self.tb.dut2.port)
        self.suiteUdks.Verify_Connectivity()

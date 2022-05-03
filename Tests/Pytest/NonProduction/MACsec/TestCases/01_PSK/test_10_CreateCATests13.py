from Tests.Pytest.NonProduction.MACsec.Resources.MACsecBase import MACsecBase
from pytest import mark

class CreateCATests(MACsecBase):
    
    def test_01_00_NOP(self):
        #Remove Tags  MACSEC
        pass #This is a dummy test which can be run to aid debug of Test Suite Setup
    
    @mark.NIGHTLY
    def test_01_10_Create_Connectivity_Association_with_128bit_CAK(self):
        """ Create a connectivity association with a 128-bit CAK and verify it exists """
        self.suiteUdks.Create_and_Verify_Connectivity_Association(self.tb.dut1.name, self.tb.config.ca128)
        self.suiteUdks.Delete_and_Verify_Connectivity_Association(self.tb.dut1.name, self.tb.config.ca128)
        
    @mark.NIGHTLY
    def test_01_11_Create_Connectivity_Association_with_256bit_CAK(self):
        """ Create a connectivity association with a 256-bit CAK and verify it exists """   
        self.suiteUdks.Create_and_Verify_Connectivity_Association(self.tb.dut1.name, self.tb.config.ca256)
        self.suiteUdks.Delete_and_Verify_Connectivity_Association(self.tb.dut1.name, self.tb.config.ca256)

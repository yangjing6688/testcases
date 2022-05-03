from Tests.Pytest.NonProduction.MACsec.Resources.MACsecBase import MACsecBase
from pytest import mark
from pytest import fixture


@fixture()
def test_01_20_teardown(request):
    print("setup - test_01_20_teardown")

    def teardown():
        print("teardown - test_01_20_teardown")
        request.instance.suiteUdks.Disable_and_Verify_Macsec_on_Port(request.instance.tb.dut1.name, request.instance.tb.config.ca128, request.instance.tb.dut1.port)
    request.addfinalizer(teardown)
        
@fixture()
def test_01_21_teardown(request):
    print("setup - test_01_21_teardown")

    def teardown():
        print("teardown - test_01_21_teardown")
        request.instance.suiteUdks.Disable_and_Verify_Macsec_on_Port(request.instance.tb.dut1.name,  request.instance.tb.config.ca128, request.instance.tb.dut1.ports)
    request.addfinalizer(teardown)

class EnableMacsecOnPortTests(MACsecBase):
    @mark.NIGHTLY
    @mark.BUILD
    def test_01_20_Create_CA_and_Assign_a_Port(self, test_01_20_teardown):
        """ Verify one port can be assigned to a connectivity assocation """
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(self.tb.dut1.name,  self.tb.config.ca128, self.tb.dut1.port)
    
    @mark.NIGHTLY
    def test_01_21_Create_CA_and_Assign_Multiple_Ports(self, test_01_21_teardown):
        """ Verify multiple ports can be assigned to a connectivity assocation """
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(self.tb.dut1.name,  self.tb.config.ca128, self.tb.dut1.ports)
        
   
        
        
  
from Tests.Pytest.NonProduction.BGP.Resources.BgpBase import BgpBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.NonProduction.BGP.Resources.BgpSuiteUdks import BgpSuiteUdks
@fixture()
def test_setup_teardown(request):
     def teardown():
         request.instance.Test_Case_Cleanup()
     request.addfinalizer(teardown)
class License14Tests(BgpBase):
     
     @mark.ONE_BOX
     def test_14_BGP_Base_License(self):
         '''[Documentation]  Test Objective: This test is intended to be run on unified hardware running EXOS, version 31.4 or later. Configure a base license only and verify 3 auto-peers are created on the default VR.'''
         # Setup here will run the "Test Suite Setup" in the Resources -> SuiteUdks.robot
         #  change_this_along_the_lines_of "[Setup]  Test_Case_Setup" if_you_have_a_setup_specific_to_a_subset_of_test_cases.
         #[Setup]
         print('  (Step 1) Verify effective license level is Base')
         self.localsuiteudks.Verify_Base_License(self.tb.config.netelem1.name)
         self.localsuiteudks.Verify_Base_License(self.tb.config.netelem2.name)
         print('  (Step 2) Configure auto-peering on dut1')
         self.localsuiteudks.Create_Bgp_Autopeering(self.tb.config.netelem1.name,self.tb.config.dut1.bgp.localAS,self.tb.config.dut1.bgp.router_id)
         self.localsuiteudks.Create_BGP_Autopeering(self.tb.config.netelem2.name,self.tb.config.dut2.bgp.localAS,self.tb.config.dut2.bgp.router_id)
         print('  (Step 3) Verify Number of BGP neighbors on dut1 is 3.')
         self.localsuiteudks.Verify_BGP_Number_Neighbors(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.numAutoPeers)
         print('  (Step 4) Verify Number of BGP neighbors on dut2 is 3.')
         self.localsuiteudks.Verify_BGP_Number_Neighbors(self.tb.config.netelem2.name,self.tb.config.globalvars.bgp.numAutoPeers)
         print('  (Step 5) Verify 3 peers are established on dut1.')
         self.localsuiteudks.Verify_Three_Auto_Peers_Established(self.tb.config.netelem1.name)
         print('  (Step 6) Verify 3 peers are established on dut2.')
         self.localsuiteudks.Verify_Three_Auto_Peers_Established(self.tb.config.netelem2.name)
         self.TestCase14Cleanup()
     def TestCase14Cleanup(self):
         print('  (Step 7) Delete BGP auto-peering from dut1')
         self.localsuiteudks.Delete_BGP_Autopeering(self.tb.config.netelem1.name)
         print('  (Step 8) Delete BGP auto-peering from dut2')
         self.localsuiteudks.Delete_BGP_Autopeering(self.tb.config.netelem2.name)

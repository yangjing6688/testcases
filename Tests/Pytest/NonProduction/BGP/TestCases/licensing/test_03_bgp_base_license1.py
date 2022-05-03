from Tests.Pytest.NonProduction.BGP.Resources.BgpBase import BgpBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.NonProduction.BGP.Resources.BgpSuiteUdks import BgpSuiteUdks
@fixture()
def test_setup_teardown(request):
     def teardown():
         request.instance.Test_Case_Cleanup()
     request.addfinalizer(teardown)
class License03Tests(BgpBase):
     
     @mark.ONE_BOX
     def test_03_BGP_Base_License(self):
         '''[Documentation]  Test_Objective: This_test_is_intended_to_be_run_on_unified_hardware_running_EXOS, version_31.4_or_later. Configure_a_base_license_only_and_verify_2_EBGP_peers_can_be_configured on_the_default_VR.  Attempt_to_configure_a_3rd_peer_and_verify_an_error_is_returned.'''
         # Setup here will run the "Test Suite Setup" in the Resources -> SuiteUdks.robot
         #  change this along the lines of "[Setup]  Test Case Setup" if you have a setup specific to a subset of test cases.
         #[Setup]
         print('  (Step 1) Verify effective license level is Base')
         self.localsuiteudks.Verify_Base_License(self.tb.config.netelem1.name)
         print('  (Step 2) Configure local BGP AS and Router ID and Enable BGP and Verify its enabled')
         self.localsuiteudks.Create_BGP_Instance(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp)
         self.localsuiteudks.Verify_BGP_Enabled(self.tb.config.netelem1.name)
         print('  (Step 3) Create 2 BGP neighbors.')
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1,self.tb.config.globalvars.bgp.remoteAS)
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.bgp.remoteAS)
         print('  (Step 4) Attempt to create a third neighbor with base license.')
         self.localsuiteudks.Create_BGP_Neighbor_Ignore_Error(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer3,self.tb.config.globalvars.bgp.remoteAS)
         print('  (Step 5) Verify the first two neighbors exist on VR-Default')
         self.localsuiteudks.Verify_BGP_Neighbor_Exists(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1,self.tb.config.globalvars.bgp.remoteAS)
         self.localsuiteudks.Verify_BGP_Neighbor_Exists(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.bgp.remoteAS)
         print('  (Step 6) Verify the third neighbor does not exist on VR-Default')
         self.localsuiteudks.Verify_BGP_Neighbor_Does_Not_Exist(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer3,self.tb.config.globalvars.bgp.remoteAS)
         print('  (Step 7) Verify only the number of neighbors on VR-Default is 2')
         self.localsuiteudks.Verify_BGP_Number_Neighbors(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.baseNumPeers)
         self.TestCase3Cleanup()
     def TestCase3Cleanup(self):
         print('  (Step 8) Cleanup delete the BGP neighbors')
         self.localsuiteudks.Delete_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1)
         self.localsuiteudks.Delete_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2)
         self.localsuiteudks.Delete_BGP_Neighbor_Ignore_Invalid(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer3)
         print('  (Step 9) Disable BGP and reset AS and router ID')
         self.localsuiteudks.Disable_BGP_Instance(self.tb.config.netelem1.name)

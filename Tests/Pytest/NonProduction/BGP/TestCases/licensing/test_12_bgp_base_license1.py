from Tests.Pytest.NonProduction.BGP.Resources.BgpBase import BgpBase
from pytest import mark
from pytest import fixture
from Tests.Pytest.NonProduction.BGP.Resources.BgpSuiteUdks import BgpSuiteUdks
@fixture()
def test_setup_teardown(request):
     def teardown():
         request.instance.Test_Case_Cleanup()
     request.addfinalizer(teardown)
class License12Tests(BgpBase):
     
     @mark.ONE_BOX
     @mark.RB
     @mark.TESTS
     def test_12_BGP_Base_License(self):
         '''[Documentation]  Test Objective: This test is intended to be run on unified hardware running EXOS, version 31.4 or later.   Enable and the verify the premier trial license is set, configure 3 peers on a non default user VR.  Reboot and verify the peers are restored. Disable premier license reboot and verify none of the peers are restored.'''
         # Setup here will run the "Test Suite Setup" in the Resources -> SuiteUdks.robot
         #  change this along the lines of "[Setup]  Test Case Setup" if you have a setup specific to a subset of test cases.
         #[Setup]
         print('  (Step 1) Verify effective license level is Base')
         self.localsuiteudks.Verify_Base_License(self.tb.config.netelem1.name)
         print('  (Step 2) Enable Premier trial license')
         self.localsuiteudks.Enable_Premier_Trial_License(self.tb.config.netelem1.name)
         print('  (Step 3) Verify effective license level is Premier')
         self.localsuiteudks.Verify_Premier_License(self.tb.config.netelem1.name)
         print('  (Step 4) Configure local BGP AS and Router ID and Enable BGP on non default user VR')
         self.localsuiteudks.Create_BGP_Instance(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp,self.tb.config.globalvars.vr.vr_user_name)
         print('  (Step 5) Create 3 BGP neighbors on non default user VR')
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vr_user_name)
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vr_user_name)
         self.localsuiteudks.Create_BGP_Neighbor(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer3,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vr_user_name)
         print('  (Step 6) Verify the 3 neighbors exist on non default user VR')
         self.localsuiteudks.Verify_BGP_Neighbor_Exists(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vr_user_name)
         self.localsuiteudks.Verify_BGP_Neighbor_Exists(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vr_user_name)
         self.localsuiteudks.Verify_BGP_Neighbor_Exists(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer3,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vr_user_name)
         self.localsuiteudks.Verify_BGP_Number_Neighbors(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.premierNumPeers,self.tb.config.globalvars.vr.vr_user_name)
         print('  (Step 7) Save the configuration and reboot')
         self.localsuiteudks.Reboot_DUT(self.tb.config.netelem1)
         print('  (Step 8) Verify the 3 neighbors exist on non default user VR after restore')
         self.localsuiteudks.Verify_BGP_Neighbor_Exists(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vr_user_name)
         self.localsuiteudks.Verify_BGP_Neighbor_Exists(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vr_user_name)
         self.localsuiteudks.Verify_BGP_Neighbor_Exists(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer3,self.tb.config.globalvars.bgp.localAS,self.tb.config.globalvars.vr.vr_user_name)
         self.localsuiteudks.Verify_BGP_Number_Neighbors(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.premierNumPeers,self.tb.config.globalvars.vr.vr_user_name)
         print('  (Step 9) Disable premier trial license')
         self.localsuiteudks.Disable_Premier_Trial_License(self.tb.config.netelem1.name)
         print('  (Step 10) Verify effective license level is Base')
         self.localsuiteudks.Verify_Base_License(self.tb.config.netelem1.name)
         print('  (Step 11) Save the configuration and reboot')
         self.localsuiteudks.Reboot_DUT(self.tb.config.netelem1)
         print('  (Step 12) Verify the no neighbors exist on non default user VR after restore with base license')
         self.localsuiteudks.Verify_BGP_Number_Neighbors(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.zeroPeers,self.tb.config.globalvars.vr.vr_user_name)
         self.TestCase12Cleanup()
     def TestCase12Cleanup(self):
         print('  (Step 13) Delete BGP neighbors if necessary')
         self.localsuiteudks.Delete_BGP_Neighbor_Ignore_Invalid(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer1,self.tb.config.globalvars.vr.vr_user_name)
         self.localsuiteudks.Delete_BGP_Neighbor_Ignore_Invalid(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer2,self.tb.config.globalvars.vr.vr_user_name)
         self.localsuiteudks.Delete_BGP_Neighbor_Ignore_Invalid(self.tb.config.netelem1.name,self.tb.config.globalvars.bgp.peer3,self.tb.config.globalvars.vr.vr_user_name)
         print('  (Step 14) Disable BGP and reset AS and router ID')
         self.localsuiteudks.Disable_BGP_Instance(self.tb.config.netelem1.name,self.tb.config.globalvars.vr.vr_user_name)

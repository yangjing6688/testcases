from Tests.Pytest.Functional.nonprod.MACsec.Resources.MACsecBase import MACsecBase
from pytest import mark
from pytest import fixture


@fixture()
def test_setup_teardown(request):
    def teardown():
        request.instance.suiteUdks.Disable_and_Verify_Macsec_Connection(request.instance.tb.dut1.name, 
                                                                        request.instance.tb.dut1.port, 
                                                                        request.instance.tb.dut2.name, 
                                                                        request.instance.tb.dut2.port, 
                                                                        request.instance.tb.config.ca128)
    request.addfinalizer(teardown)

class ConfidentialityOffsetDataDrivenTests(MACsecBase):

    # Test_Template_Confidentiality_Offset_Chosen_by_Key_Server
    #
    # *** Test_Cases ***
    # #                               Confidentiality_Offsets
    # #                                   DUT1_DUT2_Expected
    # # Test_Name_Admin_Admin_Oper
    # #------------------------------  -------  -------  --------
    # 02.20_Default_Offsets_0_0_0
        # [Tags]  NIGHTLY
    # 02.21_Non_Key_Server_Ignored 0 30 0
        # [Tags]  NIGHTLY
    # 02.22_Key_Server_Wins_ 30 50 30
        # [Tags]  NIGHTLY_BUILD
    # 02.23_Key_Server_Wins_Again_50_0_50
        # [Tags]  NIGHTLY
    # 02.24_Same_Non_Default_Offsets_50_50_50
        # [Tags]  NIGHTLY
    
    @mark.NIGHTLY
    @mark.parametrize('dut1_offset,dut2_offset,negotiated_offset', [
                                                ('0', '30', '0'),
                                                ('30', '50', '30'),
                                                ('50', '0', '50'),
                                                ('50', '50', '50'),
                                            ])
    def test_Confidentiality_Offset_Chosen_by_Key_Server(self, dut1_offset, dut2_offset, negotiated_offset, test_setup_teardown):
        """ Configure_DUT1_and_DUT2_with_different (or_the_same) confidentiality
        ...              offsets_and_verify_operational_value_on_both_DUTs_equals_the
        ...              Key_Server's_configured_value. DUT1_is_forced_to_be_Key_Server
        ...              by_configuring_it_with_a_higher_actor_priority.
        ...
        ...              NOTE: Confidentiality_Offset_is_only_configurable_when_EXOS_debug
        ...                    mode_is_enabled! """
        self.suiteUdks.Macsec_Set_Confidentiality_Offset(self.tb.dut1.name, dut1_offset, self.tb.dut1.port)
        self.suiteUdks.Macsec_Set_Confidentiality_Offset(self.tb.dut2.name, dut2_offset, self.tb.dut2.port)
        self.suiteUdks.Create_and_Verify_Macsec_Connection_DUT1_Key_Server(self.tb.dut1.name, self.tb.dut1.port, self.tb.dut2.name, self.tb.dut2.port, self.tb.config.ca128)
    
        
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_port_confidentiality_offset_admin(self.tb.dut1.name, self.tb.dut1.port, dut1_offset)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_port_confidentiality_offset_oper(self.tb.dut1.name, self.tb.dut1.port, negotiated_offset)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_port_confidentiality_offset_admin(self.tb.dut2.name, self.tb.dut2.port, dut2_offset)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_port_confidentiality_offset_oper(self.tb.dut2.name, self.tb.dut2.port, negotiated_offset)
    
      
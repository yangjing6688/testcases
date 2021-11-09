from Tests.Pytest.Functional.nonprod.MACsec.Resources.MACsecBase import MACsecBase
from pytest import mark
from pytest import fixture

@fixture()
def test_setup_teardown(request):
    request.instance.suiteUdks.Add_Port_to_Traffic_VLAN(request.instance.tb.dut1.name, request.instance.tb.dut1.port)
    request.instance.suiteUdks.Add_Port_to_Traffic_VLAN(request.instance.tb.dut2.name, request.instance.tb.dut2.port)
    
    def teardown():
        request.instance.suiteUdks.Remove_Port_from_Traffic_VLAN(request.instance.tb.dut1.name, request.instance.tb.dut1.port)
        request.instance.suiteUdks.Remove_Port_from_Traffic_VLAN(request.instance.tb.dut2.name, request.instance.tb.dut2.port)
    request.addfinalizer(teardown)

class IncludeSCITests(MACsecBase):
    
    # Test_Template_MKA_Include_SCI_Test
    #
    # *** Test_Cases ***
    # #                                 DUT1_DUT2
    # # Test_Name_I-SCI_I-SCI
    # #------------------------------   -----  -----
    # 02.40_Include_SCI_Both_Disabled_False_False
        # [Tags]  NIGHTLY
    # 02.41_Include_SCI_DUT1_Enabled_True_False
        # [Tags]  NIGHTLY
    # 02.42_Include_SCI_DUT2_Enabled_False_True
        # [Tags]  NIGHTLY
    # 02.43_Include_SCI_Both_Enabled_True_True
        # [Tags]  NIGHTLY_BUILD
    
    @mark.NIGHTLY
    @mark.parametrize('dut1_include_sci,dut2_include_sci', [
                                                (False, False),
                                                (True, False),
                                                (False, True),
                                                (True, True),
                                            ])
    def test_MKA_Include_SCI_Test(self, dut1_include_sci, dut2_include_sci, test_setup_teardown):
        """Configure_DUT1_and_DUT2_with_different (or_the_same) Include-SCI
        ...              and_verify_connectivity_in_each_case. """
       
        print( str(self.tb.dut1.name) + " include-sci " + str(dut1_include_sci) + " , " + str(self.tb.dut2.name) + " include-sci " + str(dut2_include_sci))
    
        self.Macsec_Set_Include_Sci(self.tb.dut1.name, self.tb.dut1.port, dut1_include_sci)
        self.Macsec_Set_Include_Sci(self.tb.dut2.name, self.tb.dut2.port, dut2_include_sci)
        self.suiteUdks.Create_and_Verify_Macsec_Connection(self.tb.dut1.name, self.tb.dut1.port, self.tb.dut2.name, self.tb.dut2.port, self.tb.config.ca256)
        self.Clear_Macsec_Counters(self.tb.dut1, self.tb.dut2)
    
        # Note: Testing_one_direction_at_a_time_helped_isolate_an_Xflow_bug; leaving_like_this_for_now
        print(str(self.tb.dut1.name) + " to " + str(self.tb.dut2.name))
        self.suiteUdks.Transmit_Test(tx_count=3000, tx_count_b=0)
        self.Verify_No_Macsec_Errors()
    
        print(str(self.tb.dut2.name) + " to " +  str(self.tb.dut1.name))
        self.suiteUdks.Transmit_Test(tx_count=0, tx_count_b=4000)
        self.Verify_No_Macsec_Errors()
    
        self.suiteUdks.Disable_and_Verify_Macsec_Connection(self.tb.dut1.name, self.tb.dut1.port, self.tb.dut2.name, self.tb.dut2.port, self.tb.config.ca256)
    
    
    def Macsec_Set_Include_Sci(self, dut_name, dut_port, enable):
        if  enable:
            self.defaultLibrary.apiLowLevelApis.macsec.macsec_set_include_sci_enable(dut_name, dut_port)
        else:
            self.defaultLibrary.apiLowLevelApis.macsec.macsec_set_include_sci_disable(dut_name, dut_port)
    
    # TODO: move_next_2_keywords_to_SuiteUdks_because_they_are_used_by_multiple .robot_files
    
    def Clear_Macsec_Counters(self, dut1, dut2):
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_clear_counters_on_port(dut1.name, dut1.port)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_clear_counters_on_port(dut2.name, dut2.port)
    
    def Verify_No_Macsec_Errors(self):
        print("Skip Error Checks becauase DUT2(5420) is echos back every decrypted packet")
        # TODO: add_back_in_error_checking
        # Log_Skip_Error_Checks_becauase_DUT2(5420) is_echos_back_every_decrypted_packet
        # pytest.skip(reason="Error_Checks_becauase_DUT2(5420) is_echos_back_every_decrypted_packet")
        # Verify_No_Macsec_Errors_on_Port  ${dut1.name}  ${dut1.port}
        # Verify_No_Macsec_Errors_on_Port  ${dut2.name}  ${dut2.port}

from Tests.Pytest.NonProduction.MACsec.Resources.MACsecBase import MACsecBase
from pytest import mark
from pytest import fixture


class PortLimitsTests(MACsecBase):

# Test_Template_Macsec_HW_Limits_Test
#
# *** Test_Cases ***
# # Test_Name_DUT_Limit_Type
# #----------------------------  --------  -----------
# 06.10_DUT1_Port_Limits          ${dut1}   port_limit
    # [Tags]  NIGHTLY
# # 06.11_DUT1_Bandwidth_Limits     ${dut1}     bw_limit
# #     [Tags]  NIGHTLY
# 06.15_DUT2_Port_Limits          ${dut2}   port_limit
    # [Tags]  NIGHTLY
# # 06.16_DUT2_Bandwidth_Limits     ${dut2}     bw_limit
# #     [Tags]  NIGHTLY

    @mark.NIGHTLY
    @mark.parametrize('dut,limit_type', [
                                            (1, 'port_limit'),
                                            (1, 'bw_limit'),
                                            (2, 'port_limit'),
                                            (2, 'bw_limit'),
                                        ])
    def test_Macsec_HW_Limits_Test(self, dut, limit_type):
        """ Some_MACsec-capable_products_have_a_hard_limit_to_the_number_ports
        ...              on_which_MACsec_can_be_enabled, and_on_the_overall_bandwidth_of
        ...              MACsec-enabled_ports.  These_limits_must_be_coded_in_the_testbed_yaml
        ...              as 'netelemX.macsec.port_limit' and 'netelemX.macsec.bw_limit'.
        ...              If_these_limits_are_not_found, then_this_test_will_be_skipped. """
        
        if dut == 1:
            dut = self.tb.dut1
        elif dut == 2:
            dut = self.tb.dut2
    
        self.suiteUdks.Skip_Test_if_DUT_Has_No_HW_Limits(dut, limit_type)
    
        limit = dut.macsec[limit_type]
        print(dut.name + " limit_info  " + limit)
    
        self.Macsec_Enable_Maximum_Allowable_Ports(dut, limit)
    
        if (limit.port_outside_range is not None):
            self.Verify_Enabling_Macsec_on_Port_Fails(dut, limit.port_outside_range)
            self.Disable_One_Port_to_Make_Room_for_Another_Port(dut, limit.port_inside_range)
            self.Verify_Enabling_Macsec_on_Port_Allowed(dut, limit.port_outside_range)
        else:
            print("Skip_remaining_tests_because " + dut.name + " does_not_have_enough_ports_to_exceed_limit")
    
        self.Macsec_Disable_All_Ports(dut, limit_type)
        
    
    def Macsec_Enable_Maximum_Number_of_Ports(self):
        # TODO: run_tests_using_both_DUT1_and_DUT2
        # ${dut}=  Set_Variable_If  '${dut1.macsec.port_limit}'=='None'  ${dut2}  ${dut1}
        if dut1.macsec.port_limit is None:
          dut = self.tb.dut2
        else: 
          dut = self.tb.dut1
    
        if dut.macsec.port_limit is None:
            print("Skip_test_because_neither " + dut1.name + " nor " + dut2.name + " has_MACsec_port_limits")
        else:
            # ${limit}=  Set_Variable  ${dut.macsec.port_limit}
            limit = dut.macsec.bw_limit
            pint("Port_Limit_Info " + str(limit))
        
            self.suiteUdks.Create_and_Verify_Connectivity_Association(dut.name, dut.ca)
            self.defaultLibrary.apiLowLevelApis.macsec.macsec_enable_ca_port(dut.name, dut.ca.name, limit.allowed_range)
    
    def Macsec_Enable_Maximum_Allowable_Ports(self, dut, limit):
        self.suiteUdks.Create_and_Verify_Connectivity_Association(dut.name, dut.ca)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_enable_ca_port(dut.name, dut.ca.name, limit.allowed_range)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_enabled_on_port(dut.name, limit.port_inside_range)
    
    def Macsec_Disable_All_Ports(self, dut, limit_type):
        self.suiteUdks.Skip_Test_if_DUT_Has_No_HW_Limits(dut, limit_type)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_disable_ca_port(dut.name, dut.ca.name, dut.ports_all)
        self.suiteUdks.Delete_and_Verify_Connectivity_Association(dut.name, dut.ca)
    
    def Verify_Enabling_Macsec_on_Port_Fails(self, dut, port_to_enable):
        # Run_Keyword_and_Expect_Error  *   
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_enable_ca_port(dut.name, dut.ca.name, port_to_enable, expect_error=True)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_disabled_on_port(dut.name, port_to_enable)
    
    def Verify_Enabling_Macsec_on_Port_Allowed(self, dut, port_to_enable):
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_enable_ca_port(dut.name, dut.ca.name, port_to_enable)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_enabled_on_port(dut.name, port_to_enable)
    
    def Disable_One_Port_to_Make_Room_for_Another_Port(self, dut, port_to_disable):
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_disable_ca_port(dut.name, dut.ca.name, port_to_disable)
        self.defaultLibrary.apiLowLevelApis.macsec.macsec_verify_disabled_on_port(dut.name, port_to_disable)

from Tests.Pytest.Functional.nonprod.MACsec.Resources.MACsecBase import MACsecBase
from pytest import mark
from pytest import fixture
from pytest import skip

class CipherSuiteStrengthPermutationsTests(MACsecBase):

# #                            Confidentiality Offsets
# # Test Name                                     Port   CAK  Cipher
# #---------------------------------------------  ----  ----  ------
# 02.30 Weak Port+CAK+Cipher, Allowed              128   128     128
    # [Tags]  NIGHTLY
# 02.31 Weak Port+CAK Strong Cipher, NOT Allowed   128   128     256
    # [Tags]  NIGHTLY
# 02.32 Weak Port+Cipher Strong CAK, Allowed       128   256     128
    # [Tags]  NIGHTLY
# 02.33 Weak Port Strong CAK+Cipher, NOT Allowed   128   256     256
    # [Tags]  NIGHTLY
# 02.34 Strong Port Weak CAK+Cipher, Allowed       256   128     128
    # [Tags]  NIGHTLY
# 02.35 Strong Port+Cipher Weak CAK, NOT Allowed   256   128     256
    # [Tags]  NIGHTLY  BUILD
# 02.36 Strong Port CAK Weak+Cipher, Allowed       256   256     128
    # [Tags]  NIGHTLY
# 02.37 Strong Port+CAK+Cipher, Allowed            256   256     256
    
    @mark.NIGHTLY
    @mark.parametrize('port_bits,cak_bits,cipher_bits', [
                                                ('128', '128', '128'),
                                                ('128', '128', '256'),
                                                ('128', '256', '128'),
                                                ('128', '256', '256'),
                                                ('256', '128', '128'),
                                                ('256', '128', '256'),
                                                ('256', '256', '128'),
                                                ('256', '256', '256'),
                                            ])
    def test_Cipher_Suite_Config(self, port_bits, cak_bits, cipher_bits):
        """ [Documentation]  Test_CLI_acceptance_of_varying_CAK_and_Cipher_key_strengths.
        ...              Cipher_GCM-AES-128_can_be_enabled_with_any_CAK_on_any_port.
        ...              Cipher_GCM-AES-256_can_only_be_enabled_with_256-bit_CAK_on_256-bit_port. """
        try:
            if port_bits == '128':
                port = self.tb.dut1.port128
            else:
                port = self.tb.dut1.port256
                
            if cak_bits == '128':
               ca = self.tb.config.ca128
            else:
                ca = self.tb.config.ca256
            cipher_suite =  'gcm-aes-' + str(cipher_bits)
            print( str(port_bits) + ' CAK  '+ str(cak_bits) + ' Cipher ' + str(cipher_bits))
            print( str(port) + ' CA  '+ str(self.tb.dut1.name) + ' Cipher '  + str(cipher_suite))
        
            if  port == None:
                skip(msg="Skip_test_because_DUT " + self.tb.dut1.name + " does_not_have_a_MACsec_gcm-aes-" + cipher_bits + " port")
        
            # run_keyword_and_return_if
            if  port_bits < cipher_bits:
                self.Set_Macsec_Cipher_Suite_and_Expect_Failure(self.tb.dut1.name, port, cipher_suite)
                
            self.suiteUdks.Set_Macsec_Cipher_Suite(self.tb.dut1.name, port, cipher_suite)
        
            # run_keyword_and_return_if
            if  cak_bits < cipher_bits:
                self.Enable_and_Verify_Macsec_on_Port_Expect_Failure(self.tb.dut1.name, ca, port)
        
            self.suiteUdks.Enable_and_Verify_Macsec_on_Port(self.tb.dut1.name, ca, port) 
        except Exception:
            self.suiteUdks.Set_Macsec_Cipher_Suite(self.tb.dut1.name,
                                                   port)
            
            self.suiteUdks.Disable_and_Verify_Macsec_on_Port(self.tb.dut1.name,
                                                             ca,
                                                             port,
                                                             ignore_error="Error", 
                                                             ignore_cli_feedback=True)
    
    
    def Set_Macsec_Cipher_Suite_and_Expect_Failure(self, dut_name, port, cipher_suite):
        # run_keyword_and_expect_error
        self.suiteUdks.Set_Macsec_Cipher_Suite(dut_name, port, cipher_suite, expect_error=True) 
    
    def Enable_and_Verify_Macsec_on_Port_Expect_Failure(self, dut1_name, ca, port):
        # run_keyword_and_expect_error  *
        self.suiteUdks.Enable_and_Verify_Macsec_on_Port(dut1_name, ca, port, expect_error=True)

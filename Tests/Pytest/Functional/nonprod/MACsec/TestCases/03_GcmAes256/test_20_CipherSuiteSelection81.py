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


class CipherSuiteSelectionTests(MACsecBase):

    # Test Template  Cipher Suite Selected by Key Server
    #
    # *** Test Cases ***
    # #                                ------------- Cipher Suites -------------
    # # Test Name                      DUT1 Admin     DUT2 Admin     Expected Oper
    # #------------------------------  -----------    -----------    -----------
    # 03.20 Both Configured for 128    gcm-aes-128    gcm-aes-128    gcm-aes-128
        # [Tags]  NIGHTLY
    # 03.21 Key Server Chooses 128     gcm-aes-128    gcm-aes-256    gcm-aes-128
        # [Tags]  NIGHTLY
    # 03.22 Key Server Chooses 256     gcm-aes-256    gcm-aes-128    gcm-aes-256
        # [Tags]  NIGHTLY  BUILD
    # 03.23 Both Configured for 256    gcm-aes-256    gcm-aes-256    gcm-aes-256
        # [Tags]  NIGHTLY

    @mark.NIGHTLY
    @mark.parametrize('dut1_cipher_suite,dut2_cipher_suite, expected_cipher_suite', [
                                                ('gcm-aes-128', 'gcm-aes-128','gcm-aes-128'),
                                                ('gcm-aes-128', 'gcm-aes-256','gcm-aes-128'),
                                                ('gcm-aes-256', 'gcm-aes-128','gcm-aes-256'),
                                                ('gcm-aes-256', 'gcm-aes-256','gcm-aes-256'),
                                            ])
    def Cipher_Suite_Selected_by_Key_Server(self, dut1_cipher_suite, dut2_cipher_suite, expected_cipher_suite, test_setup_teardown):
        """ Configure DUT1 and DUT2 with different (or the same) cipher
        ...              suite and verify operational value on both DUTs equals the
        ...              Key Server's configured value. DUT1 is forced to be Key Server
        ...              by configuring it with a higher actor priority. """
        self.suiteUdks.Skip_Test_if_gcm_aes_256_Not_Supported()
        
        self.suiteUdks.Set_Macsec_Cipher_Suite(self.tb.dut1.name, self.tb.dut1.port256, dut1_cipher_suite)
        self.suiteUdks.Set_Macsec_Cipher_Suite(self.tb.dut2.name, self.tb.dut2.port256, dut2_cipher_suite)
        
        self.suiteUdks.Create_and_Verify_Macsec_Connection_DUT1_Key_Server(self.tb.dut1.name, self.tb.dut1.port256, self.tb.dut2.name, self.tb.dut2.port256, self.tb.config.ca256)
        
        self.suiteUdks.Macsec_Verify_Port_Cipher_Suite_Admin(self.tb.ut1.name, self.tb.dut1.port256, dut1_cipher_suite)
        self.suiteUdks.Macsec_Verify_Port_Cipher_Suite_Oper(self.tb.dut1.name, self.tb.dut1.port256, expected_cipher_suite)
        self.suiteUdks.Macsec_Verify_Port_Cipher_Suite_Admin(self.tb.dut2.name, self.tb.dut2.port256, dut2_cipher_suite)
        self.suiteUdks.Macsec_Verify_Port_Cipher_Suite_Oper(self.tb.dut2.name, self.tb.dut2.port256, expected_cipher_suite)

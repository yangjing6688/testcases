'''*** Settings ***
Resource    ../Resources/AllResources.robot'''
#*** Test Cases ***
#04 AAA Login Validation

from pytest import fixture,mark

from Tests.Pytest.NonProduction.AAA.Resources.AAASuiteUdks import AAASuiteUdks
from Tests.Pytest.NonProduction.AAA.Resources.AAABase import AAABase


class AAA_Login_Validation_04Tests(AAABase):
    
    @mark.F_A000_0004    
    @mark.release_30_7
    @mark.BUILD
    def test_00_04_aaa_login_validation(self):
        '''[Documentation]  Test Objective: Verify Login and Password Policy Attributes.
        [Tags]   F-A000-0004  30.7  BUILD  LoginValidation'''
    
    # Setup here will run the "Test Suite Setup" in the Resources -> SuiteUdks.robot
    #  change this along the lines of "[Setup]  Test Case Setup" if you have a setup specific to a subset of test cases.
       #[Setup]  AAA Login Validation Test Case Setup
        self.AAA_Login_Validation_Test_Case_Setup()
    #   This library allows us to pause execution with the "pause execution" keyword.
    #    import library dialogs
    
        #Log  (Step 1) Verify Successful Login Information based on successful logins..
        self.aaaSuiteUdks.create_log_message ("(Step 1) Verify Successful Login Information based on successful logins..")
        # First Successful Login - though it is checking the failed login count.
        #verify failed login attempts on login    ${netelem1.name}  ${netelem1.ip}  manager  passwd  0  telnet
        self.aaaSuiteUdks.networkElementHostUtilsKeywords.verify_failed_login_attempts_on_login(self.tb.config.netelem1.name,self.tb.config.netelem1.ip, 'manager', 'passwd', 
                                                                                   str(0), 'telnet')
        
        
        # First Failed Login - used to increment the failed counter(s)
        #verify failed login attempts on login    ${netelem1.name}  ${netelem1.ip}  manager  badpasswd  0  telnet  expect_error=true
        self.aaaSuiteUdks.networkElementHostUtilsKeywords.verify_failed_login_attempts_on_login(self.tb.config.netelem1.name,self.tb.config.netelem1.ip, 'manager', 'badpasswd', 
                                                                                   str(0), 'telnet',expect_error=True)
    
        # Second Successful Login
        #verify successful login attempts on login  ${netelem1.name}  ${netelem1.ip}  manager  passwd  2  telnet    
        self.aaaSuiteUdks.networkElementHostUtilsKeywords.verify_successful_login_attempts_on_login(self.tb.config.netelem1.name,self.tb.config.netelem1.ip, 'manager', 'passwd',
                                                                                        str(2), connection_type="telnet")
        
        
        # Third Successful Login - to check for a last login date.
        #verify last login date exists     ${netelem1.name}  ${netelem1.ip}  manager  passwd  telnet
        self.aaaSuiteUdks.networkElementHostUtilsKeywords.verify_last_login_date_exists(self.tb.config.netelem1.name,self.tb.config.netelem1.ip, 'manager', 'passwd',
                                          connection_type="telnet")
    
        # Fourth Successful Login - Check for logout message.   - Bug in implementation caused this to be un-implemented.
        #  BUG ALERT ...
        # Since this is commented out The next successuful login down the road is now the fourth and we check for four
        # successful logins rather than 5 which was done previously.
        #verify logout message exists   ${netelem1.name}  ${netelem1.ip}  manager  passwd  telnet
    
        # Second Failed Login - used to increment the failed counter(s).
        #verify failed login attempts on login    ${netelem1.name}  ${netelem1.ip}  manager  badpasswd  0  telnet  expect_error=true
        self.aaaSuiteUdks.networkElementHostUtilsKeywords.verify_failed_login_attempts_on_login(self.tb.config.netelem1.name,self.tb.config.netelem1.ip, 'manager', 'badpasswd', 
                                                                                   str(0), 'telnet',expect_error=True)
    
        # Third Failed Login - used to increment the failed counter(s)
        #verify failed login attempts on login    ${netelem1.name}  ${netelem1.ip}  manager  badpasswd  0  telnet  expect_error=true
        self.aaaSuiteUdks.networkElementHostUtilsKeywords.verify_failed_login_attempts_on_login(self.tb.config.netelem1.name,self.tb.config.netelem1.ip, 'manager', 'badpasswd', 
                                                                                   str(0), 'telnet',expect_error=True)
        # Fourth Successful login - Check that there were two failed logins from the last successful login.
        #loginconfig verify failed login attempts since success   ${netelem1.name}  manager  2
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_failed_login_attempts_since_success(self.tb.config.netelem1.name, username='manager', login_attempts='2')
        #verify failed login attempts on login    ${netelem1.name}  ${netelem1.ip}  manager  passwd  2  telnet
        self.aaaSuiteUdks.networkElementHostUtilsKeywords.verify_failed_login_attempts_on_login(self.tb.config.netelem1.name,self.tb.config.netelem1.ip, 'manager', 'passwd', 
                                                                                   str(2), 'telnet')
    
    
        #loginconfig verify total failed login attempts   ${netelem1.name}  manager  3
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_total_failed_login_attempts(self.tb.config.netelem1.name, username='manager', login_attempts='3')
            
        #loginconfig verify successful logins     ${netelem1.name}  manager  4
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_successful_logins(self.tb.config.netelem1.name, username='manager', login_attempts='4')
    
        #Log  (Step 2) Verify password length minimums are observed..
        self.aaaSuiteUdks.create_log_message("(Step 2) Verify password length minimums are observed..")
        #loginconfig set account password policy min length  ${netelem1.name}  manager  10
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_set_account_password_policy_min_length(self.tb.config.netelem1.name, username='manager', min_length='10')
        #loginconfig verify password min length   ${netelem1.name}  manager  10
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_password_min_length(self.tb.config.netelem1.name, username='manager', length='10')
        #loginconfig set account password  ${netelem1.name}   manager   passwd   TooShort  expect_error=true
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_set_account_password(self.tb.config.netelem1.name, username='manager', old_password='passwd', new_password='TooShort', expect_error=True)
        #loginconfig set account password  ${netelem1.name}   manager   passwd   LongEnough
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_set_account_password(self.tb.config.netelem1.name, username='manager', old_password='passwd', new_password='LongEnough')
        #Log  (Step 3) Verify password minimum character difference setting is observed..
        self.aaaSuiteUdks.create_log_message("(Step 3) Verify password minimum character difference setting is observed..")    
        #loginconfig set account password policy min length  ${netelem1.name}  manager  5
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_set_account_password_policy_min_length(self.tb.config.netelem1.name, username='manager', min_length='5')
        #loginconfig verify password min length   ${netelem1.name}  manager  5
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_password_min_length(self.tb.config.netelem1.name, username='manager', length='5')
        #loginconfig set account password policy min different chars   ${netelem1.name}  manager  8    
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_set_account_password_policy_min_different_chars(self.tb.config.netelem1.name, username='manager', min_chars='8')
        #loginconfig verify password min diff chars   ${netelem1.name}  manager  8
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_password_min_diff_chars(self.tb.config.netelem1.name, username='manager', min_diff_chars='8')
        #loginconfig set account password  ${netelem1.name}   manager   LongEnough  AllDifferentChars
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_set_account_password(self.tb.config.netelem1.name, username='manager', old_password='LongEnough', new_password='AllDifferentChars')
        #  Fails (missing characters don't count as different)
        #loginconfig set account password  ${netelem1.name}   manager   AllDifferentChars  AllDi  expect_error=true
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_set_account_password(self.tb.config.netelem1.name, username='manager', old_password='AllDifferentChars', new_password='AllDi',expect_error=True)
        #  Passes 8 characters are the different
        #loginconfig set account password  ${netelem1.name}   manager   AllDifferentChars  NewShort
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_set_account_password(self.tb.config.netelem1.name, username='manager', old_password='AllDifferentChars', new_password='NewShort')
        #  Passes 8 characters are either different or additional
        #loginconfig set account password  ${netelem1.name}   manager   NewShort  NewLongLong
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_set_account_password(self.tb.config.netelem1.name, username='manager', old_password='NewShort', new_password='NewLongLong')
        #  Fails less than 8 different or new characters.
        #loginconfig set account password  ${netelem1.name}   manager   NewLongLong  NewShrtLongSht   expect_error=true
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_set_account_password(self.tb.config.netelem1.name, username='manager', old_password='NewLongLong', new_password='NewShrtLongSht',expect_error=True)
        #Log  (Step 4) Verify password minimum and max age config settings..
        self.aaaSuiteUdks.create_log_message ("(Step 4) Verify password minimum and max age config settings..")
        #loginconfig set account password policy min age     ${netelem1.name}  manager  5
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_set_account_password_policy_min_age(self.tb.config.netelem1.name, username='manager', age='5')
        #loginconfig verify password min age  ${netelem1.name}  manager  5
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_password_min_age(self.tb.config.netelem1.name, username='manager', age='5')
        #loginconfig set account password policy max age     ${netelem1.name}  manager  10    
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_set_account_password_policy_max_age(self.tb.config.netelem1.name, username='manager', age='10')
        #loginconfig verify password max age   ${netelem1.name}  manager  10    
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_password_max_age(self.tb.config.netelem1.name, username='manager', age='10')
        #Log  (Step 5) Do some range checking for invalid values on the CLI inputs
        self.aaaSuiteUdks.create_log_message("(Step 5) Do some range checking for invalid values on the CLI inputs")
        #loginconfig verify password max age   ${netelem1.name}  manager  -1    expect_error=true
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_password_max_age(self.tb.config.netelem1.name, username='manager', age='-1', expect_error=True)
        #loginconfig verify password max age   ${netelem1.name}  manager  0     expect_error=true
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_password_max_age(self.tb.config.netelem1.name, username='manager', age='0', expect_error=True)
        #loginconfig verify password max age   ${netelem1.name}  manager  366   expect_error=true
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_password_max_age(self.tb.config.netelem1.name, username='manager', age='366', expect_error=True)
        #loginconfig verify password min age   ${netelem1.name}  manager  -1    expect_error=true
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_password_min_age(self.tb.config.netelem1.name, username='manager', age='-1', expect_error=True)
        #loginconfig verify password min age   ${netelem1.name}  manager  0     expect_error=true
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_password_min_age(self.tb.config.netelem1.name, username='manager', age='0', expect_error=True)
        #loginconfig verify password min age   ${netelem1.name}  manager  366   expect_error=true
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_password_min_age(self.tb.config.netelem1.name, username='manager', age='366', expect_error=True)
        #loginconfig set account password policy min different chars   ${netelem1.name}  manager  -1  expect_error=true
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_set_account_password_policy_min_different_chars(self.tb.config.netelem1.name, username='manager', min_chars='-1', expect_error=True)
        # min different characters of zero is allowed.
        #loginconfig set account password policy min different chars   ${netelem1.name}  manager  17  expect_error=true
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_set_account_password_policy_min_different_chars(self.tb.config.netelem1.name, username='manager', min_chars='17',expect_error=True)
        #loginconfig set account password policy min length  ${netelem1.name}  manager  -1   expect_error=true
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_set_account_password_policy_min_length(self.tb.config.netelem1.name, username='manager', min_length='-1', expect_error=True)
        #loginconfig set account password policy min length   ${netelem1.name}  manager  0   expect_error=true
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_set_account_password_policy_min_length(self.tb.config.netelem1.name, username='manager', min_length='0', expect_error=True)
        #loginconfig set account password policy min length   ${netelem1.name}  manager  33  expect_error=true
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_set_account_password_policy_min_length(self.tb.config.netelem1.name, username='manager', min_length='33', expect_error=True)
        #Log  (Step 6) NOTE - GLOBAL CONFIG password policy attributes are not currently checked...
        self.aaaSuiteUdks.create_log_message("(Step 6) NOTE - GLOBAL CONFIG password policy attributes are not currently checked...")    
        #[Teardown]  AAA Login Validation Test Case Cleanup
        self.AAA_Login_Validation_Test_Case_Cleanup()

    #*** Keywords ***
    def AAA_Login_Validation_Test_Case_Setup(self):
        self.aaaSuiteUdks.AAA_Common_Test_Case_Setup()
        #loginconfig create admin account   ${netelem1.name}  manager  passwd
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_create_admin_account(self.tb.config.netelem1.name, username='manager', 
                                                                                   passwd='passwd')
        #loginconfig verify admin account exists   ${netelem1.name}  manager
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_verify_admin_account_exists(self.tb.config.netelem1.name, 
                                                                                          username='manager')
    
    # This section is used to create a user-defined keyword to clean up configuration made by this test case.
    def AAA_Login_Validation_Test_Case_Cleanup(self):
        # Will Dump Syslogs and Traces on a Test Failure
        self.aaaSuiteUdks.AAA_Common_Failure_Info_Dump()
        #loginconfig delete account     ${netelem1.name}  manager
        self.aaaSuiteUdks.networkElementLoginconfigGenKeywords.loginconfig_delete_account(self.tb.config.netelem1.name, username='manager')
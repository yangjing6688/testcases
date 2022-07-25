# Author        : sowmya
# Date          : May 26th 2021
# Modified      : Jay Moorkoth
# Date          : June 9th 2022
# Description   : Gemalto License Test Cases
# TestData      : Create a new user for this test run. Use a new Entitlement Key (EKEY) for every test that requires this key.
# TestData      : SFDC credentials will be updated once every few months, make sure the credentials and shared cuid are as required.

########################################################################################################################
*** Variables ***
#${LOGIN_OPTION}             trial or legacylicense or extremecloudiqlicense or connect
#For now please keep the below account for  license sanity
#May change once new accounts are created
${EKEY}                     None 
${SFDC_USER_TYPE}           partner
${SFDC_PARTNER_EMAIL}       ahqalabpw1+part11@gmail.com 
${SFDC_PARTNER_PWD}         Aerohive123
${SHARED_CUID}              FJtHxWDlE 
${SFDC_CUST_EMAIL}          ahqalabwp+cust1@gmail.com 
${SFDC_CUST_PWD}            Aerohive123 
*** Settings ***
Library     Collections
Library     common/Cli.py
Library     common/Utils.py
Library     common/TestFlow.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/manage/Client.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Device360.py
Library     xiq/flows/manage/DeviceCliAccess.py
Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/manage/Applications.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     xiq/elements/NetworkPolicyWebElements.py
Library	    xiq/flows/globalsettings/LicenseManagement.py
Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml
Force Tags   testbed_not_required
*** Test Cases ***
TCCS-11519: Welcome Page TRIAL User login to XIQ
    [Documentation]  Trial customer login to XIQ and verify link to extr portal is available
    [Tags]   sanity   gemaltolicense   development   tccs-11519  
    welcome page login  ${tenant_username}     ${tenant_password}   trial
    ${result1}=  navigate to license mgmt
    should be equal as strings  '${result1}'  '1'
    ${result2}=  verify xiq not linked to extr portal
    should be equal as strings  '${result2}'  '1'
    Logout User
    Quit Browser
TCCS-6614: Welcome Page CONNECT User login to XIQ
    [Documentation]  Connect customer login to XIQ and verify link to extr portal is available
    [Tags]   sanity  gemaltolicense   development   tccs-6614
    welcome page login   ${tenant_username}     ${tenant_password}   connect
    ${result1}=  verify upgrade option for connect user
    should be equal as strings  '${result1}'  '1'
    ${result2}=  verify xiq not linked to extr portal
    should be equal as strings  '${result2}'  '1'
    Logout User
    Quit Browser
TCCS-6657: Customer Links XIQ to extreme portal from welcome page
    [Documentation]  ExtremeCloud IQ option customer linking flow
    [Tags]   sanity  gemaltolicense   development   tccs-6657
    ${result1}=  welcome page login  ${tenant_username}   ${tenant_password}   extremecloudiqlicense     ${EKEY}    customer  ${SFDC_CUST_EMAIL}  ${SFDC_CUST_PWD}
    should be equal as strings  '${result1}'  '1'
    ${result2}=  navigate to license mgmt
    should be equal as strings  '${result2}'  '1'
    ${result4}=  verify contact sales btn dispalyed
    should be equal as strings  '${result4}'  '1'
    ${result5}=  navigate to license mgmt
    should be equal as strings  '${result5}'  '1'
    ${result6}=  unlink xiq from extr portal
    should be equal as strings  '${result6}'  '1'
    Logout User
    Quit Browser
TCCS-6597: Partner Links XIQ to extreme portal from welcome page
    [Documentation]  ExtremeCloud IQ option partner linking flow
    [Tags]   sanity  gemaltolicense   development   tccs-6597
    ${result1}=  welcome page login   ${tenant_username}   ${tenant_password}   extremecloudiqlicense   ${EKEY}    partner   ${SFDC_PARTNER_EMAIL}  ${SFDC_PARTNER_PWD}  ${SHARED_CUID}
    should be equal as strings  '${result1}'  '1'
    ${result2}=  navigate to license mgmt
    should be equal as strings  '${result2}'  '1'
    ${result4}=  verify contact sales btn dispalyed
    should be equal as strings  '${result4}'  '1'
    ${result5}=  navigate to license mgmt
    should be equal as strings  '${result5}'  '1'
    ${result6}=  unlink xiq from extr portal
    should be equal as strings  '${result6}'  '1'
    Logout User
    Quit Browser
TCCS-10206: Trial Account - Customer links to Extreme Portal from License Mgt UI
    [Documentation]  Trial Account - customer links to extr portal from lic mgt
    [Tags]   sanity  gemaltolicense   development   tccs-10206
    welcome page login    ${tenant_username}    ${tenant_password}   trial
    ${result1}=  navigate to license mgmt
    should be equal as strings  '${result1}'  '1'
    ${result6}=  verify xiq not linked to extr portal
    should be equal as strings  '${result6}'  '1'
    ${result2}=  initiate link xiq to extr portal from lic mgt
    should be equal as strings  '${result2}'  '1'
    ${result3}=  link xiq to extreme portal  customer  ${SFDC_CUST_EMAIL}  ${SFDC_CUST_PWD}
    should be equal as strings  '${result3}'  '1'
    ${result5}=  unlink xiq from extr portal
    should be equal as strings  '${result5}'  '1'
    Logout User
    Quit Browser
TCCS-10207: Trial Account - Partner links to Extreme Portal from License Mgt UI
    [Documentation]  Trial Account - partner links to extr portal from lic mgt
    [Tags]   sanity  gemaltolicense   development   tccs-10207
    welcome page login  ${tenant_username}   ${tenant_password}   trial
    ${result1}=  navigate to license mgmt
    should be equal as strings  '${result1}'  '1'
    ${result6}=  verify xiq not linked to extr portal
    should be equal as strings  '${result6}'  '1'
    ${result2}=  initiate link xiq to extr portal from lic mgt
    should be equal as strings  '${result2}'  '1'
    ${result3}=  link xiq to extreme portal  partner  ${SFDC_PARTNER_EMAIL}  ${SFDC_PARTNER_PWD}  ${SHARED_CUID}
    should be equal as strings  '${result3}'  '1'
    ${result5}=  unlink xiq from extr portal
    should be equal as strings  '${result5}'  '1'
    Logout User
    Quit Browser

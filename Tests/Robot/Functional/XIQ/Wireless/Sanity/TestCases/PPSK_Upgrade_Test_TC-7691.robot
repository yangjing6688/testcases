# Author        : asaha
# Date          : August 2021
# Description   : Verify ppsk users across upgrades TC-6759

# Topology      :
# Client -----> AP --->XIQ Instance
# Pre-Condtion
# 1. AP should be onboarded and it is online
# 2. start the remote srevre in MU. Starting remote server on MU refer testsuite/xiq/config/remote_server_config.txt
# 3. Start the stand alone selenium server on MU refer:testsuite/xiq/config/remote_server_config.txt
# 4. Required Device: 1 AP, 1 Windows10 MU

# Execution Command:
# robot -L INFO -v TESTBED:blr_tb_1 -v DEVICE:AP550 -v TOPO:topo-1 -i production  PPSK_Upgrade_Test_TC-7691.robot
# Select the "TOPO" and "DEVICE" variable based on Test bed

# Test Case TC-6759 Verify ppsk users across upgrades
# https://aerohive.qtestnet.com/p/101056/portal/project#tab=testdesign&object=1&id=49612165
*** Variables ***
${PPSK_UPGRADE_TEST_NW}             PPSK_UPGRADE_NW
${PPSK_UPGRADE_TEST_SSID}           PPSK_UPGRADE_SSID
${MULTIPLE_CLOUD_USER_GROUP}        AUTO_CLOUD_MLT_GRP

${user1}    upgrade_1
${user2}    upgrade_2
${user3}    upgrade_3
${user4}    upgrade_4

${pass1}    motorolamotorola
${pass2}    zebrazebra
${pass3}    extremeextreme
${pass4}    aerohiveaerohive
${pass4_changed}    symbolsymbol

${PAGE_TITLE}                       End-to-End Cloud Driven Networking Solutions - Extreme Networks

*** Settings ***
Library     Collections
Library     common/Utils.py
Library     common/LoadBrowser.py
Library     common/Cli.py
Library     common/TestFlow.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/common/MuCaptivePortal.py

Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DeviceCliAccess.py
Library     xiq/flows/manage/ClientMonitor.py
Library     xiq/flows/manage/Client.py

Library     xiq/flows/configure/UserGroups.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py

Library     xiq/flows/mlinsights/MLInsightClient360.py
Library     xiq/flows/globalsettings/GlobalSetting.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Resource    test_email_ids.robot
Resource    ppsk_upgrade_test_config_XIQ-000.robot

Library	    Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   mu1

Suite Setup      Pre Condition

*** Keywords ***
Pre Condition
    [Documentation]   AP Should be onboarded  and it is online
    ${result}=                      Login User                 ${tenant_username}     ${tenant_password}
    ${AP_STATUS}=                   Get AP Status              ap_mac=${ap1.mac}
    Should Be Equal As Strings     '${AP_STATUS}'             'green'

    [Teardown]   run keywords      logout user
    ...                            quit browser

Connect Ppsk Wireless Network
    [Arguments]    ${NETWORK}    ${KEY}
    ${CONNECT_STATUS}=   mu1.connect_wpa2_ppsk_network    ${NETWORK}    ${KEY}
    should be equal as strings  '${CONNECT_STATUS}'    '1'

Wi-Fi Interface IP Address Check
    ${IP}=   mu1.Get Wi Fi Interface Ip Address
    should contain any  ${IP}     ${mu1.wifi_network}    ${mu1.wifi_network_vlan10}

Re Connect To PPSK Network
    [Arguments]    ${NETWORK}     ${KEY}
    mu1.disconnect_wifi
    sleep                            ${client_disconnect_wait}
    Connect Ppsk Wireless Network    ${NETWORK}   ${KEY}
    ${URL_TITLE}=                    Check Internet Connectivity     ${mu1.ip}
    should be equal as strings       '${URL_TITLE}'   '${PAGE_TITLE}'

Test Case Level Cleanup
     Logout User
     Quit Browser
     mu1.disconnect_wifi

*** Test Cases ***
TC-6759_Step1: Create User Group and Network for PPSK Upgrade Test
    [Documentation]    Create User Group and Network for PPSK Upgrade Test
    [Tags]             TC-6759_Step1      upgrade-test

    ${LOGIN_STATUS}=                  Login User              ${tenant_username}     ${tenant_password}
    should be equal as strings       '${LOGIN_STATUS}'        '1'

    ${USER_GROUP_CREATE}=             Create User Group        ${MULTIPLE_CLOUD_USER_GROUP}   user_group_profile=&{USER_GROUP_PROFILE_CLOUD_MULTIPLE}
    should be equal as strings       '${USER_GROUP_CREATE}'   '1'

    ${NW_STATUS}=                     Create Network Policy    ${PPSK_UPGRADE_TEST_NW}      &{PPSK_UPGRADE_TEST_NW_PROFILE}
    should be equal as strings       '${NW_STATUS}'   '1'


    ${DELTA_UPDATE}=                  Update Network Policy To Ap    policy_name=${PPSK_UPGRADE_TEST_NW}    ap_serial=${ap1.serial}
    should be equal as strings       '${DELTA_UPDATE}'   '1'
    sleep                             ${config_push_wait}

    ${AP_SPAWN}=            Open Spawn          ${ap1.console_ip}       ${ap1.console_port}      ${ap1.username}       ${ap1.password}        ${ap1.platform}
    ${SHOW_CONFIG1}=        Send                ${AP_SPAWN}             show ssid
    Should Contain          ${SHOW_CONFIG1}     ${PPSK_UPGRADE_TEST_SSID}
    close spawn  ${AP_SPAWN}

    [Teardown]   run keywords      logout user
    ...                            quit browser

TC-6759_Step2: Connect Client with User1 Credentials
    [Documentation]    Connect Client with User1 Credentials
    [Tags]             production    TC-6759_Step2      upgrade-test

    ${LOGIN_STATUS}=                  Login User              ${tenant_username}     ${tenant_password}
    should be equal as strings       '${LOGIN_STATUS}'        '1'

    ${DELTA_UPDATE}=                  Update Network Policy To Ap    policy_name=${PPSK_UPGRADE_TEST_NW}    ap_serial=${ap1.serial}
    should be equal as strings       '${DELTA_UPDATE}'   '1'
    sleep                             ${config_push_wait}

    ${URL_TITLE}=                    Check Internet Connectivity    ${mu1.ip}
    should not be equal as strings   '${URL_TITLE}'               '${PAGE_TITLE}'

    Connect Ppsk Wireless Network    ${PPSK_UPGRADE_TEST_SSID}     ${pass1}

    sleep                           ${client_connect_wait}

    WI-FI INTERFACE IP ADDRESS CHECK

    ${URL_TITLE}=                   Check Internet Connectivity     ${mu1.ip}
    Run keyword if  "${URL_TITLE}" != "${PAGE_TITLE}"  Re Connect To PPSK Network  ${PPSK_UPGRADE_TEST_SSID}    ${pass1}

    [Teardown]    run keywords    Test Case Level Cleanup
    ...           AND             mu1.delete_wlan_profile   ${PPSK_UPGRADE_TEST_SSID}

TC-6759_Step3: Connect Client with User2 Credentials
    [Documentation]    Connect Client with User2 Credentials
    [Tags]             production    TC-6759_Step3      upgrade-test

    ${LOGIN_STATUS}=                  Login User              ${tenant_username}     ${tenant_password}
    should be equal as strings       '${LOGIN_STATUS}'        '1'

    ${URL_TITLE}=                    Check Internet Connectivity    ${mu1.ip}
    should not be equal as strings   '${URL_TITLE}'               '${PAGE_TITLE}'

    Connect Ppsk Wireless Network    ${PPSK_UPGRADE_TEST_SSID}     ${pass2}

    sleep                           ${client_connect_wait}

    WI-FI INTERFACE IP ADDRESS CHECK

    ${URL_TITLE}=                   Check Internet Connectivity     ${mu1.ip}
    Run keyword if  "${URL_TITLE}" != "${PAGE_TITLE}"  Re Connect To PPSK Network  ${PPSK_UPGRADE_TEST_SSID}  ${pass2}

    [Teardown]    run keywords    Test Case Level Cleanup
    ...           AND             mu1.delete_wlan_profile   ${PPSK_UPGRADE_TEST_SSID}

TC-6759_Step4: Connect Client with User3 Credentials
    [Documentation]    Connect Client with User3 Credentials
    [Tags]             production    TC-6759_Step4      upgrade-test

    ${LOGIN_STATUS}=                  Login User              ${tenant_username}     ${tenant_password}
    should be equal as strings       '${LOGIN_STATUS}'        '1'

    ${URL_TITLE}=                    Check Internet Connectivity    ${mu1.ip}
    should not be equal as strings   '${URL_TITLE}'               '${PAGE_TITLE}'

    Connect Ppsk Wireless Network    ${PPSK_UPGRADE_TEST_SSID}     ${pass3}

    WI-FI INTERFACE IP ADDRESS CHECK

    ${URL_TITLE}=                   Check Internet Connectivity     ${mu1.ip}
    Run keyword if  "${URL_TITLE}" != "${PAGE_TITLE}"  Re Connect To PPSK Network  ${PPSK_UPGRADE_TEST_SSID}  ${pass3}

    [Teardown]    run keywords    Test Case Level Cleanup
    ...           AND             mu1.delete_wlan_profile   ${PPSK_UPGRADE_TEST_SSID}

TC-6759_Step5: Connect Client with User4 Credentials
    [Documentation]    Connect Client with User4 Credentials
    [Tags]             production   TC-6759_Step5       upgrade-test

    ${LOGIN_STATUS}=                  Login User              ${tenant_username}     ${tenant_password}
    should be equal as strings       '${LOGIN_STATUS}'        '1'

    ${URL_TITLE}=                    Check Internet Connectivity    ${mu1.ip}
    should not be equal as strings   '${URL_TITLE}'               '${PAGE_TITLE}'

    Connect Ppsk Wireless Network    ${PPSK_UPGRADE_TEST_SSID}     ${pass4}

    sleep                           ${client_connect_wait}

    WI-FI INTERFACE IP ADDRESS CHECK

    ${URL_TITLE}=                   Check Internet Connectivity     ${mu1.ip}
    Run keyword if  "${URL_TITLE}" != "${PAGE_TITLE}"  Re Connect To PPSK Network  ${PPSK_UPGRADE_TEST_SSID}  ${pass4}

    [Teardown]    run keywords    Test Case Level Cleanup
    ...           AND             mu1.delete_wlan_profile   ${PPSK_UPGRADE_TEST_SSID}

TC-6759_Step6: Deleting User User3 and Trying to connect Client with User3 Credentials
    [Documentation]    Deleting User User3 and Trying to connect Client with User3 Credentials
    [Tags]             production  TC-6759_Step6      upgrade-test

    ${LOGIN_STATUS}=                  Login User              ${tenant_username}     ${tenant_password}
    should be equal as strings       '${LOGIN_STATUS}'        '1'

    ${USER_DELETE}=                   delete single user       ${user3}
    should be equal as strings        '${USER_DELETE}'   '1'

    ${DELTA_UPDATE}=                  Update Network Policy To Ap    policy_name=${PPSK_UPGRADE_TEST_NW}    ap_serial=${ap1.serial}
    should be equal as strings       '${DELTA_UPDATE}'   '1'
    sleep                             ${config_push_wait}

    ${URL_TITLE}=                    Check Internet Connectivity    ${mu1.ip}
    should not be equal as strings   '${URL_TITLE}'               '${PAGE_TITLE}'

    ${CONNECT_STATUS}=               mu1.connect_wpa2_ppsk_network    ${PPSK_UPGRADE_TEST_SSID}    ${pass3}
    should be equal as strings       '${CONNECT_STATUS}'    '-1'

    sleep                             ${config_push_wait}

    ${URL_TITLE}=                    Check Internet Connectivity    ${mu1.ip}
    should not be equal as strings   '${URL_TITLE}'               '${PAGE_TITLE}'


    [Teardown]    run keywords    Test Case Level Cleanup
    ...           AND             mu1.delete_wlan_profile   ${PPSK_UPGRADE_TEST_SSID}

TC-6759_Step7: Change Password for User4 and Connect Client with new Credentials
    [Documentation]    Change Password for User4 and Connect Client with new Credentials
    [Tags]             production   TC-6759_Step7    upgrade-test

    ${LOGIN_STATUS}=                  Login User              ${tenant_username}     ${tenant_password}
    should be equal as strings       '${LOGIN_STATUS}'        '1'

    ${USER_PASSWORD_CHANGED}=         edit single user password       ${user4}          ${pass4_changed}
    should be equal as strings       '${USER_PASSWORD_CHANGED}'   '1'

    ${DELTA_UPDATE}=                  Update Network Policy To Ap    policy_name=${PPSK_UPGRADE_TEST_NW}    ap_serial=${ap1.serial}
    should be equal as strings       '${DELTA_UPDATE}'   '1'
    sleep                             ${config_push_wait}

    ${URL_TITLE}=                       Check Internet Connectivity    ${mu1.ip}
    should not be equal as strings      '${URL_TITLE}'               '${PAGE_TITLE}'

    Connect Ppsk Wireless Network    ${PPSK_UPGRADE_TEST_SSID}     ${pass4_changed}

    sleep                           ${client_connect_wait}

    WI-FI INTERFACE IP ADDRESS CHECK

    ${URL_TITLE}=                   Check Internet Connectivity     ${mu1.ip}
    log to console                  ${URL_TITLE}
    Run keyword if  "${URL_TITLE}" != "${PAGE_TITLE}"  Re Connect To PPSK Network  ${PPSK_UPGRADE_TEST_SSID}  ${pass4_changed}

    [Teardown]    run keywords    Test Case Level Cleanup
    ...           AND             mu1.delete_wlan_profile   ${PPSK_UPGRADE_TEST_SSID}

TC-6759_Step8: Revert Changes for User3 and User4
    [Documentation]    Revert Changes for User3 and User4
    [Tags]             production    upgrade-test   TC-6759_Step8

    ${LOGIN_STATUS}=                  Login User              ${tenant_username}     ${tenant_password}
    should be equal as strings       '${LOGIN_STATUS}'        '1'

    ${USER_PASSWORD_CHANGED}=         edit single user password       ${user4}          ${pass4}
    should be equal as strings       '${USER_PASSWORD_CHANGED}'   '1'

    ${USER3_ADD}                      create add user to user group    ${MULTIPLE_CLOUD_USER_GROUP}        user_config=&{single_user3_info}
    should be equal as strings       '${USER3_ADD}'   '1'

    ${DELTA_UPDATE}=                  Update Network Policy To Ap    policy_name=${PPSK_UPGRADE_TEST_NW}    ap_serial=${ap1.serial}
    should be equal as strings       '${DELTA_UPDATE}'   '1'

    sleep                             ${config_push_wait}

    [Teardown]   run keywords      logout user
    ...                            quit browser

TC-6759_Step9: Connect Client with User3 Credentials
    [Documentation]    Connect Client with User3 Credentials
    [Tags]             production    TC-6759_Step9      upgrade-test

    ${LOGIN_STATUS}=                  Login User              ${tenant_username}     ${tenant_password}
    should be equal as strings       '${LOGIN_STATUS}'        '1'

    ${URL_TITLE}=                    Check Internet Connectivity    ${mu1.ip}
    should not be equal as strings   '${URL_TITLE}'               '${PAGE_TITLE}'

    Connect Ppsk Wireless Network    ${PPSK_UPGRADE_TEST_SSID}     ${pass3}

    WI-FI INTERFACE IP ADDRESS CHECK

    ${URL_TITLE}=                   Check Internet Connectivity     ${mu1.ip}
    Run keyword if  "${URL_TITLE}" != "${PAGE_TITLE}"  Re Connect To PPSK Network  ${PPSK_UPGRADE_TEST_SSID}  ${pass3}

    [Teardown]    run keywords    Test Case Level Cleanup
    ...           AND             mu1.delete_wlan_profile   ${PPSK_UPGRADE_TEST_SSID}

TC-6759_Step10: Connect Client with User4 Credentials
    [Documentation]    Connect Client with User4 Credentials
    [Tags]             production   TC-6759_Step10       upgrade-test

    ${LOGIN_STATUS}=                  Login User              ${tenant_username}     ${tenant_password}
    should be equal as strings       '${LOGIN_STATUS}'        '1'

    ${URL_TITLE}=                    Check Internet Connectivity    ${mu1.ip}
    should not be equal as strings   '${URL_TITLE}'               '${PAGE_TITLE}'

    Connect Ppsk Wireless Network    ${PPSK_UPGRADE_TEST_SSID}     ${pass4}

    sleep                           ${client_connect_wait}

    WI-FI INTERFACE IP ADDRESS CHECK

    ${URL_TITLE}=                   Check Internet Connectivity     ${mu1.ip}
    Run keyword if  "${URL_TITLE}" != "${PAGE_TITLE}"  Re Connect To PPSK Network  ${PPSK_UPGRADE_TEST_SSID}  ${pass4}

    [Teardown]    run keywords    Test Case Level Cleanup
    ...           AND             mu1.delete_wlan_profile   ${PPSK_UPGRADE_TEST_SSID}

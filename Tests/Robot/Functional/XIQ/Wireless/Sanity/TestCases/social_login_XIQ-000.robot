# Author        : Ramkumar
# Date          : April 03th 2020
# Description   : Captive Web Portal with Social Login Credentials
#
# Topology:
# ---------
# Windows10 Client------AreoHive AP ----- XIQ QA1R2 Instance
#
# Preconfig:
# ----------
# Pre-Condtion
# 1. AP should be onboarded and it is online
# 2. Script Will not run on Local Aerohive Instance.Run only on qa1r2 instance
# 3. Social Login credentials created for this script is cloud1tenant1@gmail.com and Symbol@123
# 4.Should Use Windows10 as Wireless client
# 5. Update ${mu1.ip} ${mu1.port} and ${mu1.wifi_mac} Variable on Topology File
# 6. start the remote server in MU. Starting remote server on MU refer testsuite/xiq/config/remote_server_config.txt
# 7. Start the stand alone selenium server on MU refer:testsuite/xiq/config/remote_server_config.txt
#
# Execution Command:
# ------------------
# robot  -v AIO_IP:$AIO_IP -v DEVICE:AP630 -v TOPO:qa1_r2 social_login.robot
*** Variables ***
${cmd_clear_client_mac}          clear auth station mac ${mu1.wifi_mac}
${cmd_show_station}              show station
${SOCIAL_WRONG_PASSWORD}         Symbol@12345
${INTERNET_PAGE_TITLE}           CNN International - Breaking News, US News, World News and Video
${PAGE_TITLE}                    End-to-End Cloud Driven Networking Solutions - Extreme Networks
${AUTH_STATUS_ACCEPT}            auth-logs-accept
${AUTH_TYPE_FACEBOOK}            facebook
${AUTH_TYPE_GOOGLE}              google
${AUTH_TYPE_LINKEDIN}            linkedin

*** Settings ***
Library     Collections
Library     common/Utils.py
Library     common/Cli.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/WirelessNetworks.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/manage/Client.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     xiq/flows/common/MuCaptivePortal.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
# 2022-08-31 Move variables to resources file, so they can be randomized for unique execution
Variables    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/social_login_config.py

Resource     Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/test_email_ids.robot

Library	        Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   Remote_Server

Force Tags   testbed_1_node

Suite Setup     Pre Condition
Suite Teardown  Test Suite Clean Up

*** Keywords ***
Pre Condition
    [Documentation]   AP Should be onboarded  and it is online
    ${LOGIN_STATUS}=              Login User          ${tenant_username}      ${tenant_password}    check_warning_msg=True
    should be equal as integers             ${LOGIN_STATUS}               1

    ${DEVICE_STATUS}=       Get Device Status       device_serial=${ap1.serial}
    Should contain any  ${DEVICE_STATUS}    green     config audit mismatch

    ${CREATE_NW_POLICY_STATUS}=     Create Network Policy          ${NW_DEFAULT_POLICY}                 &{CONFIG_PUSH_OPEN_NW_01}
    should be equal as integers     ${CREATE_NW_POLICY_STATUS}               1

    ${UPDATE_NW_POLICY_STATUS}=     Update Network Policy To Ap If Needed   policy_name=${NW_DEFAULT_POLICY}   ap_serial=${ap1.serial}
    should be equal as integers     ${UPDATE_NW_POLICY_STATUS}               1

    ${DELETE_STATUS}=               delete network policy          ${NW_POLICY_NAME1}
    should be equal as integers     ${DELETE_STATUS}               1

    ${SSID_DLT_STATUS}=             Delete ssid                    ${NW_POLICY_SSID1}
    should be equal as integers     ${SSID_DLT_STATUS}             1

    ${DELETE_CWP_STATUS}=           Delete Captive Web Portals     ${CWP_NAME_FACEBOOK}
    should be equal as integers     ${UPDATE_NW_POLICY_STATUS}               1

    Remote_Server.Disconnect WiFi
    # 2022-08-31 new browser library removes need to logout and back in to keep variables in scope. Trial.  Remove if no issues are seen
    #[Teardown]   run keywords       logout user
    #...                             quit browser

Test Suite Clean Up
    [Documentation]    delete created network policies, captive web portals,ssid

    [Tags]      production      cleanup
    # 2022-08-31 new browser library removes need to logout and back in to keep variables in scope. Trial.  Remove if no issues are seen
    #${result}=    Login User       ${tenant_username}     ${tenant_password}
    Update Network Policy To AP    policy_name=${NW_DEFAULT_POLICY}    ap_serial=${ap1.serial}
    Delete Network Polices         ${NW_POLICY_NAME1}
    Delete ssids                   ${NW_POLICY_SSID1}
    Delete Captive Web Portals     ${CWP_NAME_FACEBOOK}
    Logout User
    Quit Browser

Positive Internet connectivity check
    ${FLAG}=   Remote_Server.Connectivity Check
    should be equal as strings   '${FLAG}'   '1'


Negative Internet connectivity check
    ${FLAG}=   Remote_Server.Connectivity Check
    should be equal as strings   '${FLAG}'   '-1'

Test Case Level Cleanup
    ${UPDATE_NW_POLICY_STATUS}=     Update Network Policy To Ap    policy_name=${NW_DEFAULT_POLICY}     ap_serial=${ap1.serial}
    should be equal as integers     ${UPDATE_NW_POLICY_STATUS}               1

    ${DELETE_STATUS}=               Delete Network Policy           ${NW_POLICY_NAME1}
    should be equal as integers     ${DELETE_STATUS}                1

    ${SSID_DLT_STATUS}=             Delete ssid                     ${NW_POLICY_SSID1}
    should be equal as integers     ${SSID_DLT_STATUS}              1

    ${DELETE_CWP_STATUS}=           Delete Captive Web Portals      ${CWP_NAME_FACEBOOK}
    should be equal as integers     ${UPDATE_NW_POLICY_STATUS}      1
    # 2022-08-31 new browser library removes need to logout and back in to keep variables in scope. Trial.  Remove if no issues are seen
    #[Teardown]   run keywords       logout user
    #...                             quit browser
    Remote_Server.Disconnect WiFi

*** Test Cases ***
TCCS-11614: Social login with facebook
    [Documentation]   CWP Social login with facebook
    ...               https://jira.aerohive.com/browse/APC-36506

    [Tags]            production    tccs_11614

    # 2022-08-31 new browser library removes need to logout and back in to keep variables in scope. Trial.  Remove if no issues are seen
    #${LOGIN_STATUS}=                        Login User          ${tenant_username}      ${tenant_password}
    #should be equal as integers             ${LOGIN_STATUS}               1

    ${CREATE_NW_POLICY_STATUS}=             Create Network Policy     ${NW_POLICY_NAME1}    &{OPEN_NW_1}
    should be equal as integers             ${CREATE_NW_POLICY_STATUS}               1

    ${UPDATE_NW_POLICY_STATUS}=             Update Network Policy To AP   ${NW_POLICY_NAME1}     ap_serial=${ap1.serial}
    should be equal as integers             ${UPDATE_NW_POLICY_STATUS}               1

    #Log to Console                  wait_until_device_update_done
    #wait_until_device_update_done   device_serial=${ap1.serial}
    # update shows green at end of update policy to ap.  Though still takes some tome to bcast and client to see ssid.
    sleep                                   30

    Remote_Server.Connect Open Network    ${NW_POLICY_SSID1}

    Log to Console     Sleep for ${client_connect_wait}
    sleep              ${client_connect_wait}

    run keyword if     "${mu1.platform}" == "mac"       Remote_Server.Kill Native Captive
    IF                 "${mu1.platform}" == "mac"
                       open cp browser    ${mu1.ip}     incognito=True
    ELSE
                       open cp browser    ${mu1.ip}
    END

    Log to Console     Sleep for ${cp_page_open_wait}
    sleep              ${cp_page_open_wait}

    ${SOCIAL_AUTH_STATUS}=            Validate CWP Social Login With Facebook   ${MAIL_ID3}   ${MAIL_ID3_PASS}
    Should Be Equal As Strings        '${SOCIAL_AUTH_STATUS}'  '1'

    ${CURRENT_DATE_TIME}=                   Get Current Date Time

    Log to Console      Sleep for ${auth_logs_duration_wait}
    sleep               ${auth_logs_duration_wait}

    ${AUTH_LOGS}=                Get Authentication Logs Details       ${CURRENT_DATE_TIME}     ${MAIL_ID3}
    ${TIME_STAMP}=               Get From Dictionary     ${AUTH_LOGS}    authdate
    should contain               ${TIME_STAMP}       ${CURRENT_DATE_TIME[:-2:]}
    LOG TO CONSOLE               ${AUTH_LOGS}

    # Logs Verification
    ${AUTH_STATUS}=                 Get From Dictionary     ${AUTH_LOGS}    reply
    Should Be Equal As Strings      '${AUTH_STATUS}'     '${AUTH_STATUS_ACCEPT}'

    ${USER_NAME}=                   Get From Dictionary     ${AUTH_LOGS}    userName
    Should Be Equal As Strings      '${USER_NAME}'       '${MAIL_ID3}'

    ${SSID}=                        Get From Dictionary     ${AUTH_LOGS}    ssid
    Should Be Equal As Strings      '${SSID}'            '${NW_POLICY_SSID1}'

    ${AUTH_TYPE}=                   Get From Dictionary     ${AUTH_LOGS}    authType
    Should Be Equal As Strings      '${AUTH_TYPE}'       '${AUTH_TYPE_FACEBOOK}'

    ${CLIENT_MAC}=                  Get From Dictionary     ${AUTH_LOGS}    callingStationId
    Should Be Equal As Strings      '${CLIENT_MAC}'      '${mu1.wifi_mac}'

    ${REJ_CODE}=                    Get From Dictionary     ${AUTH_LOGS}    rejectReason
    Should Be Equal As Strings      '${REJ_CODE}'        ''

    ${TIME_STAMP}=                  Get From Dictionary     ${AUTH_LOGS}    authdate
    should contain                 ${TIME_STAMP}        ${CURRENT_DATE_TIME}

    Remote_Server.Disconnect WiFi
    Log to Console      Sleep for ${client_disconnect_wait}
    sleep  ${client_disconnect_wait}


    ${AP_SPAWN}=        Open Spawn          ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    Should Not Be Equal As Strings      '${AP_SPAWN}'        '-1'
    
    ${CLEAR_CLIENT}=        Send            ${AP_SPAWN}         ${cmd_clear_client_mac}
    Log to Console      Sleep for ${ap_clear_mac_wait}
    sleep  ${ap_clear_mac_wait}

    ${SHOW_STATION}=        Send            ${AP_SPAWN}         ${cmd_show_station}
    Close Spawn  ${AP_SPAWN}

    Should Not Contain              ${SHOW_STATION}          ${mu1.wifi_mac}

    [Teardown]   run keywords    Test Case Level Cleanup
    ...                          Close CP Browser

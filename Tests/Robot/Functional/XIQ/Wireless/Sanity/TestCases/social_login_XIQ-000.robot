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
${NW_POLICY_NAME1}               automation_policy_fb
${NW_POLICY_NAME2}               automation_policy_google
${NW_POLICY_NAME3}               automation_policy_linkedin
${NW_POLICY_NAME4}               automation_social_policy
${NW_POLICY_SSID1}               automation_policy_fb
${NW_POLICY_SSID2}               automation_policy_google
${NW_POLICY_SSID3}               automation_policy_linkedin
${NW_POLICY_SSID4}               test_social_login4
${NP_AUTHLOG_SSID}               social_login_authlogs
${CWP_NAME_FACEBOOK}             cloudcwpsocialfacebook
${CWP_NAME_GOOGLE}               cloudcwpsocialgoogle
${CWP_NAME_LINKEDIN}             cloudcwpsociallinkedin
${CWP_NAME_FACEBOOK1}            cloudcwpsocialfacebook4
${INTERNET_PAGE_TITLE}           CNN International - Breaking News, US News, World News and Video
${NW_POLICY_NAME5}               social_restrict_access
${NW_POLICY_SSID5}               social_restrict_access
${NW_POLICY_NAME6}               cache_duration_max_limit
${NW_POLICY_SSID6}               cache_duration_max_limit
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

Resource     Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/social_login_config.robot
Resource     Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/test_email_ids.robot

Library	        Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   Remote_Server

Force Tags   testbed_1_node

Suite Setup     Pre Condition
Suite Teardown  Test Suite Clean Up

*** Keywords ***
Pre Condition
    [Documentation]   AP Should be onboarded  and it is online
    ${result}=          Login User          ${tenant_username}     ${tenant_password}
    ${AP_STATUS}=       Get AP Status       ap_mac=${ap1.mac}
    Should Be Equal As Strings  '${AP_STATUS}'     'green'
    create network policy    default_network_policy     &{CONFIG_PUSH_OPEN_NW_01}
    Update Network Policy To AP    policy_name=default_network_policy    ap_serial=${ap1.serial}
    Delete Network Polices         ${NW_POLICY_NAME1}    ${NW_POLICY_NAME2}    ${NW_POLICY_NAME3}     ${NW_POLICY_NAME4}  ${NW_POLICY_NAME5}  ${NW_POLICY_NAME6}
    Delete ssids                   ${NW_POLICY_SSID1}    ${NW_POLICY_SSID2}     ${NW_POLICY_SSID4}    ${NW_POLICY_SSID3}   ${NP_AUTHLOG_SSID}   ${NW_POLICY_SSID5}
    Delete Captive Web Portals     ${CWP_NAME_FACEBOOK}  ${CWP_NAME_GOOGLE}   ${CWP_NAME_LINKEDIN}   ${CWP_NAME_FACEBOOK1}
    [Teardown]   run keywords       logout user
    ...                             quit browser

Test Suite Clean Up
    [Documentation]    delete created network policies, captive web portals,ssid

    [Tags]      production      cleanup
    ${result}=    Login User       ${tenant_username}     ${tenant_password}
    Update Network Policy To AP    policy_name=default_network_policy    ap_serial=${ap1.serial}
    Delete Network Polices         ${NW_POLICY_NAME1}    ${NW_POLICY_NAME2}    ${NW_POLICY_NAME3}     ${NW_POLICY_NAME4}  ${NW_POLICY_NAME5}   ${NW_POLICY_NAME6}
    Delete ssids                   ${NW_POLICY_SSID1}    ${NW_POLICY_SSID2}     ${NW_POLICY_SSID4}    ${NW_POLICY_SSID3}   ${NP_AUTHLOG_SSID}  ${NW_POLICY_SSID5}
    Delete Captive Web Portals     ${CWP_NAME_FACEBOOK}  ${CWP_NAME_GOOGLE}   ${CWP_NAME_LINKEDIN}   ${CWP_NAME_FACEBOOK1}
    Logout User
    Quit Browser

Positive Internet connectivity check
    ${FLAG}=   Remote_Server.Connectivity Check
    should be equal as strings   '${FLAG}'   '1'


Negative Internet connectivity check
    ${FLAG}=   Remote_Server.Connectivity Check
    should be equal as strings   '${FLAG}'   '-1'

Test Case Level Cleanup
     Update Network Policy To AP    policy_name=default_network_policy    ap_serial=${ap1.serial}
     Delete Network Polices         ${NW_POLICY_NAME1}    ${NW_POLICY_NAME2}    ${NW_POLICY_NAME3}     ${NW_POLICY_NAME4}  ${NW_POLICY_NAME5}  ${NW_POLICY_NAME6}
     Delete ssids                   ${NW_POLICY_SSID1}    ${NW_POLICY_SSID2}     ${NW_POLICY_SSID4}    ${NW_POLICY_SSID3}   ${NP_AUTHLOG_SSID}   ${NW_POLICY_SSID5}
     Delete Captive Web Portals     ${CWP_NAME_FACEBOOK}  ${CWP_NAME_GOOGLE}   ${CWP_NAME_LINKEDIN}   ${CWP_NAME_FACEBOOK1}
    [Teardown]   run keywords       logout user
    ...                             quit browser
     Remote_Server.Disconnect WiFi

*** Test Cases ***
TCCS-11614: Social login with facebook
    [Documentation]   CWP Social login with facebook
    ...               https://jira.aerohive.com/browse/APC-36506

    [Tags]            production    tccs_11614

    ${LOGIN_XIQ}=                     Login User          ${tenant_username}      ${tenant_password}    capture_version=True
    ${NW_POLICY_CREATION}=            Create Network Policy     ${NW_POLICY_NAME1}    &{OPEN_NW_1}
    ${AP_UPDATE_CONFIG}=              Update Network Policy To AP   ${NW_POLICY_NAME1}     ap_serial=${ap1.serial}
    Log to Console      Sleep for ${config_push_wait}
    sleep                         ${config_push_wait}

    Remote_Server.Connect Open Network    ${NW_POLICY_SSID1}
    Log to Console      Sleep for ${client_connect_wait}
    sleep                         ${client_connect_wait}
    open cp browser    ${mu1.ip}
    Log to Console      Sleep for ${cp_page_open_wait}
    sleep  ${cp_page_open_wait}

    ${SOCIAL_AUTH_STATUS}=                  Validate CWP Social Login With Facebook     ${MAIL_ID3}      ${MAIL_ID3_PASS}
    ${CURRENT_DATE_TIME}=                   Get Current Date Time

    Log to Console      Sleep for ${auth_logs_duration_wait}
    sleep  ${auth_logs_duration_wait}

    ${AUTH_LOGS}=                Get Authentication Logs Details       ${CURRENT_DATE_TIME}     ${MAIL_ID3}
    ${TIME_STAMP}=               Get From Dictionary     ${AUTH_LOGS}    authdate
    should contain               ${TIME_STAMP}       ${CURRENT_DATE_TIME[:-2:]}
    LOG TO CONSOLE               ${AUTH_LOGS}
    # Logs Verification
    ${AUTH_STATUS}=        Get From Dictionary     ${AUTH_LOGS}    reply
    ${USER_NAME}=          Get From Dictionary     ${AUTH_LOGS}    userName
    ${SSID}=               Get From Dictionary     ${AUTH_LOGS}    ssid
    ${AUTH_TYPE}=          Get From Dictionary     ${AUTH_LOGS}    authType
    ${CLIENT_MAC}=         Get From Dictionary     ${AUTH_LOGS}    callingStationId
    ${REJ_CODE}=           Get From Dictionary     ${AUTH_LOGS}    rejectReason
    ${TIME_STAMP}=         Get From Dictionary     ${AUTH_LOGS}    authdate
    Remote_Server.Disconnect WiFi
    Log to Console      Sleep for ${client_disconnect_wait}
    sleep  ${client_disconnect_wait}

    ${AP_SPAWN}=        Open Spawn          ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    ${CLEAR_CLIENT}=        Send            ${AP_SPAWN}         ${cmd_clear_client_mac}
    Log to Console      Sleep for ${ap_clear_mac_wait}
    sleep  ${ap_clear_mac_wait}
    ${SHOW_STATION}=        Send            ${AP_SPAWN}         ${cmd_show_station}
    Close Spawn  ${AP_SPAWN}

    Should Be Equal As Strings     '${LOGIN_XIQ}'           '1'
    Should Be Equal As Strings     '${NW_POLICY_CREATION}'  '1'
    Should Be Equal As Strings     '${AP_UPDATE_CONFIG}'    '1'
    Should Be Equal As Strings     '${SOCIAL_AUTH_STATUS}'  '1'
    Should Not Contain              ${SHOW_STATION}          ${mu1.wifi_mac}

    Should Be Equal As Strings    '${AUTH_STATUS}'     '${AUTH_STATUS_ACCEPT}'
    Should Be Equal As Strings    '${USER_NAME}'       '${MAIL_ID3}'
    Should Be Equal As Strings    '${SSID}'            '${NW_POLICY_SSID1}'
    Should Be Equal As Strings    '${AUTH_TYPE}'       '${AUTH_TYPE_FACEBOOK}'
    Should Be Equal As Strings    '${CLIENT_MAC}'      '${mu1.wifi_mac}'
    Should Be Equal As Strings    '${REJ_CODE}'        ''
    should contain                 ${TIME_STAMP}        ${CURRENT_DATE_TIME}

    [Teardown]   run keywords    Test Case Level Cleanup
    ...                          Close CP Browser

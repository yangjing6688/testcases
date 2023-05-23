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
${cmd_clear_client_mac}         clear auth station mac ${mu1.wifi_mac}
${cmd_show_station}             show station
${SOCIAL_WRONG_PASSWORD}        Symbol@12345
${INTERNET_PAGE_TITLE}          CNN International - Breaking News, US News, World News and Video
${PAGE_TITLE}                   End-to-End Cloud Driven Networking Solutions - Extreme Networks
${AUTH_STATUS_ACCEPT}           auth-logs-accept
${AUTH_TYPE_FACEBOOK}           facebook
${AUTH_TYPE_GOOGLE}             google
${AUTH_TYPE_LINKEDIN}           linkedin
${LOCATION}                     auto_location_01, Santa Clara, building_02, floor_04
${CWP_MAIL_ID}                  mail.sociallogin.cwp@gmail.com
${CWP_MAIL_PASSWORD}            Extreme@123
${FLOOR}                        floor_04
${LOCATION_DISPLAY}             auto_location_01 >> Santa Clara >> building_02 >> floor_04
${TIME_STAMP_FLAG1}              False
${TIME_STAMP_FLAG2}              False

*** Settings ***
Library     Collections
Library     extauto/common/Cli.py
Library     extauto/common/Utils.py
Library     extauto/common/Screen.py
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     extauto/xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     extauto/xiq/flows/common/MuCaptivePortal.py
Library     extauto/xiq/flows/configure/CommonObjects.py
Library     extauto/xiq/flows/configure/ExpressNetworkPolicies.py
Library     extauto/xiq/flows/configure/NetworkPolicy.py
Library     extauto/xiq/flows/configure/WirelessNetworks.py
Library     extauto/xiq/flows/globalsettings/GlobalSetting.py
Library     extauto/xiq/flows/mlinsights/Network360Plan.py
Library     extauto/xiq/flows/mlinsights/Network360Monitor.py
Library     extauto/xiq/flows/manage/Client.py
Library     extauto/xiq/flows/manage/Devices.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py
Library     ExtremeAutomation/Keywords/UserDefinedKeywords/NetworkElements/SetupTeardown/SetupTeardownUdks.py

Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}
Variables   Environments/${ENV}
Variables   Environments/Config/waits.yaml
Variables   Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/social_login_config.py

Library	    Remote  http://${mu1.ip}:${mu1.port}    WITH NAME   Remote_Server

Force Tags  testbed_1_node

Suite Setup         Suite Setup
Suite Teardown      Run Keyword And Warn On Failure     Suite Teardown

*** Keywords ***
Suite Setup
    [Documentation]     Cleanup before running the suite
    [Tags]      production  cleanup

    Log To Console      DOING CLEANUP BEFORE RUNNING THE SUITE!

    # Use this method to convert the ap, wing, netelem to a generic device object
    # ap1      => device1
    # wing1    => device1
    # netelem1 => device1 (EXOS/VOSS)
    Convert To Generic Device Object    device      index=1     look_for_device_type=ap     set_to_index=1

    # Create the connection to the device
    Base Test Suite Setup
    Set Global Variable     ${MAIN_DEVICE_SPAWN}            ${device1.name}

    ${LOGIN_RESULT}=            Login User                  ${tenant_username}      ${tenant_password}      check_warning_msg=True
    Should Be Equal As Integers     ${LOGIN_RESULT}         1

    ${SEARCH_RESULT}=           Search Device               device_serial=${device1.serial}     ignore_failure=True
    IF  ${SEARCH_RESULT} == 1
        ${DISCONNECT_DEVICE_RESULT}=    Disconnect Device From Cloud        ${device1.cli_type}      ${MAIN_DEVICE_SPAWN}
        Should Be Equal As Integers     ${DISCONNECT_DEVICE_RESULT}         1

        ${DELETE_DEVICE_RESULT}=        Delete Device                       device_serial=${device1.serial}
        Should Be Equal As Integers     ${DELETE_DEVICE_RESULT}             1
    END

    ${CONF_RESULT}=         Configure Device To Connect To Cloud            ${device1.cli_type}     ${generic_capwap_url}   ${MAIN_DEVICE_SPAWN}
    Should Be Equal As Integers     ${CONF_RESULT}          1

    ${ONBOARD_RESULT}=      Onboard Device Quick        ${device1}
    Should Be Equal As Strings      ${ONBOARD_RESULT}       1

    ${WAIT_CONF_RESULT}=    Wait For Configure Device To Connect To Cloud   ${device1.cli_type}     ${generic_capwap_url}   ${MAIN_DEVICE_SPAWN}
    Should Be Equal As Integers     ${WAIT_CONF_RESULT}     1

    ${ONLINE_STATUS}=       Wait Until Device Online    ${device1.serial}
    Should Be Equal As Integers     ${ONLINE_STATUS}        1

    ${MANAGED_STATUS}=      Wait Until Device Managed   ${device1.serial}
    Should Be Equal As Integers     ${MANAGED_STATUS}       1

    ${DEVICE_STATUS}=       Get Device Status           device_mac=${device1.mac}
    Should Contain Any              ${DEVICE_STATUS}    green   config audit mismatch

    # Upgrade the device to latest/supported version to avoid config push issues.
    ${LATEST_VERSION}=              Upgrade Device                  ${device1}
    Should Not be Empty             ${LATEST_VERSION}

    ${REBOOT_STATUS}=               Wait Until Device Reboots       ${device1.serial}       retry_count=15
    Should Be Equal as Integers     ${REBOOT_STATUS}                    1

    ${CONNECTED_STATUS}=            Wait Until Device Online        ${device1.serial}
    Should Be Equal as Integers     ${CONNECTED_STATUS}                 1

    ${DELETE_CUS_POLICY_RESULT}=    Delete Network Polices          ${NW_POLICY_NAME1}      ${NW_DEFAULT_POLICY}    ${NW_POLICY_NAME3}
    Should Be Equal As Integers     ${DELETE_CUS_POLICY_RESULT}         1

    ${DELETE_SSID_RESULT}=          Delete SSIDs                    ${NW_POLICY_SSID1}      ${NW_DEFAULT_SSID}      ${NW_POLICY_SSID3}
    Should Be Equal As Integers     ${DELETE_SSID_RESULT}               1

    ${DELETE_CWP_RESULT}=           Delete Captive Web Portals      ${CWP_NAME_FACEBOOK}    ${CWP_NAME_LINKEDIN}
    Should Be Equal As Integers     ${DELETE_CWP_RESULT}                1

    Remote_Server.Disconnect WiFi

Suite Teardown
    [Documentation]     Cleanup after running the suite
    [Tags]      production  cleanup

    Log To Console      DOING CLEANUP AFTER RUNNING THE SUITE!

    ${SEARCH_RESULT}=   Search Device               device_serial=${device1.serial}     ignore_failure=True
    IF  ${SEARCH_RESULT} == 1
        ${DISCONNECT_DEVICE_RESULT}=    Disconnect Device From Cloud        ${device1.cli_type}     ${MAIN_DEVICE_SPAWN}
        Should Be Equal As Integers     ${DISCONNECT_DEVICE_RESULT}         1

        ${DELETE_DEVICE_RESULT}=        Delete Device                       device_serial=${device1.serial}
        Should Be Equal As Integers     ${DELETE_DEVICE_RESULT}             1
    END

    ${DELETE_CUS_POLICY_RESULT}=    Delete Network Polices               ${NW_POLICY_NAME1}     ${NW_DEFAULT_POLICY}    ${NW_POLICY_NAME3}
    Should Be Equal As Integers     ${DELETE_CUS_POLICY_RESULT}         1

    ${DELETE_SSID_RESULT}=          Delete SSIDs                        ${NW_POLICY_SSID1}  ${NW_DEFAULT_SSID}  ${NW_POLICY_SSID3}
    Should Be Equal As Integers     ${DELETE_SSID_RESULT}               1

    ${DELETE_CWP_RESULT}=           Delete Captive Web Portals          ${CWP_NAME_FACEBOOK}    ${CWP_NAME_LINKEDIN}
    Should Be Equal As Integers     ${DELETE_CWP_RESULT}                1

    ${LOGOUT_RESULT}=               Logout User
    Should Be Equal As Integers     ${LOGOUT_RESULT}                    1

    ${QUIT_BROWSER_RESULT}=         Quit Browser
    Should Be Equal As Integers     ${QUIT_BROWSER_RESULT}              1

    Remote_Server.Disconnect WiFi

Negative Internet Connectivity Check
    ${FLAG}=    Remote_Server.Verify Internet Connectivity
    Should Be Equal As Integers     ${FLAG}     -1
    Log To Console      Internet is NOT available on the MU machine, as expected!

Positive Internet Connectivity Check
    ${FLAG}=    Remote_Server.Verify Internet Connectivity
    Should Be Equal As Integers     ${FLAG}     1
    Log To Console      Internet is available on the MU machine, as expected!

*** Test Cases ***
TCCS-14502: Verify AP Hostname in ML Insights Network 360 Monitor Tab and Client in ML Insights Client 360 Tab
    [Documentation]                 Verify AP Hostname and Client in ML Insights Monitor Tab

    [Tags]                          production      tccs_14502

    ${CREATE_POLICY_RESULT}=        Create Network Policy           ${NW_DEFAULT_POLICY}    ${CONFIG_PUSH_OPEN_NW_01}   cli_type=${device1.cli_type}
    Should Be Equal As Integers     ${CREATE_POLICY_RESULT}             1

    ${UPDATE_POLICY_RESULT}=        Update Network Policy To AP     ${NW_DEFAULT_POLICY}    ap_serial=${device1.serial}     update_method=Complete
    Should Be Equal As Integers     ${UPDATE_POLICY_RESULT}             1

    ${WAIT_UNTIL_UPDATE}=           Wait Until Device Update Done   device_serial=${device1.serial}
    Should Be Equal As Integers     ${WAIT_UNTIL_UPDATE}                1

    ${FLOOR_SEARCH}=                search_floor_in_network360Plan                  ${FLOOR}
    Save Screen shot
    Should Not Be Equal as Strings             '${FLOOR_SEARCH}'          '-1'

    ${AP_LIST}=                     get_aps_from_network360plan_floor               ${FLOOR}
    Should Contain                  ${AP_LIST}              ${device1.name}             ignore_case=True
    Save Screen shot

    ${loc_result}=                  Get Device Details      ${device1.serial}       LOCATION
    Should Contain                  ${loc_result}           ${LOCATION_DISPLAY}

    ${NP_FROM_UI}=                  Get Device Details      ${device1.serial}       POLICY
    should be equal as strings      ${NP_FROM_UI}           ${NW_DEFAULT_POLICY}

    ${CONNECT_STATUS}=              Remote_Server.Connect Open Network         ${NW_DEFAULT_SSID}
    should be equal as strings      '${CONNECT_STATUS}'    '1'

    sleep   ${client_connect_wait}

    ${FLOOR_SEARCH}=                search_floor_in_network360monitor               ${FLOOR}
    Save Screen shot
    Should Not Be Equal as Strings             '${FLOOR_SEARCH}'          '-1'

    ${AP_LIST}=                     get_devices_from_network360monitor_floor        ${FLOOR}
    Should Contain                  ${AP_LIST}              ${device1.name}
    Save Screen shot

    ${CLIENT_LIST}                  get_clients_from_network360monitor_floor        ${FLOOR}
    Save Screen shot
    Log                             ${CLIENT_LIST}
    Should Contain                  ${CLIENT_LIST}          ${mu1.wifi_mac}

    Remote_Server.Disconnect WiFi

TCCS-11614: Social login with facebook
    [Documentation]   CWP Social login with facebook
    ...               https://jira.aerohive.com/browse/APC-36506
    [Tags]            production    tccs_11614

    ${CLEAR_CLIENT}=        Send            ${MAIN_DEVICE_SPAWN}         ${cmd_clear_client_mac}
    Log to Console      Sleep for ${ap_clear_mac_wait} seconds
    Sleep  ${ap_clear_mac_wait}

    ${SHOW_STATION}=        Send            ${MAIN_DEVICE_SPAWN}         ${cmd_show_station}
    Should Not Contain      ${SHOW_STATION}     ${mu1.wifi_mac}

    ${CREATE_NW_POLICY_STATUS}=     Create Network Policy           ${NW_POLICY_NAME1}  ${OPEN_NW_1}    cli_type=${device1.cli_type}
    Should Be Equal As Integers     ${CREATE_NW_POLICY_STATUS}      1

    ${UPDATE_NW_POLICY_STATUS}=     Update Network Policy To AP     ${NW_POLICY_NAME1}  ap_serial=${device1.serial}
    Should Be Equal As Integers     ${UPDATE_NW_POLICY_STATUS}      1

    ${WAIT_UNTIL_UPDATE}=           Wait Until Device Update Done   device_serial=${device1.serial}
    Should Be Equal As Integers     ${WAIT_UNTIL_UPDATE}            1

    ${CONNECTED_STATUS}=            Wait Until Device Online                ${device1.serial}   None   30   20
    Should Be Equal as Integers     ${CONNECTED_STATUS}          1

    Log to Console      Sleep for ${client_connect_wait} seconds
    Sleep               ${client_connect_wait}

    ${CONNECT_STATUS}=              Remote_Server.Connect Open Network      ${NW_POLICY_SSID1}
    Should Be Equal As Integers     ${CONNECT_STATUS}               1

    Log to Console      Sleep for ${client_connect_wait} seconds
    Sleep               ${client_connect_wait}

    Negative Internet Connectivity Check

    Run Keyword If     "${mu1.platform}" == "mac"           Remote_Server.Kill Native Captive
    IF                 "${mu1.platform}" == "mac"
                        Open CP Browser    ${mu1.ip}        incognito=True
    ELSE
                        Open CP Browser    ${mu1.ip}
    END
    Log to Console      Sleep for ${cp_page_open_wait} seconds
    Sleep               ${cp_page_open_wait}

    ${SOCIAL_AUTH_STATUS}=          Validate CWP Social Login With Facebook     ${CWP_MAIL_ID}     ${CWP_MAIL_PASSWORD}
    Should Be Equal As Integers     ${SOCIAL_AUTH_STATUS}       1

    Log to Console      Sleep for ${auth_logs_duration_wait} seconds
    Sleep               ${auth_logs_duration_wait}
    ${AUTH_LOGS}=                   Get Authentication Logs Details     ${NW_POLICY_SSID1}        ${CWP_MAIL_ID}

    Log To Console          ${AUTH_LOGS}
    Should Not Be Empty     ${AUTH_LOGS}

    Positive Internet Connectivity Check

    # Logs Verification
    ${AUTH_STATUS}=                 Get From Dictionary     ${AUTH_LOGS}        reply
    Should Be Equal As Strings      '${AUTH_STATUS}'        '${AUTH_STATUS_ACCEPT}'

    ${USER_NAME}=                   Get From Dictionary     ${AUTH_LOGS}        userName
    Should Be Equal As Strings      '${USER_NAME}'          '${CWP_MAIL_ID}'

    ${SSID}=                        Get From Dictionary     ${AUTH_LOGS}        ssid
    Should Be Equal As Strings      '${SSID}'               '${NW_POLICY_SSID1}'

    ${AUTH_TYPE}=                   Get From Dictionary     ${AUTH_LOGS}        authType
    Should Be Equal As Strings      '${AUTH_TYPE}'          '${AUTH_TYPE_FACEBOOK}'

    ${CLIENT_MAC}=                  Get From Dictionary     ${AUTH_LOGS}        callingStationId
    Should Be Equal As Strings      '${CLIENT_MAC}'         '${mu1.wifi_mac}'

    ${REJ_CODE}=                    Get From Dictionary     ${AUTH_LOGS}        rejectReason
    Should Be Equal As Strings      '${REJ_CODE}'           ''

    ${AP_MAC}=                      Get From Dictionary     ${AUTH_LOGS}        calledStationId
    Should Be Equal As Strings      '${AP_MAC}'           '${device1.mac}'

    ${NAS_ID}=                      Get From Dictionary     ${AUTH_LOGS}        nasIdentifier
    Should Be Equal As Strings      '${NAS_ID}'             ''

    Remote_Server.Disconnect WiFi
    Log to Console      Sleep for ${client_disconnect_wait} seconds
    Sleep  ${client_disconnect_wait}

    ${CLEAR_CLIENT}=        Send            ${MAIN_DEVICE_SPAWN}         ${cmd_clear_client_mac}
    Log to Console      Sleep for ${ap_clear_mac_wait} seconds
    Sleep  ${ap_clear_mac_wait}

    ${SHOW_STATION}=        Send            ${MAIN_DEVICE_SPAWN}         ${cmd_show_station}
    Should Not Contain      ${SHOW_STATION}     ${mu1.wifi_mac}

    [Teardown]
    Run Keywords    Close CP Browser

TCCS-14366: Social login with Linkedin
    [Documentation]   CWP Social login with Linkedin
    ...               https://jira.aerohive.com/browse/APC-39420
    [Tags]            production    tccs_14366

    ${CREATE_NW_POLICY_STATUS}=     Create Network Policy           ${NW_POLICY_NAME3}  ${OPEN_NW_3}    cli_type=${device1.cli_type}
    Should Be Equal As Integers     ${CREATE_NW_POLICY_STATUS}      1

    ${UPDATE_NW_POLICY_STATUS}=     Update Network Policy To AP     ${NW_POLICY_NAME3}  ap_serial=${device1.serial}
    Should Be Equal As Integers     ${UPDATE_NW_POLICY_STATUS}      1

    ${WAIT_UNTIL_UPDATE}=           Wait Until Device Update Done   device_serial=${device1.serial}
    Should Be Equal As Integers     ${WAIT_UNTIL_UPDATE}            1

    Log to Console      Sleep for ${client_connect_wait} seconds
    Sleep               ${client_connect_wait}

    ${CONNECT_STATUS}=              Remote_Server.Connect Open Network      ${NW_POLICY_SSID3}
    Should Be Equal As Integers     ${CONNECT_STATUS}               1

    Log to Console      Sleep for ${client_connect_wait} seconds
    Sleep               ${client_connect_wait}

    Negative Internet Connectivity Check

    Run Keyword If     "${mu1.platform}" == "mac"           Remote_Server.Kill Native Captive
    IF                 "${mu1.platform}" == "mac"
                        Open CP Browser    ${mu1.ip}        incognito=True
    ELSE
                        Open CP Browser    ${mu1.ip}
    END
    Log to Console      Sleep for ${cp_page_open_wait} seconds
    Sleep               ${cp_page_open_wait}

    ${SOCIAL_AUTH_STATUS}=      Validate CWP Social Login With Linkedin Account    ${CWP_MAIL_ID}     ${CWP_MAIL_PASSWORD}
    Should Be Equal As Integers     ${SOCIAL_AUTH_STATUS}       1

    Log to Console      Sleep for ${auth_logs_duration_wait} seconds
    Sleep               ${auth_logs_duration_wait}

    Log to Console      Sleep for ${auth_logs_duration_wait} seconds
    Sleep               ${auth_logs_duration_wait}
    ${AUTH_LOGS}=                   Get Authentication Logs Details     ${NW_POLICY_SSID3}        ${CWP_MAIL_ID}

    Log To Console          ${AUTH_LOGS}
    Should Not Be Empty     ${AUTH_LOGS}

    Positive Internet Connectivity Check

    # Logs Verification
    ${AUTH_STATUS}=                 Get From Dictionary     ${AUTH_LOGS}        reply
    Should Be Equal As Strings      '${AUTH_STATUS}'        '${AUTH_STATUS_ACCEPT}'

    ${USER_NAME}=                   Get From Dictionary     ${AUTH_LOGS}        userName
    Should Be Equal As Strings      '${USER_NAME}'          '${CWP_MAIL_ID}'

    ${SSID}=                        Get From Dictionary     ${AUTH_LOGS}        ssid
    Should Be Equal As Strings      '${SSID}'               '${NW_POLICY_SSID3}'

    ${AUTH_TYPE}=                   Get From Dictionary     ${AUTH_LOGS}        authType
    Should Be Equal As Strings      '${AUTH_TYPE}'          '${AUTH_TYPE_LINKEDIN}'

    ${CLIENT_MAC}=                  Get From Dictionary     ${AUTH_LOGS}        callingStationId
    Should Be Equal As Strings      '${CLIENT_MAC}'         '${mu1.wifi_mac}'

    ${REJ_CODE}=                    Get From Dictionary     ${AUTH_LOGS}        rejectReason
    Should Be Equal As Strings      '${REJ_CODE}'           ''

    ${AP_MAC}=                      Get From Dictionary     ${AUTH_LOGS}        calledStationId
    Should Be Equal As Strings      '${AP_MAC}'           '${device1.mac}'

    ${NAS_ID}=                      Get From Dictionary     ${AUTH_LOGS}        nasIdentifier
    Should Be Equal As Strings      '${NAS_ID}'             ''

    Remote_Server.Disconnect WiFi
    Log to Console      Sleep for ${client_disconnect_wait} seconds
    Sleep  ${client_disconnect_wait}

    ${CLEAR_CLIENT}=        Send            ${MAIN_DEVICE_SPAWN}         ${cmd_clear_client_mac}
    Log to Console      Sleep for ${ap_clear_mac_wait} seconds
    Sleep  ${ap_clear_mac_wait}

    ${SHOW_STATION}=        Send            ${MAIN_DEVICE_SPAWN}         ${cmd_show_station}
    Should Not Contain      ${SHOW_STATION}     ${mu1.wifi_mac}

    [Teardown]
    Run Keywords    Close CP Browser

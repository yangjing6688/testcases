# Author        : Abhinith Anand
# Date          : April 28th 2022
# Description   : Extreme Guest Sanity
# Edited by     :
#
# Topology      : Needs to have :
#                   - a Floor plan: Extreme Networks,Bengaluru,Ecospace,Floor 1
#                     or needs to update the ${LOCATION_TREE} variable with the existing one.
#                   - a Fresh setup where eGuest is not yet initialized.
# Host ----- Cloud

*** Settings ***
Force Tags      testbed_1_node
Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml

Resource    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/extreme_guest/variables.robot
Resource    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/extreme_guest/extreme_guest_sanity_config.robot
Resource    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/extreme_guest/settings.robot
Resource    Tests/Robot/Functional/XIQ/Wireless/Sanity/Resources/extreme_guest/email_ids.robot

Library	    Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   Remote_Server
Library    String

Suite Setup      Pre Condition

*** Keywords ***
Pre Condition
    [Documentation]   AP Should be onboarded  and it is online


    # Use this method to convert the ap, wing, netelem to a generic device object
    # ap1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    convert to generic device object            device  index=1

    ${LOGIN_XIQ}=                       Login User          ${TENANT_USERNAME}     ${TENANT_PASSWORD}   url=${TEST_URL}    map_override=${MAP_FILE_NAME}
    Should Be Equal As Strings      '${LOGIN_XIQ}'   '1'

    ${CHANGE_DEVICE_PASSWORD}=        change device password          ${device1.password}
    Should Be Equal As Strings      '${CHANGE_DEVICE_PASSWORD}'   '1'

    ${ONBOARD_AP}=        onboard device quick        ${device1}
    Should Be Equal As Strings      '${ONBOARD_AP}'   '1'

    ${AP_SPAWN}=        Open Spawn          ${device1.ip}   ${device1.port}      ${device1.username}       ${device1.password}        ${device1.cli_type}
    Set Suite Variable  ${AP_SPAWN}

    ${OUTPUT0}=         Send Commands       ${AP_SPAWN}         capwap client server name ${CAPWAP_URL}, capwap client default-server-name ${CAPWAP_URL}, capwap client server backup name ${CAPWAP_URL}, no capwap client enable, capwap client enable, save config

    ${ONLINE_STATUS}=        Wait Until Device Online                ${device1.serial}
    Should Be Equal As Strings      '${ONLINE_STATUS}'   '1'
    Refresh Devices Page

    ${DEVICE_STATUS_RESULT}=                  get device status       ${device1.serial}
    Should Be Equal As Strings      '${DEVICE_STATUS_RESULT}'     'green'

    ${DELETE_NW_POLICIES}=        delete network polices          ${NW_POLICY_NAME0} ${NW_POLICY_NAME1} ${NW_POLICY_NAME2} ${NW_POLICY_NAME3}
    Should Be Equal As Strings      '${DELETE_NW_POLICIES}'   '1'

    ${DELETE_SSIDS}=        delete ssids                    ${SSID_NAME0} ${SSID_NAME1} ${SSID_NAME2} ${SSID_NAME3} ${SSID_NAME4}
    Should Be Equal As Strings      '${DELETE_SSIDS}'   '1'

    Run Keyword            Modify Suite Variables

    [Teardown]    go back to xiq

AP Cleanup
    [Documentation]    Clean Clien details from AP
    ${AP_SPAWN}=        Open Spawn          ${device1.ip}   ${device1.port}      ${device1.username}       ${device1.password}        ${device1.cli_type}
    ${CLEAR_CLIENT}=        Send            ${AP_SPAWN}         ${CMD_CLEAR_CLIENT_STATION}
    ${CLEAR_LOCAL_CACHE}=   Send            ${AP_SPAWN}         ${CMD_CLEAR_CLIENT_LOCAL}
    ${CLEAR_ROAMING_CACHE}=     Send            ${AP_SPAWN}         ${CMD_CLEAR_CLIENT_ROAMING}
    Log to Console      Sleep for ${AP_CLEAR_MAC_WAIT}
    sleep  ${AP_CLEAR_MAC_WAIT}
    ${SHOW_STATION}=        Send            ${AP_SPAWN}         ${CMD_SHOW_STATION}    
    
    Should Not Contain              ${SHOW_STATION}          ${mu1.wifi_mac}

    [Teardown]              Close Spawn    ${AP_SPAWN}

Modify Suite Variables
    [Documentation]    Modify Suite Variables
    ${RANDOM}=    Generate Random String
    Set Suite Variable    ${USER_EMAIL}    ${USER_NAME}+${RANDOM}@gmail.com
    Log To Console    User Email: ${USER_EMAIL}
    Set Suite Variable    ${SPONSOR_EMAIL}    ${SPONSOR_NAME}+${RANDOM}@gmail.com
    Log To Console    Sponsor Email: ${SPONSOR_EMAIL}
    Set Suite Variable    &{GUEST_MANAGEMENT_ROLE}    email=${USER_EMAIL}     name=${USER_NAME}     timeout=30     role=GuestManagement    organization=All Organizations

Create Network Policies
    [Documentation]    Create Network Policies

    ${CREATE_POLICY0}=              Create Network Policy   ${NW_POLICY_NAME0}      ${GUEST_OPEN_NW0}
    Should Be Equal As Strings      '${CREATE_POLICY0}'   '1'

    ${CREATE_POLICY1}=              Create Network Policy   ${NW_POLICY_NAME1}      ${GUEST_OPEN_NW1}
    Should Be Equal As Strings      '${CREATE_POLICY1}'   '1'

    ${CREATE_POLICY2}=              Create Network Policy   ${NW_POLICY_NAME2}      ${GUEST_OPEN_NW2}
    Should Be Equal As Strings      '${CREATE_POLICY2}'   '1'

    ${CREATE_POLICY3}=              Create Network Policy   ${NW_POLICY_NAME3}      ${GUEST_OPEN_NW3}
    Should Be Equal As Strings      '${CREATE_POLICY3}'   '1'

    ${CREATE_POLICY5}=              Create Network Policy   ${NW_POLICY_NAME5}      ${GUEST_OPEN_NW5}
    Should Be Equal As Strings      '${CREATE_POLICY5}'   '1'

    ${CREATE_POLICY6}=              Create Network Policy   ${NW_POLICY_NAME6}      ${GUEST_OPEN_NW6}
    Should Be Equal As Strings      '${CREATE_POLICY6}'   '1'

    ${CREATE_POLICY7}=              Create Network Policy   ${NW_POLICY_NAME7}      ${GUEST_OPEN_NW7}
    Should Be Equal As Strings      '${CREATE_POLICY7}'   '1'

    ${CREATE_POLICY8}=              Create Network Policy   ${NW_POLICY_NAME8}      ${GUEST_OPEN_NW8}
    Should Be Equal As Strings      '${CREATE_POLICY8}'   '1'

*** Test Cases ***
 
TCCS-12991: Guest Enablement Pre-check

    [Documentation]         Launch Extreme Guest Subscription Page

    [Tags]                  development    greenfield    subscription    tccs-12991

    ${CREATE_SSID}=             create open ssid in common objects  ${SSID_NAME4}
    Should Be Equal As Strings      '${CREATE_SSID}'     '1'

    ${CHECK_CREATED_SSID}=             check created ssid table  ${SSID_NAME4}
    Should Be Equal As Strings      '${CHECK_CREATED_SSID}'     '1'
    save screen shot

    [Teardown]   go back to xiq

TCCS-12993: Enable Guest Essentials

    [Documentation]         Launch Extreme Guest and Subscribe to Guest Application

    [Tags]                  development    greenfield    subscription    tccs-12993

    Depends On              TCCS-12991

    ${APPLY_OPEN_SSID}=             apply selected open ssid  ${SSID_NAME4}
    Should Be Equal As Strings      '${APPLY_OPEN_SSID}'     '1'
    save screen shot

    ${DELETE_SSID}=              Delete SSID    ${SSID_NAME4}
    Should Be Equal As Strings      '${DELETE_SSID}'     '1'
    
    [Teardown]    go back to xiq

TCCS-13118: Add Bulk Vouchers

    [Documentation]         Add Bulk Extreme Guest User Vouchers

    [Tags]                  development    greenfield    users    tccs-13118

    Depends On              TCCS-12993
    
    ${NAVIGATE_TO_EXTREME_GUEST_PAGE}=              go to extreme guest page
    Should Be Equal As Strings      '${NAVIGATE_TO_EXTREME_GUEST_PAGE}'     '1'

    ${NAVIGATE_TO_CONFIGURE_USERS_PAGE}=              go to configure users page
    Should Be Equal As Strings      '${NAVIGATE_TO_CONFIGURE_USERS_PAGE}'     '1'

    ${USER_COUNT1}=    Get Extreme Guest Users Count
    Log to Console     Number of Guest Users: ${USER_COUNT1}

    ${CREATE_BULK_VOUCHERS}=             create bulk vouchers  ${NO_OF_VOUCHERS}    access_group=${ACCESS_GROUP}    location_name=${LOCATION_TREE}
    Should Be Equal As Strings      '${CREATE_BULK_VOUCHERS}'     '1'

    Save Screen shot

    ${USER_COUNT2}=    Get Extreme Guest Users Count
    Log to Console     Nuselect_drop_down_options_partial_matchmber of Guest Users: ${USER_COUNT2}


    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             go back to xiq

TCCS-13119: Clone Splash Template, Onboarding Policy and Onboarding Rules

    [Documentation]         Clone Extreme Guest System Template and Create Onboarding Policy and Onboarding Rule

    [Tags]                  development    greenfield    brownfield    template    tccs-13119

    Depends On              TCCS-12993

    ${CREATE_N/W_POLICIES}=             Run Keyword        Create Network Policies

    ${NAVIGATE_TO_EXTREME_GUEST_PAGE}=             go to extreme guest page
    Should Be Equal As Strings      '${NAVIGATE_TO_EXTREME_GUEST_PAGE}'     '1'

    ${NAVIGATE_TO_CONFIGURE_PAGE}=                  go to configure page
    Should Be Equal As Strings      '${NAVIGATE_TO_CONFIGURE_PAGE}'     '1'

    ${CLONE_ACCEPT_TEMPLATE}=             clone accept connect template  template_name=${TEMPLATE1_NAME}
    Should Be Equal As Strings      '${CLONE_ACCEPT_TEMPLATE}'     '1'

    ${CLONE_SOCIAL_WIFI_TEMPLATE}=        clone social wifi with all template  template_name=${TEMPLATE6_NAME}
    Should Be Equal As Strings      '${CLONE_SOCIAL_WIFI_TEMPLATE}'     '1'

    ${CLONE_DEVICE_REG_WIFI_TEMPLATE}=    clone device registration with social wifi template   template_name=${TEMPLATE3_NAME}
    Should Be Equal As Strings      '${CLONE_DEVICE_REG_WIFI_TEMPLATE}'     '1'

    ${CLONE_EMAIL_TEMPLATE}=              Clone Email Access Template        ${TEMPLATE4_NAME}
    Should Be Equal As Strings      '${CLONE_EMAIL_TEMPLATE}'     '1'

    ${CLONE_USER_REG_TEMPLATE}=           clone user registration with social wifi template   template_name=${TEMPLATE9_NAME}
    Should Be Equal As Strings      '${CLONE_USER_REG_TEMPLATE}'     '1'

    ${CLONE_SPONSOR_TEMPLATE}=             clone_sponsored_guest_access_template  template_name=${TEMPLATE7_NAME}
    Should Be Equal As Strings      '${CLONE_ACCEPT_TEMPLATE}'     '1'

    save screen shot
    
    ${EG_POLICY_NAME_STATUS0}=             ADD ONBOARDING POLICY   policy_name=${EG_POLICY_NAME0}  group_name=${GROUP_NAME}    condition_type=${CONDITION_TYPE0}
    Should Be Equal As Strings      '${EG_POLICY_NAME_STATUS0}'     '1'

    ${EG_POLICY_NAME_STATUS1}=             ADD ONBOARDING POLICY   policy_name=${EG_POLICY_NAME1}  group_name=${GROUP_NAME}    condition_type=${CONDITION_TYPE1}
    Should Be Equal As Strings      '${EG_POLICY_NAME_STATUS1}'     '1'

    ${EG_POLICY_NAME_STATUS2}=             ADD ONBOARDING POLICY   policy_name=${EG_POLICY_NAME2}  group_name=${GROUP_NAME}    condition_type=${CONDITION_TYPE4}    condition_value=${CONDITION_VALUE}    action_type=${SEND_OTP_TO_USER}    user_notifpolicy=${DEFAULT_NOTIFICATION_POLICY1}    sponsor_notifpolicy=${DEFAULT_NOTIFICATION_POLICY2}
    Should Be Equal As Strings      '${EG_POLICY_NAME_STATUS2}'     '1'

    ${EG_POLICY_NAME_STATUS3}=             ADD ONBOARDING POLICY   policy_name=${EG_POLICY_NAME3}  group_name=${GROUP_NAME}    condition_type=${CONDITION_TYPE4}
    Should Be Equal As Strings      '${EG_POLICY_NAME_STATUS3}'     '1'

    ${EG_POLICY_NAME_STATUS4}=             ADD ONBOARDING POLICY   policy_name=${EG_POLICY_NAME4}  group_name=${GROUP_NAME}    condition_type=${CONDITION_TYPE3}    condition_value=${CONDITION_VALUE}    action_type=${SEND_PASSCODE_ON_APPROVAL}    user_notifpolicy=${DEFAULT_NOTIFICATION_POLICY1}    sponsor_notifpolicy=${DEFAULT_NOTIFICATION_POLICY2}
    Should Be Equal As Strings      '${EG_POLICY_NAME_STATUS4}'     '1'

    save screen shot

    ${EG_RULE_NAME_0}=             ADD ONBOARDING RULE     rule_name=${EG_RULE_NAME0}  policy_name=${EG_POLICY_NAME0}  location_name=${LOCATION_TREE}    network_name=${SSID_NAME0}
    Should Be Equal As Strings      '${EG_RULE_NAME_0}'     '1'

    ${EG_RULE_NAME_1}=             ADD ONBOARDING RULE     rule_name=${EG_RULE_NAME1}  policy_name=${EG_POLICY_NAME1}  location_name=${LOCATION_TREE}    network_name=${SSID_NAME1}
    Should Be Equal As Strings      '${EG_RULE_NAME_1}'     '1'

    ${EG_RULE_NAME_2}=             ADD ONBOARDING RULE     rule_name=${EG_RULE_NAME2}  policy_name=${EG_POLICY_NAME1}  location_name=${LOCATION_TREE}    network_name=${SSID_NAME2}
    Should Be Equal As Strings      '${EG_RULE_NAME_2}'     '1'

    ${EG_RULE_NAME_3}=             ADD ONBOARDING RULE     rule_name=${EG_RULE_NAME3}  policy_name=${EG_POLICY_NAME1}  location_name=${LOCATION_TREE}    network_name=${SSID_NAME3}
    Should Be Equal As Strings      '${EG_RULE_NAME_3}'     '1'

    ${EG_RULE_NAME_4}=             ADD ONBOARDING RULE     rule_name=${EG_RULE_NAME4}  policy_name=${EG_POLICY_NAME2}  location_name=${LOCATION_TREE}    network_name=${SSID_NAME5}
    Should Be Equal As Strings      '${EG_RULE_NAME_4}'     '1'
    
    ${EG_RULE_NAME_5}=             ADD ONBOARDING RULE     rule_name=${EG_RULE_NAME5}  policy_name=${EG_POLICY_NAME2}  location_name=${LOCATION_TREE}    network_name=${SSID_NAME6}
    Should Be Equal As Strings      '${EG_RULE_NAME_5}'     '1'

    ${EG_RULE_NAME_6}=             ADD ONBOARDING RULE     rule_name=${EG_RULE_NAME6}  policy_name=${EG_POLICY_NAME3}  location_name=${LOCATION_TREE}    network_name=${SSID_NAME7}
    Should Be Equal As Strings      '${EG_RULE_NAME_6}'     '1'

    ${EG_RULE_NAME_7}=             ADD ONBOARDING RULE     rule_name=${EG_RULE_NAME7}  policy_name=${EG_POLICY_NAME4}  location_name=${LOCATION_TREE}    network_name=${SSID_NAME8}
    Should Be Equal As Strings      '${EG_RULE_NAME_7}'     '1'


    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             go back to xiq

TCCS-12997: Verify User registration and authenticate CP with Facebook

    [Documentation]         Verify Facebook Social Login

    [Tags]                  development    greenfield    brownfield    social    facebook    tccs-12997

    Depends On              TCCS-12993    TCCS-13119

    ${AP1_UPDATE_CONFIG}=           Deploy Network Policy with Complete Update      ${NW_POLICY_NAME1}          ${device1.serial}
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${DEVICE_STATUS}=             Wait Until Device Online       ${device1.serial}
    Should Be Equal As Strings      '${DEVICE_STATUS}'     '1'

    ${NAVIGATE_TO_EXTREME_GUEST_PAGE}=             go to extreme guest page
    Should Be Equal As Strings      '${NAVIGATE_TO_EXTREME_GUEST_PAGE}'     '1'

    ${NAVIGATE_TO_CONFIGURE_PAGE}=             go to configure page
    Should Be Equal As Strings      '${NAVIGATE_TO_CONFIGURE_PAGE}'     '1'

    ${CONFIGURE_SPLASH_SYSTEM_TEMPLATE}=             go to configure splash system template tab
    Should Be Equal As Strings      '${CONFIGURE_SPLASH_SYSTEM_TEMPLATE}'     '1'

    ${APPLY_USER_TEMPLATE}=             apply network to user template  network_name=${SSID_NAME1}      template_name=${TEMPLATE6_NAME}     location=${LOCATION_TREE}
    Should Be Equal As Strings      '${APPLY_USER_TEMPLATE}'     '1'

    ${SEND_CMD_STATUS}=             send wg cmd to ap  ${SSID_NAME1}    @{fb_cli_obj}
    
    Log to Console      Sleep for ${CONFIG_PUSH_WAIT}
    Sleep                         ${CONFIG_PUSH_WAIT}

    ${CONNECT_CLIENT_OPEN_N/W}=             Remote_Server.Connect Open Network    ${SSID_NAME1}
    Should Be Equal As Strings      '${CONNECT_CLIENT_OPEN_N/W}'     '1'
    Log to Console      Sleep for ${CLIENT_CONNECT_WAIT}
    Sleep                         ${CLIENT_CONNECT_WAIT}
    
    ${OPEN_GUEST_PORTAL}=             open guest portal browser    ${mu1.ip}
    Log to Console      Sleep for ${CP_PAGE_OPEN_WAIT}
    Sleep  ${CP_PAGE_OPEN_WAIT}

    ${SOCIAL_AUTH_STATUS}=                 validate eguest social login with facebook     ${MAIL_ID3}      ${MAIL_ID3_PASS}
    
    get gp page screen shot

    ${FACEBOOK_USER_COUNT}=    Get Extreme Social Users Count    social_name=Facebook
    Log to Console     Number of Facebook Users: ${FACEBOOK_USER_COUNT}

    ${WIFI_DISCONNECT}=             Remote_Server.Disconnect WiFi
    Should Be Equal As Strings      '${WIFI_DISCONNECT}'     '1'

    Log to Console      Sleep for ${CLIENT_DISCONNECT_WAIT}
    Sleep  ${CLIENT_DISCONNECT_WAIT}

    ${NAVIGATE_TO_CONFIGURE_PAGE}=             go to configure users page
    Should Be Equal As Strings      '${NAVIGATE_TO_CONFIGURE_PAGE}'     '1'

    ${DELETE_USER_FB}=             delete user  facebook
    Should Be Equal As Strings      '${DELETE_USER_FB}'     '1'
    
    Should Be Equal As Strings     '${SOCIAL_AUTH_STATUS}'  '1'

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             close gp browser
    ...                             AP Cleanup
    ...                             go back to xiq

TCCS-13695: Verify Number of Facebook Registration

    [Documentation]         Verify Number of Facebook Registration

    [Tags]                  development    greenfield    brownfield    social    facebook    tccs-13695

    Depends On              TCCS-12997

TCCS-12998: Verify User registration and authenticate CP with LinkedIn

    [Documentation]         Verify LnkedIn Social Login

    [Tags]                  development    greenfield    brownfield    social    linkedin    tccs-12998

    Depends On              TCCS-12993    TCCS-13119

    ${AP1_UPDATE_CONFIG}=           Deploy Network Policy with Delta Update     ${NW_POLICY_NAME2}          ${device1.serial}
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${DEVICE_STATUS}=           Wait Until Device Online       ${device1.serial}
    Should Be Equal As Strings      '${DEVICE_STATUS}'       '1'

    ${NAVIGATE_TO_EXTREME_GUEST_PAGE}=             go to extreme guest page
    Should Be Equal As Strings      '${NAVIGATE_TO_EXTREME_GUEST_PAGE}'       '1'

    ${NAVIGATE_TO_CONFIGURE_PAGE}=             go to configure page
    Should Be Equal As Strings      '${NAVIGATE_TO_CONFIGURE_PAGE}'       '1'

    ${CONFIGURE_SPLASH_SYSTEM_TEMPLATE}=             go to configure splash system template tab
    Should Be Equal As Strings      '${CONFIGURE_SPLASH_SYSTEM_TEMPLATE}'       '1'

    ${APPLY_USER_TEMPLATE}=             apply network to user template  network_name=${SSID_NAME2}      template_name=${TEMPLATE6_NAME}     location=${LOCATION_TREE}
    Should Be Equal As Strings      '${APPLY_USER_TEMPLATE}'     '1'

    ${SEND_CMD_STATUS}=             send wg cmd to ap  ${SSID_NAME2}    @{lnkd_cli_obj}
    
    Log to Console      Sleep for ${CONFIG_PUSH_WAIT}
    Sleep                         ${CONFIG_PUSH_WAIT}

    ${CONNECT_CLIENT_OPEN_N/W}=             Remote_Server.Connect Open Network    ${SSID_NAME2}
    Should Be Equal As Strings      '${CONNECT_CLIENT_OPEN_N/W}'     '1'
    Log to Console      Sleep for ${CLIENT_CONNECT_WAIT}
    Sleep                         ${CLIENT_CONNECT_WAIT}
    
    ${OPEN_GUEST_PORTAL}=             open guest portal browser    ${mu1.ip}
    Log to Console      Sleep for ${CP_PAGE_OPEN_WAIT}
    Sleep  ${CP_PAGE_OPEN_WAIT}

    ${SOCIAL_AUTH_STATUS}=                 validate eguest social login with linkedin    ${MAIL_ID3}      ${MAIL_ID3_PASS}
    
    get gp page screen shot

    ${LINKENDIN_USER_COUNT}=    Get Extreme Social Users Count    social_name=Linkedin
    Log to Console     Number of Linkedin Users: ${LINKENDIN_USER_COUNT}

    ${WIFI_DISCONNECT}=             Remote_Server.Disconnect WiFi
    Should Be Equal As Strings      '${WIFI_DISCONNECT}'     '1'
    Log to Console      Sleep for ${CLIENT_DISCONNECT_WAIT}
    Sleep  ${CLIENT_DISCONNECT_WAIT}

    ${NAVIGATE_TO_CONFIGURE_PAGE}=             go to configure users page
    Should Be Equal As Strings      '${NAVIGATE_TO_CONFIGURE_PAGE}'       '1'
    
    ${DELETE_USER_LINKEDIN}=             delete user  linkedin
    Should Be Equal As Strings      '${DELETE_USER_LINKEDIN}'       '1'

    Should Be Equal As Strings      '${SOCIAL_AUTH_STATUS}'       '1'

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             close gp browser
    ...                             AP Cleanup
    ...                             go back to xiq

TCCS-13696: Verify Number of LinkedIn Registration

    [Documentation]         Verify Number of LinkedIn Registration

    [Tags]                  development    greenfield    brownfield    social    linkedin    tccs-13696

    Depends On              TCCS-12998

TCCS-13014: Verify Default System template (Accept and Connect)

    [Documentation]         Verify default Captive portal Login
    
    [Tags]                  development    greenfield    brownfield    simple    tccs-13014

    ${CREATE_POLICY4}=              Create Network Policy   ${NW_POLICY_NAME4}      ${GUEST_OPEN_NW4}
    Should Be Equal As Strings      '${CREATE_POLICY4}'   '1'

    ${AP1_UPDATE_CONFIG}=           Deploy Network Policy with Delta Update     ${NW_POLICY_NAME4}          ${device1.serial}
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${DEVICE_STATUS}=           Wait Until Device Online       ${device1.serial}
    Should Be Equal As Strings      '${DEVICE_STATUS}'       '1'

    ${CONNECT_CLIENT_OPEN_N/W}=             Remote_Server.Connect Open Network    ${SSID_NAME4}
    Should Be Equal As Strings      '${CONNECT_CLIENT_OPEN_N/W}'       '1'
    Log to Console      Sleep for ${CLIENT_CONNECT_WAIT}
    Sleep                         ${CLIENT_CONNECT_WAIT}
    
    ${OPEN_GUEST_PORTAL}=             open guest portal browser    ${mu1.ip}
    Log to Console      Sleep for ${CP_PAGE_OPEN_WAIT}
    Sleep       ${CP_PAGE_OPEN_WAIT}

    ${USER_AUTH_STATUS}=                 validate eguest default template with no mapping

    get gp page screen shot

    ${WIFI_DISCONNECT}=             Remote_Server.Disconnect WiFi
    Should Be Equal As Strings      '${WIFI_DISCONNECT}'       '1'
    Log to Console      Sleep for ${CLIENT_DISCONNECT_WAIT}
    Sleep       ${CLIENT_DISCONNECT_WAIT}

    Should Be Equal As Strings      '${USER_AUTH_STATUS}'       '1'

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             close gp browser
    ...                             AP Cleanup
    ...                             go back to xiq


TCCS-12994: Verify Device registration and authenticate CP with OTP notified over email

    [Documentation]         Verify Device Registration
    
    [Tags]                  development    greenfield    brownfield    dev_reg_email    tccs-12994

    Depends On              TCCS-12993    TCCS-13119

    ${AP1_UPDATE_CONFIG}=           Deploy Network Policy with Delta Update     ${NW_POLICY_NAME5}          ${device1.serial}
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${DEVICE_STATUS}=           Wait Until Device Online       ${device1.serial}
    Should Be Equal As Strings      '${DEVICE_STATUS}'       '1'

    ${NAVIGATE_TO_EXTREME_GUEST_PAGE}=             go to extreme guest page
    Should Be Equal As Strings      '${NAVIGATE_TO_EXTREME_GUEST_PAGE}'       '1'

    ${NAVIGATE_TO_CONFIGURE_PAGE}=             go to configure page
    Should Be Equal As Strings      '${NAVIGATE_TO_CONFIGURE_PAGE}'       '1'

    ${CONFIGURE_SPLASH_SYSTEM_TEMPLATE}=             go to configure splash system template tab
    Should Be Equal As Strings      '${CONFIGURE_SPLASH_SYSTEM_TEMPLATE}'       '1'

    ${APPLY_USER_TEMPLATE}=             apply network to user template  network_name=${SSID_NAME5}      template_name=${TEMPLATE3_NAME}     location=${LOCATION_TREE}
    Should Be Equal As Strings      '${APPLY_USER_TEMPLATE}'     '1'

    ${CONNECT_CLIENT_OPEN_N/W}=             Remote_Server.Connect Open Network    ${SSID_NAME5}
    Should Be Equal As Strings      '${CONNECT_CLIENT_OPEN_N/W}'     '1'
    Log to Console      Sleep for ${CLIENT_CONNECT_WAIT}
    Sleep                         ${CLIENT_CONNECT_WAIT}
    
    ${OPEN_GUEST_PORTAL}=             Open Guest Portal Browser    ${mu1.ip}
    Log to Console      Sleep for ${CP_PAGE_OPEN_WAIT}
    Sleep  ${CP_PAGE_OPEN_WAIT}

    ${REGISTRATION_STATUS}=                 Register Device for Guest Access    ${USER_NAME}    ${USER_EMAIL}
    get gp page screen shot
    Should Be Equal As Strings     '${REGISTRATION_STATUS}'  '1'

    Log to Console      Sleep for ${RECEIVE_MAIL}
    Sleep                         ${RECEIVE_MAIL}

    ${ACCESS_STATUS}=    Validate Sponsored Guest Access    ${USER_EMAIL}    ${USER_PASSWORD}    ${SEND_OTP_TO_USER}
    get gp page screen shot

    ${WIFI_DISCONNECT}=             Remote_Server.Disconnect WiFi
    Should Be Equal As Strings      '${WIFI_DISCONNECT}'     '1'
    Log to Console      Sleep for ${CLIENT_DISCONNECT_WAIT}
    Sleep  ${CLIENT_DISCONNECT_WAIT}

    ${NAVIGATE_TO_CONFIGURE_PAGE}=             Go to Configure Users Page
    Should Be Equal As Strings      '${NAVIGATE_TO_CONFIGURE_PAGE}'       '1'

    ${DELETE_USER_EMAIL}=             Delete User  ${USER_EMAIL}
    Should Be Equal As Strings     '${DELETE_USER_EMAIL}'  '1'

    Should Be Equal As Strings     '${ACCESS_STATUS}'  '1'

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             close gp browser
    ...                             AP Cleanup
    ...                             go back to xiq

TCCS-13012: Verify User registration and authenticate CP with passcode notified over email

    [Documentation]         Verify User Registration

    [Tags]                  development    greenfield    brownfield    user_reg_email    tccs_13012
    
    Depends On              TCCS-12993    TCCS-13119

    ${AP1_UPDATE_CONFIG}=           Deploy Network Policy with Delta Update     ${NW_POLICY_NAME6}          ${device1.serial}
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${DEVICE_STATUS}=           Wait Until Device Online       ${device1.serial}
    Should Be Equal As Strings     '${DEVICE_STATUS}'  '1'

    ${NAVIGATE_TO_EXTREME_GUEST_PAGE}=             go to extreme guest page
    Should Be Equal As Strings     '${NAVIGATE_TO_EXTREME_GUEST_PAGE}'  '1'

    ${NAVIGATE_TO_CONFIGURE_PAGE}=             go to configure page
    Should Be Equal As Strings     '${NAVIGATE_TO_CONFIGURE_PAGE}'  '1'

    ${CONFIGURE_SPLASH_SYSTEM_TEMPLATE}=             go to configure splash system template tab
    Should Be Equal As Strings     '${CONFIGURE_SPLASH_SYSTEM_TEMPLATE}'  '1'

    ${APPLY_USER_TEMPLATE}=             apply network to user template  network_name=${SSID_NAME6}      template_name=${TEMPLATE9_NAME}     location=${LOCATION_TREE}
    Should Be Equal As Strings     '${APPLY_USER_TEMPLATE}'  '1'

    ${CONNECT_CLIENT_OPEN_N/W}=             Remote_Server.Connect Open Network    ${SSID_NAME6}
    Should Be Equal As Strings     '${CONNECT_CLIENT_OPEN_N/W}'  '1'
    Log to Console      Sleep for ${CLIENT_CONNECT_WAIT}
    Sleep                         ${CLIENT_CONNECT_WAIT}

    ${OPEN_GUEST_PORTAL}=             Open Guest Portal Browser    ${mu1.ip}
    Log to Console      Sleep for ${CP_PAGE_OPEN_WAIT}
    Sleep  ${CP_PAGE_OPEN_WAIT}

    ${REGISTRATION_STATUS}=                 Register Device for Guest Access    ${USER_NAME}    ${USER_EMAIL}
    get gp page screen shot
    Should Be Equal As Strings     '${REGISTRATION_STATUS}'  '1'

    Log to Console      Sleep for ${RECEIVE_MAIL}
    Sleep                         ${RECEIVE_MAIL}

    ${ACCESS_STATUS}=    Validate Sponsored Guest Access    ${USER_EMAIL}    ${USER_PASSWORD}    ${SEND_OTP_TO_USER}
    get gp page screen shot

    ${WIFI_DISCONNECT}=             Remote_Server.Disconnect WiFi
    Should Be Equal As Strings     '${WIFI_DISCONNECT}'  '1'
    Log to Console      Sleep for ${CLIENT_DISCONNECT_WAIT}
    Sleep  ${CLIENT_DISCONNECT_WAIT}

    ${NAVIGATE_TO_CONFIGURE_PAGE}=             Go to Configure Users Page
    Should Be Equal As Strings     '${NAVIGATE_TO_CONFIGURE_PAGE}'  '1'

    ${DELETE_USER_EMAIL}=             Delete User  ${USER_EMAIL}
    Should Be Equal As Strings     '${DELETE_USER_EMAIL}'  '1'

    Should Be Equal As Strings     '${ACCESS_STATUS}'  '1'

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             close gp browser
    ...                             AP Cleanup
    ...                             go back to xiq


TCCS-13694: Sponsor Approval-Verify on sponsor Permit login passcode sent to user mail

    [Documentation]     Sponsor Approval-Verify on sponsor Permit login passcode sent to user mail

    [Tags]              development    greenfield    brownfield    sponsor_flow    tccs_13694
    
    Depends On              TCCS-12993    TCCS-13119

    ${AP1_UPDATE_CONFIG}=           Deploy Network Policy with Delta Update     ${NW_POLICY_NAME8}          ${device1.serial}
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${DEVICE_STATUS}=           Wait Until Device Online       ${device1.serial}
    Should Be Equal As Strings     '${DEVICE_STATUS}'  '1'

    ${NAVIGATE_TO_EXTREME_GUEST_PAGE}=             go to extreme guest page
    Should Be Equal As Strings     '${NAVIGATE_TO_EXTREME_GUEST_PAGE}'  '1'

    ${NAVIGATE_TO_CONFIGURE_PAGE}=             go to configure page
    Should Be Equal As Strings     '${NAVIGATE_TO_CONFIGURE_PAGE}'  '1'

    save screen shot

    ${CONFIGURE_SPLASH_SYSTEM_TEMPLATE}=             go to configure splash system template tab

    Should Be Equal As Strings      '${CONFIGURE_SPLASH_SYSTEM_TEMPLATE}'       '1'

    ${APPLY_USER_TEMPLATE}=             apply network to user template  network_name=${SSID_NAME8}      template_name=${TEMPLATE7_NAME}     location=${LOCATION_TREE}

    Should Be Equal As Strings      '${APPLY_USER_TEMPLATE}'     '1'

    Remote_Server.Connect Open Network    ${SSID_NAME8}

    Log to Console      Sleep for ${CLIENT_CONNECT_WAIT}

    Sleep                         ${CLIENT_CONNECT_WAIT}

    Open Guest Portal Browser    ${mu1.ip}

    Log to Console      Sleep for ${CP_PAGE_OPEN_WAIT}

    Sleep  ${CP_PAGE_OPEN_WAIT}

    ${REGISTRATION_STATUS}=                 Register Sponsored Guest User    ${USER_NAME}    ${USER_EMAIL}    ${USER_MOBILE}    ${SPONSOR_NAME}     ${SPONSOR_EMAIL}     ${ACCESS_PURPOSE}

    Log to Console      Sleep for ${RECEIVE_MAIL}
    Sleep                         ${RECEIVE_MAIL}

    ${APPROVAL_URL}=        Get Sponsor Action URL      ${SPONSOR_EMAIL}    ${SPONSOR_PASSWORD}    ${SPONSOR_PERMIT}

    ${DRIVER}=    Load Browser    ${APPROVAL_URL}    program=${PROGRAM}

    ${TEXT}=    Check Approval Success Text    ${DRIVER}

    Quit Browser    ${DRIVER}

    ${ACCESS_STATUS}=    Validate Sponsored Guest Access    ${USER_EMAIL}    ${USER_PASSWORD}    ${SEND_PASSCODE_ON_APPROVAL}

    ${WIFI_DISCONNECT}=             Remote_Server.Disconnect WiFi

    Should Be Equal As Strings      '${WIFI_DISCONNECT}'     '1'

    Log to Console      Sleep for ${CLIENT_DISCONNECT_WAIT}

    Sleep  ${CLIENT_DISCONNECT_WAIT}

    ${NAVIGATE_TO_CONFIGURE_PAGE}=             Go to Configure Users Page

    Should Be Equal As Strings      '${NAVIGATE_TO_CONFIGURE_PAGE}'       '1'

    ${DELETE_USER_EMAIL}=             Delete User  ${USER_EMAIL}

    Should Be Equal As Strings     '${DELETE_USER_EMAIL}'  '1'

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             close gp browser
    ...                             AP Cleanup
    ...                             go back to xiq


TCCS-12995: Verify user authentication with guest bulk vouchers

    [Documentation]         Verify User auth with Guest Vouchers

    [Tags]                  development    greenfield    brownfield    voucher_login    tccs_12995

    Depends On              TCCS-12993    TCCS-13119

    ${AP1_UPDATE_CONFIG}=           Deploy Network Policy with Delta Update     ${NW_POLICY_NAME0}          ${device1.serial}
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${DEVICE_STATUS}=           Wait Until Device Online       ${device1.serial}
    Should Be Equal As Strings      '${DEVICE_STATUS}'       '1'

    ${NAVIGATE_TO_EXTREME_GUEST_PAGE}=             go to extreme guest page
    Should Be Equal As Strings      '${NAVIGATE_TO_EXTREME_GUEST_PAGE}'       '1'

    ${NAVIGATE_TO_CONFIGURE_PAGE}=             go to configure page
    Should Be Equal As Strings      '${NAVIGATE_TO_CONFIGURE_PAGE}'       '1'

    ${NAVIGATE_TO_CONFIGURE_USERS_PAGE}=             go to configure users page
    Should Be Equal As Strings      '${NAVIGATE_TO_CONFIGURE_USERS_PAGE}'       '1'

    ${USER_COUNT1}=    Get Extreme Guest Users Count
    Log to Console     Number of Guest Users: ${USER_COUNT1}

    ${VOUCHER_CREDENTIALS}=             create bulk vouchers client login  ${NO_OF_VOUCHERS}    access_group=${ACCESS_GROUP}    location_name=${LOCATION_TREE}

    ${USER_COUNT2}=    Get Extreme Guest Users Count
    Log to Console     Number of Guest Users: ${USER_COUNT2}

    ${CONFIGURE_SPLASH_SYSTEM_TEMPLATE}=             go to configure splash system template tab
    Should Be Equal As Strings      '${CONFIGURE_SPLASH_SYSTEM_TEMPLATE}'       '1'

    ${APPLY_STATUS}=             apply network to user template  network_name=${SSID_NAME0}      template_name=${TEMPLATE9_NAME}     location=${LOCATION_TREE}
    Should Be Equal As Strings      '${APPLY_STATUS}'       '1'

    ${CONNECT_CLIENT_OPEN_N/W}=             Remote_Server.Connect Open Network    ${SSID_NAME0}
    Should Be Equal As Strings      '${CONNECT_CLIENT_OPEN_N/W}'       '1'
    Log to Console      Sleep for ${CLIENT_CONNECT_WAIT}
    Sleep                         ${CLIENT_CONNECT_WAIT}

    ${OPEN_GUEST_PORTAL}=             open guest portal browser    ${mu1.ip}
    Log to Console      Sleep for ${CP_PAGE_OPEN_WAIT}
    Sleep       ${CP_PAGE_OPEN_WAIT}

    ${USER_AUTH_STATUS}=                 validate eguest user login with voucher credentials    ${VOUCHER_CREDENTIALS}
    get gp page screen shot

    ${WIFI_DISCONNECT}=             Remote_Server.Disconnect WiFi
    Should Be Equal As Strings      '${WIFI_DISCONNECT}'       '1'
    Log to Console      Sleep for ${CLIENT_DISCONNECT_WAIT}
    Sleep  ${CLIENT_DISCONNECT_WAIT}

    ${USERNAME1}=                 Get Username from vouchers   ${VOUCHER_CREDENTIALS}
    ${NAVIGATE_TO_CONFIGURE_PAGE}=             Go to Configure Users Page
    Should Be Equal As Strings     '${NAVIGATE_TO_CONFIGURE_PAGE}'  '1'

    ${DELETE_USER}=             Delete User    ${USERNAME1}
    Should Be Equal As Strings     '${DELETE_USER}'  '1'

    Should Be Equal As Strings      '${USER_AUTH_STATUS}'       '1'

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             close gp browser
    ...                             AP Cleanup
    ...                             go back to xiq


TCCS-12996: Verify User registration and get CP access using E-mail

    [Documentation]         Verify Device Registration

    [Tags]                  development    greenfield    brownfield    email_access    tccs_12996

    Depends On              TCCS-12993    TCCS-13119

    ${AP1_UPDATE_CONFIG}=           Deploy Network Policy with Delta Update     ${NW_POLICY_NAME7}          ${device1.serial}
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${DEVICE_STATUS}=           Wait Until Device Online       ${device1.serial}
    Should Be Equal As Strings      '${DEVICE_STATUS}'       '1'

    ${NAVIGATE_TO_EXTREME_GUEST_PAGE}=             go to extreme guest page
    Should Be Equal As Strings      '${NAVIGATE_TO_EXTREME_GUEST_PAGE}'       '1'

    ${NAVIGATE_TO_CONFIGURE_PAGE}=             go to configure page
    Should Be Equal As Strings      '${NAVIGATE_TO_CONFIGURE_PAGE}'       '1'

    # ${EG_POLICY_NAME_STATUS1}=             ADD ONBOARDING POLICY EXISTING ONE   policy_name=${EG_POLICY_NAME2}  group_name=${GROUP_NAME}    condition_type=${CONDITION_TYPE4}    condition_value=${CONDITION_VALUE}
    # Should Be Equal As Strings      '${EG_POLICY_NAME_STATUS1}'     '1'

    ${CONFIGURE_SPLASH_SYSTEM_TEMPLATE}=             go to configure splash system template tab
    Should Be Equal As Strings      '${CONFIGURE_SPLASH_SYSTEM_TEMPLATE}'       '1'

    ${APPLY_USER_TEMPLATE}=             apply network to user template  network_name=${SSID_NAME7}      template_name=${TEMPLATE4_NAME}     location=${LOCATION_TREE}
    Should Be Equal As Strings     '${APPLY_USER_TEMPLATE}'  '1'

    ${CONNECT_CLIENT_OPEN_N/W}=             Remote_Server.Connect Open Network    ${SSID_NAME7}
    Should Be Equal As Strings     '${CONNECT_CLIENT_OPEN_N/W}'  '1'
    Log to Console      Sleep for ${CLIENT_CONNECT_WAIT}
    Sleep                         ${CLIENT_CONNECT_WAIT}

    ${OPEN_GUEST_PORTAL}=             Open Guest Portal Browser    ${mu1.ip}
    Log to Console      Sleep for ${CP_PAGE_OPEN_WAIT}
    Sleep  ${CP_PAGE_OPEN_WAIT}

    ${REGISTRATION_STATUS}=                 Register Device with Email for Guest Access    ${USER_EMAIL}
    get gp page screen shot
    Should Be Equal As Strings     '${REGISTRATION_STATUS}'  '1'

    Set Suite Variable    ${USERNAME}        ${USER_EMAIL}

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             close gp browser
    ...                             go back to xiq

TCCS-13019: Verify Analyze users UI

    [Documentation]        Check username in Analyze Users page

    [Tags]                  development    greenfield    brownfield    analyze_users    tccs_13019

    Depends On             TCCS-12996

    ${NAVIGATE_TO_ANALYZE_PAGE}=             Go To Analyze Page
    Should Be Equal As Strings      '${NAVIGATE_TO_ANALYZE_PAGE}'       '1'

    ${NAVIGATE_TO_ANALYZE_USER_PAGE}=             Go to Analyze Users Page
    Should Be Equal As Strings      '${NAVIGATE_TO_ANALYZE_USER_PAGE}'       '1'

    ${USER_EXISTS}=              Check If The User Exists        ${USERNAME}        ${LOCATION_TREE}
    Should Be Equal As Strings      '${USER_EXISTS}'       '1'

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             Go back To XIQ

TCCS-13020: Verify Analyze Clients UI

    [Documentation]        Check Client MAC address in Analyze Clients page

    [Tags]                  development    greenfield    brownfield    analyze_clients    tccs_13020

    Depends On             TCCS-12996

    ${NAVIGATE_TO_ANALYZE_PAGE}=             Go To Analyze Page
    Should Be Equal As Strings      '${NAVIGATE_TO_ANALYZE_PAGE}'       '1'

    ${NAVIGATE_TO_ANALYZE_USER_PAGE}=             Go to Analyze Clients Page
    Should Be Equal As Strings      '${NAVIGATE_TO_ANALYZE_USER_PAGE}'       '1'

    ${CLIENT_EXISTS}=              Check If The Client Exists        ${mu1.wifi_mac}        ${LOCATION_TREE}
    Should Be Equal As Strings      '${CLIENT_EXISTS}'       '1'

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             Go back To XIQ

TCCS-13000: Verify Summary Analytics Dashboard Widgets

    [Documentation]         Check all Summary page Widgets

    [Tags]                  development    greenfield    brownfield    analytics    tccs_13000

    Depends On              TCCS-12993

    ${VALIDATE_LANDING_PAGE}=             check all landing page widgets
    Save Screen shot
    Should Be Equal As Strings      '${VALIDATE_LANDING_PAGE}'     '1'

    [Teardown]   run keywords       go back to xiq


TCCS-13008: Verify Summary More Insights Dashboard Widgets

    [Documentation]         Check all Landing page widgets

    [Tags]                  development    greenfield    brownfield    analytics    tccs_13008

    Depends On              TCCS-12993

    ${CHACK_SUMMARY_PAGE}=             check all summary page widgets
    Save Screen shot
    Should Be Equal As Strings      '${CHACK_SUMMARY_PAGE}'     '1'

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             Go back To XIQ

TCCS-13009: Verify All the counters of KMS at Root Level
    [Documentation]         Verify all KMS count

    [Tags]                  development    greenfield    brownfield    analytics    tccs_13009

    Depends On              TCCS-12993    TCCS-12996

    ${NAVIGATE_TO_EXTREME_GUEST_PAGE}=             go to extreme guest page
    Should Be Equal As Strings      '${NAVIGATE_TO_EXTREME_GUEST_PAGE}'     '1'

    ${TOTAL_USER_WIDGET_DATA}=             check summary page total users widget data
    Should Be Equal As Strings      '${TOTAL_USER_WIDGET_DATA}'     '1'

    ${ONLINE_USER_WIDGET_DATA}=             check summary page online users widget data
    Should Be Equal As Strings      '${ONLINE_USER_WIDGET_DATA}'     '1'

    ${TOTAL_CLIENTS_WIDGET_DATA}=             check summary page total clients widget data
    Should Be Equal As Strings      '${TOTAL_CLIENTS_WIDGET_DATA}'     '1'

    Save Screen shot

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             Go back To XIQ

TCCS-13018: Online users by location widget
    [Documentation]        Online users by location widget

    [Tags]                  development    greenfield    brownfield    analytics    tccs_13018

    Depends On             TCCS-12993

    ${NAVIGATE_TO_EXTREME_GUEST_PAGE}=             go to extreme guest page
    Should Be Equal As Strings      '${NAVIGATE_TO_EXTREME_GUEST_PAGE}'     '1'

    ${WIDGET}=        Check Map Location Widget
    Should Be Equal As Strings      '${WIDGET}'     '1'

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             Go back To XIQ

TCCS-13004: Guest-Essentials -Summary-Visitors widget
    [Documentation]         Check Summary Visitors Widget

    [Tags]                  development    greenfield    brownfield    analytics    tccs_13004

    Depends On              TCCS-12993

    ${NAVIGATE_TO_EXTREME_GUEST_PAGE}=             go to extreme guest page
    Should Be Equal As Strings      '${NAVIGATE_TO_EXTREME_GUEST_PAGE}'     '1'

    ${CHECK_VISITOR_DATA}=             check summary page visitor widget data
    Should Be Equal As Strings      '${CHECK_VISITOR_DATA}'     '1'


    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             Go back To XIQ

TCCS-13005: Guest-Essentials -Summary-New Users Widget
    [Documentation]         Check Summary New users Widget

    [Tags]                  development    greenfield    brownfield    analytics    tccs_13005

    Depends On              TCCS-12993

    ${NAVIGATE_TO_EXTREME_GUEST_PAGE}=             go to extreme guest page
    Should Be Equal As Strings      '${NAVIGATE_TO_EXTREME_GUEST_PAGE}'     '1'

    ${CHECK_USER_WIDGET_DATA}=             check summary page new user widget data
    Should Be Equal As Strings      '${CHECK_USER_WIDGET_DATA}'     '1'

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             Go back To XIQ

TCCS-13006: Guest-Essentials -Summary-Conversion Widget
    [Documentation]         Check Summary Conversion Widget

    [Tags]                  development    greenfield    brownfield    analytics    tccs_13006

    Depends On              TCCS-12993

    ${NAVIGATE_TO_EXTREME_GUEST_PAGE}=             go to extreme guest page
    Should Be Equal As Strings      '${NAVIGATE_TO_EXTREME_GUEST_PAGE}'     '1'

    ${CHECK_SUMMARY_PAGE}=             check summary page conversion widget data
    Should Be Equal As Strings      '${CHECK_SUMMARY_PAGE}'     '1'

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             Go back To XIQ

TCCS-13007: Guest-Essentials -Summary-Gender distribution widget

    [Documentation]         Check Summary Gender Widget

    [Tags]                  development    greenfield    brownfield    analytics    tccs_13007

    Depends On              TCCS-12993

    ${NAVIGATE_TO_EXTREME_GUEST_PAGE}=             go to extreme guest page
    Should Be Equal As Strings      '${NAVIGATE_TO_EXTREME_GUEST_PAGE}'     '1'

    ${CHECK_SUMMARY_PAGE}=             check summary page gender widget data
    Should Be Equal As Strings      '${CHECK_SUMMARY_PAGE}'     '1'

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             Go back To XIQ

TCCS-13017: Adding Dashboards

    [Documentation]         Create Extreme Guest Dashboard

    [Tags]                  development    greenfield    dashboard    tccs_13017

    Depends On              TCCS-12993

    ${NAVIGATE_TO_EXTREME_GUEST_PAGE}=             go to extreme guest page
    Should Be Equal As Strings      '${NAVIGATE_TO_EXTREME_GUEST_PAGE}'     '1'

    ${NAVIGATE_TO_EXTREME_GUEST_DASHBOARD_PAGE}=             go to extreme guest dashboard page
    Should Be Equal As Strings      '${NAVIGATE_TO_EXTREME_GUEST_DASHBOARD_PAGE}'     '1'

    ${CREATE_EXTREME_GUEST_DASHBOARD_PAGE}=             create new extreme guest dashboard    dashboard_name=${DASHBOARD_NAME1}
    Should Be Equal As Strings      '${CREATE_EXTREME_GUEST_DASHBOARD_PAGE}'     '1'
    Save Screen shot

    ${CHECK_DASHBOARD_PAGE}=             check dashboard page widgets
    Should Be Equal As Strings      '${CHECK_DASHBOARD_PAGE}'     '1'
    Save Screen shot

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             Go back To XIQ

TCCS-13021: Adding of reports [Dashboard Report-PDF]

    [Documentation]         Create Dashboard Report

    [Tags]                  development    greenfield    reports    tccs_13021

    Depends On              TCCS-12993    TCCS-13017

    ${CREATE_REPORT}=         create extreme guest report  ${REPORT_NAME1}    ${REPORT_TYPE2}     ${REPORT_FORMAT1}       ${SAVE_TYPE3}       dashboard_name=${DASHBOARD_NAME1}
    save screen shot
    Should Be Equal As Strings      '${CREATE_REPORT}'     '1'

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             Go back To XIQ

TCCS-13016: Guest Management Role - Adding users

    [Documentation]         Create Guest Management Role and Create Vouchers

    [Tags]                  development    greenfield    guest_management_role    tccs_13016

    ${CREATE_ACCOUNT}=              Create Role Based Account   ${GUEST_MANAGEMENT_ROLE}
    should be equal as strings      '${CREATE_ACCOUNT}'    '1'

    ${LOGOUT_USER}=              Logout User

    ${URL}=                 Get Url To Set Password For New User        ${USER_EMAIL}      ${USER_PASSWORD}
    ${DRIVER}=              Load Web Page      url=${URL}

    ${SET_PASSWORD}=             Set Password       ${TENANT_PASSWORD}
    should be equal as strings      '${CREATE_ACCOUNT}'    '1'

    ${LOGOUT_USER}=              Logout User
    ${QUIT_BROWSER}=              Quit Browser       ${DRIVER}

    ${LOGIN_XIQ}=             Login User          ${USER_EMAIL}      ${TENANT_PASSWORD}      url=${TEST_URL}    ignore_map=True
    should be equal as strings      '${LOGIN_XIQ}'    '1'

    ${NAVIGATE_TO_CONFIGURE_USERS_PAGE}=              Navigate To Configure Guest Essentials Users
    should be equal as strings      '${NAVIGATE_TO_CONFIGURE_USERS_PAGE}'    '1'

    ${USER_COUNT1}=    Get Extreme Guest Users Count
    Log to Console     Number of Guest Users: ${USER_COUNT1}

    ${CREATE_BULK_VOUCHERS}=              Create Guest Management Role Bulk Vouchers            ${NO_OF_VOUCHERS}    access_group=${ACCESS_GROUP}    location_name=${LOCATION_TREE}
    should be equal as strings      '${CREATE_BULK_VOUCHERS}'    '1'

    ${USER_COUNT2}=    Get Extreme Guest Users Count
    Log to Console     Number of Guest Users: ${USER_COUNT2}

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

TCCS-13022: Reset VIQ

    [Documentation]         Reset Customer Account Data

    [Tags]                  development    greenfield    reset    tccs_13022

    #Step1: Perform BackUp VIQ
    ${LOGIN_XIQ}=                   Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}      url=${TEST_URL}
    Should Be Equal As Strings      '${LOGIN_XIQ}'     '1'

    ${BACKUP_VIQ_DATA}=             Backup VIQ Data
    Should Be Equal As Strings      '${BACKUP_VIQ_DATA}'              '1'

    ${QUIT_BROWSER}=                   Quit Browser

    Sleep  30 seconds

    #Step2: Perform Reset VIQ
    ${LOGIN_XIQ}=                   Login User          ${TENANT_USERNAME}      ${TENANT_PASSWORD}      url=${TEST_URL}
    Should Be Equal As Strings      '${LOGIN_XIQ}'     '1'

    ${DELETE_ACCOUNT}=                   Delete Guest Management Accounts
    Should Be Equal As Strings      '${DELETE_ACCOUNT}'     '1'

    ${RESET_VIQ_DATA}=               Reset VIQ Data

    Should Be Equal As Strings      '${RESET_VIQ_DATA}'              '1'

    ${QUIT_BROWSER}=                   Quit Browser

    #Step3: Verify Reset
    Sleep  30 seconds

    ${LOGIN_XIQ}=                       Login User          ${TENANT_USERNAME}     ${TENANT_PASSWORD}   url=${TEST_URL}    map_override=${MAP_FILE_NAME}

    Should Be Equal As Strings      '${LOGIN_XIQ}'     '1'

    ${GUEST_SUBSCRPTION_PAGE}=          Check Guest Subscription
    Should Be Equal As Strings      '${GUEST_SUBSCRPTION_PAGE}'              '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

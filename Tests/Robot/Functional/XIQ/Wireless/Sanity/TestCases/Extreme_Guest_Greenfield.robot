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

*** Variables ***
#${WEB_DRIVER_LOC}           local
${TESTBED}          BANGALORE/Dev/guest_blr_tb_1/testbed_1.yaml
${TOPO}             Extreme_Guest/topo.aanand.g2r1.yaml
${ENV}              Extreme_Guest/environment.remote.chrome.windows.guest2.yaml

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
    ${result}=                      Login User          ${TENANT_USERNAME}     ${TENANT_PASSWORD}   url=${TEST_URL}
    ${IMPORT_MAP}=                Import Map In Network360Plan  ${MAP_FILE_NAME}
    Should Be Equal As Strings    ${IMPORT_MAP}       1
    change device password          ${ap1.password}
    Onboard AP          ${ap1.serial}       ${ap1.make}        ${LOCATION_TREE}
    ${AP_SPAWN}=        Open Spawn          ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
    Set Suite Variable  ${AP_SPAWN}

    ${OUTPUT0}=         Send Commands       ${AP_SPAWN}         capwap client server name ${CAPWAP_URL}, capwap client default-server-name ${CAPWAP_URL}, capwap client server backup name ${CAPWAP_URL}, no capwap client enable, capwap client enable, save config
    Wait Until Device Online                ${ap1.serial}
    Refresh Devices Page
    ${AP1_STATUS}=                  Get AP Status       ap_mac=${ap1.mac}
    Should Be Equal As Strings      '${AP1_STATUS}'     'green'

    delete network polices          ${NW_POLICY_NAME0} ${NW_POLICY_NAME1} ${NW_POLICY_NAME2} ${NW_POLICY_NAME3}
    delete ssids                    ${SSID_NAME0} ${SSID_NAME1} ${SSID_NAME2} ${SSID_NAME3} ${SSID_NAME4}

    Run Keyword            Modify Suite Variables

    [Teardown]    go back to xiq

AP Cleanup
    [Documentation]    Clean Clien details from AP
    ${AP_SPAWN}=        Open Spawn          ${ap1.ip}   ${ap1.port}      ${ap1.username}       ${ap1.password}        ${ap1.cli_type}
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

    ${CREATE_POLICY0}=              Create Network Policy   ${NW_POLICY_NAME0}      &{GUEST_OPEN_NW0}
    Should Be Equal As Strings      '${CREATE_POLICY0}'   '1'

    ${CREATE_POLICY1}=              Create Network Policy   ${NW_POLICY_NAME1}      &{GUEST_OPEN_NW1}
    Should Be Equal As Strings      '${CREATE_POLICY1}'   '1'

    ${CREATE_POLICY2}=              Create Network Policy   ${NW_POLICY_NAME2}      &{GUEST_OPEN_NW2}
    Should Be Equal As Strings      '${CREATE_POLICY2}'   '1'

    ${CREATE_POLICY3}=              Create Network Policy   ${NW_POLICY_NAME3}      &{GUEST_OPEN_NW3}
    Should Be Equal As Strings      '${CREATE_POLICY3}'   '1'

    ${CREATE_POLICY5}=              Create Network Policy   ${NW_POLICY_NAME5}      &{GUEST_OPEN_NW5}
    Should Be Equal As Strings      '${CREATE_POLICY5}'   '1'

    ${CREATE_POLICY6}=              Create Network Policy   ${NW_POLICY_NAME6}      &{GUEST_OPEN_NW6}
    Should Be Equal As Strings      '${CREATE_POLICY6}'   '1'

    ${CREATE_POLICY7}=              Create Network Policy   ${NW_POLICY_NAME7}      &{GUEST_OPEN_NW7}
    Should Be Equal As Strings      '${CREATE_POLICY7}'   '1'

*** Test Cases ***
 
TCCS-12991: Guest Essentials after XIQ login -subscribe-SSO
    [Documentation]         Launch Extreme Guest Subscription Page
    [Tags]                  development    greenfield    subscription    tccs-12991

    ${CREATE_SSID}=             create open ssid in common objects  ${SSID_NAME4}
    Should Be Equal As Strings      '${CREATE_SSID}'     '1'

    ${CHECK_CREATED_SSID}=             check created ssid table  ${SSID_NAME4}
    Should Be Equal As Strings      '${CHECK_CREATED_SSID}'     '1'
    save screen shot

    [Teardown]   go back to xiq

TCCS-12993: Guest Essentials - Enable Adv Guest on existing networks
    
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

TCCS-13119: Clone Extreme Guest System Template
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
    save screen shot
    
    ${EG_POLICY_NAME_STATUS0}=             ADD ONBOARDING POLICY   policy_name=${EG_POLICY_NAME0}  group_name=${GROUP_NAME}    condition_type=${CONDITION_TYPE0}
    Should Be Equal As Strings      '${EG_POLICY_NAME_STATUS0}'     '1'

    ${EG_POLICY_NAME_STATUS1}=             ADD ONBOARDING POLICY   policy_name=${EG_POLICY_NAME1}  group_name=${GROUP_NAME}    condition_type=${CONDITION_TYPE1}
    Should Be Equal As Strings      '${EG_POLICY_NAME_STATUS1}'     '1'

    ${EG_POLICY_NAME_STATUS2}=             ADD ONBOARDING POLICY   policy_name=${EG_POLICY_NAME2}  group_name=${GROUP_NAME}    condition_type=${CONDITION_TYPE4}    condition_value=${CONDITION_VALUE}    action_type=${SEND_OTP_TO_USER}    user_notifpolicy=${DEFAULT_NOTIFICATION_POLICY1}    sponsor_notifpolicy=${DEFAULT_NOTIFICATION_POLICY2}
    Should Be Equal As Strings      '${EG_POLICY_NAME_STATUS2}'     '1'
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

    ${EG_RULE_NAME_6}=             ADD ONBOARDING RULE     rule_name=${EG_RULE_NAME6}  policy_name=${EG_POLICY_NAME0}  location_name=${LOCATION_TREE}    network_name=${SSID_NAME7}
    Should Be Equal As Strings      '${EG_RULE_NAME_6}'     '1'

    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             go back to xiq

TCCS-12997: Verify User can register to Cguest server and authenticate on CP with Facebook
    [Documentation]         Verify Facebook Social Login
    [Tags]                  development    greenfield    brownfield    social    facebook    tccs-12997
    Depends On              TCCS-12993    TCCS-13119
    
    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   ${NW_POLICY_NAME1}     ap_serial=${ap1.serial}   update_method=Complete
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${DEVICE_STATUS}=             Wait Until Device Online       ${ap1.serial}
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
    BuiltIn.Sleep                         ${CONFIG_PUSH_WAIT}

    ${CONNECT_CLIENT_OPEN_N/W}=             Remote_Server.Connect Open Network    ${SSID_NAME1}
    Should Be Equal As Strings      '${CONNECT_CLIENT_OPEN_N/W}'     '1'
    Log to Console      Sleep for ${CLIENT_CONNECT_WAIT}
    BuiltIn.Sleep                         ${CLIENT_CONNECT_WAIT}
    
    ${OPEN_GUEST_PORTAL}=             open guest portal browser    ${mu1.ip}
    Log to Console      Sleep for ${CP_PAGE_OPEN_WAIT}
    BuiltIn.Sleep  ${CP_PAGE_OPEN_WAIT}

    ${SOCIAL_AUTH_STATUS}=                 validate eguest social login with facebook     ${MAIL_ID3}      ${MAIL_ID3_PASS}
    Should Be Equal As Strings     '${SOCIAL_AUTH_STATUS}'  '1'
    
    get gp page screen shot

    ${WIFI_DISCONNECT}=             Remote_Server.Disconnect WiFi
    Should Be Equal As Strings      '${WIFI_DISCONNECT}'     '1'

    Log to Console      Sleep for ${CLIENT_DISCONNECT_WAIT}
    BuiltIn.Sleep  ${CLIENT_DISCONNECT_WAIT}

    ${NAVIGATE_TO_CONFIGURE_PAGE}=             go to configure users page
    Should Be Equal As Strings      '${NAVIGATE_TO_CONFIGURE_PAGE}'     '1'

    ${DELETE_USER_FB}=             delete user  facebook
    Should Be Equal As Strings      '${DELETE_USER_FB}'     '1'
    
    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             close gp browser
    ...                             AP Cleanup
    ...                             go back to xiq


TCCS-12998: Verify User can register to Cguest server and authenticate on CP with LinkedIn
    [Documentation]         Verify LnkedIn Social Login
    [Tags]                  development    greenfield    brownfield    social    linkedin    tccs-12998
    Depends On              TCCS-12993    TCCS-13119

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   ${NW_POLICY_NAME2}     ap_serial=${ap1.serial}
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${DEVICE_STATUS}=           Wait Until Device Online       ${ap1.serial}
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
    BuiltIn.Sleep                         ${CONFIG_PUSH_WAIT}

    ${CONNECT_CLIENT_OPEN_N/W}=             Remote_Server.Connect Open Network    ${SSID_NAME2}
    Log to Console      Sleep for ${CLIENT_CONNECT_WAIT}
    BuiltIn.Sleep                         ${CLIENT_CONNECT_WAIT}
    
    ${OPEN_GUEST_PORTAL}=             open guest portal browser    ${mu1.ip}
    Log to Console      Sleep for ${CP_PAGE_OPEN_WAIT}
    BuiltIn.Sleep  ${CP_PAGE_OPEN_WAIT}

    ${SOCIAL_AUTH_STATUS}=                 validate eguest social login with linkedin    ${MAIL_ID3}      ${MAIL_ID3_PASS}
    Should Be Equal As Strings      '${SOCIAL_AUTH_STATUS}'       '1'
    
    get gp page screen shot

    ${WIFI_DISCONNECT}=             Remote_Server.Disconnect WiFi
    Log to Console      Sleep for ${CLIENT_DISCONNECT_WAIT}
    BuiltIn.Sleep  ${CLIENT_DISCONNECT_WAIT}

    ${NAVIGATE_TO_CONFIGURE_PAGE}=             go to configure users page
    Should Be Equal As Strings      '${NAVIGATE_TO_CONFIGURE_PAGE}'       '1'
    
    ${DELETE_USER_LINKEDIN}=             delete user  linkedin
    Should Be Equal As Strings      '${DELETE_USER_LINKEDIN}'       '1'


    [Teardown]   run keywords       switch_to_extreme_guest_window
    ...                             close_extreme_guest_window
    ...                             close gp browser
    ...                             AP Cleanup
    ...                             go back to xiq

TCCS-13014: Verify template Accept_n_connect_w_terms_link
    [Documentation]         Verify default Captive portal Login
    
    [Tags]                  development    greenfield    brownfield    simple    tccs-13014

    ${CREATE_POLICY4}=              Create Network Policy   ${NW_POLICY_NAME4}      &{GUEST_OPEN_NW4}
    Should Be Equal As Strings      '${CREATE_POLICY4}'   '1'

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   ${NW_POLICY_NAME4}    ap_serial=${ap1.serial}
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${DEVICE_STATUS}=           Wait Until Device Online       ${ap1.serial}
    Should Be Equal As Strings      '${DEVICE_STATUS}'       '1'

    ${CONNECT_CLIENT_OPEN_N/W}=             Remote_Server.Connect Open Network    ${SSID_NAME4}
    Log to Console      Sleep for ${CLIENT_CONNECT_WAIT}
    BuiltIn.Sleep                         ${CLIENT_CONNECT_WAIT}
    
    ${OPEN_GUEST_PORTAL}=             open guest portal browser    ${mu1.ip}
    Log to Console      Sleep for ${CP_PAGE_OPEN_WAIT}
    BuiltIn.Sleep       ${CP_PAGE_OPEN_WAIT}

    ${USER_AUTH_STATUS}=                 validate eguest default template with no mapping
    Should Be Equal As Strings      '${USER_AUTH_STATUS}'       '1'

    get gp page screen shot

    ${WIFI_DISCONNECT}=             Remote_Server.Disconnect WiFi
    Log to Console      Sleep for ${CLIENT_DISCONNECT_WAIT}
    BuiltIn.Sleep       ${CLIENT_DISCONNECT_WAIT}

    [Teardown]   run keywords       close gp browser
    ...                             AP Cleanup
    ...                             go back to xiq


TCCS-12994: Device and OTP Registration - Verify User can register and authenticate on CP with OTP notified over email 
    [Documentation]         Verify Device Registration
    
    [Tags]                  development    greenfield    brownfield    dev_reg_email    tccs-12994

    Depends On              TCCS-12993    TCCS-13119

    ${AP1_UPDATE_CONFIG}=           Update Network Policy To AP   ${NW_POLICY_NAME5}     ap_serial=${ap1.serial}
    Should Be Equal As Strings      '${AP1_UPDATE_CONFIG}'       '1'

    ${DEVICE_STATUS}=           Wait Until Device Online       ${ap1.serial}

    ${NAVIGATE_TO_EXTREME_GUEST_PAGE}=             go to extreme guest page
    Should Be Equal As Strings      '${NAVIGATE_TO_EXTREME_GUEST_PAGE}'       '1'

    ${NAVIGATE_TO_CONFIGURE_PAGE}=             go to configure page
    Should Be Equal As Strings      '${NAVIGATE_TO_CONFIGURE_PAGE}'       '1'

    ${CONFIGURE_SPLASH_SYSTEM_TEMPLATE}=             go to configure splash system template tab
    Should Be Equal As Strings      '${CONFIGURE_SPLASH_SYSTEM_TEMPLATE}'       '1'

    ${APPLY_USER_TEMPLATE}=             apply network to user template  network_name=${SSID_NAME5}      template_name=${TEMPLATE3_NAME}     location=${LOCATION_TREE}
    Should Be Equal As Strings      '${APPLY_USER_TEMPLATE}'     '1'

    ${CONNECT_CLIENT_OPEN_N/W}=             Remote_Server.Connect Open Network    ${SSID_NAME5}
    Log to Console      Sleep for ${CLIENT_CONNECT_WAIT}
    BuiltIn.Sleep                         ${CLIENT_CONNECT_WAIT}
    
    ${OPEN_GUEST_PORTAL}=             Open Guest Portal Browser    ${mu1.ip}
    Log to Console      Sleep for ${CP_PAGE_OPEN_WAIT}
    BuiltIn.Sleep  ${CP_PAGE_OPEN_WAIT}

    ${REGISTRATION_STATUS}=                 Register Device for Guest Access    ${USER_NAME}    ${USER_EMAIL}
    get gp page screen shot
    Should Be Equal As Strings     '${REGISTRATION_STATUS}'  '1'

    ${ACCESS_STATUS}=    Validate Sponsored Guest Access    ${USER_EMAIL}    ${USER_PASSWORD}    ${SEND_OTP_TO_USER}
    get gp page screen shot
    Should Be Equal As Strings     '${ACCESS_STATUS}'  '1'

    ${WIFI_DISCONNECT}=             Remote_Server.Disconnect WiFi
    Log to Console      Sleep for ${CLIENT_DISCONNECT_WAIT}
    BuiltIn.Sleep  ${CLIENT_DISCONNECT_WAIT}

    ${NAVIGATE_TO_CONFIGURE_PAGE}=             Go to Configure Users Page
    ${DELETE_USER_EMAIL}=             Delete User  ${USER_EMAIL}
    

    [Teardown]   run keywords       close gp browser
    ...                             AP Cleanup
    ...                             go back to xiq
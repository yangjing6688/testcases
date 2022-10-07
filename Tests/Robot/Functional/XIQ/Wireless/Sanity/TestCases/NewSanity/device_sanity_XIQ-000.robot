
*** Variables ***
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04
################# Open Authentication network Profile for cloud captive web portal #####################################
&{OPEN_NW_1}                 ssid_name=test_social_login_fb           network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE1}
&{OPEN_NW_2}                 ssid_name=test_social_login_google       network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE2}
&{OPEN_NW_3}                 ssid_name=test_social_login_linkedin     network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE3}
&{OPEN_NW_4}                 ssid_name=test_social_login4             network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE4}
&{OPEN_NW_5}                 ssid_name=social_login_authlogs          network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE4}

&{BORADCAST_SSID_DEFAULT}=       WIFI0=Enable        WIFI1=Enable
&{BORADCAST_SSID_01}=            WIFI0=Enable        WIFI1=Enable
&{BORADCAST_SSID_02}=            WIFI0=Enable        WIFI1=Disable
&{BORADCAST_SSID_03}=            WIFI0=Disable       WIFI1=Enable

&{OPEN_AUTHENTICATION_PROFILE0}     auth_type=Open    cwp_profile=&{OPEN_CWP}
&{OPEN_AUTHENTICATION_PROFILE1}     auth_type=Open    cwp_profile=&{OPEN_CWP_1}
&{OPEN_AUTHENTICATION_PROFILE2}     auth_type=Open    cwp_profile=&{OPEN_CWP_2}
&{OPEN_AUTHENTICATION_PROFILE3}     auth_type=Open    cwp_profile=&{OPEN_CWP_3}
&{OPEN_AUTHENTICATION_PROFILE4}     auth_type=Open    cwp_profile=&{OPEN_CWP_4}


&{OPEN_CWP}        enable_cwp=Disable
&{OPEN_CWP_1}      enable_cwp=Enable   cloud_captive_web_portal=Enable  social_login=Enable   request_pin=Disable   open_cwp_config=&{OPEN_CWP_CONFIG_1}
&{OPEN_CWP_2}      enable_cwp=Enable   cloud_captive_web_portal=Enable  social_login=Enable   request_pin=Disable   open_cwp_config=&{OPEN_CWP_CONFIG_2}
&{OPEN_CWP_3}      enable_cwp=Enable   cloud_captive_web_portal=Enable  social_login=Enable   request_pin=Disable   open_cwp_config=&{OPEN_CWP_CONFIG_3}
&{OPEN_CWP_4}      enable_cwp=Enable   cloud_captive_web_portal=Enable  social_login=Enable   request_pin=Disable   open_cwp_config=&{OPEN_CWP_CONFIG_4}

&{OPEN_CWP_CONFIG_1}     social_cwp_config=&{SOCIAL_CWP_CONFIG_1}    cloud_cwp_name=cloudcwpsocialfacebook
&{OPEN_CWP_CONFIG_2}     social_cwp_config=&{SOCIAL_CWP_CONFIG_2}    cloud_cwp_name=cloudcwpsocialgoogle
&{OPEN_CWP_CONFIG_3}     social_cwp_config=&{SOCIAL_CWP_CONFIG_3}    cloud_cwp_name=cloudcwpsociallinkedin
&{OPEN_CWP_CONFIG_4}     social_cwp_config=&{SOCIAL_CWP_CONFIG_4}    cloud_cwp_name=cloudcwpsocialfacebook4

&{SOCIAL_CWP_CONFIG_1}    social_login_type=Facebook   restrict_access=default    auth_cache_duration=2
&{SOCIAL_CWP_CONFIG_2}    social_login_type=Google     restrict_access=default    auth_cache_duration=2
&{SOCIAL_CWP_CONFIG_3}    social_login_type=Linkedin   restrict_access=default    auth_cache_duration=2
&{SOCIAL_CWP_CONFIG_4}    social_login_type=Facebook   restrict_access=default    auth_cache_duration=2
&{SOCIAL_CWP_CONFIG_5}    social_login_type=Google     restrict_access=asjJ       auth_cache_duration=2
&{SOCIAL_CWP_CONFIG_6}    social_login_type=Linkedin   restrict_access=asjJ       auth_cache_duration=2


&{SOCIAL_CWP_TEMP_CONFIG}    cwp_name=cloudcwpsocialfacebook1   social_login_type_fb=Enable     social_login_type_google=Disable  social_login_type_linkedin=Disable    restrict_access=default    auth_cache_duration=1

##############################Enterprise Wireless Network Profile creation #############################################
&{WIRELESS_ENTERPRISE_NW1}    ssid_name=AutoEnterpriseradius          network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_1}
&{WIRELESS_ENTERPRISE_NW2}    ssid_name=AutoEnterprisegroup           network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_2}
&{WIRELESS_ENTERPRISE_NW3}    ssid_name=AutoEnterprisedot1x           network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_3}
&{WIRELESS_ENTERPRISE_NW4}    ssid_name=AutoEnterpriseacctlogs        network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_4}
&{WIRELESS_ENTERPRISE_NW5}    ssid_name=AutoEnterprisedot1x           network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_5}
&{WIRELESS_ENTERPRISE_NW6}    ssid_name=dot1xwpa3wronguser            network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_6}
&{WIRELESS_ENTERPRISE_NW7}    ssid_name=Autodot1xexternalradius       network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_7}
&{WIRELESS_ENTERPRISE_NW8}    ssid_name=externalradiuswronguser       network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_7}
&{WIRELESS_ENTERPRISE_NW9}    ssid_name=externalradiuswpa3            network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_8}
&{WIRELESS_ENTERPRISE_NW10}   ssid_name=AutoEnterprisedot1xwpa3       network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_5}
&{WIRELESS_ENTERPRISE_NW11}   ssid_name=externalradiuswpa3wronguser   network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_8}
&{WIRELESS_ENTERPRISE_NW12}   ssid_name=test_ap_radius_server         network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_9}
&{WIRELESS_ENTERPRISE_NW13}   ssid_name=test_ap_radius_server_wpa3    network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_8}

##################################
&{ENTERPRISE_AUTH_PROFILE_1}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_1}   cwp_profile=&{ENTERPRISE_CWP_2}  auth_settings_profile=&{AUTHENTICATION_SETTINGS1}   user_access_settings=None   additional_settings=None
&{ENTERPRISE_AUTH_PROFILE_2}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_1}   cwp_profile=&{ENTERPRISE_CWP_2}  auth_settings_profile=&{AUTHENTICATION_SETTINGS2}   user_access_settings=None   additional_settings=None
&{ENTERPRISE_AUTH_PROFILE_3}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_1}   cwp_profile=&{ENTERPRISE_CWP_1}  auth_settings_profile=&{AUTHENTICATION_SETTINGS3}   user_access_settings=None   additional_settings=None
&{ENTERPRISE_AUTH_PROFILE_4}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_1}   cwp_profile=&{ENTERPRISE_CWP_1}  auth_settings_profile=&{AUTHENTICATION_SETTINGS4}   user_access_settings=None   additional_settings=None
&{ENTERPRISE_AUTH_PROFILE_5}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_5}   cwp_profile=&{ENTERPRISE_CWP_1}  auth_settings_profile=&{AUTHENTICATION_SETTINGS3}   user_access_settings=None   additional_settings=None
&{ENTERPRISE_AUTH_PROFILE_6}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_5}   cwp_profile=&{ENTERPRISE_CWP_1}  auth_settings_profile=&{AUTHENTICATION_SETTINGS3}   user_access_settings=None   additional_settings=None
&{ENTERPRISE_AUTH_PROFILE_7}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_1}   cwp_profile=&{ENTERPRISE_CWP_1}  auth_settings_profile=&{AUTHENTICATION_SETTINGS5}   user_access_settings=None   additional_settings=None
&{ENTERPRISE_AUTH_PROFILE_8}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_5}   cwp_profile=&{ENTERPRISE_CWP_1}  auth_settings_profile=&{AUTHENTICATION_SETTINGS5}   user_access_settings=None   additional_settings=None
&{ENTERPRISE_AUTH_PROFILE_9}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_1}   cwp_profile=&{ENTERPRISE_CWP_1}  auth_settings_profile=&{AUTHENTICATION_SETTINGS6}   user_access_settings=None   additional_settings=None

################### Key and Encryption Method Options for eneterprise network
&{KEY_ENCRYPTION_1}   key_management=WPA2-802.1X    encryption_method=CCMP (AES)
&{KEY_ENCRYPTION_2}   key_management=WPA2-802.1X    encryption_method=TKIP

&{KEY_ENCRYPTION_3}   key_management=WPA-802.1X    encryption_method=CCMP (AES)
&{KEY_ENCRYPTION_4}   key_management=WPA-802.1X    encryption_method=TKIP

&{KEY_ENCRYPTION_4}   key_management=Auto (WPA or WPA2) 802.1X    encryption_method=Auto-TKIP or CCMP (AES)
&{KEY_ENCRYPTION_5}   key_management=WPA3-802.1X    encryption_method=None

################# Enterprise Captive Web Portal Profile
&{ENTERPRISE_CWP_1}   cwp=Disable
&{ENTERPRISE_CWP_2}   enable_cwp=Enable    cwp_name=enterprisecwp
&{ENTERPRISE_CWP_3}   enable_cwp=Enable    cwp_name=enterprisecwp
&{ENTERPRISE_CWP_3}   enable_cwp=Enable    different_cwp_per_clients=Enable


################### AUthentication configuration pofile
&{AUTHENTICATION_SETTINGS1}   auth_with_extcldiq_service=Disable   radius_server_group_config=&{RADIUS_SERVER_GROUP_CONFIG_1}
&{AUTHENTICATION_SETTINGS2}   auth_with_extcldiq_service=Enable    user_group=&{Enterprise_User_Group_Cfg3}

&{AUTHENTICATION_SETTINGS3}   auth_with_extcldiq_service=Enable    user_group_config=&{Enterprise_User_Group_Cfg1}
&{AUTHENTICATION_SETTINGS4}   auth_with_extcldiq_service=Enable    user_group=&{Enterprise_User_Group_Cfg2}
&{AUTHENTICATION_SETTINGS5}   auth_with_extcldiq_service=Disable   radius_server_group_config=&{RADIUS_SERVER_GROUP_CONFIG_1}
&{AUTHENTICATION_SETTINGS6}   auth_with_extcldiq_service=Disable   radius_server_group_config=&{RADIUS_SERVER_GROUP_CONFIG_3}

## User Group Config
&{Enterprise_User_Group_Cfg1}      group_name=AutoEnterprisedot1x     user_group_profile=None
&{Enterprise_User_Group_Cfg2}      group_name=AutoEnterpriseacctlogs     user_group_profile=None
&{Enterprise_User_Group_Cfg3}      group_name=AutoEnterprisegroup     user_group_profile=None

################ Creating Radius Server group profile
&{RADIUS_SERVER_GROUP_CONFIG_1}     radius_server_group_name=AutoRadiusGroup      radius_server_config=&{RADIUS_SERVER_CONFIG_1}
&{RADIUS_SERVER_GROUP_CONFIG_3}     radius_server_group_name=Testing_ap_radius    radius_server_config=&{RADIUS_SERVER_CONFIG_2}

############### Configuring the Extreneal Radius Server
&{RADIUS_SERVER_CONFIG_1}    radius_server_group_name=AutoRadiusGroup      radius_server_group_desc=Radius server group    server_type=EXTERNAL RADIUS SERVER          external_radius_server_config=&{EXTRENAL_RADIUS_SERVER_CONFIG_1}
&{RADIUS_SERVER_CONFIG_2}    radius_server_group_name=Testing_ap_radius    radius_server_group_desc=Radius server group    server_type=EXTREME NETWORKS RADIUS SERVER  extreme_radius_server_config=&{EXTREME_RADIUS_SERVER_CONFIG_2}

############## Extrenal radius Server config variables
&{EXTRENAL_RADIUS_SERVER_CONFIG_1}   radius_server_name=AutoRadiusServer   ip_or_host_type=IP Address   radius_server_ip_host_name=FreeRadiusServer   radius_server_ip_address=10.234.106.231    shared_secret=Secret@123

## Extreme Network Radius Server Config variables
&{EXTREME_RADIUS_SERVER_CONFIG_2}   radius_server_name=AH-0f6a80   aaa_profile_name=Test_AAA_profile  user_db_type=Local Database  user_group=AutoEnterprisedot1x  radius_server_ip_host_name=APVlan20Network  host_ip_type_opt=IP Address    radius_server_ip_address=20.1.1.109   shared_secret=Secret@123

#################################################### Guest Access Network Configuration #############################################
## Unsecure Network
&{GUEST_ACCESS_NW1}        ssid_name=AutoGuestAccess1     network_type=GuestAccess    guest_auth_type=Unsecure   guest_auth_config=&{UNSECURE_GUEST_ACCESS_CONFIG1}
&{GUEST_ACCESS_NW2}        ssid_name=AutoGuestAccess2     network_type=GuestAccess    guest_auth_type=Unsecure   guest_auth_config=&{UNSECURE_GUEST_ACCESS_CONFIG2}
&{GUEST_ACCESS_NW3}        ssid_name=AutoGuestAccess3     network_type=GuestAccess    guest_auth_type=Unsecure   guest_auth_config=&{UNSECURE_GUEST_ACCESS_CONFIG3}

######Guests can access the network without logging in.
&{UNSECURE_GUEST_ACCESS_CONFIG1}      guest_access_nw_without_login=Enable

###### Guests accept the use policy before accessing the network.
&{UNSECURE_GUEST_ACCESS_CONFIG2}      guest_accept_user_policy_bf_access_nw=Enable     cwp_config=&{UNSECURE_CWP_CONFIG1}
&{UNSECURE_CWP_CONFIG1}               cwp_name=Accept    upa=Select

##### Guests can self-register, then sign in.
&{UNSECURE_GUEST_ACCESS_CONFIG3}      guest_self_register_sign_in=Enable   cwp_config=&{UNSECURE_CWP_CONFIG2}   user_groups=&{GROUP_CONFIG1}   empl_approval_domain=gmail.com

&{UNSECURE_CWP_CONFIG2}              cwp_name=selfcwp         landing_page=Select
&{GROUP_CONFIG1}                     group_name=GuestGroup    passwd_settings=&{GUEST_PASSWD_SETTING_CONFIG1}

&{GUEST_PASSWD_SETTING_CONFIG1}      letters=Enable   numbers=Enable   special_characters=Disable   enforce_use_of=Any selected character types    gen_passwd_len=10

############### Secure Network
&{GUEST_ACCESS_SECURE_NW1}        ssid_name=AutoGuestSecure1     network_type=GuestAccess    guest_auth_type=Secure   guest_auth_config=&{GUEST_ACCESS_SECURE_CONFIG1}
&{GUEST_ACCESS_SECURE_NW2}        ssid_name=AutoGuestSecure2     network_type=GuestAccess    guest_auth_type=Secure   guest_auth_config=&{GUEST_ACCESS_SECURE_CONFIG2}
&{GUEST_ACCESS_SECURE_NW3}        ssid_name=AutoGuestSecure3     network_type=GuestAccess    guest_auth_type=Secure   guest_auth_config=&{GUEST_ACCESS_SECURE_CONFIG3}

#################  Create credentials for guests to log in to your network.
&{GUEST_ACCESS_SECURE_CONFIG1}              create_guest_credentials_to_login=Enable      create_guest_credentials_to_login_config=&{GUEST_CREDENTIAL_TO_LOGIN_CONFIG1}

&{GUEST_CREDENTIAL_TO_LOGIN_CONFIG1}        max_num_clients_per_ppsk=Disable   mac_binding_num_per_ppsk=Disable    auth_db=Cloud    user_groups=&{SECURE_USER_GROUPS1}
&{SECURE_USER_GROUPS1}                      group_name=SecureGuestCred         guest_user_prefix=guest01_    num_guest=2

################## Guests can self-register, then sign in. As an option, an employee can approve.
&{GUEST_ACCESS_SECURE_CONFIG2}              guest_self_reg_signin=Enable        cwp_config=&{SECURE_CWP_CONFIG1}      guest_self_reg_ssid=AutoGuestOpen
...                                         max_num_clients_per_ppsk=Disable    user_groups=&{SECURE_USER_GROUPS2}    empl_approval_domain=gmail.com

&{SECURE_CWP_CONFIG1}                       cwp_name=SecureGuestSelf        landing_page=Select
&{SECURE_USER_GROUPS2}                      group_name=SelfRegGroup         passwd_settings=&{GUEST_SECURE_PASS_SETTING_CONFIG1}

&{GUEST_SECURE_PASS_SETTING_CONFIG1}        letters=Enable   numbers=Enable   special_characters=Disable    enforce_use_of=Any selected character types    gen_passwd_len=10

############## Create global password (PSK) credentials for your guests to log in to your network.
&{GUEST_ACCESS_SECURE_CONFIG3}             global_passwd_credentials_to_guests=Enable   enable_cwp=Enable    cwp_config=&{SECURE_CWP_CONFIG2}   password=ExtremExtreme@123
&{SECURE_CWP_CONFIG2}                      cwp_name=SecureGlobalCWP    upa=Select

############################ AP Template Config#################
&{AP_TEMPLATE_CONFIG}            wifi0_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_CONFIG_1_WIFI1}

&{AP_TEMPLATE_CONFIG_1_WIFI0}    client_access=Disable    backhaul_mesh_link=Disable   sensor=Enable

&{AP_TEMPLATE_CONFIG_1_WIFI1}    client_access=Disable    backhaul_mesh_link=Disable   sensor=Enable

#######WIPS Configuartion#######################

&{WIPS_CONFIG_OPTIONS}          rougue_ap_detection=Enable           detect_ap_wired=Enable                detect_ap_mac_oui_basis=Enable    detect_ap_ssid_basis=Disable
...                             detect_client_form_adhoc=Enable      rougue_client_reporting=Enable        mitigation_mode=manual

&{WIPS_CONFIG_OPTIONS1}         rougue_ap_detection=Enable           detect_ap_wired=Enable               detect_ap_mac_oui_basis=Disable   detect_ap_ssid_basis=Disable
...                             detect_client_form_adhoc=Disable     rougue_client_reporting=Disable      mitigation_mode=manual

&{WIPS_CONFIG_OPTIONS2}         rougue_ap_detection=Enable           detect_ap_wired=Enable               detect_ap_mac_oui_basis=Enable    detect_ap_ssid_basis=Disable
...                             detect_client_form_adhoc=Disable     rougue_client_reporting=Disable      mitigation_mode=manual

&{WIPS_CONFIG_OPTIONS3}         rougue_ap_detection=Enable           detect_ap_wired=Enable               detect_ap_mac_oui_basis=Disable   detect_ap_ssid_basis=Enable
...                             detect_client_form_adhoc=Disable     rougue_client_reporting=Disable      mitigation_mode=manual

####WIPS WLAN CONFIG####
&{WIPS_OPEN_NW_01}          ssid_name=Openwips_ssid_automation1                network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                         auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

&{WIPS_OPEN_NW_02}          ssid_name=Openwips_ssid_automation2                network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                         auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}


&{WIPS_OPEN_NW_03}          ssid_name=Openwips_ssid_automation3                network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}
...                         auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}


# Update this time because we have an ap that is taking a bit longer
${MAX_CONFIG_PUSH_TIME}             600

*** Settings ***
Library     Collections
Library     extauto/common/Utils.py
Library     extauto/common/Cli.py
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/manage/Devices.py
Library     extauto/xiq/flows/manage/Device360.py
Library     extauto/xiq/flows/manage/Switch.py
Library     extauto/xiq/flows/manage/Tools.py
Library     extauto/xiq/flows/configure/NetworkPolicy.py
Library     extauto/xiq/flows/globalsettings/GlobalSetting.py
Library     extauto/common/TestFlow.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py
Library     extauto/xiq/flows/manage/AdvanceOnboarding.py
Library     extauto/xiq/flows/manage/Alarms.py
Library     extauto/xiq/flows/manage/DeviceCliAccess.py
Library     ExtremeAutomation/Keywords/UserDefinedKeywords/NetworkElements/SetupTeardown/SetupTeardownUdks.py

Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/configure/AutoProvisioning.py
Library     extauto/xiq/flows/configure/CommonObjects.py
Library     extauto/xiq/flows/configure/ExpressNetworkPolicies.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Force Tags   testbed_1_node
Suite Setup     Test Suite Setup
Suite Teardown     Test Suite Teardown


*** Keywords ***
Test Suite Setup
    # Use this method to convert the ap, wing, netelem to a generic device object
    # ap1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    convert to generic device object   device  index=1

    # Create a random string with a known string, so we track if things are not cleaned up
    ${random_string}=               Get Random String
    ${PUSH_CONFIG_SSID_01}=     Catenate    PUSH_CONFIG_SSID_${random_string}
    ${PUSH_CONFIG_POLICY_01}=   Catenate    PUSH_CONFIG_POLICY_${random_string}
    ${NEW_SSID_NAME_1}=         Catenate    PUSH_CONFIG_NEW_${random_string}

    Set Global Variable          ${NEW_SSID_NAME_1}
    Set Global Variable          ${PUSH_CONFIG_SSID_01}
    Set Global Variable          ${PUSH_CONFIG_POLICY_01}

    &{CONFIG_PUSH_OPEN_NW_01}=   Create Dictionary   ssid_name=${PUSH_CONFIG_SSID_01}         network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}
    &{CONFIG_PUSH_OPEN_NW_02}=   Create Dictionary   ssid_name=${PUSH_CONFIG_POLICY_01}         network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

    Set Global Variable          &{CONFIG_PUSH_OPEN_NW_01}
    Set Global Variable          &{CONFIG_PUSH_OPEN_NW_02}


    # Create the connection to the device(s)
    Base Test Suite Setup
    Set Global Variable    ${MAIN_DEVICE_SPAWN}    ${device1.name}

    # downgrade the device if needed
    downgrade iqagent      ${device1.cli_type}  ${MAIN_DEVICE_SPAWN}

    # log in the user
    Login User      ${tenant_username}      ${tenant_password}

Test Suite Teardown
    Clean Up Device
    Delete Network Polices                  ${PUSH_CONFIG_POLICY_01}      ignore_cli_feedback=true
    Delete SSIDs                            ${PUSH_CONFIG_SSID_01}        ${NEW_SSID_NAME_1}     ignore_cli_feedback=true
    Logout User
    Quit Browser
    Base Test Suite Cleanup

Clean Up Device
    ${search_result}=   Search Device       device_serial=${device1.serial}    ignore_cli_feedback=true
    # Disconnect from Extreme Cloud IQ
    Run Keyword If  '${search_result}' == '1'       Delete and Disconnect Device From Cloud

Delete and Disconnect Device From Cloud
    delete device   device_serial=${device1.serial}
    disconnect device from cloud     ${device1.cli_type}     ${MAIN_DEVICE_SPAWN}

Disable SSH and Close Device360 Window
    ${DISABLE_SSH}=                     Device360 Disable SSH Connectivity   ${device1.mac}
    Should Be Equal As Integers         ${DISABLE_SSH}     1

    ${CLOSE_DEVICE360_WINDOW}=          Close Device360 Window
    Should Be Equal As Integers         ${CLOSE_DEVICE360_WINDOW}     1

Validate Device Information
    @{column_list}=    Create List    MGT IP ADDRESS    MAC
    ${DEVICE_INFOMATION}=   get_device_column_information  ${device1.serial}    ${column_list}
    Run Keyword If  '${device1.cli_type}' != 'WING-AP'    Validate Device Managment IP Information   ${DEVICE_INFOMATION}
    ${DEVICE_MAC}=                 Get From Dictionary      ${DEVICE_INFOMATION}    MAC
    Should Be Equal As Strings    '${DEVICE_MAC}'           '${device1.mac}'

Validate Device Managment IP Information
    [Arguments]    ${DEVICE_INFOMATION}
    ${DEVICE_IP}=                  Get From Dictionary      ${DEVICE_INFOMATION}    MGT_IP_ADDRESS
    Should Be Equal As Strings    '${DEVICE_IP}'           '${device1.ip}'

clean up auto provisioning
    ${DLT_ALL_AUTOPROV_POLICIES}=       Delete All Auto Provision Policies
    should be equal as integers         ${DLT_ALL_AUTOPROV_POLICIES}               1

    ${DLT_NW_POLICIES}=             Delete Network Polices                  ${POLICY_NAME_01}           ${POLICY_NAME_02}
    should be equal as integers     ${DLT_NW_POLICIES}          1

    ${DELETE_SSIDS}=                Delete SSIDs                            ${SSID_NAME_01}             ${SSID_NAME_02}
    should be equal as integers     ${DELETE_SSIDS}             1

*** Test Cases ***
step1: ssh_test
    [Documentation]     Log into Device

    [Tags]              onboard        development

    ${SPAWN}=        Open Spawn          ${device1.ip}   ${device1.port}      ${device1.username}       ${device1.password}        ${device1.cli_type}
    Close Spawn      ${SPAWN}

step2: Advanced Onboard Device on XIQ
    [Documentation]         Checks for Advanced Device onboarding on XIQ

    [Tags]                  onboard      development

    Depends On              step1

    Clean Up Device

    ${ONBOARD_RESULT}=      Advance Onboard Device         ${device1.serial}    device_make=${device1.make}   dev_location=${LOCATION}  device_mac=${device1.mac}
    Should Be Equal As Strings                  ${ONBOARD_RESULT}       1

    configure device to connect to cloud    ${device1.cli_type}    ${generic_capwap_url}  ${MAIN_DEVICE_SPAWN}

    ${ONLINE_STATUS_RESULT}=    wait until device online     ${device1.serial}
    Should Be Equal As Strings                  ${ONLINE_STATUS_RESULT}       1

    ${MANAGED_STATUS_RESULT}=   wait until device managed   ${device1.serial}
    Should Be Equal As Strings                  ${MANAGED_STATUS_RESULT}      1

    ${DEVICE_STATUS_RESULT}=    get device status      ${device1.serial}
    Should Be Equal As Strings                  ${DEVICE_STATUS_RESULT}      green


step3: Verify Information on Device page (Advanced onboarding)
    [Documentation]         Verify Information on Device page

    [Tags]                  onboard     development

    Depends On              step2
    Validate Device Information

Step4: Simple Onboard Device on XIQ
    [Documentation]         Checks for Device onboarding on XIQ

    [Tags]                  onboard      development   onboard-fast

    Depends On              step3

    Clean Up Device

    ${ONBOARD_RESULT}=          onboard device      ${device1.serial}       ${device1.make}   device_mac=${device1.mac}  location=${LOCATION}
    Should Be Equal As Strings                  ${ONBOARD_RESULT}       1

    configure device to connect to cloud    ${device1.cli_type}   ${generic_capwap_url}   ${MAIN_DEVICE_SPAWN}

    ${ONLINE_STATUS_RESULT}=    wait until device online     ${device1.serial}
    Should Be Equal As Strings                  ${ONLINE_STATUS_RESULT}       1

    ${MANAGED_STATUS_RESULT}=   wait until device managed   ${device1.serial}
    Should Be Equal As Strings                  ${MANAGED_STATUS_RESULT}      1

    ${DEVICE_STATUS_RESULT}=    get device status      ${device1.serial}
    Should Be Equal As Strings                  ${DEVICE_STATUS_RESULT}      green

step5: Verify Information on Device page (Simple onboaring)
    [Documentation]         Verify Information on Device page

    [Tags]                  onboard      development

    Depends On              step4
    Validate Device Information

# Waiting for the page to be refreshed in XIQ, this will only support AH-AP Only
# and will need to be expanded for all other device.
#Step6: Generate And Validate Fake Alarms (AH-AP Only)
#    [Documentation]    Chek the generation of alarms
#
#    [Tags]             verify_alarms    development
#
#    Depends On         step5
#
#    # FIXME Need to increase Support for all Devices
#    # Check to see if this test is supported on the device type
#    @{supported_cli_types}=    Create List   AH-AP
#    check_cli_type_and_skip     ${supported_cli_types}     ${device1.cli_type}
#
#    ${DEVICE_STATUS}=                   Get Device Status       device_mac=${device1.mac}
#    Should contain any                  ${DEVICE_STATUS}    green     config audit mismatch
#
#    ${CLEAR_ALARM_STATUS}=              Clear Alarm                       CRITICAL
#
#    ${SEND_CMD_STATUS}=                 Send Cmd On Device Advanced Cli    device_serial=${device1.serial}    cmd=_test trap-case alert failure
#    Should Not Be Equal As Strings      ${SEND_CMD_STATUS}          '-1'
#    sleep                               120s
#    ${ALARM_DETAILS}=                   Get Alarm Details                  CRITICAL
#    should be equal as strings          '${ALARM_DETAILS}[severity]'       'CRITICAL'
#    should be equal as strings          '${ALARM_DETAILS}[category]'       'System'
#    should be equal as strings          '${ALARM_DETAILS}[description]'    'fan failure.'
#    should be equal as strings          '${ALARM_DETAILS}[deviceMac]'      '${device1.mac}'


Step7: Enable SSH on Switch and Confirm Only a Single SSH Session Can Be Established
    [Documentation]     Enable SSH on Switch and Confirm Only a Single SSH Session Can Be Established

    [Tags]              ssh      development

    Depends On           step5

    # make sure the feature is enabled
    enable ssh availability

    # Create the SSH connection
    &{ip_port_info}=                    Device360 Enable SSH CLI Connectivity   ${device1.mac}  run_time=30
    ${ip}=                              Get From Dictionary  ${ip_port_info}  ip
    ${port}=                            Get From Dictionary  ${ip_port_info}  port

    Should not be Empty     ${ip}
    Should not be Empty     ${port}
    # SSH to the connection
    ${ssh_spawn}=                       Open Spawn    ${ip}  ${port}  ${device1.username}  ${device1.password}  ${device1.cli_type}  pxssh=True
    # Close the connection
    ${close_result}=                    Close Spawn   ${ssh_spawn}  pxssh=True
    # Try to ssh again ( this should fail )
    ${ssh_spawn}=                       Open Spawn    ${ip}  ${port}  ${device1.username}  ${device1.password}  ${device1.cli_type}  pxssh=True  expect_error=true

    [Teardown]  Disable SSH and Close Device360 Window


Step8: Verification of config push complete config update (AH-AP Only)
    [Documentation]             Verification of config push complete config update
    [Tags]                      push_config     development
    Depends On                  step5

    @{supported_cli_types}=    Create List   AH-AP
    check_cli_type_and_skip     ${supported_cli_types}     ${device1.cli_type}

    Set To Dictionary           ${CONFIG_PUSH_OPEN_NW_01}    ssid_name=${PUSH_CONFIG_SSID_01}
    Log to Console              ${CONFIG_PUSH_OPEN_NW_01}

    ${CREATE_NW_POLICY_STATUS}=     Create Network Policy   policy=${PUSH_CONFIG_POLICY_01}      &{CONFIG_PUSH_OPEN_NW_01}
    should be equal as integers     ${CREATE_NW_POLICY_STATUS}               1

    ${DEPLOY_STATUS}=               Deploy Network Policy with Complete Update      ${PUSH_CONFIG_POLICY_01}          ${device1.serial}
    should be equal as integers     ${DEPLOY_STATUS}               1

    ${CONNECTED_STATUS}=            Wait Until Device Online                ${device1.serial}   None   30   20
    Should Be Equal as Integers     ${CONNECTED_STATUS}          1

    ${OUTPUT1}=             Send           ${MAIN_DEVICE_SPAWN}                show ssid
    Should Contain                          ${OUTPUT1}                  ${PUSH_CONFIG_SSID_01}


Step9: Verification of config push delta update (AH-AP Only)
    [Documentation]         Verification of config push delta update
    [Tags]                  push_config     development
    Depends On              step5

    @{supported_cli_types}=    Create List   AH-AP
    check_cli_type_and_skip     ${supported_cli_types}     ${device1.cli_type}

    ${EDIT_STATUS}=                 Edit Network Policy SSID                    ${PUSH_CONFIG_POLICY_01}          ${PUSH_CONFIG_SSID_01}     ${NEW_SSID_NAME_1}
    should be equal as integers             ${EDIT_STATUS}              1

    ${DEPLOY_STATUS}=       Deploy Network Policy with Delta Update     ${PUSH_CONFIG_POLICY_01}          ${device1.serial}
    should be equal as integers             ${DEPLOY_STATUS}            1

    ${CONNECTED_STATUS}=    Wait Until Device Online                ${device1.serial}
    Should Be Equal as Integers             ${CONNECTED_STATUS}          1

    ${OUTPUT1}=             Send            ${MAIN_DEVICE_SPAWN}              show ssid
    Should Contain                          ${OUTPUT1}                  ${NEW_SSID_NAME_1}

# Not sure if this should be a part of Sanity
# yes, froce the upgrade
#
#Step11: Firmware upgrade to lastest version (AH-AP Only)
#    [Documentation]         Verify IQ engine upgrade to lastest version ( we should just make sure it was upgraded )
#    [Tags]			        push_config     development
#    Depends On             step1
#
#    @{supported_cli_types}=    Create List   AH-AP
#    check_cli_type_and_skip     ${supported_cli_types}     ${device1.cli_type}
#
#    ${SPAWN1}=              Open Spawn      ${device1.ip}   ${device1.port}      ${device1.username}       ${device1.password}        ${device1.cli_type}
#
#    ${CLOCK_OUPUT1}=        Send            ${SPAWN1}         show clock
#    ${REBOOT_OUPUT1}=       Send            ${SPAWN1}         show reboot schedule
#    Should Not Contain      ${REBOOT_OUPUT1}     Next reboot Scheduled
#
#    ${VERSION_DETAIL1}=     Send            ${SPAWN1}         show version detail
#
#    Should Contain          ${VERSION_DETAIL1}   Running image:      Current version
#    Should Contain          ${VERSION_DETAIL1}   Backup version:     HiveOS 10.0r3
#    Should Contain          ${VERSION_DETAIL1}   Load after reboot:  Current version
#
#    ${AP_BUILD_VERSION1}=   Get AP Version              ${SPAWN1}
#
#    ${LATEST_VERSION}=      Upgrade Device To Latest Version            ${device1.serial}
#    Should Not be Empty     ${LATEST_VERSION}
#
#    Sleep                   ${ap_reboot_wait}
#
#    ${CONNECTED_STATUS}=    Wait Until Device Online                ${device1.serial}       retry_count=15
#    Should Be Equal as Integers             ${CONNECTED_STATUS}          1
#
#    ${REBOOT_STATUS}=    Wait Until Device Reboots               ${device1.serial}
#    Should Be Equal as Integers             ${REBOOT_STATUS}          1
#
#    Close Spawn             ${SPAWN1}
#
#    ${SPAWN2}=              Open Spawn      ${device1.ip}   ${device1.port}      ${device1.username}       ${device1.password}        ${device1.cli_type}
#    Should not be equal as Strings          '${SPAWN2}'        '-1'
#
#    ${CLOCK_OUPUT2}=        Send            ${SPAWN2}         show clock
#
#    ${REBOOT_OUPUT2}=       Send            ${SPAWN2}         show reboot schedule
#    Should Not Contain      ${REBOOT_OUPUT2}     Next reboot Scheduled
#
#    ${VERSION_DETAIL2}=     Send            ${SPAWN2}         show version detail
#
#    Should Contain          ${VERSION_DETAIL2}   Running image:      Current version
#    Should Contain          ${VERSION_DETAIL2}   Backup version:     HiveOS 10.0r3
#    Should Contain          ${VERSION_DETAIL2}   Load after reboot:  Current version
#    Should Contain          ${VERSION_DETAIL2}   Uptime:             0 weeks, 0 days, 0 hours
#
#    ${AP_BUILD_VERSION2}=   Get AP Version              ${SPAWN2}
#    Should Be Equal As Strings  ${LATEST_VERSION}           ${AP_BUILD_VERSION2}
#
#    Close Spawn        ${SPAWN2}



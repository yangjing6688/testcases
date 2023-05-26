#####################################################################################################################
# Author        : Binh Nguyen
# Date          : May 15th 2023
# Description   : User-Auth using External Radius Server
#                   TCXM-43077  PAP Authentication Method       - User Auth + External Radius Server
#                   TCXM-43078  MS-CHAPv2 Authentication Method - User Auth + External Radius Server
#                 User-Auth and UPA using External Server
#                   TCXM-43081  PAP Authentication Method       - User Auth + UPA + External Radius Server
#                   TCXM-43082  CHAP Authentication Method      - User Auth + UPA + External Radius Server
#                   TCXM-43083  MS-CHAPv2 Authentication Method - User Auth + UPA + External Radius Server
#                 User-Auth using IDM Service
#                   TCXM-43079  PAP Authentication Method       - User Auth + User Groups
#                   TCXM-43080  MS-CHAPv2 Authentication Method - User Auth + User Groups
#                 User-Auth and Self-Registration using IDM Service
#                   TCXM-43086  PAP Authentication Method       - User Auth + Self-Registration + User Groups
#                   TCXM-43085  MS-CHAPv2 Authentication Method - User Auth + Self-Registration + User Groups
#####################################################################################################################
**** Variables ***
################## Policy Detail & Wireless Network ###############################
&{WIRELESS_OPEN_00}    ssid_name=w01_usr_pap_rad             network_type=Standard   ssid_profile=&{BORADCAST_SSID_00}   auth_profile=&{OPEN_AUTH_PROFILE_00}
&{WIRELESS_OPEN_01}    ssid_name=w01_usr_mschap_rad          network_type=Standard   ssid_profile=&{BORADCAST_SSID_00}   auth_profile=&{OPEN_AUTH_PROFILE_01}
&{WIRELESS_OPEN_02}    ssid_name=w01_usrupa_pap_rad          network_type=Standard   ssid_profile=&{BORADCAST_SSID_00}   auth_profile=&{OPEN_AUTH_PROFILE_02}
&{WIRELESS_OPEN_03}    ssid_name=w01_usrupa_chap_rad         network_type=Standard   ssid_profile=&{BORADCAST_SSID_00}   auth_profile=&{OPEN_AUTH_PROFILE_03}
&{WIRELESS_OPEN_04}    ssid_name=w01_usrupa_mschap_rad       network_type=Standard   ssid_profile=&{BORADCAST_SSID_00}   auth_profile=&{OPEN_AUTH_PROFILE_04}
&{WIRELESS_OPEN_05}    ssid_name=w01_usr_pap_usrgrp          network_type=Standard   ssid_profile=&{BORADCAST_SSID_00}   auth_profile=&{OPEN_AUTH_PROFILE_05}
&{WIRELESS_OPEN_06}    ssid_name=w01_usr_mschap_usrgrp       network_type=Standard   ssid_profile=&{BORADCAST_SSID_00}   auth_profile=&{OPEN_AUTH_PROFILE_06}
&{WIRELESS_OPEN_07}    ssid_name=w01_usrself_pap_usrgrp      network_type=Standard   ssid_profile=&{BORADCAST_SSID_00}   auth_profile=&{OPEN_AUTH_PROFILE_07}
&{WIRELESS_OPEN_08}    ssid_name=w01_usrself_mschap_usrgrp   network_type=Standard   ssid_profile=&{BORADCAST_SSID_00}   auth_profile=&{OPEN_AUTH_PROFILE_08}

&{BORADCAST_SSID_00}   WIFI0=Enable   WIFI1=Enable   WIFI2=Disable

&{OPEN_AUTH_PROFILE_00}   auth_type=Open   cwp_profile=&{OPEN_CWP_00}   auth_settings_profile=&{AUTHENTICATION_SETTINGS_00}
&{OPEN_AUTH_PROFILE_01}   auth_type=Open   cwp_profile=&{OPEN_CWP_01}   auth_settings_profile=&{AUTHENTICATION_SETTINGS_00}
&{OPEN_AUTH_PROFILE_02}   auth_type=Open   cwp_profile=&{OPEN_CWP_02}   auth_settings_profile=&{AUTHENTICATION_SETTINGS_00}
&{OPEN_AUTH_PROFILE_03}   auth_type=Open   cwp_profile=&{OPEN_CWP_03}   auth_settings_profile=&{AUTHENTICATION_SETTINGS_00}
&{OPEN_AUTH_PROFILE_04}   auth_type=Open   cwp_profile=&{OPEN_CWP_04}   auth_settings_profile=&{AUTHENTICATION_SETTINGS_00}
&{OPEN_AUTH_PROFILE_05}   auth_type=Open   cwp_profile=&{OPEN_CWP_05}   auth_settings_profile=&{AUTHENTICATION_SETTINGS_01}
&{OPEN_AUTH_PROFILE_06}   auth_type=Open   cwp_profile=&{OPEN_CWP_06}   auth_settings_profile=&{AUTHENTICATION_SETTINGS_01}
&{OPEN_AUTH_PROFILE_07}   auth_type=Open   cwp_profile=&{OPEN_CWP_07}   auth_settings_profile=&{AUTHENTICATION_SETTINGS_01}
&{OPEN_AUTH_PROFILE_08}   auth_type=Open   cwp_profile=&{OPEN_CWP_08}   auth_settings_profile=&{AUTHENTICATION_SETTINGS_01}

&{OPEN_CWP_00}   enable_cwp=Enable   captive_web_portal=Enable   user_auth_on_captive_web_portal=Enable   enable_self_reg=Disable   return_aerohive_private_psk=Disable   enable_upa=Disable   open_cwp_config=&{CWP_CONFIG_00}
&{OPEN_CWP_01}   enable_cwp=Enable   captive_web_portal=Enable   user_auth_on_captive_web_portal=Enable   enable_self_reg=Disable   return_aerohive_private_psk=Disable   enable_upa=Disable   open_cwp_config=&{CWP_CONFIG_01}
&{OPEN_CWP_02}   enable_cwp=Enable   captive_web_portal=Enable   user_auth_on_captive_web_portal=Enable   enable_self_reg=Disable   return_aerohive_private_psk=Disable   enable_upa=Enable    open_cwp_config=&{CWP_CONFIG_02}
&{OPEN_CWP_03}   enable_cwp=Enable   captive_web_portal=Enable   user_auth_on_captive_web_portal=Enable   enable_self_reg=Disable   return_aerohive_private_psk=Disable   enable_upa=Enable    open_cwp_config=&{CWP_CONFIG_03}
&{OPEN_CWP_04}   enable_cwp=Enable   captive_web_portal=Enable   user_auth_on_captive_web_portal=Enable   enable_self_reg=Disable   return_aerohive_private_psk=Disable   enable_upa=Enable    open_cwp_config=&{CWP_CONFIG_04}
&{OPEN_CWP_05}   enable_cwp=Enable   captive_web_portal=Enable   user_auth_on_captive_web_portal=Enable   enable_self_reg=Disable   return_aerohive_private_psk=Disable   enable_upa=Disable   open_cwp_config=&{CWP_CONFIG_05}    auth_with_extcldiq_service=Enable
&{OPEN_CWP_06}   enable_cwp=Enable   captive_web_portal=Enable   user_auth_on_captive_web_portal=Enable   enable_self_reg=Disable   return_aerohive_private_psk=Disable   enable_upa=Disable   open_cwp_config=&{CWP_CONFIG_06}    auth_with_extcldiq_service=Enable
&{OPEN_CWP_07}   enable_cwp=Enable   captive_web_portal=Enable   user_auth_on_captive_web_portal=Enable   enable_self_reg=Enable    return_aerohive_private_psk=Disable   enable_upa=Disable   open_cwp_config=&{CWP_CONFIG_07}    auth_with_extcldiq_service=Enable
&{OPEN_CWP_08}   enable_cwp=Enable   captive_web_portal=Enable   user_auth_on_captive_web_portal=Enable   enable_self_reg=Enable    return_aerohive_private_psk=Disable   enable_upa=Disable   open_cwp_config=&{CWP_CONFIG_08}    auth_with_extcldiq_service=Enable

&{CWP_CONFIG_00}   captive_web_portal_name=w01_open_usr_pap_rad             customize_and_preview=Enable   auth_method=PAP
&{CWP_CONFIG_01}   captive_web_portal_name=w01_open_usr_mschap_rad          customize_and_preview=Enable   auth_method=MS-CHAP V2
&{CWP_CONFIG_02}   captive_web_portal_name=w01_open_usrupa_pap_rad          customize_and_preview=Enable   auth_method=PAP
&{CWP_CONFIG_03}   captive_web_portal_name=w01_open_usrupa_chap_rad         customize_and_preview=Enable   auth_method=CHAP
&{CWP_CONFIG_04}   captive_web_portal_name=w01_open_usrupa_mschap_rad       customize_and_preview=Enable   auth_method=MS-CHAP V2
&{CWP_CONFIG_05}   captive_web_portal_name=w01_open_usr_pap_usrgrp          customize_and_preview=Enable   auth_method=PAP
&{CWP_CONFIG_06}   captive_web_portal_name=w01_open_usr_mschap_usrgrp       customize_and_preview=Enable   auth_method=MS-CHAP V2
&{CWP_CONFIG_07}   captive_web_portal_name=w01_open_usrself_pap_usrgrp      customize_and_preview=Enable   auth_method=PAP
&{CWP_CONFIG_08}   captive_web_portal_name=w01_open_usrself_mschap_usrgrp   customize_and_preview=Enable   auth_method=MS-CHAP V2

&{AUTHENTICATION_SETTINGS_00}   auth_with_extcldiq_service=Disable   radius_server_group_config=&{RADIUS_SERVER_GROUP_00}
&{AUTHENTICATION_SETTINGS_01}   auth_with_extcldiq_service=Enable    user_group_config=&{USER_GROUP_CFG_00}

########## Cloud Authentication User Groups Configure ###############
&{USER_GROUP_CFG_00}             group_name=cld_user_grp   user_group_profile=&{USER_GROUP_PROFILE_00}   db_loc=Cloud

&{USER_GROUP_PROFILE_00}         user_group_config=&{DB_LOC_CLOUD_RADIUS_DEFAULT}   passwd_settings=&{PASSWD_SETTING_00}   expiration_settings=None
...                              delivery_settings=None                             users_config=&{SINGLE_USER_INFO_00}

&{DB_LOC_CLOUD_RADIUS_DEFAULT}   pass_db_loc=Cloud  pass_type=radius  cwp_register=Disable

&{PASSWD_SETTING_00}             passwd_type=RADIUS   letters=Enable   numbers=Enable   special_characters=Disable   enforce_use_of=Any selected character types   gen_passwd_len=10

&{SINGLE_USER_INFO_00}           user-type=single   name=user4           organization=ExtremeNetworks        purpose_of_visit=guest
...                              email_address=cloud1tenant1@gmail.com   phone_number=+91 India-8971766359   user_name_type=Name   password=Aerohive123
...                              pass-generate=Disable                   description=single user username password verification    deliver_pass=cloud1tenant1@gmail.com

################ RADIUS Authentication Configure ###################
&{RADIUS_SERVER_GROUP_00}      radius_server_group_name=Rad_Server_Grp   radius_server_config=&{RADIUS_SERVER_00}

&{RADIUS_SERVER_00}            radius_server_group_desc=External Radius server group   server_type=EXTERNAL RADIUS SERVER   external_radius_server_config=&{EXTRENAL_RADIUS_SERVER_00}

&{EXTRENAL_RADIUS_SERVER_00}   radius_server_name=Rad_Sever_ip   ip_or_host_type=IP Address   radius_server_ip_host_name=Radius-IP   radius_server_ip_address=10.254.152.59   shared_secret=Symbol@123

&{RADIUS_AUTH_LOGIN}           name=user1   password=Aerohive123

#################### Device Templates ##############################
&{AP_TEMPLATE_1}         wifi0_configuration=&{AP_TEMPLATE_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_1_WIFI1}
&{AP_TEMPLATE_1_WIFI0}   radio_status=On     radio_profile=radio_ng_11ax-2g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_1_WIFI1}   radio_status=On     radio_profile=radio_ng_11ax-5g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable

############### Globle Variables ######################
${RETRY}      3

*** Settings ***
Library     String
Library     Collections
Library     DependencyLibrary

Library     common/Cli.py
Library     common/Utils.py
Library     common/tools/remote/WinMuConnect.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/common/MuCaptivePortal.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DevicesActions.py
Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/manage/DeviceCliAccess.py
Library     xiq/flows/mlinsights/MLInsightClient360.py

Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/DeviceTemplate.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Library	    Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   rem_mu

Force Tags       testbed_none
Suite Setup      Pre_condition
Suite Teardown   Post_condition

*** Test Cases ***
Step1: Create Policy
    [Documentation]     Create policy, select wifi0-1, and update policy to AP
    [Tags]              tcxm-43077   tcxm-43078   tcxm-43079   tcxm-43080   tcxm-43081   tcxm-43082   tcxm-43083   tcxm-43085   tcxm-43086   development   step1   steps

    Set Suite Variable             ${POLICY}                       open_cwp
    Set Suite Variable             ${AP_TEMP_NAME}                 ${ap1.model}_cwp

    ${STATUS}                      create network policy if does not exist   ${POLICY}   ${WIRELESS_OPEN_00}
    should be equal as strings     '${STATUS}'   '1'
    ${STATUS}                      create ssid to policy                     ${POLICY}   &{WIRELESS_OPEN_01}
    should be equal as strings     '${STATUS}'   '1'
    ${STATUS}                      create ssid to policy                     ${POLICY}   &{WIRELESS_OPEN_02}
    should be equal as strings     '${STATUS}'   '1'
    ${STATUS}                      create ssid to policy                     ${POLICY}   &{WIRELESS_OPEN_03}
    should be equal as strings     '${STATUS}'   '1'
    ${STATUS}                      create ssid to policy                     ${POLICY}   &{WIRELESS_OPEN_04}
    should be equal as strings     '${STATUS}'   '1'
    ${STATUS}                      create ssid to policy                     ${POLICY}   &{WIRELESS_OPEN_05}
    should be equal as strings     '${STATUS}'   '1'
    ${STATUS}                      create ssid to policy                     ${POLICY}   &{WIRELESS_OPEN_06}
    should be equal as strings     '${STATUS}'   '1'
    ${STATUS}                      create ssid to policy                     ${POLICY}   &{WIRELESS_OPEN_07}
    should be equal as strings     '${STATUS}'   '1'
    ${STATUS}                      create ssid to policy                     ${POLICY}   &{WIRELESS_OPEN_08}
    should be equal as strings     '${STATUS}'   '1'
    ${STATUS}                      add ap template from common object        ${ap1.model}       ${AP_TEMP_NAME}   ${AP_TEMPLATE_1}
    Should Be Equal As Strings     '${STATUS}'       '1'
    ${STATUS}                      add ap template to network policy         ${AP_TEMP_NAME}    ${POLICY}
    Should Be Equal As Strings     '${STATUS}'       '1'

Step2: Assign network policy to AP
    [Documentation]     Assign network policy to AP
    [Tags]              tcxm-43077   tcxm-43078   tcxm-43079   tcxm-43080   tcxm-43081   tcxm-43082   tcxm-43083   tcxm-43085   tcxm-43086   development   step2   steps

    Depends On Test     Step1: Create Policy
    ${UPDATE}                           Update Network Policy To Ap   ${POLICY}   ${ap1.serial}   Complete
    should be equal as strings          '${UPDATE}'                   '1'
    Wait_device_online                  ${ap1}
    Enable disable client Wifi device   ${mu1}


Step3: MU connect to wifi0-1 and Verify - CWP User PAP Radius
    [Documentation]     MU connect to wifi0-1 - CWP User PAP Radius
    [Tags]              tcxm-43077   development   step3   steps

    Depends On Test     Step2: Assign network policy to AP
    MU_connect_to_wifix         ${WIRELESS_OPEN_00}   ${RADIUS_AUTH_LOGIN}
    Verify_client360_to_wifix   ${WIRELESS_OPEN_00}   ${RADIUS_AUTH_LOGIN}

Step4: MU connect to wifi0-1 and Verify - CWP User MS-CHAP V2 Radius
    [Documentation]     MU connect to wifi0-1 - CWP User MS-CHAP V2 Radius
    [Tags]              tcxm-43078   development   step4   steps

    Depends On Test     Step2: Assign network policy to AP
    MU_connect_to_wifix         ${WIRELESS_OPEN_01}   ${RADIUS_AUTH_LOGIN}
    Verify_client360_to_wifix   ${WIRELESS_OPEN_01}   ${RADIUS_AUTH_LOGIN}


Step5: MU connect to wifi0-1 and Verify - CWP User-UPA PAP Radius
    [Documentation]     MU connect to wifi0-1 - CWP User-UPA PAP Radius
    [Tags]              tcxm-43081   development   step5   steps

    Depends On Test     Step2: Assign network policy to AP
    MU_connect_to_wifix         ${WIRELESS_OPEN_02}   ${RADIUS_AUTH_LOGIN}   ${1}
    Verify_client360_to_wifix   ${WIRELESS_OPEN_02}   ${RADIUS_AUTH_LOGIN}

Step6: MU connect to wifi0-1 and Verify - CWP User-UPA CHAP Radius
    [Documentation]     MU connect to wifi0-1 - CWP User-UPA CHAP Radius
    [Tags]              tcxm-43082   development   step6   steps

    Depends On Test     Step2: Assign network policy to AP
    MU_connect_to_wifix         ${WIRELESS_OPEN_03}   ${RADIUS_AUTH_LOGIN}   ${1}
    Verify_client360_to_wifix   ${WIRELESS_OPEN_03}   ${RADIUS_AUTH_LOGIN}

Step7: MU connect to wifi0-1 and Verify - CWP User-UPA MS-CHAP V2 Radius
    [Documentation]     MU connect to wifi0-1 - CWP User-UPA MS-CHAP V2 Radius
    [Tags]              tcxm-43083   development   step7   steps

    Depends On Test     Step2: Assign network policy to AP
    MU_connect_to_wifix         ${WIRELESS_OPEN_04}   ${RADIUS_AUTH_LOGIN}   ${1}
    Verify_client360_to_wifix   ${WIRELESS_OPEN_04}   ${RADIUS_AUTH_LOGIN}


Step8: MU connect to wifi0-1 and Verify - CWP User PAP User-Groups
    [Documentation]     MU connect to wifi0-1 - CWP User PAP User-Groups
    [Tags]              tcxm-43079   development   step8   steps

    Depends On Test     Step2: Assign network policy to AP
    MU_connect_to_wifix         ${WIRELESS_OPEN_05}   ${SINGLE_USER_INFO_00}
    Verify_client360_to_wifix   ${WIRELESS_OPEN_05}   ${SINGLE_USER_INFO_00}

Step9: MU connect to wifi0-1 and Verify - CWP User MS-CHAP V2 User-Groups
    [Documentation]     MU connect to wifi0-1 - CWP User MS-CHAP V2 User-Groups
    [Tags]              tcxm-43080   development   step9   steps

    Depends On Test     Step2: Assign network policy to AP
    MU_connect_to_wifix         ${WIRELESS_OPEN_06}   ${SINGLE_USER_INFO_00}
    Verify_client360_to_wifix   ${WIRELESS_OPEN_06}   ${SINGLE_USER_INFO_00}


Step10: MU connect to wifi0-1 and Verify - CWP User-Self PAP User-Groups
    [Documentation]     MU connect to wifi0-1 - CWP User-Self PAP User-Groups
    [Tags]              tcxm-43086   development   step10   steps

    Depends On Test     Step2: Assign network policy to AP
    MU_connect_to_wifix         ${WIRELESS_OPEN_07}   ${SINGLE_USER_INFO_00}
    Verify_client360_to_wifix   ${WIRELESS_OPEN_07}   ${SINGLE_USER_INFO_00}

Step11: MU connect to wifi0-1 and Verify - CWP User-Self MS-CHAP V2 User-Groups
    [Documentation]     MU connect to wifi0-1 - CWP User-Self MS-CHAP V2 User-Groups
    [Tags]              tcxm-43085   development   step11   steps

    Depends On Test     Step2: Assign network policy to AP
    MU_connect_to_wifix         ${WIRELESS_OPEN_08}   ${SINGLE_USER_INFO_00}
    Verify_client360_to_wifix   ${WIRELESS_OPEN_08}   ${SINGLE_USER_INFO_00}

*** Keywords ***
Pre_condition
    ${STATUS}                        Login User   ${tenant_username}   ${tenant_password}
    should be equal as strings       '${STATUS}'   '1'
    reset devices to default
    log to console                   Wait for 2 minutes for completing reboot....
    sleep                            2m
    delete all devices
    delete all network policies
    delete all ssids
    delete all captive web portals   GA-UA-Self-Reg-CWP-Profile,GA-UPA-CWP-Profile
    delete all ap templates
    Delete All User Profiles
    Onboard_AP

Post_condition
    Logout User
    Quit Browser

Onboard_AP
    ${STATUS}       onboard device quick                            ${ap1}
    Should Be Equal As Strings                                      '${STATUS}'       '1'
    ${AP_SPAWN}     Open Spawn                                      ${ap1.ip}         ${ap1.port}      ${ap1.username}   ${ap1.password}   ${ap1.cli_type}
    ${STATUS}       Configure Device To Connect To Cloud            ${ap1.cli_type}   ${capwap_url}    ${AP_SPAWN}
    Should Be Equal As Strings                                      '${STATUS}'       '1'

    ${STATUS}       Wait for Configure Device to Connect to Cloud   ${ap1.cli_type}   ${capwap_url}    ${AP_SPAWN}
    Should Be Equal As Strings                                      '${STATUS}'       '1'
    Wait_device_online                                              ${ap1}
    [Teardown]      Close Spawn                                     ${AP_SPAWN}

Enable_disable_client_Wifi_device
    [Arguments]     ${mu}
    ${SPAWN}        Open Spawn    ${mu}[ip]     22    ${mu}[username]    ${mu}[password]    cli_type=MU-WINDOWS
    Send Commands   ${SPAWN}      pnputil /disable-device /deviceid \"PCI\\CC_0280\", pnputil /enable-device /deviceid \"PCI\\CC_0280\"
    [Teardown]      run keyword   Close Spawn   ${SPAWN}

Wait_device_online
    [Arguments]    ${ap}
    ${STATUS}                       Wait Until Device Online    ${ap}[serial]
    Should Be Equal As Strings      '${STATUS}'    '1'
    ${STATUS}                       Get Device Status           ${ap}[serial]
    ${STATUS}                       Run Keyword And Return Status    Should contain any    ${STATUS}    green    config audit mismatch
    IF    not ${STATUS}
        Wait Until Device Reboots       ${ap}[serial]
        ${STATUS}                       Wait Until Device Online    ${ap}[serial]    retry_count=60
        Should Be Equal As Strings      '${STATUS}'    '1'
        ${STATUS}                       Get Device Status           ${ap}[serial]
        Should contain any              ${STATUS}      green        config audit mismatch
    END

MU_connect_to_wifix
    [Arguments]     ${ssid}    ${login}    ${cwp_option}=${0}
    FOR   ${i}   IN RANGE   ${RETRY}
        ${STATUS}   rem_mu.connect open network   ${ssid}[ssid_name]
        exit for loop if   '${STATUS}'=='1'
    END
    should be equal as strings              '${STATUS}'           '1'
    open cp browser   ${mu1.ip}             http://198.18.36.1
    run keyword if    ${cwp_option}==${1}   accept user acceptance page
    ${STATUS}         Login Guest User      ${login}[name]       ${login}[password]
    should be equal as strings              '${STATUS}'           '1'
    close cp browser

Verify_client360_to_wifix
    [Arguments]     ${ssid}    ${login}
    ${OUT}           get client360 current connection status   ${mu1.wifi_mac}
    should contain   ${OUT['USER']}                            ${login}[name]
    should contain   ${OUT['CWP']}                             Used
    should contain   ${OUT['SSID']}                            ${ssid}[ssid_name]
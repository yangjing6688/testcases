#########################################################################################################
# Author        : Binh Nguyen
# Date          : Dec 22th 2022
# Description   : CFD-8698 : User Profile Assignment based on PPSK User Group
#                 TCHO-14022	 User Profile assignment based on User Group when Password DB location is LOCAL (AP)
#                 TCHO-14026	 User Profile assignment based on User Group when Password DB location is LOCAL (AP) and assignment rule is combined with OS type
#                 TCHO-14027	 User Profile assignment based on User Group when Password DB location is Cloud (IDM)
#                 TCHO-14028	 User Profile assignment based on User Group when Password DB location is Cloud (IDM) and assignment rule is combined with OS type
#########################################################################################################

**** Variables ***
################## Policy Detail & Wireless Network ###############################
&{WIRELESS_PPSK_00}     ssid_name=w0_1_loc_106_7    network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}     auth_profile=&{PPSK_AUTH_PROFILE_00}
&{WIRELESS_PPSK_01}     ssid_name=w0_1_loc_108_9    network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}     auth_profile=&{PPSK_AUTH_PROFILE_01}
&{WIRELESS_PPSK_02}     ssid_name=w0_1_cld_110_11   network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}     auth_profile=&{PPSK_AUTH_PROFILE_02}
&{WIRELESS_PPSK_03}     ssid_name=w0_1_cld_112_13   network_type=Standard    ssid_profile=&{BORADCAST_SSID_00}     auth_profile=&{PPSK_AUTH_PROFILE_03}

&{BORADCAST_SSID_00}       WIFI0=Enable     WIFI1=Enable      WIFI2=Disable
&{PPSK_AUTH_PROFILE_00}    auth_type=PPSK   key_encryption=&{PPSK_KEY_ENCRYPTION}   ppsk_config=&{PPSK_SETTING_DEFAULT}   cwp_config=&{PPSK_CWP_DEFAULT}   user_group_config=&{USER_GROUP_LOCAL_PROFILE}    user_access_settings_config=None   additional_settings_config=None
&{PPSK_AUTH_PROFILE_01}    auth_type=PPSK   key_encryption=&{PPSK_KEY_ENCRYPTION}   ppsk_config=&{PPSK_SETTING_DEFAULT}   cwp_config=&{PPSK_CWP_DEFAULT}   user_group_config=&{GUEST_GROUP_LOCAL_PROFILE}   user_access_settings_config=None   additional_settings_config=None
&{PPSK_AUTH_PROFILE_02}    auth_type=PPSK   key_encryption=&{PPSK_KEY_ENCRYPTION}   ppsk_config=&{PPSK_SETTING_DEFAULT}   cwp_config=&{PPSK_CWP_DEFAULT}   user_group_config=&{USER_GROUP_CLOUD_PROFILE}    user_access_settings_config=None   additional_settings_config=None
&{PPSK_AUTH_PROFILE_03}    auth_type=PPSK   key_encryption=&{PPSK_KEY_ENCRYPTION}   ppsk_config=&{PPSK_SETTING_DEFAULT}   cwp_config=&{PPSK_CWP_DEFAULT}   user_group_config=&{GUEST_GROUP_CLOUD_PROFILE}   user_access_settings_config=None   additional_settings_config=None

&{PPSK_KEY_ENCRYPTION}              key_management=WPA2-(WPA2 Personal)-PSK    encryption_method=CCMP (AES)
&{PPSK_SETTING_DEFAULT}             client_per_ppsk=Disable    mac_binding_num_per_ppsk=Disable   pcg_use=Disable   ppsk_classification=Disable
&{PPSK_CWP_DEFAULT}                 enable_cwp=Disable
&{USER_GROUP_LOCAL_PROFILE}         group_name=local_ppsk_user_group     user_group_profile=None     db_loc=Local
&{GUEST_GROUP_LOCAL_PROFILE}        group_name=local_ppsk_guest_group    user_group_profile=None     db_loc=Local
&{USER_GROUP_CLOUD_PROFILE}         group_name=cloud_ppsk_user_group     user_group_profile=None     db_loc=Cloud
&{GUEST_GROUP_CLOUD_PROFILE}        group_name=cloud_ppsk_guest_group    user_group_profile=None     db_loc=Cloud

&{USER_GROUP_CONFIG_LOCAL_ADD}      user_group_config=&{USER_GROUP_LOCAL_PROFILE}
&{GUEST_GROUP_CONFIG_LOCAL_ADD}     user_group_config=&{GUEST_GROUP_LOCAL_PROFILE}
&{USER_GROUP_CONFIG_CLOUD_ADD}      user_group_config=&{USER_GROUP_CLOUD_PROFILE}
&{GUEST_GROUP_CONFIG_CLOUD_ADD}     user_group_config=&{GUEST_GROUP_CLOUD_PROFILE}

&{USER_GROUP_PROFILE_LOCAL_MULTI}    user_group_config=&{DB_LOC_LOCAL_PPSK_DEFAULT}   passwd_settings=&{PASSWD_SETTING}    users_config=&{LOCAL_MULTI_USER_GROUP}     expiration_settings=None    delivery_settings=None
&{GUEST_GROUP_PROFILE_LOCAL_MULTI}   user_group_config=&{DB_LOC_LOCAL_PPSK_DEFAULT}   passwd_settings=&{PASSWD_SETTING}    users_config=&{LOCAL_MULTI_GUEST_GROUP}    expiration_settings=None    delivery_settings=None
&{USER_GROUP_PROFILE_CLOUD_MULTI}    user_group_config=&{DB_LOC_CLOUD_PPSK_DEFAULT}   passwd_settings=&{PASSWD_SETTING}    users_config=&{CLOUD_MULTI_USER_GROUP}     expiration_settings=None    delivery_settings=None
&{GUEST_GROUP_PROFILE_CLOUD_MULTI}   user_group_config=&{DB_LOC_CLOUD_PPSK_DEFAULT}   passwd_settings=&{PASSWD_SETTING}    users_config=&{CLOUD_MULTI_GUEST_GROUP}    expiration_settings=None    delivery_settings=None

&{DB_LOC_LOCAL_PPSK_DEFAULT}        pass_db_loc=LOCAL    pass_type=ppsk    client_per_ppsk=Disable   pcg_use=Disable  ppsk_classification=Disable
&{DB_LOC_CLOUD_PPSK_DEFAULT}        pass_db_loc=CLOUD    pass_type=ppsk    cwp_register=Disable      pcg_use=Disable
&{PASSWD_SETTING}                   letters=Enable       numbers=Enable    special_characters=Disable    enforce_use_of=Any selected character types    passwd_type=None    gen_passwd_len=10

${MAIL_ID}                    local3cloud3@gmail.com
&{LOCAL_MULTI_USER_GROUP}     user-type=multiple          name=loc_usr00 loc_usr01 loc_usr02               email_address=${MAIL_ID}    password=aerohive00 aerohive01 aerohive02
...                           pass-generate=Disable       description=Multi local user group username password verification
&{LOCAL_MULTI_GUEST_GROUP}    user-type=multiple          name=loc_gst_usr00 loc_gst_usr01 loc_gst_usr02   email_address=${MAIL_ID}    password=aerohive10 aerohive11 aerohive12
...                           pass-generate=Disable       description=Multi local guest group username password verification

&{CLOUD_MULTI_USER_GROUP}     user-type=multiple          name=cld_usr00 cld_usr01 cld_usr02                organization=ExtremeNetworks             purpose_of_visit=guest
...                           email_address=${MAIL_ID}    phone_number=+91 India-8971766359       user_name_type=Name    password=Aerohive00 Aerohive01 Aerohive02
...                           pass-generate=Disable       description=Multi cloud user group username password verification    deliver_pass=${MAIL_ID}
&{CLOUD_MULTI_GUEST_GROUP}    user-type=multiple          name=cld_gst_usr00 cld_gst_usr01 cld_gst_usr02    organization=ExtremeNetworks             purpose_of_visit=guest
...                           email_address=${MAIL_ID}    phone_number=+91 India-8971766359       user_name_type=Name    password=Aerohive10 Aerohive11 Aerohive12
...                           pass-generate=Disable       description=Multi cloud guest group username password verification    deliver_pass=${MAIL_ID}

&{USER_PROFILE_00}        profile_name=up_106       vlan_name=vlan_106    vlan_id=106    assignment_rule=&{LOCAL_PPSK_USR_GRP_RULE}
&{USER_PROFILE_01}        profile_name=up_107       vlan_name=vlan_107    vlan_id=107    assignment_rule=&{LOCAL_PPSK_GST_GRP_RULE}
&{USER_PROFILE_02}        profile_name=up_108       vlan_name=vlan_108    vlan_id=108    assignment_rule=&{LOCAL_PPSK_USR_GRP_OS_RULE}
&{USER_PROFILE_03}        profile_name=up_109       vlan_name=vlan_109    vlan_id=109    assignment_rule=&{LOCAL_PPSK_GST_GRP_OS_RULE}
&{USER_PROFILE_04}        profile_name=up_110       vlan_name=vlan_110    vlan_id=110    assignment_rule=&{CLOUD_PPSK_USR_GRP_RULE}
&{USER_PROFILE_05}        profile_name=up_111       vlan_name=vlan_111    vlan_id=111    assignment_rule=&{CLOUD_PPSK_GST_GRP_RULE}
&{USER_PROFILE_06}        profile_name=up_112       vlan_name=vlan_112    vlan_id=112    assignment_rule=&{CLOUD_PPSK_USR_GRP_OS_RULE}
&{USER_PROFILE_07}        profile_name=up_113       vlan_name=vlan_113    vlan_id=113    assignment_rule=&{CLOUD_PPSK_GST_GRP_OS_RULE}

&{LOCAL_PPSK_USR_GRP_RULE}       name=lc_ppsk_usr_grp_rule       description=lc_ppsk_usr_grp        add_rule=User Group                    user_group=${USER_GROUP_LOCAL_PROFILE}[group_name]
&{LOCAL_PPSK_GST_GRP_RULE}       name=lc_ppsk_gst_grp_rule       description=lc_ppsk_gst_grp        add_rule=User Group                    user_group=${GUEST_GROUP_LOCAL_PROFILE}[group_name]
&{LOCAL_PPSK_USR_GRP_OS_RULE}    name=lc_ppsk_usr_grp_os_rule    description=lc_ppsk_usr_grp_os     add_rule=User Group, Client OS Type    user_group=${USER_GROUP_LOCAL_PROFILE}[group_name]     os_type=Windows, Mac OS
&{LOCAL_PPSK_GST_GRP_OS_RULE}    name=lc_ppsk_gst_grp_os_rule    description=lc_ppsk_gst_grp_os     add_rule=User Group, Client OS Type    user_group=${GUEST_GROUP_LOCAL_PROFILE}[group_name]    os_type=Windows, Mac OS
&{CLOUD_PPSK_USR_GRP_RULE}       name=cld_ppsk_usr_grp_rule      description=cld_ppsk_usr_grp       add_rule=User Group                    user_group=${USER_GROUP_CLOUD_PROFILE}[group_name]
&{CLOUD_PPSK_GST_GRP_RULE}       name=cld_ppsk_gst_grp_rule      description=cld_ppsk_gst_grp       add_rule=User Group                    user_group=${GUEST_GROUP_CLOUD_PROFILE}[group_name]
&{CLOUD_PPSK_USR_GRP_OS_RULE}    name=cld_ppsk_usr_grp_os_rule   description=cld_ppsk_usr_grp_os    add_rule=User Group, Client OS Type    user_group=${USER_GROUP_CLOUD_PROFILE}[group_name]     os_type=Windows, Mac OS
&{CLOUD_PPSK_GST_GRP_OS_RULE}    name=cld_ppsk_gst_grp_os_rule   description=cld_ppsk_gst_grp_os    add_rule=User Group, Client OS Type    user_group=${GUEST_GROUP_CLOUD_PROFILE}[group_name]    os_type=Windows, Mac OS

################## Device Templates ###############################
&{AP_TEMPLATE_1}         wifi0_configuration=&{AP_TEMPLATE_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_1_WIFI1}
&{AP_TEMPLATE_1_WIFI0}   radio_status=On     radio_profile=radio_ng_11ax-2g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_1_WIFI1}   radio_status=On     radio_profile=radio_ng_11ax-5g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable

############### Globle Variables ######################
${retry}         3

*** Settings ***
Library     String
Library     Collections

Library     common/Cli.py
Library     common/Utils.py
Library     common/TestFlow.py
Library     common/tools/remote/WinMuConnect.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/manage/Location.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DevicesActions.py
Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/manage/DeviceCliAccess.py
Library     xiq/flows/mlinsights/MLInsightClient360.py

Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/DeviceTemplate.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/ClassificationRule.py
Library     xiq/flows/configure/UserProfile.py
Library     xiq/flows/configure/UserGroups.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/waits.yaml
Variables    Environments/Config/device_commands.yaml

Library	    Remote 	http://${mu1.ip}:${mu1.port}   WITH NAME   rem_mu

Force Tags       testbed_1_node     testbed_2_node     testbed_3_node
Suite Setup      Pre_condition
Suite Teardown   Post_condition

*** Test Cases ***
Step0: Onboard AP
    [Documentation]    Onboard AP
    [Tags]             tcho-14022    tcho-14026    tcho-14027    tcho-14028    development     step0    steps
    ${STATUS}       onboard device quick                            ${ap1}
    Should Be Equal As Strings                                      '${STATUS}'       '1'
    ${AP_SPAWN}     Open Spawn                                      ${ap1.ip}         ${ap1.port}      ${ap1.username}   ${ap1.password}   ${ap1.cli_type}
    ${STATUS}       Configure Device To Connect To Cloud            ${ap1.cli_type}   ${capwap_url}    ${AP_SPAWN}
    Should Be Equal As Strings                                      '${STATUS}'       '1'

    ${STATUS}       Wait for Configure Device to Connect to Cloud   ${ap1.cli_type}   ${capwap_url}    ${AP_SPAWN}
    Should Be Equal As Strings                                      '${STATUS}'       '1'
    Wait_device_online                                              ${ap1}
    [Teardown]      Close Spawn                                     ${AP_SPAWN}

Step1: Create Policy
    [Documentation]     Creat Policy, User Profile, VLAN Profile, and Classification Rule.
    [Tags]              tcho-14022    tcho-14026    tcho-14027    tcho-14028    development     step1      steps

    Set Suite Variable             ${POLICY}            ppsk_vlan_usr_grp
    Set Suite Variable             ${AP_TEMP_NAME}      ${ap1.model}_${POLICY}

    ${STATUS}                      Create User Group                                  ${USER_GROUP_LOCAL_PROFILE}[group_name]        user_group_profile=&{USER_GROUP_PROFILE_LOCAL_MULTI}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Create User Group                                  ${GUEST_GROUP_LOCAL_PROFILE}[group_name]       user_group_profile=&{GUEST_GROUP_PROFILE_LOCAL_MULTI}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Create User Group                                  ${USER_GROUP_CLOUD_PROFILE}[group_name]        user_group_profile=&{USER_GROUP_PROFILE_CLOUD_MULTI}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Create User Group                                  ${GUEST_GROUP_CLOUD_PROFILE}[group_name]       user_group_profile=&{GUEST_GROUP_PROFILE_CLOUD_MULTI}
    should be equal as strings     '${STATUS}'        '1'

    ${STATUS}                      create network policy if does not exist            ${POLICY}    ${WIRELESS_PPSK_00}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      create ssid to policy                              ${POLICY}    &{WIRELESS_PPSK_01}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      create ssid to policy                              ${POLICY}    &{WIRELESS_PPSK_02}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      create ssid to policy                              ${POLICY}    &{WIRELESS_PPSK_03}
    should be equal as strings     '${STATUS}'        '1'

    ${STATUS}                      Add User Group To Network Policy Ssid              ${POLICY}    ${WIRELESS_PPSK_00}[ssid_name]    ${GUEST_GROUP_CONFIG_LOCAL_ADD}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Add User Group To Network Policy Ssid              ${POLICY}    ${WIRELESS_PPSK_01}[ssid_name]    ${USER_GROUP_CONFIG_LOCAL_ADD}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Add User Group To Network Policy Ssid              ${POLICY}    ${WIRELESS_PPSK_02}[ssid_name]    ${GUEST_GROUP_CONFIG_CLOUD_ADD}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Add User Group To Network Policy Ssid              ${POLICY}    ${WIRELESS_PPSK_03}[ssid_name]    ${USER_GROUP_CONFIG_CLOUD_ADD}

    ${STATUS}                      Apply Different User Profile to Various Clients    ${WIRELESS_PPSK_00}[ssid_name]                 ${USER_PROFILE_00}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Apply Different User Profile to Various Clients    ${WIRELESS_PPSK_00}[ssid_name]                 ${USER_PROFILE_01}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Apply Different User Profile to Various Clients    ${WIRELESS_PPSK_01}[ssid_name]                 ${USER_PROFILE_02}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Apply Different User Profile to Various Clients    ${WIRELESS_PPSK_01}[ssid_name]                 ${USER_PROFILE_03}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Apply Different User Profile to Various Clients    ${WIRELESS_PPSK_02}[ssid_name]                 ${USER_PROFILE_04}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Apply Different User Profile to Various Clients    ${WIRELESS_PPSK_02}[ssid_name]                 ${USER_PROFILE_05}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Apply Different User Profile to Various Clients    ${WIRELESS_PPSK_03}[ssid_name]                 ${USER_PROFILE_06}
    should be equal as strings     '${STATUS}'        '1'
    ${STATUS}                      Apply Different User Profile to Various Clients    ${WIRELESS_PPSK_03}[ssid_name]                 ${USER_PROFILE_07}
    should be equal as strings     '${STATUS}'        '1'

    ${STATUS}                      add ap template from common object                 ${ap1.model}                                   ${AP_TEMP_NAME}                    ${AP_TEMPLATE_1}
    Should Be Equal As Strings     '${STATUS}'        '1'
    ${STATUS}                      add ap template to network policy                  ${AP_TEMP_NAME}                                ${POLICY}
    Should Be Equal As Strings     '${STATUS}'        '1'

Step2: Assign network policy with VLANs to AP1
    [Documentation]     Assign network policy with VLAN 105 to AP1
    [Tags]              tcho-14022    tcho-14026    tcho-14027    tcho-14028   development     step2      steps
    Depends On          Step1
    ${UPDATE}                      Update Network Policy To Ap     ${POLICY}     ${ap1.serial}    Complete
    should be equal as strings     '${UPDATE}'        '1'
    Wait_device_online                                             ${ap1}
    Enable_disable_client_Wifi_device                              ${mu1}

Step3: Verify (VLAN 106) by assignment the SSID to AP and upload the config
    [Documentation]     Verify (VLAN 106) by assignment the SSID to AP and upload the config
    [Tags]              tcho-14022    development     step3     stepv      steps
    Depends On          Step2
    Connetion_SSID_to_AP_and_checked_client360   ${LOCAL_MULTI_USER_GROUP}   ${WIRELESS_PPSK_00}   ${USER_PROFILE_00}

$tep4: Verify (VLAN 107) by assignment the SSID to AP and upload the config
    [Documentation]     Verify (VLAN 107) by assignment the SSID to AP and upload the config
    [Tags]              tcho-14022    development     step4     stepv      steps
    Depends On          Step2
    Connetion_SSID_to_AP_and_checked_client360   ${LOCAL_MULTI_GUEST_GROUP}   ${WIRELESS_PPSK_00}   ${USER_PROFILE_01}

Step5: Verify (VLAN 108) by assignment the SSID to AP and upload the config
    [Documentation]     Verify (VLAN 108) by assignment the SSID to AP and upload the config
    [Tags]              tcho-14026    development     step5     stepv      steps
    Depends On          Step2
    Connetion_SSID_to_AP_and_checked_client360   ${LOCAL_MULTI_USER_GROUP}   ${WIRELESS_PPSK_01}   ${USER_PROFILE_02}   ${LOCAL_PPSK_USR_GRP_OS_RULE}    ${True}

$tep6: Verify (VLAN 109) by assignment the SSID to AP and upload the config
    [Documentation]     Verify (VLAN 109) by assignment the SSID to AP and upload the config
    [Tags]              tcho-14026    development     step6     stepv      steps
    Depends On          Step2
    Connetion_SSID_to_AP_and_checked_client360   ${LOCAL_MULTI_GUEST_GROUP}   ${WIRELESS_PPSK_01}   ${USER_PROFILE_03}   ${LOCAL_PPSK_GST_GRP_OS_RULE}    ${True}

Step7: Verify (VLAN 110) by assignment the SSID to AP and upload the config
    [Documentation]     Verify (VLAN 110) by assignment the SSID to AP and upload the config
    [Tags]              tcho-14027    development     step7     stepv      steps
    Depends On          Step2
    Connetion_SSID_to_AP_and_checked_client360   ${CLOUD_MULTI_USER_GROUP}   ${WIRELESS_PPSK_02}   ${USER_PROFILE_04}

$tep8: Verify (VLAN 111) by assignment the SSID to AP and upload the config
    [Documentation]     Verify (VLAN 111) by assignment the SSID to AP and upload the config
    [Tags]              tcho-14027    development     step8     stepv      steps
    Depends On          Step2
    Connetion_SSID_to_AP_and_checked_client360   ${CLOUD_MULTI_GUEST_GROUP}   ${WIRELESS_PPSK_02}   ${USER_PROFILE_05}

Step9: Verify (VLAN 112) by assignment the SSID to AP and upload the config
    [Documentation]     Verify (VLAN 112) by assignment the SSID to AP and upload the config
    [Tags]              tcho-14028    development     step9     stepv      steps
    Depends On          Step2
    Connetion_SSID_to_AP_and_checked_client360   ${CLOUD_MULTI_USER_GROUP}   ${WIRELESS_PPSK_03}   ${USER_PROFILE_06}    ${CLOUD_PPSK_USR_GRP_OS_RULE}    ${True}

$tep10: Verify (VLAN 113) by assignment the SSID to AP and upload the config
    [Documentation]     Verify (VLAN 113) by assignment the SSID to AP and upload the config
    [Tags]              tcho-14028    development     step10     stepv      steps
    Depends On          Step2
    Connetion_SSID_to_AP_and_checked_client360   ${CLOUD_MULTI_GUEST_GROUP}   ${WIRELESS_PPSK_03}   ${USER_PROFILE_07}   ${CLOUD_PPSK_GST_GRP_OS_RULE}    ${True}

*** Keywords ***
Pre_condition
    ${STATUS}                       Login User    ${tenant_username}   ${tenant_password}
    should be equal as strings      '${STATUS}'   '1'
    reset devices to default
    log to console                  Wait for 2 minutes for completing reboot....
    sleep                           2m
    delete all devices
    delete all network policies
    delete all ssids
    delete all ap templates
    Delete All User Profiles
    Delete All Vlan Profiles

Post_condition
    Logout User
    Quit Browser

Wait_device_online
    [Arguments]    ${ap}
    ${STATUS}                       Wait Until Device Online    ${ap}[serial]
    Should Be Equal As Strings      '${STATUS}'    '1'
    ${STATUS}                       Get Device Status           ${ap}[serial]
    Should contain any              ${STATUS}      green        config audit mismatch

Connect_to_client
    [Arguments]    ${ssid}    ${password}     ${delay}=5s
    FOR    ${i}    IN RANGE    ${retry}
        ${STATUS}            rem_mu.connect wpa2 psk network     ${ssid}    ${password}
        exit for loop if    '${STATUS}'=='1'
    END
    sleep    ${delay}

Enable_disable_client_Wifi_device
    [Arguments]     ${mu}
    ${SPAWN}        Open Spawn    ${mu}[ip]     22    ${mu}[username]    ${mu}[password]    cli_type=MU-WINDOWS
    Send Commands   ${SPAWN}      pnputil /disable-device /deviceid \"PCI\\CC_0280\", pnputil /enable-device /deviceid \"PCI\\CC_0280\"
    [Teardown]      run keyword   Close Spawn   ${SPAWN}

Connetion_SSID_to_AP_and_checked_client360
    [Arguments]    ${user_group}    ${wireless_ppsk}     ${user_profile}     ${os_type_rule}=${EMPTY}    ${os_type_checked}=${False}
    @{users}           split string     ${user_group}[name]
    @{passwords}       split string     ${user_group}[password]
    @{os}              Run Keyword If   ${os_type_checked}    split string   ${os_type_rule}[os_type]   ,${SPACE}

    Connect_to_client      ${wireless_ppsk}[ssid_name]        ${passwords}[0]
    ${OUT}                 get real time client360 details    ${mu1.wifi_mac}
    ${OUT}                 convert to string                  ${OUT}
    should match regexp    ${OUT}                             'userName':\\s+'${users}[0]',
    should match regexp    ${OUT}                             'vlan':\\s+'${user_profile}[vlan_id]'
    Run Keyword If         ${os_type_checked}    should contain any     ${OUT}    ${os}[0]    ${os}[1]

    Connect_to_client      ${wireless_ppsk}[ssid_name]        ${passwords}[1]
    ${OUT}                 get real time client360 details    ${mu1.wifi_mac}
    ${OUT}                 convert to string                  ${OUT}
    should match regexp    ${OUT}                             'userName':\\s+'${users}[1]',
    should match regexp    ${OUT}                             'vlan':\\s+'${user_profile}[vlan_id]'
    Run Keyword If         ${os_type_checked}    should contain any     ${OUT}    ${os}[0]    ${os}[1]

    Connect_to_client      ${wireless_ppsk}[ssid_name]        ${passwords}[2]
    ${OUT}                 get real time client360 details    ${mu1.wifi_mac}
    ${OUT}                 convert to string                  ${OUT}
    should match regexp    ${OUT}                             'userName':\\s+'${users}[2]',
    should match regexp    ${OUT}                             'vlan':\\s+'${user_profile}[vlan_id]'
    Run Keyword If         ${os_type_checked}    should contain any     ${OUT}    ${os}[0]    ${os}[1]
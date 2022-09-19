#########################################################################################################
# Author        : Binh Nguyen
# Date          : June 15th 2022
# Description   : TCXM-17744, Enterprise SSID using cloud Auth service for Wifi2
#                 TCXM-17745, Enterprise SSID using external Radius Server Auth service for Wifi2
#                 TCXM-17748, Enterprise SSID using cloud Auth service for Wifi0/1
#                 TCXM-17750, Enterprise SSID using external Radius Server Auth service for Wifi0/1
#                 TCXM-17746, Enterprise SSID using cloud Auth service for Wifi0/1 & 2
#                 TCXM-17747, Enterprise SSID using external Radius Server Auth service for Wifi0/1 & 2
#########################################################################################################

**** Variables ***
################## Policy Detail & Wireless Network ###############################
&{WIRELESS_ENTERPRISE_00}    ssid_name=""   network_type=Standard   ssid_profile=&{BORADCAST_SSID_00}   auth_profile=&{ENTERPRISE_AUTH_PROFILE_00}
&{WIRELESS_ENTERPRISE_01}    ssid_name=""   network_type=Standard   ssid_profile=&{BORADCAST_SSID_00}   auth_profile=&{ENTERPRISE_AUTH_PROFILE_01}
&{WIRELESS_ENTERPRISE_02}    ssid_name=""   network_type=Standard   ssid_profile=&{BORADCAST_SSID_01}   auth_profile=&{ENTERPRISE_AUTH_PROFILE_02}
&{WIRELESS_ENTERPRISE_03}    ssid_name=""   network_type=Standard   ssid_profile=&{BORADCAST_SSID_01}   auth_profile=&{ENTERPRISE_AUTH_PROFILE_03}

&{BORADCAST_SSID_00}        WIFI0=Enable      WIFI1=Enable      WIFI2=Disable
&{BORADCAST_SSID_01}        WIFI0=Disable     WIFI1=Disable     WIFI2=Enable

&{ENTERPRISE_AUTH_PROFILE_00}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_00}   cwp_profile=&{ENTERPRISE_CWP_00}  auth_settings_profile=&{AUTHENTICATION_SETTINGS_00}   user_access_settings=None   additional_settings=None
&{ENTERPRISE_AUTH_PROFILE_01}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_00}   cwp_profile=&{ENTERPRISE_CWP_00}  auth_settings_profile=&{AUTHENTICATION_SETTINGS_01}   user_access_settings=None   additional_settings=None
&{ENTERPRISE_AUTH_PROFILE_02}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_01}   cwp_profile=&{ENTERPRISE_CWP_00}  auth_settings_profile=&{AUTHENTICATION_SETTINGS_00}   user_access_settings=None   additional_settings=None
&{ENTERPRISE_AUTH_PROFILE_03}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_01}   cwp_profile=&{ENTERPRISE_CWP_00}  auth_settings_profile=&{AUTHENTICATION_SETTINGS_01}   user_access_settings=None   additional_settings=None

&{KEY_ENCRYPTION_00}   key_management=WPA2-802.1X    encryption_method=CCMP (AES)
&{KEY_ENCRYPTION_01}   key_management=WPA3-802.1X    encryption_method=AES 192-bit

&{ENTERPRISE_CWP_00}   enable_cwp=Disable

&{AUTHENTICATION_SETTINGS_00}   auth_with_extcldiq_service=Enable    user_group_config=&{USER_GROUP_CFG_00}
&{AUTHENTICATION_SETTINGS_01}   auth_with_extcldiq_service=Disable   radius_server_group_config=&{RADIUS_SERVER_GROUP_00}

########## Cloud Authentication Service Enable ###############
&{USER_GROUP_CFG_00}              group_name=cld_user_grp    user_group_profile=&{USER_GROUP_PROFILE_00}      db_loc=Cloud

&{USER_GROUP_PROFILE_00}          user_group_config=&{DB_LOC_CLOUD_RADIUS_DEFAULT}      passwd_settings=&{PASSWD_SETTING_00}        expiration_settings=None
...                               delivery_settings=None                                users_config=&{SINGLE_USER_INFO_00}

&{DB_LOC_CLOUD_RADIUS_DEFAULT}    pass_db_loc=Cloud  pass_type=radius  cwp_register=Disable

&{PASSWD_SETTING_00}              passwd_type=RADIUS    letters=Enable    numbers=Enable    special_characters=Disable    enforce_use_of=Any selected character types    gen_passwd_len=10

&{SINGLE_USER_INFO_00}            user-type=single                        name=user4                          organization=ExtremeNetworks    purpose_of_visit=guest
...                               email_address=cloud1tenant1@gmail.com   phone_number=+91 India-8971766359   user_name_type=Name             password=Aerohive123
...                               pass-generate=Disable                   description=single user username password verification              deliver_pass=cloud1tenant1@gmail.com

########## Cloud Authentication Service Disable (RADIUS) ##############
&{RADIUS_SERVER_GROUP_00}        radius_server_group_name=Rad_Server_Grp   radius_server_config=&{RADIUS_SERVER_00}

&{RADIUS_SERVER_00}              radius_server_group_desc=External Radius server group   server_type=EXTERNAL RADIUS SERVER   external_radius_server_config=&{EXTRENAL_RADIUS_SERVER_00}

&{EXTRENAL_RADIUS_SERVER_00}     radius_server_name=Rad_Sever_ip   ip_or_host_type=IP Address    radius_server_ip_host_name=Radius-IP     radius_server_ip_address=10.254.152.59   shared_secret=Symbol@123

################## Device Templates ###############################
&{AP_TEMPLATE_1}         wifi0_configuration=&{AP_TEMPLATE_1_WIFI0}   wifi1_configuration=&{AP_TEMPLATE_1_WIFI1}   wifi2_configuration=&{AP_TEMPLATE_1_WIFI2}
&{AP_TEMPLATE_1_WIFI0}   radio_status=On     radio_profile=radio_ng_11ax-2g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_1_WIFI1}   radio_status=On     radio_profile=radio_ng_11ax-5g     client_mode=Disable    client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable
&{AP_TEMPLATE_1_WIFI2}   radio_status=on     radio_profile=radio_ng_11ax-6g                            client_access=Enable    backhaul_mesh_link=Disable   sensor=Disable

############### Globle Variables ######################
${retry}     3

*** Settings ***
Library     String
Library     Collections

Library     common/Cli.py
Library     common/Utils.py
Library     common/TestFlow.py
Library     common/tools/remote/WinMuConnect.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/mlinsights/MLInsightClient360.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/DevicesActions.py
Library     xiq/flows/manage/DeviceConfig.py
Library     xiq/flows/manage/DeviceCliAccess.py

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

Force Tags      testbed_1_node     testbed_2_node     testbed_3_node
Suite Setup      Pre_condition
Suite Teardown   Post_condition

*** Test Cases ***
Step0: Onboard AP
    [Documentation]    Onboard AP
    [Tags]             tcxm-17744     development     step0   steps
    ${STATUS}                      Onboard Device    ${ap1.serial}    ${ap1.make}    location=${ap1.location}
    should be equal as integers    ${STATUS}         1

    ${AP_SPAWN}=        Open Spawn          ${ap1.ip}           ${ap1.port}      ${ap1.username}      ${ap1.password}      ${ap1}[cli_type]
    ${OUTPUT0}=         Send Commands       ${AP_SPAWN}        capwap client server name ${capwap_url}, capwap client default-server-name ${capwap_url}, capwap client server backup name ${capwap_url}, no capwap client enable, capwap client enable, save config
    ${OUTPUT0}=         Send                ${AP_SPAWN}        console page 0
    ${OUTPUT0}=         Send                ${AP_SPAWN}        show version detail
    ${OUTPUT0}=         Send                ${AP_SPAWN}        show capwap client
    ${OUTPUT2}=         Send                ${AP_SPAWN}        ${cmd_capwap_hm_primary_name}
    ${OUTPUT3}=         Send                ${AP_SPAWN}        ${cmd_capwap_server_ip}
    ${OUTPUT1}=         Wait For CLI Output                    ${AP_SPAWN}         ${cmd_capwap_client_state}          ${output_capwap_status}
    Should Be Equal as Integers             ${OUTPUT1}          1
    Close Spawn         ${AP_SPAWN}

    Wait Until Device Online                ${ap1.serial}
    ${AP_STATUS}=                           Get AP Status      ap_mac=${ap1.mac}
    Should Be Equal As Strings             '${AP_STATUS}'      'green'

Step1: Create Policy - Enterprise with Cloud and Radius auth
    [Documentation]     Create policy, select wifi0,1,2, and update policy to AP
    [Tags]              tcxm-17744    tcxm-17745    tcxm-17746    tcxm-17747    tcxm-17748    tcxm-17750    development     step1      steps
    Depends On          Step0
    ${NUM}=                        Generate Random String     5    012345678
    Set Suite Variable             ${POLICY}                       enterprise_${NUM}
    Set Suite Variable             ${SSID_00}                      w0_1_cld
    Set Suite Variable             ${SSID_01}                      w0_1_rad
    Set Suite Variable             ${SSID_02}                      w2_cld
    Set Suite Variable             ${SSID_03}                      w2_rad
    Set Suite Variable             ${AP_TEMP_NAME}                 ${ap1.model}_${NUM}
    Set To Dictionary              ${WIRELESS_ENTERPRISE_00}       ssid_name=${SSID_00}
    Set To Dictionary              ${WIRELESS_ENTERPRISE_01}       ssid_name=${SSID_01}
    Set To Dictionary              ${WIRELESS_ENTERPRISE_02}       ssid_name=${SSID_02}
    Set To Dictionary              ${WIRELESS_ENTERPRISE_03}       ssid_name=${SSID_03}

    ${STATUS}                      Create Network Policy    ${POLICY}      &{WIRELESS_ENTERPRISE_00}
    should be equal as strings     '${STATUS}'       '1'
    ${STATUS}                      create ssid to policy    ${POLICY}      &{WIRELESS_ENTERPRISE_01}
    should be equal as strings    '${STATUS}'        '1'
    ${STATUS}                      create ssid to policy    ${POLICY}      &{WIRELESS_ENTERPRISE_02}
    should be equal as strings    '${STATUS}'        '1'
    ${STATUS}                      create ssid to policy    ${POLICY}      &{WIRELESS_ENTERPRISE_03}
    should be equal as strings    '${STATUS}'        '1'
    ${STATUS}                      add ap template from common object      ${ap1.model}        ${AP_TEMP_NAME}   &{AP_TEMPLATE_1}
    Should Be Equal As Strings     '${STATUS}'       '1'
    ${STATUS}                      add ap template to network policy       ${AP_TEMP_NAME}    ${POLICY}
    Should Be Equal As Strings     '${STATUS}'       '1'

Step2: Assign network policy to AP
    [Documentation]     Assign network policy to AP
    [Tags]              tcxm-17744    tcxm-17745    tcxm-17746    tcxm-17747    tcxm-17748    tcxm-17750    development     step2      steps
    Depends On          Step1
    ${UPDATE}                      Update Network Policy To Ap             ${POLICY}          ${ap1.serial}      Complete
    should be equal as strings     '${UPDATE}'       '1'
    Wait Until Device Online       ${ap1.serial}
    ${AP_STATUS}                   Get AP Status     ap_mac=${ap1.mac}
    Should Be Equal As Strings    '${AP_STATUS}'    'green'

Step3: MU connect to wifi0-1 - Cloud Auth service
    [Documentation]     MU connect to wifi0-1 - Enterprise SSID using cloud Auth service
    [Tags]              tcxm-17746     tcxm-17748     development     step3      steps
    Depends On          Step2
    FOR    ${i}    IN RANGE    ${retry}
        ${STATUS}               rem_mu.connect wifi network        ${SSID_00}
        exit for loop if        '${STATUS}'=='1'
    END
    should be equal as strings      '${STATUS}'     '1'

Step4: Verify Client360 to wifi0-1 - Cloud Auth service
    [Documentation]     Verify Client360 to wifi0-1 - Enterprise SSID using cloud Auth service
    [Tags]              tcxm-17746     tcxm-17748     development     step4      steps
    Depends On          Step3
    ${OUT}             get client360 current connection status      8EB0511639C6
    should contain     ${OUT['USER']}                               user4

Step5: MU connect to wifi0-1 - Radius Auth service
    [Documentation]     MU connect to wifi0-1 - Enterprise SSID using radius Auth service
    [Tags]              tcxm-17747     tcxm-17750     development     step5      steps
    Depends On          Step2
    FOR    ${i}    IN RANGE    ${retry}
        ${STATUS}               rem_mu.connect wifi network        ${SSID_01}
        exit for loop if        '${STATUS}'=='1'
    END
    should be equal as strings      '${STATUS}'     '1'

Step6: Verify Client360 to wifi0-1 - Radius Auth service
    [Documentation]     Verify Client360 to wifi0-1 - Enterprise SSID using radius Auth service
    [Tags]              tcxm-17747     tcxm-17750     development     step6      steps
    Depends On          Step5
    ${OUT}             get client360 current connection status      CA7BCBD1A44E
    should contain     ${OUT['USER']}                               user4

Step7: MU connect to wifi2 - Cloud Auth service
    [Documentation]     MU connect to wifi0-1 - Enterprise SSID using cloud Auth service
    [Tags]              tcxm-17744     tcxm-17746     development     step7      steps
    Depends On          Step2
    FOR    ${i}    IN RANGE    ${retry}
        ${STATUS}               rem_mu.connect wifi network        ${SSID_02}
        exit for loop if        '${STATUS}'=='1'
    END
    should be equal as strings      '${STATUS}'     '1'

Step8: Verify Client360 to wifi2- Cloud Auth service
    [Documentation]     Verify Client360 to wifi0-1 - Enterprise SSID using cloud Auth service
    [Tags]              tcxm-17744     tcxm-17746     development     step8      steps
    Depends On          Step7
    ${OUT}             get client360 current connection status      0EAE738F5906
    should contain     ${OUT['USER']}                               user4

Step9: MU connect to wifi2 - Radius Auth service
    [Documentation]     MU connect to wifi0-1 - Enterprise SSID using radius Auth service
    [Tags]              tcxm-17745     tcxm-17747     development     step9      steps
    Depends On          Step2
    FOR    ${i}    IN RANGE    ${retry}
        ${STATUS}               rem_mu.connect wifi network        ${SSID_03}
        exit for loop if        '${STATUS}'=='1'
    END
    should be equal as strings      '${STATUS}'     '1'

Step10: Verify Client360 to wifi2 - Radius Auth service
    [Documentation]     Verify Client360 to wifi0-1 - Enterprise SSID using radius Auth service
    [Tags]              tcxm-17745     tcxm-17747     development     step10      steps
    Depends On          Step9
    ${OUT}             get client360 current connection status      3A9A55246C38
    should contain     ${OUT['USER']}                               user4

*** Keywords ***
Pre_condition
    ${STATUS}                           Login User    ${tenant_username}   ${tenant_password}
    should be equal as strings          '${STATUS}'   '1'
    ${failed}     ${success}      reset device to default    ${ap1.serial}
    log to console                Wait for 2 minutes for completing reboot....
    sleep                               2m
    delete all aps
    delete all network policies
    delete all ssids
    delete all ap templates

Post_condition
    Logout User
    Quit Browser

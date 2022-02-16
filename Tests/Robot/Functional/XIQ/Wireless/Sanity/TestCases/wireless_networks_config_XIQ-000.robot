*** Variables ***
################# Open Authentication network Profile for cloud captive web portal #####################################
&{CONFIG_PUSH_OPEN_NW_01}    ssid_name=${CONFIG_PUSH_SSID_01}         network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}
&{CONFIG_PUSH_OPEN_NW_02}    ssid_name=${CONFIG_PUSH_SSID_02}         network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}
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




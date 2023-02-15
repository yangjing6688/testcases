*** Variables ***
################# Network Policy #################
${NW_POLICY_NAME1}          Auto_NW_POLICY_1
${NW_POLICY_NAME2}          Auto_NW_POLICY_2
${NW_POLICY_NAME3}          Auto_NW_POLICY_3
${NW_POLICY_NAME4}          Auto_NW_POLICY_4

################# Personal WPA/WPA2/WPA3 #################
&{WIRELESS_PESRONAL_WPA2CCMP_1}            ssid_name=automation_psk_wpa2_ccmp_1     network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}    auth_profile=&{PERSONAL_AUTH_PROFILE_WPA2CCMP}
&{WIRELESS_PESRONAL_WPA3CCMP_1}            ssid_name=automation_psk_wpa3_ccmp_1     network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}    auth_profile=&{PERSONAL_AUTH_PROFILE_WAP3CCMP}
&{WIRELESS_PESRONAL_WPA2CCMP_2}            ssid_name=automation_psk_wpa2_ccmp_2     network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}    auth_profile=&{PERSONAL_AUTH_PROFILE_WPA2CCMP}
&{WIRELESS_PESRONAL_WPA3CCMP_2}            ssid_name=automation_psk_wpa3_ccmp_2     network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}    auth_profile=&{PERSONAL_AUTH_PROFILE_WAP3CCMP}
# Broadcast SSID setting
&{BORADCAST_SSID_DEFAULT}=          WIFI0=Enable        WIFI1=Enable
# Auth profile
&{PERSONAL_AUTH_PROFILE_WPA2CCMP}           auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_WPA2CCMP}   cwp_config=&{PSK_CWP_DEFAULT}
&{PERSONAL_AUTH_PROFILE_WAP3CCMP}           auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION_WPA3CCMP}   cwp_config=&{PSK_CWP_DEFAULT}
# Key profile
&{PSK_KEY_ENCRYPTION_WPA2CCMP}              key_management=WPA2-(WPA2 Personal)-PSK    encryption_method=CCMP (AES)   key_type=ASCII Key  key_value=Extreme@123
&{PSK_KEY_ENCRYPTION_WPA3CCMP}              key_management=WPA3 (SAE)   sae_group=All  transition_mode=enable   key_value=Extreme@123  anti_logging_Threshold=10
# CWP option
&{PSK_CWP_DEFAULT}                  enable_cwp=Disable


################# Private Pre-shared Key #################
#&{WIRELESS_PPSK_WPA2CCMP_1}            ssid_name=automation_ppsk_wpa2_ccmp_1     network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}    auth_profile=&{PPSK_AUTH_PROFILE_CLOUD_BULK}
#&{WIRELESS_PPSK_WPA2CCMP_2}            ssid_name=automation_ppsk_wpa2_ccmp_2     network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}    auth_profile=&{PPSK_AUTH_PROFILE_CLOUD_BULK}
# Auth profile
&{PPSK_AUTH_PROFILE_CLOUD_SINGLE}     auth_type=PPSK   key_encryption=&{PPSK_KEY_ENCRYPTION_WPA2CCMP}   ppsk_config=&{PPSK_SETTING_DEFAULT}   cwp_config=&{PPSK_CWP_DEFAULT}   user_group_config=&{USER_GROUP_CLOUD_SIGNLE_NONE_PROFILE}   user_access_settings_config=None   additional_settings_config=None
&{PPSK_AUTH_PROFILE_CLOUD_SINGLE1}    auth_type=PPSK   key_encryption=&{PPSK_KEY_ENCRYPTION_WPA2CCMP}   ppsk_config=&{PPSK_SETTING_DEFAULT}   cwp_config=&{PPSK_CWP_DEFAULT}   user_group_config=&{USER_GROUP_CLOUD_SIGNLE_NONE_PROFILE}  user_access_settings_config=None   additional_settings_config=None
&{PPSK_AUTH_PROFILE_LOCAL_SINGLE}     auth_type=PPSK   key_encryption=&{PPSK_KEY_ENCRYPTION_WPA2CCMP}   ppsk_config=&{PPSK_SETTING_DEFAULT}   cwp_config=&{PPSK_CWP_DEFAULT}   user_group_config=&{USER_GROUP_LOCAL_SINGLE_NONE_PROFILE}   user_access_settings_config=None   additional_settings_config=None
&{PPSK_AUTH_PROFILE_CWP_USER_GROUP}   auth_type=PPSK   key_encryption=&{PPSK_KEY_ENCRYPTION_WPA2CCMP}   ppsk_config=&{PPSK_SETTING_DEFAULT}   cwp_config=&{PPSK_CWP_DEFAULT}   user_group_config=&{USER_GROUP_CLOUD_CWP_NONE_PROFILE}      user_access_settings_config=None   additional_settings_config=None

&{PPSK_AUTH_PROFILE1}                 auth_type=PPSK   key_encryption=&{PPSK_KEY_ENCRYPTION_WPA2CCMP}   ppsk_config=&{PPSK_SETTING_DEFAULT}   cwp_config=&{PPSK_CWP_DEFAULT}   user_group_config=&{USER_GROUP_LOCAL1_NONE_PROFILE}         user_access_settings_config=None   additional_settings_config=None

### Key and encryption method for ppsk network
&{PPSK_KEY_ENCRYPTION_WPA2CCMP}     key_management=WPA2-(WPA2 Personal)-PSK    encryption_method=CCMP (AES)

#######  PPSK AUTH SETTINGS ##
&{PPSK_SETTING_DEFAULT}    client_per_ppsk=Disable    mac_binding_num_per_ppsk=Disable   pcg_use=Disable   ppsk_classification=Disable
&{PPSK_SETTING1}           client_per_ppsk=Enable     num_clients=1   mac_binding_num_per_ppsk=Disable   pcg_use=Disable   ppsk_classification=Disable

### cwp
&{PPSK_CWP_DEFAULT}   enable_cwp=Disable

### User Group Settings
${BULK_CLOUD_USER_GROUP}        auto_cloud_ppsk_bulk_user_group
${SINGLE_CLOUD_USER_GROUP}      auto_cloud_ppsk_single_user_group
${BULK_LOCAL_USER_GROUP}        auto_local_ppsk_bulk_user_group
${SINGLE_LOCAL_USER_GROUP}      auto_local_ppsk_single_user_group
${CLOUD_CWP_USER_GROUP}         auto_cloud_ppsk_cwp_user_group
${CLIENT_PER_PPSK_GRP}          auto_cloud_ppsk_bulk_user_group

&{USER_GROUP_CLOUD_SIGNLE_NONE_PROFILE}    group_name=${SINGLE_CLOUD_USER_GROUP}   user_group_profile=None     db_loc=Cloud
&{USER_GROUP_LOCAL_SINGLE_NONE_PROFILE}    group_name=${SINGLE_LOCAL_USER_GROUP}   user_group_profile=None     db_loc=Local
&{USER_GROUP_CLOUD_CWP_NONE_PROFILE}       group_name=${CLOUD_CWP_USER_GROUP}      user_group_profile=None     db_loc=Cloud
&{USER_GROUP_LOCAL1_NONE_PROFILE}         group_name=${BULK_LOCAL_USER_GROUP}       user_group_profile=None     db_loc=Local



## User Access Settings Config
&{USER_ACCESS_SETTING_CONFIG1}

### Additional Setting Config
&{ADDITIONAL_SETTING_CONFIG}

####################### USER GROUP PROFILES ##################################################
# DB Location and Password type:
&{DB_LOC_CLOUD_PPSK_DEFAULT}      pass_db_loc=CLOUD    pass_type=ppsk      cwp_register=Disable      pcg_use=Disable
&{DB_LOC_CLOUD_PPSK_1}            pass_db_loc=CLOUD    pass_type=ppsk      cwp_register=Enable       pcg_use=Disable
&{DB_LOC_LOCAL_PPSK_DEFAULT}      pass_db_loc=LOCAL    pass_type=ppsk      client_per_ppsk=Disable   pcg_use=Disable  ppsk_classification=Disable


&{USER_GROUP_PROFILE_CWP}             user_group_config=&{DB_LOC_CLOUD_PPSK_1}              users_config=None
...                                   passwd_settings=None                                  expiration_settings=None               delivery_settings=None


&{USER_GROUP_PROFILE_LOCAL1}          user_group_config=&{DB_LOC_LOCAL_PPSK_DEFAULT}        users_config=None
...                                   passwd_settings=None                                  expiration_settings=&{EXPIRATION_SETTING2}

&{USER_GROUP_PROFILE_CLOUD1}          user_group_config=&{DB_LOC_CLOUD_PPSK_DEFAULT}        users_config=None
...                                   passwd_settings=None                                  expiration_settings=&{EXPIRATION_SETTING1}

## User Profiles(this may use in other testcases,keep it)

#&{bulk_users_info2}     user-type=bulk     username_prefix=user2_    no_of_accounts=2       email_user_account_to=${MAIL_ID1}
#&{bulk_users_info3}     user-type=bulk     username_prefix=user100_  no_of_accounts=1       email_user_account_to=${MAIL_ID1}

#&{single_user1_info}    user-type=single   name=Symbol        organization=ExtremeNetworks            purpose_of_visit=guest
#...                     email_address=${MAIL_ID1}      phone_number=+91 India-8971766359       user_name_type=Name
#...                     password=extremextreme                pass-generate=Enable                    description=single user username password verification
#...                     deliver_pass=${MAIL_ID1}


#&{single_user3_info}    user-type=single   name=Jims          organization=ExtremeNetworksA           purpose_of_visit=guest
#...                     email_address=${MAIL_ID1}      phone_number=+91 India-8971766459       user_name_type=Name
#...                     password=extremexxter                 pass-generate=Enable                    description=single user username password verification
#...                     deliver_pass=${MAIL_ID1}

#&{single_user2_info}    user-type=single                     name=Symbol1                             organization=ExtremeNetworks    purpose_of_visit=guest
#...                     email_address=${MAIL_ID1}     phone_number=+504 Honduras-8971766359    user_name_type=Phone Number
#...                     password=extremextreme              pass-generate=Disable                     description=single user username password verification
#...                     deliver_pass=${MAIL_ID1}


## Expiration Settings
&{EXPIRATION_SETTING1}     db_loc=Cloud                account_expiration=Valid For Time Period   in=24   in_period=hours   after=ID Creation   renew_user_cred=Enable
...                        delete_cred_after=Enable    delete_cred_after_time=24  after_period=Hour   action_at_expiration=Show Expiration Message


&{EXPIRATION_SETTING2}     db_loc=Local     account_expiration=Valid During Dates     action_at_expiration=Show Expiration Message


#
&{DB_LOC_CLOUD_PPSK3}        pass_db_loc=WOLKE     pass_type=ppsk      cwp_register=Disable      pcg_use=Disable

&{USER_GROUP_PROFILE_CLOUD2}          user_group_config=&{DB_LOC_CLOUD_PPSK3}        users_config=None
...                                   passwd_settings=None        expiration_settings=&{EXPIRATION_SETTING4}

&{EXPIRATION_SETTING4}     db_loc=Cloud                account_expiration=Gültig für den Zeitraum   in=24   in_period=Std.   after=ID-Erstellung   renew_user_cred=Enable
...                        delete_cred_after=Enable    delete_cred_after_time=24  after_period=Protokoll   action_at_expiration=Ablaufmeldung anzeigen



################# Enterprise WPA/WPA2/WPA3 #################

&{WIRELESS_ENTERPRISE_WPA2CCMP_IDM}    ssid_name=auto_8021x_wpa2ccmp_IDM           network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_3}
&{WIRELESS_ENTERPRISE_NW3}    ssid_name=AutoEnterprisedot1x           network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_3}
&{WIRELESS_ENTERPRISE_NW4}    ssid_name=AutoEnterpriseacctlogs        network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_4}
&{WIRELESS_ENTERPRISE_NW5}    ssid_name=AutoEnterprisedot1x           network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_5}
&{WIRELESS_ENTERPRISE_NW6}    ssid_name=dot1xwpa3wronguser            network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_6}
&{WIRELESS_ENTERPRISE_NW10}   ssid_name=AutoEnterprisedot1xwpa3       network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_5}

# Authentication profile
&{ENTERPRISE_AUTH_PROFILE_3}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_WAP2CCMP}   cwp_profile=&{ENTERPRISE_CWP_1}  auth_settings_profile=&{AUTHENTICATION_SETTINGS3}   user_access_settings=None   additional_settings=None
&{ENTERPRISE_AUTH_PROFILE_4}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_WAP2CCMP}   cwp_profile=&{ENTERPRISE_CWP_1}  auth_settings_profile=&{AUTHENTICATION_SETTINGS4}   user_access_settings=None   additional_settings=None
&{ENTERPRISE_AUTH_PROFILE_5}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_WAP2CCMP}   cwp_profile=&{ENTERPRISE_CWP_1}  auth_settings_profile=&{AUTHENTICATION_SETTINGS3}   user_access_settings=None   additional_settings=None
&{ENTERPRISE_AUTH_PROFILE_6}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_WAP2CCMP}   cwp_profile=&{ENTERPRISE_CWP_1}  auth_settings_profile=&{AUTHENTICATION_SETTINGS3}   user_access_settings=None   additional_settings=None

################### Key and Encryption Method Options for eneterprise network
&{KEY_ENCRYPTION_WAP2CCMP}   key_management=WPA2-802.1X    encryption_method=CCMP (AES)
&{KEY_ENCRYPTION_WPACCMP}   key_management=WPA-802.1X    encryption_method=CCMP (AES)
&{KEY_ENCRYPTION_WPA3AES192}   key_management=WPA-802.1X    encryption_method=AES 192-bit

################# Enterprise Captive Web Portal Profile
&{ENTERPRISE_CWP_1}   cwp=Disable
&{ENTERPRISE_CWP_2}   enable_cwp=Enable    cwp_name=enterprisecwp
&{ENTERPRISE_CWP_3}   enable_cwp=Enable    cwp_name=enterprisecwp
&{ENTERPRISE_CWP_3}   enable_cwp=Enable    different_cwp_per_clients=Enable


################### AUthentication configuration pofile

&{AUTHENTICATION_SETTINGS_IDM}   auth_with_extcldiq_service=Enable    user_group=&{Enterprise_User_Group_Cfg3}

&{AUTHENTICATION_SETTINGS3}   auth_with_extcldiq_service=Enable    user_group_config=&{Enterprise_User_Group_Cfg1}
&{AUTHENTICATION_SETTINGS4}   auth_with_extcldiq_service=Enable    user_group=&{Enterprise_User_Group_Cfg2}



## User Group Config
&{Enterprise_User_Group_Cfg1}      group_name=AutoEnterprisedot1x     user_group_profile=None
&{Enterprise_User_Group_Cfg2}      group_name=AutoEnterpriseacctlogs     user_group_profile=None
&{Enterprise_User_Group_Cfg3}      group_name=AutoEnterprisegroup     user_group_profile=None

#### This block is for devcie make
${DEVICE_MAKE}          Extreme - Aerohive
*** Variables ***
&{BORADCAST_SSID_DEFAULT}       WIFI0=Enable        WIFI1=Enable

# Personal Network
&{WIRELESS_PESRONAL_NW4}            ssid_name=test_wpa_quatation           network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}    auth_profile=&{PERSONAL_AUTH_PROFILE3}

############################ Private Pre-Shared Key Wireless network profile creation ##################################
&{WIRELESS_PPSK_NW_CLOUD_BULK}       ssid_name=${BULK_CLOUD_NW_SSID}      network_type=Standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{PPSK_AUTH_PROFILE_CLOUD_BULK}

##############################Enterprise Wireless Network Profile creation #############################################
&{WIRELESS_ENTERPRISE_NW3}    ssid_name=AutoEnterprisedot1x           network_type=Standard   ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{ENTERPRISE_AUTH_PROFILE_3}

# Open Network
&{CONFIG_PUSH_OPEN_NW_01}           ssid_name=AutoOPen_Nw     network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}
&{CONFIG_PUSH_OPEN_NW_02}           ssid_name=AutoOPenNetwork     network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}
&{CONFIG_PUSH_OPEN_NW_03}           ssid_name=TestOPenNetwork     network_type=standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}   auth_profile=&{OPEN_AUTHENTICATION_PROFILE0}

#Auth Profile
&{PERSONAL_AUTH_PROFILE3}           auth_type=PSK   key_encryption=&{PSK_KEY_ENCRYPTION3}   cwp_config=&{PSK_CWP_DEFAULT}
&{OPEN_AUTHENTICATION_PROFILE0}     auth_type=Open           cwp_profile=&{OPEN_CWP}
&{PPSK_AUTH_PROFILE_CLOUD_BULK}       auth_type=PPSK   key_encryption=&{PPSK_KEY_ENCRYPTION1}   ppsk_config=&{PPSK_SETTING_DEFAULT}   cwp_config=&{PPSK_CWP_DEFAULT}   user_group_config=&{USER_GROUP_CLOUD_BULK}     user_access_settings_config=None   additional_settings_config=None
&{ENTERPRISE_AUTH_PROFILE_3}   auth_type=enterprise    key_encryption=&{KEY_ENCRYPTION_1}   cwp_profile=&{ENTERPRISE_CWP_1}  auth_settings_profile=&{AUTHENTICATION_SETTINGS3}   user_access_settings=None   additional_settings=None

### Key and encryption method for ppsk network
&{PSK_KEY_ENCRYPTION3}              key_management=WPA2-(WPA2 Personal)-PSK    encryption_method=CCMP (AES)   key_type=ASCII Key  key_value=ABCD"1234


################### AUthentication configuration pofile
&{AUTHENTICATION_SETTINGS3}   auth_with_extcldiq_service=Enable    user_group_config=&{Enterprise_User_Group_Cfg1}

## User Group Config
&{Enterprise_User_Group_Cfg1}      group_name=AutoEnterprisedot1x     user_group_profile=None

################### Key and Encryption Method Options for eneterprise network
&{KEY_ENCRYPTION_1}   key_management=WPA2-802.1X    encryption_method=CCMP (AES)

#######  PPSK AUTH SETTINGS ##
&{PPSK_SETTING_DEFAULT}    client_per_ppsk=Disable    mac_binding_num_per_ppsk=Disable   pcg_use=Disable   ppsk_classification=Disable


###CWP Settings #############################
&{PPSK_CWP_DEFAULT}   enable_cwp=Disable
&{ENTERPRISE_CWP_1}   enable_cwp=Disable
&{OPEN_CWP}           enable_cwp=Disable

### User Group Settings

&{USER_GROUP_CLOUD_BULK}      group_name=${BULK_CLOUD_USER_GROUP}     user_group_profile=None     db_loc=Cloud


### Key and encryption method for ppsk network
&{PPSK_KEY_ENCRYPTION1}     key_management=WPA2-(WPA2 Personal)-PSK    encryption_method=CCMP (AES)


####################### USER GROUP PROFILES ##################################################
# DB Location and Password type:
&{DB_LOC_CLOUD_PPSK_DEFAULT}      pass_db_loc=CLOUD    pass_type=ppsk      cwp_register=Disable      pcg_use=Disable
&{bulk_users_info1}     user-type=bulk     username_prefix=user_     no_of_accounts=2       email_user_account_to=${USERS_CRED_EMAIL}

&{DB_LOC_CLOUD_RADIUS_DEFAULT}    pass_db_loc=Cloud    pass_type=radius    cwp_register=Disable

&{single_user4_info}    user-type=single                 name=symbol                             organization=ExtremeNetworks    purpose_of_visit=guest
...                     email_address=cloud1tenant1@gmail.com      phone_number=+91 India-8971766359       user_name_type=Name
...                     password=extremeextreme          pass-generate=Disable                   description=single user username password verification
...                     deliver_pass=cloud1tenant1@gmail.com

&{PASSWD_SETTING_CONFIG1}             passwd_type=RADIUS                                    letters=Enable                                 numbers=Enable
...                                   special_characters=Enable                             enforce_use_of=Any selected character types    psk_gen_method=User String Password
...                                   gen_passwd_len=12

&{USER_GROUP_PROFILE_CLOUD_BULK}      user_group_config=&{DB_LOC_CLOUD_PPSK_DEFAULT}        users_config=&{bulk_users_info1}
...                                   passwd_settings=None

&{USER_GROUP_PROFILE_Enterprise2}     user_group_config=&{DB_LOC_CLOUD_RADIUS_DEFAULT}      users_config=&{single_user4_info}
...                                   passwd_settings=&{PASSWD_SETTING_CONFIG1}             expiration_settings=None               delivery_settings=None

#########

&{PSK_CWP_DEFAULT}                  enable_cwp=Disable
*** Variables ***
&{BORADCAST_SSID_DEFAULT}       WIFI0=Enable        WIFI1=Enable

############################ Private Pre-Shared Key Wireless network profile creation ##################################
&{PPSK_UPGRADE_TEST_NW_PROFILE}       ssid_name=${PPSK_UPGRADE_TEST_SSID}      network_type=Standard    ssid_profile=&{BORADCAST_SSID_DEFAULT}      auth_profile=&{PPSK_AUTH_PROFILE_CLOUD_MULTI}
########
&{PPSK_AUTH_PROFILE_CLOUD_MULTI}       auth_type=PPSK   key_encryption=&{PPSK_KEY_ENCRYPTION1}   ppsk_config=&{PPSK_SETTING_DEFAULT}   cwp_config=&{PPSK_CWP_DEFAULT}   user_group_config=&{USER_GROUP_CLOUD_MULTIPLE}     user_access_settings_config=None   additional_settings_config=None

### Key and encryption method for ppsk network
&{PPSK_KEY_ENCRYPTION1}     key_management=WPA2-(WPA2 Personal)-PSK    encryption_method=CCMP (AES)

#######  PPSK AUTH SETTINGS ##
&{PPSK_SETTING_DEFAULT}    client_per_ppsk=Disable    mac_binding_num_per_ppsk=Disable   pcg_use=Disable   ppsk_classification=Disable

### cwp
&{PPSK_CWP_DEFAULT}   enable_cwp=Disable

### User Group Settings

&{USER_GROUP_CLOUD_MULTIPLE}      group_name=${MULTIPLE_CLOUD_USER_GROUP}     user_group_profile=None     db_loc=Cloud

####################### USER GROUP PROFILES ##################################################
# DB Location and Password type:
&{DB_LOC_CLOUD_PPSK_DEFAULT}      pass_db_loc=CLOUD    pass_type=ppsk      cwp_register=Disable      pcg_use=Disable

&{USER_GROUP_PROFILE_CLOUD_MULTIPLE}    user_group_config=&{DB_LOC_CLOUD_PPSK_DEFAULT}        users_config=&{multiple_single_user_info}
...                                   passwd_settings=None                                  expiration_settings=None               delivery_settings=None

## User Profiles

&{multiple_single_user_info}    user-type=multiple   name=${user1} ${user2} ${user3} ${user4}       organization=ExtremeNetworks            purpose_of_visit=guest
...                     email_address=${MAIL_ID1}      phone_number=+91 India-8971766359       user_name_type=Name
...                     password=${pass1} ${pass2} ${pass3} ${pass4}                pass-generate=Disable                    description=single user username password verification
...                     deliver_pass=${MAIL_ID1}

&{single_user3_info}    name=${user3}          organization=ExtremeNetworksA           purpose_of_visit=guest
...                     email_address=${MAIL_ID1}      phone_number=+91 India-8971766459       user_name_type=Name
...                     password=${pass3}                 pass-generate=Disable                    description=single user username password verification
...                     deliver_pass=${MAIL_ID1}



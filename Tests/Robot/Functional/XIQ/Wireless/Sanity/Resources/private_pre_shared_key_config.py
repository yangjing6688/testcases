import random
try:
    from Tests.Robot.Functional.XIQ.Wireless.Sanity.Resources.test_email_ids import *
except:
    try:
        from test_email_ids import *
    except:
        pass
    

RANDOM_INT = random.randint(0, 999)

OPEN_POLICY = f"PPSK_OPEN_POLICY"
OPEN_SSID = f"PPSK_OPEN_SSID"

BULK_CLOUD_NW_POLICY = f"AUTO_CLOUD_BULK_NW_{RANDOM_INT}"
BULK_CLOUD_NW_SSID = f"AUTO_CLOUD_BULK_SSID_{RANDOM_INT}"
BULK_CLOUD_USER_GROUP = f"AUTO_CLOUD_BULK_GRP_{RANDOM_INT}"

BULK_LOCAL_NW_POLICY = f"AUTO_LOCAL_BULK_NW_{RANDOM_INT}"
BULK_LOCAL_NW_SSID = f"AUTO_LOCAL_BULK_SSID_{RANDOM_INT}"
BULK_LOCAL_USER_GROUP = f"AUTO_LOCAL_BULK_GRP_{RANDOM_INT}"

SINGLE_CLOUD_NW_POLICY = f"AUTO_CLOUD_SNGLE_NW_{RANDOM_INT}"
SINGLE_CLOUD_NW_SSID = f"AUTO_CLOUD_SNG_SSID_{RANDOM_INT}"
SINGLE_CLOUD_USER_GROUP = f"AUTO_CLOUD_SNG_GRP_{RANDOM_INT}"

SINGLE_LOCAL_NW_POLICY = f"AUTO_LOCAL_SNGL_NW_{RANDOM_INT}"
SINGLE_LOCAL_NW_SSID = f"AUTO_LOCAL_SNGL_SSID_{RANDOM_INT}"
SINGLE_LOCAL_USER_GROUP = f"AUTO_LOCAL_SNGL_GRP_{RANDOM_INT}"

CLOUD_CWP_NW_POLICY = f"AUTO_PPSK_CWP_NW_{RANDOM_INT}"
CLOUD_CWP_NW_SSID = f"AUTO_PPSK_CWP_SSID_{RANDOM_INT}"
CLOUD_CWP_OPEN_NW_SSID = f"OPEN_CWP_SELF_REG_{RANDOM_INT}"
CLOUD_CWP_USER_GROUP = f"AUTO_CWP_CLOUD_GRP_{RANDOM_INT}"
SELF_REG_RETURN_PPSK_CWP = f"SELF_REG_RET_PPSK_{RANDOM_INT}"

SINGLE_CLOUD_NW_POLICY1 = f"AUTO_PPSK_CLOUD_SNGLE_NW1_{RANDOM_INT}"
SINGLE_CLOUD_NW_SSID1 = f"AUTO_PPSK_CLOUD_SNGL_SSID1_{RANDOM_INT}"
SINGLE_CLOUD_USER_GROUP1 = f"AUTO_PPSK_CLOUD_SNGL_GRP1_{RANDOM_INT}"
WRONG_PPSK_PASSWORD = f"abcdxyzss_{RANDOM_INT}"

CLIENT_PER_PPSK_POLICY = f"AUTO_CLIENT_PER_PPSK_NW_{RANDOM_INT}"
CLIENT_PER_PPSK_SSID = f"AUTO_CLIENT_PER_PPSK_SSID_{RANDOM_INT}"
CLIENT_PER_PPSK_GRP = f"AUTO_CLIENT_PER_PPSK_GRP_{RANDOM_INT}"

LOCAL_DB_PPSK_NW1 = f"LOCAL_DB_NW1_{RANDOM_INT}"
LOCAL_DB_PPSK_SSID1 = f"LOCAL_DB_SSID1_{RANDOM_INT}"
LOCAL_DB_PPSK_GROUP = f"LOCAL_DB_GRP1_{RANDOM_INT}"

self_reg_user1_info = {'email': MAIL_ID1, 'ccode': '91', 'ph_num': '8971766359', 'visitor_email': MAIL_ID2}
BORADCAST_SSID_DEFAULT = {'WIFI0': 'Enable', 'WIFI1': 'Enable'}

## User Profiles
bulk_users_info1 = {'user-type': 'bulk', 'username_prefix': 'user_', 'no_of_accounts': '2', 'email_user_account_to': MAIL_ID1}
bulk_users_info2 = {'user-type': 'bulk', 'username_prefix': 'user2_', 'no_of_accounts': '2', 'email_user_account_to': MAIL_ID1}
bulk_users_info3 = {'user-type': 'bulk', 'username_prefix': 'user100_', 'no_of_accounts': '1', 'email_user_account_to': MAIL_ID1}

single_user1_info = {'user-type': 'single', 'name': 'Symbol', 'organization': 'ExtremeNetworks', 'purpose_of_visit': 'guest',
                        'email_address': MAIL_ID1, 'phone_number': '+91 India-8971766359', 'user_name_type': 'Name',
                        'password': 'extremextreme', 'pass-generate': 'Enable', 
                        'description': 'single user username password verification', 'deliver_pass': MAIL_ID1}


single_user3_info = {'user-type': 'single', 'name': 'Jims', 'organization': 'ExtremeNetworksA',
                            'purpose_of_visit': 'guest', 'email_address': MAIL_ID1,
                            'phone_number': '+91 India-8971766459', 'user_name_type': 'Name', 'password': 'extremexxter',
                            'pass-generate': 'Enable', 'description': 'single user username password verification',
                            'deliver_pass': MAIL_ID1}

single_user2_info = {'user-type': 'single', 'name': 'Symbol1', 'organization': 'ExtremeNetworks', 'purpose_of_visit': 'guest',
                        'email_address': MAIL_ID1, 'phone_number': '+504 Honduras-8971766359', 'user_name_type': 'Phone Number',
                        'password': 'extremextreme', 'pass-generate': 'Disable', 'description': 'single user username password verification',
                        'deliver_pass': MAIL_ID1}

## Expiration Settings
EXPIRATION_SETTING1 = {'db_loc': 'Cloud', 'account_expiration': 'Valid For Time Period', 'in': '24',
                        'in_period': 'hours', 'after': 'ID Creation', 'renew_user_cred': 'Enable',
                        'delete_cred_after': 'Enable', 'delete_cred_after_time': '24', 'after_period': 'Hour',
                        'action_at_expiration': 'Show Expiration Message'}


EXPIRATION_SETTING2 = {'db_loc': 'Local', 'account_expiration': 'Valid During Dates', 
                         'action_at_expiration': 'Show Expiration Message'}

EXPIRATION_SETTING4 = {'db_loc': 'Cloud', 'account_expiration': 'Gültig für den Zeitraum', 'in': '24',
                        'in_period': 'Std.', 'after': 'ID-Erstellung', 'renew_user_cred': 'Enable',
                        'delete_cred_after': 'Enable', 'delete_cred_after_time': '24', 'after_period': 'Protokoll',
                        'action_at_expiration': 'Ablaufmeldung anzeigen'}

####################### USER GROUP PROFILES ##################################################
# DB Location and Password type:
DB_LOC_CLOUD_PPSK_DEFAULT = {'pass_db_loc': 'CLOUD', 'pass_type': 'ppsk', 'cwp_register': 'Disable', 'pcg_use': 'Disable'}
DB_LOC_CLOUD_PPSK_1 = {'pass_db_loc': 'CLOUD', 'pass_type': 'ppsk', 'cwp_register': 'Enable', 'pcg_use': 'Disable'}
DB_LOC_LOCAL_PPSK_DEFAULT = {'pass_db_loc': 'LOCAL', 'pass_type': 'ppsk', 'client_per_ppsk': 'Disable', 
                                    'pcg_use': 'Disable', 'ppsk_classification': 'Disable'}


USER_GROUP_PROFILE_CLOUD_BULK = {'user_group_config': DB_LOC_CLOUD_PPSK_DEFAULT, 'users_config': bulk_users_info1,
                                      'passwd_settings': 'None', 'expiration_settings': 'None', 'delivery_settings': 'None'}

USER_GROUP_PROFILE_CLOUD_SINGLE = {'user_group_config': DB_LOC_CLOUD_PPSK_DEFAULT, 'users_config':single_user1_info,
                                      'passwd_settings': 'None', 'expiration_settings': 'None', 'delivery_settings': 'None'}

USER_GROUP_PROFILE_LOCAL_BULK = {'user_group_config': DB_LOC_LOCAL_PPSK_DEFAULT, 'users_config': bulk_users_info2,
                                      'passwd_settings': 'None', 'expiration_settings': 'None', 'delivery_settings': 'None'}

USER_GROUP_PROFILE_LOCAL_SINGLE = {'user_group_config': DB_LOC_LOCAL_PPSK_DEFAULT, 'users_config': single_user2_info,
                                      'passwd_settings': 'None', 'expiration_settings': 'None', 'delivery_settings': 'None'}

USER_GROUP_PROFILE_CWP = {'user_group_config':DB_LOC_CLOUD_PPSK_1, 'users_config': 'None',
                                       'passwd_settings': 'None', 'expiration_settings': 'None', 'delivery_settings': 'None'}

USER_GROUP_PROFILE_CLOUD_SINGLE1 = {'user_group_config': DB_LOC_CLOUD_PPSK_DEFAULT, 'users_config': single_user3_info,
                                      'passwd_settings': 'None', 'expiration_settings': 'None', 'delivery_settings': 'None'}

USER_GROUP_PROFILE_CLOUD_BULK1 = {'user_group_config': DB_LOC_CLOUD_PPSK_DEFAULT, 'users_config': bulk_users_info3,
                                      'passwd_settings': 'None'}


USER_GROUP_PROFILE_LOCAL1 = {'user_group_config': DB_LOC_LOCAL_PPSK_DEFAULT, 'users_config': 'None',
                                      'passwd_settings': 'None', 'expiration_settings': EXPIRATION_SETTING2}

USER_GROUP_PROFILE_CLOUD1 = {'user_group_config':DB_LOC_CLOUD_PPSK_DEFAULT, 'users_config': 'None',
                                      'passwd_settings': 'None', 'expiration_settings':EXPIRATION_SETTING1}

#
DB_LOC_CLOUD_PPSK3 = {'pass_db_loc': 'WOLKE', 'pass_type': 'ppsk', 'cwp_register': 'Disable', 'pcg_use': 'Disable'}

USER_GROUP_PROFILE_CLOUD2 = {'user_group_config': DB_LOC_CLOUD_PPSK3, 'users_config': 'None', 'passwd_settings': 'None',
                                'expiration_settings': EXPIRATION_SETTING4}

# Open Network
OPEN_CWP = {'enable_cwp': 'Disable'}
OPEN_AUTHENTICATION_PROFILE0 = {'auth_type': 'Open', 'cwp_profile':OPEN_CWP}
CONFIG_PUSH_OPEN_NW_01 = {'ssid_name': OPEN_SSID, 'network_type': 'standard',
                                    'ssid_profile': BORADCAST_SSID_DEFAULT, 'auth_profile':OPEN_AUTHENTICATION_PROFILE0}

### Key and encryption method for ppsk network
PPSK_KEY_ENCRYPTION1 = {'key_management': 'WPA2-(WPA2 Personal)-PSK', 'encryption_method': 'CCMP (AES)'}

#######  PPSK AUTH SETTINGS ##
PPSK_SETTING_DEFAULT = {'client_per_ppsk': 'Disable', 'mac_binding_num_per_ppsk': 'Disable', 
                               'pcg_use': 'Disable', 'ppsk_classification': 'Disable'}
PPSK_SETTING1 = {'client_per_ppsk': 'Enable', 'num_clients': '1', 'mac_binding_num_per_ppsk': 'Disable', 
                            'pcg_use': 'Disable', 'ppsk_classification': 'Disable'}

### cwp
PPSK_CWP_DEFAULT = {'enable_cwp': 'Disable'}

### User Group Settings

USER_GROUP_CLOUD_BULK = {'group_name': BULK_CLOUD_USER_GROUP, 'user_group_profile': 'None', 'db_loc': 'Cloud'}
USER_GROUP_CLOUD_SIGNLE = {'group_name': SINGLE_CLOUD_USER_GROUP, 'user_group_profile': 'None', 'db_loc': 'Cloud'}
USER_GROUP_LOCAL_BULK = {'group_name': BULK_LOCAL_USER_GROUP, 'user_group_profile': 'None', 'db_loc': 'Local'}
USER_GROUP_LOCAL_SINGLE = {'group_name': SINGLE_LOCAL_USER_GROUP, 'user_group_profile': 'None', 'db_loc': 'Local'}
USER_GROUP_CLOUD_CWP = {'group_name': CLOUD_CWP_USER_GROUP, 'user_group_profile': 'None', 'db_loc': 'Cloud'}
USER_GROUP_CLOUD_BULK1 = {'group_name': CLIENT_PER_PPSK_GRP, 'user_group_profile': USER_GROUP_PROFILE_CLOUD_BULK1}
USER_GROUP_LOCAL1 = {'group_name': LOCAL_DB_PPSK_GROUP, 'user_group_profile': 'None', 'db_loc': 'Local'}


#USER_GROUP_CLOUD_BULK = {'group_name': BULK_CLOUD_USER_GROUP, 'user_group_profile':USER_GROUP_PROFILE_CLOUD_BULK}
USER_GROUP_CLOUD_SINGLE1 = {'group_name': SINGLE_CLOUD_USER_GROUP1, 'user_group_profile':USER_GROUP_PROFILE_CLOUD_SINGLE1}
#USER_GROUP_LOCAL_BULK = {'group_name': BULK_LOCAL_USER_GROUP, 'user_group_profile':USER_GROUP_PROFILE_LOCAL_BULK}
#USER_GROUP_LOCAL_SINGLE = {'group_name': SINGLE_LOCAL_USER_GROUP, 'user_group_profile':USER_GROUP_PROFILE_LOCAL_SINGLE}
#USER_GROUP_CLOUD_CWP = {'group_name': CLOUD_CWP_USER_GROUP, 'user_group_profile':USER_GROUP_PROFILE_CWP}

## User Access Settings Config
#&{USER_ACCESS_SETTING_CONFIG1}

### Additional Setting Config
#&{ADDITIONAL_SETTING_CONFIG}

########
PPSK_AUTH_PROFILE_CLOUD_BULK = {'auth_type': 'PPSK', 'key_encryption':PPSK_KEY_ENCRYPTION1, 
                                    'ppsk_config':PPSK_SETTING_DEFAULT, 'cwp_config':PPSK_CWP_DEFAULT, 
                                    'user_group_config':USER_GROUP_CLOUD_BULK, 'user_access_settings_config': 'None',
                                    'additional_settings_config': 'None'}
PPSK_AUTH_PROFILE_CLOUD_SINGLE = {'auth_type': 'PPSK', 'key_encryption':PPSK_KEY_ENCRYPTION1, 
                                      'ppsk_config':PPSK_SETTING_DEFAULT, 'cwp_config':PPSK_CWP_DEFAULT, 
                                      'user_group_config':USER_GROUP_CLOUD_SIGNLE, 'user_access_settings_config': 'None',
                                      'additional_settings_config': 'None'}
PPSK_AUTH_PROFILE_CLOUD_SINGLE1 = {'auth_type': 'PPSK', 'key_encryption':PPSK_KEY_ENCRYPTION1, 
                                       'ppsk_config':PPSK_SETTING_DEFAULT, 'cwp_config':PPSK_CWP_DEFAULT, 
                                       'user_group_config':USER_GROUP_CLOUD_SINGLE1, 'user_access_settings_config': 'None',
                                       'additional_settings_config': 'None'}
PPSK_AUTH_PROFILE_LOCAL_BULK = {'auth_type': 'PPSK', 'key_encryption':PPSK_KEY_ENCRYPTION1, 
                                    'ppsk_config':PPSK_SETTING_DEFAULT, 'cwp_config':PPSK_CWP_DEFAULT, 
                                    'user_group_config':USER_GROUP_LOCAL_BULK, 'user_access_settings_config': 'None', 
                                    'additional_settings_config': 'None'}
PPSK_AUTH_PROFILE_LOCAL_SINGLE = {'auth_type': 'PPSK', 'key_encryption':PPSK_KEY_ENCRYPTION1, 
                                      'ppsk_config':PPSK_SETTING_DEFAULT, 'cwp_config':PPSK_CWP_DEFAULT, 
                                      'user_group_config':USER_GROUP_LOCAL_SINGLE, 'user_access_settings_config': 'None', 
                                      'additional_settings_config': 'None'}
PPSK_AUTH_PROFILE_CWP_USER_GROUP = {'auth_type': 'PPSK', 'key_encryption':PPSK_KEY_ENCRYPTION1, 
                                    'ppsk_config':PPSK_SETTING_DEFAULT, 'cwp_config':PPSK_CWP_DEFAULT, 
                                    'user_group_config':USER_GROUP_CLOUD_CWP, 'user_access_settings_config': 'None', 
                                    'additional_settings_config': 'None'}
CLIENT_PER_PPSK_PROFILE = {'auth_type': 'PPSK', 'key_encryption':PPSK_KEY_ENCRYPTION1, 
                                       'ppsk_config':PPSK_SETTING1, 'cwp_config':PPSK_CWP_DEFAULT, 
                                       'user_group_config':USER_GROUP_CLOUD_BULK1, 'user_access_settings_config': 'None', 
                                       'additional_settings_config': 'None'}

PPSK_AUTH_PROFILE1 = {'auth_type': 'PPSK', 'key_encryption':PPSK_KEY_ENCRYPTION1, 
                                      'ppsk_config':PPSK_SETTING_DEFAULT, 'cwp_config':PPSK_CWP_DEFAULT, 
                                      'user_group_config':USER_GROUP_LOCAL1, 'user_access_settings_config': 'None', 
                                      'additional_settings_config': 'None'}
############################ Private Pre-Shared Key Wireless network profile creation ##################################
WIRELESS_PPSK_NW_CLOUD_BULK = {'ssid_name': BULK_CLOUD_NW_SSID, 'network_type': 'Standard', 
                               'ssid_profile': BORADCAST_SSID_DEFAULT, 'auth_profile': PPSK_AUTH_PROFILE_CLOUD_BULK}
WIRELESS_PPSK_NW_CLOUD_SINGLE = {'ssid_name': SINGLE_CLOUD_NW_SSID, 'network_type': 'Standard', 
                                 'ssid_profile': BORADCAST_SSID_DEFAULT, 'auth_profile': PPSK_AUTH_PROFILE_CLOUD_SINGLE}
WIRELESS_PPSK_NW_LOCAL_BULK = {'ssid_name': BULK_LOCAL_NW_SSID, 'network_type': 'Standard', 
                               'ssid_profile': BORADCAST_SSID_DEFAULT, 'auth_profile': PPSK_AUTH_PROFILE_LOCAL_BULK}
WIRELESS_PPSK_NW_LOCAL_SINGLE = {'ssid_name': SINGLE_LOCAL_NW_SSID, 'network_type': 'Standard', 
                                 'ssid_profile': BORADCAST_SSID_DEFAULT, 'auth_profile': PPSK_AUTH_PROFILE_LOCAL_SINGLE}
WIRELESS_OPEN_PPSK_NW_CLOUD_CWP = {'ssid_name': CLOUD_CWP_NW_SSID, 'network_type': 'Standard', 
                               'ssid_profile': BORADCAST_SSID_DEFAULT, 'auth_profile': PPSK_AUTH_PROFILE_CWP_USER_GROUP}
WIRELESS_CLIENT_PER_PPSK = {'ssid_name': CLIENT_PER_PPSK_SSID, 'network_type': 'Standard', 
                                    'ssid_profile': BORADCAST_SSID_DEFAULT, 'auth_profile': CLIENT_PER_PPSK_PROFILE}
WIRELESS_PPSK_NW_CLOUD_SINGLE1 = {'ssid_name': SINGLE_CLOUD_NW_SSID1, 'network_type': 'Standard', 
                                'ssid_profile': BORADCAST_SSID_DEFAULT, 'auth_profile': PPSK_AUTH_PROFILE_CLOUD_SINGLE1}
LOCAL_PPSK_NETWORK1 = {'ssid_name': LOCAL_DB_PPSK_SSID1, 'network_type': 'Standard', 
                              'ssid_profile': BORADCAST_SSID_DEFAULT, 'auth_profile': PPSK_AUTH_PROFILE1}

##############Open CWP NW With "return_aerohive_private_psk" and enable_self_reg  ######################################
PPSK_SETTINGS1 = {'choose_access_ssid': CLOUD_CWP_NW_SSID, 'choose_ppsk_server': 'Cloud PPSK Registration Server', 
                       'employee_approval': 'Disable'}
PPSK_SETTINGS2 = {'choose_access_ssid': CLOUD_CWP_NW_SSID, 'choose_ppsk_server': 'Cloud PPSK Registration Server', 
                       'employee_approval': 'Enable', 'domain': 'gmail.com'}
CWP_CONFIG1 = {'captive_web_portal_name': SELF_REG_RETURN_PPSK_CWP, 'ppsk_settings': PPSK_SETTINGS2}
OPEN_CWP_PROFILE1 = {'enable_cwp': 'Enable', 'captive_web_portal': 'Enable', 'enable_self_reg': 'Enable', 
                            'return_aerohive_private_psk': 'Enable', 'enable_upa': 'Disable', 
                            'user_auth_on_captive_web_portal': 'Disable', 'open_cwp_config': CWP_CONFIG1}
OPEN_AUTHENTICATION_CWP_PROFILE1 = {'auth_type': 'Open', 'cwp_profile': OPEN_CWP_PROFILE1}
OPEN_CWP_NW1 = {'ssid_name': CLOUD_CWP_OPEN_NW_SSID, 'network_type': 'standard', 
                       'ssid_profile': BORADCAST_SSID_DEFAULT, 'auth_profile': OPEN_AUTHENTICATION_CWP_PROFILE1}

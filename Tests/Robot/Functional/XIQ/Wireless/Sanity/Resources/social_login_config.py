import random

RANDOM_INT = random.randint(0, 9999)

NW_DEFAULT_POLICY = f"default_open_policy"
NW_DEFAULT_SSID = f"default_open_ssid"
NW_POLICY_NAME1 = f"policy_fb_{RANDOM_INT}"
NW_POLICY_NAME2 = f"policy_google_{RANDOM_INT}"
NW_POLICY_NAME3 = f"policy_linkedin_{RANDOM_INT}"
NW_POLICY_NAME4 = f"social_policy_{RANDOM_INT}"
NW_POLICY_SSID1 = f"policy_fb_{RANDOM_INT}"
NW_POLICY_SSID2 = f"policy_google_{RANDOM_INT}"
NW_POLICY_SSID3 = f"policy_linkedin_{RANDOM_INT}"
NW_POLICY_SSID4 = f"test_social_login4_{RANDOM_INT}"
NP_AUTHLOG_SSID = f"social_login_authlogs_{RANDOM_INT}"
CWP_NAME_FACEBOOK = f"cloudcwpsocialfacebook_{RANDOM_INT}"
CWP_NAME_GOOGLE = f"cloudcwpsocialgoogle_{RANDOM_INT}"
CWP_NAME_LINKEDIN = f"cloudcwpsociallinkedin_{RANDOM_INT}"
CWP_NAME_FACEBOOK1 = f"cloudcwpsocialfacebook4_{RANDOM_INT}"
NW_POLICY_NAME5 = f"social_restrict_access_{RANDOM_INT}"
NW_POLICY_SSID5 = f"social_restrict_access_{RANDOM_INT}"
NW_POLICY_NAME6 = f"cache_duration_max_limit_{RANDOM_INT}"
NW_POLICY_SSID6 = f"cache_duration_max_limit_{RANDOM_INT}"

#
EDIT_SOCIAL_CWP_CONFIG_1 = {'cwp_name': 'cloudcwpsociallinkedin', 'social_login_type_fb': 'Enable',
                             'social_login_type_google': 'Disable',  'social_login_type_linkedin': 'Disable',
                             'restrict_access': 'default', 'auth_cache_duration': 'default'}
EDIT_SOCIAL_CWP_CONFIG_2 = {'cwp_name': 'cloudcwpsocialfacebook', 'social_login_type_fb': 'Disable',
                             'social_login_type_google': 'Enable',   'social_login_type_linkedin': 'Disable',
                             'restrict_access': 'default', 'auth_cache_duration': 'default'}

SOCIAL_CWP_CONFIG_1 = {'social_login_type': 'Facebook', 'restrict_access': 'default' , 'auth_cache_duration': '2'}
SOCIAL_CWP_CONFIG_2 = {'social_login_type': 'Google', 'restrict_access': 'default' , 'auth_cache_duration': '2'}
SOCIAL_CWP_CONFIG_3 = {'social_login_type': 'Linkedin', 'restrict_access': 'default' , 'auth_cache_duration': '2'}
SOCIAL_CWP_CONFIG_4 = {'social_login_type': 'Facebook', 'restrict_access': 'default' , 'auth_cache_duration': '2'}
SOCIAL_CWP_CONFIG_5 = {'social_login_type': 'Google', 'restrict_access': 'abc.com', 'auth_cache_duration': '2'}
SOCIAL_CWP_CONFIG_6 = {'social_login_type': 'Facebook', 'restrict_access': 'default', 'auth_cache_duration': '50000'}

OPEN_CWP_CONFIG_1 = {'social_cwp_config': SOCIAL_CWP_CONFIG_1, 'cloud_cwp_name': CWP_NAME_FACEBOOK}
OPEN_CWP_CONFIG_2 = {'social_cwp_config': SOCIAL_CWP_CONFIG_2, 'cloud_cwp_name': CWP_NAME_GOOGLE}
OPEN_CWP_CONFIG_3 = {'social_cwp_config': SOCIAL_CWP_CONFIG_3, 'cloud_cwp_name': CWP_NAME_LINKEDIN}
OPEN_CWP_CONFIG_4 = {'social_cwp_config': SOCIAL_CWP_CONFIG_4, 'cloud_cwp_name': CWP_NAME_FACEBOOK1}
OPEN_CWP_CONFIG_5 = {'social_cwp_config': SOCIAL_CWP_CONFIG_5, 'cloud_cwp_name': 'socialrestrictdomain'}
OPEN_CWP_CONFIG_6 = {'social_cwp_config': SOCIAL_CWP_CONFIG_6, 'cloud_cwp_name': 'cache_duration_max_limit'}

OPEN_CWP = {'enable_cwp': 'Disable'}
OPEN_CWP_1 = {'enable_cwp': 'Enable', 'cloud_captive_web_portal': 'Enable',  'social_login': 'Enable', 'request_pin': 'Disable', 'open_cwp_config': OPEN_CWP_CONFIG_1}
OPEN_CWP_2 = {'enable_cwp': 'Enable', 'cloud_captive_web_portal': 'Enable', 'social_login': 'Enable', 'request_pin': 'Disable', 'open_cwp_config': OPEN_CWP_CONFIG_2}
OPEN_CWP_3 = {'enable_cwp': 'Enable', 'cloud_captive_web_portal': 'Enable', 'social_login': 'Enable', 'request_pin': 'Disable', 'open_cwp_config': OPEN_CWP_CONFIG_3}
OPEN_CWP_4 = {'enable_cwp': 'Enable', 'cloud_captive_web_portal': 'Enable', 'social_login': 'Enable', 'request_pin': 'Disable', 'open_cwp_config': OPEN_CWP_CONFIG_4}
OPEN_CWP_5 = {'enable_cwp': 'Enable', 'cloud_captive_web_portal': 'Enable', 'social_login': 'Enable', 'request_pin': 'Disable', 'open_cwp_config': OPEN_CWP_CONFIG_5}
OPEN_CWP_6 = {'enable_cwp': 'Enable', 'cloud_captive_web_portal': 'Enable', 'social_login': 'Enable', 'request_pin': 'Disable', 'open_cwp_config': OPEN_CWP_CONFIG_6}

OPEN_AUTHENTICATION_PROFILE0 = {'auth_type': 'Open', 'cwp_profile': OPEN_CWP}
OPEN_AUTHENTICATION_PROFILE1 = {'auth_type': 'Open', 'cwp_profile': OPEN_CWP_1}
OPEN_AUTHENTICATION_PROFILE2 = {'auth_type': 'Open', 'cwp_profile': OPEN_CWP_2}
OPEN_AUTHENTICATION_PROFILE3 = {'auth_type': 'Open', 'cwp_profile': OPEN_CWP_3}
OPEN_AUTHENTICATION_PROFILE4 = {'auth_type': 'Open', 'cwp_profile': OPEN_CWP_4}
OPEN_AUTHENTICATION_PROFILE5 = {'auth_type': 'Open', 'cwp_profile': OPEN_CWP_5}
OPEN_AUTHENTICATION_PROFILE6 = {'auth_type': 'Open', 'cwp_profile': OPEN_CWP_6}

BROADCAST_SSID_DEFAULT = {'WIFI0': 'Enable', 'WIFI1': 'Enable'}
################# Open Authentication network Profile for cloud captive web portal #####################################
CONFIG_PUSH_OPEN_NW_01 = {'ssid_name': NW_DEFAULT_SSID, 'network_type': 'standard',
                           'ssid_profile': BROADCAST_SSID_DEFAULT, 'auth_profile': OPEN_AUTHENTICATION_PROFILE0}
OPEN_NW_1 = {'ssid_name': NW_POLICY_SSID1, 'network_type': 'standard',
                           'ssid_profile': BROADCAST_SSID_DEFAULT, 'auth_profile': OPEN_AUTHENTICATION_PROFILE1}
OPEN_NW_2 = {'ssid_name': NW_POLICY_SSID2, 'network_type': 'standard',
                           'ssid_profile': BROADCAST_SSID_DEFAULT, 'auth_profile': OPEN_AUTHENTICATION_PROFILE2}
OPEN_NW_3 = {'ssid_name': NW_POLICY_SSID3, 'network_type': 'standard',
                           'ssid_profile': BROADCAST_SSID_DEFAULT, 'auth_profile': OPEN_AUTHENTICATION_PROFILE3}
OPEN_NW_4 = {'ssid_name': NW_POLICY_SSID4, 'network_type': 'standard',
                           'ssid_profile': BROADCAST_SSID_DEFAULT, 'auth_profile': OPEN_AUTHENTICATION_PROFILE4}
OPEN_NW_5 = {'ssid_name': NP_AUTHLOG_SSID, 'network_type': 'standard',
                           'ssid_profile': BROADCAST_SSID_DEFAULT, 'auth_profile': OPEN_AUTHENTICATION_PROFILE4}
OPEN_NW_6 = {'ssid_name': NW_POLICY_SSID5, 'network_type': 'standard',
                           'ssid_profile': BROADCAST_SSID_DEFAULT, 'auth_profile': OPEN_AUTHENTICATION_PROFILE5}
OPEN_NW_7 = {'ssid_name': NW_POLICY_SSID6, 'network_type': 'standard',
                           'ssid_profile': BROADCAST_SSID_DEFAULT, 'auth_profile': OPEN_AUTHENTICATION_PROFILE6}






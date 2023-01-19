*** Variables ***
${CMD_CLEAR_CLIENT_MAC}         clear auth station mac ${mu1.wifi_mac}
${CMD_CLEAR_CLIENT_SSID0}        clear auth station ssid ${SSID_NAME0}
${CMD_CLEAR_CLIENT_SSID1}        clear auth station ssid ${SSID_NAME1}
${CMD_CLEAR_CLIENT_SSID2}        clear auth station ssid ${SSID_NAME2}
${CMD_CLEAR_CLIENT_SSID3}        clear auth station ssid ${SSID_NAME3}
${CMD_CLEAR_CLIENT_SSID4}        clear auth station ssid ${SSID_NAME4}
${CMD_CLEAR_CLIENT_SSID5}        clear auth station ssid ${SSID_NAME5}
${CMD_CLEAR_CLIENT_STATION}        clear auth station
${CMD_CLEAR_CLIENT_LOCAL}       clear auth local-cache
${CMD_CLEAR_CLIENT_ROAMING}      clear auth roaming-cache
${CMD_SHOW_STATION}              show station
${POLICY_NAME0}      auto_eguest_notification_policy0
${POLICY_TYPE0}     sponsor
${POLICY_SPONSOR_NUMBER0}    8667218021
${POLICY_SPONSOR_NUMBER1}    9992929193
${POLICY_SMS0}      True
${POLICY_EMAIL0}    True
${TEMPLATE1_NAME}   accept_connect_template
${TEMPLATE2_NAME}   accept_connect_terms_template
${TEMPLATE3_NAME}   dev_reg_social_template
${TEMPLATE4_NAME}   email_access_template
${TEMPLATE5_NAME}   social_wifi_fb_gle_template
${TEMPLATE6_NAME}   social_wifi_all_template
${TEMPLATE7_NAME}   sponsored_guest_template
${TEMPLATE8_NAME}   user_reg_social_forgot_pass_template
${TEMPLATE9_NAME}   user_reg_social_wifi_template
${NW_POLICY_NAME0}  regauto_eguest_nw_policy0
${NW_POLICY_NAME1}  regauto_eguest_nw_policy1
${NW_POLICY_NAME2}  regauto_eguest_nw_policy2
${NW_POLICY_NAME3}  regauto_eguest_nw_policy3
${NW_POLICY_NAME4}  regauto_eguest_nw_policy4
${NW_POLICY_NAME5}  regauto_eguest_nw_policy5
${NW_POLICY_NAME6}  regregauto_eguest_nw_policy6
${NW_POLICY_NAME7}  auto_eguest_nw_policy7
${NW_POLICY_NAME8}  auto_eguest_nw_policy8
${NW_POLICY_NAME9}  auto_eguest_nw_policy9
${NW_POLICY_NAME10}  auto_eguest_nw_policy10
${NW_POLICY_NAME11}  auto_eguest_nw_policy11
${NW_POLICY_NAME12}  auto_eguest_nw_policy12
${NW_POLICY_NAME13}  auto_eguest_nw_policy13
${NW_POLICY_NAME14}  auto_eguest_nw_policy14
${NW_POLICY_NAME15}  auto_eguest_nw_policy15
${EG_POLICY_NAME0}  auto_eguest_onboarding_policy0
${EG_POLICY_NAME1}  auto_eguest_onboarding_policy1
${EG_POLICY_NAME2}  auto_eguest_onboarding_policy2
${EG_POLICY_NAME3}  auto_eguest_onboarding_policy3
${EG_POLICY_NAME4}  auto_eguest_onboarding_policy4
${EG_POLICY_NAME5}  auto_eguest_onboarding_policy5
${EG_POLICY_NAME6}  auto_eguest_onboarding_policy6
${EG_POLICY_NAME7}  auto_eguest_onboarding_policy7
${EG_POLICY_NAME8}  auto_eguest_onboarding_policy8
${EG_POLICY_NAME9}  auto_eguest_onboarding_policy9
${GROUP_NAME}       GuestAccess
${CONDITION_TYPE0}   Any
${CONDITION_TYPE1}   Social Type
${CONDITION_TYPE3}  Sponsor Email Domain
${CONDITION_TYPE4}  User Email Domain
${CONDITION_TYPE5}  User’s Device Count >
${CONDITION_VALUE}    gmail.com
${CONDITION_USER_VALUE}    1
${EG_RULE_NAME0}    auto_eguest_onboarding_rule0
${EG_RULE_NAME1}    auto_eguest_onboarding_rule1
${EG_RULE_NAME2}    auto_eguest_onboarding_rule2
${EG_RULE_NAME3}    auto_eguest_onboarding_rule3
${EG_RULE_NAME4}    auto_eguest_onboarding_rule4
${EG_RULE_NAME5}    auto_eguest_onboarding_rule5
${EG_RULE_NAME6}    auto_eguest_onboarding_rule6
${EG_RULE_NAME7}    auto_eguest_onboarding_rule7
${EG_RULE_NAME8}    auto_eguest_onboarding_rule8
${EG_RULE_NAME9}    auto_eguest_onboarding_rule9
${EG_RULE_NAME10}    auto_eguest_onboarding_rule10
${EG_RULE_NAME11}    auto_eguest_onboarding_rule11
${EG_RULE_NAME12}    auto_eguest_onboarding_rule12
${EG_RULE_NAME13}    auto_eguest_onboarding_rule13
${SEND_OTP_ON_APPROVAL}    Send One-Time-Passcode on Sponsor Approval
${SEND_PASSCODE_ON_APPROVAL}    Send Passcode on Sponsor Approval
${SEND_OTP_TO_SPONSOR}    Send One-Time-Passcode to Sponsor
${SEND_OTP_TO_USER}    Send One-Time-Passcode to User
${NETWORK_NAME}     test1
${SSID_NAME1}       regauto_eguest_open_social_ssid1
${SSID_NAME2}       regauto_eguest_open_social_ssid2
${SSID_NAME3}       regauto_eguest_open_social_ssid3
${SSID_NAME0}       regauto_eguest_open_ssid0
${SSID_NAME4}       regauto_eguest_open_ssid4
${SSID_NAME5}       regauto_eguest_open_ssid5
${SSID_NAME6}       regauto_eguest_open_ssid6
${SSID_NAME7}       regauto_eguest_open_ssid7
${SSID_NAME8}       regauto_eguest_open_ssid8
${SSID_NAME9}       regauto_eguest_open_ssid9
${SSID_NAME10}       regauto_eguest_open_ssid10
${SSID_NAME11}       regauto_eguest_open_ssid11
${SSID_NAME12}       regauto_eguest_open_ssid12
${SSID_NAME13}       regauto_eguest_open_ssid13
${SSID_NAME14}       regauto_eguest_open_ssid14
${SSID_NAME15}       regauto_eguest_open_ssid15

${NO_OF_VOUCHERS}   5
${ACCESS_GROUP}     GuestAccess
${LOCATION_TREE}    auto_location_03, Bengaluru, Ecospace, Floor_01
${LOCATION_TREE_01}    auto_location_03, Bengaluru, Bagmane, floor2
${MAP_FILE_NAME}    auto_location_03_Guest.tar.gz
${REPORT_NAME1}     Report-1
${REPORT_NAME2}     Report-2
${REPORT_NAME3}     Report-3
${REPORT_NAME4}     Report-4
${REPORT_TYPE1}     Guest Visit History
${REPORT_TYPE2}     Dashboard Report
${PERIOD1}          Last Day
${PERIOD2}          Last Week
${PERIOD3}          Last Month
${DASHBOARD_NAME1}  automation_db1
${DASHBOARD_NAME2}  automation_db2
${REPORT_FORMAT1}   PDF
${REPORT_FORMAT2}   CSV
${SAVE_TYPE1}       save
${SAVE_TYPE2}       run
${SAVE_TYPE3}       save-run
${USER_NAME}        extreme.guest.user
${USER_MOBILE}        8667218061
${SPONSOR_NAME}       extreme.guest.sponsor
${ACCESS_PURPOSE}     NA
${SPONSOR_PERMIT}    permit
${SPONSOR_DENY}    deny
${DEFAULT_NOTIFICATION_POLICY1}    UserNotifPolicy
${DEFAULT_NOTIFICATION_POLICY2}    SPNotifPolicy_Approval
${DEFAULT_NOTIFICATION_POLICY3}    SPNotifPolicy_Passcode
${PROGRAM}            approval
${PERMIT_SUCCESS}    Registration request has been permitted successfully
${DENY_SUCCESS}      Registration request has been denied successfully
${ACTION_PROCESSED}    The registration request is already processed.
${OVERRIDE_RESET}        No


&{GUEST_MANAGEMENT_ROLE}    email=${USER_EMAIL}     name=${USER_NAME}     timeout=30     role=GuestManagement    organization=All Organizations

&{GUEST_MANAGEMENT_MONITOR_ROLE}    email=${USER_EMAIL}     name=${USER_NAME}     timeout=30     role=Monitor    organization=All Organizations
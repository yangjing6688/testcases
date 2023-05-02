# Author        : Jeff Jones
# Date          : March 3rd 2023
# Description   : Testing keywords moved to new directory structure
#
# Topology      : N/A

*** Variables ***
${TOPO}     topo.prod.adess.va2.yaml
${ENV}      environment.local.chrome.yaml
${email}            xiqextremeqa+adess-va2@gmail.com

*** Settings ***
Variables    Environments/${TOPO}
Variables    Environments/${ENV}

*** Settings ***
Library  keywords/gui/login/KeywordsLogin.py
#Library  extauto/xiq/flows/common/Login.py


*** Test Cases ***
Test 1: Login
     ${LOGIN_STATUS}=              Login User          ${tenant_username}      ${tenant_password}     quick=True
     should be equal as integers             ${LOGIN_STATUS}               1

Test 2: Get the index of the window handle
     ${WINDOW_INDEX}=              Get Window Index
     should be equal as integers            ${WINDOW_INDEX}                0

     #${WINDOW_INDEX}=              Get Window Index  expect_error=True
     #should be equal as integers            ${WINDOW_INDEX}                -1

Test 2: Get the index of the window handle
     ${WINDOW_INDEX}=              Get Window Index
     should be equal as integers            ${WINDOW_INDEX}                0

     #${WINDOW_INDEX}=              Get Window Index  expect_error=True
     #should be equal as integers            ${WINDOW_INDEX}                -1

Test 3: Get the page title
     ${Page_title}=              Get Page Title
     should be equal            ${Page_title}                ExtremeCloud IQ

Test 4: Get the current page url
     ${Current_Page_URL}=              Get Current Page Url
     should be equal            ${Current_Page_URL}                https://va2.extremecloudiq.com/#/devices

Test 5: Get the current page base url
     ${Current_Page_base_URL}=              Get Base Url of current page
     should be equal            ${Current_Page_base_URL}                https://va2.extremecloudiq.com

Test 6: Get the XIQ Build version details
     ${XIQ_Version}=              Get_xiq_version
     should be equal            ${XIQ_Version}          23.2.1.4

Test 7: Get the VIQ ID
     ${VIQ_ID}=              Get_viq_id
     ${type string}=    Evaluate     type($VIQ_ID)
     should be equal            ${VIQ_ID}                306811

Test 8: Get the XIQ Data Center Name
     ${XIQ_datacenter_name}=              Get_data_center_name
     should be equal            ${XIQ_datacenter_name}                US_East2

Test 10: Refresh the page
     ${Page_title}=              Refresh_page

Test 11: click advance onboard popup
     ${Page_title}=              Click_advanced_onboard_popup



Test 14: Get the switch connection host
     ${connection_host}=              Get_switch_connection_host
     should be equal            ${connection_host}                	va2.extremecloudiq.com

Test 15: switch to window
     ${switch_window}=              Switch_to_window        1

Test 16: close window
     ${switch_window}=              Close_window        1

Test 17: skip_if_account_90_days
     ${switch_window}=              skip_if_account_90_days

#Test 18: verify_upgrade_option_for_connect_user
#     ${switch_window}=              verify_upgrade_option_for_connect_user

Test 18: execute_upgrade_option_for_connect_user
     ${switch_window}=              execute_upgrade_option_for_connect_user


Test 19: Logout & close browser
    Logout User
    Quit Browser


*** Comments ***

Test 9: login logo check
     ${logo}=              Logo_check_on_login_screen

Test 12: Load web page
     load_web_page

Test 13: Fogot password
     Forgot_password        _email=${email}
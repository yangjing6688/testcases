# Author        : Senthilkumar Karuppasamy
# Description   : Test Suite for Cloud Switching API - Infrastructure testing
#                   Login to a VIQ via XAPI	TC-14733
#                   Get List of Devices	TC-14738
#                   XAPI CLI Execution on a single EXOS Device	TC-14742
#                   XAPI CLI Execution on a single VOSS Device	TC-14750
#                   XAPI CLI Execution on an EXOS Stack	TC-14735
#                   Multiple XAPI CLI Execution on a single EXOS Device	TC-14739
#                   Multiple XAPI CLI Execution on a single VOSS Device	TC-14736
#                   Multiple XAPI CLI Execution on an EXOS Stack	TC-14741
#                   CLI Execution on specific EXOS Device	TC-14760
#                   CLI Execution on a specific VOSS Device	TC-14764
#                   CLI Execution on a specific EXOS Stack	TC-14767
#                   Multiple CLI Execution on specific EXOS Device	TC-14770
#                   Multiple CLI Execution on a specific VOSS Device	TC-14772
#                   Multiple CLI Execution on a specific EXOS Stack	TC-14737


*** Settings ***

Resource    Tests/Robot/Libraries/XIQ/Wired/WiredCommon.robot
Resource    Tests/Robot/Libraries/XIQ/Wired/WiredLib.robot


Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


Force Tags      testbed_1_node     

*** Variables ***
${onboard_flag}           1
${EXOSStack}              -1
${VOSSDevice}             -1
${EXOSDevice}             -1

*** Test Cases ***
TC-14733: Login to a VIQ via XAPI
    [Documentation]     Generates the access token for logging into XIQ
    [Tags]              xim_tc_14733   development   p1     test
    [Setup]  Delete Device      ${netelem1.serial}

    @{result} =    Split String    ${netelem1.serial}    ,
    FOR         ${serialnumber}     IN    @{result}
                Delete Device       device_serial=${serialnumber}
    END

    Delete Device         ${netelem1.mac}

    ${LOCATION}      Set Variable       ${location},${building},${floor}

    set global variable   ${onboard_flag}  1

    ${onboard_result}=  onboard switch     ${netelem1.serial}  device_os=${netelem1.os}   entry_type=Manual  location=${LOCATION}
	
    RUN KEYWORD IF  '${netelem1.os}' == 'exos'  Configure IQagent EXOS
    RUN KEYWORD IF  '${netelem1.os}' == 'voss'  Configure IQagent VOSS

    IF   '${netelem1.platform}' == 'Stack'
          ${onboard_result} =   Wait Until Device Online   device_mac=${netelem1.mac}
    ELSE
          ${onboard_result} =   Wait Until Device Online   ${netelem1.serial}
    END  

    IF   ${onboard_result} != 1
         set global variable   ${onboard_flag}  -1
         Log    msg="Onboarding failed, Device didn't come online.."
         should be equal as integers      ${onboard_result}          1
    END

    ${ACCESS_TOKEN}=        generate_access_token    ${TENANT_USERNAME}      ${TENANT_PASSWORD}      login

    set global variable     ${ACCESS_TOKEN}
    log to console          ${ACCESS_TOKEN}
	
	
TC-14738 : Get List of Devices
    [Documentation]     Gets the list of devices
    [Tags]              xim_tc_14738   development      p1    test 


    skip if   ${onboard_flag} == -1   msg="onboarding failed"
    
    ${output}=             rest api get             /devices
    ${deviceList}=         get json value           ${output}       data
    Log                    ${deviceList}


    ${deviceID} =   Extract By Device Mac    ${deviceList}   ${netelem1.mac}
    IF   ${deviceID} == -1
         set global variable   ${onboard_flag}  -1
         skip    msg="Device not found in VIQ"
    END


    IF   '${netelem1.os}' == 'exos' or '${netelem1.os}' == 'EXOS'
         IF   '${netelem1.platform}' == 'Stack' or '${netelem1.platform}' == 'stack'
              set global variable   ${EXOSStack}   ${deviceID} 
         ELSE
              set global variable   ${EXOSDevice}   ${deviceID}  
         END
    ELSE
         set global variable   ${VOSSDevice}   ${deviceID}   
    END  

TC-14742 : XAPI CLI Execution on a single EXOS Device
    [Documentation]     Execute a show switch CLI on an EXOS standalone switch
    [Tags]              xim_tc_14742   development  p2   

	skip if   ${onboard_flag} == -1   msg="onboarding failed"
    skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendCLI multiple devices    /devices/:cli  ${EXOSDevice}   show switch\rshow version\r
    should be equal as integers  ${status}  1

TC-14750 : XAPI CLI Execution on a single VOSS Device
    [Documentation]     Execute a show sys-info CLI on a VOSS switch
    [Tags]              xim_tc_14750   development     p2 

	skip if   ${onboard_flag} == -1   msg="onboarding failed"
    skip if  ${VOSSDevice} == -1   msg="Skipping as device is not VOSS"

    ${status}=  sendCLI multiple devices    /devices/:cli  ${VOSSDevice}   show sys-info\rshow clock\r
    should be equal as integers  ${status}  1

TC-14735 : XAPI CLI Execution on a stack
    [Documentation]     Execute a show switch CLI on an EXOS stack
    [Tags]              xim_tc_14735   development  p2

	skip if   ${onboard_flag} == -1   msg="onboarding failed"
    skip if  ${EXOSStack} == -1   msg="Skipping as device is not EXOS Stack"

    ${status}=  sendCLI multiple devices    /devices/:cli  ${EXOSStack}   show switch\rshow version\r
    should be equal as integers  ${status}  1

TC-14739 : Multiple CLI Execution on a single EXOS Device
    [Documentation]     Execute multiple CLI on an EXOS standalone switch
    [Tags]              xim_tc_14739   development  p2
	
	skip if   ${onboard_flag} == -1   msg="onboarding failed" 
    skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendCLI multiple devices    /devices/:cli  ${EXOSDevice}   show switch\rshow version\rshow mgmt\rshow configuration\r
    should be equal as integers  ${status}  1

TC-14736 : Multiple CLI Execution on a single VOSS Device
    [Documentation]     Execute Multiple CLI on a VOSS switch
    [Tags]              xim_tc_14736   development  p2

	skip if   ${onboard_flag} == -1   msg="onboarding failed"
    skip if  ${VOSSDevice} == -1   msg="Skipping as device is not VOSS"

    ${status}=  sendCLI multiple devices    /devices/:cli  ${VOSSDevice}   show sys-info\rshow clock\rshow vlan basic\rshow mgmt ip\r
    should be equal as integers  ${status}  1

TC-14741 : Multiple CLI Execution on a stack
    [Documentation]     Execute Multiple CLI on an EXOS stack
    [Tags]              xim_tc_14741   development   p2

	skip if   ${onboard_flag} == -1   msg="onboarding failed"
    skip if  ${EXOSStack} == -1   msg="Skipping as device is not EXOS Stack"

    ${status}=  sendCLI multiple devices    /devices/:cli  ${EXOSStack}   show switch\rshow version\rshow mgmt\rshow configuration\r
    should be equal as integers  ${status}  1

TC-14760 : CLI Execution on specific EXOS Device
    [Documentation]     Execute a show switch CLI on a specific EXOS switch using device endpoint
    [Tags]              xim_tc_14760   development   p2

	skip if   ${onboard_flag} == -1   msg="onboarding failed"
    skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendCLI device endpoint    ${EXOSDevice}   show switch\r
    should be equal as integers  ${status}  1

TC-14764 : XAPI CLI Execution on a single VOSS Device
    [Documentation]     Execute a show switch CLI on a specific VOSS switch using device endpoint
    [Tags]              xim_tc_14764   development   p2
 
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
    skip if  ${VOSSDevice} == -1   msg="Skipping as device is not VOSS"

    ${status}=  sendCLI device endpoint    ${VOSSDevice}   show sys-info\r
    should be equal as integers  ${status}  1

TC-14767 : XAPI CLI Execution on a stack
    [Documentation]     Execute a show switch CLI on a specific EXOS stack using device endpoint
    [Tags]              xim_tc_14767   development   p2

	skip if   ${onboard_flag} == -1   msg="onboarding failed"
    skip if  ${EXOSStack} == -1   msg="Skipping as device is not EXOS Stack"

    ${status}=  sendCLI device endpoint   ${EXOSStack}   show switch\r
    should be equal as integers  ${status}  1

TC-14770 : Multiple CLI Execution on specific EXOS Device
    [Documentation]     Execute multiple CLI on a specific EXOS switch using device endpoint
    [Tags]              xim_tc_14770   development   p2

	skip if   ${onboard_flag} == -1   msg="onboarding failed"
    skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendCLI device endpoint    ${EXOSDevice}   show switch\rshow version\rshow mgmt\rshow configuration\r
    should be equal as integers  ${status}  1

TC-14772 : Multiple CLI Execution on specific VOSS Device
    [Documentation]     Execute multiple CLI on a specific VOSS switch using device endpoint
    [Tags]              xim_tc_14772   development  p2

	skip if   ${onboard_flag} == -1   msg="onboarding failed"
    skip if  ${VOSSDevice} == -1   msg="Skipping as device is not VOSS"

    ${status}=  sendCLI device endpoint    ${VOSSDevice}   show sys-info\rshow clock\rshow vlan basic\rshow mgmt ip\r
    should be equal as integers  ${status}  1

TC-14737 : Multiple CLI Execution on specific stack
    [Documentation]     Execute multiple CLI on a specific EXOS stack using device endpoint
    [Tags]              xim_tc_14737   development   p2

	skip if   ${onboard_flag} == -1   msg="onboarding failed"
    skip if  ${EXOSStack} == -1   msg="Skipping as device is not EXOS Stack"

    ${status}=  sendCLI device endpoint   ${EXOSStack}   show switch\rshow version\rshow vlan\rshow configuration\r
    should be equal as integers  ${status}  1


*** Keywords ***

Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view and confirms the action was successful
    ${nav_result}=  Navigate to Devices
    Should Be Equal As Integers  ${nav_result}  1


Log Out of XIQ and Confirm Success
    [Documentation]     Logs out of XIQ and confirms the logout was successful
    ${result}=      Logout User

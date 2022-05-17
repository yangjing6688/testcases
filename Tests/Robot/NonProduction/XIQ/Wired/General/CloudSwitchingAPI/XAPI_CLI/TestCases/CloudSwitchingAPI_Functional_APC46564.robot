# Author        : Senthil Karuppasamy
# Description   : Test Suite for Cloud Switching API - Functional testing
#   EXOS Standalone :
#     Execute CLI for lldp port status on EXOS device TC-14768
#     Execute CLI for port Description on EXOS device  TC-14769
#     Execute CLI for port Speed Negotiation on EXOS device  TC-14771
#     Execute CLI for Storm Control Negotiation on EXOS device  TC-14775
#     Execute CLI for ELRP on EXOS device  TC-14748
#     Execute CLI for vlans on EXOS device  TC-14755
#     Execute CLI for STP on EXOS device   TC-14759
#     Execute CLI for PoE on EXOS device  TC-14763
#   EXOS Stack :
#     Execute CLI for port status on EXOS device  TC-14774
#     Execute CLI for port Description on EXOS device   TC-14780
#     Execute CLI for port Speed Negotiation on EXOS device  TC-14783
#     Execute CLI for Storm Control Negotiation on EXOS device  TC-14784
#     Execute CLI for ELRP on EXOS device  TC-14785
#     Execute CLI for vlans on EXOS device  TC-14786
#     Execute CLI for STP on EXOS device   TC-14787
#     Execute CLI for PoE on EXOS device  TC-14788
#   VOSS:
#     Execute CLI for LLDP port status on VOSS device  TC-14789
#     Execute CLI for port Description on VOSS device  TC-14790
#     Execute CLI for port Speed Negotiation on VOSS device  TC-14776
#     Execute CLI for Storm Control Negotiation on VOSS device  TC-14781
#     Execute CLI for vlans on VOSS device  TC-14777
#     Execute CLI for STP on VOSS device  TC-14782
#     Execute CLI for PoE on VOSS device  TC-14778

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
    Delete Device       ${netelem1.serial}
    @{result} =    Split String    ${netelem1.serial}    ,
    FOR		${serialnumber}     IN    @{result}
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
         Log    msg="onboarding failed, Device didn't come online"
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


TC-14768 : Execute CLI for lldp port status on EXOS device
    [Documentation]     Execute LLDP CLI on an EXOS standalone switch
    [Tags]              xim_tc_14768   development      p3
	
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
    skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendcli module device endpoint  ${EXOSDevice}  LLDP  EXOS

    should be equal as integers  ${status}  1

TC-14774 : Execute CLI for lldp port status on EXOS Stack
    [Documentation]     Execute LLDP CLI  on an EXOS stack
    [Tags]              xim_tc_14774   development      p3
 
    skip if   ${onboard_flag} == -1   msg="onboarding failed" 
    skip if  ${EXOSStack} == -1  msg="Skipping as device is not EXOS Stack"

    ${status}=  sendcli module device endpoint    ${EXOSStack}   LLDP  Stack
    should be equal as integers  ${status}  1

TC-14789 : Execute CLI for lldp port status on VOSS device
    [Documentation]     Execute LLDP CLI on a VOSS 5520 switch
    [Tags]              xim_tc_14789   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${VOSSDevice} == -1  msg="Skipping as device is not VOSS"

    ${status}=  sendcli module device endpoint    ${VOSSDevice}   LLDP  VOSS
    should be equal as integers  ${status}  1

TC-14769 : Execute CLI for port Description on EXOS device
    [Documentation]     Execute CLI for port Description on an EXOS standalone switch
    [Tags]              xim_tc_14769   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendcli module device endpoint  ${EXOSDevice}  PORTDESC  EXOS
    should be equal as integers  ${status}  1

TC-14780 : Execute CLI for port Description on EXOS Stack
    [Documentation]     Execute CLI for port Description  on an EXOS stack
    [Tags]              xim_tc_14780   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSStack} == -1  msg="Skipping as device is not EXOS Stack"

    ${status}=  sendcli module device endpoint    ${EXOSStack}   PORTDESC  Stack
    should be equal as integers  ${status}  1

TC-14790 : Execute CLI for port Description on VOSS device
    [Documentation]     Execute CLI for port Description on a VOSS 5520 switch
    [Tags]              xim_tc_14790   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${VOSSDevice} == -1  msg="Skipping as device is not VOSS"

    ${status}=  sendcli module device endpoint    ${VOSSDevice}   PORTDESC  VOSS
    should be equal as integers  ${status}  1

TC-14771 : Execute CLI for port Speed Negotiation on EXOS device
    [Documentation]     Execute CLI for port Speed Negotiation on an EXOS standalone switch
    [Tags]              xim_tc_14771   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendcli module device endpoint  ${EXOSDevice}  PORTSPEED  EXOS
    should be equal as integers  ${status}  1


TC-14783 : Execute CLI for port Speed Negotiation on EXOS Stack
    [Documentation]     Execute CLI for port Speed Negotiation  on an EXOS stack
    [Tags]              xim_tc_14783   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSStack} == -1  msg="Skipping as device is not EXOS Stack"

    ${status}=  sendcli module device endpoint    ${EXOSStack}   PORTSPEED  Stack
    should be equal as integers  ${status}  1

TC-14776 : Execute CLI for port Speed Negotiation on VOSS device
    [Documentation]     Execute CLI for port Speed Negotiation on a VOSS 5520 switch
    [Tags]              xim_tc_14776   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${VOSSDevice} == -1  msg="Skipping as device is not VOSS"

    ${status}=  sendcli module device endpoint    ${VOSSDevice}   PORTSPEED  VOSS
    should be equal as integers  ${status}  1

TC-14775 : Execute CLI for Storm Control Negotiation on EXOS device
    [Documentation]     Execute CLI for Storm Control Negotiation on an EXOS standalone switch
    [Tags]              xim_tc_14775   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendcli module device endpoint  ${EXOSDevice}  STORMCTRL  EXOS

    should be equal as integers  ${status}  1

TC-14784 : Execute CLI for Storm Control Negotiation on EXOS Stack
    [Documentation]     Execute CLI for Storm Control Negotiation  on an EXOS stack
    [Tags]              xim_tc_14784   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSStack} == -1  msg="Skipping as device is not EXOS Stack"

    ${status}=  sendcli module device endpoint    ${EXOSStack}   STORMCTRL  Stack
    should be equal as integers  ${status}  1

TC-14781 : Execute CLI for Storm Control Negotiation on VOSS device
    [Documentation]     Execute CLI for Storm Control Negotiation on a VOSS 5520 switch
    [Tags]              xim_tc_14781   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${VOSSDevice} == -1  msg="Skipping as device is not VOSS"

    ${status}=  sendcli module device endpoint    ${VOSSDevice}   STORMCTRL  VOSS
    should be equal as integers  ${status}  1

TC-14748 : Execute CLI for ELRP on EXOS device
    [Documentation]     Execute CLI for ELRP on an EXOS standalone switch
    [Tags]              xim_tc_14748   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendcli module device endpoint  ${EXOSDevice}  ELRP  EXOS

    should be equal as integers  ${status}  1

TC-14785 : Execute CLI for ELRP on EXOS Stack
    [Documentation]     Execute CLI for ELRP  on an EXOS stack
    [Tags]              xim_tc_14785   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSStack} == -1  msg="Skipping as device is not EXOS Stack"

    ${status}=  sendcli module device endpoint    ${EXOSStack}   ELRP  Stack
    should be equal as integers  ${status}  1

TC-14755 : Execute CLI for vlans on EXOS device
    [Documentation]     Execute CLI for vlans on an EXOS standalone switch
    [Tags]              xim_tc_14755   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendcli module device endpoint  ${EXOSDevice}  VLAN  EXOS

    should be equal as integers  ${status}  1

TC-14786 : Execute CLI for vlans on EXOS Stack
    [Documentation]     Execute CLI for vlans  on an EXOS stack
    [Tags]              xim_tc_14786   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSStack} == -1  msg="Skipping as device is not EXOS Stack"

    ${status}=  sendcli module device endpoint    ${EXOSStack}   VLAN  Stack
    should be equal as integers  ${status}  1

TC-14777 : Execute CLI for vlans on VOSS device
    [Documentation]     Execute CLI for vlans on a VOSS 5520 switch
    [Tags]              xim_tc_14777   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${VOSSDevice} == -1  msg="Skipping as device is not VOSS"

    ${status}=  sendcli module device endpoint    ${VOSSDevice}   VLAN  VOSS
    should be equal as integers  ${status}  1

TC-14759 : Execute CLI for STP on EXOS device
    [Documentation]     Execute CLI for STP on an EXOS standalone switch
    [Tags]              xim_tc_14759   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendcli module device endpoint  ${EXOSDevice}  STP  EXOS
    should be equal as integers  ${status}  1

TC-14787 : Execute CLI for STP on EXOS Stack
    [Documentation]     Execute CLI for STP  on an EXOS stack
    [Tags]              xim_tc_14787   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSStack} == -1  msg="Skipping as device is not EXOS Stack"

    ${status}=  sendcli module device endpoint    ${EXOSStack}   STP  Stack
    should be equal as integers  ${status}  1


TC-14782 : Execute CLI for STP on VOSS device
    [Documentation]     Execute CLI for STP on a VOSS 5520 switch
    [Tags]              xim_tc_14782   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${VOSSDevice} == -1  msg="Skipping as device is not VOSS"

    ${status}=  sendcli module device endpoint    ${VOSSDevice}   STP  VOSS
    should be equal as integers  ${status}  1

TC-14763 : Execute CLI for PoE on EXOS device
    [Documentation]     Execute CLI for PoE on an EXOS standalone switch
    [Tags]              xim_tc_14763   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendcli module device endpoint  ${EXOSDevice}  PoE  EXOS
    should be equal as integers  ${status}  1

TC-14788 : Execute CLI for PoE on EXOS Stack
    [Documentation]     Execute CLI for PoE  on an EXOS stack
    [Tags]              xim_tc_14788   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSStack} == -1  msg="Skipping as device is not EXOS Stack"

    ${status}=  sendcli module device endpoint    ${EXOSStack}   PoE  Stack
    should be equal as integers  ${status}  1

TC-14778 : Execute CLI for PoE on VOSS device
    [Documentation]     Execute CLI for PoE on a VOSS 5520 switch
    [Tags]              xim_tc_14778   development      p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${VOSSDevice} == -1  msg="Skipping as device is not VOSS"

    ${status}=  sendcli module device endpoint    ${VOSSDevice}   PoE  VOSS
    should be equal as integers  ${status}  1

*** Keywords ***


Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view and confirms the action was successful
    ${nav_result}=  Navigate to Devices
    Should Be Equal As Integers  ${nav_result}  1

Log Out of XIQ and Confirm Success
    [Documentation]     Logs out of XIQ and confirms the logout was successful
    ${result}=      Logout User

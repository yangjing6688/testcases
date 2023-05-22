# Author        : Senthil Karuppasamy
# Description   : Test Suite for Cloud Switching API - Functional testing
#   EXOS Standalone :
#     Execute CLI for lldp port status on EXOS device TCXM-14768
#     Execute CLI for port Description on EXOS device  TCXM-14769
#     Execute CLI for port Speed Negotiation on EXOS device  TCXM-14771
#     Execute CLI for Storm Control Negotiation on EXOS device  TCXM-14775
#     Execute CLI for ELRP on EXOS device  TCXM-14748
#     Execute CLI for vlans on EXOS device  TCXM-14755
#     Execute CLI for STP on EXOS device   TCXM-14759
#     Execute CLI for PoE on EXOS device  TCXM-14763
#   EXOS Stack :
#     Execute CLI for port status on EXOS device  TCXM-14774
#     Execute CLI for port Description on EXOS device   TCXM-14780
#     Execute CLI for port Speed Negotiation on EXOS device  TCXM-14783
#     Execute CLI for Storm Control Negotiation on EXOS device  TCXM-14784
#     Execute CLI for ELRP on EXOS device  TCXM-14785
#     Execute CLI for vlans on EXOS device  TCXM-14786
#     Execute CLI for STP on EXOS device   TCXM-14787
#     Execute CLI for PoE on EXOS device  TCXM-14788
#   VOSS:
#     Execute CLI for LLDP port status on VOSS device  TCXM-14789
#     Execute CLI for port Description on VOSS device  TCXM-14790
#     Execute CLI for port Speed Negotiation on VOSS device  TCXM-14776
#     Execute CLI for Storm Control Negotiation on VOSS device  TCXM-14781
#     Execute CLI for vlans on VOSS device  TCXM-14777
#     Execute CLI for STP on VOSS device  TCXM-14782
#     Execute CLI for PoE on VOSS device  TCXM-14778

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
TCXM-14733: Login to a VIQ via XAPI
    [Documentation]     Generates the access token for logging into XIQ
   
    [Tags]              tcxm_14733   production   p1

    # Sleep of 10s added as a temporary fix for XIQ-9267. Sleep needs be removed once the defect is fixed.
    Navigate to Devices and Confirm Success
    sleep    10s 

    
    IF   '${netelem1.platform}' == 'Stack' or '${netelem1.platform}' == 'stack'
	    @{result} =    Split String    ${netelem1.serial}    ,
	    FOR		${serialnumber}     IN    @{result}
			Delete Device       device_serial=${serialnumber}
	    END
    ELSE
    	    Delete Device       device_serial=${netelem1.serial}
    END
    
    Delete Device         device_mac=${netelem1.mac}

    ${LOCATION}      Set Variable       ${location},${building},${floor}

    set global variable   ${onboard_flag}  1

    ${onboard_result}=  onboard device quick     ${netelem1}

    RUN KEYWORD IF  '${netelem1.cli_type}' == 'exos'  Configure IQagent EXOS
    RUN KEYWORD IF  '${netelem1.cli_type}' == 'voss'  Configure IQagent VOSS

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
	
	
TCXM-14738 : Get List of Devices
    [Documentation]     Gets the list of devices
    [Tags]              tcxm_14738   production   p1


    skip if   ${onboard_flag} == -1   msg="onboarding failed"
    
    ${output}=             rest api get             /devices?page=1&limit=100&deviceTypes=REAL&async=false
    ${deviceList}=         get json value           ${output}       data
    Log                    ${deviceList}


    ${deviceID} =   Extract By Device Mac    ${deviceList}   ${netelem1.mac}
    IF   ${deviceID} == -1
         set global variable   ${onboard_flag}  -1
         skip    msg="Device not found in VIQ"
    END


    IF   '${netelem1.cli_type}' == 'exos' or '${netelem1.cli_type}' == 'EXOS'
         IF   '${netelem1.platform}' == 'Stack' or '${netelem1.platform}' == 'stack'
              set global variable   ${EXOSStack}   ${deviceID} 
         ELSE
              set global variable   ${EXOSDevice}   ${deviceID}  
         END
    ELSE
         set global variable   ${VOSSDevice}   ${deviceID}   
    END  


TCXM-14768 : Execute CLI for lldp port status on EXOS device
    [Documentation]     Execute LLDP CLI on an EXOS standalone switch
    [Tags]              tcxm_14768   production   p3
	
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
    skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendcli module device endpoint  ${EXOSDevice}  LLDP  EXOS

    should be equal as integers  ${status}  1

TCXM-14774 : Execute CLI for lldp port status on EXOS Stack
    [Documentation]     Execute LLDP CLI  on an EXOS stack
    [Tags]              tcxm_14774   production   p3
 
    skip if   ${onboard_flag} == -1   msg="onboarding failed" 
    skip if  ${EXOSStack} == -1  msg="Skipping as device is not EXOS Stack"

    ${status}=  sendcli module device endpoint    ${EXOSStack}   LLDP  Stack
    should be equal as integers  ${status}  1

TCXM-14789 : Execute CLI for lldp port status on VOSS device
    [Documentation]     Execute LLDP CLI on a VOSS 5520 switch
    [Tags]              tcxm_14789   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${VOSSDevice} == -1  msg="Skipping as device is not VOSS"

    ${status}=  sendcli module device endpoint    ${VOSSDevice}   LLDP  VOSS
    should be equal as integers  ${status}  1

TCXM-14769 : Execute CLI for port Description on EXOS device
    [Documentation]     Execute CLI for port Description on an EXOS standalone switch
    [Tags]              tcxm_14769   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendcli module device endpoint  ${EXOSDevice}  PORTDESC  EXOS
    should be equal as integers  ${status}  1

TCXM-14780 : Execute CLI for port Description on EXOS Stack
    [Documentation]     Execute CLI for port Description  on an EXOS stack
    [Tags]              tcxm_14780   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSStack} == -1  msg="Skipping as device is not EXOS Stack"

    ${status}=  sendcli module device endpoint    ${EXOSStack}   PORTDESC  Stack
    should be equal as integers  ${status}  1

TCXM-14790 : Execute CLI for port Description on VOSS device
    [Documentation]     Execute CLI for port Description on a VOSS 5520 switch
    [Tags]              tcxm_14790   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${VOSSDevice} == -1  msg="Skipping as device is not VOSS"

    ${status}=  sendcli module device endpoint    ${VOSSDevice}   PORTDESC  VOSS
    should be equal as integers  ${status}  1

TCXM-14771 : Execute CLI for port Speed Negotiation on EXOS device
    [Documentation]     Execute CLI for port Speed Negotiation on an EXOS standalone switch
    [Tags]              tcxm_14771   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendcli module device endpoint  ${EXOSDevice}  PORTSPEED  EXOS
    should be equal as integers  ${status}  1


TCXM-14783 : Execute CLI for port Speed Negotiation on EXOS Stack
    [Documentation]     Execute CLI for port Speed Negotiation  on an EXOS stack
    [Tags]              tcxm_14783   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSStack} == -1  msg="Skipping as device is not EXOS Stack"

    ${status}=  sendcli module device endpoint    ${EXOSStack}   PORTSPEED  Stack
    should be equal as integers  ${status}  1

TCXM-14776 : Execute CLI for port Speed Negotiation on VOSS device
    [Documentation]     Execute CLI for port Speed Negotiation on a VOSS 5520 switch
    [Tags]              tcxm_14776   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${VOSSDevice} == -1  msg="Skipping as device is not VOSS"

    ${status}=  sendcli module device endpoint    ${VOSSDevice}   PORTSPEED  VOSS
    should be equal as integers  ${status}  1

TCXM-14775 : Execute CLI for Storm Control Negotiation on EXOS device
    [Documentation]     Execute CLI for Storm Control Negotiation on an EXOS standalone switch
    [Tags]              tcxm_14775   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendcli module device endpoint  ${EXOSDevice}  STORMCTRL  EXOS

    should be equal as integers  ${status}  1

TCXM-14784 : Execute CLI for Storm Control Negotiation on EXOS Stack
    [Documentation]     Execute CLI for Storm Control Negotiation  on an EXOS stack
    [Tags]              tcxm_14784   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSStack} == -1  msg="Skipping as device is not EXOS Stack"

    ${status}=  sendcli module device endpoint    ${EXOSStack}   STORMCTRL  Stack
    should be equal as integers  ${status}  1

TCXM-14781 : Execute CLI for Storm Control Negotiation on VOSS device
    [Documentation]     Execute CLI for Storm Control Negotiation on a VOSS 5520 switch
    [Tags]              tcxm_14781   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${VOSSDevice} == -1  msg="Skipping as device is not VOSS"

    ${status}=  sendcli module device endpoint    ${VOSSDevice}   STORMCTRL  VOSS
    should be equal as integers  ${status}  1

TCXM-14748 : Execute CLI for ELRP on EXOS device
    [Documentation]     Execute CLI for ELRP on an EXOS standalone switch
    [Tags]              tcxm_14748   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendcli module device endpoint  ${EXOSDevice}  ELRP  EXOS

    should be equal as integers  ${status}  1

TCXM-14785 : Execute CLI for ELRP on EXOS Stack
    [Documentation]     Execute CLI for ELRP  on an EXOS stack
    [Tags]              tcxm_14785   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSStack} == -1  msg="Skipping as device is not EXOS Stack"

    ${status}=  sendcli module device endpoint    ${EXOSStack}   ELRP  Stack
    should be equal as integers  ${status}  1

TCXM-14755 : Execute CLI for vlans on EXOS device
    [Documentation]     Execute CLI for vlans on an EXOS standalone switch
    [Tags]              tcxm_14755   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendcli module device endpoint  ${EXOSDevice}  VLAN  EXOS

    should be equal as integers  ${status}  1

TCXM-14786 : Execute CLI for vlans on EXOS Stack
    [Documentation]     Execute CLI for vlans  on an EXOS stack
    [Tags]              tcxm_14786   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSStack} == -1  msg="Skipping as device is not EXOS Stack"

    ${status}=  sendcli module device endpoint    ${EXOSStack}   VLAN  Stack
    should be equal as integers  ${status}  1

TCXM-14777 : Execute CLI for vlans on VOSS device
    [Documentation]     Execute CLI for vlans on a VOSS 5520 switch
    [Tags]              tcxm_14777   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${VOSSDevice} == -1  msg="Skipping as device is not VOSS"

    ${status}=  sendcli module device endpoint    ${VOSSDevice}   VLAN  VOSS
    should be equal as integers  ${status}  1

TCXM-14759 : Execute CLI for STP on EXOS device
    [Documentation]     Execute CLI for STP on an EXOS standalone switch
    [Tags]              tcxm_14759   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendcli module device endpoint  ${EXOSDevice}  STP  EXOS
    should be equal as integers  ${status}  1

TCXM-14787 : Execute CLI for STP on EXOS Stack
    [Documentation]     Execute CLI for STP  on an EXOS stack
    [Tags]              tcxm_14787   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSStack} == -1  msg="Skipping as device is not EXOS Stack"

    ${status}=  sendcli module device endpoint    ${EXOSStack}   STP  Stack
    should be equal as integers  ${status}  1


TCXM-14782 : Execute CLI for STP on VOSS device
    [Documentation]     Execute CLI for STP on a VOSS 5520 switch
    [Tags]              tcxm_14782   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${VOSSDevice} == -1  msg="Skipping as device is not VOSS"

    ${status}=  sendcli module device endpoint    ${VOSSDevice}   STP  VOSS
    should be equal as integers  ${status}  1

TCXM-14763 : Execute CLI for PoE on EXOS device
    [Documentation]     Execute CLI for PoE on an EXOS standalone switch
    [Tags]              tcxm_14763   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSDevice} == -1   msg="Skipping as device is not EXOS Standalone"

    ${status}=  sendcli module device endpoint  ${EXOSDevice}  PoE  EXOS
    should be equal as integers  ${status}  1

TCXM-14788 : Execute CLI for PoE on EXOS Stack
    [Documentation]     Execute CLI for PoE  on an EXOS stack
    [Tags]              tcxm_14788   production   p3
    
	skip if   ${onboard_flag} == -1   msg="onboarding failed"
	skip if  ${EXOSStack} == -1  msg="Skipping as device is not EXOS Stack"

    ${status}=  sendcli module device endpoint    ${EXOSStack}   PoE  Stack
    should be equal as integers  ${status}  1

TCXM-14778 : Execute CLI for PoE on VOSS device
    [Documentation]     Execute CLI for PoE on a VOSS 5520 switch
    [Tags]              tcxm_14778   production   p3
    
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

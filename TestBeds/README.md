# Test Bed Standard Configurations
We have standard test bed configurations that include setups for 1-5 node DUTs, traffic generators and a primary and secondary net-tools system. The user will need to choose from the topology diagrams below in order to ensure that all tests will run on a standard test setup. 

## 1-Node Topology

![1-Node Topology](../doc/img/OneNodeTopo.png)

## 2-Node Topology

![2-Node Topology](../doc/img/TwoNodeTopo.png)

## 3-Node Topology

![3-Node Topology](../doc/img/ThreeNodeTopo.png)

## 4-Node Topology

![4-Node Topology](../doc/img/FourNodeTopo.png)

## 5-Node Topology (Legacy TCL only)

![5-Node Topology](../doc/img/FiveNodeTopo.png)

## 2-Node "Universal" Topology

![2-Node Universal Topology](../doc/img/universalTwoNodeTopo.png)

# The Test Bed Yaml Files
The test bed yaml files have been standardized to ensure that they work with the extAuto and Econ Frameworks. All devices that are used in a test bed will be defined using the options below in a yaml file. There are example test bed files located [here](https://github.com/extremenetworks/extreme_automation_tests/tree/priv_elatour_config_files_update/TestBeds/Templates). In this directory you will see the template files for the type.


### Test Bed Yaml Machine Types
All machine types are defined by the name and a number. For example the 1st and 2nd netelem should be defined as the following:
	
	netelem1
	netelem2
	tgen1
	tgen2
	endsys1
	endsys2
	
The testengine is the only machine type that does not require a number after the name. For all test bed yaml file the testengine is required and there can only be one defined.

	netelem[x]      - The Network Element (switch)
	tgen[x]	        - The Traffic Generator Element
	endsys[x]       - The End System machine	

# Type: Lab
This is the main environment section.

 |  Attribute  				 | Required | Notes |
 | ------------------------- | -------- | ----- |  
 |  lab 				     | OPTIONAL | Sets the common lab and equipments that may be used in the test |

# Type: netelem<x>
This type is the Network Element. This type of element requires a number to be placed at the end of the name. For example netelem1, netelem2. 

|  Attribute  | Required |  Notes |
| ----------- | -------- |  ----- |  
| name:       | REQUIRED | unique netelem name |
| hostname:   | REQUIRED | unique hostname |
| os:         | REQUIRED | exos/eos/linux |
| platform:   | REQUIRED |  x460G2 |
| image_family: | REQUIRED | This is the family that will be used to download the correct firmware image
| ip:         | REQUIRED |  1.1.1.3 |
| host_mac:      | OPTIONAL | 00-aa-bb-cc-dd-ee |
| username:      | REQUIRED | netelem1 username |
| password:      | REQUIRED | netelem1 password |
| connection_agent:   | REQUIRED | telnet (default) /ssh/snmp/rest |
| port:            | OPTIONAL | rewrite L4 port for static port forwarding | 
| console_ip: | OPTIONAL | The console IP
| console_port: | OPTIONAL | The console port 
| auth_mode: | OPTIONAL | The auth mode for the device
| snmp_version:    | SNMP REQUIREMENT | "v2c" # The snmp version to use (v1, v2c, or v3). |
| snmp_community_name: | SNMP REQUIREMENT | "extreme123" # The community name for v1 or v2c. |
| snmp_user_name:      | SNMP REQUIREMENT | "user_md5_des" # The user security name for v3 USM. |
| snmp_auth_protocol:  | SNMP REQUIREMENT | "md5" # The authentication protocol used by the user_name ('noauth', 'md5', or 'sha'). |
| snmp_auth_password:  | SNMP REQUIREMENT | "extreme123" # The clear text password for the auth_protocol. |
| snmp_privacy_protocol:  | SNMP REQUIREMENT | "des" # The privacy protocol used by the user_name ('nopriv', 'des', '3des', 'aes128', 'aes192', or 'aes256'). |
| snmp_privacy_password:  | SNMP REQUIREMENT | "extreme123" # The clear text password for the privacy_protocol. |
| primary_test_target:  | OPTIONAL | "True"/"False" |
| base_cfg_location:    | OPTIONAL |{path}/netelem1.cfg |
| mgmt_vlan:            | OPTIONAL |The netelem VLAN that provides connectivity outside of the test environment (i.e. lab network) - "VLAN_123" |
| management_gateway_ip:  | OPTIONAL |The IP of the router that provides connectivity outside of the test environment (i.e. lab network) - "10.52.16.17" |
| management_gateway_mac:  | OPTIONAL |The MAC of the router that provides connectivity outside of the test environment (i.e. lab network) - "20:b3:99:ad:78:fb" |
| ***power_strip:***  | | | The power strip information | 
|    --ip:          |           OPTIONAL          |               The IP for the power strip  |
|    --port:        |          OPTIONAL           |              The port for the power strip |
|    --username:    |          OPTIONAL          |              The username for the power strip  |
|    --password:    |           OPTIONAL          |               The password for the power strip |
|    --plug:        |           OPTIONAL          |               The list of plugs |
|        ----plug_a: |            OPTIONAL        |                 The 1st plug | 
|        ----plug_b: |            OPTIONAL        |                 The 2nd plug ... |
|    --type:        |           OPTIONAL          |               The type of power strip |
| template:           |      OPTIONAL       |                  AP_230-default-template |
| country:            |      OPTIONAL       |                  United Kingdom |
| network_policy:     |      OPTIONAL       |                  Test_np |
| ssid:               |      OPTIONAL       |                  AP230_01 |
| version:            |      OPTIONAL       |                  6.5 | 
| neighbour_serial:   |      OPTIONAL       |                  06301908310556 |
| neighbour_mac:      |       OPTIONAL      |                   3485843A5CC0 |
|   ***tgen:***       | | | The Tgen ports |        
|   --port_a:    | | | The Port name [port_(a-z)]|
|   ----ifname:  | REQUIRED | The netelem's interface name, as it would be entered on the device (i.e "5", "2:3" "ge.1.2" or "eth1') |
|   ----intnet:  | REQUIRED | "intnet4"  |
|   ***management:*** | | | The Management port |
|   --port_a: | | | The Port name [port_(a-z)]|
|  	----ifname: | REQUIRED | The netelem's interface name, as it would be entered on the device (i.e "5", "2:3" "ge.1.2" or "eth1') |
|  	----intnet: | REQUIRED  | "intnetmgmt1"   | 
|   ***isl:*** | | | The inter switch link | 
|   --port_a: | | | The Port name [port_(a-z)]|
|   ----ifname: | REQUIRED  | The netelem's interface name, as it would be entered on the device (i.e "5", "2:3" "ge.1.2" or "eth1') |
|   ----intnet: | REQUIRED  | "intnetisl1" |
|   ***endsys:*** | | | The End system ports |
|   --port_a: | | | The Port name [port_(a-z)]|
|   ----ifname: | REQUIRED  | The netelem's interface name, as it would be entered on the device (i.e "5", "2:3" "ge.1.2" or "eth1') |
|   ----intnet: | REQUIRED  | "intnetisl1" |

# Type: tgen<x>
This type is the Traffic Generator  Element. This type of element requires a number to be placed at the end of the name. For example tgen1, tgen1. The port will be mapped for these devices in the tgen_ports section.

|  Attribute         | Required          | Notes |
| ------------------ | ----------------- | ----- |  
| name @tgen1_name   | REQUIRED 		 | unique tgen name |
| vendor             | REQUIRED          | ixia/ostinato/spirent |
| chassis_type       | REQUIRED          | ixia/ostinato/spirent |
| software           | REQUIRED          | 5.2.3 | 
| ip       			 | REQUIRED          | 1.1.1.5 |
| vm_ipv4_address    | IXIA REQUIREMENT) | IPv4 address of Ixia Socket Listener - 1.2.3.4 |
| vm_port            | IXIA REQUIREMENT) | "5678" | 
| username           | REQUIRED          | tgen1 username | 
| password           | REQUIRED          | tgen1 password | 
| 


# Type: tgen_ports
This is where the mappings between the devices and the tgen are stated. It starts with the device name, in the example below the name netelem1. The port of the netelem1 is defined next as port_a. Then the tgen that will be used is defined and last the port of the tgen device is defined.

|  Attribute     | Required | Notes |
| -------------- | -------- | ----- |  
| netelem1:      | REQUIRED | The element name |
| --port_a:      | REQUIRED | The port name [port_(a-z)] |
| ----tgen_name: | REQUIRED | The tgen name *tgen1_name    
| ------ifname:  | REQUIRED | The tgen interface name (i.e "1/12/1" or "eth1') |
| ------intnet:  | REQUIRED | The interface name "intnet4" |
  

# Type: endsys<x>
This type is the End System. This type of element requires a number to be placed at the end of the name. For example endsys1, endsys2. 

|  Attribute          | Required | Notes |
| ------------------- | -------- | ----- |  
| name                | REQUIRED | endsys name |
| ip                  | REQUIRED | 1.1.1.2 Either the IPv4 or IPv6 Address must be used. |
| username            | REQUIRED | test engine user's name |
| connection_method   | REQUIRED | telnet/ssh/snmp/rest |
| port                | OPTIONAL | rewrite L4 port for static port forwarding |
| password            | REQUIRED | test engine user's password |

  

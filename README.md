# udp-loadbalancer
This is a stand alone python3 script.  Could be converted to a timed Lambda later.

**PREREQUISITES**  
&ensp;Python 3.9

**PURPOSE**  
&ensp;Create my own udp LB with a R53 A record holding 1 or more EC2 ipaddrs  

Automatically queries the EC2 API  
Returns ipaddrs of EC2 instances where tag:Name=‘sre-candidate’  
Write those ipaddrs to a Route53 Zone  
DNS name is ‘udp.${domain_name}’  

**INPUT**  
&ensp; Hosted ZoneID  
&ensp; Hosted Zone Domain  
&ensp; Region  
These are global variables for now.  Could be args for a future Lambda.

**NOTE**  
&ensp; This script will exit if zero (0) ipaddrs are returned (e.g. no running udp servers).  
&ensp; This is to prevent creating a udp.${domain} record with zero (0) values. 

	


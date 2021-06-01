# udp-loadbalancer
This is a stand alone python3 script.  Could be converted to a timed Lambda later.

**PREREQUISITES**  
&ensp; Python 3.x  
&ensp; boto3

**PURPOSE**  
&ensp;Create a custom "udp LB" with a R53 A record holding 1 or more EC2 ipaddrs  

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
&ensp; This script will exit if zero (0) ipaddrs are returned (e.g. no running udp servers). This is to prevent creating a udp.${domain} record with zero (0) values.  
&ensp; It will include ipaddrs only from EC2 servers which are _running_.  All other server states are excluded.    
  
**LAUNCH INSTRUCTIONS**  
```python3 ./udp-loadbalancer.py```  

**LOGGING**  
&ensp; Log verbosity is currently INFO (line 21)  
&ensp; Events are sent to console only, not to a persistent file nor a log service.  That's easy to change if the script is ported to a Lambda.


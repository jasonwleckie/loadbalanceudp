# udp-loadbalancer
This is a stand alone python3 script.  Could be converted to a timed Lambda later.

**PREREQUISITES**  
&ensp; Python 3.x  
&ensp; boto3  
&ensp; AWS Access Keypair with EC2 Describe permissions, and Route53 Describe,Create permissions

**PURPOSE**  
&ensp;Create a private "udp LB" with a R53 A record holding 1 or more EC2 private ipaddrs  

Automatically queries the EC2 API  
Returns private ipaddrs of EC2 instances where tag:Name=‘sre-candidate’  
Write those ipaddrs to a Route53 Zone, A Record ```udp.${domain_name}```  
```${domain_name}``` is dynamic and will be queried from the Zone information  

**INPUT**  
&ensp; Hosted ZoneID  
&ensp; Hosted Zone Domain  
&ensp; Region  
These are global variables for now.  Could be args for a future Lambda

**NOTE**  
&ensp; This script will exit if zero (0) private ipaddrs are returned (e.g. no running udp servers). This is to prevent creating a udp.${domain} record with zero (0) values  
&ensp; It will include private ipaddrs only from EC2 servers which are _running_.  All other server states are excluded    
&ensp; Could quickly be modified to use public ipaddrs instead    

  
**LAUNCH INSTRUCTIONS**  
```python3 ./udp-loadbalancer.py```  

**LOGGING**  
&ensp; Log verbosity is currently INFO (line 21)  
&ensp; Events are sent to console only, not to a persistent file nor a log service.  That's easy to change if the script is ported to a Lambda.


#!/usr/bin/env python3
# author: Jason Leckie
# date: June 1, 2021
# purpose: 
#   query EC2 api to find running private instances whose tag:Name is 'sre-candidate'
#   push the private ipaddr(s) to a R53 zone
#   record name should be 'udp.${domain_name} 


import boto3
import sys
import logging


ec2 = boto3.resource('ec2')

client = boto3.client('route53')

logging.basicConfig(format='%(asctime)s - %(message)s',datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

HOSTED_ZONE_ID = 'Z07654181Z3HC67SK18E6'
TAG_VALUE = 'sre-candidate'
RECORD_NAME = 'udp.' 
TTL = 300    

def send_sre_alert():
    ### stub
    pass

def list_dns_records(message):
    paginator = client.get_paginator('list_resource_record_sets')
    try:
        logger.info(message)
        source_zone_records = paginator.paginate(HostedZoneId=HOSTED_ZONE_ID)
        for record_set in source_zone_records:
            for record in record_set['ResourceRecordSets']:
                logger.info(record)
    except Exception as error:
        logger.error('An error occurred in list_dns_records:')
        logger.error(error)
        raise

def get_domain(id):
    try:
        response = client.get_hosted_zone(
            Id=id,
        )
        domain = response['HostedZone']['Name']
        logger.debug('domain is: ', domain)
        return domain
    except Exception as error:
        logger.error('An error occurred get_domain:')
        logger.error(error)
        raise        

def get_running_servers_ipaddrs(tag):
    ipaddrs = [ ]
    try:
        instances = ec2.instances.filter(
                Filters=[
                    {'Name': 'tag:Name',  'Values': [tag]},
                    {'Name': 'instance-state-name', 'Values': ['running']}
                ])
        for instance in instances:
            ipaddrs.append(instance.private_ip_address)    
        return (ipaddrs)
    except Exception as error:
        logger.error('An error occurred in get_running_servers_ipaddrs:')
        logger.error(error)
        raise 


def new_r53_records(name, ipaddrs, domain):
    ResourceRecords = [ ]
    if len(ipaddrs) == 0:
        logger.error('No servers available for UDP')
        logger.error('P1 problem - I am creating a SRE alert')
        # add a call here to SRE's alert tool's api to get someone's attention on this  
        send_sre_alert()
    else:
        for x in range(len(ipaddrs)):
            ResourceRecords.append({'Value':ipaddrs[x]})
        try:
            response = client.change_resource_record_sets(
            HostedZoneId=HOSTED_ZONE_ID,
            ChangeBatch={
                'Comment': 'comment',
                    'Changes': [
                        {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': name + domain,
                            'Type': 'A',
                            'TTL': TTL,
                            'ResourceRecords': 
                                ResourceRecords
                            }    
                        }]
            })
            logger.info('attempted DNS A record create with these values: ' + str(ipaddrs))
            list_dns_records('created UDP record.  Listing records now ')
        except Exception as error:
            logger.error('An error occurred in new_r53_records:')
            logger.error(error)
            raise 

def main():

    ### Create a new R53 record using the private ipaddrs from any running servers with the TAG_VALUE
    new_r53_records(RECORD_NAME, get_running_servers_ipaddrs(TAG_VALUE), get_domain(HOSTED_ZONE_ID))

if __name__ == "__main__":
    main()


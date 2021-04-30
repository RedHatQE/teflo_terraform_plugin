# User Guide

### To return to documentation home page press [here](https://redhatqe.github.io/teflo_linchpin_plugin/docs/index.html)

## Installation

### Install
To install the plugin you can use pip. 
```bash
pip install -e git+https://github.com/RedHatQE/teflo_terraform_plugin.git@master#egg=teflo_terraform_plugin
```

This will install 
* Teflo software from pypi
* Terraform
* Terraform plugin for Teflo

## Examples



### Run from existing terraform workspace locally
```yaml
provision:
    - name: terrfrom test
      provisioner: teflo_terraform_plugin
      groups: client, test_driver
      terraform_resource_definition:
        workspace_path: "teflo_terraform_workspace/"
        ip_output_name: "ip_addr"
```

### Run from the input parameters
```yaml
provision:
    - name: terrfrom test
      provisioner: teflo_terraform_plugin
      groups: client, test_driver
      terraform_resource_definition:
        ip_output_name: "ip_addr"
        hcl:
          provider:
            aws:
              region: us-east-1
              access_key: "{{ access_key }}"
              secret_key: "{{ secret_key }}"
          resource:
            aws_instance:
              ec2:
                instance_type: t2.micro
                ami: ami-098f16afa9edf40be
          output:
            ip_addr:
              value: "${aws_instance.ec2.public_ip}"
```

### Sample output from Teflo

```bash
--------------------------------------------------                                                                                                                                                                                                                                                                                                                                                                                                                                          
Teflo Framework v1.1.0                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
Copyright (C) 2020, Red Hat, Inc.                                                                                                                                                                                                                                                                                                                                                                                                                                                           
--------------------------------------------------                                                                                                                                                                                                                                                                                                                                                                                                                                          
2021-04-26 15:19:16,056 WARNING Scenario workspace was not set, therefore the workspace is automatically assigned to the current working directory. You may experience problems if files needed by teflo do not exists in the scenario workspace.                                                                                                                                                                                                                                           
2021-04-26 15:19:16,325 INFO                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
2021-04-26 15:19:16,326 INFO                                TEFLO RUN (START)                                                                                                                                                                                                                                                                                                                                                                                                               
2021-04-26 15:19:16,326 INFO -------------------------------------------------------------------------------                                                                                                                                                                                                                                                                                                                                                                                
2021-04-26 15:19:16,326 INFO  * Data Folder           : /tmp/4hzksm83d7                                                                                                                                                                                                                                                                                                                                                                                                                     
2021-04-26 15:19:16,327 INFO  * Workspace             : /home/junqizhang/terra/teflo                                                                                                                                                                                                                                                                                                                                                                                                        
2021-04-26 15:19:16,327 INFO  * Log Level             : info                                                                                                                                                                                                                                                                                                                                                                                                                                
2021-04-26 15:19:16,327 INFO  * Tasks                 : ['provision']                                                                                                                                                                                                                                                                                                                                                                                                                       
2021-04-26 15:19:16,328 INFO  * Scenario              : py3_included_scenario_linchpin                                                                                                                                                                                                                                                                                                                                                                                                      
2021-04-26 15:19:16,328 INFO -------------------------------------------------------------------------------                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
2021-04-26 15:19:16,328 INFO  * Task    : provision                                                                                                                                                                                                                                                                                                                                                                                                                                         
2021-04-26 15:19:16,329 INFO Sending out any notifications that are registered.                                                                                                                                                                                                                                                                                                                                                                                                             
2021-04-26 15:19:16,329 INFO ..................................................                                                                                                                                                                                                                                                                                                                                                                                                             
2021-04-26 15:19:16,330 INFO Starting tasks on pipeline: notify                                                                                                                                                                                                                                                                                                                                                                                                                             
2021-04-26 15:19:16,330 WARNING ... no tasks to be executed ...                                                                                                                                                                                                                                                                                                                                                                                                                             
2021-04-26 15:19:16,331 INFO ..................................................                                                                                                                                                                                                                                                                                                                                                                                                             
2021-04-26 15:19:16,331 INFO Starting tasks on pipeline: provision                                                                                                                                                                                                                                                                                                                                                                                                                          
2021-04-26 15:19:16,332 INFO --> Blaster v0.4.0 <--                                                                                                                                                                                                                                                                                                                                                                                                                                         
2021-04-26 15:19:16,332 INFO Task Execution: Concurrent                                                                                                                                                                                                                                                                                                                                                                                                                                     
2021-04-26 15:19:16,333 INFO Tasks:                                                                                                                                                                                                                                                                                                                                                                                                                                                         
2021-04-26 15:19:16,334 INFO 1. Task     : terrfrom test                                                                                                                                                                                                                                                                                                                                                                                                                                    
                                Class    : <class 'teflo.tasks.provision.ProvisionTask'>                                                                                                                                                      
                                Methods  : ['run']                                                                     
2021-04-26 15:19:16,334 INFO ** BLASTER BEGIN **                                                                       
2021-04-26 15:19:16,356 INFO    provisioning asset terrfrom test                                                       
2021-04-26 15:19:16,357 INFO Provisioning asset terrfrom test.                                                         

Initializing the backend...                                                                                            

Initializing provider plugins...                                                                                       
- Reusing previous version of hashicorp/aws from the dependency lock file                                              
- Using previously-installed hashicorp/aws v3.37.0                                                                     

Terraform has been successfully initialized!                                                                           

You may now begin working with Terraform. Try running "terraform plan" to see                                          
any changes that are required for your infrastructure. All Terraform commands                                          
should now work.                                                                                                       

If you ever set or change modules or backend configuration for Terraform,                                              
rerun this command to reinitialize your working directory. If you forget, other                                                                                                                                                               
commands will detect it and remind you to do so if necessary.                                                          
2021-04-26 15:20:03,172 INFO {'name': 'terrfrom test', 'ip': '54.145.118.168'}                                         
2021-04-26 15:20:03,176 INFO Successfully provisioned asset terrfrom test with asset_id None.                                                                                                                                                 
2021-04-26 15:20:03,186 INFO ** BLASTER COMPLETE **                                                                    
2021-04-26 15:20:03,188 INFO     -> TOTAL DURATION: 0h:0m:46s                                                          
2021-04-26 15:20:03,244 INFO Populating master inventory file with host(s) terrfrom test                                                                                                                                                      
2021-04-26 15:20:03,245 INFO ..................................................                                                                                                                                                               
2021-04-26 15:20:03,246 INFO Sending out any notifications that are registered.                                                                                                                                                               
2021-04-26 15:20:03,246 INFO ..................................................                                                                                                                                                               
2021-04-26 15:20:03,247 INFO Starting tasks on pipeline: notify                                                        
2021-04-26 15:20:03,247 WARNING ... no tasks to be executed ...                                                        
2021-04-26 15:20:03,252 INFO                                                                                           

2021-04-26 15:20:03,252 INFO                                SCENARIO RUN (END)                                                                                                                                                                
2021-04-26 15:20:03,252 INFO -------------------------------------------------------------------------------                                                                                                                                  
2021-04-26 15:20:03,252 INFO  * Duration                       : 0h:0m:46s                                             
2021-04-26 15:20:03,253 INFO  * Passed Tasks                   : ['provision']                                         
2021-04-26 15:20:03,253 INFO  * Results Folder                 : /tmp/.results                                         
2021-04-26 15:20:03,253 INFO  * Included Scenario Definition   : []                                                    
2021-04-26 15:20:03,254 INFO  * Final Scenario Definition      : /tmp/.results/results.yml                                                                                                                                                    
2021-04-26 15:20:03,254 INFO -------------------------------------------------------------------------------                                                                                                                                  
2021-04-26 15:20:03,254 INFO TEFLO RUN (RESULT=PASSED) 
```
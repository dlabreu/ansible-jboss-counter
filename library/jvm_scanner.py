#!/usr/bin/python

# Copyright: (c) 2024, Francis Viviers <fviviers@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from tempfile import NamedTemporaryFile
import subprocess

DOCUMENTATION = r'''
---
module: verify_jvm_linux

short_description: Module to Scan for JDK, Versions, Libraries used etc for counting usage / subscriptions


version_added: "1.0.0"

description: Scan JDK Usage

#options:
#    secret: Secret contianing the Gitops Admin password
#    namespace: Namespace GitOps Operator
#    url: URL where GitOps is running
#    port: Port on which GitOps is running/exposed
#    application: Application within GitOps to sync

author:
    - Francis Viviers (@cainza)
'''

EXAMPLES = r'''

To test this module:

python library/sync_gitops_application.py /tmp/args.json
cat args.json 

{
    "ANSIBLE_MODULE_ARGS": {
        "jdk": "yes"
    }
}

'''

RETURN = r'''

{"changed": true, "invocation": {"module_args": {"name": "openshift-gitops-operator", "namespace": "openshift-operators", "group": "operators.coreos.com", "version": "v1", "plural": "operators", "timeout": 600}}}

'''

from ansible.module_utils.basic import AnsibleModule

# Import Kubernetes Requirements
from pprint import pprint
import time
import os
# Check for OS
from sys import platform
import psutil # sudo dnf install psutils.noarch
import re
import subprocess
from pathlib import Path

def check_os():
    
    if platform == "linux" or platform == "linux2":
        pprint("linux")
        return "linux"
    
    elif platform == "win32":
        pprint ("Windows")
        return False #"win32"
    else:
        pprint ("some other OS")
        return False

def get_windows_processes():

    pprint ("Windows processes")
    #https://www.geeksforgeeks.org/python-get-list-of-running-processes/

def identify_jdk(javapath):

    if javapath == "java":
        # Find full path
        javapath = subprocess.run(['which', javapath], stdout=subprocess.PIPE)
        javapath = (str(javapath.stdout, 'utf-8').strip())

    result = subprocess.run(['rpm', '-qf', javapath], stdout=subprocess.PIPE)
    javapackage = str(result.stdout, 'utf-8').strip()
    return javapackage

def identify_jws(processargs):
    

    for arg in processargs:
        
        # Match Catalina Base argument
        if re.match(".*catalina.base=.*", arg):

            catalinabase = arg.split("=")[1]
            #print ("Found Catalina base: " + catalinabase)
            if os.path.exists( ("%s/bin/tomcat-juli.jar" % catalinabase)):
                # Logic if version file still exists
                versiontxt = "%s/../version.txt" % catalinabase
                with open(versiontxt) as f:
                    if 'redhat' in f.read():
                        return "Red Hat JWS Running"
                    # Add additional Logic for identification!!!    
                    else:
                        return "Community Tomcat"                   
        
    return "No JWS Found Running"

def identify_eap(processargs):

    for arg in processargs:

        # Match JBOSS Home Dir argument
        if re.match(".*jboss.home.dir=.*", arg):
            
            # Get JBOSS Home path
            jbosshome = arg.split("=")[1]

            if os.path.exists( "%s/version.txt" % jbosshome):
                version = open("%s/version.txt" % jbosshome, 'r').read().strip()
            else:
                version = ""
            
            if re.match(".*Red Hat JBoss Enterprise Application Platform - Version.*", version):
                return version

            modulelist = subprocess.run(['find', "%s/modules" % jbosshome], stdout=subprocess.PIPE)
            for module in  str(modulelist.stdout, 'utf-8').split("\n"):

                if re.match(".*.redhat-.*.jar", module):
                    return "Red Hat EAP Found"

            return "Community Wildfly found"           

    return "No EAP / Wildfly found"

def identify_rhbk(processargs):

    print ("Finding Keycloak") 

    if "io.quarkus.bootstrap.runner.QuarkusEntryPoint" in processargs:
        print ("Quarkus runtime")

        for arg in processargs:
    
            # Match JBOSS Home Dir argument
            if re.match(".*kc.home.dir=.*", arg):
                kc_home = arg.split("=")[1]

                if os.path.exists( "%s/version.txt" % kc_home):
                    version = open("%s/version.txt" % kc_home, 'r').read().strip()
                else:
                    version = "Red Hat Build of Keycloak"
        return version
    return "None"

def identify_linux_java_processes(processinfo):

    # Check if java running or not
    if len(processinfo) != 0:

        # Identify which java package is being used for process
        javapackage = identify_jdk(processinfo[0])
        print ("Used Java package: " + javapackage)

        # Check if process shows information for Red Hat JWS / Apache Tomcat
        jws = identify_jws(processinfo)
        print ("Used RH JWS / Tomcat: " + jws)

        # Check if process shows information for Red Hat EAP
        eap = identify_eap(processinfo)
        print ("Used RH EAP / Wildfly: " + eap)

        # Check if process shows information for Red Hat Keycloak
        # OLD SSO will be detected on EAP Section
        keycloak = identify_rhbk(processinfo)
        print ("Used Red Hat build of Keycloak / Community: " + keycloak)
    
    # Check if process shows information for Red Hat Fuse
    # Check if process shows information for Red Hat Quarkus

    #print (processinfo)

    # ISSUES:
    

def identify_linux_java_quarkus_processes():
    
    print ("Identifying Quarkus based workloads - binary")


def get_linux_processes():

    processes = psutil.process_iter()
    for process in processes:
        if re.match(".*java.*", process.name()):

            # JDK Based Middleware
            identify_linux_java_processes (psutil.Process(process.pid).cmdline())

            # Quarkus based Middleware
            #identify_linux_java_quarkus_processes()
            
    #import psutil
    #processes = psutil.process_iter()
    #for process in processes:
    #    print(f"Process ID: {process.pid}, Name: {process.name()}")

def scan_java():

    if check_os() == "linux":
        get_linux_processes()
        return "linux"
    elif check_os() == "win32":
        get_windows_processes()
        return "windows"
    else:
        return False
    #sh-5.1$ cat /proc/1/environ
    #PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    #TERM=xtermHOSTNAME=rhbk-operator-77b6d6cf45-czm2rNSS_SDB_USE_CACHE=no
    #RELATED_IMAGE_KEYCLOAK=registry.redhat.io/rhbk/keycloak-rhel9@sha256:1983814b4f98b505e31e25df3a16ea3134a1a6b4a693c173865c02283dd61b41
    #QUARKUS_OPERATOR_SDK_CONTROLLERS_KEYCLOAKCONTROLLER_NAMESPACES=authentication
    #QUARKUS_OPERATOR_SDK_CONTROLLERS_KEYCLOAKREALMIMPORTCONTROLLER_NAMESPACES=authenticationPOD_NAME=rhbk-operator-77b6d6cf45-czm2r
    #OPERATOR_NAME=rhbk-operatorOPERATOR_CONDITION_NAME=rhbk-operator.v24.0.3-opr.1
    #KUBERNETES_SERVICE_PORT_HTTPS=443
    #KUBERNETES_PORT=tcp://172.30.0.1:443KUBERNETES_PORT_443_TCP=tcp://172.30.0.1:443KUBERNETES_PORT_443_TCP_PROTO=tcp
    #KUBERNETES_PORT_443_TCP_PORT=443
    #KUBERNETES_PORT_443_TCP_ADDR=172.30.0.1
    #KUBERNETES_SERVICE_HOST=172.30.0.1
    #KUBERNETES_SERVICE_PORT=443LANG=en_US.UTF-8HOME=/sh-5.1$ cat /proc/1/environ 

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(    
        jdk=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Generate the subscription
    sync_status = scan_java()

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['changed'] = sync_status

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if result['changed'] == False:
        module.fail_json(msg='Middleware could not be scanned', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
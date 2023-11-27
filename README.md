
# Running the Ansible Playbook for Checking JBoss/WildFly and Fuse/Apache Camel Installation


## Prerequisites

- **Ansible Installed**: Ensure Ansible is installed on your local machine or control node. You can install it using package managers like `apt`, `yum`, or `brew`.
  
  Example for Fedora/RHEL:
  ```bash
  $ sudo yum update -y
  $ sudo yum install ansible -y
  ```

- **Inventory Configuration**: Modify the `inventory.ini` file to include the target hosts' IP addresses or hostnames. Ensure SSH access to these hosts is properly configured.


- **Ensure Target Hosts Are Reachable**: Verify that the target hosts are reachable from the control node where Ansible is being executed. You can use `ping` or `ssh` commands to ensure connectivity. Bellow is an simple test.

  ```bash
  ansible -i inventory.ini all -m ping
  ``` 
The above command will try to log in into each one of your target nodes and do an ping from withing the node to ensure it can shell into it and execute the command. 


## Steps to Run the Playbook

1. **Clone the Repository**:
   
   ```bash
   $ git clone [repository_url]
   $ cd [repository_directory]
   ```

2. **Update Variables (if required)**:
   
   If needed for your environment, modify the variables in `vars/` or `group_vars/` directory within the playbook.

3. **Execute the Playbook**:

   Run the playbook with the following command:

   ```bash
   $ ansible-playbook -i inventory.ini playbook.yml
   ```

   Replace `playbook.yml` with the actual name of your playbook file if it differs.

4. **Review the Excel Report**:

   Upon successful execution, the playbook will generate an Excel spreadsheet containing the collected data. You can find this report at the location specified by the `excel_loc` variable in the playbook.

## Additional Notes

- **Output Interpretation**:
  - The Excel report will contain details about the hostname, operating system, vCPU count, and the presence of JBoss/WildFly and Fuse/Apache Camel installations.
  - "yes" or "no" values will indicate the presence or absence of JBoss/WildFly and Fuse/Apache Camel respectively.

- **Troubleshooting**:
  - In case of any errors during playbook execution, review the output for any failure messages or check the Ansible logs for detailed information.
  - Ensure proper permissions and access to the specified locations (such as the Excel report path).

- **Customization**:
  - Customize the playbook variables or inventory to suit your specific environment or requirements.
  - Refer to the playbook tasks and modify them as necessary for more detailed checks or additional data collection.

## Need Help or Assistance?

For any further assistance, questions, or issues related to running the playbook, please contact dleitede@redhat.com.
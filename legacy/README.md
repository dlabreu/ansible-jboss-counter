# ansible-jboss-windows-counter
This playbook collect jboss and fuse counts on windows, this playbook uses a Jinja template and loops through the group hosts while writing once. 

Keep the j2 template in the same project folder as the eap playbook

It is important to note, if you are using tower or controler to run this playbook, to just allow writing to the local filesystem.

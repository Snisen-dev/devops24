# Examination 7 - MariaDB installation

To make a dynamic web site, many use an SQL server to store the data for the web site.

[MariaDB](https://mariadb.org/) is an open-source relational SQL database that is good
to use for our purposes.

We can use a similar strategy as with the _nginx_ web server to install this
software onto the correct host(s). Create the playbook `07-mariadb.yml` with this content:

    ---
    - hosts: db
      become: true
      tasks:
        - name: Ensure MariaDB-server is installed.
          ansible.builtin.package:
            name: mariadb-server
            state: present

# QUESTION A

Make similar changes to this playbook that we did for the _nginx_ server, so that
the `mariadb` service starts automatically at boot, and is started when the playbook
is run.

# QUESTION B

When you have run the playbook above successfully, how can you verify that the `mariadb`
service is started and is running?

Answer: There are lots of ways to check if the service is running. I would say that the easiest is to run the the playbook again. If no changes have happened and no errors occur then the service should be running. You can also ssh to the server and check manually. You can also use ansible to check directly in the terminal with ansible db -a "systemctl is-active mariadb" where the -a flah are arguments.

# BONUS QUESTION

How many different ways can use come up with to verify that the `mariadb` service is running?

It depends on what you mean by different ways.
On the server: 
* systemctl
* ps
* mysql
* Using a db viewer ex. dbeaver (if you have a display manager)

On the host:
* run the playbook again
* use ansible without playbook 
* using ansible with register
# Examination 5 - Handling Configuration Changes

Today, plain HTTP is considered insecure. Most public facing web sites use the encrypted HTTPS
protocol.

In order to set up our web server to use HTTPS, we need to make a configuration change in nginx.

## Preparations

Begin by running the [install-cert.yml](install-cert.yml) playbook to generate a self-signed certificate
in the correct location on the webserver.

You may need to install the Ansible `community.crypto` collection first, unless you have
already done so earlier.

In the `lab_environment` folder, there is a file called `requirements.yml` that can be used like this:

    $ ansible-galaxy collection install -r requirements.yml

Or, if you prefer, you can install the collection directly with

    $ ansible-galaxy collection install community.crypto

# HTTPS configuration in nginx

The default nginx configuration file suggests something like the following to be added to its
configuration:

    server {
        listen       443 ssl;
        http2        on;
        server_name  _;
        root         /usr/share/nginx/html;

        ssl_certificate "/etc/pki/nginx/server.crt";
        ssl_certificate_key "/etc/pki/nginx/private/server.key";
        ssl_session_cache shared:SSL:1m;
        ssl_session_timeout  10m;
        ssl_ciphers PROFILE=SYSTEM;
        ssl_prefer_server_ciphers on;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;
    }

There are many ways to get this configuration into nginx, but we are going to copy
this as a file into `/etc/nginx/conf.d/https.conf` with Ansible with the
[ansible.builtin.copy](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html)
module.

If you have gone through the preparation part for this examinination, the certificate and the key for the
certificate has already been created so we don't need to worry about that.

In this directory, there is already a file called `files/https.conf`. Copy this directory to your Ansible
working directory, with the contents intact.

Now, we will create an Ansible playbook that copies this file via the `ansible.builtin.copy` module
to `/etc/nginx/conf.d/https.conf`.

# QUESTION A

Create a playbook, `05-web.yml` that copies the local `files/https.conf` file to `/etc/nginx/conf.d/https.conf`,
and acts ONLY on the `web` group from the inventory.

Refer to the official Ansible documentation for this, or work with a classmate to
build a valid and working playbook, preferrably that conforms to Ansible best practices.

Run the playbook with `ansible-playbook` and `--verbose` or `-v` as option:

    $ ansible-playbook -v 05-web.yml

The output from the playbook run contains something that looks suspiciously like JSON, and that contains
a number of keys and values that come from the output of the Ansible module.

What does the output look like the first time you run this playbook?

Answer:
´´´Bash
➜  ansible ansible-playbook 05-web.yml

PLAY [Configure HTTPS for nginx] ***********************************************************************

TASK [Gathering Facts] *********************************************************************************
ok: [192.168.121.31]

TASK [Copy HTTPS configuration to nginx] ***************************************************************
changed: [192.168.121.31]

PLAY RECAP *********************************************************************************************
192.168.121.31             : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

➜  ansible ansible-playbook -v 05-web.yml
Using /home/snis/ansible/ansible.cfg as config file

PLAY [Configure HTTPS for nginx] ***********************************************************************

TASK [Gathering Facts] *********************************************************************************
ok: [192.168.121.31]

TASK [Copy HTTPS configuration to nginx] ***************************************************************
ok: [192.168.121.31] => {"changed": true, "checksum": "4928f5d40694d15bf3e276596d47b8fc75544d59", "dest": "/etc/nginx/conf.d/https.conf", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/nginx/conf.d/https.conf", "secontext": "system_u:object_r:httpd_config_t:s0", "size": 465, "state": "file", "uid": 0}

PLAY RECAP *********************************************************************************************
192.168.121.31             : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

➜  ansible ansible-playbook -v install-cert.yml
Using /home/snis/ansible/ansible.cfg as config file

PLAY [Set up self-signed certificates for HTTPS] *******************************************************

TASK [Gathering Facts] *********************************************************************************
ok: [192.168.121.31]

TASK [Ensure the /etc/pki/nginx directory exists] ******************************************************
ok: [192.168.121.31] => {"changed": true, "gid": 0, "group": "root", "mode": "0755", "owner": "root", "path": "/etc/pki/nginx", "secontext": "unconfined_u:object_r:cert_t:s0", "size": 39, "state": "directory", "uid": 0}

TASK [Ensure we have a /etc/pkig/nginx/private directory] **********************************************
ok: [192.168.121.31] => {"changed": true, "gid": 0, "group": "root", "mode": "0700", "owner": "root", "path": "/etc/pki/nginx/private", "secontext": "unconfined_u:object_r:cert_t:s0", "size": 24, "state": "directory", "uid": 0}

TASK [Ensure we have necessary software installed] *****************************************************
ok: [192.168.121.31] => {"changed": true, "msg": "Nothing to do", "rc": 0, "results": []}

TASK [Ensure we have a private key for our certificate] ************************************************
ok: [192.168.121.31] => {"changed": true, "filename": "/etc/pki/nginx/private/server.key", "fingerprint": {"blake2b": "bb:cd:37:2b:5d:22:dc:48:0b:f2:99:6b:f2:96:d4:b5:b3:3e:60:3d:62:19:5f:91:22:f3:50:9c:b3:9e:97:7a:23:61:3e:56:62:7c:ce:4d:70:d2:75:c4:ca:44:53:50:3d:ad:cc:78:fc:5e:c2:1d:03:36:1a:3e:57:c3:ed:e5", "blake2s": "eb:6c:28:21:00:81:dd:e8:a6:b8:7f:42:e8:86:a7:80:dd:1f:85:f3:b7:c9:f7:33:85:b9:e0:9e:65:e4:9b:4e", "md5": "4b:a5:80:3c:f1:f4:0c:f9:92:57:7c:92:2a:bb:12:18", "sha1": "00:6a:97:7b:c5:b0:cf:6b:d3:b9:f7:1c:6a:72:78:cf:5a:a9:35:d9", "sha224": "7d:52:65:b3:c3:2e:27:16:f9:00:b9:0f:98:e3:ab:a1:0c:e7:00:36:c7:5d:78:83:bd:78:01:f3", "sha256": "f4:21:4c:1d:7c:e9:f8:a2:e7:3a:be:65:1f:7b:63:29:b7:ca:c8:61:2e:25:f9:81:7e:cb:3c:f3:06:2c:b4:90", "sha384": "bf:aa:c4:7e:2b:22:85:cb:c3:50:91:b7:2a:c0:93:57:55:0d:54:40:fc:a0:22:8f:ae:1b:07:3c:fd:db:70:25:08:6c:7e:7c:21:52:ad:a8:25:6b:8a:c2:35:60:16:65", "sha3_224": "28:ae:b3:4a:f5:6c:ed:bf:f6:e6:2a:05:b8:f4:a5:d4:2c:d1:96:5d:a8:c1:85:c7:fc:d9:d0:d7", "sha3_256": "20:0a:00:3f:a0:66:a1:c1:6a:ad:d3:a5:8b:dd:5d:7e:4c:4c:2e:54:b1:cf:d2:91:cf:60:64:10:89:16:b0:7b", "sha3_384": "ec:0b:4c:be:10:aa:00:d7:72:f4:d6:6a:b5:29:dc:e1:32:d5:f8:84:04:ea:f6:ae:4e:78:c4:80:0e:62:28:8f:70:b5:23:64:e6:07:f4:4d:64:e3:bf:65:4d:7e:8c:60", "sha3_512": "d7:10:55:e1:75:85:fb:20:74:9e:e8:f9:69:a5:72:c1:7c:94:7b:93:0d:79:a3:bc:3f:3f:c9:27:46:fe:fc:66:84:78:fc:1d:bf:a3:80:3a:09:c3:51:0e:8f:d0:40:de:7a:9d:c0:9a:9b:79:cd:a4:91:85:38:c3:51:61:ed:53", "sha512": "29:57:55:1c:73:5b:70:12:14:ab:4a:82:6c:78:ed:a2:f1:d2:17:b3:e6:21:9b:53:6a:a5:67:b3:3b:04:84:5d:ac:04:c1:82:08:9b:ea:c0:4c:5f:0d:37:79:76:67:36:af:7b:46:e6:1f:90:3a:05:5c:fd:f2:ee:b9:e7:61:cf", "shake_128": "cc:51:cf:57:24:7c:25:05:ae:ba:85:23:ca:31:bc:b2:f3:42:9d:b3:df:77:76:8e:5a:5a:c1:eb:d8:74:d6:41", "shake_256": "fd:25:01:65:87:9b:48:3f:03:d2:ec:ba:7a:79:61:38:b3:47:c7:39:d0:d9:8a:d7:a1:ee:71:6f:7b:6f:4b:a0"}, "size": 4096, "type": "RSA"}

TASK [Create a self-signed certificate] ****************************************************************
ok: [192.168.121.31] => {"changed": true, "csr": null, "filename": "/etc/pki/nginx/server.crt", "notAfter": "20351018223911Z", "notBefore": "20251020223911Z", "privatekey": "/etc/pki/nginx/private/server.key", "serial_number": 146032914911275965452871370599420539465875725483}

PLAY RECAP *********************************************************************************************
192.168.121.31             : ok=6    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
What does the output look like the second time you run this playbook?

Answer: It looks the same but the changed: is false instead of true


# QUESTION B

Even if we have copied the configuration to the right place, we still do not have a working https service
on port 443 on the machine, which is painfully obvious if we try connecting to this port:

    $ curl -v https://192.168.121.10
    *   Trying 192.168.121.10:443...
    * connect to 192.168.121.10 port 443 from 192.168.121.1 port 56682 failed: Connection refused
    * Failed to connect to 192.168.121.10 port 443 after 0 ms: Could not connect to server
    * closing connection #0
    curl: (7) Failed to connect to 192.168.121.10 port 443 after 0 ms: Could not connect to server

The address above is just an example, and is likely different on your machine. Make sure you use the IP address
of the webserver VM on YOUR machine.

In order to make `nginx` use the new configuration by restarting the service and letting `nginx` re-read
its configuration.

On the machine itself we can do this by:

    [deploy@webserver ~]$ sudo systemctl restart nginx.service

Given what we know about the [ansible.builtin.service](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/service_module.html),
how can we do this through Ansible?

Add an extra task to the `05-web.yml` playbook to ensure the service is restarted after the configuration
file is installed.

When you are done, verify that `nginx` serves web pages on both TCP/80 (http) and TCP/443 (https):

    $ curl http://192.168.121.10
    $ curl --insecure https://192.168.121.10

Again, these addresses are just examples, make sure you use the IP of the actual webserver VM.

Note also that `curl` needs the `--insecure` option to establish a connection to a HTTPS server with
a self signed certificate.

# QUESTION C

What is the disadvantage of having a task that _always_ makes sure a service is restarted, even if there is
no configuration change?

# BONUS QUESTION

There are at least two _other_ modules, in addition to the `ansible.builtin.service` module that can restart
a `systemd` service with Ansible. Which modules are they?

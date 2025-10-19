# Examination 1 - Understanding SSH and public key authentication

Connect to one of the virtual lab machines through SSH, i.e.

    $ ssh -i deploy_key -l deploy webserver

Study the `.ssh` folder in the home directory of the `deploy` user:

    $ ls -ld ~/.ssh

Look at the contents of the `~/.ssh` directory:

    $ ls -la ~/.ssh/

## QUESTION A

What are the permissions of the `~/.ssh` directory?

```bash
drwx------. 2 deploy deploy 72 Oct 16 11:37 /home/deploy/.ssh
```

The owner has full access and is the only one with access

Why are the permissions set in such a way?

For security reasons. Inorder to keep the keys and config inacessable to other users otherwise the device may be accessed by an unathorized user. 

## QUESTION B

What does the file `~/.ssh/authorized_keys` contain?

It conatins a list of public ssh keys. It authorizes users that wants to access via ssh dont have to put in a password

## QUESTION C

When logged into one of the VMs, how can you connect to the
other VM without a password?

By putting your public key in the VMs autorized_keys in ~/.ssh

example:

If you want to connect from webserver to dbserver without password. You can copy webservers public key to dbservers authorized_keys

### Hints:

* man ssh-keygen(1)
* ssh-copy-id(1) or use a text editor

## BONUS QUESTION

Can you run a command on a remote host via SSH? How?

Yes you can by appending it to the ssh command
example:
```Bash
ssh dbserver ls -a ~ 
```

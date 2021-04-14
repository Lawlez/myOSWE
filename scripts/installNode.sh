# install desired version with nvm
nvm install v14.16.1

# cp the new files to plesk
cp -R ~/.nvm/versions/node/v14.16.1/ /opt/plesk/node/

# activate new node version in plesk
plesk sbin nodemng register /opt/plesk/node/v14.16.1/bin/node
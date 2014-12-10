# install node.js and pi-gpio
wget http://node-arm.herokuapp.com/node_lastest_armhf.deb
sudo dpkg -i node_latest_armhf.deb
npm install coffee-script
npm install pi-gpio

# install vim
sudo apt-get install vim

# install pip and virtualenvwrapper
sudo apt-get install python-setuptools
sudo easy_install pip
sudo pip install virtualenvwrapper

# git settings
git config --global user.name "Yoonseop Kang"
git config --global user.email e0engoon@gmail.com
git config --global core.editor vim

ssh-keygen -t rsa -C "e0engoon@gmail.com"
cat ~/.ssh/id_rsa.pub  # add this result to github settings

# download dotfiles and get them working
git clone --recursive git@github.com:e0en/dotfiles
echo "source ~/dotfiles/.bash_profile" > ~/.bash_profile
source ~/.bash_profile
echo "source ~/dotfiles/vimrc" > ~/.vimrc
vim +PluginUpdate +qall

# setup wifi

cd
mkdir src

cd ~/src
git clone git://github.com/SomeoneElseOSM/mod_tile.git
cd mod_tile

./autogen.sh
./configure
make
make install
make install-mod_tile
ldconfig

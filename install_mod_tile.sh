cd
mkdir src

echo "telecharger mod_tile"
cd ~/src
git clone git://github.com/SomeoneElseOSM/mod_tile.git
cd mod_tile
echo "fin de telecharger mod_tile"

echo "installer mod_tile"
./autogen.sh
./configure
make
sudo make install
sudo make install-mod_tile
sudo ldconfig
echo "fin de installer mod_tile"

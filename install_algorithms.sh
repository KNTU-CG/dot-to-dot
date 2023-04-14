echo "install algorithms libraries"
cd CT-Shape
sh CGALInstall.sh
cd ..
cd hole_detection_ED
sh install.sh
cd ..
cd RGG
sh script.sh
cd ..
echo "Installing CGAL fro alpha"
wget https://github.com/CGAL/cgal/releases/download/releases%2FCGAL-4.6.3/CGAL-4.6.3.tar.xz
tar -xf CGAL-4.6.3.tar.xz --directory ~
cd ~
cd CGAL-4.6.3 # go to CGAL directory
cmake . # configure CGAL
make # build the CGAL libraries
sudo make install # install

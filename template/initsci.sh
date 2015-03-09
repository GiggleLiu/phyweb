#!/bin/bash
#file: initsci.sh
#author: Jinguo Leo
#wget https://bootstrap.pypa.io/get-pip.py --no-check-certificate

(pip&&echo "pip already installed! skip")||(echo "Get and install pip locally"&&python get-pip.py --user&&echo "pip has been successfully installed, setting the PATH ..."&&export PATH=$PATH:$HOME/.local/bin&&echo "export PATH=$PATH:$HOME/.local/bin">>.bashrc&&echo "pip installed success fully, now you can use 'easy_install packagename' to install python packages."||exit 1)
(virtualenv&&echo "virtualenv already installed! skip")||(pip install virtualenv --user||exit 1)
if [ ! -d 'sci' ]; then
    virtualenv sci&&echo "alias scienv='source $PWD/sci/bin/activate'">>.bashrc&&echo "Now you can use command 'scienv' to start virtualenv! activating ..."&&source sci/bin/activate&&echo "ok"||exit 1
fi

echo "Installing Numpy and Scipy"
echo "if any error accurs in this section, please check:  https://software.intel.com/en-us/articles/numpyscipy-with-intel-mkl for more information!"
tar -xvf numpy.tar.gz&&cd numpy&&echo "Entering into numpy"||exit 1
python setup.py config --compiler=intelem build_clib --compiler=intelem build_ext --compiler=intelem install||(echo "install numpy failed"&&exit 1)
cd ..
tar -xvf scipy.tar.gz
cd scipy&&echo "Entering into scipy"||exit 1
python setup.py config --compiler=intelem --fcompiler=intelem build_clib --compiler=intelem --fcompiler=intelem build_ext --compiler=intelem --fcompiler=intelem install||(echo "install scipy failed"&&exit 1)

echo "Installing matplotlib and some other required library"
easy_install -r requirements.txt||exit 1

echo "Congratulations!"

curdir=`pwd`
mkdir tools && cd tools && git clone https://github.com/r9y9/hts_engine_API.git

cd ${curdir}

# NOTE: python3 failed to execute waf script
cd tools/hts_engine_API/src && python2 ./waf configure --prefix=${curdir}/dist && python2 ./waf build install

cd ${curdir}

cd tools && git clone https://github.com/r9y9/open_jtalk.git

cd ${curdir}

mkdir -p tools/open_jtalk/src/build && cd tools/open_jtalk/src/build && cmake -DCMAKE_INSTALL_PREFIX=${curdir}/dist -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON .. && make install

cd ${curdir}

export OPEN_JTALK_INSTALL_PREFIX=${curdir}/dist

cd tools && git clone https://github.com/r9y9/pyopenjtalk.git

cd ${curdir}
cd tools/pyopenjtalk && pip install .

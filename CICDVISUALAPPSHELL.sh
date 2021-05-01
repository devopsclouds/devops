git clone -b ${Branch} https://avpuser@infyvbs-infosysorc.developer.ocp.oraclecloud.com/infyvbs-infosysorc/s/infyvbs-infosysorc_securefast-vbcs-deployment_30549/scm/${Repo}.git 
ls -l
cd ${Repo}/${appname}
npm install
grunt vb-archive:sources --sources-zip-path=build/sources.zip vb-process-local vb-package vb-archive:optimized --optimized-zip-path=build/built-assets.zip
grunt vb-deploy --url=https://{ServerURL}/ic/builder/ --username=avpuser --password=$pass
cd ../../
rm -rf ${Repo}

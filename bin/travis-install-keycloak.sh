set -o errexit
set -o xtrace

KEYCLOAK_VERSION="4.1.0.Final"
KEYCLOAK_ADMIN="admin"
KEYCLOAK_PASSWORD="123456"
KEYCLOAK_DOWNLOAD_URL="https://downloads.jboss.org/keycloak/${KEYCLOAK_VERSION}/keycloak-${KEYCLOAK_VERSION}.tar.gz"

wget ${KEYCLOAK_DOWNLOAD_URL}

tar -xvzf keycloak-${KEYCLOAK_VERSION}.tar.gz

cd keycloak-${KEYCLOAK_VERSION}

./bin/add-user-keycloak.sh \
    -r master \
    -u ${KEYCLOAK_ADMIN} \
    -p ${KEYCLOAK_PASSWORD}

# launch keycloak in background and import realm settings file
LAUNCH_JBOSS_IN_BACKGROUND=1 ./bin/standalone.sh \
    -Dkeycloak.migration.action=import \
    -Dkeycloak.migration.provider=singleFile \
    -Dkeycloak.migration.file=${TRAVIS_BUILD_DIR}/tests/data/keycloak-demo-realm.json \
    -Dkeycloak.migration.realmName=demo

# give keycloak some time to start up and import the realm settings
sleep 30s

./bin/add-user-keycloak.sh \
    -r save-my-bike \
    -u ${KEYCLOAK_ADMIN} \
    -p ${KEYCLOAK_PASSWORD}
    -g /end-users


# use the jboss-cli to perform further keycloak configuration
./bin/jboss-cli --connect --controller=localhost:10090 << EOF
EOF

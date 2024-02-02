BASEDIR=$(dirname $0)


source ${BASEDIR}/venv/bin/activate
export FLASK_APP=${BASEDIR}/main.py
Python3 ${BASEDIR}/main.py
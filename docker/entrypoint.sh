#!/bin/sh
set -e

BOT_CMD='python src/main.py'

if [ "$1" = 'run' ]; then
    shift
    exec ${BOT_CMD} $@
elif [ "$1" = 'lint' ]; then
    shift
    OPTS=${@:-'.'}
    echo "-- black --" && black --check --diff $OPTS || EXIT=$?
    echo "-- isort --" && isort -c --diff $OPTS || EXIT=$?
    echo "-- flake8 --" && flake8 $OPTS || EXIT=$?
    MYPY_OPTS=${@:-'src/'}
    echo "-- mypy --" && mypy $MYPY_OPTS || EXIT=$?
    exit ${EXIT:-0}
elif [ "$1" = 'fmt' ]; then
    shift
    OPTS=${@:-'.'}
    echo "-- black --" && black $OPTS
    echo "-- isort --" && isort --atomic $OPTS
    exit 0
fi

exec "$@"

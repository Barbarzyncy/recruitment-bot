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
    echo "-- ruff --" && ruff check . $OPTS || EXIT=$?
    exit ${EXIT:-0}
elif [ "$1" = 'fmt' ]; then
    shift
    OPTS=${@:-'.'}
    echo "-- black --" && black $OPTS
    echo "-- ruff --" && ruff --fix $OPTS
    exit 0
fi

exec "$@"

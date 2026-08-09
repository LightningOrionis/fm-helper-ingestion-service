#!/bin/bash
set -e

if [ -z "$TEST_POSTGRES_URL" ]; then
    export TEST_POSTGRES_URL="sqlite:///:memory:"
fi

pytest tests/test_save.py -v


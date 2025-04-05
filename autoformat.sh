#!/bin/bash

ruff check --fix --select I,E mboxmake2/ tests/ &&\
    ruff format mboxmake2 tests/

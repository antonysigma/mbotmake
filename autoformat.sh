#!/bin/bash

ruff format mbotmake2 tests/ &&\
    ruff check --fix --select I,E mbotmake2/ tests/

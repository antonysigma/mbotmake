#!/bin/bash

ruff format mboxmake2 tests/ &&\
    ruff check --fix --select I,E mboxmake2/ tests/

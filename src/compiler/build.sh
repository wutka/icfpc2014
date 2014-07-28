#!/bin/sh

# This requires corebuild. If you have OPAM installed, you should
# be able to install it with: opam install core
corebuild -use-menhir compiler.byte

# Important notes for building pdf2htmlEX source code in Ubuntu 18.04

##fontforge

    * install libc++-dev
    * for the error related to "math.h" 'please include config.h firstly', we need to replace 'math.h'->'stdlib.h' in the source code causing the compile error

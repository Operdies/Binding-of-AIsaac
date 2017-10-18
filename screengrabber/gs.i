/* File : gs.i */
%module gs

%{
#include "gs.h"
%}

%include stl.i

namespace std {
    %template(UintVector) vector<uint8_t>;
}

%include "gs.h"


%module gs
%{
extern void ImageFromDisplay(std::vector<uint8_t>& Pixels, int& Width, int& Height, int& BitsPerPixel);
%}

extern void ImageFromDisplay(std::vector<uint8_t>& Pixels, int& Width, int& Height, int& BitsPerPixel);


#include <string>
#include <iostream>
#include <vector>
#include <fstream>
#include <map>


#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "lib/stb_image_write.h" /* http://nothings.org/stb/stb_image_write.h */

#define STB_TRUETYPE_IMPLEMENTATION 
#include "lib/stb_truetype.h" /* http://nothings.org/stb/stb_truetype.h */


//#include "SerialPort.h"



void writeText(const char* font, const char* file) {

	long size;
	unsigned char* fontBuffer;
	
	/*read text from input file*/
	string word;
	//string mword;
    ifstream myfile ("input.txt");
    if (myfile.is_open())
    {
        getline (myfile,word);
		//word = word.c_str();
		myfile.close();
	}
	else cout << "Unable to open file"; 

	/* load font file */ {
		FILE* fontFile = fopen(font, "rb");
		fseek(fontFile, 0, SEEK_END);
		size = ftell(fontFile); /* how long is the file ? */
		fseek(fontFile, 0, SEEK_SET); /* reset */

		fontBuffer = (unsigned char*)malloc(size);

		fread(fontBuffer, size, 1, fontFile);
		fclose(fontFile);
	}

	/* prepare font */
	stbtt_fontinfo info;
	if (!stbtt_InitFont(&info, fontBuffer, 0)) {
		printf("failed\n");
		return;
	}

	int l_h = 64; /* line height */
	int b_w = strlen(word.c_str()) * 64; /* bitmap width */
	int b_h = 64; /* bitmap height */

	/* create a bitmap for the phrase */
	unsigned char* bitmap = (unsigned char*)malloc(b_w * b_h);

	/* Make it black*/
	for (int i = 0; i < b_h * b_w;i++) {
		bitmap[i] = 0;
	}

	/* calculate font scaling */
	float scale = stbtt_ScaleForPixelHeight(&info, l_h);

	int x = 0;

	int ascent, descent, lineGap;
	stbtt_GetFontVMetrics(&info, &ascent, &descent, &lineGap);

	ascent *= scale;
	descent *= scale;

	int i;
	for (i = 0; i < strlen(word.c_str()); ++i) {
		/* get bounding box for character (may be offset to account for chars that dip above or below the line */
		int c_x1, c_y1, c_x2, c_y2;
		stbtt_GetCodepointBitmapBox(&info, word[i], scale, scale, &c_x1, &c_y1, &c_x2, &c_y2);

		/* compute y (different characters have different heights */
		int y = ascent + c_y1;

		/* render character (stride and offset is important here) */
		int byteOffset = x + (y  * b_w);
		stbtt_MakeCodepointBitmap(&info, bitmap + byteOffset, c_x2 - c_x1, c_y2 - c_y1, b_w, scale, scale, word[i]);

		/* how wide is this character */
		int ax;
		stbtt_GetCodepointHMetrics(&info, word[i], &ax, 0);
		x += ax * scale;

		/* add kerning */
		int kern;
		kern = stbtt_GetCodepointKernAdvance(&info, word[i], word[i + 1]);
		x += kern * scale;
	}


	std::string filename(file);
	filename += ".bmp";
	/* save out a 1 channel image */
	stbi_write_bmp(filename.c_str(), b_w, b_h, 1, bitmap);

	free(fontBuffer);
	free(bitmap);
}



void doTrace(const std::string& name) {
	std::string potfile = "helper/trace.exe -s ";
	potfile += name;
	potfile += ".bmp -o ";
	potfile += name;
	potfile += ".svg";
	system(potfile.c_str());
}

void doGcode(const std::string& name) {
	std::string gcode = "helper/gcode.exe ";
	gcode += name;
	gcode += ".svg -o ";
	gcode += name;
	gcode += ".gcode";
	system(gcode.c_str());
}





void getFilename(std::string& filename) {
	char str2[100];
	std::cout << "Filename:";
	std::cin.getline(str2, 100);
}





int main(int argc, const char * argv[]) {
	std::map<std::string, std::string> lineargs;
	for (int i = 0; i < argc; i++) {
		switch (i){
		case 0: //Name of exe. Not really usefull.

			break;
		default:
			std::string linearg(argv[i]);
			if (linearg[0] == '-') { //Is command.
				if (i + 1 != argc) {
					std::string linearg2(argv[i + 1]);
					if (linearg2[0] == '-') { //Is command.
						lineargs[linearg.substr(1)] = "1";
					}
					else {
						lineargs[linearg.substr(1)] = linearg2;
						i++;
					}
				}
				else{
					lineargs[linearg.substr(1)] = "1";
				}
			}
			break;
		}
	}

	//std::string config = lineargs["config"];
	std::string textInputFile = lineargs["input"];
	std::string fontname = lineargs["font"];
	std::string filename = lineargs["filename"];
	std::string port = lineargs["port"];

	//if (config.size() == 0) {
		//TODO: Load config for gcode
	//}

	if (filename.size() == 0) {
		filename = "test";
	}

/*
	if (text.size() == 0) {
		getText(text);
	}

	if (fontname.size() == 0) {
		getRandomFont(fontname);
	}
*/

	

	writeText(fontname.c_str(), filename.c_str()); //Create a .bmp file

	doTrace(filename); //Convert bmp to svg

	doGcode(filename); //Convert svg to gcode

	//sendGcode(filename, port); //Send data.

	return EXIT_SUCCESS;
}
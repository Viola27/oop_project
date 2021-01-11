#include <iostream>
#include <sstream>

#define MAX_VALUE 20

using namespace std;

typedef struct singleFileValues {
  int chip;
  int ch;
  float real_threshold;
  float x[MAX_VALUE] = {0};
  float y[MAX_VALUE] = {0};
} singleFileValues;

int main(void) {

  singleFileValues* v;
  string token = "34";

  auto ss = std::stringstream(token); // token = "Ch_0_offset_0_Chip_001.txt"
  cout << token.c_str();
  sscanf(token.c_str(), "%d", &v->ch);
  cout << token.c_str();

}
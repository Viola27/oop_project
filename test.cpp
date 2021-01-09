#include <iostream>
#include <sstream>

using namespace std;

int main(void) {

  int ch, chip;

  string filepath = "../secondolotto_1/Station_1__11/Station_1__11_Summary/"
                    "Chip_001/S_curve/Ch_0_offset_0_Chip_001.txt";

  stringstream ss(filepath);
  string token;
  for (int i = 0; i < 7; i++)
    getline(ss, token, '/');

  //stringstream ss1(token); // token = "Ch_0_offset_0_Chip_001.txt"
  ss=std::stringstream(token);
  getline(ss, token, '_');
  getline(ss, token, '_');
  sscanf(token.c_str(), "%d", &ch);

  cout << ch;

#pragma unroll
  for (int i = 0; i < 4; i++)
    getline(ss, token, '_'); // token = "001.txt"

  stringstream ss2(token);
  getline(ss2, token, '.');
  sscanf(token.c_str(), "%d", &chip);

  cout << chip;
}
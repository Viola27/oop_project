#include <cmath>
#include <fstream>
#include <iostream>
#include <sstream>

#define MAX_VALUE 10

using namespace std;

typedef struct singleFileValues {
  float x[MAX_VALUE] = {0};
  float y[MAX_VALUE] = {0};
  int chip;
  int ch;
  float real_threshold;
} singleFileValues;

singleFileValues read_single_file(string filepath) {

  singleFileValues values;
  string line;
  float test;
  int i = 0;

  stringstream ss(filepath);
  string token;
  for (int i = 0; i < 7; i++)
    getline(ss, token, '/');

  ss = std::stringstream(token); // token = "Ch_0_offset_0_Chip_001.txt"
  getline(ss, token, '_');
  getline(ss, token, '_');
  sscanf(token.c_str(), "%d", &values.ch);

#pragma unroll
  for (int i = 0; i < 4; i++)
    getline(ss, token, '_'); // token = "001.txt"

  ss = std::stringstream(token);
  getline(ss, token, '.');
  sscanf(token.c_str(), "%d", &values.chip);

  ifstream f(filepath);
  getline(f, line);
  ss = std::stringstream(line);
  getline(ss, token, '\t');
  if (sscanf(token.c_str(), "%f", &test) != 1) { // file errato
    values.real_threshold = -1;
    return values;
  }
  getline(ss, token, '\t');
  sscanf(token.c_str(), "%f", &values.real_threshold);
  getline(f, line);
  getline(f, line);

  // cominciano i valori X e Y
  while (getline(f, line)) {
    ss = std::stringstream(line);
    getline(ss, token, '\t');
    sscanf(token.c_str(), "%f", &values.x[i]);
    getline(ss, token, '\t');
    sscanf(token.c_str(), "%f", &values.y[i]);
    i++;
  }

  return values;
}

float polyfit(float X[MAX_VALUE], float Y[MAX_VALUE], float y_fit, int j) {
  // Dati i valori X e Y e dato il punto y, restituisce la x corrispondente.
  float acc_x = 0.0;
  float acc_y = 0.0;
  float media_x = 0.0;
  float media_y = 0.0;
  float cov = 0.0;
  float sqm = 0.0; // scarto quadr. medio di X
  float m = 0.0;
  float q = 0.0;

  for (int i = 0; i < j; i++) {
    acc_x += X[i];
    acc_y += Y[i];
  }
  media_x = acc_x / j;
  media_y = acc_y / j;
  for (int i = 0; i < j; i++) {
    cov += ((X[i] - media_x) * (Y[i] - media_y));
    sqm += ((X[i] - media_x) * (X[i] - media_x));
  }
  cov /= (j - 1);
  sqm /= (j - 1);
  sqm = sqrt(sqm);

  m = cov / (sqm * sqm);
  q = media_y - media_x * m;

  return (y_fit - q) / m;
}

int main(void) {

  // try {
  //   exec("./analisi_file.sh");
  // } catch (const Exception e) {
  //   cerr << e.what();
  // }

  ifstream file_path("file_path.txt");
  ofstream risultati("risultati_cpp.txt");
  int tot_file = 10;

  for (int curr_file = 0; curr_file < tot_file; curr_file++) {
    string onepath;
    getline(file_path, onepath);
    singleFileValues v = read_single_file(onepath);

    float X[MAX_VALUE] = {0};
    float Y[MAX_VALUE] = {0};
    int j = 0;

    for (int i = 0; i < MAX_VALUE; i++) {
      if (v.y[i] > 1 && v.y[i] < 999) {
        X[j] = v.x[i];
        Y[j] = v.y[i];
        j++;
      }
    }

    float x_fit = polyfit(X, Y, 500, j);

    risultati << "Chip: " << v.chip << "\tCh: " << v.ch
              << "\tReal Thres: " << v.real_threshold
              << "\tThresh found: " << x_fit
              << "\tDiff: " << abs(x_fit - v.real_threshold) << "\n";
  }

  file_path.close();
  risultati.close();
}
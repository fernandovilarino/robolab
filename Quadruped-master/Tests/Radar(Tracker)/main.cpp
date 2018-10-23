#include <iostream>
#include <cstdlib>
#include <ctime>
#include <cmath>

using namespace std;

void multiplyMatrices(double firstMatrix[][3], double secondMatrix[][2], double mult[][2], int rowFirst, int columnFirst, int rowSecond, int columnSecond);
void multiply2x2Matrices(double firstMatrix[][2], double secondMatrix[][2], double mult[][2], int rowFirst, int columnFirst, int rowSecond, int columnSecond);
void multiplyMatCol(double firstMatrix[][2], double secondMatrix[][1], double mult[][1]);
void transposeMatrix(double firstMatrix[][3], double transposeMatrix[][2], int rows, int columns);
void transpose2x2Matrix(double firstMatrix[][2], double transposeMatrix[][2]);
void display2x2Matrix(double mult[][2], double rowFirst, double columnSecond);
void inverse2x2Matrix(double pMatrix[2][2], double inverseMatrix[2][2]);

/* ======================================
   BLUE ESTIMATOR FOR SOURCE LOCALIZATION
   ======================================
*/
int main(int argc, char const *argv[]) {

  // Useful variables
  double c = 340.29; // The speed of sound [m/s]
  srand((unsigned)time(0));
  //TODO: Add noise to the simulation
  double noiseAmp = 0.000000001; // Very tiny, deprecable noise
  // double noise[3];
  // noise[0] = noiseAmp*(rand()%100)+1;
  // noise[1] = noiseAmp*(rand()%100)+1;
  // noise[2] = noiseAmp*(rand()%100)+1;

  // ===== Covariance Matrix C =====
  double A[2][3], Atr[3][2], C[2][2];
  A[0][0] = -1; A[0][1] = 1; A[0][2] = 0;
  A[1][0] = 0; A[1][1] = -1; A[1][2] = 1;

  transposeMatrix(A, Atr, 2, 3);
  display2x2Matrix(Atr, 3, 2);
  multiplyMatrices(A, Atr, C, 2, 3, 3, 2);
  C[0][0] *= pow(noiseAmp, 2);
  C[0][1] *= pow(noiseAmp, 2);
  C[1][0] *= pow(noiseAmp, 2);
  C[1][1] *= pow(noiseAmp, 2);
  display2x2Matrix(C, 2, 2);

  // Distances between sensors and Nominal Position nomP and their angles;
  double d = 6;
  double nomP[2]; nomP[0] = 0; nomP[1] = 6;
  double Antenna0[2]; Antenna0[0] = -d; Antenna0[1] = 0;
  double Antenna1[2]; Antenna1[0] = 0; Antenna1[1] = 0;
  double Antenna2[2]; Antenna2[0] = d; Antenna2[1] = 0;

  double dist_0_nomP = sqrt(pow((nomP[0]-Antenna0[0]),2)+pow((nomP[1]-Antenna0[1]),2));
  double dist_1_nomP = sqrt(pow((nomP[0]-Antenna1[0]),2)+pow((nomP[1]-Antenna1[1]),2));
  double dist_2_nomP = sqrt(pow((nomP[0]-Antenna2[0]),2)+pow((nomP[1]-Antenna2[1]),2));
  double angle_0_nomP = acos(d/dist_0_nomP);
  double angle_1_nomP = acos(0/dist_1_nomP);
  double angle_2_nomP = acos(-d/dist_2_nomP);

  // ===== Matrix H of coefficients =====
  double H[2][2];
  H[0][0] = (cos(angle_1_nomP) - cos(angle_0_nomP))/c;
  H[0][1] = (sin(angle_1_nomP) - sin(angle_0_nomP))/c;
  H[1][0] = (cos(angle_2_nomP) - cos(angle_1_nomP))/c;
  H[1][1] = (sin(angle_2_nomP) - sin(angle_1_nomP))/c;

  // ======================================
  // ====== Simulation of Estimator =======
  // ======================================
  // ===== Vector Epsilon E of TDOA from the sensors =====
  /* Let us suppose the target is in (3, 5).
    Remember that THIS INFORMATION IS UNKNOWN. This is precisely what
    we want to estimate. */
  double sourceP[2]; sourceP[0] = 3; sourceP[1] = 5;
  // This is what our sensors see, the time that the signal takes to go and return
  // to a from the target. THIS IS KNOWN
  double dist_0_sourceP = sqrt(pow((sourceP[0]-Antenna0[0]),2)+pow((sourceP[1]-Antenna0[1]),2));
  double dist_1_sourceP = sqrt(pow((sourceP[0]-Antenna1[0]),2)+pow((sourceP[1]-Antenna1[1]),2));
  double dist_2_sourceP = sqrt(pow((sourceP[0]-Antenna2[0]),2)+pow((sourceP[1]-Antenna2[1]),2));

  // TDOA taus and Epsilon vector TODO: add noise
  double tau0 = dist_0_sourceP/c - dist_0_nomP/c;
  double tau1 = dist_1_sourceP/c - dist_1_nomP/c;
  double tau2 = dist_2_sourceP/c - dist_2_nomP/c;

  double E[2][1]; // Column vector with TDOA information
  E[0][0] = tau1 - tau0;
  E[1][0] = tau2 - tau1;

  // BLUE Estimator
  // Denominator of estimator
  double Htr[2][2]; transpose2x2Matrix(H, Htr);
  double Cinv[2][2]; inverse2x2Matrix(C, Cinv);
  double denom[2][2], aux[2][2], aux2[2][2];
  multiply2x2Matrices(Htr, Cinv, aux, 2, 2, 2, 2);
  multiply2x2Matrices(aux, H, denom, 2, 2, 2, 2);
  double denomInv[2][2]; inverse2x2Matrix(denom, denomInv);

  // Numerator of estimator
  multiply2x2Matrices(denomInv, aux, aux2, 2, 2, 2, 2);
  double theta[2][1];
  multiplyMatCol(aux2, E, theta);

  display2x2Matrix(H, 2, 2);

  cout << "x: " << theta[0][0] << " - y: " << theta[1][0] << endl;

  return 0;
}





void multiplyMatrices(double firstMatrix[][3], double secondMatrix[][2], double mult[][2], int rowFirst, int columnFirst, int rowSecond, int columnSecond)
{
	int i, j, k;

	// Initializing elements of matrix mult to 0.
	for(i = 0; i < rowFirst; ++i)
	{
		for(j = 0; j < columnSecond; ++j)
		{
			mult[i][j] = 0;
		}
	}

	// Multiplying matrix firstMatrix and secondMatrix and storing in array mult.
	for(i = 0; i < rowFirst; ++i)
	{
		for(j = 0; j < columnSecond; ++j)
		{
			for(k=0; k<columnFirst; ++k)
			{
				mult[i][j] += firstMatrix[i][k] * secondMatrix[k][j];
			}
		}
	}
}

void multiply2x2Matrices(double firstMatrix[][2], double secondMatrix[][2], double mult[][2], int rowFirst, int columnFirst, int rowSecond, int columnSecond)
{
	int i, j, k;

	// Initializing elements of matrix mult to 0.
	for(i = 0; i < rowFirst; ++i)
	{
		for(j = 0; j < columnSecond; ++j)
		{
			mult[i][j] = 0;
		}
	}

	// Multiplying matrix firstMatrix and secondMatrix and storing in array mult.
	for(i = 0; i < rowFirst; ++i)
	{
		for(j = 0; j < columnSecond; ++j)
		{
			for(k=0; k<columnFirst; ++k)
			{
				mult[i][j] += firstMatrix[i][k] * secondMatrix[k][j];
			}
		}
	}
}

void multiplyMatCol(double firstMatrix[][2], double secondMatrix[][1], double mult[][1])
{
	int i, j, k;
  int rowFirst = 2; int columnFirst = 2;
  int columnSecond = 1;
	// Initializing elements of matrix mult to 0.
	for(i = 0; i < rowFirst; ++i)
	{
		for(j = 0; j < columnSecond; ++j)
		{
			mult[i][j] = 0;
		}
	}

	// Multiplying matrix firstMatrix and secondMatrix and storing in array mult.
	for(i = 0; i < rowFirst; ++i)
	{
		for(j = 0; j < columnSecond; ++j)
		{
			for(k=0; k<columnFirst; ++k)
			{
				mult[i][j] += firstMatrix[i][k] * secondMatrix[k][j];
			}
		}
	}
}

void transposeMatrix(double firstMatrix[][3], double transposeMatrix[][2], int rows, int columns)
{
  int i,j;
  // Finding transpose of matrix a[][] and storing it in array trans[][].
  for(i = 0; i < rows; i++)
      for(j = 0; j < columns; j++)
      {
        transposeMatrix[j][i]=firstMatrix[i][j];
      }
}

void transpose2x2Matrix(double firstMatrix[][2], double transposeMatrix[][2])
{
  int i,j;
  int rows = 2;
  int columns = 2;
  // Finding transpose of matrix a[][] and storing it in array trans[][].
  for(i = 0; i < rows; i++)
      for(j = 0; j < columns; j++)
      {
        transposeMatrix[j][i]=firstMatrix[i][j];
      }
}

void display2x2Matrix(double mult[][2], double rowFirst, double columnSecond)
{
	int i, j;

	cout << "Output Matrix:" << endl;
	for(i = 0; i < rowFirst; ++i)
	{
		for(j = 0; j < columnSecond; ++j)
		{
			cout << mult[i][j] << " ";
			if(j == columnSecond - 1)
				cout << endl << endl;
		}
	}
}

void inverse2x2Matrix(double pMatrix[2][2], double inverseMatrix[2][2])
{
  double det = pMatrix[0][0] * pMatrix[1][1] - pMatrix[0][1] * pMatrix[1][0];

  inverseMatrix[0][0] = pMatrix[1][1]/det;
  inverseMatrix[0][1] = -pMatrix[0][1]/det;
  inverseMatrix[1][0] = -pMatrix[1][0]/det;
  inverseMatrix[1][1] = pMatrix[0][0]/det;
}

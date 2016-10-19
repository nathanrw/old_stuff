#include <cstdlib>
#include <iostream>
#include <math.h>

#define pi 3.14159265

using namespace std;

//===============================================================================================
// Some Structures:
//===============================================================================================

struct point3D {
	float x;
	float y;
	float z;
	bool inuse;
} ;

struct tri3D {
    point3D* A;
    point3D* B;
    point3D* C;
    bool inuse;
} ;

//===============================================================================================
// Some Subroutines:
//===============================================================================================

int CoutLine(char* text) {
    cout << text << "\n";
    return 0;
}

int CoutWords(char* text) {
    cout << text;
    return 0;
}

// Rotates a about b by angle.
void rotate2D(float X1, float Y1, float X2, float Y2, float& Xr, float& Yr, float angle) {

	float sinval = sin((pi/180)*angle);
	float cosval = cos((pi/180)*angle);

	// Make b the origin.
	X1 -= X2;
	Y1 -= Y2;

	// Rotate and return the resulting x and y values.
	Xr = (X1 * cosval - Y1 * sinval + X2);
	Yr = (X1 * sinval + Y1 * cosval + Y2);
}

// Rotates point about (0,0,0) by angle.
point3D rotate3D(point3D point, point3D angle) {

	// No point rotating, as angle is nought.
	if ((angle.x == 0) && (angle.y == 0) && (angle.z == 0)) { return point; }

	// Else, do all three axes
    rotate2D( point.y, point.z, 0, 0, point.y, point.z, angle.x ); // About x
	rotate2D( point.x, point.z, 0, 0, point.x, point.z, angle.y ); // About y
	rotate2D( point.x, point.y, 0, 0, point.x, point.y, angle.z ); // About z

	return point;
}

// Rotate a point about the camera by the rotation of the camera.
point3D rotateAboutCamera(point3D point, point3D& pos, point3D angle) {

	point.x -= pos.x;
	point.y -= pos.y;
	point.z -= pos.z;

	angle.x = -angle.x;
	angle.y = -angle.y;
	angle.z = -angle.z;

	return rotate3D(point,angle);
}

// 3D Projection.
void projectPoint( point3D& point, int& screenwidth, int& screenheight, float& dist,
                   float& returnx, float& returny)
{

	float conv = dist / (point.z+0.000001);
 	returnx = conv*point.x + screenwidth*0.5;
	returny = conv*point.y + screenheight*0.5;
}

//Convenience.

point3D MakePoint3D(float x, float y, float z)
{
    point3D point;
    point.x = x;
    point.y = y;
    point.z = z;
    return point;
}

tri3D MakeTri3D(int VertsAddress)
{
    tri3D tri;
    tri.A = (point3D*)(VertsAddress);
    tri.B = (point3D*)(VertsAddress+1);
    tri.C = (point3D*)(VertsAddress+2);
    return tri;
}

int CreateTriangle(point3D* VERTICES, tri3D* POLYGONS, int& vertcounter, int& tricounter,
                   point3D pointa, point3D pointb, point3D pointc)
{
    VERTICES[vertcounter] = pointa;
    VERTICES[vertcounter+1] = pointb;
    VERTICES[vertcounter+2] = pointc;

    POLYGONS[tricounter] = MakeTri3D((int)VERTICES+vertcounter);

    vertcounter += 3;
    tricounter += 1;

    return (int)POLYGONS + tricounter - 1;
}

//===============================================================================================
// Entry Point:
//===============================================================================================

int main()
{
    // Camera information
    int screenwidth = 640;
    int screenheight = 480;
    point3D cameraposition = MakePoint3D(0,0,0);
    float dist = 320;

    // Test 2D rotation.
    float OUT_X, OUT_Y;
    rotate2D(10,10,0,0,OUT_X,OUT_Y,30);
    cout << "\n" << "X: " << OUT_X << " Y: " << OUT_Y << "\n";

    // Test 3D rotation.
    point3D ONE = MakePoint3D(10,10,330);
    point3D ANGLE = MakePoint3D(0,30,0);
    point3D OUT_POINT = rotate3D(ONE,ANGLE);

    cout << "\n" << "X: " << OUT_POINT.x << " Y: " << OUT_POINT.y << " Z: " << OUT_POINT.z <<
    "\n";

    // Test rotation about camera.
    OUT_POINT = rotateAboutCamera(ONE,cameraposition,ANGLE);

    cout << "\n" << "X: " << OUT_POINT.x << " Y: " << OUT_POINT.y << " Z: " << OUT_POINT.z <<
    "\n";

    // Test 3D projection.
    float X;
    float Y;
    projectPoint(ONE, screenwidth, screenheight, dist, X, Y);
    cout << "\n" << "X: " << X << " Y: " << Y << "\n";

    // Test polygons and such.

    tri3D   POLYGONS[100];
    point3D VERTICES[300];

    point3D PONE = MakePoint3D(-10,10,0);
    point3D PTWO = MakePoint3D(10,10,0);
    point3D PTHREE = MakePoint3D(0,0,0);
    int vertcounter = 0;
    int tricounter = 0;

    int thetriangle = CreateTriangle(VERTICES,POLYGONS, vertcounter, tricounter, PONE, PTWO, PTHREE);

    cout << "\n" << ((tri3D*)thetriangle)->A->x << " " << ((tri3D*)thetriangle)->A->y << " " << ((tri3D*)thetriangle)->A->z << " " << "\n";

    // Pretty newline!
    cout << "\n";

    system("PAUSE");
    return 0;
}

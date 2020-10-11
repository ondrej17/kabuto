//#include <iostream>
//#include <boost/math/special_functions/spherical_harmonic.hpp>
//
//double function_y_lm(int l, int m, double dx, double dy, double dz);
//
//using namespace std;
//
//int main() {
//    cout << "Testing spherical harmonics in C" << endl;
//    cout << function_y_lm(0, 0, 1, 1, 1) << endl;
//    cout << function_y_lm(0, 0, -1, -1, -1) << endl;
//    cout << function_y_lm(1, 1, 1, 1, 9) << endl;
//    cout << function_y_lm(1, 0, 1, 1, 9) << endl;   // != Python
//    cout << function_y_lm(2, 0, 1, 1, 9) << endl;   // != Python
//    cout << function_y_lm(2, 1, 1, 1, 9) << endl;   // != Python
//    cout << function_y_lm(2, -1, 1, 1, 9) << endl;   // != Python
//
//    return 0;
//}
//
//double function_y_lm(int l_param, int m, double dx, double dy, double dz) {
//    // spherical coordinates of vector r_ij
//    double r{sqrt(pow(dx, 2) + pow(dy, 2) + pow(dz, 2))};
//    double phi{atan2(dy, dx)};
//    double theta{acos(dz / r)};
//
//    // return real form spherical harmonics in form Y_lm
//    //      sph_harm() returns Y_l^m --> wikipedia
//    if (m < 0) {
//        return pow(-1, m) * M_SQRT2 * (boost::math::spherical_harmonic_i(l_param, abs(m), theta, phi));
//    } else if (m == 0) {
//        return boost::math::spherical_harmonic_r(l_param, 0, theta, phi);
//    } else {
//        return pow(-1, m) * M_SQRT2 * (boost::math::spherical_harmonic_r(l_param, m, theta, phi));
//    }
//}
//

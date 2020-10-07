#include <iostream>
#include <boost/math/special_functions/spherical_harmonic.hpp>

double function_y_lm(int l_param, int m, double dx, double dy, double dz);

using namespace std;

int main() {
    cout << "Testing spherical harmonics ..." << endl;
    return 0;
}

double function_y_lm(int l_param, int m, double dx, double dy, double dz) {
    // spherical coordinates of vector r_ij
    double r{sqrt(pow(dx, 2) + pow(dy, 2) + pow(dz, 2))};
    double phi{atan2(dy, dx)};
    double theta{acos(dz / r)};

    // return real form spherical harmonics in form Y_lm
    //      sph_harm() returns Y_l^m --> wikipedia
    if (m < 0) {
        return pow(-1, m) * M_SQRT2 * (boost::math::spherical_harmonic_i(abs(m), l_param, theta, phi));
    } else if (m == 0) {
        return boost::math::spherical_harmonic_r(0, l_param, theta, phi);
    } else {
        return pow(-1, m) * M_SQRT2 * (boost::math::spherical_harmonic_r(m, l_param, theta, phi));
    }
}


#include "descriptors_descriptors.h"

std::vector<double> Descriptors::getDescriptors()
{
    std::vector<double> result;

    for (std::vector<double> params : m_g2FunctionParameters)
    {
        result.push_back(symmetryFunctionG2(params.at(0), params.at(1)));
    }
    for (double param : m_g3FunctionParameters)
    {
        result.push_back(symmetryFunctionG3(param));
    }
    for (int param : m_steinhardtFunctionParameters)
    {
        result.push_back(steinhardtFunction(param));
    }

    return result;
}

double Descriptors::symmetryFunctionG2(double eta, double rs)
{
    double result{0.0};
    double myX{m_atoms.at(m_id).getX()};
    double myY{m_atoms.at(m_id).getY()};
    double myZ{m_atoms.at(m_id).getZ()};

    for (int id : m_atomsId)
    {
        if (m_id != id)
        { // skip myself

            // coordinates of other atom
            double otherX{m_atoms.at(id).getX()};
            double otherY{m_atoms.at(id).getY()};
            double otherZ{m_atoms.at(id).getZ()};

            // components of the vector r_ij
            double x_ij{otherX - myX};
            double y_ij{otherY - myY};
            double z_ij{otherZ - myZ};

            // correction of vector r_ij for PBC (and minimum image convention)
            x_ij -= m_pbcX * std::round(x_ij / m_pbcX);
            y_ij -= m_pbcY * std::round(y_ij / m_pbcY);
            z_ij -= m_pbcZ * std::round(z_ij / m_pbcZ);

            // calculate the correct length of vector r_ij
            double r_ij{sqrt(pow(x_ij, 2) + pow(y_ij, 2) + pow(z_ij, 2))};

            // add correct contribution to result
            result += fcFunction(r_ij, m_rMinSym, m_rMaxSym) * exp(-eta * pow(r_ij - rs, 2));
        }
    }
    return result;
}

double Descriptors::symmetryFunctionG3(double kappa)
{
    double result{0.0};
    double myX{m_atoms.at(m_id).getX()};
    double myY{m_atoms.at(m_id).getY()};
    double myZ{m_atoms.at(m_id).getZ()};

    for (int id : m_atomsId)
    {
        if (m_id != id)
        { // skip myself

            // coordinates of other atom
            double otherX{m_atoms.at(id).getX()};
            double otherY{m_atoms.at(id).getY()};
            double otherZ{m_atoms.at(id).getZ()};

            // vector r_ij
            double x_ij{otherX - myX};
            double y_ij{otherY - myY};
            double z_ij{otherZ - myZ};

            // correction of vector r_ij for PBC (and minimum image convention)
            x_ij -= m_pbcX * std::round(x_ij / m_pbcX);
            y_ij -= m_pbcY * std::round(y_ij / m_pbcY);
            z_ij -= m_pbcZ * std::round(z_ij / m_pbcZ);

            // calculate the correct length of vector r_ij
            double r_ij{sqrt(pow(x_ij, 2) + pow(y_ij, 2) + pow(z_ij, 2))};

            // add correct contribution to result
            result += fcFunction(r_ij, m_rMinSym, m_rMaxSym) * cos(kappa * r_ij);
        }
    }
    return result;
}

double Descriptors::steinhardtFunction(int l)
{
    double result{0.0};

    for (int m = -l; m <= l; m++)
    {
        result += pow(fabs(qlmFunction(m, l)), 2);
    }
    return sqrt(result * 4 * M_PI / (2 * l + 1));
}

double Descriptors::fcFunction(double r, double rMin, double rMax)
{
    if (r <= rMin)
    {
        return 1.0;
    }
    else if ((rMin < r) && (r <= rMax))
    {
        return 0.5 + 0.5 * cos(M_PI * (r - rMin) / (rMax - rMin));
    }
    else
    {
        return 0.0;
    }
}

double Descriptors::qlmFunction(int m, int l)
{
    double myX{m_atoms.at(m_id).getX()};
    double myY{m_atoms.at(m_id).getY()};
    double myZ{m_atoms.at(m_id).getZ()};

    double numerator{0.0};
    double denominator{0.0};

    for (int id : m_atomsId)
    {
        if (m_id != id)
        { // skip myself

            // coordinates of other atom
            double otherX{m_atoms.at(id).getX()};
            double otherY{m_atoms.at(id).getY()};
            double otherZ{m_atoms.at(id).getZ()};

            // vector r_ij
            double x_ij{otherX - myX};
            double y_ij{otherY - myY};
            double z_ij{otherZ - myZ};

            // correction of vector r_ij for PBC (and minimum image convention)
            x_ij -= m_pbcX * std::round(x_ij / m_pbcX);
            y_ij -= m_pbcY * std::round(y_ij / m_pbcY);
            z_ij -= m_pbcZ * std::round(z_ij / m_pbcZ);

            // calculate the correct length of vector r_ij
            double r_ij{sqrt(pow(x_ij, 2) + pow(y_ij, 2) + pow(z_ij, 2))};

            numerator += fcFunction(r_ij, m_rMinStein, m_rMaxStein) * ylmFunction(m, l, x_ij, y_ij, z_ij);
            denominator += fcFunction(r_ij, m_rMinStein, m_rMaxStein);
        }
    }
    return numerator / denominator;
}

double Descriptors::ylmFunction(int m, int l, double dx, double dy, double dz)
{
    // spherical angles of vector (dx, dy, dz)
    double phi{getSphericalPhi(dx, dy, dz)};
    double theta{getSphericalTheta(dx, dy, dz)};

    // return real form spherical harmonics in form Y_lm
    //      sph_harm() returns Y_l^m --> wikipedia
    if (m < 0)
    {
        return pow(-1, m) * M_SQRT2 * boost::math::spherical_harmonic_i(l, abs(m), theta, phi);
    }
    else if (m > 0)
    {
        return pow(-1, m) * M_SQRT2 * boost::math::spherical_harmonic_r(l, m, theta, phi);
    }
    // m == 0
    return boost::math::spherical_harmonic_r(l, m, theta, phi);
}

double Descriptors::getSphericalR(double x, double y, double z)
{
    return sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2));
}

double Descriptors::getSphericalPhi(double x, double y, double z)
{
    return atan2(y, x);
}

double Descriptors::getSphericalTheta(double x, double y, double z)
{
    return acos(z / getSphericalR(x, y, z));
}
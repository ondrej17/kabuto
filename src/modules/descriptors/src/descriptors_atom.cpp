#include "descriptors_atom.h"

void Atom::calculateDescriptors(const double pbcX,
                                const double pbcY,
                                const double pbcZ,
                                const std::vector<int> &atomsInVerletListIds,
                                std::map<int, Atom> &atomsInVerletList,
                                const double rMinSym,
                                const double rMaxSym,
                                const double rMinStein,
                                const double rMaxStein,
                                const std::vector <std::vector<double>> &g2FunctionParameters,
                                const std::vector<double> &g3FunctionParameters,
                                const std::vector<int> &steinhardtFunctionParameters) {
    auto start = std::chrono::steady_clock::now();
    evaluateSymmetryFunctions(pbcX,
                              pbcY,
                              pbcZ,
                              atomsInVerletListIds,
                              atomsInVerletList,
                              rMinSym, rMaxSym,
                              g2FunctionParameters,
                              g3FunctionParameters);
    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double> duration = end - start;
//    std::cout << "\t\t" << duration.count() << "s - Symmetry ..." << std::endl;

    start = std::chrono::steady_clock::now();
    evaluateSteinhardtParameters(pbcX,
                                 pbcY,
                                 pbcZ,
                                 atomsInVerletListIds,
                                 atomsInVerletList,
                                 rMinStein,
                                 rMaxStein,
                                 steinhardtFunctionParameters);

    end = std::chrono::steady_clock::now();
    duration = end - start;
//    std::cout << "\t\t" << duration.count() << "s - Steinhardt ..." << std::endl
//              << std::endl;
}

void Atom::evaluateSymmetryFunctions(const double pbcX,
                                     const double pbcY,
                                     const double pbcZ,
                                     const std::vector<int> &atomsInVerletListIds,
                                     std::map<int, Atom> &atomsInVerletList,
                                     const double rMinSym,
                                     const double rMaxSym,
                                     const std::vector <std::vector<double>> &g2FunctionParameters,
                                     const std::vector<double> &g3FunctionParameters) {
    double myX{atomsInVerletList.at(m_id).getX()};
    double myY{atomsInVerletList.at(m_id).getY()};
    double myZ{atomsInVerletList.at(m_id).getZ()};

    for (int id : atomsInVerletListIds) {
        if (m_id != id) { // skip myself

            // coordinates of other atom
            double otherX{atomsInVerletList.at(id).getX()};
            double otherY{atomsInVerletList.at(id).getY()};
            double otherZ{atomsInVerletList.at(id).getZ()};

            // components of the vector r_ij
            double x_ij{otherX - myX};
            double y_ij{otherY - myY};
            double z_ij{otherZ - myZ};

            // correction of vector r_ij for PBC (and minimum image convention)
            x_ij -= pbcX * round(x_ij / pbcX);
            y_ij -= pbcY * round(y_ij / pbcY);
            z_ij -= pbcZ * round(z_ij / pbcZ);

            // calculate the correct length of vector r_ij
            double r_ij{getSphericalR(x_ij, y_ij, z_ij)};

            // calculate value of fcFunction
            double fcValue{fcFunction(r_ij, rMinSym, rMaxSym)};

            // add correct contributions to correct descriptors
            int index{0};
            for (const std::vector<double> &params : g2FunctionParameters) {
                m_descriptors.at(index) += fcValue * exp(-params.at(0) * pow(r_ij - params.at(1), 2));
                index++;
            }
            for (const double &param : g3FunctionParameters) {
                m_descriptors.at(index) += fcValue * cos(param * r_ij);
                index++;
            }
        }
    }
}

void Atom::evaluateSteinhardtParameters(const double pbcX,
                                        const double pbcY,
                                        const double pbcZ,
                                        const std::vector<int> &atomsInVerletListIds,
                                        std::map<int, Atom> &atomsInVerletList,
                                        const double rMinStein,
                                        const double rMaxStein,
                                        const std::vector<int> &steinhardtFunctionParameters) {
    double myX{atomsInVerletList.at(m_id).getX()};
    double myY{atomsInVerletList.at(m_id).getY()};
    double myZ{atomsInVerletList.at(m_id).getZ()};

    std::array<double, 2 * 6 + 1> numerator6{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
    std::array<double, 2 * 6 + 1> denominator6{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
    std::array<double, 2 * 7 + 1> numerator7{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
    std::array<double, 2 * 7 + 1> denominator7{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                               0.0};
    std::array<double, 2 * 8 + 1> numerator8{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                             0.0, 0.0};
    std::array<double, 2 * 8 + 1> denominator8{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                               0.0, 0.0, 0.0};

    for (int id : atomsInVerletListIds) {
        if (m_id != id) { // skip myself

            // coordinates of other atom
            double otherX{atomsInVerletList.at(id).getX()};
            double otherY{atomsInVerletList.at(id).getY()};
            double otherZ{atomsInVerletList.at(id).getZ()};

            // components of the vector r_ij
            double x_ij{otherX - myX};
            double y_ij{otherY - myY};
            double z_ij{otherZ - myZ};

            // correction of vector r_ij for PBC (and minimum image convention)
            x_ij -= pbcX * round(x_ij / pbcX);
            y_ij -= pbcY * round(y_ij / pbcY);
            z_ij -= pbcZ * round(z_ij / pbcZ);

            // calculate the correct length of vector r_ij
            double r_ij{sqrt(pow(x_ij, 2) + pow(y_ij, 2) + pow(z_ij, 2))};
            // double r_ij{getSphericalR(x_ij, y_ij, z_ij)};

            // calculate value of fcFunction
            double fcValue{fcFunction(r_ij, rMinStein, rMaxStein)};

            int index6{0};
            int index7{0};
            int index8{0};

            for (int m = -8; m <= 8; m++) {
                if (m >= -6 && m <= 6) {
                    numerator6[index6] += fcValue * ylmFunction(m, 6, x_ij, y_ij, z_ij);
                    denominator6[index6] += fcValue;
                    index6++;
                }
                if (m >= -7 && m <= 7) {
                    numerator7[index7] += fcValue * ylmFunction(m, 7, x_ij, y_ij, z_ij);
                    denominator7[index7] += fcValue;
                    index7++;
                }
                numerator8[index8] += fcValue * ylmFunction(m, 8, x_ij, y_ij, z_ij);
                denominator8[index8] += fcValue;
                index8++;
            }
        }
    }

    // calculate steinhardt parameter for l = 6
    double result;
    int numOfElements;

    result = 0;
    numOfElements = numerator6.size();
    for (int index{0}; index < numOfElements; index++) {
        result += pow(fabs(numerator6.at(index) / denominator6.at(index)), 2);
    }
    m_descriptors.at(11) = sqrt(result * 4 * M_PI / (2 * 6 + 1));

    // calculate steinhardt parameter for l = 7
    result = 0;
    numOfElements = numerator7.size();
    for (int index{0}; index < numOfElements; index++) {
        result += pow(fabs(numerator7.at(index) / denominator7.at(index)), 2);
    }
    m_descriptors.at(12) = sqrt(result * 4 * M_PI / (2 * 7 + 1));

    // calculate steinhardt parameter for l = 8
    result = 0;
    numOfElements = numerator8.size();
    for (int index{0}; index < numOfElements; index++) {
        result += pow(fabs(numerator8.at(index) / denominator8.at(index)), 2);
    }
    m_descriptors.at(13) = sqrt(result * 4 * M_PI / (2 * 8 + 1));

    // print(m_descriptors);
}

//double Atom::symmetryFunctionG2(const double eta,
//                                const double rs,
//                                const double pbcX,
//                                const double pbcY,
//                                const double pbcZ,
//                                const std::vector<int> &atomsInVerletListIds,
//                                std::map<int, Atom> &atomsInVerletList)
//{
//    double result{0.0};
//    double myX{atomsInVerletList.at(m_id).getX()};
//    double myY{atomsInVerletList.at(m_id).getY()};
//    double myZ{atomsInVerletList.at(m_id).getZ()};
//
//    for (int id : atomsInVerletListIds)
//    {
//        if (m_id != id)
//        { // skip myself
//
//            // coordinates of other atom
//            double otherX{atomsInVerletList.at(id).getX()};
//            double otherY{atomsInVerletList.at(id).getY()};
//            double otherZ{atomsInVerletList.at(id).getZ()};
//
//            // components of the vector r_ij
//            double x_ij{otherX - myX};
//            double y_ij{otherY - myY};
//            double z_ij{otherZ - myZ};
//
//            // correction of vector r_ij for PBC (and minimum image convention)
//            x_ij -= pbcX * round(x_ij / pbcX);
//            y_ij -= pbcY * round(y_ij / pbcY);
//            z_ij -= pbcZ * round(z_ij / pbcZ);
//
//            // calculate the correct length of vector r_ij
//            double r_ij{sqrt(pow(x_ij, 2) + pow(y_ij, 2) + pow(z_ij, 2))};
//
//            // add correct contribution to result
//            result += fcFunction(r_ij, m_rMinSym, m_rMaxSym) * exp(-eta * pow(r_ij - rs, 2));
//        }
//    }
//    return result;
//}
//
//double Atom::symmetryFunctionG3(const double kappa,
//                                const double pbcX,
//                                const double pbcY,
//                                const double pbcZ,
//                                const std::vector<int> &atomsInVerletListIds,
//                                std::map<int, Atom> &atomsInVerletList)
//{
//    double result{0.0};
//    double myX{atomsInVerletList.at(m_id).getX()};
//    double myY{atomsInVerletList.at(m_id).getY()};
//    double myZ{atomsInVerletList.at(m_id).getZ()};
//
//    for (int id : atomsInVerletListIds)
//    {
//        if (m_id != id)
//        { // skip myself
//
//            // coordinates of other atom
//            double otherX{atomsInVerletList.at(id).getX()};
//            double otherY{atomsInVerletList.at(id).getY()};
//            double otherZ{atomsInVerletList.at(id).getZ()};
//
//            // vector r_ij
//            double x_ij{otherX - myX};
//            double y_ij{otherY - myY};
//            double z_ij{otherZ - myZ};
//
//            // correction of vector r_ij for PBC (and minimum image convention)
//            x_ij -= pbcX * round(x_ij / pbcX);
//            y_ij -= pbcY * round(y_ij / pbcY);
//            z_ij -= pbcZ * round(z_ij / pbcZ);
//
//            // calculate the correct length of vector r_ij
//            double r_ij{sqrt(pow(x_ij, 2) + pow(y_ij, 2) + pow(z_ij, 2))};
//
//            // add correct contribution to result
//            result += fcFunction(r_ij, m_rMinSym, m_rMaxSym) * cos(kappa * r_ij);
//        }
//    }
//    return result;
//}
//
//double Atom::steinhardtFunction(const int l,
//                                const double pbcX,
//                                const double pbcY,
//                                const double pbcZ,
//                                const std::vector<int> &atomsInVerletListIds,
//                                std::map<int, Atom> &atomsInVerletList)
//{
//    double result{0.0};
//
//    for (int m = -l; m <= l; m++)
//    {
//        result += pow(fabs(qlmFunction(m, l, pbcX, pbcY, pbcZ, atomsInVerletListIds, atomsInVerletList)), 2);
//    }
//    return sqrt(result * 4 * M_PI / (2 * l + 1));
//}

double Atom::fcFunction(const double r,
                        const double rMin,
                        const double rMax) {
    if (r <= rMin) {
        return 1.0;
    } else if ((rMin < r) && (r <= rMax)) {
        return 0.5 + 0.5 * cos(M_PI * (r - rMin) / (rMax - rMin));
    } else {
        return 0.0;
    }
}

double Atom::qlmFunction(const int m,
                         const int l,
                         const double pbcX,
                         const double pbcY,
                         const double pbcZ,
                         const std::vector<int> &atomsInVerletListIds,
                         std::map<int, Atom> &atomsInVerletList,
                         const double rMinStein,
                         const double rMaxStein) {
    double myX{atomsInVerletList.at(m_id).getX()};
    double myY{atomsInVerletList.at(m_id).getY()};
    double myZ{atomsInVerletList.at(m_id).getZ()};

    double numerator{0.0};
    double denominator{0.0};

    for (int id : atomsInVerletListIds) {
        if (m_id != id) { // skip myself

            // coordinates of other atom
            double otherX{atomsInVerletList.at(id).getX()};
            double otherY{atomsInVerletList.at(id).getY()};
            double otherZ{atomsInVerletList.at(id).getZ()};

            // vector r_ij
            double x_ij{otherX - myX};
            double y_ij{otherY - myY};
            double z_ij{otherZ - myZ};

            // correction of vector r_ij for PBC (and minimum image convention)
            x_ij -= pbcX * round(x_ij / pbcX);
            y_ij -= pbcY * round(y_ij / pbcY);
            z_ij -= pbcZ * round(z_ij / pbcZ);

            // calculate the correct length of vector r_ij
            double r_ij{sqrt(pow(x_ij, 2) + pow(y_ij, 2) + pow(z_ij, 2))};

            numerator += fcFunction(r_ij, rMinStein, rMaxStein) * ylmFunction(m, l, x_ij, y_ij, z_ij);
            denominator += fcFunction(r_ij, rMinStein, rMaxStein);
        }
    }
    return numerator / denominator;
}

double Atom::ylmFunction(const int m,
                         const int l,
                         const double dx,
                         const double dy,
                         const double dz) {
    // spherical angles of vector (dx, dy, dz)
    double phi{getSphericalPhi(dx, dy, dz)};
    double theta{getSphericalTheta(dx, dy, dz)};

    // return real form spherical harmonics in form Y_lm
    //      sph_harm() returns Y_l^m --> wikipedia
    if (m < 0) {
        return pow(-1, m) * M_SQRT2 * std::sph_legendre(l, abs(m), theta) * sin(abs(m) * phi);
    } else if (m > 0) {
        return pow(-1, m) * M_SQRT2 * std::sph_legendre(l, m, theta) * cos(m * phi);
    }
    // m == 0
    return std::sph_legendre(l, m, theta);
}

double Atom::getSphericalR(const double x,
                           const double y,
                           const double z) {
    return sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2));
}

double Atom::getSphericalPhi(const double x,
                             const double y,
                             const double z) {
    return atan2(y, x);
}

double Atom::getSphericalTheta(const double x,
                               const double y,
                               const double z) {
    return acos(z / getSphericalR(x, y, z));
}

void Atom::print(std::vector<double> const &input) {
    for (long unsigned int i = 0; i < input.size(); i++) {
        std::cout << input.at(i) << ' ';
    }
    std::cout << std::endl;
}

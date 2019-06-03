/*
 *  bris_translate.hpp
 *  fdtdutils
 *
 *  Created by Ian Buss on 12/08/2009.
 *  Copyright 2009 __MyCompanyName__. All rights reserved.
 *
 */

#ifndef BRIS_TRANSLATE_HPP_INCLUDED
#define BRIS_TRANSLATE_HPP_INCLUDED

#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <complex>
#include <cstdlib>
#include <locale>
#include <set>
#include <algorithm>

#include "bris_sim.hpp"

#define A 1e-6
#define CSPEED 2.99792458e8

namespace fdtdutils {
  class sim_translation : public sim {
  protected:
    float dimensions[3];
    float resolution;
    int rank,n_probes,n_snaps;
  public:
    sim_translation() { }
    sim_translation(const std::string &fname);
    void translate(const std::string &out, bool verbose);
    friend void get_dimensions(sim_translation* trans,bool verbose);
    friend void print_resolution(std::ofstream &of, sim_translation* trans,bool verbose);
    friend void print_geom_lattice(std::ofstream &of, sim_translation* trans,bool verbose);
    friend void print_geometries(std::ofstream &of, sim_translation* trans,bool verbose);
    friend void print_sources(std::ofstream &of, sim_translation* trans,bool verbose);
    friend void print_boundaries(std::ofstream &of, sim_translation* trans,bool verbose);
    friend void print_run_info(std::ofstream &of, sim_translation* trans,bool verbose);
  };
  
  void preamble(std::ofstream& of,bool verbose);
}

#endif
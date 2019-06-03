/*
 *  bris_sim.hpp
 *  fdtdutils
 *
 *  Created by Ian Buss on 12/08/2009.
 *  Copyright 2009 __MyCompanyName__. All rights reserved.
 *
 */
#ifndef BRIS_SIM_HPP_INCLUDED
#define BRIS_SIM_HPP_INCLUDED

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

namespace fdtdutils {
  
  const std::string COMPS[] = {"box","block","cylinder","distorted_block","sphere","tube","excitation","probe","frequency_snapshot",
  "snapshot","boundary","flag","xmesh","ymesh","zmesh","nodes"};
  
  const char COMMENT = '*';
  
  struct point {
    float x, y, z;
  };
  
  struct boundary_param {
    int type;
    float p[3];
  };
  
  struct param {
    std::string s;
    float f;
  };
  
  class sim_entity {
  protected:
    std::string comp_type;
    int id;
  public:
    //void entity_type ();
    virtual void init_entity(std::vector<param>& plist, int id_)=0;
    virtual void print_entity()=0;
    std::string type() { return comp_type; }
  };
  
  class object {
  protected:
    std::vector<param> param_list;
    std::string obj_name;
  public:
    object(std::ifstream& in, const std::string obj_name_);
    void print_object();
    sim_entity* process_object(int id_);
  };
    
  class geom_entity : public sim_entity {
  protected:
    point p1,p2,p3,p4,p5,p6,p7,p8;
    float eps, sigma;
  public:
    void init_entity(std::vector<param>& plist, int id_) {};
    void print_entity() {};
    friend void get_eps(geom_entity* g, float* eps_);
  };
  
  class box : public geom_entity {
  public:
    void init_entity(std::vector<param>& plist, int id_);
    void print_entity();
    friend void dims(box* b, float dims_[]);
  };
  
  class block : public geom_entity {
  public:
    void init_entity(std::vector<param>& plist, int id_);
    void print_entity();
    friend void centre(block* b, float* c, int axis);
    friend void size(block* b, float* c, int axis);
  };
  
  class cylinder : public geom_entity {
    float r1,r2,h;
  public:
    void init_entity(std::vector<param>& plist, int id_);
    void print_entity();
    friend void centre(cylinder* c, float cen[]);
    friend void size(cylinder* c, float size[]);
  };
  
  class sphere : public geom_entity {
    float r1,r2;
  public:
    void init_entity(std::vector<param>& plist, int id_);
    void print_entity();
    friend void centre(sphere* s, float cen[]);
    friend void size(sphere* s, float size[]);
  };
  
  class distorted_block : public geom_entity {
  public:
    void init_entity(std::vector<param>& plist, int id_);
    void print_entity();
  };
  
  class tube : public geom_entity {
    float a1,b1,a2,b2;
    int plane;
  public:
    void init_entity(std::vector<param>& plist, int id_);
    void print_entity();
  };
  
  class control_entity : public sim_entity {
  protected:
  public:
    void init_entity(std::vector<param>& plist) {};
    void print_entity() {};
  };
  
  class excitation : public control_entity {
    point p1,p2;
    int s_type,s_func;
    bool ex,ey,ez,hx,hy,hz;
    float tc,amp,offset,freq;
  public:
    void init_entity(std::vector<param>& plist, int id_);
    void print_entity();
    friend void func_type(excitation* e, int* func);
    friend void centre(excitation* e, float* c, int axis);
    friend void size(excitation* e, float* s, int axis);
    friend void ex_props(excitation* e, float props[]);
    friend void component(excitation* e, std::string &s);
  };
  
  class probe : public control_entity {
    point p1;
    int step;
    bool ex,ey,ez,hx,hy,hz,jx,jy,jz,pow;
  public:
    void init_entity(std::vector<param>& plist, int id_);
    void print_entity();
    void get_probe_info(float loc[],int* st,bool fields[]);
  };
  
  class snapshot : public control_entity {
    int first,repetition,plane;
    point p1,p2;
    bool ex,ey,ez,hx,hy,hz,jx,jy,jz,pow;
  public:
    void init_entity(std::vector<param>& plist, int id_);
    void print_entity();
    void get_snap_info(float cen[3],float size[3],int* repetition, int* first,char* plane_,bool fields[6]);
  };
  
  class flag : public control_entity {
    int niter;
    float tmult;
    std::string id_char;
  public:
    void init_entity(std::vector<param>& plist, int id_);
    void print_entity();
    void get_flags(std::string& ident, int* niter);
  };
  
  class boundary : public control_entity {
    boundary_param b1,b2,b3,b4,b5,b6;
    bool absorbing;
  public:
    void init_entity(std::vector<param>& plist, int id_);
    void print_entity();
    friend void boundaries(boundary* b, boundary_param bpars[]);
  };
  
  class nodes : public control_entity {
    int x,y,z;
  public:
    void init_entity(std::vector<param>& plist, int id_);
    void print_entity();
    void get_nodes(float nnodes[]);
  };
  
  class mesh : public control_entity {
    int x,y,z;
    std::vector<float> mesh_;
  public:
    void init_entity(std::vector<param>& plist, int id_);
    void print_entity();
    float get_min_mesh();
  };
  
  class sim {
  protected:
    std::vector<object*> objects;
    std::vector<sim_entity*> sim_entities;
  public:
    sim() { }
    sim(const std::string &fname);
    ~sim();
    void read_in_file(const std::string &fname);
    void print_objects();
    void process_objects(bool verbose);
  };	

}

#endif
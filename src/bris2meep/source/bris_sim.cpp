/*
 *  bris2meep.cpp
 *  fdtdutils
 *
 *  Created by Ian Buss on 12/08/2009.
 *  Copyright 2009 __MyCompanyName__. All rights reserved.
 *
 */

#include "bris_sim.hpp"

namespace fdtdutils {
  sim::sim(const std::string &fname) {
    read_in_file(fname);
  }
  
  sim::~sim() {
    for (int i=0;i<objects.size();++i) { delete objects[i]; }
    for (int i=0;i<sim_entities.size();++i) { delete sim_entities[i]; }
    objects.clear();
    sim_entities.clear();
  }

  void sim::read_in_file(const std::string &fname) {
    /* Read the text file into memory. */
    std::string word,line;
    std::ifstream infile;
    std::set<std::string> comp_set;
    for (int i=0;i<sizeof(COMPS)/sizeof(COMPS[0]);++i) {
      comp_set.insert(COMPS[i]);
    }
    
    infile.open(fname.c_str(),std::ios::in);
    if (infile.is_open()) {
      while (!infile.eof()) {
        infile >> word;
        std::transform (word.begin(), word.end(), word.begin(), ::tolower);
        if (word[0]==COMMENT) { getline(infile,line); }
        else if (comp_set.count(word)>0) {
          objects.push_back(new object(infile,word));
        }
      }
    }
    else { 
      std::cerr << "Could not open input file " << fname << std::endl;
      exit(1);
    }
  }
  
  void sim::print_objects() {
    std::cout.precision(std::ios::scientific);
    for (int i=0;i<objects.size();++i) {
      std::cout << "object " << std::setw(3) << i << std::endl;
      objects[i]->print_object();
    }
  }
  
  void sim::process_objects(bool verbose) {
    sim_entity* n_ent=0;
    for (int i=0;i<objects.size();++i) {
      n_ent=objects[i]->process_object(i);
      if (n_ent!=0) { 
        sim_entities.push_back(n_ent); 
        //if (verbose) { n_ent->print_entity(); }
      }
    }
    //if (frsnap==true) { std::cerr << "WARNING: frequency_snapshots not yet implemented\n"; }
  }
  
  object::object(std::ifstream& in, const std::string obj_name_) {
    std::string word, line, s;
    param tmp_parm;
    obj_name=obj_name_;
    while (word!="{") { 
      in >> word;
      if (word[0]==COMMENT) { getline(in,line); }
    }
    while (word!="}") {
      tmp_parm.s.clear();
      in >> word;
      if (word[0]==COMMENT) { 
        getline(in,line);
      }
      else if (word!="}") { 
        tmp_parm.s=word;
        tmp_parm.f=atof(tmp_parm.s.c_str());
        param_list.push_back(tmp_parm);
      }
    }		
  }
  
  void object::print_object() {
    std::cout.precision(6);
    std::cout.setf(std::ios::scientific);
    std::cout << obj_name << std::endl;
    for (int i=0;i<param_list.size();++i) {
      std::cout << " " << std::setw(3) << i << "\t";
      std::cout << param_list[i].s << "\t\t" << param_list[i].f << std::endl;
    }
  }
  
  sim_entity* object::process_object(int id_) {
    bool frsnap=false;
    sim_entity* ps_e=0;
    if (obj_name=="box") { ps_e=new box(); }
    else if (obj_name=="block") { ps_e=new block();	}
    else if (obj_name=="cylinder") { ps_e=new cylinder(); }
    else if (obj_name=="flag") { ps_e=new flag(); }
    else if (obj_name=="boundary") { ps_e=new boundary(); }
    else if (obj_name=="nodes") { ps_e=new nodes();	}
    else if (obj_name=="probe") { ps_e=new probe();	}
    else if (obj_name=="snapshot") { ps_e=new snapshot(); }
    else if (obj_name=="excitation") { ps_e=new excitation(); }
    else if (obj_name=="xmesh") { ps_e=new mesh(); }
    else if (obj_name=="ymesh") { ps_e=new mesh(); }
    else if (obj_name=="zmesh") { ps_e=new mesh(); }
    else if (obj_name=="frequency_snapshot") {
      //ps_e=new probe();
    }
    
    if (frsnap==true) { std::cerr << "WARNING: frequency_snapshots not yet implemented\n"; }
    
    if (ps_e!=0) { ps_e->init_entity(param_list,id_); }

    
    return ps_e;
  }
  
  void get_eps(geom_entity* g, float* eps_) {
    *eps_=g->eps;
  }
  
  void block::init_entity(std::vector<param>& plist, int id_) {
    comp_type="block";
    id=id_;
    p1.x=plist[0].f; p1.y=plist[1].f; p1.z=plist[2].f;
    p2.x=plist[3].f; p2.y=plist[4].f; p2.z=plist[5].f;
    eps=plist[6].f;
    sigma=plist[7].f;
  }
  
  void block::print_entity() {
    std::cout.precision(6);
    std::cout.setf(std::ios::scientific);
    std::cout << "block, component id " << id << std::endl;
    std::cout << "\tx1: " << p1.x << " y1: " << p1.y << " z1: " << p1.z << std::endl;
    std::cout << "\tx2: " << p2.x << " y2: " << p2.y << " z2: " << p2.z << std::endl;
    std::cout << "\teps: " << eps << std::endl;
    std::cout << "\tsigma: " << sigma << std::endl;
  }
  
  void centre(block* b, float* c, int axis) {
    if (axis==1) { *c=((b->p2.x-b->p1.x)/2)+b->p1.x; }
    if (axis==2) { *c=((b->p2.y-b->p1.y)/2)+b->p1.y; }
    if (axis==3) { *c=((b->p2.z-b->p1.z)/2)+b->p1.z; }
  }
  
  void size(block* b, float* c, int axis) {
    if (axis==1) { *c=(b->p2.x)-(b->p1.x); }
    if (axis==2) { *c=(b->p2.y)-(b->p1.y); }
    if (axis==3) { *c=(b->p2.z)-(b->p1.z); }
  }
  
  void cylinder::init_entity(std::vector<param>& plist, int id_) {
    comp_type="cylinder";
    id=id_;
    p1.x=plist[0].f; p1.y=plist[1].f; p1.z=plist[2].f;
    r1=plist[3].f; r2=plist[4].f; h=plist[5].f;
    eps=plist[6].f;
    sigma=plist[7].f;
  }
  
  void cylinder::print_entity() {
    std::cout.precision(6);
    std::cout.setf(std::ios::scientific);
    std::cout << "cylinder, component id " << id << std::endl;
    std::cout << "\txc: " << p1.x << " yc: " << p1.y << " zc: " << p1.z << std::endl;
    std::cout << "\tr1: " << r1 << " r2: " << r2 << " h: " << h << std::endl;
    std::cout << "\teps: " << eps << std::endl;
    std::cout << "\tsigma: " << sigma << std::endl;
  }
  
  void centre(cylinder* c, float cen[]) {
    cen[0]=c->p1.x;
    cen[1]=c->p1.y;
    cen[2]=c->p1.z;
  }
  
  void size(cylinder* c, float size[]) {
    size[0]=c->r1;
    size[1]=c->r2;
    size[2]=c->h;
  }
  
  void sphere::init_entity(std::vector<param>& plist, int id_) {
    comp_type="sphere";
    id=id_;
    p1.x=plist[0].f; p1.y=plist[1].f; p1.z=plist[2].f;
    r1=plist[3].f; r2=plist[4].f;
    eps=plist[5].f;
    sigma=plist[6].f;
  }
  
  void sphere::print_entity() {
    std::cout.precision(6);
    std::cout.setf(std::ios::scientific);
    std::cout << "sphere, component id " << id << std::endl;
    std::cout << "\txc: " << p1.x << " yc: " << p1.y << " zc: " << p1.z << std::endl;
    std::cout << "\tr1: " << r1 << " r2: " << r2 << std::endl;
    std::cout << "\teps: " << eps << std::endl;
    std::cout << "\tsigma: " << sigma << std::endl;
  }
  
  void centre(sphere* s, float cen[]) {
    cen[0]=s->p1.x;
    cen[1]=s->p1.y;
    cen[2]=s->p1.z;
  }
  
  void size(sphere* s, float size[]) {
    size[0]=s->r1;
  }
  
  void distorted_block::init_entity(std::vector<param>& plist, int id_) {
    comp_type="distorted_block";
    id=id_;
    p1.x=plist[0].f; p1.y=plist[1].f; p1.z=plist[2].f;
    p2.x=plist[3].f; p2.y=plist[4].f; p2.z=plist[5].f;
    p3.x=plist[6].f; p3.y=plist[7].f; p3.z=plist[8].f;
    p4.x=plist[9].f; p4.y=plist[10].f; p4.z=plist[11].f;
    p5.x=plist[12].f; p5.y=plist[13].f; p5.z=plist[14].f;
    p6.x=plist[15].f; p6.y=plist[16].f; p6.z=plist[17].f;
    p7.x=plist[18].f; p7.y=plist[19].f; p7.z=plist[20].f;
    p8.x=plist[21].f; p8.y=plist[22].f; p8.z=plist[23].f;
    eps=plist[24].f;
    sigma=plist[25].f;
  }
  
  void distorted_block::print_entity() {
    std::cout.precision(6);
    std::cout.setf(std::ios::scientific);
    std::cout << "distorted block, component id " << id << std::endl;
    std::cout << "\tx1: " << p1.x << " y1: " << p1.y << " z1: " << p1.z << std::endl;
    std::cout << "\tx2: " << p2.x << " y2: " << p2.y << " z2: " << p2.z << std::endl;
    std::cout << "\tx3: " << p3.x << " y3: " << p3.y << " z3: " << p3.z << std::endl;
    std::cout << "\tx4: " << p4.x << " y4: " << p4.y << " z4: " << p4.z << std::endl;
    std::cout << "\tx5: " << p5.x << " y5: " << p5.y << " z5: " << p5.z << std::endl;
    std::cout << "\tx6: " << p6.x << " y6: " << p6.y << " z6: " << p6.z << std::endl;
    std::cout << "\tx7: " << p7.x << " y7: " << p7.y << " z7: " << p7.z << std::endl;
    std::cout << "\tx8: " << p8.x << " y8: " << p8.y << " z8: " << p8.z << std::endl;
    std::cout << "\teps: " << eps << std::endl;
    std::cout << "\tsigma: " << sigma << std::endl;
  }
  
  void tube::init_entity(std::vector<param>& plist, int id_) {
    comp_type="tube";
    id=id_;
    p1.x=plist[0].f; p1.y=plist[1].f; p1.z=plist[2].f;
    a1=plist[3].f; b1=plist[4].f;
    p2.x=plist[5].f; p2.y=plist[6].f; p2.z=plist[7].f;
    a2=plist[8].f; b2=plist[9].f;
    plane=plist[10].f;
    eps=plist[11].f;
    sigma=plist[12].f;
  }
  
  void tube::print_entity() {
    std::cout.precision(6);
    std::cout.setf(std::ios::scientific);
    std::cout << "tube, component id " << id << std::endl;
    std::cout << "\tx1: " << p1.x << " y1: " << p1.y << " z1: " << p1.z << std::endl;
    std::cout << "\ta1: " << a1 << " b1: " << b1 << " h: " << std::endl;
    std::cout << "\tx2: " << p2.x << " y2: " << p2.y << " z2: " << p2.z << std::endl;
    std::cout << "\ta2: " << a2 << " b2: " << b2 << " h: " << std::endl;
    std::cout << "\teps: " << eps << std::endl;
    std::cout << "\tsigma: " << sigma << std::endl;
  }
  
  void box::init_entity(std::vector<param>& plist, int id_) {
    comp_type="box";
    id=id_;
    p1.x=plist[0].f; p1.y=plist[1].f; p1.z=plist[2].f;
    p2.x=plist[3].f; p2.y=plist[4].f; p2.z=plist[5].f;
  }
  
  void box::print_entity() {
    std::cout.precision(6);
    std::cout.setf(std::ios::scientific);
    std::cout << "box, component id " << id << std::endl;
    std::cout << "\tx1: " << p1.x << " y1: " << p1.y << " z1: " << p1.z << std::endl;
    std::cout << "\tx2: " << p2.x << " y2: " << p2.y << " z2: " << p2.z << std::endl;
  }
  
  void dims(box* b, float dims_[]) {
    dims_[0]=b->p2.x-b->p1.x;
    dims_[1]=b->p2.y-b->p1.y;
    dims_[2]=b->p2.z-b->p1.z;
  }
  
  void excitation::init_entity(std::vector<param>& plist, int id_) {
    comp_type="excitation";
    id=id_;
    s_type=(int)plist[0].f;
    p1.x=plist[1].f; p1.y=plist[2].f; p1.z=plist[3].f;
    p2.x=plist[4].f; p2.y=plist[5].f; p2.z=plist[6].f;
    ex=(bool) plist[7].f; ey=(bool) plist[8].f; ez=(bool) plist[9].f;
    hx=(bool) plist[10].f; hy=(bool) plist[11].f; hz=(bool) plist[12].f;
    s_func=(int)plist[13].f;
    tc=plist[14].f;
    amp=plist[15].f;
    offset=plist[16].f;
    freq=plist[17].f;
  }
  
  void excitation::print_entity() {
    std::cout.precision(6);
    std::cout.setf(std::ios::scientific);
    std::cout << "excitation, component id " << id << std::endl;
    std::cout << "\tx1: " << p1.x << " y1: " << p1.y << " z1: " << p1.z << std::endl;
    std::cout << "\tx2: " << p2.x << " y2: " << p2.y << " z2: " << p2.z << std::endl;
    std::cout << "\tex: " << ex << " ey: " << ey << " ez: " << ez << std::endl;
    std::cout << "\thx: " << hx << " hy: " << hy << " hz: " << hz << std::endl;
    std::cout << "\ttype: " << s_type << std::endl;
    std::cout << "\tfunc: " << s_func << std::endl;
    std::cout << "\ttime constant: " << tc << std::endl;
    std::cout << "\tamplitude: " << amp << std::endl;
    std::cout << "\ttime offset: " << offset << std::endl;
    std::cout << "\tfrequency: " << freq << std::endl;
  }
  
  void func_type(excitation* e, int* func) {
    *func=e->s_func;
  }
  
  void centre(excitation* e, float* c, int axis) {
    if (axis==1) { *c=((e->p2.x-e->p1.x)/2)+e->p1.x; }
    if (axis==2) { *c=((e->p2.y-e->p1.y)/2)+e->p1.y; }
    if (axis==3) { *c=((e->p2.z-e->p1.z)/2)+e->p1.z; }
  }
  
  void size(excitation* e, float* s, int axis) {
    if (axis==1) { *s=(e->p2.x-e->p1.x); }
    if (axis==2) { *s=(e->p2.y-e->p1.y); }
    if (axis==3) { *s=(e->p2.z-e->p1.z); }
  }
  
  void ex_props(excitation* e, float props[]) {
    props[0]=e->freq;
    props[1]=e->tc;
    props[2]=e->amp;
    props[3]=e->offset;
  }
  
  void component(excitation* e, std::string &s) {
    if (e->ex) { s="Ex"; }
    else if (e->ey) { s= "Ey"; }
    else if (e->ez) { s= "Ez"; }
    else if (e->hx) { s= "Hx"; }
    else if (e->hy) { s= "Hy"; }
    else if (e->hz) { s= "Hz"; }
  }
  
  void probe::init_entity(std::vector<param>& plist, int id_) {
    comp_type="probe";
    id=id_;
    p1.x=plist[0].f; p1.y=plist[1].f; p1.z=plist[2].f;
    step=(int) plist[3].f;
    ex=(bool) plist[4].f; ey=(bool) plist[5].f; ez=(bool) plist[6].f;
    hx=(bool) plist[7].f; hy=(bool) plist[8].f; hz=(bool) plist[9].f;
    jx=(bool) plist[10].f; jy=(bool) plist[11].f; jz=(bool) plist[12].f;
    pow=(bool) plist[13].f;
  }
  
  void probe::print_entity() {
    std::cout.precision(6);
    std::cout.setf(std::ios::scientific);
    std::cout << "probe, component id " << id << std::endl;
    std::cout << "\tx1: " << p1.x << " y1: " << p1.y << " z1: " << p1.z << std::endl;
    std::cout << "\tstep: " << step << std::endl;
    std::cout << "\tex: " << ex << " ey: " << ey << " ez: " << ez << std::endl;
    std::cout << "\thx: " << hx << " hy: " << hy << " hz: " << hz << std::endl;
    std::cout << "\tjx: " << jx << " jy: " << jy << " jz: " << jz << std::endl;
    std::cout << "\tpow: " << pow << std::endl;
  }
  
  void probe::get_probe_info(float loc[],int* st,bool fields[]) {
    loc[0]=p1.x; loc[1]=p1.y; loc[2]=p1.z;
    *st=step;
    fields[0]=ex; fields[1]=ey; fields[2]=ez;
    fields[3]=hx; fields[4]=hy; fields[5]=hz;
  }
  
  void snapshot::init_entity(std::vector<param>& plist, int id_) {
    comp_type="snapshot";
    id=id_;
    first=(int) plist[0].f;
    repetition=(int) plist[1].f;
    plane=(int) plist[2].f;
    p1.x=plist[3].f; p1.y=plist[4].f; p1.z=plist[5].f;
    p2.x=plist[6].f; p2.y=plist[7].f; p2.z=plist[8].f;
    ex=(bool) plist[9].f; ey=(bool) plist[10].f; ez=(bool) plist[11].f;
    hx=(bool) plist[12].f; hy=(bool) plist[13].f; hz=(bool) plist[14].f;
    jx=(bool) plist[15].f; jy=(bool) plist[16].f; jz=(bool) plist[17].f;
    pow=(bool) plist[18].f;
  }
  
  void snapshot::print_entity() {
    std::cout.precision(6);
    std::cout.setf(std::ios::scientific);
    std::cout << "snapshot, component id " << id << std::endl;
    std::cout << "\tx1: " << p1.x << " y1: " << p1.y << " z1: " << p1.z << std::endl;
    std::cout << "\tx2: " << p2.x << " y2: " << p2.y << " z2: " << p2.z << std::endl;
    std::cout << "\tfirst: " << first << std::endl;
    std::cout << "\trepetition: " << repetition << std::endl;
    std::cout << "\tplane: " << plane << std::endl;
    std::cout << "\tex: " << ex << " ey: " << ey << " ez: " << ez << std::endl;
    std::cout << "\thx: " << hx << " hy: " << hy << " hz: " << hz << std::endl;
    std::cout << "\tjx: " << jx << " jy: " << jy << " jz: " << jz << std::endl;
    std::cout << "\tpow: " << pow << std::endl;
  }
  
  void snapshot::get_snap_info(float cen[3],float size[3],int* rep, int* f,char* plane_,bool fields[6]) {
    size[0]=(p2.x-p1.x); size[1]=(p2.y-p1.y); size[2]=(p2.z-p1.z); 
    cen[0]=(p2.x-p1.x)/2+p1.x; cen[1]=(p2.y-p1.y)/2+p1.y; cen[2]=(p2.z-p1.z)/2+p1.z;
    *rep=repetition;
    *f=first;
    fields[0]=ex; fields[1]=ey; fields[2]=ez;
    fields[3]=hx; fields[4]=hy; fields[5]=hz;
    *plane_=char(int('x')+plane-1);
  }
  
  void flag::init_entity(std::vector<param>& plist, int id_) {
    comp_type="flag";
    id=id_;
    niter=plist[4].f;
    tmult=plist[5].f;
    id_char=plist[6].s;
    // Remove quotes
    id_char=id_char.substr(1,id_char.size()-2);
  }
  
  void flag::print_entity() {
    std::cout.precision(6);
    std::cout.setf(std::ios::scientific);
    std::cout << "flag, component id " << id << std::endl;
    std::cout << "\titerations: " << niter << std::endl;
    std::cout << "\tmultiplier: " << tmult << std::endl;
    std::cout << "\tID: " << id_char << std::endl;
  }
  
  void flag::get_flags(std::string& ident, int* niter_) {
    ident=id_char;
    *niter_=niter;
  }
  
  void boundary::init_entity(std::vector<param>& plist, int id_) {
    comp_type="boundary";
    id=id_;
    if (plist.size()==24) {
      absorbing=true;
      b1.type=(int) plist[0].f; b1.p[0]=plist[1].f; b1.p[1]=plist[2].f; b1.p[2]=plist[3].f;
      b2.type=(int) plist[4].f; b2.p[0]=plist[5].f; b2.p[1]=plist[6].f; b2.p[2]=plist[7].f;
      b3.type=(int) plist[8].f; b3.p[0]=plist[9].f; b3.p[1]=plist[10].f; b3.p[2]=plist[11].f;
      b4.type=(int) plist[12].f; b4.p[0]=plist[13].f; b4.p[1]=plist[14].f; b4.p[2]=plist[15].f;
      b5.type=(int) plist[16].f; b5.p[0]=plist[17].f; b5.p[1]=plist[18].f; b5.p[2]=plist[19].f;
      b6.type=(int) plist[20].f; b6.p[0]=plist[21].f; b6.p[1]=plist[22].f; b6.p[2]=plist[23].f;
    }
    else {
      absorbing=false;
      b1.type=(int) plist[0].f;
      b2.type=(int) plist[1].f;
      b3.type=(int) plist[2].f;
      b4.type=(int) plist[3].f;
      b5.type=(int) plist[4].f;
      b6.type=(int) plist[5].f;
    }
  }
  
  void boundary::print_entity() {
    std::cout.precision(6);
    std::cout.setf(std::ios::scientific);
    std::cout << "boundary, component id " << id << std::endl;
    std::cout << "\t1: " << b1.type << " " << b1.p[0] << std::endl;
    std::cout << "\t2: " << b2.type << " " << b2.p[0] << std::endl;
    std::cout << "\t3: " << b3.type << " " << b3.p[0] << std::endl;
    std::cout << "\t4: " << b4.type << " " << b4.p[0] << std::endl;
    std::cout << "\t5: " << b5.type << " " << b5.p[0] << std::endl;
    std::cout << "\t6: " << b6.type << " " << b6.p[0] << std::endl;
  }
  
  void boundaries(boundary* b, boundary_param bpars[]) {
    bpars[0]=b->b1;
    bpars[1]=b->b2;
    bpars[2]=b->b3;
    bpars[3]=b->b4;
    bpars[4]=b->b5;
    bpars[5]=b->b6;
  }
  
  void nodes::init_entity(std::vector<param>& plist, int id_) {
    comp_type="nodes";
    id=id_;
    x=(int) plist[0].f;
    y=(int) plist[1].f;
    z=(int) plist[2].f;
  }
  
  void nodes::print_entity() {
    std::cout.precision(6);
    std::cout.setf(std::ios::scientific);
    std::cout << "nodes, component id " << id << std::endl;
    std::cout << "\tx: " << x << std::endl;
    std::cout << "\ty: " << y << std::endl;
    std::cout << "\tz: " << z << std::endl;
  }
  
  void nodes::get_nodes(float nnodes[]) {
    nnodes[0]=x;
    nnodes[1]=y;
    nnodes[2]=z;
  }
  
  void mesh::init_entity(std::vector<param>& plist, int id_) {
    comp_type="mesh";
    id=id_;
    mesh_.resize(plist.size());
    for (int i=0;i<mesh_.size();++i) {
      mesh_[i]=plist[i].f;
    }
  }
  
  void mesh::print_entity() {
    for (int i=0;i<mesh_.size();++i) {
      std::cout<<mesh_[i];
    }
  }
  
  float mesh::get_min_mesh() {
    float m=mesh_[0];
    for (int i=1;i<mesh_.size();++i) {
      if (mesh_[i]<m) { m=mesh_[i]; }
    }
    return m;
  }
}

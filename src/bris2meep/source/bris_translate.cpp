/*
 *  bris_translate.cpp
 *  fdtdutils
 *
 *  Created by Ian Buss on 12/08/2009.
 *  Copyright 2009 __MyCompanyName__. All rights reserved.
 *
 */

#include <iostream>
using namespace std;

#include "bris_translate.hpp"

namespace fdtdutils {
  sim_translation::sim_translation(const std::string &fname) {
    read_in_file(fname);
    rank=3;
    for (int i=0;i<3;++i) { dimensions[i]=0; }
  }

  void sim_translation::translate(const std::string &fname, bool verbose) {
    std::ofstream of;

    of.open(fname.c_str(), std::ios::out);
    if (of.is_open()) {
      // Write preamble to simulation
      preamble(of,verbose);
      get_dimensions(this,verbose);
      print_resolution(of,this,verbose);
      print_geom_lattice(of,this,verbose);
      print_geometries(of,this,verbose);
      print_sources(of,this,verbose);
      print_boundaries(of,this,verbose);
      print_run_info(of,this,verbose);
    }
    of.close();
  }

  void preamble(std::ofstream& of,bool verbose) {
    of << ";preamble - some interesting settings" << std::endl;
    of << "(set! filename-prefix false)\n";
    of << "(set! output-single-precision? true)\n";
  }

  void get_dimensions(sim_translation* trans,bool verbose) {
    int i=0;
    bool found=false;
    while (i<trans->sim_entities.size() && !found) {
      // Get simulation dimensions
      if (trans->sim_entities[i]->type()=="box") {
        dims(dynamic_cast<box*>(trans->sim_entities[i]),trans->dimensions);
        if (trans->dimensions[0]*trans->dimensions[1]*trans->dimensions[2]==0) { trans->rank=2; }
        //if (trans->dimensions[0]*trans->dimensions[1]==0) { trans->rank=1; }
        found=true;
      }
      ++i;
    }
  }

  void print_resolution(std::ofstream &of, sim_translation* trans,bool verbose) {
    int i=0;
    bool found=false;
    float nxyz[3]={0,0,0};
    float dx,dy,dz,d=0,dtmp;

    while (i<trans->sim_entities.size() && !found) {
      // Get simulation resolution
      if (trans->sim_entities[i]->type()=="nodes") {
        dynamic_cast<nodes*>(trans->sim_entities[i])->get_nodes(nxyz);
        dx=trans->dimensions[0]/nxyz[0];
        dy=trans->dimensions[1]/nxyz[1];
        dz=trans->dimensions[2]/nxyz[2];
        if ((dx<=dy) && (dx<=dz)) { of << "(set-param! resolution " << 1/dx << ")\n"; trans->resolution=1/dx; }
        else if ((dy<=dx) && (dy<=dz)) { of << "(set-param! resolution " << 1/dy << ")\n"; trans->resolution=1/dy; }
        else if ((dz<=dx) && (dz<=dy)) { of << "(set-param! resolution " << 1/dz << ")\n"; trans->resolution=1/dz; }
        found=true;
      }
      if (trans->sim_entities[i]->type()=="mesh") {
        if (d==0) {
          d=dynamic_cast<mesh*>(trans->sim_entities[i])->get_min_mesh();
        }
        dtmp=dynamic_cast<mesh*>(trans->sim_entities[i])->get_min_mesh();
        if (dtmp<d) { d=dtmp; }
      }
      ++i;
    }

    if (!found && d!=0) { of << "(set-param! resolution " << 1/d << ")\n"; trans->resolution=1/d; }
  }

  void print_geom_lattice(std::ofstream &of, sim_translation* trans,bool verbose) {
    of << "\n;simulation size\n";
    of << "(define-param sx " << trans->dimensions[0] << ") ; x size\n";
    of << "(define-param sy " << trans->dimensions[1] << ") ; y size\n";
    of << "(define-param sz " << trans->dimensions[2] << ") ; z size\n";
    of << "(set! geometry-lattice (make lattice (size " << trans->dimensions[0] <<
      " " << trans->dimensions[1] << " " << trans->dimensions[2] << ")))\n";
    if (verbose) { std::cout << "Sim dimensions: " << trans->dimensions[0] << "x" <<
    trans->dimensions[1] << "x" << trans->dimensions[2] << std::endl; }
  }

  void print_geometries(std::ofstream &of, sim_translation* trans,bool verbose) {
    // To do
    //		- double cylinder and spheres
    float centre_[3]={0,0,0};
    float size_[3]={0,0,0};
    float eps_=0;
    int blocks=0;
    int cyls=0;
    int spheres=0;
    int dist=0;
    of << "\n;geometry specification\n";
    of << "(set! geometry\n";
    of << "\t(list\n";
    for (int i=0;i<trans->sim_entities.size();++i) {
      if (trans->sim_entities[i]->type()=="block") {
        ++blocks;
        centre(dynamic_cast<block*>(trans->sim_entities[i]),&centre_[0],1);
        centre(dynamic_cast<block*>(trans->sim_entities[i]),&centre_[1],2);
        centre(dynamic_cast<block*>(trans->sim_entities[i]),&centre_[2],3);
        centre_[0]=centre_[0]-((trans->dimensions[0])/2);
        centre_[1]=-1*(centre_[1]-((trans->dimensions[1])/2));
        centre_[2]=centre_[2]-((trans->dimensions[2])/2);
        size(dynamic_cast<block*>(trans->sim_entities[i]),&size_[0],1);
        size(dynamic_cast<block*>(trans->sim_entities[i]),&size_[1],2);
        size(dynamic_cast<block*>(trans->sim_entities[i]),&size_[2],3);
        get_eps(dynamic_cast<geom_entity*> (trans->sim_entities[i]), &eps_);
        of << "\t\t(make block\n";
        of << "\t\t\t(center " << centre_[0] << " " << centre_[1] << " " << centre_[2] << ")" << std::endl;
        of << "\t\t\t(size " << size_[0] << " " << size_[1] << " " << size_[2] << ")" << std::endl;
        of << "\t\t\t(material (make dielectric (epsilon " << eps_ << "))))" << std::endl;
      }
      else if (trans->sim_entities[i]->type()=="cylinder") {
        ++cyls;
        centre(dynamic_cast<cylinder*>(trans->sim_entities[i]),centre_);
        centre_[0]=centre_[0]-(trans->dimensions[0]/2);
        centre_[1]=-1*(centre_[1]-((trans->dimensions[1])/2));
        centre_[2]=centre_[2]-(trans->dimensions[2]/2);
        size(dynamic_cast<cylinder*>(trans->sim_entities[i]),size_);
        get_eps(dynamic_cast<geom_entity*> (trans->sim_entities[i]), &eps_);
        of << "\t\t(make cylinder\n";
        of << "\t\t\t(center " << centre_[0] << " " << centre_[1] << " " << centre_[2] << ")" << std::endl;
        of << "\t\t\t(radius " << size_[1] << ")" << std::endl;
        of << "\t\t\t(height " << size_[2] << ")" << std::endl;
        of << "\t\t\t(material (make dielectric (epsilon " << eps_ << "))))" << std::endl;
      }
      else if (trans->sim_entities[i]->type()=="sphere") {
        ++spheres;
        centre(dynamic_cast<sphere*>(trans->sim_entities[i]),centre_);
        centre_[0]=centre_[0]-(trans->dimensions[0]/2);
        centre_[1]=-1*(centre_[1]-((trans->dimensions[1])/2));
        centre_[2]=centre_[2]-(trans->dimensions[2]/2);
        size(dynamic_cast<sphere*>(trans->sim_entities[i]),size_);
        get_eps(dynamic_cast<sphere*> (trans->sim_entities[i]), &eps_);
        of << "\t\t(make sphere\n";
        of << "\t\t\t(center " << centre_[0] << " " << centre_[1] << " " << centre_[2] << ")" << std::endl;
        of << "\t\t\t(radius " << size_[0] << ")" << std::endl;
        of << "\t\t\t(material (make dielectric (epsilon " << eps_ << "))))" << std::endl;
      }
      else {
        //std::cerr << "WARNING: component " << trans->sim_entities[i]->type() << "is not currently supported by bris2meep\n";
      }
    }
    of << "\t)\n)\n";

    if (verbose) {
      if (blocks>0) { std::cout << blocks << " blocks\n"; }
      if (cyls>0) { std::cout << blocks << " cylinders\n"; }
      if (spheres>0) { std::cout << blocks << " spheres\n"; }
    }
  }

  void print_sources(std::ofstream &of, sim_translation* trans,bool verbose) {
    // To add:
    //		- multiple components translated to multiple sources
    float centre_[3]={0,0,0};
    float size_[3]={0,0,0};
    int func_=0;
    float ex_props_[4]={0,0,0,0};
    float freq,tc,offset=0,amp=1;
    enum sourcetype {gaussian,continuous};
    sourcetype sourcet_;
    std::string comp_;
    int sources=0;
    of << "\n;;excitations specification\n";
    of << "(set! sources\n";
    of << "\t(list\n";
    for (int i=0;i<trans->sim_entities.size();++i) {
      if (trans->sim_entities[i]->type()=="excitation") {
        ++sources;
        centre(dynamic_cast<excitation*>(trans->sim_entities[i]),&centre_[0],1);
        centre(dynamic_cast<excitation*>(trans->sim_entities[i]),&centre_[1],2);
        centre(dynamic_cast<excitation*>(trans->sim_entities[i]),&centre_[2],3);
        centre_[0]=centre_[0]-(trans->dimensions[0]/2);
        centre_[1]=-1*(centre_[1]-(trans->dimensions[1]/2));
        centre_[2]=centre_[2]-(trans->dimensions[2]/2);
        size(dynamic_cast<excitation*>(trans->sim_entities[i]),&size_[0],1);
        size(dynamic_cast<excitation*>(trans->sim_entities[i]),&size_[1],2);
        size(dynamic_cast<excitation*>(trans->sim_entities[i]),&size_[2],3);
        func_type(dynamic_cast<excitation*>(trans->sim_entities[i]), &func_);
        ex_props(dynamic_cast<excitation*>(trans->sim_entities[i]),ex_props_);
        component(dynamic_cast<excitation*>(trans->sim_entities[i]),comp_);
        /* Calculate frequency and time information in Meep */
        freq=ex_props_[0]/CSPEED;
        tc=ex_props_[1]*CSPEED;
        amp=ex_props_[2];
        offset=ex_props_[3]*CSPEED;

        switch (func_) {
          case 10:
            sourcet_=gaussian;
            break;
          case 4:
            sourcet_=continuous;
            break;
          default:
            std::cerr << "Source type " << func_ << " not implemented in MEEP yet" << std::endl;
        }

        of << "\t\t(make source\n";
        of << "\t\t\t(src (make ";
        if (sourcet_==gaussian) {
          of << "gaussian-src (frequency " << freq << ") (width " << tc << ")\n";
          of << "\t\t\t\t(start-time " << offset << ")))\n";
        }
        else if (sourcet_==continuous) {
          of << "continuous-src (frequency " << freq << ")\n";
          of << "\t\t\t\t(start-time " << offset << ")))\n";
        }
        of << "\t\t\t(component " << comp_ << ")\n";
        of << "\t\t\t(center " << centre_[0] << " " << centre_[1] << " " << centre_[2] << ")" << std::endl;
        of << "\t\t\t(size " << size_[0] << " " << size_[1] << " " << size_[2] << "))" << std::endl;
      }
    }
    of << "\t)\n)\n";

    if (verbose) { std::cout << sources << " excitations\n"; }
  }

  void print_boundaries(std::ofstream &of, sim_translation* trans,bool verbose) {

    cout << "===> print_boundaries called" << endl;

    int abc=0,mag=0,elec=0;
    boundary_param bpars_[6];
    int boundary_types[6];
    float abc_pars[3]={8,2,0.001};

    of << "\n;boundaries specification\n";

    for (int i=0;i<trans->sim_entities.size();++i) {
      if (trans->sim_entities[i]->type()=="boundary") {
          cout << "CASTING BOUNDARIES" << endl;
        boundaries(dynamic_cast<boundary*> (trans->sim_entities[i]), bpars_);
        //for (int idx=0;idx<6;idx++) cout << "bpars_["<<idx<<"] = " << bpars_[idx] << endl;
      }
    }

    // Assign boundaries: 0 Mag, 1 Elec, 2 Absorbing (PML)
    for (int i=0;i<6;++i) {
      if (bpars_[i].type==10) {
        boundary_types[i]=2;
        if (abc==0) {
            cout << "WARNING: modifying abc_pars" << endl;
                    for (int idx=0;idx<3;idx++) cout << "before: abc_pars["<<idx<<"] = " << abc_pars[idx] << endl;
          abc_pars[0]=bpars_[0].p[0];
          abc_pars[1]=bpars_[1].p[1];
          abc_pars[2]=bpars_[2].p[2];
                    for (int idx=0;idx<3;idx++) cout << "after: abc_pars["<<idx<<"] = " << abc_pars[idx] << endl;
        }
        ++abc;
      }
      else if (bpars_[i].type>1) {
        boundary_types[i]=2;
        ++abc;
      }
      else if (bpars_[i].type==0) {
        boundary_types[i]=0;
        ++mag;
      }
      else if (bpars_[i].type==1) {
        boundary_types[i]=1;
        ++elec;
      }
    }

    if (abc==6) {
      of << "(set! pml-layers (list (make pml (thickness " << abc_pars[0]*(1/trans->resolution) << "))))\n";
    }
    else {
      if (abc!=0) {
        of << "(set! pml-layers\n";
        of << "\t(list\n";
        for (int i=0;i<6;++i) {
          if (boundary_types[i]==2) {
            of << "\t\t(make pml (direction ";
            if ((i==0) || (i==3)) { of << "X"; }
            if ((i==1) || (i==4)) { of << "Y"; }
            if ((i==2) || (i==5)) { of << "Z"; }
            of << ") (side ";
            if (i<3) { of << "Low) (thickness "; }
            if (i>2) { of << "High) (thickness "; }

            for (int idx=0;idx<3;idx++) cout << "abc_pars["<<idx<<"] = " << abc_pars[idx] << endl;
            cout << "trans->resolution = " << trans->resolution <<endl;
            cout << "abc_pars[0]*(1/trans->resolution) = " << abc_pars[0]*(1/trans->resolution) << endl;

            of << abc_pars[0]*(1/trans->resolution) << "))\n";

          }
        }
        of << "\t))\n";
      }

      if ((elec>0) || (mag>0)) {
        of << "(init-fields)\n";
        if (bpars_[0].type==0) { of << "(meep-fields-set-boundary fields Low X Magnetic)\n"; }
        else if (bpars_[0].type==1) { of << "(meep-fields-set-boundary fields Low X Metallic)\n"; }
        if (bpars_[1].type==0) { of << "(meep-fields-set-boundary fields Low Y Magnetic)\n"; }
        else if (bpars_[1].type==1) { of << "(meep-fields-set-boundary fields Low Y Metallic)\n"; }
        if (bpars_[2].type==0) { of << "(meep-fields-set-boundary fields Low Z Magnetic)\n"; }
        else if (bpars_[2].type==1) { of << "(meep-fields-set-boundary fields Low Z Metallic)\n"; }
        if (bpars_[3].type==0) { of << "(meep-fields-set-boundary fields High X Magnetic)\n"; }
        else if (bpars_[3].type==1) { of << "(meep-fields-set-boundary fields High X Metallic)\n"; }
        if (bpars_[4].type==0) { of << "(meep-fields-set-boundary fields High Y Magnetic)\n"; }
        else if (bpars_[4].type==1) { of << "(meep-fields-set-boundary fields High Y Metallic)\n"; }
        if (bpars_[5].type==0) { of << "(meep-fields-set-boundary fields High Z Magnetic)\n"; }
        else if (bpars_[5].type==1) { of << "(meep-fields-set-boundary fields High Z Metallic)\n"; }
      }
    }

    cout << "===> print_boundaries done" << endl;

  }

  void print_run_info(std::ofstream &of, sim_translation* trans,bool verbose) {
    std::string ident;
    int niter;

    of << "\n;simulation run specification\n";
    of << "(run-until ";

    // Calculate run time based on number of iterations x time step
    for (int i=0;i<trans->sim_entities.size();++i) {
      if (trans->sim_entities[i]->type()=="flag") {
        dynamic_cast<flag*>(trans->sim_entities[i])->get_flags(ident,&niter);
      }
    }
    of << ceil(niter*(1/(2*trans->resolution))) << "\n";

    bool fields[6]={0,0,0,0,0,0};
    float loc[3]={0,0,0};
    float size[3]={0,0,0};
    int step=1;
    int pnum=0;
    int snum=0;

    // Print probe and snapshot info
    for (int i=0;i<trans->sim_entities.size();++i) {
      if (trans->sim_entities[i]->type()=="probe") {
        ++pnum;
        dynamic_cast<probe*>(trans->sim_entities[i])->get_probe_info(loc,&step,fields);
        loc[0]=loc[0]-(trans->dimensions[0]/2);
        loc[1]=-1*(loc[1]-(trans->dimensions[1]/2));
        loc[2]=loc[2]-(trans->dimensions[2]/2);

        of << "\t(to-appended \"p" << pnum/10 << pnum%10 << ident << "\" (at-every ";
        of << step*(1/(2*trans->resolution)) << " (in-volume (volume (center ";
        of << loc[0] << " " << loc[1] << " " << loc[2] << ") (size 0 0 0))\n\t\t";
        if (fields[0]) { of << " output-efield-x"; }
        if (fields[1]) { of << " output-efield-y"; }
        if (fields[2]) { of << " output-efield-z"; }
        if (fields[3]) { of << " output-hfield-x"; }
        if (fields[4]) { of << " output-hfield-y"; }
        if (fields[5]) { of << " output-hfield-z"; }
        of << ")))\n";
      }
      if (trans->sim_entities[i]->type()=="snapshot") {
        ++snum;
        int first;
        char plane;
        dynamic_cast<snapshot*>(trans->sim_entities[i])->get_snap_info(loc,size,&step,&first,&plane,fields);
        loc[0]=loc[0]-(trans->dimensions[0]/2);
        loc[1]=-1*(loc[1]-(trans->dimensions[1]/2));
        loc[2]=loc[2]-(trans->dimensions[2]/2);

        of << "\t(after-time " << first*(1/(2*trans->resolution));
        of << " (to-appended \"" << plane << snum << ident << "\" (at-every ";
        of << step*(1/(2*trans->resolution)) << " (in-volume (volume (center ";
        of << loc[0] << " " << loc[1] << " " << loc[2] << ") (size ";
        of << size[0] << " " << size[1] << " " << size[2] <<"))\n\t\t";
        if (fields[0]) { of << " output-efield-x"; }
        if (fields[1]) { of << " output-efield-y"; }
        if (fields[2]) { of << " output-efield-z"; }
        if (fields[3]) { of << " output-hfield-x"; }
        if (fields[4]) { of << " output-hfield-y"; }
        if (fields[5]) { of << " output-hfield-z"; }
        of << "))))\n";
      }
    }

    of << ")\n";

    if (verbose) {
      if (pnum>0) { std::cout << pnum << " probes\n"; }
      if (snum>0) { std::cout << snum << " snapshots\n"; }
    }
  }
}

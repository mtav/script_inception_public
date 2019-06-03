#include <unistd.h>
#include "fdtdutils.hpp"

using namespace std;

void usage() {
  cout << "Usage: bris2meep [options] <bristol-input1> <bristol-input2> ... <meep-output>\n"
  "Options:\n"
  "         -h : this help message\n"
  "         -V : print version number\n"
  "         -v : verbose output\n";
}

int main(int argc, char *argv[])
{
  extern char *optarg;
  extern int optind;
  int c;
  bool verbose=false;
  string out;
  vector<string> in;
  
  while ((c = getopt(argc, argv, "hvV")) != -1) {
    switch (c) {
      case 'h':
        usage();
        return 0;
      case 'v':
        verbose=true;
        break;
      case 'V':
        cout << "bris2meep " << VERSION << " by Ian Buss\n";
        return 0;
      default:
        cout << "Invalid argument -" << c << "\n";
        usage();
        return 1;
    }
  }
  if (argc<optind+2) {  /* should be 2 or more parameters left */
    usage();
    return 1;
  }
  for (int i=optind;i<=argc-2;++i) {
    in.push_back(argv[i]);
  }
  
  out=argv[argc-1];
  
  fdtdutils::sim_translation sim(in[0]);
  for (int i=1;i<in.size();++i) {
    sim.read_in_file(in[i]);
  }
  
  sim.process_objects(verbose);
  sim.translate(out,verbose);
  
  return 0;
}

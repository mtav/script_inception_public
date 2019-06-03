% Class containing data necessary for FDTD simulations
function sim = FDTDobject

  sim = struct();

  % geometry objects
  sim.sphere_list =  [];
  sim.block_list =  [];
  sim.cylinder_list =  [];
  sim.rotation_list =  [];
  sim.geometry_object_list = [];

  % mesh
  sim.xmesh = [];
  sim.ymesh = [];
  sim.zmesh = [];

  % input
  sim.excitations =  [];
  sim.flag = struct('iMethod',{0},'propCons',{0},'flagOne',{0},'flagTwo',{0},'numSteps',{0},'stabFactor',{0},'id',{'_id_'});
  sim.boundaries = struct('type',{0,0,0,0,0,0},'position',{[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]});
  sim.box = struct('lower',{[0,0,0]},'upper',{[1,1,1]});

  % output
  sim.all_snapshots = [];
  sim.time_snapshots =  [];
  sim.epsilon_snapshots =  [];
  sim.frequency_snapshots =  [];
  
  sim.time_snapshots_X =  [];
  sim.time_snapshots_Y =  [];
  sim.time_snapshots_Z =  [];

  sim.epsilon_snapshots_X =  [];
  sim.epsilon_snapshots_Y =  [];
  sim.epsilon_snapshots_Z =  [];
  
  sim.frequency_snapshots_X =  [];
  sim.frequency_snapshots_Y =  [];
  sim.frequency_snapshots_Z =  [];
  
  sim.probe_list =  [];

  sim = class(sim, 'FDTDobject');

end

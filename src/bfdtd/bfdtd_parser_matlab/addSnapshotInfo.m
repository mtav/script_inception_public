function snapshot = addSnapshotInfo(snapshot)
  snapshot.centro = 0.5*(snapshot.P1 + snapshot.P2);
  snapshot.plane_bfdtd_index = snapshot.plane;
  plane_letter_list = {'x','y','z'};
  snapshot.plane_letter = plane_letter_list{snapshot.plane_bfdtd_index};
  snapshot.plane_position = snapshot.centro(snapshot.plane_bfdtd_index);
end

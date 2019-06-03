#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
import tempfile
import bfdtd

class test_Snapshots(unittest.TestCase):

  def setUp(self):
    import warnings
    warnings.simplefilter("error")
    
  def tearDown(self):
    return

  def test_All(self):
    with tempfile.TemporaryDirectory(prefix='snapshot_class_test-') as outdir:
      sim = bfdtd.BFDTDobject()

      #sim.appendSnapshot(Snapshot)
      sim.appendSnapshot(bfdtd.FrequencySnapshot())
      sim.appendSnapshot(bfdtd.TimeSnapshot())
      sim.appendSnapshot(bfdtd.EpsilonSnapshot())
      sim.appendSnapshot(bfdtd.ModeFilteredProbe())

      #sim.appendSnapshot(SnapshotBox())
      sim.appendSnapshot(bfdtd.SnapshotBoxXYZ())
      sim.appendSnapshot(bfdtd.SnapshotBoxSurface())
      sim.appendSnapshot(bfdtd.SnapshotBoxVolume())

      sim.appendSnapshot(bfdtd.EnergySnapshot())
      sim.appendSnapshot(bfdtd.EpsilonBox())
      sim.appendSnapshot(bfdtd.EpsilonBoxFull())
      sim.appendSnapshot(bfdtd.ModeVolumeBox())

      #sim.writeAll('/tmp/snapshot_class_test')
      sim.writeAll(outdir)
    return
  
  def test_SnapshotBoxXYZ(self):
    with tempfile.TemporaryDirectory(prefix='testSnapshotBoxVolume-') as outdir:
      #outdir = '/tmp/testSnapshotBoxVolume'

      sim = bfdtd.BFDTDobject()
      sim.setSizeAndResolution([10, 11, 12], [41, 42, 43])
      
      b = bfdtd.Block()
      b.setSize([1, 2, 3])
      b.setLocation([4, 5, 6])
      sim.appendGeometryObject(b)

      tsnap = bfdtd.TimeSnapshot()
      tsnap.setExtension(*b.getExtension())
      esnap = bfdtd.EpsilonSnapshot()
      esnap.setExtension(*b.getExtension())
      mfp = bfdtd.ModeFilteredProbe()
      mfp.setExtension(*b.getExtension())
      fsnap = bfdtd.FrequencySnapshot()
      fsnap.setExtension(*b.getExtension())
      
      MV = bfdtd.SnapshotBoxXYZ()
      MV.setIntersectionPoint([3.75,5.5,7])
      
      sim.appendSnapshot(MV)

      sim.writeGeoFile(os.path.join(outdir, 'testSnapshotBoxVolume.geo'))
      
      MV.setBaseSnapshot(tsnap)
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_tsnap_xyz.inp'))

      MV.setBaseSnapshot(esnap)
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_esnap_xyz.inp'))

      MV.setBaseSnapshot(mfp)
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_mfp_xyz.inp'))

      MV.setBaseSnapshot(fsnap)
      fsnap.setFullExtensionOff()
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_fsnap_xyz.inp'))
    
    return

  def test_SnapshotBoxSurface(self):
    with tempfile.TemporaryDirectory(prefix='testSnapshotBoxVolume-') as outdir:
      #outdir = '/tmp/testSnapshotBoxVolume'

      sim = bfdtd.BFDTDobject()
      sim.setSizeAndResolution([10, 11, 12], [41, 42, 43])
      
      b = bfdtd.Block()
      b.setSize([1, 2, 3])
      b.setLocation([4, 5, 6])
      sim.appendGeometryObject(b)

      tsnap = bfdtd.TimeSnapshot()
      tsnap.setExtension(*b.getExtension())
      esnap = bfdtd.EpsilonSnapshot()
      esnap.setExtension(*b.getExtension())
      mfp = bfdtd.ModeFilteredProbe()
      mfp.setExtension(*b.getExtension())
      fsnap = bfdtd.FrequencySnapshot()
      fsnap.setExtension(*b.getExtension())
      
      MV = bfdtd.SnapshotBoxSurface()
      sim.appendSnapshot(MV)

      sim.writeGeoFile(os.path.join(outdir, 'testSnapshotBoxVolume.geo'))
      
      MV.setBaseSnapshot(tsnap)
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_tsnap_box.inp'))

      MV.setBaseSnapshot(esnap)
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_esnap_box.inp'))

      MV.setBaseSnapshot(mfp)
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_mfp_box.inp'))

      MV.setBaseSnapshot(fsnap)
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_fsnap_box.inp'))
    
    return

  def test_SnapshotBoxVolume(self):
    with tempfile.TemporaryDirectory(prefix='testSnapshotBoxVolume-') as outdir:
    
      #outdir = '/tmp/testSnapshotBoxVolume'

      sim = bfdtd.BFDTDobject()
      sim.setSizeAndResolution([10, 11, 12], [41, 42, 43])
      
      b = bfdtd.Block()
      b.setSize([1, 2, 3])
      b.setLocation([4, 5, 6])
      sim.appendGeometryObject(b)

      tsnap = bfdtd.TimeSnapshot()
      tsnap.setExtension(*b.getExtension())
      esnap = bfdtd.EpsilonSnapshot()
      esnap.setExtension(*b.getExtension())
      mfp = bfdtd.ModeFilteredProbe()
      mfp.setExtension(*b.getExtension())
      fsnap = bfdtd.FrequencySnapshot()
      fsnap.setExtension(*b.getExtension())
      
      MV = bfdtd.SnapshotBoxVolume()
      sim.appendSnapshot(MV)
      
      #code.interact(local=locals())

      sim.writeGeoFile(os.path.join(outdir, 'testSnapshotBoxVolume.geo'))
      
      
      tsnap.setPlaneLetter('x')
      MV.setBaseSnapshot(tsnap)
      sim.setFileBaseName('tsnap_x')
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_tsnap_x.inp'))

      tsnap.setPlaneLetter('y')
      MV.setBaseSnapshot(tsnap)
      sim.setFileBaseName('tsnap_y')
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_tsnap_y.inp'))

      tsnap.setPlaneLetter('z')
      MV.setBaseSnapshot(tsnap)
      sim.setFileBaseName('tsnap_z')
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_tsnap_z.inp'))


      esnap.setPlaneLetter('x')
      MV.setBaseSnapshot(esnap)
      sim.setFileBaseName('esnap_x')
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_esnap_x.inp'))

      esnap.setPlaneLetter('y')
      MV.setBaseSnapshot(esnap)
      sim.setFileBaseName('esnap_y')
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_esnap_y.inp'))

      esnap.setPlaneLetter('z')
      MV.setBaseSnapshot(esnap)
      sim.setFileBaseName('esnap_z')
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_esnap_z.inp'))


      mfp.setPlaneLetter('x')
      MV.setBaseSnapshot(mfp)
      sim.setFileBaseName('mfp_x')
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_mfp_x.inp'))

      mfp.setPlaneLetter('y')
      MV.setBaseSnapshot(mfp)
      sim.setFileBaseName('mfp_y')
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_mfp_y.inp'))

      mfp.setPlaneLetter('z')
      MV.setBaseSnapshot(mfp)
      sim.setFileBaseName('mfp_z')
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_mfp_z.inp'))


      fsnap.setPlaneLetter('x')
      MV.setBaseSnapshot(fsnap)
      sim.setFileBaseName('fsnap_x')
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_fsnap_x.inp'))

      fsnap.setPlaneLetter('y')
      MV.setBaseSnapshot(fsnap)
      sim.setFileBaseName('fsnap_y')
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_fsnap_y.inp'))

      fsnap.setPlaneLetter('z')
      MV.setBaseSnapshot(fsnap)
      sim.setFileBaseName('fsnap_z')
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_fsnap_z.inp'))
    
    return

  def test_EnergySnapshot(self):
    with tempfile.TemporaryDirectory(prefix='testSnapshotBoxVolume-') as outdir:
      #outdir = '/tmp/testSnapshotBoxVolume'

      sim = bfdtd.BFDTDobject()
      sim.setSizeAndResolution([10, 11, 12], [41, 42, 43])

      E = bfdtd.EnergySnapshot()
      E.setPlaneOrientationY()
      E.setExtensionX(5,6)
      E.setExtensionY(4,4)
      E.setExtensionZ(7,9)
      E.setFrequencies([11,22,33])
      
      E.setFullExtensionOff()
      
      sim.appendSnapshot(E)
      
      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_energy.inp'))

    return

  def test_ModeVolumeBox(self):
    with tempfile.TemporaryDirectory(prefix='testSnapshotBoxVolume-') as outdir:
      #outdir = '/tmp/testSnapshotBoxVolume'

      sim = bfdtd.BFDTDobject()
      sim.setSizeAndResolution([10, 11, 12], [41, 42, 43])
      
      b = bfdtd.Block()
      b.setSize([1, 2, 3])
      b.setLocation([4, 5, 6])
      sim.appendGeometryObject(b)
      
      MV = bfdtd.ModeVolumeBox()
      
      MV.setFullExtensionOff()
      
      MV.setPlaneOrientationZ()
      MV.setExtension(*b.getExtension())
      
      MV.epsilon_repetition = 456

      MV.name = 'myname'
      MV.layer = 'mylayer'
      MV.group = 'mygroup'

      MV.first = 11
      MV.repetition = 1337
      MV.starting_sample = 789

      MV.frequency_vector = [22,33]

      MV.interpolate = 45
      MV.mod_only = 46
      MV.mod_all = 47
      MV.real_dft = 123

      MV.useForMeshing = False

      MV.E = [1, 2, 3]
      MV.H = [4, 5, 6]
      MV.J = [7, 8, 9]
      
      sim.appendSnapshot(MV)

      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_MV.inp'))

    return

  def test_EpsilonBox(self):
    with tempfile.TemporaryDirectory(prefix='testSnapshotBoxVolume-') as outdir:

      #outdir = '/tmp/testSnapshotBoxVolume'

      sim = bfdtd.BFDTDobject()
      sim.setSizeAndResolution([10, 11, 12], [41, 42, 43])
      
      b = bfdtd.Block()
      b.setSize([1, 2, 3])
      b.setLocation([4, 5, 6])
      sim.appendGeometryObject(b)
      
      mybox = bfdtd.EpsilonBox()
      mybox.setPlaneOrientationY()
      mybox.setExtension(*b.getExtension())
      mybox.setFullExtensionOff()
        
      sim.appendSnapshot(mybox)

      sim.writeInpFile(os.path.join(outdir, 'testSnapshotBoxVolume_epsbox.inp'))

    return

if __name__ == '__main__':
  unittest.main()

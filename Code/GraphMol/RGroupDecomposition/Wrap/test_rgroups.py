#  Copyright (c) 2018-2021, Novartis Institutes for BioMedical Research Inc.
#   and other RDKit contributors
#  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#     * Neither the name of Novartis Institutes for BioMedical Research Inc.
#       nor the names of its contributors may be used to endorse or promote
#       products derived from this software without specific prior written
#       permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import unittest
from collections import OrderedDict
import json
import itertools

# the RGD code can generate a lot of warnings. disable them
from rdkit import Chem, RDLogger, rdBase
from rdkit.Chem.rdRGroupDecomposition import (RGroupCoreAlignment,
                                              RGroupDecompose,
                                              RGroupDecomposition,
                                              RGroupDecompositionParameters,
                                              RGroupLabels,
                                              RGroupLabelling,
                                              RelabelMappedDummies)

RDLogger.DisableLog("rdApp.warning")


class TestCase(unittest.TestCase):

  def test_multicores(self):
    cores_smi_easy = OrderedDict()
    cores_smi_hard = OrderedDict()

    # cores_smi_easy['cephem'] = Chem.MolFromSmiles('O=C1C([1*])[C@@H]2N1C(C(O)=O)=C([3*])CS2')
    cores_smi_easy['cephem'] = Chem.MolFromSmarts('O=C1C([*:1])C2N1C(C(O)=O)=C([*:3])CS2')
    cores_smi_hard['cephem'] = Chem.MolFromSmarts('O=C1C([2*])([1*])[C@@H]2N1C(C(O)=O)=C([3*])CS2')

    # cores_smi_easy['carbacephem'] = Chem.MolFromSmiles('O=C1C([1*])[C@@H]2N1C(C(O)=O)=C([3*])CC2')
    cores_smi_easy['carbacephem'] = Chem.MolFromSmarts('O=C1C([1*])C2N1C(C(O)=O)=C([3*])CC2')
    cores_smi_hard['carbacephem'] = Chem.MolFromSmarts(
      'O=C1C([2*])([1*])[C@@H]2N1C(C(O)=O)=C([3*])CC2')

    # cores_smi_easy['oxacephem'] = Chem.MolFromSmiles('O=C1C([1*])[C@@H]2N1C(C(O)=O)=C([3*])CO2')
    cores_smi_easy['oxacephem'] = Chem.MolFromSmarts('O=C1C([1*])C2N1C(C(O)=O)=C([3*])CO2')
    cores_smi_hard['oxacephem'] = Chem.MolFromSmarts(
      'O=C1C([2*])([1*])[C@@H]2N1C(C(O)=O)=C([3*])CO2')

    # cores_smi_easy['carbapenem'] = Chem.MolFromSmiles('O=C1C([1*])[C@@H]2N1C(C(O)=O)=C([3*])C2')
    cores_smi_easy['carbapenem'] = Chem.MolFromSmarts('O=C1C([1*])C2N1C(C(O)=O)=C([3*])C2')
    cores_smi_hard['carbapenem'] = Chem.MolFromSmarts(
      'O=C1C([2*])([1*])[C@@H]2N1C(C(O)=O)=C([3*])C2')

    # cores_smi_easy['carbapenam'] = Chem.MolFromSmiles('O=C1C([1*])[C@@H]2N1C(C(O)=O)C([3*])([4*])C2')
    cores_smi_easy['carbapenam'] = Chem.MolFromSmarts('O=C1C([1*])C2N1C(C(O)=O)C([3*])([4*])C2')
    cores_smi_hard['carbapenam'] = Chem.MolFromSmarts(
      'O=C1C([2*])([1*])[C@@H]2N1C(C(O)=O)C([3*])([4*])C2')

    # cores_smi_easy['penem'] = Chem.MolFromSmiles('O=C1C([1*])[C@@H]2N1C(C(O)=O)=C([3*])S2')
    cores_smi_easy['penem'] = Chem.MolFromSmarts('O=C1C([1*])C2N1C(C(O)=O)=C([3*])S2')
    cores_smi_hard['penem'] = Chem.MolFromSmarts('O=C1C([2*])([1*])[C@@H]2N1C(C(O)=O)=C([3*])S2')

    # cores_smi_easy['penam'] = Chem.MolFromSmiles('O=C1C([1*])[C@@H]2N1C(C(O)=O)C([3*])([4*])S2')
    cores_smi_easy['penam'] = Chem.MolFromSmarts('O=C1C([*:1])C2N1C(C(O)=O)C([*:3])([*:4])S2')
    cores_smi_hard['penam'] = Chem.MolFromSmarts(
      'O=C1C([*:2])([*:1])[C@@H]2N1C(C(O)=O)C([*:3])([*:4])S2')

    # cores_smi_easy['oxapenam'] = Chem.MolFromSmiles('O=C1C([1*])[C@@H]2N1C(C(O)=O)C([3*])([4*])O2')
    cores_smi_easy['oxapenam'] = Chem.MolFromSmarts('O=C1C([1*])C2N1C(C(O)=O)C([3*])([4*])O2')
    cores_smi_hard['oxapenam'] = Chem.MolFromSmarts(
      'O=C1C([2*])([1*])[C@@H]2N1C(C(O)=O)C([3*])([4*])O2')

    cores_smi_easy['monobactam'] = Chem.MolFromSmarts('O=C1C([1*])C([5*])N1')
    cores_smi_hard['monobactam'] = Chem.MolFromSmarts('O=C1C([2*])([1*])C([6*])([5*])N1')
    rg_easy = RGroupDecomposition(cores_smi_easy.values())
    rg_stereo = RGroupDecomposition(cores_smi_hard.values())

  def test_stereo(self):
    smiles = """C1CCO[C@@H](N)1
C1CCO[C@H](N)1
C1CCO[C@@](N)(O)1
C1CCO[C@@](N)(P)1
C1CCO[C@@](N)(S)1
C1CCO[C@@H](O)1
C1CCO[C@H](O)1
C1CCO[C@@](O)(N)1
C1CCO[C@@](O)(P)1
C1CCO[C@@](O)(S)1
C1CCO[C@@H](P)1
C1CCO[C@H](P)1
C1CCO[C@@](P)(N)1
C1CCO[C@@](P)(O)1
C1CCO[C@@](P)(S)1
C1CCO[C@@H](S)1
C1CCO[C@H](S)1
C1CCO[C@@](S)(N)1
C1CCO[C@@](S)(O)1
C1CCO[C@@](S)(P)1
"""
    mols = []
    for smi in smiles.split():
      m = Chem.MolFromSmiles(smi)
      assert m, smi
      mols.append(m)
    core = Chem.MolFromSmarts("C1CCOC1")
    rgroups = RGroupDecomposition(core)
    for m in mols:
      rgroups.Add(m)
    rgroups.Process()
    columns = rgroups.GetRGroupsAsColumns()
    data = {}
    for k, v in columns.items():
      data[k] = [Chem.MolToSmiles(m, True) for m in v]

    rgroups2, unmatched = RGroupDecompose([core], mols)
    columns2, unmatched = RGroupDecompose([core], mols, asRows=False)
    data2 = {}
    for k, v in columns2.items():
      data2[k] = [Chem.MolToSmiles(m, True) for m in v]

    self.assertEqual(data, data2)
    columns3, unmatched = RGroupDecompose([core], mols, asRows=False, asSmiles=True)
    self.assertEqual(data, columns3)

  def test_h_options(self):
    core = Chem.MolFromSmiles("O=c1oc2ccccc2cc1")
    smiles = ("O=c1cc(Cn2ccnc2)c2ccc(Oc3ccccc3)cc2o1", "O=c1oc2ccccc2c(Cn2ccnc2)c1-c1ccccc1",
              "COc1ccc2c(Cn3cncn3)cc(=O)oc2c1")
    params = RGroupDecompositionParameters()
    rgd = RGroupDecomposition(core, params)
    for smi in smiles:
      m = Chem.MolFromSmiles(smi)
      rgd.Add(m)
    rgd.Process()
    columns = rgd.GetRGroupsAsColumns()
    self.assertEqual(columns['R2'][0].GetNumAtoms(), 7)

    params.removeHydrogensPostMatch = False
    rgd = RGroupDecomposition(core, params)
    for smi in smiles:
      m = Chem.MolFromSmiles(smi)
      rgd.Add(m)
    rgd.Process()
    columns = rgd.GetRGroupsAsColumns()
    self.assertEqual(columns['R2'][0].GetNumAtoms(), 12)

  def test_unmatched(self):
    cores = [Chem.MolFromSmiles("N")]
    mols = [
      Chem.MolFromSmiles("CC"),
      Chem.MolFromSmiles("CC"),
      Chem.MolFromSmiles("CC"),
      Chem.MolFromSmiles("N"),
      Chem.MolFromSmiles("CC")
    ]

    res, unmatched = RGroupDecompose(cores, mols)
    self.assertEqual(len(res), 1)
    self.assertEqual(unmatched, [0, 1, 2, 4])

  def test_userlabels(self):
    smis = ["C(Cl)N(N)O(O)"]
    mols = [Chem.MolFromSmiles(smi) for smi in smis]
    smarts = 'C([*:1])N([*:5])O([*:6])'
    core = Chem.MolFromSmarts(smarts)
    rg = RGroupDecomposition(core)
    for m in mols:
      rg.Add(m)
    rg.Process()
    self.assertEqual(rg.GetRGroupsAsColumns(asSmiles=True), {
      'Core': ['C(N(O[*:6])[*:5])[*:1]'],
      'R1': ['Cl[*:1]'],
      'R5': ['N[*:5]'],
      'R6': ['O[*:6]']
    })

    smarts = 'C([*:4])N([*:5])O([*:6])'

    core = Chem.MolFromSmarts(smarts)
    rg = RGroupDecomposition(core)
    for m in mols:
      rg.Add(m)
    rg.Process()
    self.assertEqual(rg.GetRGroupsAsColumns(asSmiles=True), {
      'Core': ['C(N(O[*:6])[*:5])[*:4]'],
      'R4': ['Cl[*:4]'],
      'R5': ['N[*:5]'],
      'R6': ['O[*:6]']
    })

  def test_match_only_at_rgroups(self):
    smiles = ['c1ccccc1']  # , 'c1(Cl)ccccc1', 'c1(Cl)cc(Br)ccc1']
    mols = [Chem.MolFromSmiles(smi) for smi in smiles]

    core1 = Chem.MolFromSmiles("c1([*:5])cc([*:6])ccc1")
    params = RGroupDecompositionParameters()
    params.onlyMatchAtRGroups = True
    rg = RGroupDecomposition(core1, params)
    for smi, m in zip(smiles, mols):
      self.assertTrue(rg.Add(m) != -1, smi)

  def test_incorrect_multiple_rlabels(self):
    mols = [Chem.MolFromSmiles(smi) for smi in (
      "C1NC(Cl)CC1",
      "C1OC(Cl)CC1",
      "C1(Cl)OCCC1",
    )]

    scaffolds = [Chem.MolFromSmarts(x) for x in ("C1NCCC1", )]
    groups, unmatched = RGroupDecompose(scaffolds, mols, asSmiles=True, asRows=False)

    self.assertEqual(groups, {'Core': ['C1CNC([*:1])C1'], 'R1': ['Cl[*:1]']})

    scaffolds = [Chem.MolFromSmarts(x) for x in ("C1OCCC1", )]
    groups, unmatched = RGroupDecompose(scaffolds, mols, asSmiles=True, asRows=False)
    self.assertEqual(groups, {
      'Core': ['C1COC([*:1])C1', 'C1COC([*:1])C1'],
      'R1': ['Cl[*:1]', 'Cl[*:1]']
    })
    scaffolds = [Chem.MolFromSmarts(x) for x in ("C1NCCC1", "C1OCCC1")]
    groups, unmatched = RGroupDecompose(scaffolds, mols, asSmiles=True, asRows=False)
    self.assertEqual(
      groups, {
        'Core': ['C1CNC([*:1])C1', 'C1COC([*:1])C1', 'C1COC([*:1])C1'],
        'R1': ['Cl[*:1]', 'Cl[*:1]', 'Cl[*:1]']
      })

  def test_aligned_cores(self):
    scaffolds = [Chem.MolFromSmarts(x) for x in ("C1NC1OC", "C1NC1NC")]
    mols = [Chem.MolFromSmiles(smi) for smi in ("C1NC1OCCC", "C1NC1NCCC")]
    groups, unmatched = RGroupDecompose(scaffolds, mols, asSmiles=True, asRows=True)
    # print("test_aligned_Cores")
    # print("groups:", groups)
    self.assertEqual(groups, [{
      'Core': 'C1NC1OC[*:1]',
      'R1': 'CC[*:1]'
    }, {
      'Core': 'C1NC1NC[*:2]',
      'R2': 'CC[*:2]'
    }])

  def test_aligned_cores2(self):
    scaffolds = [Chem.MolFromSmarts(x) for x in ("C1NCC1", "C1SCC1")]
    mols = [Chem.MolFromSmiles(smi) for smi in ("C1N(P)CC1", "C1S(P)CC1")]
    # print("test_aligned_Cores2")
    groups, unmatched = RGroupDecompose(scaffolds, mols, asSmiles=True, asRows=True)
    # print("groups: ", groups)
    self.assertEqual(groups, [{
      'Core': 'C1CN([*:1])C1',
      'R1': 'P[*:1]'
    }, {
      'Core': 'C1C[SH]([*:2])C1',
      'R2': 'P[*:2]'
    }])

  def test_getrgrouplabels(self):
    smis = ["C(Cl)N(N)O(O)"]
    mols = [Chem.MolFromSmiles(smi) for smi in smis]
    smarts = 'C([*:1])N([*:5])O([*:6])'
    core = Chem.MolFromSmarts(smarts)
    rg = RGroupDecomposition(core)
    for m in mols:
      rg.Add(m)
    rg.Process()
    self.assertEqual(set(rg.GetRGroupLabels()), set(rg.GetRGroupsAsColumns()))

  def test_timeout(self):
    smis = '''CN(C)Cc1cccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)c1
CNc1cccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)c1
Cc1cc2cc(Oc3cc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)ccc3C(=O)NS(=O)(=O)c3ccc(NC4CCN(C)CC4)c([N+](=O)[O-])c3)ccc2[nH]1
Cc1cc2cc(Oc3cc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)ccc3C(=O)NS(=O)(=O)c3ccc(NCCCN4CCOCC4)c([N+](=O)[O-])c3)ccc2[nH]1
O=C(NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1ccccc1Cl
O=C(NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1cccc(Cl)c1
O=C(NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1ccc(Cl)cc1
O=C(NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1cccc([N+](=O)[O-])c1
O=C(NS(=O)(=O)c1ccc(NCCCN2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1cccc(CO)c1
CN(C)CCCNc1ccc(S(=O)(=O)NC(=O)c2ccc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)cc2Oc2ccccc2Cl)cc1[N+](=O)[O-]
O=C(NS(=O)(=O)c1ccc(NCCCN2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1cccc(Cl)c1
O=C(NS(=O)(=O)c1ccc(NCCCN2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1ccc(Cl)cc1
CN(C)CCCNc1ccc(S(=O)(=O)NC(=O)c2ccc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)cc2Oc2cccc(Cl)c2)cc1[N+](=O)[O-]
CN(C)CCCNc1ccc(S(=O)(=O)NC(=O)c2ccc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)cc2Oc2ccc(Cl)cc2)cc1[N+](=O)[O-]
CN(C)CCCNc1ccc(S(=O)(=O)NC(=O)c2ccc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)cc2Oc2cccc3c2ccn3C)cc1[N+](=O)[O-]
CC(=O)Nc1cccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)c1
Nc1ccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)cc1
Nc1cccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)c1
COc1cccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)c1
CN(C)c1cccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)c1
N#Cc1cccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)c1
Cc1nc2ccc(Oc3cc(N4CCN(Cc5ccccc5-c5ccc(Cl)cc5)CC4)ccc3C(=O)NS(=O)(=O)c3ccc(NCC4CCOCC4)c([N+](=O)[O-])c3)cc2s1
Cc1nc2cc(Oc3cc(N4CCN(Cc5ccccc5-c5ccc(Cl)cc5)CC4)ccc3C(=O)NS(=O)(=O)c3ccc(NCCCN4CCOCC4)c([N+](=O)[O-])c3)ccc2s1
Cc1nc2cc(Oc3cc(N4CCN(Cc5ccccc5-c5ccc(Cl)cc5)CC4)ccc3C(=O)NS(=O)(=O)c3ccc(NCCCN(C)C)c([N+](=O)[O-])c3)ccc2s1
CN(C)C(=O)CCc1ccccc1Oc1cc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)ccc1C(=O)NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1
CN(C)C(=O)Cc1ccccc1Oc1cc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)ccc1C(=O)NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1
CN(C)CCCc1ccccc1Oc1cc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)ccc1C(=O)NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1
CN(C)CCc1ccccc1Oc1cc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)ccc1C(=O)NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1
CN(C)C(=O)c1ccccc1Oc1cc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)ccc1C(=O)NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1
CN(C)Cc1ccccc1Oc1cc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)ccc1C(=O)NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1
CN(C)CCCNc1ccc(S(=O)(=O)NC(=O)c2ccc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)cc2Oc2cccc(N3CCOCC3)c2)cc1[N+](=O)[O-]
Cc1nc(C)c(-c2cccc(Oc3cc(N4CCN(Cc5ccccc5-c5ccc(Cl)cc5)CC4)ccc3C(=O)NS(=O)(=O)c3ccc(NCCCN4CCOCC4)c([N+](=O)[O-])c3)c2)s1
CN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)cc3Oc3cc(Cl)cc(Cl)c3)cc2[N+](=O)[O-])CC1
CN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)cc3Oc3cccc(Cl)c3)cc2[N+](=O)[O-])CC1
CN(C)CCOc1ccc(-c2ccc(Cl)cc2)c(CN2CCN(c3ccc(C(=O)NS(=O)(=O)c4ccc(NC5CCN(C)CC5)c([N+](=O)[O-])c4)c(Oc4cccc(Cl)c4)c3)CC2)c1
CN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)OC5)CC4)cc3Oc3ccccc3Cl)cc2[N+](=O)[O-])CC1
CN(C)CCOc1cccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)c1
CN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)cc3Oc3ccc(N)c(Cl)c3)cc2[N+](=O)[O-])CC1
CC(C)N1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)cc3Oc3ccccc3Cl)cc2[N+](=O)[O-])CC1
CN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)cc3Oc3ccccc3Br)cc2[N+](=O)[O-])CC1
CN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CCCC5)CC4)cc3Oc3ccccc3Cl)cc2[N+](=O)[O-])CC1
Cc1n[nH]c2cccc(Oc3cc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)ccc3C(=O)NS(=O)(=O)c3ccc(NCCCN4CCOCC4)c([N+](=O)[O-])c3)c12
CN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)cc3Oc3cccc(F)c3F)cc2[N+](=O)[O-])CC1
CN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)cc3Oc3cccc(Br)c3)cc2[N+](=O)[O-])CC1
CCN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)cc3Oc3ccccc3Cl)cc2[N+](=O)[O-])CC1
CN1C(C)(C)CC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)cc3Oc3ccccc3Cl)cc2[N+](=O)[O-])CC1(C)C
CC1(C)CCC(CN2CCN(c3ccc(C(=O)NS(=O)(=O)c4ccc(NC5CCN(C6CCOCC6)CC5)c([N+](=O)[O-])c4)c(Oc4cccc(F)c4F)c3)CC2)=C(c2ccc(Cl)cc2)C1
CN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)cc3Oc3cc(F)c4[nH]ccc4c3)cc2[N+](=O)[O-])CC1
CC1(C)CCC(CN2CCN(c3ccc(C(=O)NS(=O)(=O)c4ccc(NCCCN5CCOCC5)c([N+](=O)[O-])c4)c(Oc4cccc(F)c4F)c3)CC2)=C(c2ccc(Cl)cc2)C1
CC1(C)CCC(CN2CCN(c3ccc(C(=O)NS(=O)(=O)c4ccc(NCCCN5CCOCC5)c([N+](=O)[O-])c4)c(Oc4ccc(N)c(Cl)c4)c3)CC2)=C(c2ccc(Cl)cc2)C1
O=C(NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3cc(CCN4CCCC4)ccc3-c3ccc(Cl)cc3)CC2)cc1Oc1cccc(Cl)c1
CN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)cc3Oc3cccc(Cl)c3Cl)cc2[N+](=O)[O-])CC1
Cc1n[nH]c2cccc(Oc3cc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)ccc3C(=O)NS(=O)(=O)c3ccc(NC4CCN(C)CC4)c([N+](=O)[O-])c3)c12
CN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CCCCC5)CC4)cc3Oc3ccccc3Cl)cc2[N+](=O)[O-])CC1
CN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)cc3Oc3cccc(C(F)(F)F)c3)cc2[N+](=O)[O-])CC1
CN(C)CCCNc1ccc(S(=O)(=O)NC(=O)c2ccc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)cc2Oc2cccc3c2CCC(=O)N3)cc1[N+](=O)[O-]
CN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)cc3Oc3ccccc3Cl)cc2S(=O)(=O)C(F)(F)F)CC1
CN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)cc3Oc3cc(Cl)ccc3Cl)cc2[N+](=O)[O-])CC1
CN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)cc3Oc3ccc(F)cc3Cl)cc2[N+](=O)[O-])CC1
CN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)C5)CC4)cc3Oc3ccccc3Cl)cc2[N+](=O)[O-])CC1
Cc1c[nH]c2cccc(Oc3cc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)ccc3C(=O)NS(=O)(=O)c3ccc(NCCCN4CCOCC4)c([N+](=O)[O-])c3)c12
CN1CCC(Nc2ccc(S(=O)(=O)NC(=O)c3ccc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)cc3Oc3cccc(C(F)(F)F)c3Cl)cc2[N+](=O)[O-])CC1
CC1(C)CCC(CN2CCN(c3ccc(C(=O)NS(=O)(=O)c4ccc(NC5CCN(C6CC6)CC5)c([N+](=O)[O-])c4)c(Oc4ccccc4Cl)c3)CC2)=C(c2ccc(Cl)cc2)C1
Cc1c[nH]c2cccc(Oc3cc(N4CCN(CC5=C(c6ccc(Cl)cc6)CC(C)(C)CC5)CC4)ccc3C(=O)NS(=O)(=O)c3ccc(NC4CCN(C)CC4)c([N+](=O)[O-])c3)c12
CC1(C)CCC(CN2CCN(c3ccc(C(=O)NS(=O)(=O)c4ccc(NCCCN5CCOCC5)c([N+](=O)[O-])c4)c(Oc4cc(Cl)ccc4Cl)c3)CC2)=C(c2ccc(Cl)cc2)C1
Cn1ccc2c(Oc3cc(N4CCN(Cc5ccccc5-c5ccc(Cl)cc5)CC4)ccc3C(=O)NS(=O)(=O)c3ccc(NCCCN4CCOCC4)c([N+](=O)[O-])c3)cccc21
O=C(NS(=O)(=O)c1ccc(NCCCN2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1cccc(N2CCOCC2)c1
CN(C)CCCNc1ccc(S(=O)(=O)NC(=O)c2ccc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)cc2Oc2ccc3[nH]cc(CCC(=O)N4CCOCC4)c3c2)cc1[N+](=O)[O-]
O=C(NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1cccc(OCc2ccccc2)c1
N#Cc1ccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)cc1
O=C(NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1ccc2[nH]cc(CCC(=O)N3CCOCC3)c2c1
O=C(NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1ccc2[nH]cc(CCCN3CCOCC3)c2c1
CN(C)Cc1ccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)cc1
O=C(NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1ccc(-n2ccnc2)cc1
O=C(NS(=O)(=O)c1ccc(NCC2CCOCC2)cc1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1cccc([N+](=O)[O-])c1
CCN(Cc1ccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)cc1)C(=O)OC(C)(C)C
CCN(Cc1cccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)c1)C(=O)OC(C)(C)C
CCNCc1ccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)cc1
CCNCc1cccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)c1
CC(=O)Nc1ccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)cc1
CC(C)(C)OC(=O)Nc1ccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)cc1
O=C(NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1ccccc1-c1ccccc1
CC(C)(C)OC(=O)Nc1cccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)c1
O=C(NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1cccc(-c2ccccc2)c1
CN(C)CCc1ccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)cc1
O=C(NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1ccc(OCc2ccccc2)cc1
O=C(NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1cccc(N2CCOCC2)c1
Cc1nc2cc(Oc3cc(N4CCN(Cc5ccccc5-c5ccc(Cl)cc5)CC4)ccc3C(=O)NS(=O)(=O)c3ccc(NCC4CCOCC4)c([N+](=O)[O-])c3)ccc2s1
CC(C)(C)OC(=O)N1CCN(c2cccc(Oc3cc(N4CCN(Cc5ccccc5-c5ccc(Cl)cc5)CC4)ccc3C(=O)NS(=O)(=O)c3ccc(NCC4CCOCC4)c([N+](=O)[O-])c3)c2)CC1
CN(C)CCCNc1ccc(S(=O)(=O)NC(=O)c2ccc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)cc2Oc2cccc(OCc3ccccc3)c2)cc1[N+](=O)[O-]
O=C(NS(=O)(=O)c1ccc(NCCCN2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1cccc(OCc2ccccc2)c1
O=C(NS(=O)(=O)c1ccc(NCC2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1ccc(OCCN2CCOCC2)cc1
O=C1CCc2c(cccc2Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)N1
O=C(NS(=O)(=O)c1ccc(NCCCN2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1ccc(OCc2ccccc2)cc1
CC(C)(C)OC(=O)N1CCN(c2ccc(Oc3cc(N4CCN(Cc5ccccc5-c5ccc(Cl)cc5)CC4)ccc3C(=O)NS(=O)(=O)c3ccc(NCCCN4CCOCC4)c([N+](=O)[O-])c3)cc2)CC1
O=C(NS(=O)(=O)c1ccc(NCCCN2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1cccc(-c2ccncc2)c1
O=C(NS(=O)(=O)c1ccc(NCCCN2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1ccc(-c2ccncc2)cc1
O=C(NS(=O)(=O)c1ccc(NCCCN2CCOCC2)c([N+](=O)[O-])c1)c1ccc(N2CCN(Cc3ccccc3-c3ccc(Cl)cc3)CC2)cc1Oc1ccc(-c2cccnc2)cc1
CN(C)C(=O)COc1ccc(Oc2cc(N3CCN(Cc4ccccc4-c4ccc(Cl)cc4)CC3)ccc2C(=O)NS(=O)(=O)c2ccc(NCC3CCOCC3)c([N+](=O)[O-])c2)cc1
Cn1cnc2cc(Oc3cc(N4CCN(Cc5ccccc5-c5ccc(Cl)cc5)CC4)ccc3C(=O)NS(=O)(=O)c3ccc(NCCCN4CCOCC4)c([N+](=O)[O-])c3)ccc21'''
    mols = [Chem.MolFromSmiles(x) for x in smis.split('\n')]

    core = Chem.MolFromSmarts('O=C(NS(=O)(=O)c1ccccc1)c1ccccc1Oc1ccccc1')
    ps = RGroupDecompositionParameters()
    ps.timeout = 0.1
    res = None
    with self.assertRaises(RuntimeError):
      rg = RGroupDecomposition(core, ps)
      for m in mols:
        res = rg.Add(m)
    self.assertIsNotNone(res)
    self.assertGreater(res, 0)

    with self.assertRaises(RuntimeError):
      columns2, unmatched = RGroupDecompose([core], mols, asRows=False, options=ps)

  def test_github3402(self):
    core1 = "[$(C-!@[a])](=O)(Cl)"
    sma = Chem.MolFromSmarts(core1)
    m = Chem.MolFromSmiles("c1ccccc1C(=O)Cl")
    self.assertEqual(RGroupDecompose(sma, [m], asSmiles=True), ([{
      'Core': 'O=C(Cl)[*:1]',
      'R1': 'c1ccc([*:1])cc1'
    }], []))

  def test_multicore_prelabelled(self):

    def multicorergd_test(cores, params, expected_rows, expected_items):
      mols = [Chem.MolFromSmiles(smi) for smi in ("CNC(=O)C1=CN=CN1CC", "Fc1ccc2ccc(Br)nc2n1")]
      params.removeHydrogensPostMatch = True
      params.onlyMatchAtRGroups = True
      decomp = RGroupDecomposition(cores, params)
      i = 0
      for i, m in enumerate(mols):
        res = decomp.Add(m)
        self.assertEqual(res, i)
      self.assertTrue(decomp.Process())
      rows = decomp.GetRGroupsAsRows(asSmiles=True)
      self.assertEqual(rows, expected_rows)
      items = decomp.GetRGroupsAsColumns(asSmiles=True)
      self.assertEqual(items, expected_items)

    sdcores = """
     RDKit          2D

  9  9  0  0  0  0  0  0  0  0999 V2000
    1.1100   -1.3431    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0
    1.5225   -0.6286    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.9705   -0.0156    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.2168   -0.3511    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0
    0.3029   -1.1716    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.1419    0.7914    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.5289    1.3431    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
    1.9266    1.0463    0.0000 R#  0  0  0  0  0  0  0  0  0  0  0  0
   -0.4976    0.0613    0.0000 R#  0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0
  2  3  2  0
  3  4  1  0
  4  5  1  0
  1  5  2  0
  3  6  1  0
  6  7  2  0
  6  8  1  0
  4  9  1  0
M  RGP  2   8   1   9   2
V    8 *
V    9 *
M  END
$$$$

     RDKit          2D

 12 13  0  0  0  0  0  0  0  0999 V2000
   -6.5623    0.3977    0.0000 R#  0  0  0  0  0  0  0  0  0  0  0  0
   -5.8478   -0.0147    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -5.1333    0.3977    0.0000 A   0  0  0  0  0  0  0  0  0  0  0  0
   -4.4188   -0.0147    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -4.4188   -0.8397    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -5.1333   -1.2522    0.0000 A   0  0  0  0  0  0  0  0  0  0  0  0
   -5.8478   -0.8397    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -3.7044   -1.2522    0.0000 A   0  0  0  0  0  0  0  0  0  0  0  0
   -3.7044    0.3977    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0
   -2.9899   -0.0147    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -2.9899   -0.8397    0.0000 A   0  0  0  0  0  0  0  0  0  0  0  0
   -2.2754    0.3978    0.0000 R#  0  0  0  0  0  0  0  0  0  0  0  0
  3  4  1  0
  4  5  2  0
  5  6  1  0
  6  7  2  0
  2  3  2  0
  2  7  1  0
  9 10  2  0
 10 11  1  0
  8 11  2  0
  8  5  1  0
  4  9  1  0
 10 12  1  0
  1  2  1  0
M  RGP  2   1   2  12   1
V    1 *
V   12 *
M  END
$$$$
"""
    sdsup = Chem.SDMolSupplier()
    sdsup.SetData(sdcores)
    cores = [c for c in sdsup]

    expected_rows = [{
      'Core': 'O=C(c1cncn1[*:2])[*:1]',
      'R1': 'CN[*:1]',
      'R2': 'CC[*:2]'
    }, {
      'Core': 'c1cc2ccc([*:2])nc2nc1[*:1]',
      'R1': 'F[*:1]',
      'R2': 'Br[*:2]'
    }]

    expected_items = {
      'Core': ['O=C(c1cncn1[*:2])[*:1]', 'c1cc2ccc([*:2])nc2nc1[*:1]'],
      'R1': ['CN[*:1]', 'F[*:1]'],
      'R2': ['CC[*:2]', 'Br[*:2]']
    }

    params = RGroupDecompositionParameters()

    # test pre-labelled with MDL R-group labels, autodetect
    params.labels = RGroupLabels.AutoDetect
    params.alignment = RGroupCoreAlignment.MCS
    multicorergd_test(cores, params, expected_rows, expected_items)
    # test pre-labelled with MDL R-group labels, no autodetect
    params.labels = RGroupLabels.MDLRGroupLabels | RGroupLabels.RelabelDuplicateLabels
    params.alignment = RGroupCoreAlignment.MCS
    multicorergd_test(cores, params, expected_rows, expected_items)
    # test pre-labelled with MDL R-group labels, autodetect, no MCS alignment
    params.labels = RGroupLabels.AutoDetect
    params.alignment = RGroupCoreAlignment.NoAlignment
    multicorergd_test(cores, params, expected_rows, expected_items)

    # Reading from a MDL molblock also sets isotopic labels, so no need
    # to set them again; we only clear MDL R-group labels
    for core in cores:
      for a in core.GetAtoms():
        if a.HasProp("_MolFileRLabel"):
          a.ClearProp("_MolFileRLabel")
    # test pre-labelled with isotopic labels, autodetect
    params.labels = RGroupLabels.AutoDetect
    params.alignment = RGroupCoreAlignment.MCS
    multicorergd_test(cores, params, expected_rows, expected_items)
    # test pre-labelled with isotopic labels, no autodetect
    params.labels = RGroupLabels.IsotopeLabels | RGroupLabels.RelabelDuplicateLabels
    params.alignment = RGroupCoreAlignment.MCS
    multicorergd_test(cores, params, expected_rows, expected_items)
    # test pre-labelled with isotopic labels, autodetect, no MCS alignment
    params.labels = RGroupLabels.AutoDetect
    params.alignment = RGroupCoreAlignment.NoAlignment
    multicorergd_test(cores, params, expected_rows, expected_items)

    for core in cores:
      for a in core.GetAtoms():
        iso = a.GetIsotope()
        if iso:
          a.SetAtomMapNum(iso)
          a.SetIsotope(0)
    # test pre-labelled with atom map labels, autodetect
    params.labels = RGroupLabels.AutoDetect
    params.alignment = RGroupCoreAlignment.MCS
    multicorergd_test(cores, params, expected_rows, expected_items)
    # test pre-labelled with atom map labels, no autodetect
    params.labels = RGroupLabels.AtomMapLabels | RGroupLabels.RelabelDuplicateLabels
    params.alignment = RGroupCoreAlignment.MCS
    multicorergd_test(cores, params, expected_rows, expected_items)
    # test pre-labelled with atom map labels, autodetect, no MCS alignment
    params.labels = RGroupLabels.AutoDetect
    params.alignment = RGroupCoreAlignment.NoAlignment
    multicorergd_test(cores, params, expected_rows, expected_items)

    for core in cores:
      for a in core.GetAtoms():
        if a.GetAtomMapNum():
          a.SetAtomMapNum(0)
    # test pre-labelled with dummy atom labels, autodetect

    expected_rows = [{
      'Core': 'O=C(c1cncn1[*:2])[*:1]',
      'R1': 'CN[*:1]',
      'R2': 'CC[*:2]'
    }, {
      'Core': 'c1cc2ccc([*:2])nc2nc1[*:1]',
      'R1': 'Br[*:1]',
      'R2': 'F[*:2]'
    }]

    expected_items = {
      'Core': ['O=C(c1cncn1[*:2])[*:1]', 'c1cc2ccc([*:2])nc2nc1[*:1]'],
      'R1': ['CN[*:1]', 'Br[*:1]'],
      'R2': ['CC[*:2]', 'F[*:2]']
    }

    params.labels = RGroupLabels.AutoDetect
    params.alignment = RGroupCoreAlignment.MCS
    multicorergd_test(cores, params, expected_rows, expected_items)
    # test pre-labelled with dummy atom labels, no autodetect
    # in this case there is no difference from autodetect as the RGD code
    # cannot tell the difference between query atoms and dummy R-groups
    params.labels = RGroupLabels.DummyAtomLabels | RGroupLabels.RelabelDuplicateLabels
    params.alignment = RGroupCoreAlignment.MCS
    multicorergd_test(cores, params, expected_rows, expected_items)

  def testRemoveAllHydrogenFlags(self):
    core = Chem.MolFromSmiles("[1*]c1ccc([2*])cn1")
    mol = Chem.MolFromSmiles("Fc1ccccn1")

    params = RGroupDecompositionParameters()
    rgd = RGroupDecomposition(core, params)
    self.assertEqual(rgd.Add(mol), 0)
    self.assertTrue(rgd.Process())
    res = rgd.GetRGroupsAsColumns(asSmiles=True)
    self.assertEqual(res, {'Core': ['c1ccc([*:1])nc1'], 'R1': ['F[*:1]']})

    # no change, as removeAllHydrogenRGroupsAndLabels is True
    params = RGroupDecompositionParameters()
    params.removeAllHydrogenRGroups = False
    rgd = RGroupDecomposition(core, params)
    self.assertEqual(rgd.Add(mol), 0)
    self.assertTrue(rgd.Process())
    res = rgd.GetRGroupsAsColumns(asSmiles=True)
    self.assertEqual(res, {'Core': ['c1ccc([*:1])nc1'], 'R1': ['F[*:1]']})

    # Unused user-defined labels retained on core
    # R groups still retained as removeAllHydrogenRGroups is True
    params = RGroupDecompositionParameters()
    params.removeAllHydrogenRGroupsAndLabels = False
    rgd = RGroupDecomposition(core, params)
    self.assertEqual(rgd.Add(mol), 0)
    self.assertTrue(rgd.Process())
    res = rgd.GetRGroupsAsColumns(asSmiles=True)
    self.assertEqual(res, {'Core': ['c1cc([*:1])ncc1[*:2]'], 'R1': ['F[*:1]']})

    # Unused user-defined labels retained on core and in R groups
    params = RGroupDecompositionParameters()
    params.removeAllHydrogenRGroups = False
    params.removeAllHydrogenRGroupsAndLabels = False
    rgd = RGroupDecomposition(core, params)
    self.assertEqual(rgd.Add(mol), 0)
    self.assertTrue(rgd.Process())
    res = rgd.GetRGroupsAsColumns(asSmiles=True)
    self.assertEqual(res, {'Core': ['c1cc([*:1])ncc1[*:2]'], 'R1': ['F[*:1]'], 'R2': ['[H][*:2]']})

  def testSubstructMatchParameters(self):
    mols = [
      Chem.MolFromSmiles(x) for x in ("C1CN[C@H]1F", "C1CN[C@]1(O)F", "C1CN[C@@H]1F", "C1CN[CH]1F")
    ]
    cores = [Chem.MolFromSmiles('C1CNC1[*:1]')]
    chiral_cores = [Chem.MolFromSmiles('C1CN[C@H]1[*:1]')]

    rgroups, unmatched = RGroupDecompose(cores, mols)
    self.assertEqual(unmatched, [])
    rgroups, unmatched = RGroupDecompose(chiral_cores, mols)
    self.assertEqual(unmatched, [3])

    params = RGroupDecompositionParameters()
    params.substructMatchParams.useChirality = False
    rgroups, unmatched = RGroupDecompose(cores, mols, options=params)
    self.assertEqual(unmatched, [])
    rgroups, unmatched = RGroupDecompose(chiral_cores, mols, options=params)
    self.assertEqual(unmatched, [])

  def testTautomerCore(self):
    block = """"
  Mrv2008 08072313382D          

  9  9  0  0  0  0            999 V2000
    5.9823    5.0875    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    5.9823    4.2625    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    5.2679    3.8500    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    4.5534    4.2625    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    4.5534    5.0875    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0
    5.2679    5.5000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    5.2679    6.3250    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
    6.6968    3.8500    0.0000 R#  0  0  0  0  0  0  0  0  0  0  0  0
    5.2679    3.0250    0.0000 R#  0  0  0  0  0  0  0  0  0  0  0  0
  1  2  2  0  0  0  0
  2  3  1  0  0  0  0
  3  4  2  0  0  0  0
  4  5  1  0  0  0  0
  5  6  1  0  0  0  0
  6  7  2  0  0  0  0
  1  6  1  0  0  0  0
  2  8  1  0  0  0  0
  3  9  1  0  0  0  0
M  RGP  2   8   1   9   2
M  END
"""
    core = Chem.MolFromMolBlock(block)
    mol1 = Chem.MolFromSmiles('Cc1cnc(O)cc1Cl')
    mol2 = Chem.MolFromSmiles('CC1=CNC(=O)C=C1F')

    params = RGroupDecompositionParameters()
    params.doTautomers = True
    rgd = RGroupDecomposition(core, params)
    self.assertEqual(rgd.Add(mol1), 0)
    self.assertEqual(rgd.Add(mol2), 1)
    self.assertTrue(rgd.Process())
    rows = rgd.GetRGroupsAsRows(asSmiles=True)
    expected_rows = [
        {'Core': 'Oc1cc([*:1])c([*:2])cn1', 'R1': 'Cl[*:1]', 'R2': 'C[*:2]'},
        {'Core': 'O=c1cc([*:1])c([*:2])c[nH]1', 'R1': 'F[*:1]', 'R2': 'C[*:2]'}]
    self.assertEqual(rows, expected_rows)

  def testMolMatchesCore(self):
    core = Chem.MolFromSmarts("[*:1]c1[!#1]([*:2])cc([*:3])n([*:4])c(=O)1")
    cmol = Chem.MolFromSmiles("Clc1c(C)cc(F)n(CC)c(=O)1")
    nmol = Chem.MolFromSmiles("Clc1ncc(F)n(CC)c(=O)1")
    smol = Chem.MolFromSmiles("Clc1ncc(F)n(CC)c(=S)1")
    params = RGroupDecompositionParameters()
    params.onlyMatchAtRGroups = True
    rgd = RGroupDecomposition(core, params)
    self.assertEqual(rgd.GetMatchingCoreIdx(cmol), 0)
    self.assertEqual(rgd.GetMatchingCoreIdx(nmol), 0)
    self.assertEqual(rgd.GetMatchingCoreIdx(smol), -1)
    matches = []
    self.assertEqual(rgd.GetMatchingCoreIdx(cmol, matches), 0)
    self.assertEqual(len(matches), 1)
    self.assertEqual(len(matches[0]), core.GetNumAtoms())
    matches = []
    self.assertEqual(rgd.GetMatchingCoreIdx(nmol, matches), 0)
    self.assertEqual(len(matches), 1)
    self.assertEqual(len(matches[0]), core.GetNumAtoms() - 1)
    matches = []
    self.assertEqual(rgd.GetMatchingCoreIdx(smol, matches), -1)
    self.assertEqual(len(matches), 0)
    cmol_h = Chem.AddHs(cmol)
    nmol_h = Chem.AddHs(nmol)
    self.assertTrue(cmol_h.HasSubstructMatch(core))
    self.assertEqual(len(cmol_h.GetSubstructMatch(core)), core.GetNumAtoms())
    self.assertFalse(nmol_h.HasSubstructMatch(core))

  def testRelabelMappedDummies(self):
    p = Chem.SmilesWriteParams()
    p.canonical = False
    allDifferentCore = Chem.MolFromMolBlock("""
     RDKit          2D

  8  8  0  0  0  0  0  0  0  0999 V2000
    1.0808   -0.8772    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.0827    0.1228    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.2177    0.6246    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.2198    1.6246    0.0000 R#  0  0  0  0  0 15  0  0  0  4  0  0
   -0.6493    0.1262    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -1.5142    0.6280    0.0000 R#  0  0  0  0  0 15  0  0  0  3  0  0
   -0.6513   -0.8736    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.2137   -1.3754    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  2  0
  2  3  1  0
  3  4  1  0
  3  5  2  0
  5  6  1  0
  5  7  1  0
  7  8  2  0
  8  1  1  0
M  RGP  2   4   2   6   1
M  END
)CTAB
""")
    allDifferentCore.RemoveConformer(0)
    allDifferentCore.GetAtomWithIdx(3).SetIsotope(6)
    allDifferentCore.GetAtomWithIdx(5).SetIsotope(5)
    self.assertEqual(Chem.MolToCXSmiles(allDifferentCore, p), "c1cc([6*:4])c([5*:3])cn1 |atomProp:3.dummyLabel.R2:3.molAtomMapNumber.4:5.dummyLabel.R1:5.molAtomMapNumber.3|")
    # AtomMap in, MDLRGroup out
    core = Chem.MolFromSmiles("c1cc([*:2])c([*:1])cn1")
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc([*:2])c([*:1])cn1 |atomProp:3.dummyLabel.*:3.molAtomMapNumber.2:5.dummyLabel.*:5.molAtomMapNumber.1|")
    RelabelMappedDummies(core)
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc(*)c(*)cn1 |atomProp:3.dummyLabel.R2:5.dummyLabel.R1|")
    # Isotope in, MDLRGroup out
    core = Chem.MolFromSmiles("c1cc([2*])c([1*])cn1")
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc([2*])c([1*])cn1 |atomProp:3.dummyLabel.*:5.dummyLabel.*|")
    RelabelMappedDummies(core)
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc(*)c(*)cn1 |atomProp:3.dummyLabel.R2:5.dummyLabel.R1|")
    # MDLRGroup in, MDLRGroup out
    core = Chem.MolFromMolBlock("""
     RDKit          2D

  8  8  0  0  0  0  0  0  0  0999 V2000
    1.0808   -0.8772    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.0827    0.1228    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.2177    0.6246    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.2198    1.6246    0.0000 R#  0  0  0  0  0  1  0  0  0  0  0  0
   -0.6493    0.1262    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -1.5142    0.6280    0.0000 R#  0  0  0  0  0  1  0  0  0  0  0  0
   -0.6513   -0.8736    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.2137   -1.3754    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  2  0
  2  3  1  0
  3  4  1  0
  3  5  2  0
  5  6  1  0
  5  7  1  0
  7  8  2  0
  8  1  1  0
M  RGP  2   4   2   6   1
M  END
)CTAB
""")
    core.RemoveConformer(0)
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc([2*])c([1*])cn1 |atomProp:3.dummyLabel.R2:5.dummyLabel.R1|")
    RelabelMappedDummies(core)
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc(*)c(*)cn1 |atomProp:3.dummyLabel.R2:5.dummyLabel.R1|")
    # AtomMap and Isotope in, MDLRGroup out - AtomMap has priority
    core = Chem.MolFromSmiles("c1cc([4*:2])c([3*:1])cn1")
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc([4*:2])c([3*:1])cn1 |atomProp:3.dummyLabel.*:3.molAtomMapNumber.2:5.dummyLabel.*:5.molAtomMapNumber.1|")
    RelabelMappedDummies(core)
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc(*)c(*)cn1 |atomProp:3.dummyLabel.R2:5.dummyLabel.R1|")
    # AtomMap and Isotope in, MDLRGroup out - force Isotope priority
    core = Chem.MolFromSmiles("c1cc([4*:2])c([3*:1])cn1")
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc([4*:2])c([3*:1])cn1 |atomProp:3.dummyLabel.*:3.molAtomMapNumber.2:5.dummyLabel.*:5.molAtomMapNumber.1|")
    RelabelMappedDummies(core, RGroupLabelling.Isotope)
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc(*)c(*)cn1 |atomProp:3.dummyLabel.R4:5.dummyLabel.R3|")
    # AtomMap, Isotope and MDLRGroup in, MDLRGroup out - AtomMap has priority
    core = Chem.Mol(allDifferentCore)
    RelabelMappedDummies(core)
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc(*)c(*)cn1 |atomProp:3.dummyLabel.R4:5.dummyLabel.R3|")
    # AtomMap, Isotope and MDLRGroup in, MDLRGroup out - force Isotope priority
    core = Chem.Mol(allDifferentCore)
    RelabelMappedDummies(core, RGroupLabelling.Isotope)
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc(*)c(*)cn1 |atomProp:3.dummyLabel.R6:5.dummyLabel.R5|")
    # AtomMap, Isotope and MDLRGroup in, MDLRGroup out - force MDLRGroup priority
    core = Chem.Mol(allDifferentCore)
    RelabelMappedDummies(core, RGroupLabelling.MDLRGroup)
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc(*)c(*)cn1 |atomProp:3.dummyLabel.R2:5.dummyLabel.R1|")
    # AtomMap, Isotope and MDLRGroup in, AtomMap out - AtomMap has priority
    core = Chem.Mol(allDifferentCore)
    RelabelMappedDummies(core, outputLabels=RGroupLabelling.AtomMap)
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc([*:4])c([*:3])cn1 |atomProp:3.molAtomMapNumber.4:5.molAtomMapNumber.3|")
    # AtomMap, Isotope and MDLRGroup in, Isotope out - AtomMap has priority
    core = Chem.Mol(allDifferentCore)
    RelabelMappedDummies(core, outputLabels=RGroupLabelling.Isotope)
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc([4*])c([3*])cn1")
    # AtomMap, Isotope and MDLRGroup in, AtomMap out - Isotope has priority
    core = Chem.Mol(allDifferentCore)
    RelabelMappedDummies(core, inputLabels=(RGroupLabelling.Isotope | RGroupLabelling.MDLRGroup), outputLabels=RGroupLabelling.AtomMap)
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc([*:6])c([*:5])cn1 |atomProp:3.molAtomMapNumber.6:5.molAtomMapNumber.5|")
    # AtomMap, Isotope and MDLRGroup in, Isotope out - Isotope has priority
    core = Chem.Mol(allDifferentCore)
    RelabelMappedDummies(core, inputLabels=(RGroupLabelling.Isotope | RGroupLabelling.MDLRGroup), outputLabels=RGroupLabelling.Isotope)
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc([6*])c([5*])cn1")
    # AtomMap, Isotope and MDLRGroup in, AtomMap out - MDLRGroup has priority
    core = Chem.Mol(allDifferentCore)
    RelabelMappedDummies(core, inputLabels=RGroupLabelling.MDLRGroup, outputLabels=RGroupLabelling.AtomMap)
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc([*:2])c([*:1])cn1 |atomProp:3.molAtomMapNumber.2:5.molAtomMapNumber.1|")
    # AtomMap, Isotope and MDLRGroup in, Isotope out - MDLRGroup has priority
    core = Chem.Mol(allDifferentCore)
    RelabelMappedDummies(core, inputLabels=RGroupLabelling.MDLRGroup, outputLabels=RGroupLabelling.Isotope)
    self.assertEqual(Chem.MolToCXSmiles(core, p), "c1cc([2*])c([1*])cn1")

  def testRgroupMolZip(self):
    core = Chem.MolFromSmiles("CO")
    mols = [Chem.MolFromSmiles("C1NNO1")]
    rgroups, unmatched = RGroupDecompose(core, mols)
    for rgroup in rgroups:
      self.assertEqual(Chem.MolToSmiles(Chem.molzip(rgroup)),
                       Chem.CanonSmiles("C1NNO1"))

  def testIncludeTargetMolInResults(self):
    core = Chem.MolFromSmiles("c1cc(-c2c([*:1])nn3nc([*:2])ccc23)nc(N(c2ccc([*:4])c([*:3])c2))n1")
    self.assertIsNotNone(core)
    mols = [Chem.MolFromSmiles(smi) for smi in [
      "Cc1ccc2c(c3ccnc(Nc4cccc(c4)C(F)(F)F)n3)c(nn2n1)c5ccc(F)cc5",
      "Cc1ccc2c(c3ccnc(Nc4ccc(F)c(F)c4)n3)c(nn2n1)c5ccc(F)cc5",
      "Cc1ccc2c(c3ccnc(Nc4ccc5OCCOc5c4)n3)c(nn2n1)c6ccc(F)cc6",
      "Cc1ccc2c(c3ccnc(Nc4ccc(Cl)c(c4)C(F)(F)F)n3)c(nn2n1)c5ccc(F)cc5",
      "C1CC1c2nn3ncccc3c2c4ccnc(Nc5ccccc5)n4",
      "Fc1ccc(Nc2nccc(n2)c3c(nn4ncccc34)C5CC5)cc1F",
      "C1CCC(CC1)c2nn3ncccc3c2c4ccnc(Nc5ccccc5)n4",
      "Fc1ccc(Nc2nccc(n2)c3c(nn4ncccc34)C5CCCCC5)cc1F",
      "COCCOc1cnn2ncc(c3ccnc(Nc4cccc(OC)c4)n3)c2c1",
      "Cc1ccc2c(c3ccnc(Nc4ccc(F)c(F)c4)n3)c(nn2n1)c5ccccc5",
      "Cc1ccc2c(c3ccnc(Nc4ccc(Cl)c(c4)C(F)(F)F)n3)c(nn2n1)c5ccccc5",
      "Cc1ccc2c(c3ccnc(Nc4ccc5OCCOc5c4)n3)c(nn2n1)c6ccccc6",
      "Cc1ccc2c(c3ccnc(Nc4ccccc4)n3)c(nn2n1)c5cccc(c5)C(F)(F)F",
      "Cc1ccc2c(c3ccnc(Nc4ccc(F)c(F)c4)n3)c(nn2n1)c5cccc(c5)C(F)(F)F",
      "Cc1ccc2c(c3ccnc(Nc4ccc(Cl)c(c4)C(F)(F)F)n3)c(nn2n1)c5cccc(c5)C(F)(F)F",
      "Cc1ccc2c(c3ccnc(Nc4ccc5OCCOc5c4)n3)c(nn2n1)c6cccc(c6)C(F)(F)F",
    ]]
    self.assertTrue(all(mols))
    ps = RGroupDecompositionParameters()
    ps.includeTargetMolInResults = True
    rgd = RGroupDecomposition(core, ps)
    for mol in mols:
      self.assertNotEqual(rgd.Add(mol), -1)
    self.assertTrue(rgd.Process())
    def checkRow(row):
      targetMol = None
      # These are sets of int tuples rather just plain int tuples
      # because there can be cyclic R groups with 2 attachment points
      # in that case it is OK for 2 R groups to have exactly the same
      # target atom and bond indices
      allAtomIndices = set()
      allBondIndices = set()
      for rlabel, rgroup in row.items():
        if rlabel == "Mol":
          targetMol = rgroup
        else:
          numNonRAtoms = len([atom for atom in rgroup.GetAtoms() if atom.GetAtomicNum() > 0 or not atom.GetAtomMapNum()])
          self.assertGreater(rgroup.GetNumAtoms(), numNonRAtoms)
          numBonds = 0
          if rlabel == "Core":
            numBonds = len([bond for bond in rgroup.GetBonds() if (
              bond.GetBeginAtom().GetAtomicNum() > 0 or not bond.GetBeginAtom().GetAtomMapNum()
            ) and (
              bond.GetEndAtom().GetAtomicNum() > 0 or not bond.GetEndAtom().GetAtomMapNum()
            )])
          else:
            numBonds = rgroup.GetNumBonds()
          self.assertTrue(rgroup.HasProp("_rgroupTargetAtoms"))
          atomIndices = tuple(json.loads(rgroup.GetProp("_rgroupTargetAtoms")))
          self.assertTrue(rgroup.HasProp("_rgroupTargetBonds"))
          bondIndices = tuple(json.loads(rgroup.GetProp("_rgroupTargetBonds")))
          self.assertEqual(len(atomIndices), numNonRAtoms)
          allAtomIndices.add(atomIndices)
          self.assertEqual(len(bondIndices), numBonds)
          allBondIndices.add(bondIndices)
      self.assertIsNotNone(targetMol)
      flattenedAtomIndices = list(itertools.chain.from_iterable(allAtomIndices))
      uniqueAtomIndices = set(flattenedAtomIndices)
      self.assertEqual(len(flattenedAtomIndices), len(uniqueAtomIndices))
      self.assertEqual(len(flattenedAtomIndices), targetMol.GetNumAtoms())
      flattenedBondIndices = list(itertools.chain.from_iterable(allBondIndices))
      uniqueBondIndices = set(flattenedBondIndices)
      self.assertEqual(len(flattenedBondIndices), len(uniqueBondIndices))
      self.assertEqual(len(flattenedBondIndices), targetMol.GetNumBonds())
    rows = rgd.GetRGroupsAsRows()
    self.assertEqual(len(rows), len(mols))
    for row in rows:
      checkRow(row)
    cols = rgd.GetRGroupsAsColumns()
    rows = []
    for i in range(len(mols)):
      row = {}
      for rlabel, rgroups in cols.items():
        self.assertEqual(len(rgroups), len(mols))
        row[rlabel] = rgroups[i]
      rows.append(row)
    self.assertEqual(len(rows), len(mols))
    for row in rows:
      checkRow(row)


if __name__ == '__main__':
  rdBase.DisableLog("rdApp.debug")
  unittest.main()

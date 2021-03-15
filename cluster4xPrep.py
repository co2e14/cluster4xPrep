#!/usr/bin/env python3 
import os
import time
import glob
from pathlib import Path
from shutil import copyfile as cp
from distutils.dir_util import copy_tree


class c4xp:
    def __init__(self, directory):
        self.cwd = os.getcwd()
        self.l = [x[0] for x in os.walk(directory)]

    def folderfindandcopy(self, foldername, tocopy):
        self.m = []
        folder_num = 0
        for x in self.l:
            if str(foldername) in x:
                self.m += [x]
        
        for y in self.m:
            folder_num += 1
            copyto = str(os.path.join(self.cwd, ("c4x_" + str(folder_num))))
            os.mkdir(copyto)
            for x in os.listdir(y):
                if x.endswith(tocopy):
                    sourcefile = os.path.join(y, x)
                    destfile = os.path.join(copyto, x)
                    cp(sourcefile, destfile)
                else:
                    pass
            print("Copied ", str(folder_num), " out of ", str(len(self.m)), end="\r")

    def HKL_PDB(self, model):
        self.model = os.path.abspath(model)
        self.torun = [x[0] for x in os.walk(self.cwd)]
        try:
            self.torun.remove(self.cwd)
        except ValueError:
            pass
        folder_num = 0
        for x in self.torun:
            folder_num += 1
            copyto = str(os.path.join(self.cwd, ("c4x_" + str(folder_num)), "modelin.pdb"))
            cp(self.model, copyto)
            if "c4x_" in x:
                filelist = os.listdir(x)
                for f in filelist:
                    if f.endswith(".HKL"):
                        os.chdir(x)
                        os.rename(f, "HKLIN.HKL")
                        #os.system(str('pointless HKLOUT pointless.mtz HKLIN HKLIN.HKL >/dev/null 2>&1'))
                        #os.system(str('aimless HKLIN pointless.mtz HKLOUT scaled.mtz --no-input >/dev/null 2>&1'))
                        #os.system(str('molrep -f scaled.mtz -m modelin.pdb >/dev/null 2>&1'))
                        #s.system(str('dimple --anode -s scaled.mtz modelin.pdb ./ >/dev/null 2>&1'))
                        os.chdir(self.cwd)
                        #print("Completed " + str(folder_num) + " out of " + str(len(self.torun)))
                    else:
                        pass
            else:
                pass

    def mainrun(self):
        print("")
        n = 0
        for x in self.torun:
            if "c4x_" in x:
                os.chdir(x)
                n += 1
                print("pointess run: ", str(n), " of ", str(len(self.torun)), end="\r")
                os.system(str('pointless HKLOUT pointless.mtz HKLIN HKLIN.HKL >/dev/null 2>&1'))
                time.sleep(1)
        print("")
        n = 0
        for x in self.torun:
            if "c4x_" in x:
                os.chdir(x)
                n += 1
                print("aimless run: ", str(n), " of ", str(len(self.torun)), end="\r")
                os.system(str('aimless HKLIN pointless.mtz HKLOUT scaled.mtz --no-input >/dev/null 2>&1'))
                time.sleep(1)
        print("")
        n = 0
        for x in self.torun:
            if "c4x_" in x:
                os.chdir(x)
                n += 1
                print("dimple run: ", str(n), " of ", str(len(self.torun)), end="\r")
                os.system(str('dimple --anode -s scaled.mtz modelin.pdb ./ >/dev/null 2>&1'))
                time.sleep(1)


if __name__ == "__main__":
    rundimp = "m" #str(input("Do you want to run dimple from an mtz/sca/HKL or use autoprocessed dimple runs? (m/a) ")).lower()
    if rundimp is "a":
        searchpath = "/dls/i23/data/2021/mx22563-22/processed/L247_WT_old/20210223" #str(input("Path to processed dimple runs: "))
        searchterm = str("dimple")
        tocopy = ("final.pdb", "final.mtz", "anode.lsa", "anode.pha")
    if rundimp == "m":
        os.system("module load ccp4")
        searchpath = "/dls/i23/data/2021/mx22563-22/processed/L247_WT_old/20210223" #str(input("Path to processed xia2-3dii runs: "))
        modelin = str(input("Model in: "))
        searchterm = str("xia2-3dii/DataFiles")
        tocopy = str("CORRECT.HKL")
    cluster4xPrep = c4xp(searchpath)
    cluster4xPrep.folderfindandcopy(searchterm, tocopy)
    if rundimp == "m":
        cluster4xPrep.HKL_PDB(modelin)
        cluster4xPrep.mainrun()
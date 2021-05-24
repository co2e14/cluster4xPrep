#!/usr/bin/env python3
import os
import time
import glob
from pathlib import Path
from shutil import copyfile as cp
from distutils.dir_util import copy_tree
from multiprocessing import Pool


class c4xp:
    def __init__(self, directory):
        self.cwd = os.getcwd()
        self.cpus = os.cpu_count()
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
                    with open("filelist.txt", "a") as filelist:
                        filelist.write("\nc4x_" + str(folder_num) + " = " + str(y))
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
        self.torun = [x for x in self.torun if "c4x_" in x]
        for x in self.torun:
            folder_num += 1
            copyto = str(
                os.path.join(self.cwd, ("c4x_" + str(folder_num)), "modelin.pdb")
            )
            cp(self.model, copyto)
            if "c4x_" in x:
                filelist = os.listdir(x)
                for f in filelist:
                    if f.endswith(".HKL"):
                        os.chdir(x)
                        os.rename(f, "HKLIN.HKL")
                        os.chdir(self.cwd)
                    else:
                        pass
            else:
                pass
        torun = self.torun
        print("\nModels copied, starting poinless runs")
        return torun

    def pointless(self, dir):
        os.chdir(dir)
        os.system(str("pointless HKLOUT pointless.mtz HKLIN HKLIN.HKL >/dev/null 2>&1"))

    def aimless(self, dir):
        os.chdir(dir)
        os.system(
            str(
                "aimless HKLIN pointless.mtz HKLOUT scaled.mtz --no-input >/dev/null 2>&1"
            )
        )

    def dimple(self, dir):
        os.chdir(dir)
        os.system(str("dimple --anode -s scaled.mtz modelin.pdb ./ >/dev/null 2>&1"))


if __name__ == "__main__":
    pool = Pool(os.cpu_count() - 1)
    print("Using ", str(os.cpu_count() - 1), "CPU cores")
    rundimp = str(
        input(
            "Do you want to run dimple from an mtz/sca/HKL or use autoprocessed dimple runs? (m/a) "
        )
    ).lower()
    if rundimp is "a":
        searchpath = str(input("Path to processed dimple runs: "))
        searchterm = str("dimple")
        tocopy = ("final.pdb", "final.mtz", "anode.lsa", "anode.pha")
    if rundimp == "m":
        os.system("module load ccp4")
        searchpath = str(input("Path to processed xia2-3dii runs: "))
        modelin = str(input("Model in: "))
        searchterm = str("xia2-3dii/DataFiles")
        tocopy = str("CORRECT.HKL")
    cluster4xPrep = c4xp(searchpath)
    cluster4xPrep.folderfindandcopy(searchterm, tocopy)
    if rundimp == "m":
        torun = cluster4xPrep.HKL_PDB(modelin)
        pool.map(cluster4xPrep.pointless, torun)
        print("Pointless runs finished, starting aimless runs", end="\r")
        pool.map(cluster4xPrep.aimless, torun)
        print("Aimless runs finished, starting dimple runs   ", end="\r")
        pool.map(cluster4xPrep.dimple, torun)
        print("Dimple finished. All done!                    ", end="\r")
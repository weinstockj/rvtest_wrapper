import os
import stat
import sys
import argparse
import ipdb

argparser = argparse.ArgumentParser(description = 'create Makefile from rvtest')

argparser.add_argument('--pheno-name', metavar = 'name(s)', 
                        dest = 'pheno_name', required = True, help = 'SLURM partition name.')
argparser.add_argument('--directory', metavar = 'name(s)', 
                        dest = 'directory', required = True, help = 'rvtest output directory')
argparser.add_argument('--ped', metavar = 'name(s)', 
                        dest = 'ped', required = True, help = 'ped file')


def create_command(genotype, ped, directory, pheno_name, chrom):
    cmd = """/net/fantasia/home/jweinstk/downloads/rvtests/executable/rvtest --inVcf {genotype} --pheno {ped} --pheno-name {pheno_name} --out {directory}chr{chrom} --dosage DS --covar-name AGE,SEX,PC1,PC2,PC3,PC4 --single firth --freqLower 0.01""".format(genotype = genotype,
                                                ped = ped,
                                                pheno_name = pheno_name,
                                                directory = directory,
                                                chrom = chrom)
    return cmd


class rule:
    def __init__(self, directory, ped, pheno_name, chrom):
        self.directory = directory
        self.ped = ped
        self.chrom = chrom
        self.pheno_name = pheno_name
        self.target = os.path.join(self.directory, "chr{}.SingleFirth.assoc".format(self.chrom))
        self.genotype = "/net/fantasia/home/schellen/PheWAS/genotypes/DataFreeze_201602/MGI_HRC_chr{}.dose.vcf.gz".format(self.chrom)

    def create_rule(self):
        command = create_command(self.genotype, self.ped, self.directory, self.pheno_name, self.chrom)
        return """\n{target}: {genotype} {ped}\n\t{command}\n""".format(target = self.target, 
                                                                    genotype = self.genotype, 
                                                                    ped = self.ped,
                                                                    command = command)

def makefile_start(args):
    # https://stackoverflow.com/questions/24641948/merging-csv-files-appending-instead-of-merging/24643455
    cmd = """/net/fantasia/home/jweinstk/rvtest_wrapper/cat_rvtest.sh {directory} {pheno}\n""".format(directory = args.directory,
                                                                                                    pheno = args.pheno_name)
    return cmd

def create_makefile(args):

    makefile = ""
    makefile = "all: {directory}rvtests.OK\n".format(directory = args.directory)
    # makefile = ".DELETE_ON_ERROR\nall: {directory}rvtests.OK\n".format(directory = args.directory)
    autosomes = range(1, 23)
    global rule
    rules = [rule(args.directory, args.ped, args.pheno_name, chrom) for chrom in autosomes]
    makefile += "\n{directory}rvtests.OK: {targets}".format(directory = args.directory, 
                                                            targets = " ".join([r.target for r in rules]))
    makefile += makefile_start(args)

    for r in rules:
        makefile += r.create_rule()

    return makefile

class test_args:
    pheno_name = "250.2"
    directory = "/net/fantasia/home/jweinstk/mgi/mgiAnalysis/output/case_control/250.2/"
    ped = "/net/fantasia/home/jweinstk/julia-epacts/data/MGI.filtered.discrete.FINAL2.ped"

# test = test_args()

if __name__ == "__main__":
    args = argparser.parse_args()
    script = create_makefile(args)
    output = "{directory}{pheno}.Makefile".format(directory = args.directory, pheno = args.pheno_name)
    with open(output, "w") as f:
        f.write(script)


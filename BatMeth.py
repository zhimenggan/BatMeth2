#!/usr/bin/env python
import os
import sys, getopt

##alignment
threads = 6
mismatches = 2
genome_index = ""
input_prefix = ""
output_prefix = ""

##calmeth
Qual = 10
redup = 0
region = 1000
##calmeth and methyGff
coverage = 5
binCover = 3
chromstep = 50000

##methyGff
step = 0.025
distance = 2000
gfffile = ""
bedfile = ""

##mode
mode = "pipel"

def usage():
    print "BatMeth2 [mode] [paramaters]"
    print "mode:  build_index, pipel, align, calmeth, annoation, methyPlot, batDMR, visul2sample"
    print "\n[build_index]"
    print "    Usage: BatMeth2 build_index genomefile. (must run this step first)"

    print "\n[pipel (Contains: align, calmeth, annoation, methyPlot):]"
    print "    [main paramaters]"
    print "    -o    Name of output file prefix"
    print "    [alignment paramaters]"
    print "    -i    Name of input file"
    print "    -g    Name of the genome mapped against"
    print "    -n    maximum mismatches allowed due to seq. errors"
    print "    -p <interger>    Launch <integer> threads"
    print "    [calmeth paramaters]"
    print "    --Qual      caculate the methratio while read QulityScore >= Q. default:10"
    print "    --redup     REMOVE_DUP"
    print "    --region    Bins for DMR caculate , default 1000bp ."
    print "    [calmeth and annoation paramaters]"
    print "    --coverage    >= <INT> coverage. default:5"
    print "    --binCover    >= <INT> nCs per region. default:3"
    print "    --chromstep   Chrosome using an overlapping sliding window of 100000bp at a step of 50000bp. default step: 50000(bp)"
    print "    [annoation paramaters]"
    print "    --gtf/--bed    Gtf or gff file / bed file"
    print "    --distance    DNA methylation level distributions in body and <INT>-bp flanking sequences. The distance of upstream and downstream. default:2000"
    print "    --step    Gene body and their flanking sequences using an overlapping sliding window of 5% of the sequence length at a step of 2.5% of the sequence length. So default step: 0.025 (2.5%)"

    print "\n[align paramaters:]"
    print "    see the details in 'BatMeth2 align'"
    print "\n[calmeth paramaters:]"
    print "    see the details in 'BatMeth2 calmeth'"
    print "\n[annotion paramaters:]"
    print "    see the details in 'BatMeth2 annoation'"
    print "\n[methyPlot paramaters:]"
    print "    see the details in 'BatMeth2 methyPlot'"
    print "\n[batDMR paramaters:]"
    print "    see the details in 'BatMeth2 batDMR'"
    print "\n[visul2sample paramaters:]"
    print "    see the details in 'BatMeth2 visul2sample'\n"


if len(sys.argv) < 2:
    usage()
    sys.exit()

def detect_paramater():
    opts, args = getopt.getopt(sys.argv[2:], "hi:o:n:g:p:", ["gtf", "bed", "coverage", "binCover", 
        "chromstep", "step", "distance"])
    global input_prefix, output_prefix, genome_index, threads, mismatches
    for op, value in opts:
        print op, value
        if op == "-i":
            input_prefix = value
        elif op == "-o":
            output_prefix = value
        elif op == "g":
            genome_index = value
        elif op == "p":
            threads = value
        elif op == "n":
            mismatches = value
        elif op == "gtf":
            gfffile = value
        elif op == "bed":
            bedfile = value
        elif op == "coverage":
            coverage = value
        elif op == "binCover":
            binCover = value
        elif op == "chromstep":
            chromstep = value
        elif op == "step":
            step = value
        elif op == "distance":
            distance = value
        elif op == "-h":
            usage()
            sys.exit()

mode = sys.argv[1]

if mode == "pipel":
    detect_paramater()


##for i in range(1, len(sys.argv)):
##  print sys.argv[i]

def runprogram(cmd):
    print cmd
    error = os.system(cmd)
    if error != 0:
        print "program %s error!"%cmd
        sys.exit()

def calmeth(genome_index, mismatches, inputf, output_prefix, threads):
    if genome_index == "":
        print "Please use -g pramater to defined the genome index location."
        sys.exit()
    if methratio == "":
        print "Must have methratio file (-m paramater)."
        sys.exit()
    if inputf == "":
        print "Must have input sam file (-i paramater)."
        sys.exit()
    cmd = "calmeth" + " -g " + genome_index + " -n " + str(mismatches) + " -i " + inputf + " -m " + output_prefix  + " -p " + str(threads)
    if chromstep != 50000:
        cmd = cmd + " -s " + chromstep
    elif coverage != 5:
        cmd = cmd + " -C " + coverage
    elif binCover != 3:
        cmd = cmd + " -nC " + binCover
    runprogram(cmd)
    return

def build_index(genome_index):
    if genome_index == "":
        print "Must have genome file."
        sys.exit()
    cmd = "build_all " + genome
    runprogram(cmd)

def alignment(genome_index, threads, mismatches, inputf, outputf):
    if (genome_index == "") or (inputf == "") or (outputf == ""):
        print "Please check the pramater."
        runprogram("batmeth2")
        sys.exit()
    cmd = "batmeth2" + " -g " + genome_index + " -p " + str(threads) + " -n " + str(mismatches) + " -i " + input_prefix + " -o " + output_prefix
    runprogram(cmd)

def annoation():
    if gfffile != "":
        cmd = "methyGff" + " -o " + output_prefix + " -G " + genome_index + " -g " + gfffile + " -m " + methratio + " -B -P --TSS --TTS --GENE"
    elif bedfile != "":
        cmd = "methyGff" + " -o " + output_prefix + " -G " + genome_index + " -b " + bedfile + " -m " + methratio + " -B -P --TSS --TTS --GENE"
    elif step != 0.025:
        cmd = cmd + " -s " + step
    elif chromstep != 50000:
        cmd = cmd + " -S " + chromstep
    elif coverage != 5:
        cmd = cmd + " -C " + coverage
    elif binCover != 3:
        cmd = cmd + " -nC " + binCover
    elif distance != 2000:
        cmd = cmd + " -d " + distance
    runprogram(cmd)

##methylation data visulization
def visulize():
    abspath = os.path.abspath(sys.argv[0])

## whole pipeline for DNA methylation analysis. Contains alignment, calute meth level, DNA methylation annatation
## on gff file or bed region, DNA methylation visulization. Differentail analysis use diffmeth function.
def runpipe():
    align_result = output_prefix + ".sam"
    alignment(genome_index, threads, mismatches, input_prefix, align_result)
    calmeth(genome_index, mismatches, align_result, output_prefix, threads)
    annoation()
    methyPlot()

def methyPlot():
    ##
    cmd = "methyPlot {output_prefix}.methBins.txt {output_prefix}.chrosome.methy.distri.pdf {step} {output_prefix}.Methylevel.1.txt {output_prefix}.methlevel.pdf {output_prefix}.AverMethylevel.1.txt {output_prefix}.elements.pdf"
    cmd = cmd.format(**locals())
    runprogram(cmd)
    abspath = os.path.abspath(methyPlot)
    cmd = "Rscript {abspath}/density_plot_with_methyl_oneSample_oneGff.r {output_prefix}.methBins.txt {output_prefix}.annoDensity.1.txt {output_prefix}.density.pdf {output_prefix} "
    cmd = cmd.format(**locals())
    runprogram(cmd)

def visul2sample():
    cmd = "GeneMethHeatmap {sample1_prefix} {sample2_prefix} {CG} {CHG} {CHG}"

#"pipel", "index", "align", "calmeth", "anno", "visul", "diffmeth", "visuldiff", DManno"
command = sys.argv[1]
if command == "build_index":
    build_index(genome_index)
elif command == "pipel":
    runpipe()
elif command == "align":
    cmd = "batmeth2 "
    runprogram(cmd)
elif command == "calmeth":
    cmd = "calmeth "
    runprogram(cmd)
elif command == "anno":
    cmd = "methyGff "
    runprogram(cmd)
elif command == "visul":
    cmd = "methyPlot" 
    runprogram(cmd)
elif command == "diffmeth":
    cmd = "batDMR" 
    runprogram(cmd)
elif command == "DManno":
    cmd = "DMCannotationPlot" 
    runprogram(cmd)
else:
    print "can not detect any command!"
    usage()
    sys.exit()
    



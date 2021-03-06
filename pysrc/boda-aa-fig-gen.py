
#note: to be run from a run directory at a depth like: boda/run/tr1, so that ../.. is the root of a boda WC. e.g:
# cd boda/run/tr1
# python ../../pysrc/boda-aa-fig-gen.py

#note: for safety, start with an empty directory, or at least remove
#all csv/png/pdf files before starting. that way, in case of errors,
#stale files won't be used. and actually read the output to look for
#errors!


import os
ospj = os.path.join

def run_cmds( cmds, fmt_data ):
    for cmd in cmds:
        fin_cmd = cmd % fmt_data
        print "RUN: "+fin_cmd
        os.system( fin_cmd )

class figgen_t( object ):
    def __init__( self, args ):
        self.args = args

        fmt_data = { "wis" : "--min_flops=1e8 --wisdom-in-fn=" + args.wis_fn, 
                     "cudnn_ref" : "--ref-tune='(use_be=nvrtc,use_culibs=1)'",
                     "s_img" : "--s-img=5" }
        fmt_data["ops_out_fn"] = ospj(self.args.out_dir,"ops-out-sort-by-flops.tex")
        fmt_data["out_fn"] = ospj(self.args.out_dir,"titan-ocl-vs-nvrtc") # generate ocl/nvrtc comparison figure
        cmds = [
            "boda wis-ana %(wis)s %(s_img)s --s-plat='ocl.*TITAN' --ops-out-fn=ops-out-nosort.tex --show-pom=0 --show-ref=0 --show-aom=0",
            "sort -g -k25 ops-out-nosort.tex > %(ops_out_fn)s",
            "boda wis-ana %(wis)s %(s_img)s --s-plat='ocl.*TITAN' --csv-out-fn=out-tit-ocl-5-pom.csv --pom-tag='boda-autotuned-TITAN-OpenCL' --show-ref=0 --show-aom=0",
            "boda wis-ana %(wis)s %(s_img)s %(cudnn_ref)s --s-plat='nvrtc.*TITAN' --csv-out-fn=out-tit-nvrtc-5-pom.csv --pom-tag='boda-autotuned-TITAN-CUDA' --show-ref=0 --show-aom=0",
            "python ../../pysrc/wis-plot.py out-tit-ocl-5-pom.csv out-tit-nvrtc-5-pom.csv --out-fn=%(out_fn)s --out-fmt=pdf --title='OpenCL vs CUDA(nvrtc) Speed on NVIDIA Titan-X(Maxwell)'",
        ]
        run_cmds( cmds, fmt_data )
        fmt_data["out_fn"] = ospj(self.args.out_dir,"sd820-tune") # generate SD820 tuning figure
        cmds = [
            "boda wis-ana %(wis)s %(s_img)s --s-plat='Adreno' --csv-out-fn=out-adreno.csv --show-ref=0 --show-aom=0 --pom-tag='boda-autotuned-SD820'",
            "boda wis-ana %(wis)s %(s_img)s --s-plat='Adreno' --csv-out-fn=out-adreno-nvtune.csv --show-ref=1 --show-aom=0 --show-pom=0 --ref-tune='(use_be=ocl)' --ref-tag='boda-intial-SD820'",
            "python ../../pysrc/wis-plot.py out-adreno.csv out-adreno-nvtune.csv --out-fn=%(out_fn)s --out-fmt=pdf --title='Tuned and Autotuned Speed on Qualcomm Snapdragon 820'" ]
        run_cmds( cmds, fmt_data )

        fmt_data["out_fn"] = ospj(self.args.out_dir,"fiji-tune") # generate AMD tuning figure
        cmds = [
            "boda wis-ana %(wis)s %(s_img)s --s-plat='Fiji' --csv-out-fn=out-fiji.csv --show-ref=0 --pom-tag='boda-autotuned-R9' --aom-tag='boda-manual-tune-R9'",
            "python ../../pysrc/wis-plot.py out-fiji.csv --out-fn=%(out_fn)s --out-fmt=pdf --title='Tuned and Autotuned Speed on AMD R9-Nano(Fiji)'" ]
        run_cmds( cmds, fmt_data )
        fmt_data["out_fn"] = ospj(self.args.out_dir, "titan-tune") # generate NVIDIA tuning figure
        cmds = [
            "boda wis-ana %(wis)s %(s_img)s %(cudnn_ref)s --s-plat='nvrtc.*TITAN' --csv-out-fn=out-titan.csv --show-ref=1 --show-aom=0 --pom-tag='boda-autotuned-TITAN' --ref-tag='NVIDIA-cuDNNv5-library'",
            "python ../../pysrc/wis-plot.py out-titan.csv --out-fn=%(out_fn)s --out-fmt=pdf --title='Tuned, Autotuned, and Reference(cuDNNv5) Speed on NVIDIA TITAN-X(Maxwell)'" ]
        run_cmds( cmds, fmt_data )
        fmt_data["out_fn"] = ospj(self.args.out_dir,"all-plats") # generate all-plats figure
        cmds = [
            "boda wis-ana %(wis)s %(s_img)s %(cudnn_ref)s --s-plat='nvrtc.*TITAN' --csv-out-fn=all-plats-titan.csv --show-ref=0 --show-aom=0 --pom-tag='boda-autotuned-TITAN'",
            "boda wis-ana %(wis)s %(s_img)s --s-plat='Fiji' --csv-out-fn=all-plats-fiji.csv --show-ref=0 --show-aom=0 --pom-tag='boda-autotuned-R9'",
            "boda wis-ana %(wis)s %(s_img)s --s-plat='Adreno' --csv-out-fn=all-plats-SD820.csv --show-ref=0 --show-aom=0 --pom-tag='boda-autotuned-SD820'",
            "python ../../pysrc/wis-plot.py all-plats-titan.csv all-plats-fiji.csv all-plats-SD820.csv --out-fn=%(out_fn)s --out-fmt=pdf --title='Autotuned Speed on NVIDIA TITAN-X, AMD R9-Nano, and Qualcomm Snapdragon 820'" ]
        run_cmds( cmds, fmt_data )
        

        



import argparse
parser = argparse.ArgumentParser(description='generate list of figures for boda-aa paper.')
parser.add_argument('--wis-fn', metavar="FN", type=str, default="../../test/wisdom-merged.wis", help="filename of results database" )
parser.add_argument('--out-dir', metavar="FN", type=str, default="../../../boda-autotune-amd/figs", help="filename of results database" )
args = parser.parse_args()

figgen_t( args )


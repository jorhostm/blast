import fileinput
import os, sys, stat
import glob

def parameterize(filenames):
   for file in filenames:
      with open(file,"r") as f:
            header = f.readline().strip('\n')
      if header == "*Heading":
         print(f"Parameterizing {file} ...")
         for line in fileinput.input(file, inplace=1):
            line = line.replace("material=AA6016_T4", "material=<MAT>")
            line = line.replace("*Dsload\n", "*Dsload, amplitude=<AMP>\n")
            line = line.replace("LoadSurface", "<LOADSURFACE>")
            sys.stdout.write(line)
      else:
         print(f"Ignoring file {file} as it doesn't start with '*Heading'.")

if __name__ == "__main__":
   parameterize_all = True
   make_jobs = True
   files = set()
   amps = set()
   mats = set()
   loadsurface = "fsi"
   ann_model = "model.ann"

   if len(sys.argv) > 1:
      arg = sys.argv[1]
      if arg == "p":
         parameterize_all = True
         make_jobs = False
      elif arg == "j":
         make_jobs = True
         parameterize_all = False
      else:
         parameterize_all = True
         make_jobs = True

      for arg in sys.argv:
         split = arg.split("=",1)
         if len(split) == 2:
            opt = split[0]
            val = split[1]
            if opt == "file":
               files.add(str(val))
            elif opt == "files":
               files.update(eval(val))
            elif opt == "dir":
               files.update(glob.iglob(val + '/*.inp'))
            elif opt == "mat":
               mats.add(str(val))
            elif opt == "mats":
               mats.update(eval(val))
            elif opt == "amp":
               amps.add(str(val))
            elif opt == "amps":
               amps.update([str(v) for v in eval(val)])
            elif opt == "load":
               val = str(val).lower()
               assert val == "fsi" or val == "ann"
               loadsurface = val
            elif opt == "model":
               val = str(val)
               assert val.endswith(".ann")
               ann_model = val


   materials = {"T6":"SMM_AA6016_T6", "T4":"SMM_AA6016_T4", "T7":"SMM_AA6016_T7", "FSI":"FSI_T7"}
   amplitudes = {"10": "Driver10Bar","15": "Driver15Bar"}
   loadsurfaces = {"fsi": "FSISurface", "ann": "ANNSurface"}

   if len(files) == 0:
      files = list(glob.iglob('*.inp'))
   if len(amps) == 0:
      amps = list(amplitudes.keys())
   if len(mats) == 0:
      mats = list(materials.keys())

   if parameterize_all:
      print("Parameterizing input files.")
      parameterize(files)
   
   if make_jobs:
      print("Creating jobfiles.")
      print("Materials:", mats)
      print("Amplitudes:", amps)
      print("LoadSurface:", loadsurface)
      if loadsurface == "ann":
         print("ANN model:", ann_model)
      with open("template.inp","r") as f:
         template = f.read()

      queue_script = open("queue_all.sh","w")
      queue_script.writelines(["#!/bin/bash\n"])

      clean_script = open("clean.sh","w")
      clean_script.writelines(["#!/bin/bash\n","rm -f *.out *.msg *.abq *.cid *.com *.dat *.mdl *.pac *.par *.pes *.pmg *.prt *.res *.sel *.sta *.stt *.src *.exception"])

      post_script = open("post_all.sh","w")
      post_script.writelines(["#!/bin/bash\n"])

      for filename in files:
         with open(filename,"r") as f:
            header = f.readline().strip('\n')
         if header == "*Heading":
            print(f"Model file: {filename}")
            model = os.path.splitext(filename)[0]
            for matk in mats:
               matv = materials[matk]
               for ampk in amps:
                  ampv = amplitudes[ampk]
                  jobname = f"{model}_{matk}_{ampk}.inp"
                  print(f"Generating job {jobname}...")
                  if loadsurface == "ann":
                     queue_script.writelines([f"cp {ann_model} {model}_{matk}_{ampk}.ann\n"])
                     clean_script.writelines([f" {model}_{matk}_{ampk}.ann"])
                  queue_script.writelines([f"sbatch ../jobaba {jobname}\n"])
                  clean_script.writelines([f" {jobname}"])
                  post_script.writelines([f"abaqus python post_plate.py {model}_{matk}_{ampk} {ampv.upper()} &>/dev/null &\n"])
                  with open(jobname,'w') as f:
                     f.write(template.format(mat=matv, amp=ampv, model=model, loadsurface=loadsurfaces[loadsurface]))

      queue_script.close()
      clean_script.close()
      post_script.close()

      os.chmod("queue_all.sh",stat.S_IRWXU)
      os.chmod("clean.sh",stat.S_IRWXU)
      os.chmod("post_all.sh",stat.S_IRWXU)
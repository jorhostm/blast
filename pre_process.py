import fileinput
import sys
import glob

def replacement(file):
   for line in fileinput.input(file, inplace=1):
       line = line.replace("material=AA6016_T4", "material=<MAT>")
       line = line.replace("*Dsload\n", "*Dsload, amplitude=<AMP>\n")
       sys.stdout.write(line)


with open("template.inp","r") as f:
   template = f.read()

materials = {"T6":"SMM_AA6016_T6", "T4":"SMM_AA6016_T4", "T7":"SMM_AA6016_T7"}
amplitudes = {"10": "Driver10Bar","15": "Driver15Bar"}

queue_script = open("queue_all.sh","w")
queue_script.writelines(["#!/bin/bash\n"])

clean_script = open("clean.sh","w")
clean_script.writelines(["#!/bin/bash\n","rm -f *.out *.msg *.abq *.cid *.com *.dat *.mdl *.pac *.par *.pes *.pmg *.prt *.res *.sel *.sta *.stt\n", "rm -f"])

post_script = open("post_all.sh","w")
post_script.writelines(["#!/bin/bash\n"])

print("Preprocess all input files.")
print("Materials:", materials.values())
print("Amplitudes:", amplitudes.values())
print("Searching for model input files...")

for filename in glob.iglob('*.inp'):
   with open(filename,"r") as f:
      header = f.readline().strip('\n')
   if header == "*Heading":
      print(f"Found model file: {filename}")
      print("Parameterizing...")
      replacement(filename)
      model = filename.split('.')[0]
      for matk,matv in materials.items():
         for ampk,ampv in amplitudes.items():
            jobname = f"{model}_{matk}_{ampk}.inp"
            print(f"Generating job {jobname}...")
            queue_script.writelines([f"sbatch ../jobaba {jobname}\n"])
            clean_script.writelines([f" {jobname}"])
            post_script.writelines([f"abaqus python post_plate.py {model}_{matk}_{ampk} {ampv.upper()}\n"])
            with open(jobname,'w') as f:
               f.write(template.format(mat=matv, amp=ampv, model=model))
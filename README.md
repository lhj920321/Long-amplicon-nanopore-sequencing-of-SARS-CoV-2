# Long-amplicon-nanopore-sequencing-of-SARS-CoV-2


## Summary

We developed a multiplex PCR panel for severe acute respiratory syndrome coronavirus 2 with improved coverage evenness, which greatly reduces the requirement of sequencing data amount for MinION.

## Dependencies

- snakemake
- BWA  v0.7.17-r1188
- SAMtools v1.9
- iVar v1.0
- python 2.7

## Repo Contents

scripts: python script and snakemake script for analysis .

## **Bioinformatics analysis**

1. snakemake scripts for alignment of reads  :

    `snakemake -s minION_1k_Flongle_pipeline.snakemake.py -p`

    `snakemake -s minION_1k_pipeline.snakemake.py -p`

    `snakemake -s Miseq_1k_pipeline.snakemake.py -p`

    `snakemake -s Miseq_ARTIC_pipeline.snakemake.py -p`

2. script for sequencing depth statistics   of  all sample from the same batch:

   `python Coverage_distrib.py  -i  $depth_file_from_samtools   -o  $outfile`

3. script for statistics of sequencing coverage of each sample :

   `python Coverage.py  -i   $sample_depthF   -o  $sample_DepthStatF  -f  [ARTIC_Miseq|1k_Miseq|1k_MinION|1k_Flongle]`

4. Calling iSNV and SNP mutations by using script "iSNV_calling.sh" according to https://github.com/generality/iSNV-calling: `bash iSNV_calling.sh 3,4,5`

## Citation

If you use data, results or conclusion from this work, please cite:



## Acknowledgement

This work was supported by grants from the Mega-projects of Science and Technology Research (No. 2018ZX10201001-003 and No. 2018ZX10305410-004). M.N and P.L were supported by the Beijing Nova Program (Z181100006218114 and Z181100006218110).

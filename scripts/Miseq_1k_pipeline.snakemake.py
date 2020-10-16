###################################
#######1k Miseq
#######
###################################

REP_INDEX =["S1","S2","S3","S4","S5","S6","S7","S8"]


rule all:
	input:
	## bwa to ref  genome
		expand("1k_Miseq/bwa/{samp}/{samp}.sorted.bam",samp=REP_INDEX),
	##bam_index
		expand("1k_Miseq/bwa/{samp}/{samp}.sorted.bam.bai",samp=REP_INDEX),
	##bedFile
		#expand("ARTIC-V1_youhua.bed"),
	##refGonm_faidx
		#expand("ref/MN908947.3_genome.fna.fai"),		
	##ivarTrim_Primer_sort
		expand("1k_Miseq/Primer/sorted/{samp}.primertrim.sorted.bam",samp=REP_INDEX),
	##ivarTrim_Primer_sortindex
		expand("1k_Miseq/Primer/sorted/{samp}.primertrim.sorted.bam.bai",samp=REP_INDEX),
			
	##ivarTrim_Primer_sort_depth
		expand("1k_Miseq/ivartrimPrimer_depth/{samp}.primertrim.sorted.depth.txt",samp=REP_INDEX),
	
	##mpileup
		expand("1k_Miseq/Mpileup/{samp}.ivar_trim.mpileup",samp=REP_INDEX),




rule bwa_index:
	input:
		"ref/MN908947.3_genome.fna"
	output:
		"ref/MN908947.3_genome.fna.bwt"
	shell:
		"bwa  index  {input}"

rule bwa_run:
	input:
		"ref/MN908947.3_genome.fna",
		"data/Miseq/{samp}_R1.fastq.gz",
		"data/Miseq/{samp}_R2.fastq.gz",
		"ref/MN908947.3_genome.fna.bwt"
	output:
		temp("1k_Miseq/bwa/{samp}/{samp}.sorted.bam"),
	log:
		"1k_Miseq/bwa/{samp}/{samp}.log"
	shell:
		"bwa  mem  -t  8  {input[0]}  {input[1]}  {input[2]} \
		| samtools sort -@  8 |  samtools view -F 4 -o  {output}   2>{log}  "
 


rule bam_index:
	input:
		"1k_Miseq/bwa/{samp}/{samp}.sorted.bam"
	output:
		temp("1k_Miseq/bwa/{samp}/{samp}.sorted.bam.bai"),
	shell:
		"samtools index  {input}"


rule refGonm_faidx:
	input:
		"ref/MN908947.3_genome.fna"
	output:
		"ref/MN908947.3_genome.fna.fai"
	shell:
		"samtools  faidx  {input}"


rule ivar_trim_Primer:
	input:
		"1k_Miseq/bwa/{samp}/{samp}.sorted.bam",
		"data/primer_panel/1k_primer.bed",
	output:
		temp("1k_Miseq/Primer/{samp}.primertrim.bam"),
		"1k_Miseq/Primer/log/{samp}.primertrim.bam.log"
	params:
		"1k_Miseq/Primer/{samp}.primertrim",
	shell:
		"ivar trim -i {input[0]} -b {input[1]} -p {params[0]}  1>{output[1]}"


rule ivarTrim_Primer_sort:
	input:
		"1k_Miseq/Primer/{samp}.primertrim.bam",
	output:
		"1k_Miseq/Primer/sorted/{samp}.primertrim.sorted.bam"
	shell:
		"samtools sort -@ 6 {input} -o {output}"

rule ivarTrim_Primer_sortindex:
	input:
		"1k_Miseq/Primer/sorted/{samp}.primertrim.sorted.bam",
	output:
		"1k_Miseq/Primer/sorted/{samp}.primertrim.sorted.bam.bai"
	shell:
		"samtools index  {input}"


rule ivarTrim_Primer_depth:
	input:
		"ref/MN908947.3_genome.fna",
		"1k_Miseq/Primer/sorted/{samp}.primertrim.sorted.bam",
	output:
		"1k_Miseq/ivartrimPrimer_depth/{samp}.primertrim.sorted.depth.txt"
	shell:
		"samtools depth -a  -d 80000  --reference {input[0]} {input[1]}  >{output}"



rule mpileup:
	input:
		"ref/MN908947.3_genome.fna",
		"1k_Miseq/Primer/sorted/{samp}.primertrim.sorted.bam",
		"ref/MN908947.3_genome.fna.fai",
		"1k_Miseq/Primer/sorted/{samp}.primertrim.sorted.bam.bai"
	output:
		"1k_Miseq/Mpileup/{samp}.ivar_trim.mpileup"
	log:
		"1k_Miseq/Mpileup/{samp}.ivar_trim.mpileup.log"
	shell:
		"samtools mpileup -A  -d 80000  -B -Q 0 --reference  {input[0]}  {input[1]}  1>{output} 2>{log}"     











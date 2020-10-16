###################################
#######1k minION
#######
###################################


REP_INDEX =["S1","S2","S3","S4","S5","S6","S7","S8"]


rule all:
	input:
	## map to ref  genome
		expand("1k_minION/nglmr/{samp}/{samp}_nglmr2.sorted.bam",samp=REP_INDEX),
	##bam_index
		expand("1k_minION/nglmr/{samp}/{samp}_nglmr2.sorted.bam.bai",samp=REP_INDEX),
	##bam_depth
		expand("1k_minION/nglmr_Depth/{samp}_nglmr2.sorted.bam.depth.txt",samp=REP_INDEX),	
	##mpileup
		expand("1k_minION/Mpileup/{samp}_nglmr2.sorted.bam.mpileup",samp=REP_INDEX),
	##ivarTrim_varscan2
		expand("1k_minION/varscan2/{samp}.varscan2.snp.vcf",samp=REP_INDEX),


rule NGLMR_map:
	input:
		"ref/MN908947.3_genome.fna",
		#"data_7samp/{samp}.fq.gz",
		"data/minION-1k/{samp}.fq.gz",
	output:	
		"1k_minION/nglmr/{samp}/{samp}_nglmr2.sorted.bam",
	log:
		"1k_minION/nglmr/log/{samp}_nglmr2.sorted.bam.log"
	threads:20
	shell:
		"ngmlr -t 6 -r {input[0]}  -q {input[1]} -x ont | samtools sort -@ 6 |  samtools view -F 4 -o  {output}   1>{log}  "   #-t {nglmr_THREADS}

 
#-i <0-1>,  --min-identity <0-1>   Alignments with an identity lower than this threshold will be discarded [0.65]

rule NGLMR_bamsort:
	input:
		"1k_minION/nglmr/{samp}/{samp}_nglmr2.bam",
	output:
		"1k_minION/nglmr/{samp}/{samp}_nglmr2.sorted.bam"
	shell:
		"samtools sort -@ 6 {input} -o {output}"


rule bam_index:
	input:
		"1k_minION/nglmr/{samp}/{samp}_nglmr2.sorted.bam"
	output:
		"1k_minION/nglmr/{samp}/{samp}_nglmr2.sorted.bam.bai"
	shell:
		"samtools index  {input}"


rule bam_depth:
	input:
		"ref/MN908947.3_genome.fna",
		"1k_minION/nglmr/{samp}/{samp}_nglmr2.sorted.bam",
	output:
		"1k_minION/nglmr_Depth/{samp}_nglmr2.sorted.bam.depth.txt"
	shell:
		"samtools depth -a  -d 30000  --reference {input[0]} {input[1]}  >{output}"


rule mpileup:
	input:
		"ref/MN908947.3_genome.fna",
		"1k_minION/nglmr/{samp}/{samp}_nglmr2.sorted.bam",
		"ref/MN908947.3_genome.fna.fai",
		"1k_minION/nglmr/{samp}/{samp}_nglmr2.sorted.bam.bai"
	output:
		"1k_minION/Mpileup/{samp}_nglmr2.sorted.bam.mpileup"
	log:
		"1k_minION/Mpileup/{samp}.ivar_trim.mpileup.log"
	shell:
		"samtools mpileup -A  -d 6000000  -B -Q 0 --reference  {input[0]}  {input[1]}  1>{output} 2>{log}"     

#-Q, --min-BQ INT        skip bases with baseQ/BAQ smaller than INT [13]
#-q, --min-MQ INT        skip alignments with mapQ smaller than INT [0]
#-d, –max-depth 最大测序深度，过滤掉超深度测序的位点






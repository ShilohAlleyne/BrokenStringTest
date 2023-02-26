#Bioinformatics

# Mapping the read to chromosome 21

- Map the reads to chromosome 21 The sequence of chromosome 21 is provided within the same data folder as the fastqs for indexing with bwa prior to mapping. After mapping you will have a bam file per sample.

1. Generate the following directory structure, and put each sample file in the __input__ directory and the reference chromosome file in the __refchr__ directory. 

```
~/BrokenString/
    ├── input/
    ├── refchr/
    ├── asisl/
    ├── tmp/
	    ├── alignments/
	    ├── intervals
		    ├── adjustedintervals/
    ├── output/
        ├── bwa/
```

2. cd to the __tmp__ directory, which we will work from.
3. Index the reference chromosome.

```bash
$ bwa index ../refchr/chr21.fasta
```

4. Map Reads for each sample using BAM MEM and output as a BAM file

```bash
$ bwa mem -t 12 ../refchr/chr21.fasta ../input/Sample1.fastq.gz | samtools sort -o Sample1.bam
```

# Converting the BAM files to BED files

- Convert the bam file to the commonly-utilised and standardised bed file format, for downstream
processing.

1. In the tmp/__intervals__ directory convert the BAM files for each sample to a bed file

```bash
bedtools bamtobed -i ../alignments/Sample1.bam > Sample1.bed
```

# Adjusting Bed file Coordinated to only include break site

- The bed files from step 1b contains the positions of the mapped reads. However as stated in the
introduction, we are only interested in the 5’ end where the break occurred. For each interval in
the bed file, adjust the positions as follows to produce a new bed file.

1. If the read is on the + strand adjust the __end__ position to be __start__ + 1
2. If the read is on the – strand adjust the __start__ position to be __end__ -1

1. From the tmp/intervals/__ajustedintervals__ directory, use the awk command to adjust the positions of each strand.

```bash
awk -v OFS="\t" '{if($6=="+"){print $1,$2,$2+1,$4,$5,$6}else if($6=="-"){print $1,$3-1,$3,$4,$5,$6}}' ../Sample1.bed > adj.Sample1.bed
``` 

- Sample 1 head.

```bash
chr21   299708  299784  NB552753:20:H32L2BGXT:4:13408:2708:15737        60      +
chr21   302489  302565  NB552753:20:H32L2BGXT:3:22507:15059:13335       60      -
chr21   308256  308332  NB552753:20:H32L2BGXT:2:23102:22009:14583       11      +
chr21   316909  316985  NB552753:20:H32L2BGXT:4:13503:4337:14359        29      -
chr21   336045  336121  NB552753:20:H32L2BGXT:3:12603:6062:15527        43      -
chr21   336686  336761  NB552753:20:H32L2BGXT:4:21604:11220:13619       9       -
```

- Adjusted Sample 1 head.

```bash
chr21   299708  299709  NB552753:20:H32L2BGXT:4:13408:2708:15737        60      +
chr21   302564  302565  NB552753:20:H32L2BGXT:3:22507:15059:13335       60      -
chr21   308256  308257  NB552753:20:H32L2BGXT:2:23102:22009:14583       11      +
chr21   316984  316985  NB552753:20:H32L2BGXT:4:13503:4337:14359        29      -
chr21   336120  336121  NB552753:20:H32L2BGXT:3:12603:6062:15527        43      -
chr21   336760  336761  NB552753:20:H32L2BGXT:4:21604:11220:13619       9       -
```

# Intersecting the breaks in with Predicted AsiSI sites

- We provide a bed file of AsiSI cut sites in the human genome (T2T v2.0 release) named chr21_AsiSI_sites.t2t.bed. Intersect this with the break sites in the sample bed from step 1c

1. As we only care about the cut sites on Chr21 we can remove all other chromosomes from the AsiSl file using:

```bash
awk -v OFS="\t" '{if($1=="chr21"){print $1,$2,$3}}' chr21_AsiSI_sites.t2t.bed > chr21.AsiSL.t2t.bed
```

2. In the __output__ directory, intersect the AsiSl cut sites using betools:

```bash
bedtools intersect -a ../asisl/chr21.AsiSL.t2t.bed -b ../tmp/intervals/adjustedintervals/adj.Sample1.bed -c > inter.Sample1.bed
```


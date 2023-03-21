transcription_key = {'A': 'U', 'T': 'A', 'C': 'G', 'G': 'C'}

codon_table = {
    'UUU': 'phe', 'UUC': 'phe', 'UUA': 'leu', 'UUG': 'leu',
    'UCU': 'ser', 'UCC': 'ser', 'UCA': 'ser', 'UCG': 'ser',
    'UAU': 'tyr', 'UAC': 'tyr', 'UAA': 'stop', 'UAG': 'stop',
    'UGU': 'cys', 'UGC': 'cys', 'UGA': 'stop', 'UGG': 'trp',
    'CUU': 'leu', 'CUC': 'leu', 'CUA': 'leu', 'CUG': 'leu',
    'CCU': 'pro', 'CCC': 'pro', 'CCA': 'pro', 'CCG': 'pro',
    'CAU': 'his', 'CAC': 'his', 'CAA': 'gin', 'CAG': 'gin',
    'CGU': 'arg', 'CGC': 'arg', 'CGA': 'arg', 'CGG': 'arg',
    'AUU': 'ile', 'AUC': 'ile', 'AUA': 'ile', 'AUG': 'met',
    'ACU': 'thr', 'ACC': 'thr', 'ACA': 'thr', 'ACG': 'thr',
    'AAU': 'asn', 'AAC': 'asn', 'AAA': 'lys', 'AAG': 'lys',
    'AGU': 'ser', 'AGC': 'ser', 'AGA': 'arg', 'AGG': 'arg',
    'GUU': 'val', 'GUC': 'val', 'GUA': 'val', 'GUG': 'val',
    'GCU': 'ala', 'GCC': 'ala', 'GCA': 'ala', 'GCG': 'ala',
    'GAU': 'asp', 'GAC': 'asp', 'GAA': 'glu', 'GAG': 'glu',
    'GGU': 'gly', 'GGC': 'gly', 'GGA': 'gly', 'GGG': 'gly',
}

amino_acid_table = {
    'phe': 'phenylalanine',
    'leu': 'leucine',
    'ser': 'serine',
    'tyr': 'tyrosine',
    'cys': 'cysteine',
    'trp': 'tryptophan',
    'pro': 'proline',
    'his': 'histidine',
    'gln': 'glutamine',
    'arg': 'arginine',
    'ile': 'isoleucine',
    'met': 'methionine',
    'thr': 'threonine',
    'asn': 'asparagine',
    'lys': 'lysine',
    'val': 'valine',
    'ala': 'alanine',
    'asp': 'aspartate',
    'glu': 'glutamate',
    'gly': 'glycine',
}

dragon_phenotype_table = {
    'serine-glutamate-alanine-valine': 'green scales',
    'serine-glutamate-valine-alanine': 'red scales',
    'proline-histidine-arginine': 'fire breathing',
    'glycine-histidine-arginine': 'acid breathing',
    'threonine-alanine-lysine-leucine': 'yellow belly',
    'isoleucine-alanine-serine-leucine': 'black belly',
    'phenylalanine-glycine-serine': 'four claws',
    'phenylalanine-glycine-proline': 'five claws',
    'histidine-tyrosine-proline-serine': 'straight horns',
    'serine-tyrosine-proline-valine': 'curved horns',
    'glutamate-lysine-histidine-cysteine': 'pointed tail',
    'proline-lysine-histidine-cysteine': 'rounded tail',
    'threonine-tryptophan-histidine': 'ice-blue eyes',
    'threonine-alanine-histidine': 'glowing-orange eyes',
    'glycine-tyrosine-alanine': 'feathered wings',
    'alanine-tyrosine-glycine': 'scaly wings',
    'cysteine-cysteine-isoleucine': 'pointed spikes on the spine',
    'histidine-leucine-isoleucine': 'rounded spikes on the spine',
}

def transcribe(sequence: str) -> str:
    return ''.join(transcription_key[nucleotide] for nucleotide in sequence.upper())

def split_codons(codons: str) -> list[str]:
    return [codons[i:i+3] for i in range(0, len(codons), 3)]

def translate(codons: str) -> str:
    amino_acids = [codon_table[codon] for codon in split_codons(codons)]
    genes = []
    translating_gene = False
    for amino_acid in amino_acids:
        if amino_acid == 'met':
            translating_gene = True
            current_gene = []
        elif amino_acid == 'stop':
            translating_gene = False
            genes.append(current_gene)
        elif translating_gene:
            current_gene.append(amino_acid)
    return genes

def get_amino_acid_sequences(genes: list[list[str]]) -> list[list[str]]:
    return [[amino_acid_table[amino_acid] for amino_acid in gene] for gene in genes]

def get_phenotypes(amino_acid_sequences) -> list[str]:
    return [dragon_phenotype_table['-'.join(amino_acid_sequence)] for amino_acid_sequence in amino_acid_sequences]

if __name__ == '__main__':
    sequence = input("Enter DNA sequence 3'-5': ").strip().replace(' ', '')
    codons = transcribe(sequence)
    genes = translate(codons)
    amino_acid_sequences = get_amino_acid_sequences(genes)
    phenotypes = get_phenotypes(amino_acid_sequences)
    print('='*40, 'Result', '='*40)
    print("mRNA codons: [5'-"+' '.join(split_codons(codons))+"-3']")
    print('Genes: ['+' '.join('-'.join(gene) for gene in genes)+']')
    print('Amino acid sequences:\n'+'\n'.join('   '+'-'.join(gene) for gene in amino_acid_sequences))
    print('Phenotypes: ['+(', '.join(phenotypes))+']')
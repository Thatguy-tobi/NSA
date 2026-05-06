from flask import Flask, render_template, request

app = Flask(__name__)

CODON_DICT = {
    'UUU': 'Phe', 'UUC': 'Phe', 'UUA': 'Leu', 'UUG': 'Leu', 'CUU': 'Leu', 'CUC': 'Leu', 'CUA': 'Leu', 'CUG': 'Leu',
    'AUU': 'Ile', 'AUC': 'Ile', 'AUA': 'Ile', 'AUG': 'Met', 'GUU': 'Val', 'GUC': 'Val', 'GUA': 'Val', 'GUG': 'Val',
    'UCU': 'Ser', 'UCC': 'Ser', 'UCA': 'Ser', 'UCG': 'Ser', 'CCU': 'Pro', 'CCC': 'Pro', 'CCA': 'Pro', 'CCG': 'Pro',
    'ACU': 'Thr', 'ACC': 'Thr', 'ACA': 'Thr', 'ACG': 'Thr', 'GCU': 'Ala', 'GCC': 'Ala', 'GCA': 'Ala', 'GCG': 'Ala',
    'UAU': 'Tyr', 'UAC': 'Tyr', 'UAA': 'Stop', 'UAG': 'Stop', 'CAU': 'His', 'CAC': 'His', 'CAA': 'Gln', 'CAG': 'Gln',
    'AAU': 'Asn', 'AAC': 'Asn', 'AAA': 'Lys', 'AAG': 'Lys', 'GAU': 'Asp', 'GAC': 'Asp', 'GAA': 'Glu', 'GAG': 'Glu',
    'UGU': 'Cys', 'UGC': 'Cys', 'UGA': 'Stop', 'UGG': 'Trp', 'CGU': 'Arg', 'CGC': 'Arg', 'CGA': 'Arg', 'CGG': 'Arg',
    'AGU': 'Ser', 'AGC': 'Ser', 'AGA': 'Arg', 'AGG': 'Arg', 'GGU': 'Gly', 'GGC': 'Gly', 'GGA': 'Gly', 'GGG': 'Gly'
}
AMINO_1_LETTER = {
    'Phe': 'F', 'Leu': 'L', 'Ile': 'I', 'Met': 'M', 'Val': 'V', 'Ser': 'S', 'Pro': 'P', 'Thr': 'T', 'Ala': 'A', 'Tyr': 'Y',
    'His': 'H', 'Gln': 'Q', 'Asn': 'N', 'Lys': 'K', 'Asp': 'D', 'Glu': 'E', 'Cys': 'C', 'Trp': 'W', 'Arg': 'R', 'Gly': 'G', 'Stop': '*'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    data = {}
    if request.method == 'POST':
        seq = request.form.get('seq').strip().upper()
        if 'U' in seq:
            data['type'] = 'RNA'
            comp = "".join([{'A':'U', 'U':'A', 'C':'G', 'G':'C'}.get(b, b) for b in seq])
            data['comp'] = comp
            data['rev_comp'] = comp[::-1]
        else:
            data['type'] = 'DNA'
            mrna = "".join([{'A':'U', 'T':'A', 'C':'G', 'G':'C'}.get(b, b) for b in seq])
            trna = "".join([{'A':'U', 'U':'A', 'C':'G', 'G':'C'}.get(b, b) for b in mrna])
            amino_3, amino_1 = [], []
            for i in range(0, len(mrna) - 2, 3):
                codon = mrna[i:i+3]
                aa = CODON_DICT.get(codon, "?")
                amino_3.append(aa)
                amino_1.append(AMINO_1_LETTER.get(aa, "?"))
            data.update({'mrna': mrna, 'trna': trna, 'amino_3': "-".join(amino_3), 'amino_1': "".join(amino_1)})
            
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, port=5002) # Running on port 5002
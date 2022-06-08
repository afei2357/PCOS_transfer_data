import sys
def change_sola_to_guoke(infile,outfile):
    i = 0
    with open(infile,'r') as fh,open(outfile,'w') as wh:
        i += 1
        if i %1000 == 0:
            print('reading for ' +str(i)+'  line,please wait')

        header = '#CHROM\tPOS\tID\tREF\tINFO'
        for line in fh:
            line =line.strip()
            if  not line :
                continue 
            #print(line)
            if line.startswith('gxid'):
                rs_name = line.split('\t',3)[-1]
                wh.write(header+'\t'+rs_name+'\n')
                continue
            gxid,chromosome,position,rs_lst = line.split('\t',3)
            wh.write(chromosome+'\t'+position+'\t'+gxid+'\t'+'REF'+'\t'+'INFO'+'\t'+rs_lst+'\n')

if __name__ == '__main__':
    infile = sys.argv[1]
    outfile = sys.argv[2]
    #readfile('20190822_2s_Final_report.txt','testout.txt')
    change_sola_to_guoke(infile,outfile)
    print('finish')


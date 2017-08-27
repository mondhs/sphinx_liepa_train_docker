#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus

    find -iname '*.txt' -print0 | xargs -0  sed -i -e 's/programį/programą/g' 
find -iname '*.txt' -print0 | xargs -0  sed -i -e 's/tolesną/tolesnę/g' 
find -iname '*.txt' -print0 | xargs -0  sed -i -e 's/ankstesną/ankstesnę/g' 
find -iname '*.txt' -print0 | xargs -0  sed -i -e 's/pabaigį/pabaigą/g' 
find -iname '*.txt' -print0 | xargs -0  sed -i -e 's/paskyrį/paskyrą/g' 
find -iname '*.txt' -print0 | xargs -0  sed -i -e 's/centriną/centrinę/g' 
find -iname '*.txt' -print0 | xargs -0  sed -i -e 's/tąsk/tęsk/g' 
find -iname '*.txt' -print0 | xargs -0  sed -i -e 's/paveikslį/paveikslą/g' 
find -iname '*.txt' -print0 | xargs -0  sed -i -e 's/abipusą/abipusę/g' 
find -iname '*.txt' -print0 | xargs -0  sed -i -e 's/abipusą/abipusę/g'
find -iname '*.txt' -print0 | xargs -0  sed -i -e 's/kairiną/kairinę/g' 
find -iname '*.txt' -print0 | xargs -0  sed -i -e 's/ėjunk/įjunk/g' 




'''
import glob,os,re
import itertools
import subprocess
import logging
import codecs
from multiprocessing import Pool


logging.basicConfig(filename='/tmp/liepa/02_extract_dict.log',level=logging.DEBUG)
#logger = logging.getLogger()
#logger.addHandler(logging.FileHandler('/tmp/liepa/extract_dict.log', encoding='utf-8'))


wav_dir = "../liepa_audio"
env_type = "train"

#dest_unkown_dir = "../wav_unknown"
#dest_minus_dir = "../wav_minus"
#dest_coding_dir = "../wav_coding"
#dest_short_dir = "../wav_short"

def checkSpellingNot(text):
    return []

def checkSpelling(text):
    '''
    Sils:
    <sil>
    <sil+pause>
    <sil+breathin>
    <sil+breathout>
    <sil+smack>
    <sil+other>
    <sil+chair>
    <sil+cough>
    <sil+ingest>
    <sil+stomach>
    <sil+page>
    '''
    text = text.replace("<sil>", "")
    text = text.replace("<sil+pause>", "")
    text = text.replace("<sil+breathin>", "")
    text = text.replace("<sil+breathout>", "")
    text = text.replace("<sil+smack>", "")
    text = text.replace("<sil+other>", "")
    text = text.replace("<sil+chair>", "")
    text = text.replace("<sil+cough>", "")
    text = text.replace("<sil+ingest>", "")
    text = text.replace("<sil+stomach>", "")
    text = text.replace("<sil+page>", "")
    
    text = text.replace("<sil+page>", "")
    

    cmd = "echo \"" +text + "\" | hunspell -p liepa_hunspell.dic -i utf-8 -d lt_LT"
    #print cmd
    p = None
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    except:
        print "ERROR in spellchecker: {}".format(text)
        return ["ERROR in spellchecker"]

    result, err = p.communicate()
    if err:
        print "ERROR: {}; ({})".format(err,text)
        return [err]

    wordIssues = []

    if result:
        #print result
        for line in result.split("\n"):
            #print (line, re.search('& ([\wąčęėįšųūž]+) \d \d: ([\wąčęėįšųūž]+)', line))
            match = re.search('& ([\wąčęėįšųūž]+) \d+ \d+: ([\wąčęėįšųūž]+)', line)
            if not match is None:
                #print ("test",line, match.group(1).lower() != match.group(2).lower())
                if match.group(1).lower() != match.group(2).lower():
                    print "Spell issue: "+ line
                    wordIssues.append( match.group(1).lower() )
    #print text
    return wordIssues

def force_decode(string, codecs=[ 'utf-8', 'utf-16-le', 'windows-1257']):
    pattern = ur'[\wąčęėįšųūž]+'
    lt_letter =  r'[àáæèëðàøûþ]+'
    unicode_pattern = re.compile(pattern,  re.IGNORECASE)
    lt_letter_re = re.compile(lt_letter,  re.IGNORECASE)
    #print '>'*120
    #print string 

    
    for i in codecs:
        #print i + ">>>"
        try:
            decoded = string.decode(i)
            decoded = decoded.lower()
            testEncode = decoded.encode('utf-8')
            #print u"testEncode %s : %s === %s" % (i, testEncode, decoded)
            #print u'Unicode : %s' % (u', '.join(unicode_pattern.findall(testEncode)))

            if unicode_pattern.search(testEncode) is not None:
                #if lt_letter_re.search(testEncode) is not None:
                #    logging.error("Not possible detect coding as unkown char exists! %s" % ([string]))              
                #    continue
                     #print 'return : %s' % (testEncode)
                return testEncode.strip()
        except:
            #print "Exception in user code:"
            #print '-'*60
            #traceback.print_exc(file=sys.stdout)
            #print '-'*60
            pass

    logging.error("Not possible detect coding! %s" % ([string]))
    raise Exception("Not possible detect coding! " + string)     


def moveWavAndText(in_txt_file,dest_path):
    '''
    Move txt and wav file to marked dir
    '''
    baseName = os.path.basename(in_txt_file)
    try:
        os.makedirs(dest_path)
    except OSError:
        if not os.path.isdir(dest_path):
            raise
    os.rename(in_txt_file, os.path.join(dest_path,baseName))
    wav_base_file = baseName.replace('.txt', '.wav')
    wav_file = in_txt_file.replace('.txt', '.wav')
    os.rename(wav_file, os.path.join(dest_path,wav_base_file))
    print "move {} to {}".format(in_txt_file, dest_path) 


def processCorpusDir(corpus_dir):
    contentMap = {}
    wordsSet = set([])
    #dest_unknown_path = os.path.join(dest_unkown_dir,corpus_dir)
    #dest_minus_path = os.path.join(dest_minus_dir,corpus_dir)
    #dest_coding_path = os.path.join(dest_coding_dir,corpus_dir)
    #dest_short_path = os.path.join(dest_coding_dir,corpus_dir)
    print (corpus_dir)
    read_files = glob.glob( wav_dir +"/"+env_type+ "/" + corpus_dir + "/*.txt")
    if len(read_files) == 0:
        #os.rmdir( wav_dir + "/" + corpus_dir)
        logging.warning(',%s, Deleting dir %s',  wav_dir + "/error.txt",corpus_dir)
        return 
    #print "read_files: {}".format( read_files )
    for in_file in read_files:
        #print "in_file: " + in_file
        with open(in_file, "rb") as infile:
            line = infile.read()
            #if os.path.getsize(in_file) < 10:
            #    logging.warning(',%s,too short %i, %s', in_file, os.path.getsize(in_file), line)
            #    moveWavAndText(in_file,dest_short_path)
            #    continue;
            #try:
            #    line = force_decode(line).replace(u"\ufeff", "")
            #except:
            #    logging.error("Not possible detect coding! %s in %s" % ([line], in_file))
            #    moveWavAndText(in_file,dest_coding_path)
            #    continue;
            #line = line.encode('utf-8').replace(u"\ufeff", "")
            line = line.lower()
            #<s></s>
            line = line.replace("_tyla", " <sil> ")
            line = re.sub('[_\-]{1}\s*pauze'," <sil+pause>", line)#pause could be written in multiple ways
            line = line.replace("_ikvepimas", " <sil+breathin> ");#should be breath
            line = line.replace("_iskvepimas", " <sil+breathout> ");#should be breath
            line = line.replace("_cepsejimas", " <sil+smack> ");
            line = line.replace("_garsas", " <sil+other> ");
            line = line.replace("_kede", " <sil+chair> ");
            line = line.replace("_kosejimas", " <sil+cough> ");
            line = line.replace("_nurijimas", " <sil+ingest> ");
            line = line.replace("_pilvas", " <sil+stomach> ");
            line = line.replace("_puslapis", " <sil+page> ");

            #line = re.sub('_([\wąčęėįšųū])',"<sil> \g<1>", line, re.UNICODE)
            #line = re.sub('(<sil>\s+)+'," <sil> ", line, re.UNICODE)#multi silences
            #line = re.sub('^\s*<sil>\s+',"", line) #extra silence in front
            #line = re.sub('^\s*<silpause>\s+',"", line) #extra silence in front            
            #line = re.sub('\s*<sil>$',"", line)#extra silence in end
            #line = re.sub('\s*<silpause>$',"", line)#extra silence in end            
            line = re.sub(r'\r',r' ',line)
            line = re.sub(r'\n',r' ',line)
            line = re.sub(r'\s{2,}',r" ",line)
            line = re.sub('\?',"", line)
            line = re.sub('c2',"č", line)
            line = re.sub('s2',"š", line)
            line = re.sub('z2',"ž", line)
            line = re.sub('u1',"ų", line)
            line = re.sub('u4',"ū", line)
            line = re.sub('a1',"ą", line)
            line = re.sub('a2',"a", line)#???
            line = re.sub('e1',"ę", line)
            line = re.sub('i1',"į", line)
            line = re.sub('e3',"ė", line)
            
            line = line.replace("buo", "buvo")
            line = line.replace(" letuv", " lietuv")
            line = line.replace("lituvos", "lietuvos")
            line = line.replace("dešim ", "dešimt ")
            line = line.replace("zdeš", "sdeš")
            line = line.replace("joe ", "joje ")
            line = line.replace("ye ", "yje ")
            
            line = line.replace(" vienaz ", " vienas ")
            line = line.replace(" ira ", " yra ")
            line = line.replace(" laiška ", " laišką ")
            line = line.replace(" grįšti ", " grįžti ")
            line = line.replace(" koplystulpiai ", " koplytstulpiai ")

            

            

            

            
            
            
            #print line
            #if not re.search('_', line) is None or not re.search('-', line) is None:
#                print "skiping. due _: " + in_file
                #logging.warning(',%s, unkown underscore: %s', in_file, line)
#                moveWavAndText(in_file,dest_minus_path)
 #               continue;


            line = re.sub('_',"", line)
            line = re.sub('\-',"", line)


            #spellIssue = checkSpellingNot(line)
            #if spellIssue:
                #logging.warning(',%s, spelling issue: %s', in_file, "; ".join(spellIssue))
                #raise Exception(" has unexepcted - %s (%s)" % (line, in_file))
                #moveWavAndText(in_file,dest_unknown_path)
                #continue;


            wordList = line.split(' ')


            wordsSet.update(wordList)

            base_name = os.path.basename(in_file)
            contentMap[os.path.splitext(base_name)[0]] = line

    trainMap = contentMap

    print [corpus_dir, ": ", len(trainMap)]
    if len(trainMap) == 0:
        #raise Exception("Not possible detect list! " + corpus_dir)
        logging.warning(',%s, List is empty for dir %s', wav_dir+"/error.txt", corpus_dir)

    
    with codecs.open("../target/_"+corpus_dir+"_"+env_type+".transcription", "w",encoding='utf8') as outfile:
        for key, value in trainMap.iteritems():
            out_line = "<s> {line} </s> ({file_name})".format(line=value,file_name=key)
            outfile.write(out_line.decode("utf-8") + "\n")

    with codecs.open("../target/_"+corpus_dir+"_"+env_type+".fileids", "w",encoding='utf8') as outfile:
        for key, value in trainMap.iteritems():
            outfile.write(corpus_dir +"/" + key + "\n")

    #print wordsSet
    with codecs.open("../target/_"+corpus_dir+"_word.txt", 'w',encoding='utf8') as outfile:
        for item in set(wordsSet):
            outfile.write(item.decode("utf-8")+"\n")

#######################################################################################################################
## Main codec
#######################################################################################################################

def main():
    processingDirs = []
    for corpus_dir in os.listdir(wav_dir +"/" + env_type):
        #if not corpus_dir == "D265":
        #    continue
        #processingDirs.append(corpus_dir);
        processCorpusDir(corpus_dir)
    pool = Pool(10)
    
    for corpus_dir in processingDirs:
        try:
            result = pool.apply_async(processCorpusDir, args=(corpus_dir,))
        except KeyboardInterrupt:
            print "Caught KeyboardInterrupt, terminating workers"
            pool.terminate()
            pool.wait()
            break
    pool.close()
    pool.join()


############################################################

if __name__ == "__main__":
    main()

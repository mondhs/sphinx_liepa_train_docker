#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
'''
import glob,os, re
import codecs
import subprocess
import logging
from multiprocessing import Pool
import itertools
import shutil



logging.basicConfig(filename='/tmp/liepa/01_transform_files.log',level=logging.DEBUG)

# coruptedFileSet = set(line.strip() for line in open('corupted_files.txt'))

src_dir = "../mounted-liepa"
#src_dir = "/home/mgreibus/tmp/mounted-liepa/Testavimui"
dest_dir = "../wav"
dest_short_dir = "../wav_short"
dest_coding_dir = "../wav_coding"
# two formats should support: Z184Vk_021 S180Mj_040_43 
fileFromatRegeExp = re.compile('([A-Za-z\d]+)_([\dA-Za-z\_]+)')
count_dir = len(os.listdir(src_dir))
narsytuvas_dirs = ("Z030", "Z031", "Z032", "Z033", "Z034", "Z035", "Z036", "Z037", "Z038", "Z039");
valdytuvas_dirs = ("Z025", "Z026", "Z027", "Z028", "Z029");
pazintuvas_dirs = ("Z065", "Z066", "Z067", "Z068");
all_dirs = ()

active_dirs = all_dirs   


def copyToUtfFile(sourcePath, destinationPath):
    lt_letter =  ur'[àáæèëðàøûþõ˛�\d\(\)]+'
    lt_letter_re = re.compile(lt_letter, re.UNICODE)
    #print "copyToUtfFile: " + sourcePath
    cmd = "cat " +sourcePath + " | enconv - | sed 's/.*/\L&/'"
    #print cmd 
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result, err = p.communicate()
    resultUtf = ""
    try:
        resultUtf = result.decode("utf-8")
        #print "AAAAAAAAAAAAAAAAAAAAAa" + resultUtf
    except:
        print "enconv failed. result: '"+  result +"'. path: "  + sourcePath
    
    if not resultUtf:
        #print "try iconv" 
        cmd = "cat " +sourcePath + " | iconv -f WINDOWS-1257 -tUTF8  | sed 's/.*/\L&/'"
        #print cmd 
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        result, err = p.communicate()
        resultUtf = result.decode("utf-8")
        print u"iconv result: '"+  resultUtf +"'. sourcePath: "  + sourcePath + " . destinationPath: " + destinationPath
        

    if not resultUtf:
        #shutil.copy(sourcePath, os.path.join(dest_coding_dir))
        #logging.warning(",%s,coding undetectible! %s", sourcePath, result)
        raise Exception("Not possible detect coding! %s " % (result))
        #return False
        
    
    try:  
        if lt_letter_re.search(resultUtf) is not None:
            logging.warning(",%s,coding before fix: %s", sourcePath, resultUtf)
            raise Exception("Not possible detect coding! %s " % (result))
            #resultUtf = resultUtf.replace(u"à",u"į")
            #resultUtf = resultUtf.replace(u"á",u"ą")
            #resultUtf = resultUtf.replace(u"æ",u"ę")
            #resultUtf = resultUtf.replace(u"è",u"č")
            #resultUtf = resultUtf.replace(u"ë",u"ė")
            #resultUtf = resultUtf.replace(u"ð",u"š")
            #resultUtf = resultUtf.replace(u"ø",u"ų")
            #resultUtf = resultUtf.replace(u"û",u"ū")
            #resultUtf = resultUtf.replace(u"þ",u"ž")
            #resultUtf = resultUtf.replace(u"˛",u"ž")
            #resultUtf = resultUtf.replace(u"�",u"ž")
            
        resultUtf = resultUtf.lower()
            #logging.warning(",%s,coding fixed ignore! %s", sourcePath, resultUtf)
            #raise Exception("Not possible detect coding! %s " % (resultUtf))
        
        with codecs.open(destinationPath, mode='w',encoding='utf-8') as destinationFile:
            destinationFile.write(resultUtf);
            return True
    except Exception, e:
        logging.warning(",%s,coding undetectible! %s", sourcePath, result)
        print "Cannot write: '"+  resultUtf +"'. sourcePath: "  + sourcePath + " . destinationPath: " + destinationPath
        shutil.copy(sourcePath, os.path.join(dest_coding_dir))
        raise# Exception("Not possible detect coding! %s " % (result))
        #os.remove(destinationPath)
        return False
    return False

    #with codecs.open(destinationPath, mode='w',encoding='utf-8') as destinationFile:
    #    with codecs.open(sourcePath) as sourceFile:
    #        for line in sourceFile:
    #            try:
    #                line = force_decode(line)
    #            except:
    #                #logging.error("Not possible detect coding! %s in %s" % ([line], in_file))
    #                raise Exception("Not possible detect coding! %s in %s" % ([line], sourcePath))
    #            #print line
    #            destinationFile.write(line);

def copyCorpusDir(speak_dir):
    speaker_path = os.path.join(src_dir, speak_dir)
    print "Start: " + speaker_path
    for corpus_dir in os.listdir(speaker_path):
            if active_dirs and not corpus_dir in active_dirs:
                print "Skiping not active dir: " + corpus_dir
                continue
            #if not corpus_dir.startswith("S"):
            #    print "Skiping: " + corpus_dir
            #    continue
            print "{}".format(speak_dir, corpus_dir)
            #os.makedirs (dest_dir + "/" + corpus_dir)
            read_files = glob.glob(src_dir + "/" + speak_dir + "/"  + corpus_dir + "/*.wav")
            for wav_file in read_files:
                #print wav_file
                baseName = os.path.basename(wav_file)
                baseName = os.path.splitext(baseName)[0]
                txt_file = os.path.join(src_dir, speak_dir, corpus_dir, baseName+".txt")
                txtA_file = os.path.join(src_dir, speak_dir, corpus_dir, baseName+".txtA")
                lab_file = os.path.join(src_dir, speak_dir, corpus_dir, baseName+".lab")
                
                if os.path.getsize(wav_file) < 40000:
                    logging.warning(',%s,too short %i', wav_file, os.path.getsize(wav_file))
                    continue
                
                replaceName = corpus_dir+"_"+fileFromatRegeExp.sub(r'\2-\1', baseName)+"_"+speak_dir
                speaker_seq_code = ""
                try:
                    speaker_seq_code = fileFromatRegeExp.match(baseName).group(1)
                except:
                    logging.warning(',%s,unable to parse ', wav_file)
                    print "skipping. Not possible parse!" + wav_file
                    continue

                if os.path.isfile(txt_file) and os.path.getsize(txt_file) > 0:
                    #do nothing as file exists
                    pass
                    #if txt does note exists mayhe exists txtA file with ANSI encription
                elif os.path.isfile(txtA_file) and os.path.getsize(txtA_file) > 0:
                    txt_file = txtA_file
                elif os.path.isfile(lab_file) and os.path.getsize(lab_file) > 0:
                    txt_file = lab_file
                else:
                    logging.warning(',%s,%s', txt_file, 'lab, txt or txtA file not exists')
                    continue
                current_dest_dir = dest_dir
                    


                wav_speaker_dir = os.path.join(current_dest_dir, speak_dir.replace(" ", ""))
                dstWavfile = os.path.join(wav_speaker_dir, replaceName + ".wav")
                dstTxtfile = os.path.join(wav_speaker_dir, replaceName + ".txt")

                try:
                    os.makedirs(wav_speaker_dir)
                except OSError:
                    if not os.path.isdir(wav_speaker_dir):
                        raise

                if not copyToUtfFile(txt_file, dstTxtfile):
                    continue
    #             print  (wav_file,dstWavfile)
    #           sox  wav_file -b16 dstWavfile rate 16000 dither -s
                cmd = "sox  \""+wav_file+"\" -b16 \"" +dstWavfile+ "\" rate 16000 dither -s"
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                result, err = p.communicate()
                if err:
                    logging.warning(',%s,resampling issue: %s', baseName, err)
                    continue
                
    print "End: " + speaker_path


############################################################

if __name__ == "__main__":
    processingDirs = []

    for idx,speak_dir in enumerate(os.listdir(src_dir)):
        #print "Speaker: %s (%i of %i)" % (speak_dir, idx, count_dir)
        speaker_path_test = os.path.join(src_dir, speak_dir)
        if os.path.isfile(speaker_path_test):
            print "skipping. Not dir!" + speak_dir
            continue
        #if not speak_dir == "D514":
        #    continue
        #processingDirs.append(speak_dir);
        copyCorpusDir(speak_dir)

    pool = Pool(20)
    try:
        #pool.map(copyCorpusDir, itertools.islice(processingDirs, 1))
        for speaker_path in processingDirs:
            result = pool.apply_async(copyCorpusDir, args=(speaker_path,))
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        print "Caught KeyboardInterrupt, terminating workers"
        pool.terminate()
        pool.join()


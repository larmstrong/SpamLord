"""
This program was adapted from the Stanford NLP class SpamLord homework assignment.
    The code has been rewritten and the data modified, nevertheless
    please do not make this code or the data public.
This base version has no patterns, but has two patterns suggested in comments
    in order to get you started .
"""
import sys
import os
import re
import pprint

"""
TODO
For Part 1 of our assignment, add to these two lists of patterns to match
examples of obscured email addresses and phone numbers in the text.
For optional Part 3, you may need to add other lists of patterns.
"""
# email .edu patterns

# each regular expression pattern should have exactly two sets of parentheses.
#   the first parenthesis should be around the someone part
#   the second parenthesis should be around the somewhere part
#   in an email address whose standard form is someone@somewhere.edu
epatterns = []
## Pattern #1 --------------------------------------------------
# epatterns.append(r'([\w]+)@([\w]+)\.edu')                     ## Iteration 1.1
# epatterns.append(r'([\w\.]+)@([\w\.]+)\.edu')                 ## Iteration 1.2
# epatterns.append(r'([\w\.]+)\ ?@\ ?([\w\.]+)\.edu')           ## Iteration 1.3	[ulman]
# epatterns.append(r'([\w\.]+)\ *@\ *([\w\.]+)\.edu')           ## Iteration 1.4  [dabo]
epatterns.append(r'([\w\.]+)\ *@\ *([\w\.]+)\.[eE][dD][uU]')    ## Iteration 1.5 [cheriton]
## Pattern #2 --------------------------------------------------
# epatterns.append(r'([\w\.]+)\s+at\s+([\w\.]+)\.edu')          ## Iteration 2.1 [lam]
epatterns.append(r'mail:\s+([\w\.]+)\s+at\s+([\w\.]+)\.edu')    ## [removes jure: "Server at..."]
## Pattern #3 --------------------------------------------------
epatterns.append(r'([\w\.]+)\ ?<at symbol>\ ?([\w\.]+)\.edu')   ## [manning]
## Pattern #4
epatterns.append(r'([\w\.]+)&#x40;([\w\.]+)\.edu')              ## [levoy]
## Pattern #5
epatterns.append(r'([\w\.]+)<del>@([\w\.]+)\.edu')              ## [latombe]
## Pattern #6
epatterns.append(r'([\w\.]+)\s+at\s+<![^>]+>\s+([\w\.]+)\s+<![^>]+>\s+dot\s+<![^>]+>\s+edu') ## [vladen]
## Pattern #7
epatterns.append(r'([\w\.]+)\ ?[aA][tT]\ ?([\w\.]+)\ [dD][oO][tT] edu')
## Pattern #8
#epatterns.append(r'([\w\.]+)\ [\(\w\"\ ]+?@([\w\.]+).edu[\"\)]+')
epatterns.append(r'([\w\.]+)\ [\(\w\"\ ]+@([\w\.]+).edu[\"\)]+')        ## [teresa in ouster]
## Pattern #9
epatterns.append(r'([\w\.]+)\ \(followed by \&ldquo;@([\w\.]+)\.edu')   ## [ouster in ouster]
## Pattern #10
epatterns.append(r'(\w+) WHERE (\w+) DOM')
## Pattern #11
epatterns.append(r'(\w+)@(\w+).com')


# phone patterns
# each regular expression pattern should have exactly three sets of parentheses.
#   the first parenthesis should be around the area code part XXX
#   the second parenthesis should be around the exchange part YYY
#   the third parenthesis should be around the number part ZZZZ
#   in a phone number whose standard form is XXX-YYY-ZZZZ
ppatterns = []
ppatterns.append(r'(\d{3})[-\s](\d{3})[-\s](\d{4})')
ppatterns.append(r'\((\d{3})\)\s*(\d{3})-(\d{4})')
ppatterns.append(r'\[(\d{3})\]\s(\d{3})-(\d{4})')


#ppatterns.append('(\d{3})-(\d{3})-(\d{4})')

def preprocess (line) :
    """
    preprocess - Preprocesses a single line of text before standard pattern 
      maching is invoked. Inside this preprocessing, more complex patterns are
      sought and are replaced with a simpler canonical form that standard 
      pattern matching will find.

    :param line: Current line of input file text.
    :type line: Character string
    :return: An e-mail address in canonical form if an address was found that
      matches one of the non-standard patterns. Otherwise, the original line of
      text is returned.
    :rtype: Character string.
    """
    #--------------------------------------------------------------------------
    # Extended Pattern 1
    r1 = re.compile(r'([\w\.]+) at (((([\w\.]+)|dot|dt)\s)+)(edu|com)\b')
    p1 = r1.findall(line)
    if len(p1) > 0 : 
        user = p1[0][0]
        dotsymbol = p1[0][4]
        subdomain = p1[0][1].replace(
            " " + dotsymbol + " ", ".") if dotsymbol in ['dot', 'dt'] else p1[0][1]
        tld = p1[0][5]
        result1 = f'{user}@{subdomain}{tld}'
        result1 = result1.replace(' ', '.')
        return(result1)
    #--------------------------------------------------------------------------
    # Extended Pattern 2
    r2 = re.compile(r"obfuscate\('([\w\.]+)','([\w\.]+)'\)")
    p2 = r2.findall(line)
    if len(p2) > 0:
        user = p2[0][1]
        domain = p2[0][0]
        result2 = f'{user}@{domain}'
        # print(p2)
        return(result2)
    #--------------------------------------------------------------------------
    # Extended Pattern 3
    r3 = re.compile(r'([\w\.]+) at ((\w+;)+(\w+))')
    p3 = r3.findall(line)
    if len(p3) > 0:
        user = p3[0][0]
        domain = p3[0][1].replace(';', '.')
        result3 = f'{user}@{domain}'
        # print(p3)
        return result3
    #--------------------------------------------------------------------------
    # Extended Pattern 4
    r4 = re.compile(r'((((\w)-)+)@-(((\w)-)+)\.((-(\w))+))')
    p4 = r4.findall(line)
    if len(p4) > 0:
        result4 = p4[0][0].replace('-','')
        # print(p4)
        # print(result4)
        return result4
    #--------------------------------------------------------------------------
    # No preprocessing patterns found
    return line


""" 
This function takes in a filename along with the file object and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

TODO
For Part 3, if you have added other lists, you should add
additional for loops that match the patterns in those lists
and produce correctly formatted results to append to the res list.
"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    for line in f:
        # you may modify the line, using something like substitution
        #    before applying the patterns
        # UPDATE #1
        line = preprocess(line)

        # email pattern list
        for epat in epatterns:
            # each epat has 2 sets of parentheses so each match will have 2 items in a list
            matches = re.findall(epat,line)
            for m in matches:
                # string formatting operator % takes elements of list m
                #   and inserts them in place of each %s in the result string
                # email has form  someone@somewhere.edu
                #email = '%s@%s.edu' % m
                # email = '{}@{}.edu'.format(m[0],m[1])
                # UPDATE #2
                # Allow .com email addresses.
                email = f'{m[0]}@{m[1]}.{"com" if line.endswith(".com") else "edu"}'
                res.append((name,'e',email))

        # phone pattern list
        for ppat in ppatterns:
            # each ppat has 3 sets of parentheses so each match will have 3 items in a list
            matches = re.findall(ppat,line)
            for m in matches:
                # phone number has form  areacode-exchange-number
                #phone = '%s-%s-%s' % m
                phone = '{}-{}-{}'.format(m[0],m[1],m[2])
                res.append((name,'p',phone))
    return res

"""
You should not edit this function.
"""
def process_dir(data_path):
    # save complete list of candidates
    guess_list = []
    # save list of filenames
    fname_list = []

    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        fname_list.append(fname)
        path = os.path.join(data_path,fname)
        f = open(path,'r', encoding='latin-1')
        # get all the candidates for this file
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list, fname_list

"""
You should not edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r', encoding='latin-1')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not edit this function.
Given a list of guessed contacts and gold contacts, this function
    computes the intersection and set differences, to compute the true
    positives, false positives and false negatives. 
It also takes a dictionary that gives the guesses for each filename, 
    which can be used for information about false positives. 
Importantly, it converts all of the values to lower case before comparing.
"""
def score(guess_list, gold_list, fname_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    # for each file name, put the golds from that file in a dict
    gold_dict = {}
    for fname in fname_list:
        gold_dict[fname] = [gold for gold in gold_list if fname == gold[0]]

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)

    print ('True Positives (%d): ' % len(tp))
    # print all true positives
    pp.pprint(tp)
    print ('False Positives (%d): ' % len(fp))
    # for each false positive, print it and the list of gold for debugging
    for item in fp:
        fp_name = item[0]
        pp.pprint(item)
        fp_list = gold_dict[fp_name]
        for gold in fp_list:
            s = pprint.pformat(gold)
            print('   gold: ', s)
    print ('False Negatives (%d): ' % len(fn))
    # print all false negatives
    pp.pprint(fn)
    print ('Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn)))

"""
You should not edit this function.
It takes in the string path to the data directory and the gold file
"""
def main(data_path, gold_path):
    guess_list, fname_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list, fname_list)

"""
commandline interface assumes that you are in the directory containing "data" folder
It then processes each file within that data folder and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    print ('Assuming ContactFinder.py called in directory with data folder')
    main('data/dev', 'data/devGOLD')

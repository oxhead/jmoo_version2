import xml.etree.cElementTree as ET
from jmoo_core import *
from collections import defaultdict
from utility import *


#----------------------------------------------------------------------
def stat(list):
    def median(xs, is_sorted=False):
        """
        Return the median of the integer-indexed object passed in. To save sorting
        time, the client can pass in is_sorted=True to skip the sorting step.
        """
        # implementation from http://stackoverflow.com/a/10482734/3408454
        if not is_sorted:
            xs = sorted(xs)
        n = len(xs)
        return xs[n // 2] if n % 2 else (xs[n // 2] + xs[n // 2 - 1]) / 2


    def mean(xs):
        "Returns the mean of the iterable argument."
        return sum(xs) / len(xs)


    def iqr(xs):
        xs = sorted(xs)
        n = len(xs)
        return xs[int(n * .75)] - xs[int(n * .25)]

    out = "Median: %2.3f "% median(list)
    out += " IQR: %2.3f" % iqr(list)

    print out

    return out

def parseXML(xml_file, tag):
    """
    Parse XML with ElementTree
    """

    tree = ET.ElementTree(file=xml_file)
    experiment = tree.getroot()
    result = "Experiment: \n"
    if tag == "charts":
        import os
        os.remove(DEFECT_PREDICT_PREFIX + "DefectPredict_chart.txt")

    for problem in experiment:
        result += "Problem Name: " + str(problem.attrib["name"])+"\n"
        if problem.tag == "Problem":
            scores_pd = defaultdict(list)
            scores_pf = defaultdict(list)
            scores_prec = defaultdict(list)
            scores_eval = defaultdict(list)
            dpd = []
            dpf =[]
            dprec = []
            for algorithm in problem:
                result +="Algorithm: "+ str(algorithm.attrib["name"])+"\n"
                numeval = []
                runtime = []
                pd = []
                pf =[]
                prec = []
                for run in algorithm:
                    for summary in run:
                        for junk in summary:
                            if junk.tag == "NumEvals":
                                numeval.append(float(junk.text))
                            elif junk.tag == "RunTime":
                                runtime.append(float(junk.text))
                            elif junk.tag == "Testing":
                                for i in junk:
                                    if i.tag == "pd":
                                        pd.append(float(i.text))
                                    elif i.tag == "pf":
                                        pf.append(float(i.text))
                                    elif i.tag == "prec":
                                        prec.append(float(i.text))
                            elif junk.tag == "Default":
                                for i in junk:
                                    if i.tag == "pd":
                                        dpd.append(float(i.text))
                                    elif i.tag == "pf":
                                        dpf.append(float(i.text))
                                    elif i.tag == "prec":
                                        dprec.append(float(i.text))

                if tag == "stats":
                    result += "NumEval: "+ str(stat(numeval))+"\n"
                    result += "RunTime: "+ str(stat(runtime))+"\n"
                    result += "pd: "+ str(stat(pd))+"\n"
                    result += "pf: "+ str(stat(pf))+"\n"
                    result += "prec: "+ str(stat(prec))+"\n"
                    result += "Default pd: "+ str(stat(dpd))+"\n"
                    result += "Default pf: "+ str(stat(dpf))+"\n"
                    result += "Default prec: "+ str(stat(dprec))+"\n\n\n"

                if tag == "charts":
                    scores_pd[str(algorithm.attrib["name"])] = []
                    scores_pf[str(algorithm.attrib["name"])] = []
                    scores_prec[str(algorithm.attrib["name"])] = []
                    scores_eval[str(algorithm.attrib["name"])] = []
                    scores_pd[str(algorithm.attrib["name"])] = pd
                    scores_pf[str(algorithm.attrib["name"])] = pf
                    scores_prec[str(algorithm.attrib["name"])] = prec
                    scores_eval[str(algorithm.attrib["name"])] = numeval

            if tag == "charts":
                scores_pd["default"] = []
                scores_pf["default"] = []
                scores_prec["default"] = []
                scores_pd["default"] = dpd
                scores_pf["default"] = dpf
                scores_prec["default"] = dprec
                import sys
                f = open(DEFECT_PREDICT_PREFIX + "DefectPredict_chart.txt", 'a+')
                sys.stdout = f
                print "Problem Name: ", str(problem.attrib["name"])
                print "Algorithm: ", str(algorithm.attrib["name"])
                names = ["PD", "PF", "PREC", "EVALS"]
                for i,x in enumerate([scores_pd, scores_pf, scores_prec, scores_eval]):
                    print "Features: ", names[i]
                    callrdivdemo(x)
                sys.stdout = sys.__stdout__
                f.close()




    if tag == "stats":
        f = open(DEFECT_PREDICT_PREFIX + "DefectPredict_report.txt", "w")
        f.write(result)
        f.close()
        print result
    print "Report saved at : ", DEFECT_PREDICT_PREFIX



    # ----------------------------------------------------------------------
    if __name__ == "__main__":
        parseXML("test_xml.xml")
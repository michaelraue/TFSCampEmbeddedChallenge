import string
import re
import sys
from xml.sax.saxutils import escape

def createXML(testData, outputfilepath):
    template_testsuites = string.Template("""<?xml version="1.0" encoding="UTF-8"?>
<testsuite>
${successtestcases}
${failingtestcases}
</testsuite>
""")

    template_successtestcase = string.Template("""  <testcase classname="${classname}" name="${name}"/>""")
    template_failingtestcase = string.Template("""  <testcase classname="${classname}" name="${name}">
    <failure>${message}</failure>
  </testcase>""")

    contents_successtestcase = [template_successtestcase.substitute(id=id, classname=classname, name=name, result=result) for (id, classname, name, result, message) in testData if result != "Failed"]
    contents_failingtestcase = [template_failingtestcase.substitute(id=id, classname=classname, name=name, result=result, message=message) for (id, classname, name, result, message) in testData if result == "Failed"]
    result = template_testsuites.substitute(successtestcases='\n'.join(contents_successtestcase), failingtestcases='\n'.join(contents_failingtestcase))
    #print (result)
    with open(outputfilepath, 'w') as outputfile:
      outputfile.write(result)

    print("Finished converting data, result written to " + outputfilepath)

def readFileContent(inputfilepath, outputfile):
    TestBlock = False
    print ("      Reading testresults from file " + inputfilepath)
    with open(inputfilepath, 'r') as inputfile:
      testData = []

      for line in inputfile:
        line = line.replace("FAIL:", "FAIL->").strip().replace("[FAILED]", "Failed").replace("[PASSED]", "Passed")
        #print (line)
        if line.strip() == "" and TestBlock == True:
          TestBlock = False
          print ("      End of testing block")
        if TestBlock == True:
          parts = re.split(":|\t", line)
          print ("      Found Test Case: " + str(parts))
          if (len(parts) > 4):
            testData.append((parts[1], parts[0], parts[2], parts[4], parts[3]))
          else:
            testData.append((parts[1], parts[0], parts[2], parts[3], ''))
        if line.__contains__("Testing...") == True:
          TestBlock = True
          print ("      Found testing block - start reading test cases")
      print ("      Found " + str(len(testData)) + " Test Cases, exporting them now to output file")
      createXML(testData, outputfile)

print ("#################################################################################################")
print ("# Test Results Parser 1.0 by @tschissler")
print ("#################################################################################################")
print ()
print ("This tool is parsing test results from PlatformIO unit tests and converting into NUnit format")
print ()
print ("Usage: python TestResultsParser.py <inputfile> <outputfile>")
print ()

print (sys.argv)
if (len(sys.argv) != 3):
  print ("Wrong number of parameters [" + str(len(sys.argv)) + "], expecting 2 parameters")
  sys.exit([-1])

print ("   -- Starting conversion process --")
readFileContent(sys.argv[1], sys.argv[2])






#<?xml version="1.0" encoding="UTF-8"?>
#<testsuites disabled="" errors="" failures="" name="" tests="" time="">
#    <testsuite disabled="" errors="" failures="" hostname="" id=""
#               name="" package="" skipped="" tests="" time="" timestamp="">
#        <properties>
#            <property name="" value=""/>
#        </properties>
#        <testcase assertions="" classname="" name="" status="" time="">
#            <skipped/>
#            <error message="" type=""/>
#            <failure message="" type=""/>
#            <system-out/>
#            <system-err/>
#        </testcase>
#        <system-out/>
#        <system-err/>
#    </testsuite>
#</testsuites>

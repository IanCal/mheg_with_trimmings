import sys
import getopt

def helpMessage():
    print  """
    A pre-processor which creates MHEG-5 code from a higher level language. See http://github.com/IanCal/mheg_with_trimmings
    Usage:
        -h --help Displays this message
        -i --input The input file
        -o --output The output file
    Example:
        python parseFile.py --input sourcefile --output sourcefile.mheg
        """

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["help", "input","output"])
        print opts, args
    except getopt.GetoptError:
        helpMessage()
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])

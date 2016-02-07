''' Implementation of scalar and vector types.
Used in the Loopers and for plotting.
'''

# Standard imports
import abc

# Translation of short types to ROOT C types
cStringTypeDict = {
    'b': 'UChar_t',
    'S': 'Short_t',
    's': 'UShort_t',
    'I': 'Int_t',
    'i': 'UInt_t',
    'F': 'Float_t',
    'D': 'Double_t',
    'L': 'Long64_t',
    'l': 'ULong64_t',
    'O': 'Bool_t',
}
# reversed
shortTypeDict = {v: k for k, v in cStringTypeDict.items()}

# defaults
defaultCTypeDict = {
    'b': '0',
    'S': '-1',
    's': '0',
    'I': '-1',
    'i': '0',
    'F': 'TMath::QuietNaN()',
    'D': 'TMath::QuietNaN()',
    'L': '-1',
    'l': '-1',
    'O': '0',
}

allTypes  = set(cStringTypeDict.keys())
allCTypes = set(cStringTypeDict.values())

class Variable( object ):
    __metaclass__ = abc.ABCMeta
   
    @abc.abstractmethod
    def __init__(self):
        return 

    @classmethod
    def fromString(cls, string):
        try:
            return VectorType.fromString(string)
        except ( ValueError, AssertionError ):
            return ScalarType.fromString(string)

class ScalarType( Variable ):

    def __init__( self, name, tp, filler = None, defaultCString = None):
        ''' Initialize variable. 
            tp: shortcut for ROOT type (b/s/S/I/i/F/D/L/l/O) or the corresponding C ROOT types, 
            'filler': function that fills the variable,
            'defaultCString': value the variable will be initialized with in a string representing  C code (!), 
                i.e. '-1' or 'TMath::QuietNaN()'
        '''
        self.name = name

        assert tp in allTypes.union( allCTypes ), "Type %r not known"%tp
        # translate type to short form
        self.tp = tp if tp in allTypes else shortTypeDict[tp]

        self.filler = filler

        # store default
        self.defaultCString = defaultCString if defaultCString is not None else defaultCTypeDict[self.tp]

    @classmethod
    def fromString(cls, string):
        '''Create scalar variable from name/type
        '''
        if not type(string)==type(""): raise ValueError( "Expected string got '%r'"%string )
        string = string.replace(' ', '')
        assert string.count('/')==1, "Could not parse string '%s', format is 'name/type'."%string

            
        name, tp = string.split('/')
        return cls( name = name, tp = tp)

    def __str__(self):
        if self.filler:
            return "%s(scalar, type: %s, filler)" %(self. name, self.tp)
        else:
            return "%s(scalar, type: %s)" %(self. name, self.tp)

class VectorType( Variable ):

    def __init__( self, name, components, filler = None, nMax = None):
        ''' Initialize variable.
            'components': list of ScalarType 
            'filler': function that fills the vector,
            default is the value the variable will be initialized with,
            nMax is the maximal length of the vector in memory (if not specified: 100)
        '''
        self.name = name
        # Scalar components
        self.components = [ ScalarType.fromString(x) if type(x)==type("") else x for x in components ]

        self.filler = filler
        
        self.nMax = int(nMax) if nMax is not None else 100

    @classmethod
    def fromString(cls, string):
        '''Create vector variable from name[c1/type1,c2/type2,...]
        '''
        if not type(string)==type(""): raise ValueError( "Expected string got '%r'"%string )
        string = string.replace(' ', '')

        name_ = string[:string.find("[")]

        ts_ = string[string.find("[")+1:string.find("]")]
        componentStrings_ = ts_.split(',')

        components = [ ScalarType.fromString(s) for s in componentStrings_]

#        except:
#            raise ValueError("Could not interpret string '%s')"%string)
        return cls( name = name_, components = components, nMax = None, filler = None)

    def __str__(self):
        return "%s(vector[%s], filler: %r, components: %s )" %(self. name, self.nMax, bool(self.filler), ",".join(str(c) for c in self.components) )
''' A stack of samples (not plots).
Must be a list of lists.
'''

from RootTools.tools.Sample import Sample

class Stack ( list ):
        
    def __init__(self, *stackList):

        # change [[...], X, [...] ...]  to [[...], [X], [...], ...]
        stackList = [ s if type(s)==type([]) else [s] for s in stackList]


        super(Stack, self).__init__( stackList )

        # Check the input. LBYL.
        for s in stackList:
            if not type(s)==type([]) or not all(isinstance(p, Sample) for p in s):
                raise ValueError("Stack should be a list of lists of Samples. Got '%r'."%( stackList ) )


    @staticmethod
    def cut( cut ):
        for s in self:
            for p in s:
                p.cut( cut ) 
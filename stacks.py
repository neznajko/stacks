#! /usr/bin/env python3
from random import randint
from heapq import ( heappush as heepush,
                    heappop  as heepop )
import numpy as np
########################################################
# oK the stack is FILO, so the first in will be last out
# and if we have only one stack than the only strategy
# is pushing new containers if they have smaller removal
# times than the stack's top container, be cos the crane
# is operating above the depot only. If there are moar
# stacks than we can delegate one of them as buffer and
# keep all other stacks sorted using the buffer as 
# temporary area.
class Stack( list ):

    def look( self, key ):
        """ the stack is sorted non increasingly, so 
        we find the first position j: key > self[j].
        E.g. if the current stack is like so:
        90 70 65 50 50 30 20 20 15 13
         0  1  2  3  4  5  6  7  8  9
        ,and key is 17 it should spit 8. To insert that
        cont. ve need total fai möz. 2 pops, 3 pushes.
        """
        # Binary Search 
        l, u = 0, len( self ) - 1
        while l <= u:
            m = ( l + u ) >> 1
            if self[m] >= key: l = m + 1
            else:              u = m - 1
        # that's:
        return l
    
########################################################
class Depot:

    def __init__( self, x, y, z ):
        self.capa = z; # stacks' maximum capacity
        # delegate 0th as buffer
        n = x * y - 1
        self.stacks = [Stack() for j in range( n )]
    
    def insert( self, key ):
        ''' don't moov '''
        nofpops = []
        # - Popping vs breakdance?
        # - I think popping!
        for stk in self.stacks:
            if len( stk ) == self.capa: continue # full
            nofpops.append( len( stk ) - stk.look( key ))
        if not nofpops: return -1, -1
        # pick the stack with minimum pops
        nofpops = np.array( nofpops )
        j = np.argmin( nofpops ) # that's
        stk = self.stacks[j] # shortcut
        i = len( stk ) - nofpops[j] # insert position
        stk.insert( i, key )
        # return ( stack index, crane moves ) tuple
        return j, ( nofpops[j] << 1 ) + 1

    def popping( self, j ): self.stacks[j].pop()

if __name__ == '__main__':

    depot = Depot( 2, 2, 5 )
    maxtime = 12
    heep = []
    for t in range( 1, maxtime ):
        d = randint( 1, 5 ) # depot time
        r = t + d           # removal time
        j, m = depot.insert( r )
        if j == -1:
            print( "depot full" )
            continue
        heepush( heep, ( r, j ))
        while heep[0][0] == t:
            print( "Watch out!" )
            _, j = heepop( heep )
            depot.stacks[j].pop()
        print( depot.stacks )

########################################################
# log:

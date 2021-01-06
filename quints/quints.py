import re
import os
import sys

from datetime import datetime

################################################################################
#                                                                              #
#                                  Classes                                     #
#                                                                              #
################################################################################

##
# Represents a fully assembled Quint.  Has a copy of its own key (presumably the
# lowest timestamp and seq) for tracking.  If valid(), should have size() == 5.
class Quint(object):
    def __init__(self, quint_key):
        self.key = quint_key
        self.filenames = []

    def add(self, filename):
        self.filenames.append(filename)

    def size(self):
        return len(self.filenames)

    def valid(self):
        return self.size() == 5

    def __str__(self):
        return "Quint %s (size %d)" % (str(self.key), self.size())

##
# Represents a unique key identifying one Quint, using the sequence number
# and one timestamp (presumably the lowest) for the whole quint.  
class QuintKey(object):
    def __init__(self, parsed_filename):
        self.seq = parsed_filename.seq
        self.timestamp = parsed_filename.timestamp

    ## 
    # Convenience string representation for debugging.  String version takes
    # the form "YYYYMMDDhhmmssfff-seq", so should be chronologically sortable.
    def __str__(self):
        sortable_timestamp = self.timestamp.strftime("%y%m%d%H%M%S%f")
        return "%s-%05d" % (sortable_timestamp, self.seq)

    ## required to use QuintKey as dict key
    def __hash__(self):
        return hash(str(self))

    ## two QuintKeys match if they have the same seq and timestamps within 60sec
    def __eq__(self, other):
        if other is None:
            return False

        # QuintKeys must have the same sequence
        if self.seq != other.seq:
            return False

        # QuintKeys must be within 60 seconds
        if abs(self.timstamp - other.timestamp).total_seconds() > 60:
            return False

        return True


## Given a filename, parses out all the bits and pieces.
class ParsedFilename(object):
    def __init__(self, filename):
        self.valid = False

        m = re.match(r'^([^-]+)-(\d+)_(\d+)-(\d+)', filename, re.IGNORECASE)
        if not m:
            print("failed to parse filename: %s" % filename)
            return

        self.camera = m.groups(1)
        self.seq    = m.groups(4)

        # parse timestamp into a single datetime object
        timestamp   = m.groups(2)
        millisec    = m.groups(3)
        full_timestamp = "%s%03d" % (timestamp, millisec)
        self.timestamp = datetime.strptime(full_timestamp, "%y%m%d%H%M%S%f")

        self.valid = True

    ## convenience for debugging
    def __str__(self):
        return "[ParsedFilename: cam %s, seq %d, timestamp %s]" % (self.camera, self.seq, self.timestamp)

################################################################################
#                                                                              #
#                           QuintProcessor Application                         #
#                                                                              #
################################################################################

class QuintProcessor(object):

    def __init__(self):
        self.seqs = {}          # a map of seq to array of QuintKeys using that seq, ex: { 123 -> [ QuintKeyA, QuintKeyB ], 124 -> [ QuintKeyC ] }
        self.quints = {}        # a map of all QuintKeys to their respective Quints

    def load(self, pathname):
        # generate the list of filenames
        filenames = os.listdir(pathname)

        # parse each filename and associate with its Quint
        for filename in sorted(filenames):
            parsed = ParsedFilename(filename)
            if not parsed.valid:
                print("can't parse filename: %s" % filename)
                continue

            # Associate this filename with a quint (either an existing one, or
            # a new one).
            quint_key = None

            # check if we've ever seen this sequence before
            if not parsed.seq in self.seqs:
                # We've never seen this sequence, so it must be a new quint.
                # Make the new quint key and register it under the sequence.
                quint_key = QuintKey(parsed)
                self.seqs[parsed.seq] = [ quint_key ]
                print("first time seeing seq %d, created new quint_key %s" % (parsed.seq, str(quint_key)))
            else:
                # We have seen this sequence before.  Check if this filename
                # should belong to an existing quint.
                quint_key = self.find_quint_key(parsed)

                if not quint_key:
                    # This seems to be a new quint, so make a key and register
                    # it to the current sequence.
                    quint_key = QuintKey(parsed)
                    self.seqs[parsed.seq].append(quint_key)
                    print("starting new quint_key %s under repeat seq %d" % (str(quint_key), parsed.seq))
                else:
                    print("matched parsed file to existing quint_key %s" % str(quint_key))

            # at this point we should definitely have a quint_key
            if not quint_key:
                raise Exception("Logic error: missing quint_key for filename %s" % filename)

            # either create or grab the quint for this key
            if quint_key in self.quints:
                quint = self.quints[quint_key]
                print("using existing Quint %s" % str(quint))
            else:
                quint = Quint(quint_key)
                print("creating new Quint %s" % str(quint))

            # add this file to the quint
            quint.add(filename)
            print("added to Quint %s: %s" % (str(quint), filename))
                
    def find_quint_key(self, parsed_filename):
        seq = parsed_filename.seq
        if not seq in self.seqs:
            return

        # make a temporary quint_key from this filename
        this_key = QuintKey(parsed_filename)

        # check if this key matches any quints already on file
        for quint_key in self.seqs[seq]:
            if quint_key == this_key:
                # the keys match (same seq, "close" timestamp)
                return quint_key

        # apparently we didn't match any existing quint key,
        # so return nothing to indicate failure

    def process_quints(self):
        for quint_key in sorted(self.quints):
            quint = self.quints[quint_key]
            if not quint.valid():
                print("skipping invalid quint: %s" % str(quint))
                continue
            self.process_quint(quint)

    def process_quint(self):
        print("processing quint %s" % str(quint))
        for filename in quint.filenames:
            print("  processing file %s" % filename)

################################################################################
#                                                                              #
#                                  main()                                      #
#                                                                              #
################################################################################

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: quints.py directory_path")
        sys.exit(1)
    qp = QuintProcessor()
    qp.load(sys.argv[1])
    qp.process_quints()

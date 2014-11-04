################################################################################
#                                                                              #
#   This file is part of the Bibolamazi Project.                               #
#   Copyright (C) 2013 by Philippe Faist                                       #
#   philippe.faist@bluewin.ch                                                  #
#                                                                              #
#   Bibolamazi is free software: you can redistribute it and/or modify         #
#   it under the terms of the GNU General Public License as published by       #
#   the Free Software Foundation, either version 3 of the License, or          #
#   (at your option) any later version.                                        #
#                                                                              #
#   Bibolamazi is distributed in the hope that it will be useful,              #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#   GNU General Public License for more details.                               #
#                                                                              #
#   You should have received a copy of the GNU General Public License          #
#   along with Bibolamazi.  If not, see <http://www.gnu.org/licenses/>.        #
#                                                                              #
################################################################################


from pybtex.utils import OrderedCaseInsensitiveDict

from core.bibfilter import BibFilter, BibFilterError, CommaStrList;
from core.blogger import logger;

from .util import auxfile

HELP_AUTHOR = u"""\
only_used filter by Philippe Faist, (C) 2013, GPL 3+
"""

HELP_DESC = u"""\
Filter that keeps only BibTeX entries which are referenced in the LaTeX document
"""

HELP_TEXT = u"""
This filter detects which citations you have referenced in a LaTeX document, and keeps
only those bibtex entries; the rest is discarded. (Of course this doesn't modify your
original sources.)

You need to specify the latex job name, i.e. the base file name of your LaTeX document. 
If, for example your LaTeX document is named `mydocument.tex', then you should provide the
option `-sJobname=mydocument'. The file `mydocument.aux' should exist, i.e. you should run
(Pdf)LaTeX before running bibolamazi. In case the `mydocument.aux' file is not in the same
directory as the bibolamazi file, you may specify an additional directory (or several
additional directories) in which to search while looking for the aux file with the option
`-sSearchDirs=...'.

WARNING: This filter doesn't integrate very well with the `duplicates' filter. If you
would also like to use the `duplicates' filter, you must invoke the `only_used' filter
*BEFORE* the `duplicates' filter. Otherwise, you'll most likely get missing bibtex
entries. But then, be warned that no merging of the duplicates will be possible as the
duplicates may have been removed by the `only_used' filter. Bottom line: avoid using both
filters at the same time. In the future hopefully I'll fix this.

"""



class OnlyUsedFilter(BibFilter):

    helpauthor = HELP_AUTHOR
    helpdescription = HELP_DESC
    helptext = HELP_TEXT

    def __init__(self, jobname, search_dirs=[]):
        """OnlyUsedFilter constructor.

        Arguments:
          - jobname: the base name of the latex file. Will search for jobname.aux and look for
              \citation{..} commands as they are generated by latex.
          - search_dirs(CommaStrList): the .aux file will be searched for in this list of
              directories; separate directories with commas e.g. 'path/to/dir1,path/to/dir2'
              (escape commas and backslashes with a backslash)
        """

        BibFilter.__init__(self);

        self.jobname = jobname
        self.search_dirs = CommaStrList(search_dirs)

        if (not self.search_dirs):
            self.search_dirs = ['.', '_cleanlatexfiles'] # also for my cleanlatex utility :)

        logger.debug('only_used: jobname=%r' % (jobname,));


    def name(self):
        return "only_used"

    def getRunningMessage(self):
        return u"only_used: filtering entries ..."

    
    def action(self):
        return BibFilter.BIB_FILTER_BIBOLAMAZIFILE;


    def filter_bibolamazifile(self, bibolamazifile):

        logger.debug("Getting list of used citations from %s.aux." %(self.jobname))

        citations = auxfile.get_all_auxfile_citations(self.jobname, bibolamazifile, self.name(), self.search_dirs,
                                                      return_set=True);

        logger.longdebug("set of citations: %r"%(citations))


        bibdata = bibolamazifile.bibliographyData()
        
        newentries = OrderedCaseInsensitiveDict()

        for key,entry in bibdata.entries.iteritems():
            if key in citations:
                newentries[key] = entry

        logger.longdebug("the new database has entries %r" %(newentries.keys()))

        bibolamazifile.setEntries(newentries.iteritems())

        return


def bibolamazi_filter_class():
    return OnlyUsedFilter;



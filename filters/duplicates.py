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


import os
import os.path
import re
import codecs


from pybtex.database import BibliographyData;


from core.bibfilter import BibFilter, BibFilterError;
from core.blogger import logger;

import arxiv # getArXivInfo()



BIBALIAS_HEADER = ur"""
%
% NOTE: THIS FILE WAS AUTOMATICALLY GENERATED BY bibolamazi SCRIPT!
%       ANY CHANGES WILL BE LOST!
%
% You should include this file in your main LaTeX file with the command
%
%   \input{####DUP_FILE_NAME####}
%
% in your document preamble.
%



%
% The following will define the command \bibalias{<alias>}{<source>}, which will make
% the command \cite[..]{<alias>} the same as doing \cite[..]{<source>}.
%
% This code has been copied and adapted from
%    http://tex.stackexchange.com/questions/37233/
%

\makeatletter
% \bibalias{<alias>}{<source>} makes \cite{<alias>} equivalent to \cite{<source>}
\newcommand\bibalias[2]{%
  \@namedef{bibali@#1}{#2}%
}

\newtoks\biba@toks
\let\bibalias@oldcite\cite
\renewcommand\cite[2][]{%
  \biba@toks{\bibalias@oldcite#1}%
  \def\biba@comma{}%
  \def\biba@all{}%
  \@for\biba@one:=#2\do{%
    \@ifundefined{bibali@\biba@one}{%
      \edef\biba@all{\biba@all\biba@comma\biba@one}%
    }{%
      \PackageInfo{bibalias}{%
        Replacing citation `\biba@one' with `\@nameuse{bibali@\biba@one}'
      }%
      \edef\biba@all{\biba@all\biba@comma\@nameuse{bibali@\biba@one}}%
    }%
    \def\biba@comma{,}%
  }%
  \edef\biba@tmp{\the\biba@toks{\biba@all}}%
  \biba@tmp
}
\makeatother


%
% Now, declare all the alias keys.
%

"""



DUPL_WARN_TOP = """

    DUPLICATE ENTRIES WARNING
    -------------------------

"""

DUPL_WARN_ENTRY = """\
    %(alias)-25s \tis a duplicate of  %(orig)s
"""

DUPL_WARN_BOTTOM = """
    -------------------------

"""




HELP_AUTHOR = u"""\
Duplicates filter by Philippe Faist, (C) 2013, GPL 3+
"""

HELP_DESC = u"""\
Filter that detects duplicate entries and produces rules to make one entry an alias of the other.
"""

HELP_TEXT = u"""
This filter works by writing a LaTeX file to a specified location (via the
`dupfile' option) which contains the commands needed to define the bibtex
aliases.

Note that the dupfile option is mandatory in order to create the file with
duplicate definitions. You need to specify a file to write to. You may do this
with `--dupfile=dupfile.tex' or with `-sDupfile=dupfile.tex'.

In your main LaTeX document, you need to add the following command in the
preamble:

  \input{yourdupfile.tex}

where of couse yourdupfile.tex is the file that you specified to this filter.

Alternatively, if you just set the warn flag on, then a duplicate file is not
created (unless the dupfile option is given), and a warning is displayed for
each duplicate found.
"""


class DuplicatesFilter(BibFilter):

    helpauthor = HELP_AUTHOR
    helpdescription = HELP_DESC
    helptext = HELP_TEXT


    def __init__(self, dupfile=None, warn=False):
        """DuplicatesFilter constructor.

        *dupfile: the name of a file to write latex code for defining duplicates to. This file
                  will be overwritten!!
        *warn: if this flag is set, dupfile is not mandatory, and a warning is issued for every
               duplicate entry found in the database.
        """

        BibFilter.__init__(self);

        self.dupfile = dupfile
        self.warn = warn

        if (not self.dupfile and not self.warn):
            logger.warning("bibolamazi duplicates filter: no action will be taken as neither -sDupfile or"+
                           " -dWarn are given!")

        logger.debug('duplicates: dupfile=%r, warn=%r' % (dupfile, warn));


    def name(self):
        return "duplicates processing"

    def getRunningMessage(self):
        if (self.dupfile):
            return (u"processing duplicate entries. Don't forget to insert `\\include{%s}' in "
                    "your LaTeX file!" %(self.dupfile) );
        return u"processing duplicate entries (warning will be generated only)"
    

    def action(self):
        return BibFilter.BIB_FILTER_BIBFILTERFILE;


    def compare_entries_same(self, a, b):
        apers = a.persons.get('author',[]);
        bpers = b.persons.get('author',[]);
        if (len(apers) != len(bpers)):
            return False

        def getlast(pers):
            # join last names
            last = pers.last()[-1].upper();
            # additionally, remove any special LaTeX chars which may be written differently.
            last = re.sub(r'\\([a-zA-Z]+|.)', '', last);
            last = re.sub(r'(\{|\})', '', last);
            return last;

        for k in range(len(apers)):
            if (not (getlast(apers[k]) == getlast(bpers[k]))):
                return False

        def compare_neq_fld(x, y, fld, filt=lambda x: x):
            return filt(x.get(fld, y.get(fld))) != filt(y.get(fld, x.get(fld))) ;

        # authors are the same. check year
        if (compare_neq_fld(a.fields, b.fields, 'year')):
            return False
        if (compare_neq_fld(a.fields, b.fields, 'month')):
            return False

        if (compare_neq_fld(a.fields, b.fields, 'doi')):
            return False

        arxiv_a = arxiv.getArXivInfo(a);
        arxiv_b = arxiv.getArXivInfo(b);
        if (arxiv_a and arxiv_b and
            'arxivid' in arxiv_a and 'arxivid' in arxiv_b and
            arxiv_a['arxivid'] != arxiv_b['arxivid']):
            return False

        # if they have different notes, then they're different entries
        if ( compare_neq_fld(a.fields, b.fields, 'note',
                             lambda x: (arxiv.stripArXivInfoInNote(x) if x else "")) ):
            return False

        # create abbreviations of the journals by keeping only the uppercase letters
        j_abbrev_a = re.sub('[^A-Z]', '', a.fields.get('journal', ''));
        j_abbrev_b = re.sub('[^A-Z]', '', b.fields.get('journal', ''));
        if (j_abbrev_a != j_abbrev_b):
            return False

        # well at this point the publications are pretty much duplicates
        return True
        


    def filter_bibfilterfile(self, bibfilterfile):
        #
        # bibdata is a pybtex.database.BibliographyData object
        #

        bibdata = bibfilterfile.bibliographydata();

        duplicates = [];

        newbibdata = BibliographyData();

        for (key, entry) in bibdata.entries.iteritems():
            #
            # search the newbibdata object, in case this entry already exists.
            #
            logger.longdebug('inspecting new entry %s ...', key);
            is_duplicate_of = None
            for (nkey, nentry) in newbibdata.entries.iteritems():
                if self.compare_entries_same(entry, nentry):
                    logger.longdebug('    ... matches existing entry %s!', nkey);
                    is_duplicate_of = nkey;
                    break

            #
            # if it's a duplicate
            #
            if is_duplicate_of is not None:
                dup = (key, is_duplicate_of)
                duplicates.append(dup);
            else:
                newbibdata.add_entry(key, entry);

        # output duplicates to the duplicates file

        if (self.dupfile):
            ### TODO: do a minimum checks before overwriting:
            ###       * has a previously-written dupfile header
            ###       * compare modif. time w/ some reference?
            ###       * add --force-overwrite flag?
            dupstrlist = [];
            with codecs.open(os.path.join(bibfilterfile.fdir(),self.dupfile), 'w', 'utf-8') as dupf:
                dupf.write(re.sub(r'####DUP_FILE_NAME####', self.dupfile, BIBALIAS_HEADER, 1));
                for (dupalias, duporiginal) in duplicates:
                    dupf.write((r'\bibalias{%s}{%s}' % (dupalias, duporiginal)) + "\n");
                    dupstrlist.append("\t%s is an alias of %s" % (dupalias,duporiginal)) ;

                dupf.write('\n\n');

            # issue debug message
            logger.debug("wrote duplicates to file: \n" + "\n".join(dupstrlist));

        if (self.warn):
            logger.warning(DUPL_WARN_TOP  +
                           "".join([ DUPL_WARN_ENTRY % { 'alias': dupalias,
                                                         'orig': duporiginal
                                                         }
                                     for (dupalias, duporiginal) in duplicates
                                     ])  +
                           DUPL_WARN_BOTTOM);


        bibfilterfile.setBibliographyData(newbibdata);

        return


def get_class():
    return DuplicatesFilter;


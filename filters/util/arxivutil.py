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

import arxiv2bib
import re
from urllib2 import URLError, HTTPError

from core.blogger import logger



# --- code to detect arXiv info ---

_RX_BEFORE = r'(?:\s*([;,]?\s*)|\b|\s+|^)'
_RX_AFTER = r'(?:\s*[;,]?\s*|$)'

_RX_ARXIVID_PURE = r'(?P<arxivid>[0-9.]+(?:v\d+)?)' # only the numerical arxiv ID (+possible version)
_RX_ARXIVID_TOL = r'(?P<arxivid>[-a-zA-Z0-9./]+)' # allow primary-class/ etc.

def _mk_braced_pair_rx(mid):
    return [ re.compile(_RX_BEFORE + r'\{\s*' + mid + r'\s*\}' + _RX_AFTER, re.IGNORECASE) ,
             re.compile(_RX_BEFORE + mid + _RX_AFTER, re.IGNORECASE) ]

# a list of regexes that we will need often
_rxarxiv = (
    []
    + _mk_braced_pair_rx(
        r'\\href\s*\{\s*(?:http://)?arxiv\.org/(?:abs|pdf)/' + _RX_ARXIVID_TOL + r'\s*\}\s*\{[^\{\}]*\}'
        )
    + _mk_braced_pair_rx(
        r'\\(?:url|href)\s*\{\s*(?:http://)?arxiv\.org/(?:abs|pdf)/' + _RX_ARXIVID_TOL + r's*\}'
        )
    + _mk_braced_pair_rx(
        r'(?:http://)?arxiv\.org/(?:abs|pdf)/' + _RX_ARXIVID_TOL
        )
    + _mk_braced_pair_rx(
        r'arXiv[-\}\{.:/\s]+(((?P<primaryclass>[-a-zA-Z0-9./]+)/)?' + _RX_ARXIVID_PURE + r')'
        )
    );

# "pure" arxiv ID means the arxiv ID (with primary class for old IDs only), without version information.
_rx_purearxivid = re.compile(r'(?P<purearxivid>((\d{4}\.\d{4,})|([-a-zA-Z0-9.]+/\d+))(v\d+)?)', re.IGNORECASE)

# extract arXiv info from an entry
def detectEntryArXivInfo(entry):
    """
    Extract arXiv information from a pybtex.database.Entry bibliographic entry.

    Returns upon success a dictionary of the form
        { 'primaryclass': <primary class, if available>,
          'arxivid': <the (minimal) arXiv ID (in format XXXX.XXXX  or  archive/XXXXXXX)>,
          'archiveprefix': value of the 'archiveprefix' field
          'published': True/False <whether this entry was published in a journal other than arxiv>,
          'doi': <DOI of entry if any, otherwise None>
        }

    If no arXiv information was detected, then this function returns None.
    """
    
    fields = entry.fields;

    d =  { 'primaryclass': None ,
           'arxivid': None ,
           'published': True ,
           'archiveprefix': None,
           'doi': None,
           };
    
    if (entry.type == u'unpublished' or entry.type == u'misc'):
        d['published'] = False
    elif ('journal' in fields and re.search(r'arxiv', fields['journal'], re.IGNORECASE)):
        # if journal is the arXiv, then it's not published.
        d['published'] = False
    elif ('journal' in fields and fields['journal'].strip()):
        # otherwise, if there is a journal, it's published
        d['published'] = True
    elif (entry.type == u'inproceedings'):
        # in conference proceedings -- published
        d['published'] = True
    elif ('journal' not in fields or fields['journal'] == ""):
        # if there's no journal, it's the arxiv.
        d['published'] = False
    else:
        logger.longdebug('No decisive information about whether this entry is published: %s (type %s), '
                         'defaulting to True.', entry.key, entry.type);


    def extract_pure_id(x, primaryclass=None):
        m = _rx_purearxivid.search( (primaryclass+'/' if primaryclass else "") + x)
        if m is None:
            raise IndexError
        return m.group('purearxivid')


    if ('doi' in fields and fields['doi']):
        d['doi'] = fields['doi']

    if ('eprint' in fields):
        # this gives the arxiv ID
        try:
            d['arxivid'] = extract_pure_id(fields['eprint'], primaryclass=fields.get('primaryclass', None));
            m = re.match('^([-\w.]+)/', d['arxivid']);
            if (m):
                d['primaryclass'] = m.group(1);
        except IndexError as e:
            logger.longdebug("Indexerror: invalid arXiv ID [%r/]%r: %s",
                             fields.get('primaryclass',None), fields['eprint'], e)
            logger.warning("Entry `%s' has invalid arXiv ID %r", entry.key, fields['eprint'])

    if ('primaryclass' in fields):
        d['primaryclass'] = fields['primaryclass'];

    if ('archiveprefix' in fields):
        d['archiveprefix'] = fields['archiveprefix'];


    def processNoteField(notefield, d):

        for rx in _rxarxiv:
            m = rx.search(notefield);
            if m:
                if (not d['arxivid']):
                    try:
                        primaryclass = None
                        try: primaryclass = m.group('primaryclass')
                        except IndexError: pass

                        d['arxivid'] = extract_pure_id(m.group('arxivid'), primaryclass=primaryclass)
                    except IndexError as e:
                        logger.longdebug("indexerror while getting arxivid in note=%r, m=%r: %s", notefield, m, e)
                        pass
                if (not d['primaryclass']):
                    try:
                        d['primaryclass'] = m.group('primaryclass');
                    except IndexError:
                        pass
                
    if ('note' in fields):
        processNoteField(fields['note'], d);

    if ('annote' in fields):
        processNoteField(fields['annote'], d);

    if ('url' in fields):
        processNoteField(fields['url'], d);

    if (d['arxivid'] is None):
        # no arXiv info.
        return None

    # FIX: if archive-ID is old style, and does not contain the primary class, add it as "quant-ph/XXXXXXX"
    if (re.match(r'^\d{7}$', d['arxivid']) and d['primaryclass'] and len(d['primaryclass']) > 0):
        d['arxivid'] = d['primaryclass']+'/'+d['arxivid']
    
    return d


def stripArXivInfoInNote(notestr):
    """Assumes that notestr is a string in a note={} field of a bibtex entry, and strips any arxiv identifier
    information found, e.g. of the form 'arxiv:XXXX.YYYY' (or similar).
    """

    newnotestr = notestr
    for rx in _rxarxiv:
        # replace all occurences of rx's in _rxarxiv with nothing.
        newnotestr = rx.sub('', newnotestr)

    if (notestr != newnotestr):
        logger.longdebug("stripArXivInfoInNote: stripped %r to %r", notestr, newnotestr)
    return newnotestr






# ---- API info ------



def reference_doi(ref):
    try:
        doi = ref._field_text('doi', namespace=arxiv2bib.ARXIV)
    except:
        return None
    if (doi):
        return doi
    return None

def reference_category(ref):
    try:
        return ref.category;
    except AttributeError:
        # happens for ReferenceErrorInfo, for example
        return None


def fetch_arxiv_api_info(idlist, cache_entrydic, filterobj=None):
    """
    Populates the given cache with information about the arXiv entries given in `idlist`.

    cache_entrydic is expected to be the cache
    `[filter/bibolamazifile].cache_for('arxiv_fetched_api_info')['fetched']`
    """

    missing_ids = [ aid for aid in idlist
                    if (aid not in cache_entrydic  or
                        cache_entrydic.get(aid) is None  or
                        isinstance(cache_entrydic.get(aid), arxiv2bib.ReferenceErrorInfo)) ]
    
    if not missing_ids:
        logger.longdebug('nothing to fetch: no missing ids')
        # nothing to fetch
        return True

    logger.longdebug('fetching missing id list %r' %(missing_ids))
    try:
        arxivdict = arxiv2bib.arxiv2bib_dict(missing_ids)
        logger.longdebug('got entries %r: %r' %(arxivdict.keys(), arxivdict))
    except URLError as error:
        filtname = filterobj.name() if filterobj else None;
        if isinstance(error, HTTPError) and error.getcode() == 403:
            raise BibFilterError(
                filtname,
                textwrap.dedent("""\
                403 Forbidden error. This usually happens when you make many
                rapid fire requests in a row. If you continue to do this, arXiv.org may
                interpret your requests as a denial of service attack.
                
                For more information, see http://arxiv.org/help/robots.
                """))
        else:
            msg = (("%d: %s" %(error.code, error.reason)) if isinstance(error, HTTPError)
                   else error.reason)
            logger.warning("HTTP Connection Error: %s.", msg)
            logger.warning("ArXiv API information will not be retreived, and your bibliography "
                           "might be incomplete.")
            return False
            #
            # Don't raise an error, in case the guy is running bibolamazi on his laptop in the
            # train. In that case he might prefer some missing entries rather than a huge complaint.
            #
            #            raise BibFilterError(
            #                filtname,
            #                "HTTP Connection Error: {0}".format(error.getcode())
            #                )

    for (k,ref) in arxivdict.iteritems():
        logger.longdebug("Got reference object for id %s: %r" %(k, ref.__dict__))
        cache_entrydic[k]['reference'] = ref
        bibtex = ref.bibtex()
        cache_entrydic[k]['bibtex'] = bibtex

    return True








# --- the cache mechanism ---

class ArxivInfoCacheAccess:
    def __init__(self, entrydic, bibolamazifile):
        self.entrydic = entrydic;
        self.bibolamazifile = bibolamazifile;

    def rebuild_cache(self):
        self.entrydic.clear()
        self.complete_cache()

    def complete_cache(self):
        bibdata = self.bibolamazifile.bibliographydata()

        needs_to_be_completed = []
        for k,v in bibdata.entries.iteritems():
            if (k in self.entrydic):
                continue
            arinfo = detectEntryArXivInfo(v);
            self.entrydic[k] = arinfo;
            logger.longdebug("got arXiv information for `%s': %r.", k, arinfo)
            
            if (self.entrydic[k] is not None):
                needs_to_be_completed.append( (k, arinfo['arxivid'],) )

        # complete the entry arXiv info using fetched info from the arXiv API.
        fetched_api_cache = self.bibolamazifile.cache_for('arxiv_fetched_api_info')['fetched'];
        fetch_arxiv_api_info( (x[1] for x in needs_to_be_completed),
                             fetched_api_cache)


        # ### BUG: if a fetch failed once, then we need to remove the cache file before it
        #     will fetch it again...

        for (k,aid) in needs_to_be_completed:
            api_info = fetched_api_cache.get(aid)
            if (api_info is None):
                logger.warning("Failed to fetch arXiv information for %s", aid);
                continue
            
            self.entrydic[k]['primaryclass'] = reference_category(api_info['reference'])
            self.entrydic[k]['doi'] = reference_doi(api_info['reference']);
    

    def getArXivInfo(self, entrykey):
        if (entrykey not in self.entrydic):
            self.complete_cache()

        return self.entrydic.get(entrykey, None)
            

def get_arxiv_cache_access(bibolamazifile):
    arxiv_info_cache = bibolamazifile.cache_for('arxiv_info')

    #logger.longdebug("ArXiv cache state is: %r" %(arxiv_info_cache))

    arxivaccess = ArxivInfoCacheAccess(arxiv_info_cache['entries'], bibolamazifile);
    
    if not arxiv_info_cache['cache_built']:
        arxivaccess.rebuild_cache()
        arxiv_info_cache['cache_built'] = True

    return arxivaccess


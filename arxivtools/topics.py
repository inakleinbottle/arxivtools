### Arxivtools.topics
import logging
import csv
import os.path as osp


from arxivtools import APP_CONF_DIR

logger = logging.getLogger(__name__)



ARXIV_TOPICS = {
    'math' : {'CA' : 'Classical analysis and ODEs',
              'CV' : 'Complex variables',
              'FA' : 'Functional analysis',
              'OA' : 'Operator algebras',
              'DS' : 'Dynamical systems',
              'PR' : 'Probability',
              'GN' : 'General topology',
              'AG' : 'Algebraic geometry',
              'AT' : 'Algebraic topology',
              'AP' : 'Analysis of PDEs',
              'CT' : 'Category thoery',
              'CO' : 'Combinatorics',
              'AC' : 'Commutative algebra',
              'DG' : 'Differential geometry',
              'GM' : 'General mathematics',
              'GT' : 'Geometric topology',
              'HO' : 'History and overview',
              'IT' : 'Information technology',
              'KT' : 'K-theory and homology',
              'LO' : 'Logic',
              'MP' : 'Mathematical physics',
              'MG' : 'Metric geometry',
              'NT' : 'Number theory',
              'OC' : 'Optimization and control',
              'QA' : 'Quantum algebra',
              'RT' : 'Representation theory',
              'RA' : 'Rings and algebras',
              'SP' : 'Spectral theory',
              'ST' : 'Statistics theory',
              'SG' : 'Sympectic geometry',
              },
    'astro-ph' : {'GA' : 'Astrophysics of galaxies',
                  'CO' : 'Cosmology and nongalactic astrophysics',
                  'EP' : 'Earth and planetary astrophysics',
                  'HE' : 'High energy astrophysical phenomena',
                  'IM' : 'Instrumentation and methods for astrophysics',
                  'SR' : 'Solar and stellar astrophysics',
                  },
    'cond-mat' : {'dis-nn' : 'Disordered systems and Nerual Networks',
                  'mtrl-sci' : 'Materials science',
                  'mes-hall' : 'Mesocale and nanoscal physics',
                  'other' : 'Other condensed matter',
                  'quant-gas' : 'Quantum gases',
                  'soft' : 'Soft condensed matter',
                  'stat-mech' : 'Statistical mechanics',
                  'str-el' : 'Strongly correlated electrons',
                  'supr-con' : 'Superconductivity',
                  },
    'gr-qc' : 'General relativity and quantum cosmology',
    'hep-ex' : 'High energy physics - experimental',
    'hep-ph' : 'High energy physics - phenomenology',
    'hep-lat' : 'High energy physics - lattice',
    'hep-th' : 'high energy physics - theory',
    'math-ph' : 'Mathematical physics',
    'nlin' : {'AO' : 'Adaptation and self-organizing systems',
              'CG' : 'Cellular automata and lattice gases',
              'CD' : 'Chaotic dynamics',
              'SL' : 'Exactly solvable and integrable systems',
              'PS' : 'Pattern formation and solitons',
              },
    'nucl-ex' : 'Nuclear experimentation',
    'nucl-th' : 'Nuclear theory',
    'physics' : {'acc-ph' : 'Accelerator physics',
                 'app-ph' : 'Applied physics',
                 'ao-ph' : 'atmospheric and oceanic physics',
                 'atom-ph' : 'Atomic physics',
                 'atm-clus' : 'Atomic and molecuar clusters',
                 'bio-ph' : 'Biological physics',
                 'chem-ph' : 'Chemical physics',
                 'class-ph' : 'Classical physics',
                 'comp-ph' : 'Computational physics',
                 'data-an' : 'Data analysis, statistics and probability',
                 'flu-dyn' : 'Fluid dynamics',
                 'gen-ph' : 'General physics',
                 'geo-ph' : 'Geophysics',
                 'hist-ph' : 'History and philosophy of physics',
                 'ins-det' : 'Instrumetation and detectors',
                 'med-ph' : 'Medical physics',
                 'optics' : 'Optics',
                 'ed-ph' : ' Physics education',
                 'soc-ph' : 'Physics and society',
                 'plasm-ph' : 'Plasma physics',
                 'pop-ph' : 'Popular physics',
                 'space-ph' : 'Space physics',
                 },
    'quant-ph' : 'Quantum physics',
    'cs' : {'AI' : 'Artificial intelligence',
            'CL' : 'Computation and language',
            'CC' : 'Computational complexity',
            'CE' : 'Computational engineering, finance, and science',
            'CG' : 'Computation geometry',
            'GT' : 'Computer science and game theory',
            'CV' : 'Computer vision and pattern recognition',
            'CY' : 'Computers and society',
            'CR' : 'Cryptography and security',
            'DS' : 'Data structures and algorithms',
            'DB' : 'Databases',
            'DL' : 'Digital libraries',
            'DM' : 'Discrete mathematics',
            'DC' : 'Distributed, parallel, and cluster computing',
            'ET' : 'Emerging technologies',
            'FL' : 'Formal languages and automata theory',
            'GL' : 'General literature',
            'GR' : 'Graphics',
            'AR' : 'Hardware architecture',
            'HC' : 'Human-computer interaction',
            'IR' : 'Information retrieval',
            'IT' : 'Information theory',
            'LG' : 'Machine learning',
            'LO' : 'Logic in computer science',
            'MS' : 'Mathematical software',
            'MA' : 'Multiagent systems',
            'MM' : 'Multimedia',
            'NI' : 'Networking and internet architecture',
            'NE' : 'Neural and evolutionary computing',
            'NA' : 'Numerical analysis',
            'OS' : 'Operating systems',
            'OH' : 'Other',
            'PF' : 'Performance',
            'PL' : 'Programming languages',
            'RO' : 'Robotics',
            'SI' : 'Social and information networks',
            'SE' : 'Software engineering',
            'SD' : 'Sound',
            'SC' : 'Symbolic computation',
            'SY' : 'Systems and control',
            },
    'q-bio' : {'BM' : 'Biomolecules',
               'CB' : 'Cell behavior',
               'GN' : 'Genomics',
               'MN' : 'Molecular networks',
               'NC' : 'Neurons and cognition',
               'OT' : 'Other quantitative biology',
               'PE' : 'Populations and evolution',
               'QM' : 'Quantitative methods',
               'SC' : 'Subcellular processes',
               'TO' : 'Tissues and organs',
               },
    'q-fin' : {'CP' : 'Computational finance',
               'EC' : 'Economics',
               'GN' : 'General Finance',
               'MF' : 'Mathematical finance',
               'PM' : 'Portfolio management',
               'PR' : 'Pricing of securities',
               'RM' : 'Risk management',
               'ST' : 'Statistical finance',
               'TR' : 'Trading and market microstructure',
               },
    'stat' : {'AP' : 'Applications',
              'CO' : 'Computation',
              'ML' : 'Machine learning',
              'ME' : 'Methodology',
              'OT' : 'Other statistics',
              'TH' : 'Statistical theory',
              },
    'eess' : {'AS' : 'Audio and speech processing',
              'IV' : 'Image and video processing',
              'SP' : 'Signal processing',
              },
    'econ' : {'EM' : 'Econometrics',
              'GN' : 'General economics',
              'TH' : 'Theoretical economics',
              },
    }



def resolve(topic):
    '''Get the title for a topic code.'''
    if '.' in topic:
        main, sub = topic.split('.')
        if not main in ARXIV_TOPICS:
            raise ValueError(f'Topic {main} does not exist')
        elif not sub in ARXIV_TOPICS[main]:
            raise ValueError(f'Subtopic {main}.{sub} does not exist')
        return ARXIV_TOPICS[main][sub]
    else:
        topic
        if not topic in ARXIV_TOPICS:
            raise ValueError(f'Topic {main} does not exist')
        if isinstanec(ARXIV_TOPICS[topic], dict):
            return topic
        else:
            return ARXIV_TOPICS[topic]

def check_reduce(topics):
    '''Check for invalid topics and reduce to minimal set.'''
    invalid_mains = [topic for topic in topics
                     if not topic.split('.')[0] in ARXIV_TOPICS]
    for top in invalid_mains:
        logger.warning(f'Topic {top} is invalid and will be removed')
        topics.remove(top)

    invalid_subs = [topic for topic in topics
                    if '.' in topic
                    if not topic.split('.')[1] in
                    ARXIV_TOPICS[topic.split('.')[0]]]
    for top in invalid_subs:
        logger.warning(f'Topic {top} is invalid and will be removed')
        topics.remove(top)

    if not topics:
        raise ValueError('No valid topics in list')

    return [topic for topic in topics
            if not ('.' in topic and topic.split('.')[0] in topics)]


def load_topics():
    '''Load the selected topics from config.'''
    path = osp.join(APP_CONF_DIR, 'topics.csv')
    if not osp.exists(path):
        logger.error('No topics specified in config, exiting')
        raise RuntimeError('No topics specified in config')

    with open(path, 'r') as f:
        topics = [top for row in csv.reader(f) for top in row]

    return check_reduce(topics)
        

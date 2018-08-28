import logging
import csv
import os
import os.path as osp
from configparser import ConfigParser


import click


from arxivtools import APP_CONF_DIR, OUTPUT_DIR



logger = logging.getLogger(__name__)



def _load_csv(name):
    '''Utility function to load csv files from the config dir.'''
    path = osp.join(APP_CONF_DIR, name + '.csv')
    ret = []
    if not osp.exists(path):
        with open(path, 'w') as f:
            f.write('')
    else:
        with open(osp.join(path), 'r') as f:
            ret = [item for row in csv.reader(f) for item in row]
    return ret

def _update_csv(name, data):
    '''Utility function to update csv file in the config dir.'''
    path = osp.join(APP_CONF_DIR, name + '.csv')
    with open(path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def _manage_data(name, add, remove):
    '''Manage the data in one of the csv config files.'''
    data = _load_csv(name)
            
    if not add and not remove:
        logger.debug(f'Listing {name}')
        click.echo('\n'.join(data))
    else:
        logger.info('Modifying {name}.csv')
        for item in add:
            if not item in data:
                data.append(item)
                logger.info(f'Adding {item}')
            else:
                logger.warning(f'Item {item} is already in list {name}.')
        for item in remove:
            if item in authors:
                author.remove(item)
                logger.info(f'Removing {item}')
            else:
                logger.warning(f'Item {item} is not in list {name}.')
        logger.debug('Updating {name} config file')
        _update_csv(name, data)


@click.group()
@click.pass_context
def arxivtools(ctx):
    '''Command line utilities for arxivtools.'''
    pass



##@arxivtools.command()
##@click.pass_context
##def setup(ctx):
##    '''Set up arxivtools with a new configuration.
##
##    Build a new arxivtools profile, retrieve training articles,
##    and build a new filter for daily searches.
##    '''
##    logger.info('Running setup')
##    parser = ConfigParser()
##    MAIN_CONFIG = None # Replace me
##    parser.read(MAIN_CONFIG,
##                osp.join(APP_CONF_DIR, 'config.ini'))


def _display_records(records, authors, titles, abstracts):
    for entry in records:
        if titles:
            click.echo(f'{entry.title}')
        if authors:
            click.echo(f'{",".join(entry.authors)}')
        if abstracts:
            click.echo(f'{entry.abstract}')


@arxivtools.command()
@click.option('-t', '--type', 'typ', default='au',
              type=click.Choice(['au','ti','all']),
              help='Search type: au = author, ti = title, all = all')
@click.option('-T', '--titles', default=True, is_flag=True,
              help='Display titles')
@click.option('-a', '--authors', is_flag=True,
              help='Display authors')
@click.option('-A', '--abstracts', is_flag=True,
              help='Display abstracts')
@click.option('-n', '--number', default=10,
              help='Max number of records')
@click.argument('terms', nargs=-1)
@click.pass_context
def search(ctx, typ, terms, number, authors, titles, abstracts):
    '''Search the ArXiv for specified terms.

    Search the ArXiv for the terms specified in the "terms" arguments.
    Multiple terms can be provided, but must all be of the same type,
    as specified in the type option.

    Args:
        terms: Terms to search in the ArXiv.

    '''
    from arxivtools.arxivapi import ArxivAPIRequest
    query = { typ : terms }
    
    AAR = ArxivAPIRequest(search_terms=query,
                          max_records=number)
    _display_records(AAR.make_request(), authors, titles, abstracts)
        

@arxivtools.command()
@click.argument('arxiv_id', nargs=-1)
@click.option('-T', '--titles', default=True, is_flag=True,
              help='Display titles')
@click.option('-a', '--authors', is_flag=True,
              help='Display authors')
@click.option('-A', '--abstracts', is_flag=True,
              help='Display abstracts')
@click.option('-n', '--number', default=10,
              help='Max number of records')
@click.pass_context
def get(ctx, arxiv_id, titles, authors, abstracts, number):
    '''Retrive entries from the ArXiv by their ArXiv ID.

    Args:
        arxiv_id: ArXiv IDs to retrieve.
    '''
    from arxivtools.arxivapi import ArxivAPIRequest
    AAR = ArxivAPIRequest(id_list=arxiv_id,
                          max_records=number)
    _display_records(AAR.make_request(), authors, titles, abstracts)


@arxivtools.command()
@click.option('-a', '--add', multiple=True,
              help='Add a new author.')
@click.option('-r', '--remove', multiple=True,
              help='Remove an author.')
@click.pass_context
def authors(ctx, add, remove):
    '''Show the list of authors currently on your follow list.

    List all of the authors currently on your follow list. 
    '''
    _manage_data('authors', add, remove)
                    
@arxivtools.command()
@click.option('-a', '--add', multiple=True,
              help='Add a new topic.')
@click.option('-r', '--remove', multiple=True,
              help='Remove an topic.')
@click.pass_context
def topics(ctx, add, remove):
    '''Manage topics for the daily search.'''
    _manage_data('topics', add, remove)
        

            

@arxivtools.command()
@click.pass_context
def rebuild(ctx):
    '''Rebuild the current filter.

    Rebuild the filter object used to accept or reject papers in
    daily searches. This will take newly added followed authors
    and any changes to settings into account.
    '''
    from arxivtools.filter import new_filter
    logger.debug('Rebuilding filter')

    # main filter is held in default.flt
    os.remove(osp.join(APP_CONF_DIR, 'default.flt'))
    new_filter(APP_CONF_DIR)

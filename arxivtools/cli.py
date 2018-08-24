import logging
import csv
import os
import os.path as osp
from configparser import ConfigParser


import click


from arxivtools import APP_CONF_DIR, OUTPUT_DIR
from arxivtools.filter import new_filter


## CLI setup
# TLC: arxivtools
#   - setup
#   - add authors
#   - remove authors
#   - show authors
#   - update data

logger = logging.getLogger(__name__)



@click.group
@click.pass_context
def arxivtools(ctx):
	'''Command line utilities for arxivtools.'''
	pass



@arxivtools.command
@click.pass_context
def setup(ctx):
	'''Set up arxivtools with a new configuration.

	Build a new arxivtools profile, retrieve training articles,
	and build a new filter for daily searches.
	'''
	logger.info('Running setup')






@arxivtools.command
@click.option('-a', '--add', multiple=True,
              help='Add a new author.')
@click.option('-r', '--remove', multiple=True,
              help='Remove an author.')
@click.pass_context
def author(ctx, add, remove):
	'''Show the list of authors currently on your follow list.

	List all of the authors currently on your follow list. 
	'''
	with open(osp(APP_CONF_DIR, 'authors.csv'), 'r') as f:
                authors = [au for row in csv.reader(f) for au in row]
                
	if not add or not remove:
                logger.debug('Listing authors')
                click.echo('\n'.join(authors))
        else:
                for au in add:
                        if not au in authors:
                                authors.append(au)
                                click.echo(f'Adding {au}')
                                logger.debug(f'Adding {au} to author list.')
                        else:
                                logger.warning(f'Author {au} is already in the author list')
                for au in remove:
                        if au in authors:
                                author.remove(au)
                                click.echo(f'Removing {au}')
                                logger.debug(f'Removing {au} from author list')
                        else:
                                logger.warning(f'Author {au} is not in the author list.')
                                
                                
                

                

@arxivtools.command
@click.pass_context
def rebuild(ctx):
	'''Rebuild the current filter.

	Rebuild the filter object used to accept or reject papers in
	daily searches. This will take newly added followed authors
	and any changes to settings into account.
	'''
	logger.debug('Rebuilding filter')

	# main filter is held in default.flt
	os.remove(osp.join(APP_CONF_DIR, 'default.flt'))
	new_filter(APP_CONF_DIR)

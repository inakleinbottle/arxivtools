import logging
from configparser import ConfigParser


import click


from . import APP_CONF_DIR, OUTPUT_DIR


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
	logger.debug('Running setup')



@arxivtools.command
@click.argument('authors', nargs='+')
@click.pass_context
def add(ctx, authors):
	'''Add authors to your follow list.

	Arixvtools will automatically accept any papers by an accepted
	author, and their abstracts will be used to train any learning
	filters.

	:param: authors The authors you wish to add to your follow list.
	'''
	logger.debug('Adding new authors')



@arxivtools.command
@click.argument('authors', nargs='+')
@click.pass_context
def remove(ctx, authors):
	'''Remove authors from your follow list.

	Remove an author from your follow list so their articles will no
	longer be accepted automatically.

	:param: authors The authors you wish to remove.
	'''
	logger.debug('Removing authors')


@arxivtools.command
@click.pass_context
def authors(ctx):
	'''Show the list of authors currently on your follow list.

	List all of the authors currently on your follow list. 
	'''
	logger.debug('Listing authors')



@arxivtools.command
@click.pass_context
def rebuild(ctx):
	'''Rebuild the current filter.

	Rebuild the filter object used to accept or reject papers in
	daily searches. This will take newly added followed authors
	and any changes to settings into account.
	'''
	logger.debug('Rebuilding filter')

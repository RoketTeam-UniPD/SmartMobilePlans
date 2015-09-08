#!/usr/bin/perl -w

use strict;
use utf8;
use warnings;

use CGI;
use SUB;
use CGI::Session;
use HTML::Entities;
use XML::LibXML;
use POSIX qw(strftime);
use feature qw( switch );

my $parser = XML::LibXML->new();

$parser->keep_blanks(0);
my $doc = $parser->parse_file('../data/plans.xml');

my $cgi = CGI->new();

my $operator = $cgi->param('operator');
my $id = $cgi->param('id');

my $root = $doc->documentElement();
for my $node ($root->findnodes(
   '//' . $operator . "[\@id='" . $id . "']"
)) {
   $root->removeChild($node);
}


$doc->toFile('../data/plans.xml', 1);
print $cgi->redirect('operator.cgi?name=' . $operator);

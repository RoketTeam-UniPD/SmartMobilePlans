#!/usr/bin/perl -w

use strict;
use utf8;
use warnings;

use CGI;
use HTML::Entities;
use Template;
use XML::LibXML;


# Declarations and parse of XML file document
my $parser = XML::LibXML->new(no_blanks => 1);
my $doc = $parser->parse_file('../data/plans.xml');


# Declarations and retreive the id over GET
my $cgi = CGI->new();
my $id = $cgi->param('id');


# Get element from id
my $node = $doc->getElementById("$id");


# If not find redirect to error page, else inizialized web page
if (!defined $node){
	print $cgi->redirect('../404.html');
	exit;
}else{
	print $cgi->header( -type => "text/html", charset => 'utf-8', -status => "200 OK" );
	print $cgi->start_html;
}


# Convert text from XML to HTML Entity names
my $desc = $node->findvalue('description');
my $txt = encode_entities($desc);


# Fill var to send an template file
my $vars = {
	operator		=> $node->getName(),
	id				=> $node->findvalue('@xml:id'),
	payments		=> $node->findvalue('@payments'),
	title			=> $node->findvalue('title'),
	insertdatetime	=> $node->findvalue('insertdatetime'),
	available		=> $node->findvalue('available/@disabled'),
	startdate		=> $node->findvalue('available/startdate'),
	enddate			=> $node->findvalue('available/enddate'),
	currency		=> $node->findvalue('price/@currency'),
	price			=> $node->findvalue('price'),
	unit			=> $node->findvalue('expiry/@unit'),
	expiry			=> $node->findvalue('expiry'),
	minutes			=> $node->findvalue('rates/minutes'),
	messages		=> $node->findvalue('rates/messages'),
	datasize		=> $node->findvalue('rates/internet/@datasize'),
	internet		=> $node->findvalue('rates/internet'),
	description		=> "$txt"
};


# Create istance of template and declare file to use
my $template = Template->new();
my $template_file = 'plan.tt';

# Process vars in to template file
$template->process($template_file, $vars) || die "Template process failed: ", $template->error(), "\n";

# Close end HTML page
print $cgi->end_html;
#!/usr/bin/perl -w

use strict;
use utf8;
use warnings;

use Data::Dumper;
use HTML::Entities;
use Template;
use XML::LibXML;
use CGI;

my $filename = '../data/plans.xml';

my $parser = XML::LibXML->new(no_blanks => 1);
my $doc = $parser->parse_file($filename);

my $cgi = CGI->new();
my $name = $cgi->param('id');

my $node = $doc->getElementById("$name");

if ($node == ""){
  print $cgi->header( -type => "text/html", charset => 'utf-8', -status => "404 Not Found" );
  print $cgi->start_html;
}else{
  print $cgi->header( -type => "text/html", charset => 'utf-8', -status => "200 OK" );
  print $cgi->start_html;
}
my $desc = $node->findvalue('description');
my $txt = encode_entities($desc);


my $file = 'prova.tpl';
my $vars = {
  operator        => $node->getName(),
  id              => $node->findvalue('@xml:id'),
  payments        => $node->findvalue('@payments'),
  title           => $node->findvalue('title'),
  insertdatetime  => $node->findvalue('insertdatetime'),
  available       => $node->findvalue('available/@disabled'),
  startdate       => $node->findvalue('available/startdate'),
  enddate         => $node->findvalue('available/enddate'),
  currency        => $node->findvalue('price/@currency'),
  price           => $node->findvalue('price'),
  unit            => $node->findvalue('expiry/@unit'),
  expiry          => $node->findvalue('expiry'),
  minutes         => $node->findvalue('rates/minutes'),
  messages        => $node->findvalue('rates/messages'),
  datasize        => $node->findvalue('rates/internet/@datasize'),
  internet        => $node->findvalue('rates/internet'),
  description     => "$txt"
};


my $template = Template->new();
$template->process($file, $vars) || die "Template process failed: ", $template->error(), "\n";
print $cgi->end_html;
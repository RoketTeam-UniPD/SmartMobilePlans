#!/usr/bin/perl -w

use strict;
use utf8;
use warnings;

use Template;
use CGI;
use HTML::Entities;
use Template;
use XML::LibXML;


my $parser = XML::LibXML->new();
$parser->keep_blanks(0);
my $doc = $parser->parse_file('../data/admins.xml');

my $cgi = CGI->new();

my $username = $cgi->param('username');
my $pwd = $cgi->param('pwd');

my $admin  = $doc->getDocumentElement;

my $node = XML::LibXML::Element->new("admin");

my $u = XML::LibXML::Element->new("username");
$u->appendText($username);

my $p = XML::LibXML::Element->new("password");
$p->appendText($pwd);

$node->addChild($u);
$node->addChild($p);

$admin->addChild($node);


$doc->toFile('../data/admins.xml', 1);

print $cgi->redirect('admin.cgi');
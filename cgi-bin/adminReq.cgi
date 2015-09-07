#!/usr/bin/perl -w

use strict;
use utf8;
use warnings;

use CGI;
use SUB;
use HTML::Entities;
use XML::LibXML;
use POSIX qw(strftime);
use Digest::SHA qw(sha256_hex);


my $parser = XML::LibXML->new();

$parser->keep_blanks(0);
my $doc = $parser->parse_file('../data/admins.xml');

my $cgi = CGI->new();

my $username = $cgi->param('username');
my $pwd = $cgi->param('pwd');
my $pwdc = $cgi->param('pwd-confirm');

if (!$pwd or !$pwdc or !$username) {
	print $cgi->redirect('admin.cgi?e=admin-empty'); 
}

my $admin = $doc->findnodes("//admin[username='" . $username . "']");
if ($admin) {
	print $cgi->redirect('admin.cgi?e=admin-usr'); 
}

if ($pwd ne $pwdc) {
	print $cgi->redirect('admin.cgi?e=admin-pwd'); 
}

my $admin_n  = $doc->getDocumentElement;

my $node = XML::LibXML::Element->new('admin');
$node->setAttribute('xml:id', SUB::generateID($doc));

my $u = XML::LibXML::Element->new('username');
$u->appendText($username);

my $p = XML::LibXML::Element->new('password');
$p->appendText(sha256_hex($pwd));

$node->addChild($u);
$node->addChild($p);

$admin_n->addChild($node);

$doc->toFile('../data/admins.xml', 1);
print $cgi->redirect('admin.cgi?e=admin-success');

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
my $payments = $cgi->param('payments');
my $title = $cgi->param('title');
my $insertdatetime = strftime "%Y-%m-%d %H-%M-%s", localtime;
my $startdate = $cgi->param('syear') . "-" . $cgi->param('smonth') . "-" . $cgi->param('sday');
my $enddate = $cgi->param('eyear') . "-" . $cgi->param('emonth') . "-" . $cgi->param('eday');
my $price = $cgi->param('price');
my $currency = $cgi->param('currency');
my $unit = $cgi->param('unit');
my $expiry = $cgi->param('expiry');
my $minutes = $cgi->param('minutes');
my $messages = $cgi->param('messages');
my $datasize = $cgi->param('datasize');
my $internet = $cgi->param('internet');
my $description = $cgi->param('description');

if (!$title or !$price or !$expiry or !$minutes or !$messages or !$internet or !$description) {
	saveformData();
	print $cgi->redirect('admin.cgi?e=plan-empty');  

	exit;
}

my $plan = $doc->findnodes("//" . $operator . "[title='" . $title . "']");
if ($plan) {
	saveformData();
	print $cgi->redirect('admin.cgi?e=plan-exists'); 
}

sub saveformData {
	my $session = CGI::Session->load();

	my %formData = (
		title 		=> $title, 
		operator 	=> $operator,
		payments 	=> $payments,
		syear 		=> $cgi->param('syear'),
		smonth 		=> $cgi->param('smonth'),
		sday 		=> $cgi->param('sday'),
		eyear 		=> $cgi->param('eyear'),
		emonth 		=> $cgi->param('emonth'),
		eday 		=> $cgi->param('eday'),
		price 		=> $price,
		currency 	=> $currency,
		unit 		=> $unit,
		expiry 		=> $expiry,
		minutes     => $minutes,
		messages    => $messages,
		datasize    => $datasize,
		internet    => $internet,
		description => $description
	);
	$session->param("form-data", \%formData);
}

## TEST
# my $operator = "tre";
# my $payments = "rechargable";
# my $title = "My title";
# my $insertdatetime = strftime "%Y-%m-%d %H-%M-%s", localtime;
# my $startdate = "2014-12-21";
# my $enddate = "2015-6-5";
# my $price = "34";
# my $currency = "euro";
# my $unit = "week";
# my $expiry = "4";
# my $minutes = "100";
# my $messages = "100";
# my $datasize = "GB";
# my $internet = "3";
# my $description = "This is the description";


my $plans  = $doc->getDocumentElement;

my $title_n = XML::LibXML::Element->new('title');
$title_n->appendText($title);

my $insertdatetime_n = XML::LibXML::Element->new('insertdatetime');
$insertdatetime_n->appendText($insertdatetime);

my $available_n = XML::LibXML::Element->new('available');
my $startdate_n = XML::LibXML::Element->new('startdate');
$startdate_n->appendText($startdate);
my $enddate_n = XML::LibXML::Element->new('enddate');
$enddate_n->appendText($enddate);
$available_n->addChild($startdate_n);
$available_n->addChild($enddate_n);

my $price_n = XML::LibXML::Element->new('price');
$price_n->setAttribute('currency', $currency);
$price_n->appendText($price);

my $expiry_n = XML::LibXML::Element->new('expiry');
$expiry_n->setAttribute('unit', $unit);
$expiry_n->appendText($expiry);

my $rates_n = XML::LibXML::Element->new('rates');
my $minutes_n = XML::LibXML::Element->new('minutes');
$minutes_n->appendText($minutes);
my $messages_n = XML::LibXML::Element->new('messages');
$messages_n->appendText($messages);
my $internet_n = XML::LibXML::Element->new('internet');
$internet_n->setAttribute('datasize', $datasize);
$internet_n->appendText($internet);
$rates_n->addChild($minutes_n);
$rates_n->addChild($messages_n);
$rates_n->addChild($internet_n);

my $description_n = XML::LibXML::Element->new('description');
$description_n->appendText($description);

my $operator_n;

if ($operator eq "vodafone") {
	$operator_n = XML::LibXML::Element->new('vodafone'); 
} elsif ($operator eq "wind") { 
	$operator_n = XML::LibXML::Element->new('wind'); 
} elsif ($operator eq "tim")	{ 
	$operator_n = XML::LibXML::Element->new('tim'); 
} elsif ($operator eq "tre") { 
	$operator_n = XML::LibXML::Element->new('tre'); 
}

$operator_n->setAttribute("payments", $payments);
$operator_n->setAttribute("xml:id", SUB::generateID($doc));

$operator_n->addChild($title_n);
$operator_n->addChild($insertdatetime_n);
$operator_n->addChild($price_n);
$operator_n->addChild($expiry_n);
$operator_n->addChild($rates_n);
$operator_n->addChild($description_n);

$plans->addChild($operator_n);


$doc->toFile('../data/plans.xml', 1);
print $cgi->redirect('admin.cgi?e=plan-success');

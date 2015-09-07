#!/usr/bin/perl -w

package SUB;

use strict;
use utf8;
use warnings;

use Template;
use CGI;
use POSIX;
use CGI::Session;
use XML::LibXML;

sub closeSession {
    my $session = CGI::Session->load();
    $session->close();
    $session->delete();
    $session->flush();

    return;
}


sub validateSchema {
    my $schema = XML::LibXML::Schema->new(location => $_[0]);

    eval { $schema->validate($_[1]) };

    if (my $ex = $@) {

      return undef;
    }

    return "";
}   


sub generateID {
    my $nodes = $_[0]->findnodes('(//*[@xml:id])[last()]');
    my $idref = $nodes->pop()->getAttribute("xml:id");
    $idref =~ s/(\d+)$/$1 + 1/e;
    
    return $idref; 

}


sub generateDate {
    return $_[0] . "-" . $_[1]  . "-" - $_[2];
}





# stramite la avriabile $title viene recepito il titolo da assegnale alla pagina
sub printStartHeader {
    my ($title) = @_;
    my $hr = qq{<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en" dir="ltr">
<head>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type"/>
    <title>$title Smart Mobile Plans Site</title>
    <meta name="keywords" content="" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <!-- provvisorio -->
    <link rel="stylesheet" type="text/css" href="../css/default.css" media="screen" />

    <!-- <link rel="stylesheet" type="text/css" href="../css/default.css" media="only screen and (min-width:641px)" /> -->
    <!-- <link rel="stylesheet" type="text/css" href="../css/mobile.css" media="only screen and (max-width:640px)" /> -->
    
    <link rel="stylesheet" type="text/css" href="../css/print.css" media="media="print"" />
    <link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Open+Sans:400,700" />
</head>
<body>
};
    return $hr;
}




sub printHeaderSITE {
    my $hr = qq{
<div class="header" title="Welcome in to Smart Mobile Plans site. We help you for choosing a better mobile phone plan.">
    <h1 title="Title">Smart Mobile Plans</h1>
    <p title="Description of">Choosing a mobile phone plan has never been this simple!</p>
</div>
};
    return $hr;
}





sub printMenuSITE {
    my ($active) = @_;
    my $hr = qq{
<div class="menu">
    <ul>};

    if(lc $active eq lc 'home'){
        $hr .= qq{
    <li><a tabindex="1" title="Homepage" class="active">HOME</a></li>};
    }else{
        $hr .= qq{
    <li><a tabindex="1" title="Homepage" href="home.cgi">HOME</a></li>};
    }

    if(lc $active eq lc 'tim'){
        $hr .= qq{
    <li><a tabindex="2" title="Tim plans" class="active">TIM</a></li>};
    }else{
        $hr .= qq{
    <li><a tabindex="2" title="Tim plans" href="operator.cgi?name=tim">TIM</a></li>};
    }

    if(lc $active eq lc 'vodafone'){
        $hr .= qq{
    <li><a tabindex="3" title="Vodafone plans" class="active">VODAFONE</a></li>};
    }else{
        $hr .= qq{
    <li><a tabindex="3" title="Vodafone plans" href="operator.cgi?name=vodafone">VODAFONE</a></li>};
    }

    if(lc $active eq lc 'tre'){
        $hr .= qq{
    <li><a tabindex="4" title="Tre plans" class="active">TRE</a></li>};
    }else{
        $hr .= qq{
    <li><a tabindex="4" title="Tre plans" href="operator.cgi?name=tre">TRE</a></li>};
    }

    if(lc $active eq lc 'wind'){
        $hr .= qq{
    <li><a tabindex="5" title="Wind plans" class="active">WIND</a></li>};
    }else{
        $hr .= qq{
    <li><a tabindex="5" title="Wind plans" href="operator.cgi?name=wind">WIND</a></li>};
    }

    $hr .= qq{
    </ul>
</div>
};

    return $hr;
}





sub printBreadcrumbsSITE {

    my @array = @{_};

    my $hr = qq{
<div class="breadcrumbs">
    <p>You are in: };

    my $size = scalar @{ $array[0] };
    my $i = 1;

    foreach my $desc (@{ $array[0] }) {

        if($i != $size){
            $hr .= qq{<a title="$desc->[0]" href="$desc->[1]">}.(uc$desc->[0]).qq{</a>};
            $hr .= qq{ \\ };
        }
        $i++;
    }

    $hr .= qq{<a title="$array[0][$size-1][0]">}.(uc$array[0][$size-1][0]).qq{</a>};

    $hr .= qq{</p>
</div>
};

    return $hr;
}





sub printFooterHTML {

    my $hr = qq{
<div class="footer">
    <p>Access to <a title="login area" tabindex="6" href="login.cgi">login</a> for edit site. | Copyright &copy; 2015 RocketTeam</p>
</div>
};

    return $hr;
}


sub printCloseHeader {
    my $hr = qq{
</body>
</html>
};
    return $hr
}



1;

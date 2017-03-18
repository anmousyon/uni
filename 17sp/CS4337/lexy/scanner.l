%{
	#include <stdlib.h>
	#include <stdio.h>
	#include "y.tab.h"
%}

%%

[a-zA-Z][a-zA-Z0-9]*       	{ return VAR; }
[0-9]+ 						{ yylval = atoi(yytext); return INT; }
[-+=/*\n\ \t]				{ return *yytext; }
'\('						{ return LP; }
'\)' 						{ return RP; }

%%

int yywrap(void) 			{ return 1; }

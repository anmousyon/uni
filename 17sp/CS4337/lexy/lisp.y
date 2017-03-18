%token INT VAR LP RP
%left '+' '-'
%left '*' '/'
%right UMINUS

%{
	void yyerror(char *);
	int yylex(void);
	int sym[100];
%}

%%

program 	: 	program statement '\n'
			|
			;

statement 	: 	exp
			| 	LP 'setq' VAR exp RP { sym[$1] = $3; }
			;

exp			: INT
			| VAR 					{ $$ = sym[$1]; }
			| LP '+' exp exp RP 	{ $$ = $3 + $4; }
			| LP '-' exp exp RP 	{ $$ = $3 - $4; }
			| LP '*' exp exp RP 	{ $$ = $3 * $4; }
			| LP '/' exp exp RP 	{ $$ = $3 / $4; }
			| LP exp RP 			{ $$ = $2; }
			;
 %%
 void yyerror(char *s) {
	 printf("** error ** %s\n", s);
 }

 int main(void){
	 yyparse();
	 return 0;
 }
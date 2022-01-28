#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "opts.h"

int getopts(int argc, char **argv, const struct opts *opts)
{
	/*
	 * 1. build option string from opts
	 * 2. get char from getopt()
	 * 3. look for character in opts and do given action
	 */
	char *s, *s2;
	const struct opt *op;
	int size = 0;
	int c;
	for (op = opts->opts; op->option > 0; ++op) {
		if (op->type >= OPT_VALUES) {
			++size;
		}
	}
	size += op - opts->opts + 1;
	s = malloc(size);
	s2 = s;
	if (!s) return -1;
	for (op = opts->opts; op->option > 0; ++op) {
		*s2++ = op->option;
		if (op->type >= OPT_VALUES) {
			*s2++ = ':';
		}
	}
	*s2 = '\0';
	while ((c = getopt(argc, argv, s)) != -1) {
		if (c == '?') return -1;
		/* look for c in opts->opts list */
		for (op = opts->opts; op->option > 0; ++op) {
			if (c == op->option) break;
		}
		if (op->option <= 0) {
			fprintf(stderr, "%s: how did this happen?\n",
			        argv[0]);
			return -1;
		}
		switch (op->type) {
		case OPT_SET:
			*(int *)op->value = 1;
			break;
		case OPT_RESET:
			*(int *)op->value = 0;
			break;
		case OPT_TOGGLE:
			*(int *)op->value = !*(int *)op->value;
			break;
		case OPT_INC:
			++*(int *)op->value;
			break;
		case OPT_DEC:
			--*(int *)op->value;
			break;
		case OPT_VALUE_INT:
			*(int *)op->value = atoi(optarg);
			break;
		case OPT_VALUE_LONG:
			*(long *)op->value = atol(optarg);
			break;
		case OPT_VALUE_FLOAT:
			*(float *)op->value = atof(optarg);
			break;
		case OPT_VALUE_DOUBLE:
			*(double *)op->value = atof(optarg);
			break;
		case OPT_VALUE_STRING:
			*(char **)op->value = optarg;
			break;
		default:
			fprintf(stderr, "%s: option '%c' has bad type %d\n",
			        argv[0], op->option, op->type);
			return -1;
		}
	}
	return optind;
}

#define WRAP() do { \
	pos = start; \
	printf("%*s", pos, ""); \
} while (0)

int printopts(int argc, char **argv, const struct opts *opts)
{
	size_t indent = 0;
	const struct opt *op;
	size_t n;
	char *cp, *cp1;
	int termwidth = 72; /* XXX constant */
	int pos, start;
	
	for (op = opts->opts; op->option > 0; ++op) {
		if (!op->valuename) continue;
		n = strlen(op->valuename);
		if (n > indent) indent = n;
	}
	if (indent > 0) ++indent;
	printf("Usage: %s %s\n", argv[0], opts->synopsis);
	for (op = opts->opts; op->option > 0; ++op) {
		printf("  -%c %-*s ", op->option, (int)indent,
		       op->valuename ? : "");
#if 0
		printf("%s\n", op->description);
#else
		/*
		 * word-wrap the description on the right side
		 * 
		 * this should work even when the first word on a line is too
		 * long for the term width
		 * 
		 * if there are multiple consecutive spaces, preserve them
		 * unless wrapping to the next line
		 */
		cp = op->description;
		pos = start = indent + 6;
		for (;;) {
			while (*cp == ' ' || *cp == '\n') {
				putchar(*cp);
				++pos;
				if (*cp == '\n') {
					++cp;
					WRAP();
				} else {
					++cp;
				}
			}
			while (*cp != ' ' && *cp != '\n' && *cp) {
				putchar(*cp);
				++pos;
				++cp;
			}
			if (!*cp) break;
			
			/* test the next word */
			cp1 = cp;
			while (*cp1 == ' ') ++cp1;
			while (*cp1 != ' ' && *cp1) ++cp1;
			if (pos + cp1-cp > termwidth) {
				/* wrap */
				putchar('\n');
				/* eat spaces before next word */ \
				while (*cp == ' ') ++cp;
				WRAP();
			}
		}
		printf("\n");
#endif
	}
	return 0;
}

#ifdef TEST
int optionx, optiony, optionz, value;
char *name;
int help;
struct opts example = {
	"-hxyz -a name -b value",
	{
	{ 'h', OPT_SET, &help, NULL, "display this help message and exit" },
	{ 'x', OPT_SET, &optionx, NULL, "option x" },
	{ 'y', OPT_INC, &optiony, NULL, "increase y" },
	{ 'z', OPT_TOGGLE, &optionz, NULL, "toggle z" },
	{ 'a', OPT_VALUE_STRING, &name, "name", "set name" },
	{ 'b', OPT_VALUE_INT, &value, "value", "set value" },
	{ -1, 0, 0, 0, 0 },
	}
};

int main(int argc, char *argv[])
{
	int n;
	n = getopts(argc, argv, &example);
	if (n < 0) {
		printopts(argc, argv, &example);
		return 1;
	}
	if (help)
		printopts(argc, argv, &example);
	return 0;
}
#endif

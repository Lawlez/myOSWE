#ifndef _OPTS_H_
#define _OPTS_H_

enum opttype {
	OPT_SET,
	OPT_RESET,
	OPT_TOGGLE,
	OPT_INC,
	OPT_INCREMENT = OPT_INC,
	OPT_DEC,
	OPT_DECREMENT = OPT_DEC,
	
	OPT_VALUES,
	OPT_VALUE_INT = OPT_VALUES,
	OPT_VALUE_LONG,
	OPT_VALUE_FLOAT,
	OPT_VALUE_DOUBLE,
	OPT_VALUE_STRING,
};

struct opt {
	int option;
	enum opttype type;
	void *value;
	char *valuename;
	char *description;
};

struct opts {
	char *synopsis;
	struct opt opts[];
};

int getopts(int argc, char **argv, const struct opts *opts);
/* printopts = show usage */
int printopts(int argc, char **argv, const struct opts *opts);

#ifdef EXAMPLE
int optionx, optiony, optionz, value;
char *name;
struct opts example = {
	"-xyz -a name -b value",
	{
	{ 'x', OPT_SET, &optionx, NULL, "option x" },
	{ 'y', OPT_INC, &optiony, NULL, "increase y" },
	{ 'z', OPT_TOGGLE, &optionz, NULL, "toggle z" },
	{ 'a', OPT_VALUE_STRING, &name, "name", "set name" },
	{ 'b', OPT_VALUE_INT, &value, "value", "set value" },
	{ -1, 0, 0, 0, 0 },
	}
};
#endif

#endif
